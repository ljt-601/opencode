#!/usr/bin/env python3
"""
微信公众号草稿箱操作
支持创建、更新草稿，上传素材等
"""

import requests
import json
import os
import time
from typing import Dict, List, Optional
from wechat_auth import WeChatAuth


class WeChatDraft:
    """微信公众号草稿箱管理"""

    def __init__(self, auth: WeChatAuth):
        """
        初始化草稿箱管理

        Args:
            auth: 微信认证实例
        """
        self.auth = auth
        self.base_url = "https://api.weixin.qq.com/cgi-bin"
        self.media_upload_url = f"{self.base_url}/material/add_material"
        self.draft_add_url = f"{self.base_url}/draft/add"
        self.draft_update_url = f"{self.base_url}/draft/update"

    def upload_image(self, image_path: str, image_type: str = "thumb") -> Dict[str, str]:
        """
        上传图片素材

        Args:
            image_path: 图片文件路径
            image_type: 素材类型（thumb: 缩略图, image: 图片）

        Returns:
            包含 media_id 和 url 的字典，失败返回空字典

        Raises:
            Exception: 上传失败时抛出异常
        """
        if not os.path.exists(image_path):
            raise Exception(f"图片文件不存在: {image_path}")

        token = self.auth.get_access_token()
        url = f"{self.media_upload_url}?access_token={token}&type={image_type}"

        try:
            with open(image_path, "rb") as f:
                files = {"media": f}
                response = requests.post(url, files=files, timeout=30)
                response.raise_for_status()
                data = response.json()

                if "media_id" in data:
                    result = {
                        "media_id": data["media_id"]
                    }
                    # 如果返回了 URL，也保存起来
                    if "url" in data:
                        result["url"] = data["url"]
                    return result
                else:
                    error_msg = data.get("errmsg", "未知错误")
                    error_code = data.get("errcode", "N/A")
                    raise Exception(f"上传图片失败: [{error_code}] {error_msg}")

        except requests.exceptions.RequestException as e:
            raise Exception(f"网络请求失败: {str(e)}")

    def upload_image_from_url(self, image_url: str, save_path: str, image_type: str = "thumb") -> Optional[str]:
        """
        从 URL 下载图片并上传到微信

        Args:
            image_url: 图片 URL
            save_path: 临时保存路径
            image_type: 素材类型

        Returns:
            media_id: 素材 ID
        """
        try:
            # 下载图片
            response = requests.get(image_url, timeout=30)
            response.raise_for_status()

            # 确保目录存在
            os.makedirs(os.path.dirname(save_path), exist_ok=True)

            # 保存图片
            with open(save_path, "wb") as f:
                f.write(response.content)

            # 上传到微信
            return self.upload_image(save_path, image_type)

        except Exception as e:
            raise Exception(f"从 URL 上传图片失败: {str(e)}")

    def create_draft(self, articles: List[Dict]) -> Optional[str]:
        """
        创建草稿

        Args:
            articles: 文章列表，每篇文章包含：
                - title: 标题
                - author: 作者（可选）
                - digest: 摘要（可选）
                - content: 内容（HTML 格式）
                - content_source_url: 原文链接（可选）
                - thumb_media_id: 封面图片素材 ID
                - need_open_comment: 是否打开评论（可选，默认 False）
                - only_fans_can_comment: 是否只有粉丝可以评论（可选，默认 False）

        Returns:
            media_id: 草稿的 media_id

        Raises:
            Exception: 创建失败时抛出异常
        """
        token = self.auth.get_access_token()
        url = f"{self.draft_add_url}?access_token={token}"

        payload = {
            "articles": articles
        }

        try:
            # 手动序列化 JSON，确保中文字符不被转义
            json_data = json.dumps(payload, ensure_ascii=False)
            headers = {"Content-Type": "application/json; charset=utf-8"}
            response = requests.post(url, data=json_data.encode("utf-8"), headers=headers, timeout=30)
            response.raise_for_status()
            data = response.json()

            if "media_id" in data:
                return data["media_id"]
            else:
                error_msg = data.get("errmsg", "未知错误")
                error_code = data.get("errcode", "N/A")
                raise Exception(f"创建草稿失败: [{error_code}] {error_msg}")

        except requests.exceptions.RequestException as e:
            raise Exception(f"网络请求失败: {str(e)}")

    def update_draft(self, media_id: str, index: int, article: Dict) -> bool:
        """
        更新草稿

        Args:
            media_id: 草稿 media_id
            index: 要更新的文章索引（从 0 开始）
            article: 文章内容

        Returns:
            是否成功

        Raises:
            Exception: 更新失败时抛出异常
        """
        token = self.auth.get_access_token()
        url = f"{self.draft_update_url}?access_token={token}"

        payload = {
            "media_id": media_id,
            "index": index,
            "article": article
        }

        try:
            # 手动序列化 JSON，确保中文字符不被转义
            json_data = json.dumps(payload, ensure_ascii=False)
            headers = {"Content-Type": "application/json; charset=utf-8"}
            response = requests.post(url, data=json_data.encode("utf-8"), headers=headers, timeout=30)
            response.raise_for_status()
            data = response.json()

            # 判断是否成功
            errcode = data.get("errcode", 0)
            if errcode == 0:
                return True
            else:
                error_msg = data.get("errmsg", "未知错误")
                raise Exception(f"更新草稿失败: [{errcode}] {error_msg}")

        except requests.exceptions.RequestException as e:
            raise Exception(f"网络请求失败: {str(e)}")


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 3:
        print("Usage: python wechat_draft.py <app_id> <app_secret> <image_path>")
        sys.exit(1)

    app_id = sys.argv[1]
    app_secret = sys.argv[2]
    image_path = sys.argv[3] if len(sys.argv) > 3 else None

    auth = WeChatAuth(app_id, app_secret)
    draft = WeChatDraft(auth)

    if image_path:
        media_id = draft.upload_image(image_path)
        print(f"Uploaded image media_id: {media_id}")
