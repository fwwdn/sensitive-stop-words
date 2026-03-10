<div align="center">

# sensitive-stop-words

**互联网中文敏感词、停止词词库**

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)
[![GitHub stars](https://img.shields.io/github/stars/fwwdn/sensitive-stop-words.svg?style=social)](https://github.com/fwwdn/sensitive-stop-words/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/fwwdn/sensitive-stop-words.svg?style=social)](https://github.com/fwwdn/sensitive-stop-words/network/members)
[![GitHub issues](https://img.shields.io/github/issues/fwwdn/sensitive-stop-words.svg)](https://github.com/fwwdn/sensitive-stop-words/issues)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)

一个收录了互联网常用中文敏感词和停止词的综合词库，适用于内容审核、文本过滤、搜索引擎分词、自然语言处理等场景。

[快速开始](#快速开始) · [词库概览](#词库概览) · [使用示例](#使用示例) · [参与贡献](#参与贡献)

</div>

---

## 特性

- **分类全面** — 涵盖色情、政治、广告、涉枪涉爆、违规网址等多个维度
- **通用停止词** — 包含 1,800+ 条中文通用停止词，可用于搜索引擎和 NLP 分词
- **开箱即用** — 纯文本格式，无需额外依赖，任何编程语言均可直接读取
- **持续更新** — 社区驱动，欢迎提交 PR 补充新词条
- **宽松许可** — 基于 Apache 2.0 协议，可商业使用

## 词库概览

| 文件 | 分类 | 词条数 | 格式 | 说明 |
|------|------|--------|------|------|
| `色情类.txt` | 色情 | ~300 | 逗号分隔 | 涉及色情、成人内容的敏感词 |
| `政治类.txt` | 政治 | ~325 | 逗号分隔 | 涉及政治敏感人物、事件的关键词 |
| `广告.txt` | 广告 | ~120 | 每行一词 | 广告推广、垃圾信息相关词汇 |
| `涉枪涉爆违法信息关键词.txt` | 涉枪涉爆 | ~430 | 每行一词 | 枪支弹药、爆炸物等违法信息关键词 |
| `网址.txt` | 违规网址 | ~14,500 | 每行一条 | 违规或可疑网站域名黑名单 |
| `stopword.dic` | 停止词 | ~1,890 | 每行一词 | 中文通用停止词（标点、助词、连词等） |

> **编码说明**：所有文件均采用 UTF-8 编码。

## 快速开始

### 直接下载

```bash
git clone https://github.com/fwwdn/sensitive-stop-words.git
```

### 作为 Git Submodule

```bash
git submodule add https://github.com/fwwdn/sensitive-stop-words.git data/sensitive-words
```

## 使用示例

### Python

```python
def load_words(filepath, delimiter='\n'):
    """加载词库文件"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    if delimiter == ',':
        return [w.strip() for w in content.split(',') if w.strip()]
    return [line.strip() for line in content.splitlines() if line.strip()]

# 加载停止词
stopwords = load_words('stopword.dic')

# 加载敏感词（逗号分隔格式）
porn_words = load_words('色情类.txt', delimiter=',')

# 加载敏感词（每行一词格式）
ad_words = load_words('广告.txt')

# 文本过滤示例
def contains_sensitive(text, word_list):
    """检测文本是否包含敏感词"""
    return [w for w in word_list if w in text]

result = contains_sensitive("这是一段测试文本", ad_words)
if result:
    print(f"检测到敏感词: {result}")
```

### Java

```java
import java.io.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.util.*;
import java.util.stream.*;

public class SensitiveWordFilter {

    public static Set<String> loadWords(String path) throws IOException {
        return Files.lines(Paths.get(path), StandardCharsets.UTF_8)
                .map(String::trim)
                .filter(s -> !s.isEmpty())
                .collect(Collectors.toSet());
    }

    public static Set<String> loadCommaSeparated(String path) throws IOException {
        String content = new String(Files.readAllBytes(Paths.get(path)), StandardCharsets.UTF_8);
        return Arrays.stream(content.split(","))
                .map(String::trim)
                .filter(s -> !s.isEmpty())
                .collect(Collectors.toSet());
    }

    public static boolean containsSensitive(String text, Set<String> words) {
        return words.stream().anyMatch(text::contains);
    }
}
```

### Go

```go
package sensitive

import (
	"os"
	"strings"
)

func LoadWords(filepath string) ([]string, error) {
	data, err := os.ReadFile(filepath)
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

func ContainsSensitive(text string, words []string) []string {
	var matched []string
	for _, w := range words {
		if strings.Contains(text, w) {
			matched = append(matched, w)
		}
	}
	return matched
}
```

### Node.js

```javascript
const fs = require('fs');
const path = require('path');

function loadWords(filepath, delimiter = '\n') {
  const content = fs.readFileSync(filepath, 'utf-8');
  return content.split(delimiter)
    .map(w => w.trim())
    .filter(Boolean);
}

const stopwords = loadWords(path.join(__dirname, 'stopword.dic'));
const adWords = loadWords(path.join(__dirname, '广告.txt'));
const pornWords = loadWords(path.join(__dirname, '色情类.txt'), ',');

function containsSensitive(text, wordList) {
  return wordList.filter(w => text.includes(w));
}
```

## 项目结构

```
sensitive-stop-words/
├── 色情类.txt                     # 色情类敏感词
├── 政治类.txt                     # 政治类敏感词
├── 广告.txt                       # 广告类敏感词
├── 涉枪涉爆违法信息关键词.txt      # 涉枪涉爆类敏感词
├── 网址.txt                       # 违规网址黑名单
├── stopword.dic                   # 中文通用停止词
├── scripts/                       # 工具脚本
│   └── validate.py                # 数据验证脚本
├── examples/                      # 使用示例
│   ├── python_example.py
│   ├── java_example.java
│   └── node_example.js
├── CONTRIBUTING.md                 # 贡献指南
├── CHANGELOG.md                   # 变更日志
├── CODE_OF_CONDUCT.md             # 行为准则
├── SECURITY.md                    # 安全策略
└── LICENSE                        # Apache 2.0 许可证
```

## 常见使用场景

| 场景 | 推荐词库 | 说明 |
|------|----------|------|
| 论坛 / 社区内容审核 | 色情类 + 政治类 + 广告 | 过滤用户发布的不当内容 |
| 搜索引擎分词 | stopword.dic | 去除无意义的停止词提高搜索精度 |
| 爬虫数据清洗 | 全部词库 | 对采集数据做多维度清洗 |
| 垃圾邮件 / 短信过滤 | 广告 + 网址 | 识别推广类垃圾信息 |
| 电商评论审核 | 广告 + 色情类 | 过滤商品评论中的违规内容 |
| 新闻舆情监控 | 政治类 | 监测政治敏感话题 |

## 参与贡献

我们欢迎任何形式的贡献！无论是新增词条、修复错误还是改进文档，请参阅 [CONTRIBUTING.md](CONTRIBUTING.md) 了解详细的贡献流程。

### 快速贡献

1. Fork 本仓库
2. 创建特性分支：`git checkout -b feature/add-new-words`
3. 提交更改：`git commit -m 'feat: 新增 XX 类敏感词'`
4. 推送分支：`git push origin feature/add-new-words`
5. 创建 Pull Request

## 免责声明

本词库仅用于内容安全审核、自然语言处理等技术研究与合法用途。使用者应自行承担合规责任，本项目不对使用者的行为及后果负责。词库内容来源于互联网公开信息整理，如有侵权请及时联系删除。

## 许可证

本项目基于 [Apache License 2.0](LICENSE) 开源。

---

<div align="center">

如果这个项目对你有帮助，请点个 Star :star: 支持一下！

</div>
