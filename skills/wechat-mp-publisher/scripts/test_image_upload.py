#!/usr/bin/env python3
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from wechat_auth import WeChatAuth
from wechat_draft import WeChatDraft

import json as _json
_creds_path = os.path.expanduser("~/.config/credentials.json")
with open(_creds_path, 'r') as _f:
    _creds = _json.load(_f)
app_id = _creds["wechat"]["app_id"]
app_secret = _creds["wechat"]["app_secret"]

auth = WeChatAuth(app_id, app_secret)
draft = WeChatDraft(auth)

# 测试上传一张图片并查看返回数据
test_image = "/tmp/wechat_mp_images/minimalist_desk_pixabay_0.jpg"

print("测试上传图片并查看返回数据...")
print("=" * 60)

result = draft.upload_image(test_image, image_type="image")

print("返回数据:")
print(f"  media_id: {result.get('media_id', 'N/A')}")
print(f"  url: {result.get('url', 'N/A')}")
print()

if result.get("url"):
    print("✓ 微信返回了图片 URL")
    print(f"URL: {result['url']}")
else:
    print("✗ 微信没有返回 URL，只有 media_id")
