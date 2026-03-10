#!/usr/bin/env python3
"""
词库统计脚本

输出每个词库文件的词条数量及总计。
"""

import os

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

FILES = {
    "色情类.txt": ",",
    "政治类.txt": ",",
    "广告.txt": "\n",
    "涉枪涉爆违法信息关键词.txt": "\n",
    "网址.txt": "\n",
    "stopword.dic": "\n",
}


def count_words(filepath, delimiter):
    for enc in ("utf-8", "utf-16", "gbk"):
        try:
            with open(filepath, "r", encoding=enc) as f:
                content = f.read()
            break
        except (UnicodeDecodeError, UnicodeError):
            continue
    else:
        return -1, -1

    if delimiter == ",":
        words = [w.strip() for w in content.split(",") if w.strip()]
    else:
        words = [line.strip() for line in content.splitlines() if line.strip()]

    unique = set(words)
    return len(words), len(unique)


def main():
    total = 0
    total_unique = 0

    print(f"{'文件':<35} {'总数':>8} {'去重后':>8}")
    print("-" * 55)

    for filename, delimiter in FILES.items():
        filepath = os.path.join(REPO_ROOT, filename)
        if not os.path.exists(filepath):
            print(f"{filename:<35} {'N/A':>8} {'N/A':>8}")
            continue

        count, unique = count_words(filepath, delimiter)
        total += count
        total_unique += unique
        print(f"{filename:<35} {count:>8} {unique:>8}")

    print("-" * 55)
    print(f"{'合计':<35} {total:>8} {total_unique:>8}")


if __name__ == "__main__":
    main()
