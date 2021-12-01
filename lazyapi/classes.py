from httpx import Response
from httpx import Request as HttpRequest
from starlette.requests import Request as Request
from lazycls import BaseCls, Field
from lazycls.types import *
from lazycls.serializers import Json, Base
from lazycls.funcs import timed_cache

from .utils import convert_to_cls
from .timez import get_timestamp_utc

RequestType = TypeVar('RequestType', Dict[Any, Any], HttpRequest, Request)
JsonResponse = TypeVar('JsonResponse', Response, Union[None, int], None, Union[Response, int], Union[Dict[Any, Any], int], Dict[Any, Any], Dict[str, Any], Json.Object)
TextResponse = TypeVar('TextResponse', Response, Union[None, int], None, Union[Response, int], Union[str, int], str)
ContentResponse = TypeVar('ContentResponse', Response, Union[None, int], None, Union[Response, int], Union[bytes, int], Union[str, int], bytes, str)
AnyResponse = TypeVar('AnyResponse', Response, Union[None, int], None, Union[Response, int], Union[Any, int], Any, bytes, str, Json.Object, Json.Array)
BoolResponse = TypeVar('BoolResponse', Response, Union[bool, int], bool, Union[Response, int], Union[bool, int], bool)

ContentType = TypeVar('ContentType', str, bytes)
DataType = TypeVar('DataType', Dict[str, Any], Dict[Any, Any], List[Any], str)
DataObjType = TypeVar('DataObjType', Json.Array, Json.Object, Dict[str, Any], Dict[Any, Any], List[Any])


class HttpResponse(BaseCls):
    resp: Response
    clientType: str = 'sync'
    method: str = 'get'
    timestamp: str = Field(default_factory=get_timestamp_utc)

    @property
    def status_code(self): return self.resp.status_code
    @property
    def text(self) -> str: return self.resp.text
    @property
    def content(self) -> ContentType: return self.resp.content
    @property
    def data(self) -> DataType: return self.resp.json()
    @property
    def dataObj(self) -> DataObjType: return Json.parse(self.resp)
    @property
    def data_obj(self) -> DataObjType: return Json.parse(self.resp)
    @property
    def url(self): return self.resp.url
    @property
    def isAsync(self): return bool(self.clientType == 'async')
    @property
    def is_async(self): return bool(self.clientType == 'async')
    @property
    def isSync(self): return bool(self.clientType == 'sync')
    @property
    def is_sync(self): return bool(self.clientType == 'sync')
    @property
    def isError(self): return bool(self.status_code >= 400)
    @property
    def is_error(self): return bool(self.status_code >= 400)
    @property
    def isSuccess(self): return bool(self.status_code < 300)
    @property
    def isRedirect(self): return bool(self.status_code in range(300, 399))
    @property
    def is_redirect(self): return bool(self.status_code in range(300, 399))
    @property
    def status(self): return self.resp.status_code
    
    @property
    @timed_cache(10)
    def _valid_data(self):
        try: return self.data
        except: return None

    @property
    def dataCls(self) -> Type[BaseCls]:
        """Attempts to turn the response (if valid json/dict) to lazycls object. Returns None if not valid"""
        if not self._valid_data: return None
        return convert_to_cls(resp=self._valid_data)
    
    @property
    def dataBase64(self) -> str:
        """ Attempts to Serialize the Data into Base64(str)"""
        return Base.b64_encode(self.text)

    @property
    def dataBase64Gzip(self) -> str:
        """ Attempts to Serialize the Data into Base64(Gzip(str))"""
        return Base.b64_gzip_encode(self.text)
    
    @property
    def dataBase64Decode(self) -> str:
        """ Attempts to Deserialize the Data from Base64(bytes)"""
        return Base.b64_decode(self.content)

    @property
    def dataBase64GzipDecode(self) -> str:
        """ Attempts to Deserialize the Data from Base64(Gzip(str))"""
        return Base.b64_gzip_decode(self.content)

    @property
    def data_cls(self)-> Type[BaseCls]: return self.dataCls






__all__ = [
    'Response',
    'HttpRequest',
    'RequestType',
    'JsonResponse',
    'TextResponse',
    'ContentResponse',
    'AnyResponse',
    'BoolResponse',
    'HttpResponse',
    'ContentType',
    'DataType',
    'DataObjType'
]

    



