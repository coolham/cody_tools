# URL 平台识别工具

用于识别 URL 所属的平台及其访问限制。

## 功能

- 识别常见中文内容平台（微信、小红书、知乎、抖音、淘宝、京东、B站）
- 返回平台名称和是否需要登录

## 使用方法

```python
from url_utils import identify_platform

# 基本用法
platform, requires_login = identify_platform('https://mp.weixin.qq.com/s/xxxxxx')
print(f"平台: {platform}, 需要登录: {requires_login}")

# 详细信息
from url_utils import identify_platform_with_info

info = identify_platform_with_info('https://item.taobao.com/item.htm?id=123')
print(info)
# {'platform': '淘宝', 'requires_login': True, 'hostname': 'item.taobao.com', 'recognized': True}
```

## 测试

```bash
python platform_identifier.py
```
