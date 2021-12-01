from httpx import Response
from httpx import Request as HttpRequest
from lazycls import BaseCls
from lazycls.types import *
from lazycls.serializers import Json


RequestType = TypeVar('RequestType', Dict[Any, Any], HttpRequest)
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

    



