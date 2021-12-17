import httpx
from logz import get_cls_logger
from lazycls.envs import *

get_logger = get_cls_logger('lazyapi')
logger = get_logger()

DefaultHeaders = {
    'Accept': 'application/json',
    'Content-Type': 'application/json'
}

class TimezCfg:
    desired_timezone = envToStr('TIMEZONE_DESIRED', default='America/Chicago')
    timezone_format = envToStr('TIMEZONE_FORMAT', default='%Y-%m-%dT%H:%M:%SZ')

class FastAPICfg:
    app_title = envToStr('FASTAPI_TITLE', 'LazyAPI')
    app_desc = envToStr('FASTAPI_DESC', 'Just a LazyAPI Backend')
    app_version = envToStr('FASTAPI_VERSION', 'v0.0.1')
    include_middleware = envToBool('FASTAPI_MIDDLEWARE', 'true')
    allow_origins = envToList('FASTAPI_ALLOW_ORIGINS', default=["*"])
    allow_methods = envToList('FASTAPI_ALLOW_METHODS', default=["*"])
    allow_headers = envToList('FASTAPI_ALLOW_HEADERS', default=["*"])
    allow_credentials = envToBool('FASTAPI_ALLOW_CREDENTIALS', 'true')


class HttpCfg:
    timeout = envToFloat('HTTPX_TIMEOUT', 30.0)
    keep_alive = envToInt('HTTPX_KEEPALIVE', 50)
    max_connect = envToInt('HTTPX_MAXCONNECT', 200)
    headers = envToDict('HTTPX_HEADERS', default=DefaultHeaders)

class HttpClientCfg:
    timeout = httpx.Timeout(HttpCfg.timeout, connect=HttpCfg.timeout)
    limits = httpx.Limits(max_keepalive_connections=HttpCfg.keep_alive, max_connections=HttpCfg.max_connect)
    headers = HttpCfg.headers

class AsyncHttpCfg:
    timeout = envToFloat('HTTPX_ASYNC_TIMEOUT', 30.0)
    keep_alive = envToInt('HTTPX_ASYNC_KEEPALIVE', 50)
    max_connect = envToInt('HTTPX_ASYNC_MAXCONNECT', 200)
    headers = envToDict('HTTPX_ASYNC_HEADERS', default=DefaultHeaders)

class AsyncHttpClientCfg:
    timeout = httpx.Timeout(AsyncHttpCfg.timeout, connect=AsyncHttpCfg.timeout)
    limits = httpx.Limits(max_keepalive_connections=AsyncHttpCfg.keep_alive, max_connections=AsyncHttpCfg.max_connect)
    headers = AsyncHttpCfg.headers


__all__ = [
    'HttpCfg',
    'HttpClientCfg',
    'AsyncHttpCfg',
    'AsyncHttpClientCfg',
    'DefaultHeaders'
]
