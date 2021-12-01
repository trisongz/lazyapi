import httpx
import logging
from lazycls.envs import *

logger = logging.getLogger(name='lazyapi')

DefaultHeaders = {
    'Accept': 'application/json',
    'Content-Type': 'application/json'
}


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
