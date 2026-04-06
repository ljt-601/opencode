#!/usr/bin/env python3
"""
文章格式化和排版工具
支持将内容转换为微信公众号文章格式
"""

import re
from typing import Dict, Optional, List


class ArticleFormatter:
    """文章格式化器"""

    def __init__(self):
        """初始化格式化器"""
        self.templates = self._load_templates()

    def _load_templates(self) -> Dict[str, str]:
        """加载文章模板"""
        return {
            "classic": self._classic_template(),
            "modern": self._modern_template(),
            "minimal": self._minimal_template(),
            "business": self._business_template(),
            "tech_magazine": self._tech_magazine_template(),
            "vivid_fresh": self._vivid_fresh_template(),
            "dark_tech": self._dark_tech_template(),
            "future_newspaper": self._future_newspaper_template()
        }

    def _classic_template(self) -> str:
        """经典风格模板"""
        return """
<section style="padding: 20px; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;">
  <h1 style="color: #333; font-size: 24px; font-weight: bold; margin-bottom: 20px;">{title}</h1>
  <div style="color: #666; font-size: 14px; margin-bottom: 20px; border-bottom: 1px solid #eee; padding-bottom: 10px;">
    <span>作者：{author}</span>
  </div>
  <div style="line-height: 1.8; color: #333; font-size: 16px;">
    {content}
  </div>
</section>
"""

    def _modern_template(self) -> str:
        """现代风格模板"""
        return """
<section style="padding: 20px; font-family: -apple-system, BlinkMacSystemFont, 'Helvetica Neue', sans-serif;">
  <div style="text-align: center; margin-bottom: 30px;">
    <h1 style="color: #1a1a1a; font-size: 28px; font-weight: 600; letter-spacing: 1px;">{title}</h1>
    <p style="color: #999; font-size: 13px; margin-top: 10px;">{author}</p>
  </div>
  <div style="line-height: 2; color: #2c2c2c; font-size: 15px; letter-spacing: 0.5px;">
    {content}
  </div>
</section>
"""

    def _minimal_template(self) -> str:
        """极简风格模板"""
        return """
<section style="padding: 20px; font-family: Georgia, serif;">
  <h1 style="color: #000; font-size: 22px; font-weight: normal; margin-bottom: 30px;">{title}</h1>
  <div style="line-height: 1.9; color: #333; font-size: 15px;">
    {content}
  </div>
</section>
"""

    def _business_template(self) -> str:
        """商务风格模板"""
        return """
<section style="padding: 20px; font-family: 'Microsoft YaHei', sans-serif;">
  <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; margin: -20px -20px 20px -20px;">
    <h1 style="font-size: 26px; font-weight: bold; margin: 0;">{title}</h1>
    <p style="font-size: 14px; margin-top: 10px; opacity: 0.9;">{author}</p>
  </div>
  <div style="line-height: 1.8; color: #444; font-size: 16px;">
    {content}
  </div>
</section>
"""

    def _tech_magazine_template(self) -> str:
        """科技杂志风格模板 — MIT Tech Review 风格，适合 AI 热点快报"""
        return """
<section style="max-width: 100%; margin: 0 auto; padding: 0; background-color: #FFFFFF; font-family: -apple-system, BlinkMacSystemFont, 'Helvetica Neue', 'PingFang SC', 'Microsoft YaHei', 'Source Han Sans SC', sans-serif; color: #1a1a2e; line-height: 1.8; -webkit-text-size-adjust: 100%;">
  <!-- 深色杂志头部 -->
  <section style="padding: 36px 20px 28px 20px; background-color: #1a1a2e; text-align: center;">
    <p style="font-size: 11px; font-weight: 600; color: rgba(255,255,255,0.45); letter-spacing: 4px; margin: 0 0 18px 0;">TECH WEEKLY · AI 热点快报</p>
    <h1 style="font-size: 26px; font-weight: 700; color: #FFFFFF; line-height: 1.3; margin: 0 0 12px 0; letter-spacing: 1px;">{title}</h1>
    <p style="font-size: 14px; color: rgba(255,255,255,0.55); line-height: 1.6; margin: 0 0 22px 0;">{subtitle}</p>
    <div style="display: inline-block; padding: 5px 18px; border: 1px solid rgba(255,255,255,0.2); border-radius: 20px;">
      <span style="font-size: 12px; color: rgba(255,255,255,0.7); letter-spacing: 2px; font-family: 'SF Mono', 'Menlo', 'Monaco', 'Consolas', monospace;">{date}</span>
    </div>
  </section>
  <!-- 渐变色分割条 -->
  <div style="height: 4px; background: linear-gradient(to right, #E63946, #1D3557, #7B61FF);"></div>
  <!-- 正文区域 -->
  <section style="padding: 0 16px;">
    {content}
  </section>
  <!-- 页脚 -->
  <section style="padding: 28px 20px; text-align: center; background-color: #F8F9FA; margin-top: 32px;">
    <div style="height: 1px; background: linear-gradient(to right, transparent, #DEE2E6 20%, #DEE2E6 80%, transparent); margin: 0 auto 20px auto; max-width: 200px;"></div>
    <p style="font-size: 11px; color: #888899; letter-spacing: 3px; margin: 0 0 8px 0;">TECH WEEKLY</p>
    <p style="font-size: 12px; color: #AAAAAA; margin: 0 0 16px 0;">{author} · AI 驱动的科技资讯</p>
    <p style="font-size: 12px; color: #BBBBBB; margin: 0;">
      <span style="color: #E63946;">♥</span> 感谢阅读 · 点击在看分享给更多人
    </p>
  </section>
</section>
"""

    def _vivid_fresh_template(self) -> str:
        """明亮清新风格 — The Verge 风格，白底+渐变色卡片+配图"""
        return """
<section style="max-width: 100%; margin: 0 auto; padding: 0; background-color: #FFFFFF; font-family: -apple-system, BlinkMacSystemFont, 'Helvetica Neue', 'PingFang SC', 'Microsoft YaHei', sans-serif; color: #1B1B1B; line-height: 1.8; -webkit-text-size-adjust: 100%;">
  <!-- 渐变头部 -->
  <section style="padding: 40px 20px 32px 20px; background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%); text-align: center;">
    <p style="font-size: 11px; font-weight: 700; color: rgba(255,255,255,0.6); letter-spacing: 5px; margin: 0 0 16px 0;">AI NEWS WEEKLY</p>
    <h1 style="font-size: 28px; font-weight: 800; color: #FFFFFF; line-height: 1.2; margin: 0 0 10px 0; letter-spacing: 1px;">{title}</h1>
    <p style="font-size: 14px; color: rgba(255,255,255,0.7); line-height: 1.6; margin: 0 0 18px 0;">{subtitle}</p>
    <div style="display: inline-block; padding: 6px 20px; background-color: rgba(255,255,255,0.2); border-radius: 20px;">
      <span style="font-size: 13px; color: #FFFFFF; font-weight: 600; letter-spacing: 1px;">{date}</span>
    </div>
  </section>
  <!-- 正文白色区域 -->
  <section style="padding: 16px 12px 0 12px;">
    {content}
  </section>
  <!-- 页脚 -->
  <section style="padding: 28px 20px; text-align: center; margin-top: 24px;">
    <div style="height: 3px; background: linear-gradient(to right, #667eea, #764ba2, #f093fb); border-radius: 2px; max-width: 120px; margin: 0 auto 20px auto;"></div>
    <p style="font-size: 12px; font-weight: 600; color: #764ba2; letter-spacing: 2px; margin: 0 0 6px 0;">AI NEWS WEEKLY</p>
    <p style="font-size: 12px; color: #AAAAAA; margin: 0;">{author} · 由 AI 驱动的科技资讯</p>
  </section>
</section>
"""

    def _dark_tech_template(self) -> str:
        """暗夜科技风格模板 — Brutalist Luxury，GitHub Dark 风格"""
        return """
<section style="max-width: 100%; margin: 0 auto; padding: 0; background-color: #0d1117; font-family: -apple-system, BlinkMacSystemFont, 'PingFang SC', 'Microsoft YaHei', sans-serif; color: #e6edf3; line-height: 1.8; -webkit-text-size-adjust: 100%;">
  <!-- 顶部蓝色光晕线 -->
  <div style="height: 2px; background: linear-gradient(to right, transparent, #58a6ff 30%, #58a6ff 70%, transparent); box-shadow: 0 0 12px #58a6ff;"></div>
  <!-- 头部 -->
  <section style="padding: 40px 20px 32px 20px; text-align: center;">
    <p style="font-size: 11px; font-weight: 600; color: #484f58; letter-spacing: 5px; margin: 0 0 20px 0; font-family: 'SF Mono', 'Menlo', 'Monaco', 'Consolas', monospace;">TECH WEEKLY · AI 热点快报</p>
    <h1 style="font-size: 26px; font-weight: 800; color: #ffffff; line-height: 1.3; margin: 0 0 12px 0; letter-spacing: 2px;">{title}</h1>
    <p style="font-size: 13px; color: #8b949e; line-height: 1.6; margin: 0 0 22px 0;">{subtitle}</p>
    <table style="margin: 0 auto; border-collapse: collapse;"><tr><td style="padding: 5px 18px; border: 1px solid #30363d; border-radius: 20px;">
      <span style="font-size: 12px; color: #58a6ff; letter-spacing: 2px; font-family: 'SF Mono', 'Menlo', 'Monaco', 'Consolas', monospace;">{date}</span>
    </td></tr></table>
  </section>
  <div style="height: 1px; background: linear-gradient(to right, transparent, #30363d 20%, #30363d 80%, transparent);"></div>
  <section style="padding: 8px 10px 0 10px;">{content}</section>
  <section style="padding: 28px 20px; text-align: center; background-color: #010409; margin-top: 16px;">
    <div style="height: 1px; background-color: #21262d; margin: 0 auto 20px auto; max-width: 240px;"></div>
    <p style="font-size: 11px; color: #484f58; letter-spacing: 3px; margin: 0 0 8px 0; font-family: 'SF Mono', 'Menlo', 'Monaco', 'Consolas', monospace;">TECH WEEKLY</p>
    <p style="font-size: 12px; color: #6e7681; margin: 0 0 12px 0;">{author} · AI 驱动的科技资讯</p>
    <p style="font-size: 12px; color: #6e7681; margin: 0;"><span style="color: #58a6ff;">♥</span> 感谢阅读 · 点击在看分享给更多人</p>
  </section>
</section>
"""

    def _build_dark_tech_card(self, index: str, title: str, summary: str,
                              source: str = "", image_url: str = "", link: str = "") -> str:
        """暗夜科技风格卡片 — 暗色底 + 蓝色边框 + 镂空编号"""
        source_tag = ""
        if source:
            source_tag = f'''<span style="display: inline-block; font-size: 11px; color: #58a6ff; background-color: #0d2240; border: 1px solid #1a3a5c; padding: 2px 10px; border-radius: 10px; vertical-align: middle;">{source}</span>'''

        # 编号行：table 替代 flexbox
        if source:
            header_html = f'''<table style="width: 100%; margin-bottom: 12px; border-collapse: collapse;"><tr>
        <td style="width: 48px; vertical-align: top; padding: 0;">
          <div style="width: 44px; height: 44px; line-height: 40px; text-align: center; background-color: #161b22; border: 2px solid #58a6ff; border-radius: 6px; font-family: 'SF Mono', 'Menlo', 'Monaco', 'Consolas', monospace; font-size: 16px; font-weight: 700; color: #58a6ff;">{index}</div>
        </td>
        <td style="vertical-align: middle; padding: 0 0 0 12px;">{source_tag}</td>
      </tr></table>'''
        else:
            header_html = f'''<div style="margin-bottom: 12px;">
      <div style="width: 44px; height: 44px; line-height: 40px; text-align: center; background-color: #161b22; border: 2px solid #58a6ff; border-radius: 6px; font-family: 'SF Mono', 'Menlo', 'Monaco', 'Consolas', monospace; font-size: 16px; font-weight: 700; color: #58a6ff;">{index}</div>
    </div>'''

        image_section = ""
        if image_url:
            image_section = f'''<div style="width: 100%; max-height: 180px; overflow: hidden; border-radius: 6px; margin-bottom: 12px;">
      <img src="{image_url}" style="width: 100%; display: block;" alt="{title}" />
    </div>'''

        link_section = ""
        if link:
            link_section = f'''<a href="{link}" style="font-size: 13px; color: #58a6ff; text-decoration: none;">阅读详情 →</a>'''

        card = f'''<div style="position: relative; margin: 0 0 2px 0; padding: 18px 16px; background-color: #161b22; border-left: 2px solid #58a6ff; border-radius: 0 6px 6px 0;">
    {header_html}
    <p style="font-size: 16px; font-weight: 600; color: #e6edf3; line-height: 1.45; margin: 0 0 8px 0;">{title}</p>
    {image_section}
    <p style="font-size: 13px; color: #8b949e; line-height: 1.8; margin: 0 0 {('10px' if link else '0')};">{summary}</p>
    {link_section}
  </div>
  <div style="height: 6px;"></div>'''
        return card

    def _future_newspaper_template(self) -> str:
        """未来报纸风格模板 — Editorial/Newspaper，Financial Times 风格"""
        return """
<section style="max-width: 100%; margin: 0 auto; padding: 0; background-color: #fafaf9; font-family: Georgia, 'Noto Serif SC', 'Source Han Serif SC', 'STSong', serif; color: #1a1a1a; line-height: 1.8; -webkit-text-size-adjust: 100%;">
  <!-- 头部 -->
  <section style="padding: 44px 20px 28px 20px; text-align: center;">
    <p style="font-size: 11px; font-weight: 600; color: #999999; letter-spacing: 6px; margin: 0 0 18px 0; font-family: 'SF Mono', 'Menlo', 'Monaco', 'Consolas', monospace;">AI 热点快报</p>
    <h1 style="font-size: 24px; font-weight: 700; color: #1a1a1a; line-height: 1.3; margin: 0 0 16px 0; letter-spacing: 1px;">{title}</h1>
    <!-- 装饰分隔符：细线 + 圆点 + 细线 -->
    <table style="margin: 0 auto 16px auto; border-collapse: collapse;"><tr>
      <td style="padding: 0 12px 0 0;"><div style="width: 50px; height: 1px; background-color: #cccccc;"></div></td>
      <td style="padding: 0;"><span style="display: inline-block; width: 6px; height: 6px; background-color: #1a1a1a; border-radius: 50%;"></span></td>
      <td style="padding: 0 0 0 12px;"><div style="width: 50px; height: 1px; background-color: #cccccc;"></div></td>
    </tr></table>
    <p style="font-size: 13px; color: #666666; line-height: 1.6; margin: 0 0 20px 0;">{subtitle}</p>
    <table style="margin: 0 auto; border-collapse: collapse;"><tr><td style="padding: 4px 16px; background-color: #1a1a1a; border-radius: 2px;">
      <span style="font-size: 12px; color: #fafaf9; letter-spacing: 1px; font-family: 'SF Mono', 'Menlo', 'Monaco', 'Consolas', monospace;">{date}</span>
    </td></tr></table>
  </section>
  <!-- 双线分隔 -->
  <div style="padding: 0 20px;">
    <div style="height: 3px; background-color: #1a1a1a;"></div>
    <div style="height: 4px;"></div>
    <div style="height: 1px; background-color: #1a1a1a;"></div>
  </div>
  <section style="padding: 4px 16px 0 16px;">{content}</section>
  <section style="padding: 32px 20px; text-align: center; margin-top: 16px;">
    <div style="height: 2px; background-color: #1a1a1a; margin: 0 auto 20px auto;"></div>
    <p style="font-size: 12px; color: #999999; letter-spacing: 2px; margin: 0 0 6px 0;">TECH WEEKLY</p>
    <p style="font-size: 12px; color: #bbbbbb; margin: 0;">{author} · AI 驱动的科技资讯</p>
  </section>
</section>
"""

    def _build_future_newspaper_card(self, index: str, title: str, summary: str,
                                     source: str = "", image_url: str = "", link: str = "") -> str:
        """未来报纸风格卡片 — 衬线体 + 水印编号 + 干净线条"""
        source_tag = ""
        if source:
            source_tag = f'''<span style="font-size: 11px; color: #999999; font-family: 'SF Mono', 'Menlo', 'Monaco', 'Consolas', monospace;">· {source}</span>'''

        image_section = ""
        if image_url:
            image_section = f'''<div style="width: 100%; max-height: 200px; overflow: hidden; margin: 10px 0 14px 0; border: 1px solid #e5e5e0;">
      <img src="{image_url}" style="width: 100%; display: block;" alt="{title}" />
    </div>'''

        link_section = ""
        if link:
            link_section = f'''<a href="{link}" style="font-size: 13px; color: #1a1a1a; text-decoration: underline;">阅读详情 →</a>'''

        card = f'''<div style="position: relative; padding: 20px 4px 16px 4px;">
    <span style="position: absolute; top: -4px; right: 8px; font-family: Georgia, 'Noto Serif SC', serif; font-size: 72px; font-weight: 900; color: #f0f0ec; line-height: 1;">{index}</span>
    <div style="position: relative;">
      {source_tag}
      <p style="font-size: 17px; font-weight: 700; color: #1a1a1a; line-height: 1.4; margin: 4px 0 8px 0;">{title}</p>
      {image_section}
      <p style="font-size: 13px; color: #555555; line-height: 1.9; margin: 0 0 {('10px' if link else '0')};">{summary}</p>
      {link_section}
    </div>
  </div>
  <div style="padding: 0 4px;"><div style="height: 1px; background-color: #e5e5e0;"></div></div>'''
        return card

    def format_news_brief(self, news_items: list, date: str = "", subtitle: str = "",
                         author: str = "AI 编辑部", template: str = "tech_magazine") -> dict:
        """
        将资讯列表格式化为科技杂志风 Top 10 快报

        Args:
            news_items: 资讯列表，每项包含：
                - title: 新闻标题
                - summary: 2-3 句摘要
                - source: 来源标签（如 "HackerNews", "Reddit"）
                - image_url: 配图 URL（可选）
                - link: 原文链接（可选）
            date: 日期字符串（如 "2026.04.03"）
            subtitle: 副标题
            author: 作者/编辑名

        Returns:
            包含 formatted_content、digest、title 的字典
        """
        if not date:
            from datetime import datetime
            date = datetime.now().strftime("%Y.%m.%d")

        if not subtitle:
            subtitle = "48 小时内最值得关注的 AI 领域重大进展"

        article_title = "AI 热点 Top 10"

        cards_html = []
        for i, item in enumerate(news_items, 1):
            idx = f"{i:02d}"
            title_text = item.get("title", "")
            summary_text = item.get("summary", "")
            source_text = item.get("source", "")
            image_url = item.get("image_url", "")
            link = item.get("link", "")

            if template == "vivid_fresh":
                card = self._build_vivid_card(
                    index=idx, title=title_text, summary=summary_text,
                    source=source_text, image_url=image_url, link=link
                )
            else:
                card = self._build_news_card(
                    index=idx, title=title_text, summary=summary_text,
                    source=source_text, image_url=image_url, link=link
                )
            cards_html.append(card)

        content_html = "\n".join(cards_html)

        tpl = self.templates.get(template, self.templates["tech_magazine"])
        html = tpl.format(
            title=article_title,
            author=author,
            content=content_html,
            date=date,
            subtitle=subtitle
        )

        all_titles = "；".join([item.get("title", "") for item in news_items[:3]])
        digest = f"本期精选：{all_titles}..."

        return {
            "formatted_content": html,
            "digest": digest,
            "title": f"AI 热点 Top 10｜{date}"
        }

    def _build_vivid_card(self, index: str, title: str, summary: str,
                          source: str = "", image_url: str = "", link: str = "") -> str:
        """The Verge 风格的圆角卡片（白底圆角 + 渐变编号 + 内嵌配图）"""
        source_tag = ""
        if source:
            source_tag = f'''<span style="display: inline-block; font-size: 11px; font-weight: 600; color: #764ba2; background-color: #f3e8ff; padding: 2px 10px; border-radius: 10px; margin-bottom: 8px;">{source}</span>'''

        image_section = ""
        if image_url:
            image_section = f'''
        <div style="width: 100%; max-height: 180px; overflow: hidden; border-radius: 8px; margin-bottom: 12px;">
          <img src="{image_url}" style="width: 100%; display: block; border-radius: 8px;" alt="{title}" />
        </div>'''

        link_section = ""
        if link:
            link_section = f'''
        <a href="{link}" style="font-size: 13px; color: #667eea; text-decoration: none; font-weight: 500;">阅读详情 →</a>'''

        card = f'''
  <div style="margin: 0 4px 14px 4px; padding: 18px 16px; background-color: #FFFFFF; border-radius: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.06); border: 1px solid #f0f0f5;">
    <div style="display: flex; align-items: center; margin-bottom: 10px;">
      <span style="display: inline-flex; align-items: center; justify-content: center; min-width: 32px; height: 32px; border-radius: 8px; background: linear-gradient(135deg, #667eea, #764ba2); color: #FFFFFF; font-family: 'SF Mono', 'Menlo', 'Monaco', monospace; font-size: 14px; font-weight: 700; margin-right: 12px;">{index}</span>
      {source_tag}
    </div>
    {image_section}
    <p style="font-size: 16px; font-weight: 600; color: #1B1B1B; line-height: 1.45; margin: 0 0 8px 0;">{title}</p>
    <p style="font-size: 14px; color: #666666; line-height: 1.7; margin: 0 0 {('10px' if link else '0')};">{summary}</p>
    {link_section}
  </div>'''

        return card

    def _build_news_card(self, index: str, title: str, summary: str,
                         source: str = "", image_url: str = "", link: str = "") -> str:
        """
        构建单条新闻卡片（水印编号 + 左侧色条 + 可选配图）

        Args:
            index: 编号字符串（如 "01", "02"）
            title: 新闻标题
            summary: 摘要
            source: 来源标签
            image_url: 配图 URL（可选）
            link: 原文链接（可选）

        Returns:
            HTML 字符串
        """
        # 来源标签
        source_tag = ""
        if source:
            source_tag = f'''<span style="font-size: 11px; font-weight: 600; color: #888899; letter-spacing: 1.5px;">{source}</span>'''

        # 配图区域
        image_section = ""
        if image_url:
            image_section = f'''
      <div style="width: 100%; max-height: 200px; overflow: hidden; border-radius: 6px; margin-bottom: 12px;">
        <img src="{image_url}" style="width: 100%; display: block; border-radius: 6px;" alt="{title}" />
      </div>'''

        # 阅读原文链接
        link_section = ""
        if link:
            link_section = f'''
      <p style="font-size: 12px; color: #1D3557; word-break: break-all; margin: 0; padding-top: 4px;">🔗 {link}</p>'''

        card = f'''
  <!-- 新闻 #{index} -->
  <div style="position: relative; margin: 0 -16px; padding: 22px 20px 18px 20px; background-color: #F8F9FA; border-left: 3px solid #E63946;">
    <!-- 水印大号编号 -->
    <span style="position: absolute; top: 2px; right: 14px; font-family: 'SF Mono', 'Menlo', 'Monaco', 'Consolas', monospace; font-size: 64px; font-weight: 900; color: rgba(0,0,0,0.04); line-height: 1; pointer-events: none;">{index}</span>
    <!-- 内容 -->
    <div style="position: relative; z-index: 1;">
      {source_tag}
      <p style="font-size: 17px; font-weight: 600; color: #1a1a2e; line-height: 1.45; margin: 6px 0 8px 0; padding-right: 36px;">{title}</p>
      {image_section}
      <p style="font-size: 14px; color: #555566; line-height: 1.75; margin: 0 0 {('10px' if link else '0')};">{summary}</p>
      {link_section}
    </div>
  </div>
  <!-- 条目间距 -->
  <div style="height: 8px;"></div>'''

        return card

    def format_text(self, text: str) -> str:
        """
        格式化纯文本为 HTML

        Args:
            text: 纯文本内容

        Returns:
            HTML 格式内容
        """
        # 转义 HTML 特殊字符
        text = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

        # 处理段落（空行分隔）
        paragraphs = re.split(r"\n\s*\n", text.strip())
        html_paragraphs = []

        for para in paragraphs:
            para = para.strip()
            if not para:
                continue

            # 处理标题（### 开头）
            if para.startswith("###"):
                title = para[3:].strip()
                html_paragraphs.append(f'<h3 style="color: #333; font-size: 18px; font-weight: bold; margin: 20px 0 10px;">{title}</h3>')
            # 处理标题（## 开头）
            elif para.startswith("##"):
                title = para[2:].strip()
                html_paragraphs.append(f'<h2 style="color: #333; font-size: 20px; font-weight: bold; margin: 25px 0 15px;">{title}</h2>')
            # 处理列表（- 开头）
            elif para.startswith("- "):
                items = re.findall(r"^-\s+(.+)$", para, re.MULTILINE)
                if items:
                    list_items = "".join([f'<li style="margin: 5px 0;">{item}</li>' for item in items])
                    html_paragraphs.append(f'<ul style="padding-left: 20px; margin: 10px 0;">{list_items}</ul>')
            # 普通段落
            else:
                html_paragraphs.append(f'<p style="margin: 15px 0; text-align: justify;">{para}</p>')

        return "\n".join(html_paragraphs)

    def format_article(self, title: str, content: str, author: str = "", template: str = "modern") -> Dict[str, str]:
        """
        格式化文章为微信公众号格式

        Args:
            title: 文章标题
            content: 文章内容（纯文本或 HTML）
            author: 作者
            template: 模板名称（classic, modern, minimal, business）

        Returns:
            包含 formatted_content 和 digest 的字典
        """
        # 检查内容是否包含 HTML 标签（特别是 img 标签）
        has_html_tags = any(tag in content for tag in ['<img', '<div', '<section', '<p>', '<h1>', '<h2>', '<h3>'])

        # 如果内容包含 HTML 标签，直接使用；否则进行格式化
        if has_html_tags:
            formatted_content = content
        elif not content.strip().startswith("<"):
            formatted_content = self.format_text(content)
        else:
            formatted_content = content

        # 应用模板
        if template in self.templates:
            html = self.templates[template].format(
                title=title,
                author=author or "佚名",
                content=formatted_content
            )
        else:
            html = formatted_content

        # 生成摘要（取前 100 个字符）
        digest = self._generate_digest(content)

        return {
            "formatted_content": html,
            "digest": digest
        }

    def _generate_digest(self, content: str, max_length: int = 120) -> str:
        """
        生成文章摘要

        Args:
            content: 文章内容
            max_length: 最大长度

        Returns:
            摘要文本
        """
        # 移除 HTML 标签
        text = re.sub(r"<[^>]+>", "", content)
        # 移除多余空格和换行
        text = re.sub(r"\s+", " ", text).strip()

        if len(text) <= max_length:
            return text

        return text[:max_length] + "..."

    def add_highlight_box(self, content: str, color: str = "#f0f0f0") -> str:
        """
        添加高亮框

        Args:
            content: 框内内容
            color: 背景颜色

        Returns:
            HTML 代码
        """
        return f'<section style="background: {color}; padding: 15px; border-radius: 8px; margin: 15px 0;">{content}</section>'

    def add_quote(self, text: str) -> str:
        """
        添加引用样式

        Args:
            text: 引用文本

        Returns:
            HTML 代码
        """
        return f'<blockquote style="border-left: 4px solid #667eea; padding-left: 15px; margin: 20px 0; color: #666; font-style: italic;">{text}</blockquote>'


if __name__ == "__main__":
    import sys

    formatter = ArticleFormatter()

    if len(sys.argv) < 3:
        print("Usage: python article_formatter.py <title> <content>")
        sys.exit(1)

    title = sys.argv[1]
    content = sys.argv[2]

    result = formatter.format_article(title, content, "测试作者", "modern")
    print(result["formatted_content"])
