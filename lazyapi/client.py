from httpx import Client as xClient
from httpx import AsyncClient as xAsyncClient
from lazycls import classproperty, BaseCls
from lazycls.types import *
from .config import *
from .classes import *
from .utils import convert_to_cls


class HttpClient:
    _web: xClient = None
    _async: xAsyncClient = None 
    
    @classmethod
    def createClient(cls, base_url: str = "", cfg: HttpClientCfg = None, **kwargs) -> xClient:
        """Creates a Sync httpx Client"""
        cfg = cfg or HttpClientCfg
        if 'headers' in kwargs:
            h = kwargs.pop('headers')
            if h: cfg.headers = h
        return xClient(base_url=base_url, timeout=cfg.timeout, limits=cfg.limits, headers=cfg.headers, **kwargs)
    
    @classmethod
    def createAsyncClient(cls, base_url: str = "", cfg: AsyncHttpClientCfg = None, **kwargs) -> xAsyncClient:
        """ Creates an async httpx Client"""
        cfg = cfg or AsyncHttpClientCfg
        if 'headers' in kwargs:
            h = kwargs.pop('headers')
            if h: cfg.headers = h
        return xAsyncClient(base_url=base_url, timeout=cfg.timeout, limits=cfg.limits, headers=cfg.headers, **kwargs)

    @classmethod
    def create_client(cls, *args, **kwargs): return cls.createClient(*args, **kwargs)
    
    @classmethod
    def create_async_client(cls, *args, **kwargs): return cls.createAsyncClient(*args, **kwargs)
    
    @classproperty
    def client(cls) -> xClient:
        if not HttpClient._web: HttpClient._web = HttpClient.createClient()
        return HttpClient._web
    
    @classproperty
    def asyncClient(cls) -> xAsyncClient:
        if not HttpClient._async: HttpClient._async = HttpClient.createAsyncClient()
        return HttpClient._async

    @classproperty
    def async_client(cls) -> xAsyncClient: return cls.asyncClient


class ApiClient:
    def __init__(self, base_url: str = "", headers: DictAny = {}, cfg: HttpClientCfg = None, async_cfg: AsyncHttpClientCfg = None, module_name: str = 'lazyapi', default_resp: bool = False, **kwargs):
        self.base_url = ""
        self.headers = {}
        self.cfg = None
        self.async_cfg = None
        self._module_name = None
        self._kwargs = {}
        self._web = None
        self._async = None
        self._default_mode = False
        self.set_configs(base_url = base_url, headers = headers, cfg = cfg, async_cfg = async_cfg, module_name = module_name, default_resp = default_resp, **kwargs)

    def set_configs(self, base_url: str = "", headers: DictAny = {}, cfg: HttpClientCfg = None, async_cfg: AsyncHttpClientCfg = None, module_name: str = 'lazyapi', default_resp: bool = False,  **kwargs):
        self.base_url = base_url or self.base_url
        self.headers = headers or self.headers
        self.cfg = cfg or self.cfg
        self.async_cfg = async_cfg or self.async_cfg
        self._module_name = module_name or self._module_name
        self._default_mode = default_resp or self._default_mode
        self._kwargs = kwargs or self._kwargs

    def reset_clients(self, base_url: str = "", headers: DictAny = {}, cfg: HttpClientCfg = None, async_cfg: AsyncHttpClientCfg = None, module_name: str = 'lazyapi', default_resp: bool = False,  **kwargs):
        self.set_configs(base_url = base_url, headers = headers, cfg = cfg, async_cfg = async_cfg, module_name = module_name, default_resp = default_resp, **kwargs)
        self._web = None
        self._async = None
    
    @property
    def client(self):
        if not self._web: self._web = HttpClient.createClient(base_url=self.base_url, cfg=self.cfg, headers=self.headers, **self._kwargs)
        return self._web
    
    @property
    def aclient(self):
        if not self._async: self._async = HttpClient.createAsyncClient(base_url=self.base_url, cfg=self.async_cfg, headers=self.headers, **self._kwargs)
        return self._async
    

    #############################################################################
    #                             Base REST APIs                                #
    #############################################################################
    
    def delete(self, path: str, **kwargs) -> Union[Response, HttpResponse]:
        resp = self.client.delete(url=path, **kwargs)
        if self._default_mode: return resp
        return HttpResponse(resp = resp, clientType = 'sync', method = 'delete')

    def get(self, path: str, **kwargs) -> Union[Response, HttpResponse]:
        resp = self.client.get(url=path, **kwargs)
        if self._default_mode: return resp
        return HttpResponse(resp = resp, clientType = 'sync', method = 'get')

    def head(self, path: str, **kwargs) -> Union[Response, HttpResponse]:
        resp = self.client.head(url=path, **kwargs)
        if self._default_mode: return resp
        return HttpResponse(resp = resp, clientType = 'sync', method = 'head')

    def patch(self, path: str, **kwargs) -> Union[Response, HttpResponse]:
        resp = self.client.patch(url=path, **kwargs)
        if self._default_mode: return resp
        return HttpResponse(resp = resp, clientType = 'sync', method = 'patch')

    def put(self, path: str, **kwargs) -> Union[Response, HttpResponse]:
        resp = self.client.put(url=path, **kwargs)
        if self._default_mode: return resp
        return HttpResponse(resp = resp, clientType = 'sync', method = 'put')
    
    def post(self, path: str, **kwargs) -> Union[Response, HttpResponse]:
        resp = self.client.post(url=path, **kwargs)
        if self._default_mode: return resp
        return HttpResponse(resp = resp, clientType = 'sync', method = 'post')

    #############################################################################
    #                          Async REST Methods                               #
    #############################################################################
    
    async def async_delete(self, path: str, **kwargs) -> Union[Response, HttpResponse]:
        resp = await self.aclient.delete(url=path, **kwargs)
        if self._default_mode: return resp
        return HttpResponse(resp = resp, clientType = 'async', method = 'delete')

    async def async_get(self, path: str, **kwargs) -> Union[Response, HttpResponse]:
        resp = await self.aclient.get(url=path, **kwargs)
        if self._default_mode: return resp
        return HttpResponse(resp = resp, clientType = 'async', method = 'get')
    
    async def async_head(self, path: str, **kwargs) -> Union[Response, HttpResponse]:
        resp = await self.aclient.head(url=path, **kwargs)
        if self._default_mode: return resp
        return HttpResponse(resp = resp, clientType = 'async', method = 'head')

    async def async_patch(self, path: str, **kwargs) -> Union[Response, HttpResponse]:
        resp = await self.aclient.patch(url=path, **kwargs)
        if self._default_mode: return resp
        return HttpResponse(resp = resp, clientType = 'async', method = 'patch')

    async def async_put(self, path: str, **kwargs) -> Union[Response, HttpResponse]:
        resp = await self.aclient.put(url=path, **kwargs)
        if self._default_mode: return resp
        return HttpResponse(resp = resp, clientType = 'async', method = 'put')
    
    async def async_post(self, path: str, **kwargs) -> Union[Response, HttpResponse]:
        resp = await self.aclient.post(url=path, **kwargs)
        if self._default_mode: return resp
        return HttpResponse(resp = resp, clientType = 'async', method = 'post')


    #############################################################################
    #                       Supplementary Helpful Callers                       #
    #############################################################################

    def ping(self, path: str, max_status_code: int = 300, min_status_code: int = None, **kwargs) -> bool:
        """ Returns a bool of whether response code is great/within range/less than an int
            Can be used as a health check """
        res = self.get(url=path, **kwargs)
        if min_status_code and max_status_code:
            return bool(res.status_code in range(min_status_code, max_status_code))
        if min_status_code:
            return bool(res.status_code > min_status_code)
        return bool(res.status_code < max_status_code)
    
    def get_data(self, path: str, key: str = 'data', **kwargs) -> DataType:
        """ Expects to get data in JSON. If does not get the key, returns None. """
        resp = self.get(url=path, **kwargs)
        return resp.data.get(key, None)
    
    def get_lazycls(self, path: str, key: str = 'data', **kwargs) -> Type[BaseCls]:
        """
        Expects to get data in JSON. If does not get the key, returns None.
        Returns the data from a GET request to Path as a LazyCls
        """
        data = self.get_data(path=path, key=key, **kwargs)
        if not data: return None
        return convert_to_cls(resp=data, module_name=self._module_name, base_key=key)


    #############################################################################
    #                  Async Supplementary Helpful Callers                      #
    #############################################################################

    async def async_ping(self, path: str, max_status_code: int = 300, min_status_code: int = None, **kwargs) -> bool:
        """ Returns a bool of whether response code is great/within range/less than an int
            Can be used as a health check """
        res = await self.async_get(url=path, **kwargs)
        if min_status_code and max_status_code:
            return bool(res.status_code in range(min_status_code, max_status_code))
        if min_status_code:
            return bool(res.status_code > min_status_code)
        return bool(res.status_code < max_status_code)
    
    async def async_get_data(self, path: str, key: str = 'data', **kwargs) -> DataType:
        """ Expects to get data in JSON. If does not get the key, returns None. """
        resp = await self.async_get(url=path, **kwargs)
        return resp.data.get(key, None)
    
    async def async_get_lazycls(self, path: str, key: str = 'data', **kwargs) -> Type[BaseCls]:
        """
        Expects to get data in JSON. If does not get the key, returns None.
        Returns the data from a GET request to Path as a LazyCls
        """
        data = await self.async_get_data(path=path, key=key, **kwargs)
        if not data: return None
        return convert_to_cls(resp=data, module_name=self._module_name, base_key=key)
    
    




        
APIClient = ApiClient

__all__ = [
    'HttpClient',
    'HttpResponse',
    'ApiClient',
    'APIClient',
    'Response',
    'xClient',
    'xAsyncClient'
]
