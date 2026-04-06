#!/usr/bin/env python3
import requests

api_key = "os.environ.get("PIXABAY_API_KEY", "")"
url = "https://pixabay.com/api/"

# 最简单的请求
params = {
    "key": api_key,
    "q": "computer",
    "per_page": 3
}

print("Testing URL:")
print(f"{url}?key={api_key}&q=computer&per_page=3")
print()

response = requests.get(url, params=params, timeout=10)

print(f"Status Code: {response.status_code}")
print(f"Response URL: {response.url}")
print()

if response.status_code == 200:
    data = response.json()
    print(f"Found {len(data.get('hits', []))} images")
    if data.get('hits'):
        print(f"First image URL: {data['hits'][0]['webformatURL']}")
else:
    print(f"Error: {response.text}")
