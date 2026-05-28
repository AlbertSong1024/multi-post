"""Platform implementations for multi-post."""

from typing import Any, Dict, Optional

import requests
from rich.console import Console

from .core import Article, MarkdownPublisher, Platform, PublishResult

console = Console()


class JuejinPlatform(MarkdownPublisher):
    """掘金平台发布器"""

    BASE_URL = "https://api.juejin.com"

    def validate_config(self) -> bool:
        """验证掘金配置"""
        return bool(self.config.get("cookie"))

    def publish(self, article: Article) -> PublishResult:
        """发布到掘金"""
        if not self.validate_config():
            return PublishResult(
                platform="juejin",
                success=False,
                error="Missing cookie in config"
            )

        try:
            # 获取用户信息
            headers = {
                "Cookie": self.config["cookie"],
                "Content-Type": "application/json",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            }

            # 创建文章
            create_url = f"{self.BASE_URL}/content_api/v1/article/create"
            data = {
                "title": article.title,
                "content": article.content,
                "mark_content": article.content,
                "brief_content": article.summary or article.content[:100],
                "category_id": self.config.get("category_id", ""),
                "tag_ids": self.config.get("tag_ids", []),
                "cover_image": article.cover_image or "",
                "is_gfw": 0,
                "is_original": 1,
                "html_content": self.convert_markdown_to_html(article.content),
            }

            response = requests.post(create_url, json=data, headers=headers)
            result = response.json()

            if result.get("err_no") == 0:
                article_id = result["data"]["article_id"]
                url = f"https://juejin.cn/post/{article_id}"
                return PublishResult(
                    platform="juejin",
                    success=True,
                    url=url,
                    message="Published successfully"
                )
            else:
                return PublishResult(
                    platform="juejin",
                    success=False,
                    error=result.get("err_msg", "Unknown error")
                )

        except Exception as e:
            return PublishResult(platform="juejin", success=False, error=str(e))


class CSDNPlatform(MarkdownPublisher):
    """CSDN平台发布器"""

    BASE_URL = "https://bizapi.csdn.net"

    def validate_config(self) -> bool:
        """验证CSDN配置"""
        return bool(self.config.get("cookie"))

    def publish(self, article: Article) -> PublishResult:
        """发布到CSDN"""
        if not self.validate_config():
            return PublishResult(
                platform="csdn",
                success=False,
                error="Missing cookie in config"
            )

        try:
            headers = {
                "Cookie": self.config["cookie"],
                "Content-Type": "application/json",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                "Referer": "https://editor.csdn.net/"
            }

            # 创建文章
            create_url = f"{self.BASE_URL}/blog-console-api/v3/editor/saveArticle"
            data = {
                "title": article.title,
                "content": article.content,
                "markdowncontent": article.content,
                "description": article.summary or article.content[:100],
                "tags": ",".join(article.tags) if article.tags else "",
                "categories": ",".join(article.categories) if article.categories else "",
                "type": "original",
                "status": 0,  # 0=发布, 1=草稿
                "articleedittype": 1,
            }

            response = requests.post(create_url, json=data, headers=headers)
            result = response.json()

            if result.get("code") == 200:
                article_id = result["data"]["articleId"]
                url = f"https://blog.csdn.net/{self.config.get('username', '')}/article/details/{article_id}"
                return PublishResult(
                    platform="csdn",
                    success=True,
                    url=url,
                    message="Published successfully"
                )
            else:
                return PublishResult(
                    platform="csdn",
                    success=False,
                    error=result.get("msg", "Unknown error")
                )

        except Exception as e:
            return PublishResult(platform="csdn", success=False, error=str(e))


class ZhihuPlatform(MarkdownPublisher):
    """知乎平台发布器"""

    BASE_URL = "https://www.zhihu.com/api/v4"

    def validate_config(self) -> bool:
        """验证知乎配置"""
        return bool(self.config.get("cookie"))

    def publish(self, article: Article) -> PublishResult:
        """发布到知乎"""
        if not self.validate_config():
            return PublishResult(
                platform="zhihu",
                success=False,
                error="Missing cookie in config"
            )

        try:
            headers = {
                "Cookie": self.config["cookie"],
                "Content-Type": "application/json",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                "Referer": "https://zhuanlan.zhihu.com/write"
            }

            # 创建文章
            create_url = f"{self.BASE_URL}/articles"
            data = {
                "title": article.title,
                "content": self.convert_markdown_to_html(article.content),
                "delta": "",
                "reshipment_settings": {
                    "can_reshipment": True,
                    "need_credit": False
                },
                "comment_permission": "all",
            }

            response = requests.post(create_url, json=data, headers=headers)
            result = response.json()

            if "id" in result:
                url = f"https://zhuanlan.zhihu.com/p/{result['id']}"
                return PublishResult(
                    platform="zhihu",
                    success=True,
                    url=url,
                    message="Published successfully"
                )
            else:
                return PublishResult(
                    platform="zhihu",
                    success=False,
                    error=result.get("error", {}).get("message", "Unknown error")
                )

        except Exception as e:
            return PublishResult(platform="zhihu", success=False, error=str(e))


class WechatPlatform(Platform):
    """微信公众号平台发布器"""

    BASE_URL = "https://api.weixin.qq.com/cgi-bin"

    def validate_config(self) -> bool:
        """验证微信配置"""
        return bool(self.config.get("app_id") and self.config.get("app_secret"))

    def get_access_token(self) -> Optional[str]:
        """获取access_token"""
        try:
            url = f"{self.BASE_URL}/token"
            params = {
                "grant_type": "client_credential",
                "appid": self.config["app_id"],
                "secret": self.config["app_secret"],
            }
            response = requests.get(url, params=params)
            result = response.json()
            return result.get("access_token")
        except Exception:
            return None

    def publish(self, article: Article) -> PublishResult:
        """发布到微信公众号（草稿箱）"""
        if not self.validate_config():
            return PublishResult(
                platform="wechat",
                success=False,
                error="Missing app_id or app_secret in config"
            )

        try:
            access_token = self.get_access_token()
            if not access_token:
                return PublishResult(
                    platform="wechat",
                    success=False,
                    error="Failed to get access_token"
                )

            # 创建草稿
            url = f"{self.BASE_URL}/draft/add?access_token={access_token}"
            data = {
                "articles": [
                    {
                        "title": article.title,
                        "author": self.config.get("author", ""),
                        "digest": article.summary or article.content[:100],
                        "content": markdown.markdown(article.content, extensions=['extra', 'codehilite']),
                        "content_source_url": article.original_url or "",
                        "thumb_media_id": self.config.get("thumb_media_id", ""),
                        "need_open_comment": 1,
                        "only_fans_can_comment": 0,
                    }
                ]
            }

            response = requests.post(url, json=data)
            result = response.json()

            if "media_id" in result:
                return PublishResult(
                    platform="wechat",
                    success=True,
                    message=f"Draft created with media_id: {result['media_id']}"
                )
            else:
                return PublishResult(
                    platform="wechat",
                    success=False,
                    error=result.get("errmsg", "Unknown error")
                )

        except Exception as e:
            return PublishResult(platform="wechat", success=False, error=str(e))


class SegmentFaultPlatform(MarkdownPublisher):
    """思否平台发布器"""

    BASE_URL = "https://segmentfault.com/api"

    def validate_config(self) -> bool:
        """验证思否配置"""
        return bool(self.config.get("cookie"))

    def publish(self, article: Article) -> PublishResult:
        """发布到思否"""
        if not self.validate_config():
            return PublishResult(
                platform="segmentfault",
                success=False,
                error="Missing cookie in config"
            )

        try:
            headers = {
                "Cookie": self.config["cookie"],
                "Content-Type": "application/json",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                "Referer": "https://segmentfault.com/write"
            }

            # 创建文章
            create_url = f"{self.BASE_URL}/article/create"
            data = {
                "title": article.title,
                "content": article.content,
                "tags": article.tags,
            }

            response = requests.post(create_url, json=data, headers=headers)
            result = response.json()

            if result.get("status") == 0:
                article_id = result["data"]["id"]
                url = f"https://segmentfault.com/a/{article_id}"
                return PublishResult(
                    platform="segmentfault",
                    success=True,
                    url=url,
                    message="Published successfully"
                )
            else:
                return PublishResult(
                    platform="segmentfault",
                    success=False,
                    error=result.get("msg", "Unknown error")
                )

        except Exception as e:
            return PublishResult(platform="segmentfault", success=False, error=str(e))


class LocalFilePlatform(Platform):
    """本地文件平台（用于测试）"""

    def validate_config(self) -> bool:
        """验证配置"""
        return True

    def publish(self, article: Article) -> PublishResult:
        """保存到本地文件"""
        try:
            output_dir = self.config.get("output_dir", "./output")
            os.makedirs(output_dir, exist_ok=True)

            # 生成文件名
            safe_title = "".join(c for c in article.title if c.isalnum() or c in (' ', '-', '_')).strip()
            safe_title = safe_title.replace(' ', '-')
            file_path = os.path.join(output_dir, f"{safe_title}.md")

            # 写入文件
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(f"---\ntitle: {article.title}\n")
                if article.tags:
                    f.write(f"tags: {', '.join(article.tags)}\n")
                if article.summary:
                    f.write(f"summary: {article.summary}\n")
                f.write(f"---\n\n{article.content}")

            return PublishResult(
                platform="local",
                success=True,
                url=file_path,
                message=f"Saved to {file_path}"
            )

        except Exception as e:
            return PublishResult(platform="local", success=False, error=str(e))


# 平台注册表
PLATFORM_REGISTRY = {
    "juejin": JuejinPlatform,
    "csdn": CSDNPlatform,
    "zhihu": ZhihuPlatform,
    "wechat": WechatPlatform,
    "segmentfault": SegmentFaultPlatform,
    "local": LocalFilePlatform,
}
