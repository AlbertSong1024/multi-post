[English](README.md) | [中文](README_CN.md)

# 📤 multi-post

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Version](https://img.shields.io/badge/Version-1.0.0-orange.svg)]()

> 一条命令将文章发布到多个平台。支持掘金、CSDN、知乎、微信公众号、思否等平台。

## ✨ 功能特性

- 🚀 **一键发布** - 一条命令发布到多个平台
- 📝 **Markdown支持** - 原生Markdown格式，支持frontmatter元数据
- 🔌 **多平台支持** - 掘金、CSDN、知乎、微信公众号、思否
- 🎨 **格式适配** - 自动适配不同平台的格式要求
- 📊 **发布报告** - 显示每个平台的发布结果
- 🧪 **干运行模式** - 预览发布内容而不实际发布
- ⚙️ **YAML配置** - 简单的YAML配置文件
- 📦 **Pip安装** - 一键安装

## 📦 安装

### 通过PyPI安装（推荐）

```bash
pip install multi-post
```

### 从源码安装

```bash
git clone https://github.com/Alex-2Code/multi-post.git
cd multi-post
pip install -e .
```

## 🔧 配置

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

## 🚀 使用方法

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

命令:
  publish    发布文章到多个平台
  platforms  列出可用平台
  init       生成示例配置文件
  preview    预览文章内容
```

#### publish 命令

```bash
multi-post publish [OPTIONS] ARTICLE_FILE

选项:
  -c, --config TEXT     配置文件路径 (默认: multi-post.yaml)
  -p, --platforms TEXT  逗号分隔的平台列表
  --dry-run             预览模式，不实际发布
  --help                显示帮助信息
```

## 📖 使用示例

### 示例 1: 基本发布

```bash
$ multi-post publish article.md

正在加载文章: article.md
✓ 文章加载成功: 如何使用Python开发CLI工具
正在加载配置: multi-post.yaml
✓ 配置加载成功
平台列表: juejin, csdn, zhihu

正在发布到 juejin...
  ✓ 发布成功
  URL: https://juejin.cn/post/123456789

正在发布到 csdn...
  ✓ 发布成功
  URL: https://blog.csdn.net/user/article/details/123456789

正在发布到 zhihu...
  ✓ 发布成功
  URL: https://zhuanlan.zhihu.com/p/123456789

📤 发布结果

┌──────────┬────────┬──────────────────────────────────────────────────────────────┬─────────┐
│ 平台     │ 状态   │ URL/消息                                                     │ 错误    │
├──────────┼────────┼──────────────────────────────────────────────────────────────┼─────────┤
│ juejin   │   ✓    │ https://juejin.cn/post/123456789                            │ -       │
│ csdn     │   ✓    │ https://blog.csdn.net/user/article/details/123456789        │ -       │
│ zhihu    │   ✓    │ https://zhuanlan.zhihu.com/p/123456789                      │ -       │
└──────────┴────────┴──────────────────────────────────────────────────────────────┴─────────┘

汇总: 3个成功, 0个失败
```

### 示例 2: 指定平台发布

```bash
$ multi-post publish article.md --platforms juejin,csdn

平台列表: juejin, csdn

正在发布到 juejin...
  ✓ 发布成功
  URL: https://juejin.cn/post/123456789

正在发布到 csdn...
  ✓ 发布成功
  URL: https://blog.csdn.net/user/article/details/123456789

汇总: 2个成功, 0个失败
```

### 示例 3: 干运行模式

```bash
$ multi-post publish article.md --dry-run

干运行模式 - 不会实际发布

  将发布到: juejin
  将发布到: csdn
  将发布到: zhihu
```

### 示例 4: 预览文章

```bash
$ multi-post preview article.md

┌─────────────────────────────────────────────────────────┐
│ 文章预览                                                │
├─────────────────────────────────────────────────────────┤
│ 如何使用Python开发CLI工具                                │
│                                                         │
│ 标签: python, cli, tutorial                             │
│ 分类: 技术教程                                          │
│ 摘要: 本文介绍如何使用Python开发命令行工具...            │
│                                                         │
│ 内容预览:                                               │
│ # 如何使用Python开发CLI工具                              │
│                                                         │
│ 在日常开发中，我们经常需要编写一些命令行工具来提高...    │
└─────────────────────────────────────────────────────────┘
```

## 📝 文章格式

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

## 🔌 支持的平台

| 平台 | 状态 | 说明 |
|------|------|------|
| 掘金 | ✅ | 支持Markdown格式 |
| CSDN | ✅ | 支持Markdown格式 |
| 知乎 | ✅ | 自动转换为HTML |
| 微信公众号 | ✅ | 创建草稿箱 |
| 思否 | ✅ | 支持Markdown格式 |
| 本地文件 | ✅ | 用于测试 |

## 🤝 贡献

欢迎贡献！请随时提交Pull Request。

## 📄 许可证

本项目基于MIT许可证 - 详见 [LICENSE](LICENSE) 文件

## 📧 联系方式

- GitHub: [@Alex-2Code](https://github.com/Alex-2Code)

---

由 [Alex-2Code](https://github.com/Alex-2Code) 用 ❤️ 制作
