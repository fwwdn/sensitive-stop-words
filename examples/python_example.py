#!/usr/bin/env python3
"""
Python 使用示例

演示如何加载词库并进行简单的文本过滤。
"""

import os
import time

DATA_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def load_words(filename, delimiter="\n"):
    """加载词库文件，返回词条列表"""
    filepath = os.path.join(DATA_DIR, filename)
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    if delimiter == ",":
        return [w.strip() for w in content.split(",") if w.strip()]
    return [line.strip() for line in content.splitlines() if line.strip()]


def build_filter_set(filenames_and_delimiters):
    """合并多个词库为一个集合，用于高效查找"""
    word_set = set()
    for filename, delimiter in filenames_and_delimiters:
        words = load_words(filename, delimiter)
        word_set.update(words)
    return word_set


def check_text(text, word_set):
    """检查文本中是否包含敏感词，返回匹配列表"""
    matched = []
    for word in word_set:
        if word in text:
            matched.append(word)
    return matched


def replace_sensitive(text, word_set, mask="*"):
    """将文本中的敏感词替换为遮罩字符"""
    for word in word_set:
        if word in text:
            text = text.replace(word, mask * len(word))
    return text


def remove_stopwords(text, stopwords):
    """从分词结果中移除停止词（需配合分词器使用）"""
    return [w for w in text if w not in stopwords]


def main():
    print("加载词库...")
    start = time.time()

    sensitive_words = build_filter_set([
        ("色情类.txt", ","),
        ("政治类.txt", ","),
        ("广告.txt", "\n"),
        ("涉枪涉爆违法信息关键词.txt", "\n"),
    ])

    stopwords = set(load_words("stopword.dic"))

    elapsed = time.time() - start
    print(f"加载完成: {len(sensitive_words)} 条敏感词, {len(stopwords)} 条停止词 ({elapsed:.2f}s)\n")

    test_text = "这是一段测试文本，用于验证词库加载是否正常工作。"
    print(f"测试文本: {test_text}")

    matches = check_text(test_text, sensitive_words)
    if matches:
        print(f"发现敏感词: {matches}")
        cleaned = replace_sensitive(test_text, sensitive_words)
        print(f"过滤后: {cleaned}")
    else:
        print("未发现敏感词。")

    print("\n--- 停止词过滤示例 ---")
    sample_tokens = ["我", "喜欢", "这个", "开源", "项目", "的", "设计"]
    filtered = remove_stopwords(sample_tokens, stopwords)
    print(f"原始分词: {sample_tokens}")
    print(f"去停止词: {filtered}")


if __name__ == "__main__":
    main()
