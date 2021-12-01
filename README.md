# lazyapi
 Async and Sync wrapper client around httpx, fastapi, and datetime stuff.

---

## Motivation

This library is forked from an internal project that works with a _lot_ of backend APIs, namely interacting with kubernetes's API. In certain cases, you want to use sync where async isnt suitable, but managing two seperate sync / async client can be annoying, especially when you aren't initializing from async at the start.

This project aims to solve a few problems:

- Enables both `sync` and `async` REST calls from the same client.

- Improves upon serialization/deserialization over standard `json` library by using `simdjson`.

- Enables dynamic dataclass creation from responses via `lazycls` that are based on `pydantic` `BaseModel`.

- Work with Timestamp / Datetime much quicker and simpler.

- Manipulate `response` objects as efficiently as possible.

- Wrapper functions for `fastapi` to enable quick api creation.


---

## Quickstart

```bash
pip install --upgrade lazyapi
```

```python
from lazyapi import APIClient

# Allows initialization of the client from sync call. 
# The client has both async and sync call methods.
apiclient = APIClient(
    base_url = 'https://google.com',
    headers = {},
    module_name = 'customlib',
)

# All requests will be routed through the base_url
# Sync Method
resp = apiclient.get(path='/search?...', **kwargs)

# Async Method
resp = await apiclient.async_get(path='/search?...', **kwargs)

"""
Both yield the same results, only differing in the clientType = sync | async
The underlying classes are auto-generated from Pydantic BaseModels, so anything you can do with Pydantic Models, you can do with these.

> HttpResponse(resp=<Response [301 Moved Permanently]>, clientType='sync', method='get', timestamp=datetime.datetime(2021, 12, 1, 7, 55, 10, 478544, tzinfo=datetime.timezone.utc))

class HttpResponse(BaseCls):
    resp: Response
    clientType: str = 'sync'
    method: str = 'get'
    timestamp: str = Field(default_factory=get_timestamp_utc)

DefaultHeaders = {
    'Accept': 'application/json',
    'Content-Type': 'application/json'
}

---
Client Configs from Env Variables

class HttpCfg:
    timeout = envToFloat('HTTPX_TIMEOUT', 30.0)
    keep_alive = envToInt('HTTPX_KEEPALIVE', 50)
    max_connect = envToInt('HTTPX_MAXCONNECT', 200)
    headers = envToDict('HTTPX_HEADERS', default=DefaultHeaders)

class AsyncHttpCfg:
    timeout = envToFloat('HTTPX_ASYNC_TIMEOUT', 30.0)
    keep_alive = envToInt('HTTPX_ASYNC_KEEPALIVE', 50)
    max_connect = envToInt('HTTPX_ASYNC_MAXCONNECT', 200)
    headers = envToDict('HTTPX_ASYNC_HEADERS', default=DefaultHeaders)

"""

```
---

## API Specific Features

### API Responses

Responses returned from APIClient are of `lazyapi.classes.HttpResponse` classes which wraps `httpx.response` in a `BaseModel` to do response validation, and interfacing with the response such as:

- `.is_error -> bool`

- `.is_redirect -> bool`

- `.data -> resp.json()`

- `.data_obj -> SimdJson.Object / SimdJson.Array`

- `.data_cls -> lazycls.LazyCls`

- `.timestamp -> str with utc timestamp of request`


### Time/Datetime Functions

`lazyapi.timez`: Includes a multitude of `datetime` based functions to work with timestamp / time / duration.

- `TIMEZONE_DESIRED` env to set the desired Timezone Default: `America/Chicago` 

- `TIMEZONE_FORMAT` env to set the desired Timezone parse. Default: `%Y-%m-%dT%H:%M:%SZ`

- `TimezCfg` class can be modified based on above two variables.

- `get_timestamp`: creates a `str` based timestamp using local TZ

- `get_timestamp_tz`: creates a `str` based timestamp using the desired TZ

- `get_timestamp_utc`: creates a `str` based timestamp using UTC

- `timer`: Simple `timer` function

- `dtime`: Get a `datetime` object. If no `datetime` obj is given, returns `datetime.now()`, otherwise will get the difference

- `get_dtime_secs`: converts a `datetime` object to total num secs.

- `get_dtime_str`: Converts a `datetime` object to a string. If no `datetime` obj is given, returns `datetime.now()` converted into desired `str` format

- `get_dtime_iso`: attempts to standardize a `datetime` obj from existing `tz` into an iso/desired-formatted `datetime`

- `dtime_parse`: attempts to parse a string, timestamp, etc. into a `datetime` obj

- `dtime_diff`: gets the difference between two `datetime` objects.


### FastAPI wrapper functions

Primarily used to create subapp mounts behind the primary fastapi app.

```python
from lazyapi import create_fastapi, FastAPICfg

"""
class FastAPICfg:
    app_title = envToStr('FASTAPI_TITLE', 'LazyAPI')
    app_desc = envToStr('FASTAPI_DESC', 'Just a LazyAPI Backend')
    app_version = envToStr('FASTAPI_VERSION', 'v0.0.1')
    include_middleware = envToBool('FASTAPI_MIDDLEWARE', 'true')
    allow_origins = envToList('FASTAPI_ALLOW_ORIGINS', default=["*"])
    allow_methods = envToList('FASTAPI_ALLOW_METHODS', default=["*"])
    allow_headers = envToList('FASTAPI_ALLOW_HEADERS', default=["*"])
    allow_credentials = envToBool('FASTAPI_ALLOW_CREDENTIALS', 'true')

"""
app = create_fastapiapp_name: str, title: str = None, desc: str = None, version: str = None)
subapp = create_fastapi(app_name: 'subapp')

@subapp.get('/healthz')
async def healthcheck() -> PlainTextResponse:
    return PlainTextResponse(content='ok')


app.mount('/subapp', subapp)

if __name__ == '__main__':
    import uvicorn
    uvicorn.run("main:app")

"""
Now you can expect the route at
/subapp/healthz


"""


```


