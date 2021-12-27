
from fastapi import FastAPI, Header, Depends, Body, Form, HTTPException, status, BackgroundTasks
from fastapi.responses import JSONResponse, PlainTextResponse
from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request
from lazycls.types import *
from .config import FastAPICfg


def create_fastapi(app_name: str = None, title: str = None, desc: str = None, version: str = None, include_middleware: bool = FastAPICfg.include_middleware, allow_credentials: bool = None, allow_origins: List[str] = None, allow_methods: List[str] = None, allow_headers: List[str] = None, **kwargs) -> Type[FastAPI]:
    if not title: title = FastAPICfg.app_title + (': ' + app_name if app_name else '')
    if not desc: desc = FastAPICfg.app_desc + (' ' + app_name if app_name else '')
    if not version: version = FastAPICfg.app_version
    new_fastapi_app = FastAPI(title=title, description=desc, version=version, **kwargs)
    if include_middleware:
        if allow_credentials is None: allow_credentials = FastAPICfg.allow_credentials
        if allow_origins is None: allow_origins = FastAPICfg.allow_origins
        if allow_methods is None: allow_methods = FastAPICfg.allow_methods
        if allow_headers is None: allow_headers = FastAPICfg.allow_headers
        new_fastapi_app.add_middleware(
            CORSMiddleware,
            allow_credentials=allow_credentials,
            allow_origins=allow_origins,
            allow_methods=allow_methods,
            allow_headers=allow_headers,
        )
    return new_fastapi_app


class FastAPIValidator:
    header: Header = None
    def __init__(self, key: str, alias: str = 'token'):
        self._key = key
        self._alias = alias
        self.header = Header(..., alias=self._alias)

"""
The following can be called using

validator = create_validator(key=secretapikey, alias='apikey') # or leave alias to use token

@app.post('/download', summary='returns the file to download')
async def download_file(req: DownloadRequest, background_tasks: BackgroundTasks, _ = Depends(validator)) -> FileResponse:
    ...

"""

def create_validator(key: str, alias: str = 'token') -> Type[Callable]:
    async def verify_token(token: str = Header(..., alias=alias)):
        if token == key: return True
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication credentials", headers={"WWW-Authenticate": "Bearer"})
    return verify_token


def create_multi_validator(keys: List[str], alias: str = 'token') -> Type[Callable]:
    async def verify_token(token: str = Header(..., alias=alias)):
        if token in keys: return True
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication credentials", headers={"WWW-Authenticate": "Bearer"})
    return verify_token

def create_form_validator(key: str, alias: str = 'token') -> Type[Callable]:
    async def verify_token(token: str = Form(..., alias=alias)):
        if token == key: return True
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication credentials", headers={"WWW-Authenticate": "Bearer"})
    return verify_token


def create_multi_form_validator(keys: List[str], alias: str = 'token') -> Type[Callable]:
    async def verify_token(token: str = Form(..., alias=alias)):
        if token in keys: return True
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication credentials", headers={"WWW-Authenticate": "Bearer"})
    return verify_token

def create_func_multi_validator_body(func: Callable, keys: List[str], alias: str = 'user_id', data_key: str = None, **funcKwargs) -> Type[Callable]:
    datakey = data_key or alias
    async def verify_data(data: Dict[str, Any] = Body(..., alias=alias)):
        if data.get(datakey) and func(data[datakey], **funcKwargs) in keys: return True
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication credentials", headers={"WWW-Authenticate": "Bearer"})
    return verify_data


def create_func_multi_validator_request(func: Callable, keys: List[str], alias: str = 'user_id', data_key: str = None, reqType: str = 'form', **funcKwargs) -> Type[Callable]:
    datakey = data_key or alias
    async def verify_data(req: Request = Body(..., alias=alias)):
        reqMethod = getattr(req, reqType)
        req = await reqMethod()
        if req.get(datakey) and func(req[datakey], **funcKwargs) in keys: return True
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication credentials", headers={"WWW-Authenticate": "Bearer"})
    return verify_data


__all__ = [
    'FastAPICfg',
    'create_fastapi',
    'Request',
    'PlainTextResponse',
    'JSONResponse',
    'Header',
    'Body',
    'Form',
    'Depends', 
    'HTTPException', 
    'status', 
    'BackgroundTasks',
    'create_validator',
    'create_multi_validator',
    'create_form_validator',
    'create_multi_form_validator',
    'create_func_multi_validator_body',
    'create_func_multi_validator_request',
]