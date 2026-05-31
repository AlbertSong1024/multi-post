# 📤 multi-post

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Version](https://img.shields.io/badge/Version-1.0.0-orange.svg)]()

> Publish articles to multiple platforms with one command. 支持掘金、CSDN、知乎、微信公众号、思否等平台。

## ✨ Features

- 🚀 **一键发布** - 一条命令发布到多个平台
- 📝 **Markdown支持** - 原生Markdown格式，支持frontmatter元数据
- 🔌 **多平台支持** - 掘金、CSDN、知乎、微信公众号、思否
- 🎨 **格式适配** - 自动适配不同平台的格式要求
- 📊 **发布报告** - 显示每个平台的发布结果
- 🧪 **干运行模式** - 预览发布内容而不实际发布
- ⚙️ **YAML配置** - 简单的YAML配置文件
- 📦 **Pip安装** - 一键安装

## 📦 Installation

### From PyPI (recommended)

```bash
pip install multi-post
```

### From source

```bash
git clone https://github.com/AlbertSong1024/multi-post.git
cd multi-post
pip install -e .
```

## 🔧 Setup

### 1. 生成配置文件

```bash
multi-post init
```

这会生成 `multi-post.yaml` 配置文件。

### 2. 编辑配置文件

```yaml
# 掘金配置
juejin:
  cookie: "your_juejin_cookie_here"
  category_id: ""
  tag_ids: []

# CSDN配置
csdn:
  cookie: "your_csdn_cookie_here"
  username: "your_username"

# 知乎配置
zhihu:
  cookie: "your_zhihu_cookie_here"

# 微信公众号配置
wechat:
  app_id: "your_app_id"
  app_secret: "your_app_secret"
  author: "your_author_name"

# 思否配置
segmentfault:
  cookie: "your_segmentfault_cookie_here"

# 本地文件（用于测试）
local:
  output_dir: "./output"
```

### 3. 获取平台凭证

**掘金:**
1. 登录 [juejin.cn](https://juejin.cn)
2. 打开浏览器开发者工具 (F12)
3. 在Network标签页找到任意API请求
4. 复制Cookie值

**CSDN:**
1. 登录 [csdn.net](https://csdn.net)
2. 同样方法获取Cookie

**知乎:**
1. 登录 [zhihu.com](https://zhihu.com)
2. 同样方法获取Cookie

**微信公众号:**
1. 登录 [mp.weixin.qq.com](https://mp.weixin.qq.com)
2. 在开发 > 基本配置中获取AppID和AppSecret

**思否:**
1. 登录 [segmentfault.com](https://segmentfault.com)
2. 同样方法获取Cookie

## 🚀 Usage

### 基本用法

```bash
# 发布到所有配置的平台
multi-post publish article.md

# 发布到指定平台
multi-post publish article.md --platforms juejin,csdn

# 使用自定义配置文件
multi-post publish article.md --config my-config.yaml

# 干运行模式（预览）
multi-post publish article.md --dry-run
```

### 命令参考

```bash
multi-post [OPTIONS] COMMAND [ARGS]

Commands:
  publish    发布文章到多个平台
  platforms  列出可用平台
  init       生成示例配置文件
  preview    预览文章内容
```

#### publish 命令

```bash
multi-post publish [OPTIONS] ARTICLE_FILE

Options:
  -c, --config TEXT     配置文件路径 (default: multi-post.yaml)
  -p, --platforms TEXT  逗号分隔的平台列表
  --dry-run             预览模式，不实际发布
  --help                显示帮助信息
```

## 📖 Examples

### Example 1: 基本发布

```bash
$ multi-post publish article.md

Loading article: article.md
✓ Article loaded: 如何使用Python开发CLI工具
Loading config: multi-post.yaml
✓ Config loaded
Platforms: juejin, csdn, zhihu

Publishing to juejin...
  ✓ Published successfully
  URL: https://juejin.cn/post/123456789

Publishing to csdn...
  ✓ Published successfully
  URL: https://blog.csdn.net/user/article/details/123456789

Publishing to zhihu...
  ✓ Published successfully
  URL: https://zhuanlan.zhihu.com/p/123456789

📤 Publish Results

┌──────────┬────────┬──────────────────────────────────────────────────────────────┬─────────┐
│ Platform │ Status │ URL/Message                                                  │ Error   │
├──────────┼────────┼──────────────────────────────────────────────────────────────┼─────────┤
│ juejin   │   ✓    │ https://juejin.cn/post/123456789                            │ -       │
│ csdn     │   ✓    │ https://blog.csdn.net/user/article/details/123456789        │ -       │
│ zhihu    │   ✓    │ https://zhuanlan.zhihu.com/p/123456789                      │ -       │
└──────────┴────────┴──────────────────────────────────────────────────────────────┴─────────┘

Summary: 3 succeeded, 0 failed
```

### Example 2: 指定平台发布

```bash
$ multi-post publish article.md --platforms juejin,csdn

Platforms: juejin, csdn

Publishing to juejin...
  ✓ Published successfully
  URL: https://juejin.cn/post/123456789

Publishing to csdn...
  ✓ Published successfully
  URL: https://blog.csdn.net/user/article/details/123456789

Summary: 2 succeeded, 0 failed
```

### Example 3: 干运行模式

```bash
$ multi-post publish article.md --dry-run

DRY RUN MODE - No actual publishing

  Would publish to: juejin
  Would publish to: csdn
  Would publish to: zhihu
```

### Example 4: 预览文章

```bash
$ multi-post preview article.md

┌─────────────────────────────────────────────────────────┐
│ Article Preview                                         │
├─────────────────────────────────────────────────────────┤
│ 如何使用Python开发CLI工具                                │
│                                                         │
│ Tags: python, cli, tutorial                             │
│ Categories: 技术教程                                     │
│ Summary: 本文介绍如何使用Python开发命令行工具...          │
│                                                         │
│ Content Preview:                                        │
│ # 如何使用Python开发CLI工具                              │
│                                                         │
│ 在日常开发中，我们经常需要编写一些命令行工具来提高...     │
└─────────────────────────────────────────────────────────┘
```

## 📝 Article Format

文章使用Markdown格式，支持frontmatter元数据：

```markdown
---
title: 文章标题
summary: 文章摘要
tags: [python, tutorial, cli]
categories: [技术教程]
cover_image: https://example.com/cover.jpg
---

# 文章正文

这里是文章内容...

## 二级标题

更多内容...
```

### Frontmatter 字段

| 字段 | 类型 | 说明 |
|------|------|------|
| title | string | 文章标题（必填） |
| summary | string | 文章摘要 |
| tags | list | 标签列表 |
| categories | list | 分类列表 |
| cover_image | string | 封面图URL |

## 🔌 Supported Platforms

| 平台 | 状态 | 说明 |
|------|------|------|
| 掘金 | ✅ | 支持Markdown格式 |
| CSDN | ✅ | 支持Markdown格式 |
| 知乎 | ✅ | 自动转换为HTML |
| 微信公众号 | ✅ | 创建草稿箱 |
| 思否 | ✅ | 支持Markdown格式 |
| 本地文件 | ✅ | 用于测试 |

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'feat: add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Click](https://click.palletsprojects.com/) for the CLI framework
- [Rich](https://rich.readthedocs.io/) for beautiful terminal output
- [python-frontmatter](https://python-frontmatter.readthedocs.io/) for frontmatter parsing

## 📧 Contact

- GitHub: [@AlbertSong1024](https://github.com/AlbertSong1024)

---

Made with ❤️ by [AlbertSong1024](https://github.com/AlbertSong1024)
