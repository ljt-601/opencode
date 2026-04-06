#!/usr/bin/env python3
"""
Markdown 转微信公众号 HTML 排版器

适用于技术教程类文章，支持：
- 代码块（深色 One Dark 风格）
- 行内代码（高亮背景）
- 引用框（蓝紫色竖线）
- 表格（深色表头 + 交替行）
- H2/H3 标题（渐变装饰）
- 有序/无序列表
- 加粗/斜体
- 分割线（渐变色）

用法：
  # 命令行
  python markdown_to_wechat.py input.md output.html

  # 作为模块
  from markdown_to_wechat import markdown_to_wechat_html
  html = markdown_to_wechat_html("# Hello\\nWorld")
"""

import re
import sys
import os


def _escape(text: str) -> str:
    """转义 HTML 特殊字符"""
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def _inline(text: str) -> str:
    """处理行内元素：代码、加粗、斜体"""
    text = text.replace(
        "`([^`]+)`",
        '<code style="background:#edf2f7;color:#e53e3e;padding:2px 6px;border-radius:4px;'
        'font-family:SF Mono,Consolas,monospace;font-size:13px;">\\1</code>'
    )
    text = text.replace(
        r"\*\*(.+?)\*\*",
        '<strong style="color:#1a202c;font-weight:700;">\\1</strong>'
    )
    text = text.replace(
        r"(?<!\*)\*([^*]+?)\*(?!\*)",
        "<em>\\1</em>"
    )
    return text


def _code_block(code: str, lang: str) -> str:
    """生成代码块 HTML"""
    lang_tag = ""
    if lang:
        lang_tag = (
            f'<span style="position:absolute;top:8px;right:12px;'
            f'font-size:11px;color:#5c6370;">{_escape(lang)}</span>'
        )
    return (
        f'<section style="margin:16px 0;border-radius:8px;overflow:hidden;'
        f'position:relative;">'
        f'<section style="background:#282c34;padding:16px 18px;">'
        f'{lang_tag}'
        f'<pre style="margin:0;font-family:SF Mono,Consolas,Monaco,monospace;'
        f'font-size:13px;line-height:1.7;color:#abb2bf;white-space:pre;">'
        f'{_escape(code)}</pre></section></section>'
    )


def _h2(text: str) -> str:
    """生成 H2 标题 HTML（带渐变装饰条）"""
    text = _escape(re.sub(r"^[\d.]+\s+", "", text))
    return (
        f'<section style="margin:36px 0 20px 0;">'
        f'<section style="display:flex;align-items:center;margin-bottom:4px;">'
        f'<section style="width:4px;height:22px;'
        f'background:linear-gradient(180deg,#667eea,#764ba2);'
        f'border-radius:2px;margin-right:10px;flex-shrink:0;"></section>'
        f'<h2 style="margin:0;padding:0;font-size:20px;font-weight:bold;'
        f'color:#1a202c;line-height:1.4;">{text}</h2></section>'
        f'<section style="width:100%;height:1px;'
        f'background:linear-gradient(to right,rgba(102,126,234,0.2),transparent);'
        f'margin-top:6px;"></section></section>'
    )


def _h3(text: str) -> str:
    """生成 H3 标题 HTML（带左侧竖线）"""
    text = _escape(re.sub(r"^[\d.]+\s+", "", text))
    return (
        f'<section style="margin:24px 0 12px 0;">'
        f'<h3 style="margin:0;padding:0;font-size:17px;font-weight:bold;'
        f'color:#2d3748;line-height:1.4;border-left:3px solid #cbd5e0;'
        f'padding-left:10px;">{text}</h3></section>'
    )


def _blockquote(text: str) -> str:
    """生成引用框 HTML（蓝紫色竖线 + 浅蓝背景）"""
    return (
        f'<blockquote style="margin:16px 0;padding:12px 16px;'
        f'border-left:4px solid #667eea;background:#f0f3ff;'
        f'border-radius:0 8px 8px 0;">'
        f'<p style="margin:0;font-size:14px;color:#4a5568;line-height:1.8;'
        f'font-style:italic;">{_inline(text)}</p></blockquote>'
    )


def _table(rows: list) -> str:
    """生成表格 HTML（深色表头 + 交替行）"""
    parts = [
        '<section style="margin:16px 0;overflow-x:auto;">'
        '<table style="width:100%;border-collapse:collapse;font-size:14px;">',
        '<thead><tr style="background:#2d3748;">',
    ]
    # Header
    for cell in rows[0]:
        parts.append(
            f'<th style="padding:10px 14px;text-align:left;color:#fff;'
            f'font-weight:600;border:1px solid #e2e8f0;font-size:13px;">'
            f'{_escape(cell)}</th>'
        )
    parts.append("</tr></thead><tbody>")
    # Body rows
    for ri in range(1, len(rows)):
        bg = "#f7fafc" if ri % 2 == 0 else "#ffffff"
        parts.append(f'<tr style="background:{bg};">')
        for cell in rows[ri]:
            parts.append(
                f'<td style="padding:10px 14px;color:#4a5568;'
                f'border:1px solid #e2e8f0;font-size:13px;">'
                f'{_escape(cell)}</td>'
            )
        parts.append("</tr>")
    parts.append("</tbody></table></section>")
    return "".join(parts)


def _hr() -> str:
    """生成渐变分割线"""
    return (
        '<section style="margin:28px 0;text-align:center;">'
        '<section style="display:inline-block;width:60%;height:1px;'
        'background:linear-gradient(to right,transparent,#667eea,#764ba2,transparent);">'
        '</section></section>'
    )


def _paragraph(text: str) -> str:
    """生成段落 HTML"""
    return (
        f'<p style="margin:0 0 16px 0;line-height:1.8;font-size:15px;'
        f'color:#2d3748;letter-spacing:0.5px;">{_inline(text)}</p>'
    )


def _list_item(text: str, ordered: bool = False, index: str = "") -> str:
    """生成列表项 HTML"""
    if ordered:
        return (
            f'<p style="margin:4px 0 4px 18px;line-height:1.8;font-size:15px;'
            f'color:#2d3748;padding-left:6px;">'
            f'<span style="color:#667eea;margin-right:6px;font-weight:600;">'
            f'{index}.</span>{_inline(text)}</p>'
        )
    return (
        f'<p style="margin:4px 0 4px 18px;line-height:1.8;font-size:15px;'
        f'color:#2d3748;padding-left:6px;">'
        f'<span style="color:#667eea;margin-right:6px;">&#8226;</span>'
        f'{_inline(text)}</p>'
    )


def markdown_to_wechat_html(markdown: str) -> str:
    """
    将 Markdown 文本转为微信公众号兼容的 HTML

    Args:
        markdown: Markdown 文本

    Returns:
        完整的 HTML 字符串（含 DOCTYPE 和 body）
    """
    lines = markdown.split("\n")
    parts = []
    i = 0
    n = len(lines)
    TICK = "```"

    def is_special(line: str) -> bool:
        t = line.strip()
        if not t:
            return True
        if t.startswith("#"):
            return True
        if t.startswith(">"):
            return True
        if t.startswith(TICK):
            return True
        if re.match(r"^---+\s*$", t):
            return True
        if re.match(r"^[-*]\s+", t):
            return True
        if re.match(r"^\d+[.)]\s+", t):
            return True
        if "|" in t:
            return True  # heuristic for table rows
        return False

    while i < n:
        line = lines[i]

        # Code block
        if line.strip().startswith(TICK):
            lang = line.strip()[3:].strip()
            code_lines = []
            i += 1
            while i < n and not lines[i].strip().startswith(TICK):
                code_lines.append(lines[i])
                i += 1
            i += 1  # skip closing ```
            parts.append(_code_block("\n".join(code_lines), lang))
            continue

        # HR
        if re.match(r"^---+\s*$", line.strip()):
            parts.append(_hr())
            i += 1
            continue

        # H2
        m = re.match(r"^##\s+(.+)$", line)
        if m:
            parts.append(_h2(m.group(1)))
            i += 1
            continue

        # H3
        m = re.match(r"^###\s+(.+)$", line)
        if m:
            parts.append(_h3(m.group(1)))
            i += 1
            continue

        # H1 - skip (title handled externally)
        if line.strip().startswith("#") and not line.strip().startswith("##"):
            i += 1
            continue

        # Blockquote
        if line.strip().startswith(">"):
            quote_lines = []
            while i < n and lines[i].strip().startswith(">"):
                quote_lines.append(lines[i].strip()[1:].strip())
                i += 1
            parts.append(_blockquote(" ".join(quote_lines)))
            continue

        # Table
        if "|" in line and i + 1 < n and re.match(r"^\|[\s\-:|]+\|$", lines[i + 1].strip()):
            table_rows = []
            while i < n and "|" in lines[i]:
                if not re.match(r"^\|[\s\-:|]+\|$", lines[i].strip()):
                    table_rows.append(lines[i])
                i += 1
            if table_rows:
                rows = [
                    [c.strip() for c in r.strip().strip("|").split("|")]
                    for r in table_rows
                ]
                parts.append(_table(rows))
            continue

        # Unordered list
        m = re.match(r"^[-*]\s+(.+)$", line.strip())
        if m:
            parts.append(_list_item(m.group(1), ordered=False))
            i += 1
            continue

        # Ordered list
        m = re.match(r"^(\d+)[.)]\s+(.+)$", line.strip())
        if m:
            parts.append(_list_item(m.group(2), ordered=True, index=m.group(1)))
            i += 1
            continue

        # Empty line
        if not line.strip():
            i += 1
            continue

        # Paragraph - collect consecutive non-special lines
        para_lines = []
        while i < n and not is_special(lines[i]):
            para_lines.append(lines[i])
            i += 1
        if para_lines:
            parts.append(_paragraph(" ".join(para_lines)))
        else:
            i += 1

    body = "\n".join(parts)
    return (
        '<!DOCTYPE html>\n<html>\n<head><meta charset="utf-8"></head>\n'
        '<body style="margin:0;padding:0;background:#fff;">'
        '<section style="max-width:100%;padding:20px 16px;'
        'font-family:PingFang SC,Helvetica Neue,Microsoft YaHei,sans-serif;'
        'color:#2d3748;line-height:1.8;font-size:15px;box-sizing:border-box;">\n'
        f'{body}\n</section>\n</body>\n</html>'
    )


def convert_file(input_path: str, output_path: str) -> str:
    """
    读取 Markdown 文件并转换为 HTML

    Args:
        input_path: 输入 Markdown 文件路径
        output_path: 输出 HTML 文件路径

    Returns:
        生成的 HTML 字符串
    """
    with open(input_path, "r", encoding="utf-8") as f:
        markdown = f.read()

    html = markdown_to_wechat_html(markdown)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)

    return html


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python markdown_to_wechat.py <input.md> <output.html>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    if not os.path.exists(input_file):
        print(f"Error: file not found: {input_file}")
        sys.exit(1)

    html = convert_file(input_file, output_file)
    print(f"Done: {output_file} ({len(html)} bytes)")
