# 贡献指南

感谢你对 sensitive-stop-words 项目的关注！我们欢迎任何形式的贡献，包括但不限于：

- 新增敏感词条
- 修正已有词条中的错误
- 新增词库分类
- 改进文档
- 提交使用示例
- 报告 Bug

## 开始之前

1. 确保你已经阅读并同意遵守我们的 [行为准则](CODE_OF_CONDUCT.md)
2. 查看 [Issue 列表](https://github.com/fwwdn/sensitive-stop-words/issues)，确认你要做的事情没有被他人认领

## 贡献流程

### 1. Fork & Clone

```bash
git clone https://github.com/<your-username>/sensitive-stop-words.git
cd sensitive-stop-words
```

### 2. 创建分支

请基于 `master` 分支创建你的工作分支：

```bash
git checkout -b feature/your-feature-name
```

分支命名规范：

| 前缀 | 用途 | 示例 |
|------|------|------|
| `feature/` | 新增词条或功能 | `feature/add-gambling-words` |
| `fix/` | 修复错误 | `fix/remove-duplicates` |
| `docs/` | 文档改进 | `docs/update-readme` |

### 3. 修改内容

#### 词条格式规范

**每行一词格式**（推荐，适用于 `广告.txt`、`涉枪涉爆违法信息关键词.txt`、`stopword.dic`）：

```
词条A
词条B
词条C
```

**逗号分隔格式**（适用于 `色情类.txt`、`政治类.txt`）：

```
词条A,词条B,词条C
```

#### 词条提交规范

- **去重**：提交前请确认新增词条在目标文件中不存在
- **分类准确**：确保词条归属到正确的分类文件
- **编码统一**：所有文件使用 UTF-8 编码，不带 BOM
- **无空行**：文件末尾不留多余空行
- **无特殊字符**：词条本身不应包含多余的空格或控制字符

#### 数据验证

提交前可运行验证脚本检查数据质量：

```bash
python scripts/validate.py
```

### 4. 提交更改

请使用清晰的提交信息：

```bash
git add .
git commit -m "feat: 新增赌博类敏感词 50 条"
```

提交信息规范：

| 类型 | 说明 | 示例 |
|------|------|------|
| `feat` | 新增词条或功能 | `feat: 新增赌博类敏感词` |
| `fix` | 修复错误或去重 | `fix: 移除色情类重复词条` |
| `docs` | 文档变更 | `docs: 更新 README 使用示例` |
| `chore` | 维护性工作 | `chore: 更新 CI 配置` |

### 5. 提交 PR

```bash
git push origin feature/your-feature-name
```

然后在 GitHub 上创建 Pull Request，并：

- 简要描述你的改动内容
- 说明新增/修改了多少词条
- 如有关联的 Issue，请引用（如 `closes #123`）

## 新增分类

如果你希望新增一个词库分类（如"赌博类"、"暴力类"等），请：

1. 先创建 Issue 讨论该分类的必要性和范围
2. 获得维护者同意后，创建对应的 `.txt` 文件
3. 遵循现有的格式规范
4. 在 README 中更新词库概览表

## 问题反馈

如果你发现词库中的问题（如误判、缺失等），欢迎通过以下方式反馈：

- [创建 Issue](https://github.com/fwwdn/sensitive-stop-words/issues/new/choose)
- 直接提交 PR 修复

## 行为准则

参与本项目即表示你同意遵守我们的 [行为准则](CODE_OF_CONDUCT.md)。

---

再次感谢你的贡献！
