# Spider Test

- [catalog](https://newtrade6699.x.yupoo.com/albums)
- [other catalog](https://newtrade6699.x.yupoo.com/albums/156268944?uid=1&isSubCate=false&referrercate=3515821)

## 5-14

### I

- MySpider.start_requests: clear db
- Added one-to-many relation between HatNode and HatLeaf
- Separated out items from models
- Just confirmed we are saving nodes and leafs in db

### II

- I might have fixed the problem of adding relations between tables

## 5-18

- Fixed 302 image download problem with code:

```python
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
DEFAULT_REQUEST_HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'en',
}
DEFAULT_REQUEST_HEADERS = {
    'Referer': 'https://newtrade6699.x.yupoo.com/albums'
}

DOWNLOAD_DELAY = 0.25    # 250 ms of delay
HTTPCACHE_ENABLED = True

COOKIES_ELABLED = True
```