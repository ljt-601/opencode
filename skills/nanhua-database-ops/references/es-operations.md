# ES 操作参考

本文件提供 ES 常用操作的 Python 脚本模板。

## ES 连接配置

```python
import requests
import json

# ES连接配置
ES_CONFIG = {
    'url': 'http://121.43.56.42:9292',
    'auth': ('elastic', '<YOUR_ES_DEV_PASSWORD>')
}
```

## 1. 查询索引结构

```python
def get_index_mapping(index_name):
    """获取索引mapping结构"""
    url = f"{ES_CONFIG['url']}/{index_name}/_mapping"
    response = requests.get(url, auth=ES_CONFIG['auth'], timeout=10)
    if response.status_code == 200:
        return response.json()
    return None
```

## 2. 查询数据

```python
def search_data(index_name, size=10, query=None):
    """查询数据"""
    url = f"{ES_CONFIG['url']}/{index_name}/_search"

    # 构建查询DSL
    if query is None:
        query = {"match_all": {}}

    search_body = {
        "size": size,
        "query": query
    }

    response = requests.post(url,
                            auth=ES_CONFIG['auth'],
                            data=json.dumps(search_body),
                            headers={'Content-Type': 'application/json'},
                            timeout=10)
    return response.json()
```

## 3. 插入单条数据

```python
def insert_data(index_name, doc_id, data):
    """插入单条数据"""
    url = f"{ES_CONFIG['url']}/{index_name}/_doc/{doc_id}"

    response = requests.put(url,
                           auth=ES_CONFIG['auth'],
                           data=json.dumps(data, ensure_ascii=False),
                           headers={'Content-Type': 'application/json'},
                           timeout=10)
    return response.status_code in [200, 201]
```

## 4. 批量插入数据

```python
def bulk_insert_data(index_name, data_list):
    """批量插入数据（使用bulk API）"""
    url = f"{ES_CONFIG['url']}/_bulk"

    # 构建bulk请求数据
    bulk_data = []
    for data in data_list:
        # index操作
        bulk_data.append(json.dumps({
            "index": {
                "_index": index_name,
                "_id": data.get('id')  # 使用数据中的id字段
            }
        }, ensure_ascii=False))
        # 数据行
        bulk_data.append(json.dumps(data, ensure_ascii=False))

    # 使用换行符连接
    bulk_body = '\n'.join(bulk_data) + '\n'

    response = requests.post(url,
                            auth=ES_CONFIG['auth'],
                            data=bulk_body.encode('utf-8'),
                            headers={'Content-Type': 'application/x-ndjson'},
                            timeout=30)

    if response.status_code == 200:
        result = response.json()
        return not result.get('errors', True)
    return False
```

## 5. 更新数据

```python
def update_data(index_name, doc_id, data):
    """更新数据"""
    url = f"{ES_CONFIG['url']}/{index_name}/_update/{doc_id}"

    update_body = {
        "doc": data
    }

    response = requests.post(url,
                            auth=ES_CONFIG['auth'],
                            data=json.dumps(update_body),
                            headers={'Content-Type': 'application/json'},
                            timeout=10)
    return response.status_code in [200, 201]
```

## 6. 删除数据

```python
def delete_data(index_name, doc_id):
    """删除数据"""
    url = f"{ES_CONFIG['url']}/{index_name}/_doc/{doc_id}"

    response = requests.delete(url, auth=ES_CONFIG['auth'], timeout=10)
    return response.status_code in [200, 404]
```

## 7. 删除索引

```python
def delete_index(index_name):
    """删除索引"""
    url = f"{ES_CONFIG['url']}/{index_name}"

    response = requests.delete(url, auth=ES_CONFIG['auth'], timeout=10)
    return response.status_code in [200, 404]
```

## 8. 创建索引

```python
def create_index(index_name, mapping):
    """创建索引"""
    url = f"{ES_CONFIG['url']}/{index_name}"

    response = requests.put(url,
                           auth=ES_CONFIG['auth'],
                           data=json.dumps(mapping, ensure_ascii=False),
                           headers={'Content-Type': 'application/json'},
                           timeout=10)
    return response.status_code in [200, 201]
```

## 9. 按照实体类创建索引Mapping

```python
def create_index_from_entity(index_name):
    """
    按照EsScrmUser实体类创建索引
    参考: six-modules/six-module-es/src/main/java/com/six/es/model/EsScrmUser.java
    """
    mapping = {
        "settings": {
            "number_of_shards": 1,
            "number_of_replicas": 2,
            "index": {
                "max_result_window": 10000
            }
        },
        "mappings": {
            "properties": {
                # EsBaseModel字段
                "id": {"type": "keyword"},
                "isvalid": {"type": "keyword"},
                "createTime": {
                    "type": "date",
                    "format": "yyyy-MM-dd HH:mm:ss"
                },
                "updateTime": {
                    "type": "date",
                    "format": "yyyy-MM-dd HH:mm:ss"
                },
                # EsScrmUser字段
                "mobile": {"type": "keyword"},
                "tag": {
                    "type": "text",
                    "analyzer": "ik_max_word"
                },
                "origin": {"type": "keyword"},
                "registerTime": {
                    "type": "date",
                    "format": "yyyy-MM-dd HH:mm:ss"
                },
                "sourceCreateTime": {
                    "type": "date",
                    "format": "yyyy-MM-dd HH:mm:ss"
                },
                "type": {"type": "keyword"}
            }
        }
    }

    return create_index(index_name, mapping)
```

## 10. 生成测试数据

```python
import random
from datetime import datetime, timedelta

def generate_scrm_user_test_data(count=20):
    """生成SCRM用户测试数据（按照EsScrmUser字段）"""

    mobile_prefixes = ['130', '131', '132', '133', '135', '136', '137', '138', '139',
                       '150', '151', '152', '153', '155', '156', '157', '158', '159',
                       '180', '181', '182', '183', '185', '186', '187', '188', '189']

    origins = ['APP', 'H5', '小程序', '微信', '线下', '推广', '活动', '转介绍', '官网', '其他']
    types = ['7', '30', '60', '90', '180']
    tag_keywords = ['高价值', '活跃', '潜在', '休眠', 'VIP', '新用户', '老客户', '复购', '转化', '流失']

    test_data = []
    base_time = datetime.now()

    for i in range(1, count + 1):
        user_id = f'SCRM{i:04d}'
        mobile = f"{random.choice(mobile_prefixes)}{random.randint(10000000, 99999999)}"

        days_ago = random.randint(0, 365)
        register_time = base_time - timedelta(days=days_ago)
        source_create_time = register_time - timedelta(days=random.randint(0, 30))
        create_time = register_time
        update_time = register_time + timedelta(days=random.randint(0, min(days_ago, 30)))

        tag_count = random.randint(1, 3)
        tags = ' '.join(random.sample(tag_keywords, tag_count))

        user_data = {
            'id': user_id,
            'mobile': mobile,
            'tag': tags,
            'origin': random.choice(origins),
            'type': random.choice(types),
            'isvalid': '1',
            'registerTime': register_time.strftime('%Y-%m-%d %H:%M:%S'),
            'sourceCreateTime': source_create_time.strftime('%Y-%m-%d %H:%M:%S'),
            'createTime': create_time.strftime('%Y-%m-%d %H:%M:%S'),
            'updateTime': update_time.strftime('%Y-%m-%d %H:%M:%S')
        }

        test_data.append(user_data)

    return test_data
```

## 完整使用示例

```python
# 1. 删除并重建索引
delete_index('nh_scrm_user')
create_index_from_entity('nh_scrm_user')

# 2. 生成测试数据
test_data = generate_scrm_user_test_data(20)

# 3. 批量插入
bulk_insert_data('nh_scrm_user', test_data)

# 4. 查询验证
result = search_data('nh_scrm_user', size=10)
```

## 常用查询DSL

### 匹配查询
```python
query = {
    "match": {
        "tag": "VIP"
    }
}
```

### 精确查询
```python
query = {
    "term": {
        "origin": "APP"
    }
}
```

### 范围查询
```python
query = {
    "range": {
        "registerTime": {
            "gte": "2024-01-01 00:00:00",
            "lte": "2024-12-31 23:59:59"
        }
    }
}
```

### 组合查询
```python
query = {
    "bool": {
        "must": [
            {"term": {"isvalid": "1"}},
            {"range": {"registerTime": {"gte": "2024-01-01 00:00:00"}}}
        ]
    }
}
```

## 注意事项

1. **不要安装 elasticsearch Python库**，使用 requests 即可
2. **批量操作使用 bulk API**，性能更好
3. **日期格式**：严格按照 `yyyy-MM-dd HH:mm:ss` 格式
4. **keyword类型字段**：用于精确匹配、聚合、排序
5. **text类型字段**：用于全文搜索，支持分词
6. **数据编码**：使用 `ensure_ascii=False` 保留中文
7. **请求超时**：批量操作设置较长超时时间（30秒）
