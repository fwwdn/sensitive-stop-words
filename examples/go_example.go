package main

import (
	"fmt"
	"os"
	"path/filepath"
	"strings"
	"time"
)

// LoadWords 加载换行分隔的词库文件
func LoadWords(path string) ([]string, error) {
	data, err := os.ReadFile(path)
	if err != nil {
		return nil, err
	}
	var words []string
	for _, line := range strings.Split(string(data), "\n") {
		w := strings.TrimSpace(line)
		if w != "" {
			words = append(words, w)
		}
	}
	return words, nil
}

// LoadCommaSeparated 加载逗号分隔的词库文件
func LoadCommaSeparated(path string) ([]string, error) {
	data, err := os.ReadFile(path)
	if err != nil {
		return nil, err
	}
	var words []string
	for _, part := range strings.Split(string(data), ",") {
		w := strings.TrimSpace(part)
		if w != "" {
			words = append(words, w)
		}
	}
	return words, nil
}

// CheckText 检查文本中是否包含敏感词
func CheckText(text string, words []string) []string {
	var matched []string
	for _, w := range words {
		if strings.Contains(text, w) {
			matched = append(matched, w)
		}
	}
	return matched
}

// ReplaceSensitive 将敏感词替换为遮罩字符
func ReplaceSensitive(text string, words []string, mask rune) string {
	for _, w := range words {
		if strings.Contains(text, w) {
			replacement := strings.Repeat(string(mask), len([]rune(w)))
			text = strings.ReplaceAll(text, w, replacement)
		}
	}
	return text
}

func main() {
	dataDir := filepath.Join("..")

	fmt.Println("加载词库...")
	start := time.Now()

	var allWords []string
	files := []struct {
		name  string
		comma bool
	}{
		{"色情类.txt", true},
		{"政治类.txt", true},
		{"广告.txt", false},
		{"涉枪涉爆违法信息关键词.txt", false},
	}

	for _, f := range files {
		path := filepath.Join(dataDir, f.name)
		var words []string
		var err error
		if f.comma {
			words, err = LoadCommaSeparated(path)
		} else {
			words, err = LoadWords(path)
		}
		if err != nil {
			fmt.Printf("加载 %s 失败: %v\n", f.name, err)
			continue
		}
		allWords = append(allWords, words...)
	}

	stopwords, _ := LoadWords(filepath.Join(dataDir, "stopword.dic"))

	elapsed := time.Since(start)
	fmt.Printf("加载完成: %d 条敏感词, %d 条停止词 (%v)\n\n", len(allWords), len(stopwords), elapsed)

	testText := "这是一段测试文本，用于验证词库加载是否正常工作。"
	fmt.Println("测试文本:", testText)

	matches := CheckText(testText, allWords)
	if len(matches) > 0 {
		fmt.Printf("发现敏感词: %v\n", matches)
		cleaned := ReplaceSensitive(testText, allWords, '*')
		fmt.Println("过滤后:", cleaned)
	} else {
		fmt.Println("未发现敏感词。")
	}

	fmt.Println("\n--- 停止词过滤示例 ---")
	tokens := []string{"我", "喜欢", "这个", "开源", "项目", "的", "设计"}
	stopSet := make(map[string]bool)
	for _, w := range stopwords {
		stopSet[w] = true
	}
	var filtered []string
	for _, t := range tokens {
		if !stopSet[t] {
			filtered = append(filtered, t)
		}
	}
	fmt.Printf("原始分词: %v\n", tokens)
	fmt.Printf("去停止词: %v\n", filtered)
}
