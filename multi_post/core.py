"""Core functionality for publishing articles to multiple platforms."""

import os
import sys
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional

import frontmatter
import markdown
from rich.console import Console
from rich.table import Table

console = Console()


@dataclass
class Article:
    """Represents an article to be published."""
    title: str
    content: str
    summary: str = ""
    tags: List[str] = field(default_factory=list)
    categories: List[str] = field(default_factory=list)
    cover_image: Optional[str] = None
    original_url: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class PublishResult:
    """Result of publishing to a platform."""
    platform: str
    success: bool
    url: Optional[str] = None
    error: Optional[str] = None
    message: str = ""


class Platform(ABC):
    """Base class for publishing platforms."""

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.name = self.__class__.__name__

    @abstractmethod
    def publish(self, article: Article) -> PublishResult:
        """Publish an article to the platform."""
        pass

    @abstractmethod
    def validate_config(self) -> bool:
        """Validate platform configuration."""
        pass


class MarkdownPublisher(Platform):
    """Base class for platforms that accept Markdown content."""

    def convert_markdown_to_html(self, markdown_content: str) -> str:
        """Convert Markdown to HTML."""
        return markdown.markdown(
            markdown_content,
            extensions=['extra', 'codehilite', 'toc', 'tables', 'fenced_code']
        )


def load_article(file_path: str) -> Article:
    """Load article from Markdown file with frontmatter."""
    path = Path(file_path)
    if not path.exists():
        console.print(f"[red]Error: File not found: {file_path}[/red]")
        sys.exit(1)

    with open(path, 'r', encoding='utf-8') as f:
        post = frontmatter.load(f)

    # Extract frontmatter metadata
    title = post.get('title', path.stem.replace('-', ' ').title())
    summary = post.get('summary', post.get('description', ''))
    tags = post.get('tags', [])
    categories = post.get('categories', [])
    cover_image = post.get('cover_image', post.get('cover', None))

    # Convert tags/categories to list if string
    if isinstance(tags, str):
        tags = [t.strip() for t in tags.split(',')]
    if isinstance(categories, str):
        categories = [c.strip() for c in categories.split(',')]

    return Article(
        title=title,
        content=post.content,
        summary=summary,
        tags=tags,
        categories=categories,
        cover_image=cover_image,
        metadata=dict(post.metadata),
    )


def display_results(results: List[PublishResult]) -> None:
    """Display publish results in a table."""
    table = Table(title="📤 Publish Results", border_style="blue")
    table.add_column("Platform", style="bold cyan")
    table.add_column("Status", justify="center")
    table.add_column("URL/Message")
    table.add_column("Error")

    for result in results:
        status = "[green]✓[/green]" if result.success else "[red]✗[/red]"
        url_or_msg = result.url or result.message or "-"
        error = result.error or "-"

        table.add_row(result.platform, status, url_or_msg, error)

    console.print(table)


def load_config(config_path: str) -> Dict[str, Any]:
    """Load configuration from YAML file."""
    import yaml

    path = Path(config_path)
    if not path.exists():
        console.print(f"[red]Error: Config file not found: {config_path}[/red]")
        sys.exit(1)

    with open(path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


def get_platform_instance(platform_name: str, config: Dict[str, Any]) -> Optional[Platform]:
    """Get platform instance by name."""
    from .platforms import PLATFORM_REGISTRY

    platform_class = PLATFORM_REGISTRY.get(platform_name)
    if not platform_class:
        console.print(f"[yellow]Warning: Unknown platform: {platform_name}[/yellow]")
        return None

    platform_config = config.get(platform_name, {})
    return platform_class(platform_config)
