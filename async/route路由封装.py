from webob import Response,Request,dec,exc
from wsgiref.simple_server import make_server
import re

class Application:

    ROUTETABLE = []

    @dec.wsgify
    def __call__(self,request:Request):
        # return self.ROUTETABLE.get(request.path,self.notfound)(request)
        try:
            # return self.ROUTETABLE[request.path](request)
            for method,regex,handler in self.ROUTETABLEL:
                if request.method.upper() == method:
                    matcher = regex.match(request.path)
                    if matcher:
                        return handler(request)

        except:
            raise exc.HTTPNotFound("Not Found~")

    @classmethod
    def get(cls,pattern:str):
        return cls.register("GET",pattern)

    @classmethod
    def post(cls,pattern:str):
        return cls.register("POST",pattern)


    # def register(cls,path:str):
    @classmethod
    def register(cls,method:str,pattern:str):
        def _wrap(handler):
            # cls.ROUTETABLE[pattern] = handler
            #改进使用正则进行匹配路径,因为如果是字典类型存储存在
            #键值对乱序，那么，匹配是正则，存在先后顺序
            cls.ROUTETABLE.append((re.compile(pattern,re.S),handler))
            return handler
        return _wrap


@Application.register("GET","/")
def index(request:Request)->Response:
    res = Response()
    res.status_code = 200
    res.body = "<h1>index</h1>".encode()
    return res

@Application.register("GET","/user")
def user(request:Request) ->Response:
    res = Response()
    res.status_code = 200
    res.body = "<h1>user</h1>".encode()
    return res

server = make_server("127.0.0.1",8080,Application())
server.serve_forever()
server.close_request()




