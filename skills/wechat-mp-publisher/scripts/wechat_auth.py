#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
微信公众号认证和 access_token 管理
支持会话内缓存 access_token，避免频繁请求
"""

import requests
import json
import time
from typing import Optional, Dict


class WeChatAuth:
    """微信公众号认证管理器"""

    def __init__(self, app_id: str, app_secret: str):
        """
        初始化微信认证

        Args:
            app_id: 微信公众号 AppId
            app_secret: 微信公众号 AppSecret
        """
        self.app_id = app_id
        self.app_secret = app_secret
        self.access_token: Optional[str] = None
        self.expires_at: float = 0
        self.token_url = "https://api.weixin.qq.com/cgi-bin/token"

    def get_access_token(self, force_refresh: bool = False) -> str:
        """
        获取 access_token

        Args:
            force_refresh: 是否强制刷新 token

        Returns:
            access_token 字符串

        Raises:
            Exception: 获取 token 失败时抛出异常
        """
        # 检查缓存是否有效（提前 5 分钟刷新）
        if not force_refresh and self.access_token and time.time() < self.expires_at - 300:
            return self.access_token

        # 获取新的 access_token
        params = {
            "grant_type": "client_credential",
            "appid": self.app_id,
            "secret": self.app_secret
        }

        try:
            response = requests.get(self.token_url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()

            if "access_token" not in data:
                error_msg = data.get("errmsg", "未知错误")
                error_code = data.get("errcode", "N/A")
                raise Exception(f"获取 access_token 失败: [{error_code}] {error_msg}")

            token = data["access_token"]
            self.access_token = token
            self.expires_at = time.time() + data.get("expires_in", 7200)
            return token

        except requests.exceptions.RequestException as e:
            raise Exception(f"网络请求失败: {str(e)}")
        except json.JSONDecodeError as e:
            raise Exception(f"解析响应失败: {str(e)}")

    def is_authenticated(self) -> bool:
        """检查是否已认证且 token 有效"""
        return self.access_token is not None and time.time() < self.expires_at - 300


if __name__ == "__main__":
    # 测试代码
    import sys

    if len(sys.argv) < 3:
        print("Usage: python wechat_auth.py <app_id> <app_secret>")
        sys.exit(1)

    app_id = sys.argv[1]
    app_secret = sys.argv[2]

    auth = WeChatAuth(app_id, app_secret)
    token = auth.get_access_token()
    print(f"Access Token: {token}")
    print(f"Expires at: {time.ctime(auth.expires_at)}")
