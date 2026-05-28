"""CLI interface for multi-post."""

import os
import sys
from pathlib import Path

import click
from rich.console import Console
from rich.panel import Panel

from . import __version__
from .core import (
    display_results,
    get_platform_instance,
    load_article,
    load_config,
)
from .platforms import PLATFORM_REGISTRY

console = Console()


@click.group()
@click.version_option(version=__version__, prog_name="multi-post")
def cli():
    """Publish articles to multiple platforms with one command."""
    pass


@cli.command()
@click.argument("article_file")
@click.option(
    "--config", "-c",
    default="multi-post.yaml",
    help="Config file path (default: multi-post.yaml)",
)
@click.option(
    "--platforms", "-p",
    default=None,
    help="Comma-separated list of platforms (default: all in config)",
)
@click.option(
    "--dry-run",
    is_flag=True,
    help="Preview without publishing",
)
def publish(article_file: str, config: str, platforms: str, dry_run: bool):
    """Publish an article to multiple platforms.

    Examples:

        multi-post publish article.md

        multi-post publish article.md --platforms juejin,csdn

        multi-post publish article.md --config my-config.yaml
    """
    # Load article
    console.print(f"\n[bold blue]Loading article: {article_file}[/bold blue]")
    article = load_article(article_file)
    console.print(f"[green]✓ Article loaded: {article.title}[/green]")

    # Load config
    console.print(f"[bold blue]Loading config: {config}[/bold blue]")
    config_data = load_config(config)
    console.print(f"[green]✓ Config loaded[/green]")

    # Get platforms to publish
    if platforms:
        platform_list = [p.strip() for p in platforms.split(",")]
    else:
        platform_list = list(config_data.keys())

    # Filter out non-platform keys
    platform_list = [p for p in platform_list if p in PLATFORM_REGISTRY]

    if not platform_list:
        console.print("[red]Error: No valid platforms found in config[/red]")
        sys.exit(1)

    console.print(f"[bold cyan]Platforms: {', '.join(platform_list)}[/bold cyan]\n")

    # Dry run mode
    if dry_run:
        console.print("[bold yellow]DRY RUN MODE - No actual publishing[/bold yellow]\n")
        for platform_name in platform_list:
            console.print(f"  Would publish to: {platform_name}")
        return

    # Publish to each platform
    results = []
    for platform_name in platform_list:
        console.print(f"[bold green]Publishing to {platform_name}...[/bold green]")

        platform = get_platform_instance(platform_name, config_data)
        if not platform:
            continue

        result = platform.publish(article)
        results.append(result)

        if result.success:
            console.print(f"  [green]✓ {result.message or 'Success'}[/green]")
            if result.url:
                console.print(f"  [blue]URL: {result.url}[/blue]")
        else:
            console.print(f"  [red]✗ {result.error}[/red]")

    # Display results table
    console.print()
    display_results(results)

    # Summary
    success_count = sum(1 for r in results if r.success)
    fail_count = sum(1 for r in results if not r.success)
    console.print(f"\n[bold]Summary: {success_count} succeeded, {fail_count} failed[/bold]")


@cli.command()
def platforms():
    """List available platforms."""
    table_data = []
    for name, cls in PLATFORM_REGISTRY.items():
        table_data.append((name, cls.__doc__ or ""))

    console.print("\n[bold cyan]Available Platforms:[/bold cyan]")
    for name, desc in table_data:
        console.print(f"  • [bold]{name}[/bold] - {desc}")
    console.print()


@cli.command()
@click.option(
    "--output", "-o",
    default="multi-post.yaml",
    help="Output config file path (default: multi-post.yaml)",
)
def init(output: str):
    """Generate example config file."""
    example_config = """# multi-post 配置文件
# 填入各平台的认证信息

# 掘金配置
juejin:
  cookie: "your_juejin_cookie_here"
  category_id: ""  # 分类ID
  tag_ids: []  # 标签ID列表

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
  thumb_media_id: ""  # 封面图素材ID

# 思否配置
segmentfault:
  cookie: "your_segmentfault_cookie_here"

# 本地文件（用于测试）
local:
  output_dir: "./output"
"""

    if os.path.exists(output):
        console.print(f"[yellow]Warning: {output} already exists[/yellow]")
        if not click.confirm("Overwrite?"):
            return

    with open(output, 'w', encoding='utf-8') as f:
        f.write(example_config)

    console.print(f"[green]✓ Config file created: {output}[/green]")
    console.print("[dim]Edit the file to add your platform credentials[/dim]")


@cli.command()
@click.argument("article_file")
def preview(article_file: str):
    """Preview article content."""
    article = load_article(article_file)

    console.print(Panel(
        f"[bold]{article.title}[/bold]\n\n"
        f"Tags: {', '.join(article.tags) if article.tags else 'None'}\n"
        f"Categories: {', '.join(article.categories) if article.categories else 'None'}\n"
        f"Summary: {article.summary or 'None'}\n\n"
        f"Content Preview:\n{article.content[:500]}...",
        title="Article Preview",
        border_style="blue"
    ))


if __name__ == "__main__":
    cli()
