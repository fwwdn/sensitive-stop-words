#!/usr/bin/env python3
"""
词库数据验证脚本

检查项：
  - 文件编码（UTF-8）
  - 空行检测
  - 重复词条检测
  - 词条统计
"""

import os
import sys

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

LINE_SEPARATED_FILES = [
    ("广告.txt", "\n"),
    ("涉枪涉爆违法信息关键词.txt", "\n"),
    ("网址.txt", "\n"),
    ("stopword.dic", "\n"),
]

COMMA_SEPARATED_FILES = [
    ("色情类.txt", ","),
    ("政治类.txt", ","),
]

ALL_FILES = LINE_SEPARATED_FILES + COMMA_SEPARATED_FILES


def check_encoding(filepath):
    """检查文件是否为有效的 UTF-8 编码"""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            f.read()
        return True
    except UnicodeDecodeError:
        return False


def load_words(filepath, delimiter):
    """加载词条列表"""
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    if delimiter == ",":
        words = [w.strip() for w in content.split(",")]
    else:
        words = [line.strip() for line in content.splitlines()]

    return words


def find_duplicates(words):
    """查找重复词条"""
    seen = {}
    duplicates = []
    for i, w in enumerate(words):
        if not w:
            continue
        if w in seen:
            duplicates.append((w, seen[w], i))
        else:
            seen[w] = i
    return duplicates


def find_empty_entries(words):
    """查找空词条"""
    return [i for i, w in enumerate(words) if not w.strip()]


def main():
    errors = 0
    warnings = 0
    total_words = 0

    print("=" * 60)
    print("  sensitive-stop-words 数据验证")
    print("=" * 60)
    print()

    for filename, delimiter in ALL_FILES:
        filepath = os.path.join(REPO_ROOT, filename)

        if not os.path.exists(filepath):
            print(f"  [SKIP] {filename} — 文件不存在")
            continue

        print(f"  检查 {filename}")

        if not check_encoding(filepath):
            print(f"    [ERROR] 文件编码不是有效的 UTF-8")
            errors += 1
            continue

        words = load_words(filepath, delimiter)
        non_empty = [w for w in words if w]
        total_words += len(non_empty)

        # 重复检测
        duplicates = find_duplicates(words)
        if duplicates:
            print(f"    [WARN]  发现 {len(duplicates)} 个重复词条:")
            for word, first, second in duplicates[:5]:
                print(f"            '{word}' (行 {first + 1} 与 {second + 1})")
            if len(duplicates) > 5:
                print(f"            ... 还有 {len(duplicates) - 5} 个")
            warnings += len(duplicates)

        # 空条目检测
        empty = find_empty_entries(words)
        if empty:
            print(f"    [WARN]  发现 {len(empty)} 个空条目")
            warnings += len(empty)

        print(f"    [OK]    {len(non_empty)} 条有效词条")
        print()

    print("=" * 60)
    print(f"  总计: {total_words} 条词条")
    print(f"  错误: {errors}")
    print(f"  警告: {warnings}")
    print("=" * 60)

    if errors > 0:
        print("\n验证失败！请修复以上错误。")
        sys.exit(1)

    print("\n验证通过。")
    sys.exit(0)


if __name__ == "__main__":
    main()
