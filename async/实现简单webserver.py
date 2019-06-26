import re,logging
from webob import Response,Request,dec,exc
from wsgiref import simple_server
logging.basicConfig(level=logging.INFO,format="%(message)s")

pattern = re.compile("/({[^{}:]+:?[^{}:]*})")
#/person/{name:str}/{id:int}
#/person/{name}/{id:int}



TYPEATTRNS = {
    "str":r'[^/]',
    "word":"r[\w+]",
    "float":r"[+-]?\d+\.\d+",  #支持传递正负数整数
    "int":"[+-]?\d+",   #支持传递正负数浮点数
    "any":"r.+"
}

TYPECAST = {
    "str":str,
    "word":str,
    "float":float,
    "int":int,
    "any":str
}



class DictObj:
    """
        将对象包装成使用点的方式来访问属性，但是有不允许别人修改属性里边的值
    """
    def __init__(self,d:dict):
        if isinstance(d,dict):
            self.__dict__["_dict"] = d
        else:
            self.__dict__["_dict"] = {}

    def __getattr__(self, item):
        return self._dict[item]

    def __setattr__(self, key, value):
        raise NotImplemented("not Implement..")


class Router:
    def __init__(self,prefix:str):
        self.__prefix = prefix.rstrip("/\\")
        self.__routertable = []  #保存三元组[(method,pattern,handler),]

    def route(self,pattern,*methods):
        def wrapper(handler):
            self.__routertable.append((methods,re.compile(pattern,re.S),handler))
            return handler
        return wrapper

    def prefix(self):
        return self.__prefix

    def get(self,pattern):
        return self.route(pattern,"GET")

    def post(self, pattern):
        return self.route(pattern, "POST")

    def head(self, pattern):
        return self.route(pattern, "HEAD")

    def delete(self, pattern):
        return self.route(pattern, "DELETE")

    def match(self,request:Request) -> Response:
        #判断是否属于这个Router实例管辖的路由prefix前缀
        if not request.path.startswith(self.__prefix):
            return None
        for methods,pattern,handler in self.__routertable:
            if not methods or request.method.upper() in methods:
                matcher = pattern.match(request.path.replace(self.__prefix,"",1))
                if matcher:
                    request.args = matcher.group()
                    #在这里包装一下我们获得的属性，但是不允许在修改
                    request.kwargs = DictObj(matcher.groupdict())
                    return handler(request)
        # raise exc.HTTPNotFound("页面没有找到")
        # return None



class Application:

    ROUTERS = []
    @classmethod
    def register(cls,router:Router):
        cls.ROUTERS.append(router)

    @dec.wsgify
    def __call__(self,request:Request):
        for router in self.ROUTERS:
            logging.info(request.path)
            response = router.match(request)
            if response:
                # 因为这里做了处理，那么在match中找不到可以不返回，这里统一做了处理
                return response
        raise exc.HTTPNotFound("没有找到你想访问的网页")

if __name__ == "__main__":

    server = simple_server.make_server("127.0.0.1",8080,Application())
    router = Router("/person")
    Application.register(router)

    @router.get("/index")
    def index(request:Request):
        res = Response()
        res.status_code = 200
        res.body = "<h1>index</h1>".encode()
        return res

    @router.get("/user")
    def user(request: Request) -> Response:
        res = Response()
        res.status_code = 200
        res.body = "<h1>user</h1>".encode()
        return res

    server.serve_forever()
    server.close_request()