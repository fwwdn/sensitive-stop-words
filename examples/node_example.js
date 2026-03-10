/**
 * Node.js 使用示例
 *
 * 演示如何加载词库并进行简单的文本过滤。
 */

const fs = require('fs');
const path = require('path');

const DATA_DIR = path.dirname(__dirname);

function loadWords(filename, delimiter = '\n') {
  const filepath = path.join(DATA_DIR, filename);
  const content = fs.readFileSync(filepath, 'utf-8');

  return content.split(delimiter)
    .map(w => w.trim())
    .filter(Boolean);
}

function buildFilterSet(filesAndDelimiters) {
  const wordSet = new Set();
  for (const [filename, delimiter] of filesAndDelimiters) {
    const words = loadWords(filename, delimiter);
    words.forEach(w => wordSet.add(w));
  }
  return wordSet;
}

function checkText(text, wordSet) {
  const matched = [];
  for (const word of wordSet) {
    if (text.includes(word)) {
      matched.push(word);
    }
  }
  return matched;
}

function replaceSensitive(text, wordSet, mask = '*') {
  let result = text;
  for (const word of wordSet) {
    if (result.includes(word)) {
      result = result.split(word).join(mask.repeat(word.length));
    }
  }
  return result;
}

function main() {
  console.log('加载词库...');
  const start = Date.now();

  const sensitiveWords = buildFilterSet([
    ['色情类.txt', ','],
    ['政治类.txt', ','],
    ['广告.txt', '\n'],
    ['涉枪涉爆违法信息关键词.txt', '\n'],
  ]);

  const stopwords = new Set(loadWords('stopword.dic'));

  const elapsed = Date.now() - start;
  console.log(`加载完成: ${sensitiveWords.size} 条敏感词, ${stopwords.size} 条停止词 (${elapsed}ms)\n`);

  const testText = '这是一段测试文本，用于验证词库加载是否正常工作。';
  console.log(`测试文本: ${testText}`);

  const matches = checkText(testText, sensitiveWords);
  if (matches.length > 0) {
    console.log(`发现敏感词: ${matches.join(', ')}`);
    const cleaned = replaceSensitive(testText, sensitiveWords);
    console.log(`过滤后: ${cleaned}`);
  } else {
    console.log('未发现敏感词。');
  }

  console.log('\n--- 停止词过滤示例 ---');
  const sampleTokens = ['我', '喜欢', '这个', '开源', '项目', '的', '设计'];
  const filtered = sampleTokens.filter(w => !stopwords.has(w));
  console.log(`原始分词: ${sampleTokens.join(', ')}`);
  console.log(`去停止词: ${filtered.join(', ')}`);
}

main();
