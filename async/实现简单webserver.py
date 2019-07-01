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


class Context:
    def __getattr__(self, item):
        try:
            return self[item]
        except KeyError:
            raise AttributeError("not {} Attribute".format(item))

    def __setattr__(self, key, value):
        self[key] = value


class NestedContext(Context):
    """
        NestedContext是一个嵌套的Context的子类，如果在子类中
        每找到那么取父类Context中查找
    """
    def __init__(self,globalContext:Context):
        super().__init__()
        self.relate(globalContext)

    def relate(self,globalContext:Context):
        self.globalContext = globalContext

    def __getattr__(self, item):
        if item in self.item():
            return self[item]
        return self.globalContext[item]


class Router:
    def __init__(self,prefix:str):
        """
        :param prefix: 路由的一级前缀
        :param pre_interceptor：请求前的拦截器，可以有多个，所以是一个列表
        :param post_interceptor：响应前的拦截器，可以有多个，所以是一个列表

        """
        self.pre_interceptor = []
        self.post_interceptor = []

        #注册路由实例的上下文，但是这里初始化为None
        #等到路由实例注册的时候，真正关联到全局上下文
        self.ctx = NestedContext()

        self.__prefix = prefix.rstrip("/\\")
        self.__routertable = []  #保存三元组[(method,pattern,handler),]

    def route(self,pattern,*methods):
        def wrapper(handler):
            self.__routertable.append((methods,re.compile(pattern,re.S),handler))
            return handler
        return wrapper

    def register_pre_interceptor(self,fn):
            self.pre_interceptor.append(fn)
            return fn

    def register_post_interceptor(self,fn):
            self.post_interceptor.append(fn)
            return fn

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

        #TODO  router做请求处理前的拦截
        for fn in self.pre_interceptor:
            request = fn(self.ctx,request)


        for methods,pattern,handler in self.__routertable:
            if not methods or request.method.upper() in methods:
                matcher = pattern.match(request.path.replace(self.__prefix,"",1))
                if matcher:
                    request.args = matcher.group()
                    #在这里包装一下我们获得的属性，但是不允许在修改
                    request.kwargs = DictObj(matcher.groupdict())
                    response  = handler(self.ctx,request)

                    #TODO router局部做请求响应前的拦截
                    for fn in self.post_interceptor:
                        response = fn(self.ctx,request,response)

                    return  response
        # raise exc.HTTPNotFound("页面没有找到")
        # return None



#后期改成单例模式，只允许创建一个Aplication实例
    #解决方法：
        #使用信号量
class Application:

    """
        :Attribute ROUTERS：注册的一级路由实例
        :Attribute ctx：应用的上下文
        :Attribute PREINTERCEPTOR:请求前的全局拦截
        :Attribute POSTINTERCEPTOR:请求响应前的全局拦截
    """

    ROUTERS = []
    ctx = Context()
    PREINTERCEPTOR = []
    POSTINTERCEPTOR = []

    def __init__(self,**kwargs):
        self.ctx.app= self
        for k,v in kwargs.items():
            self.ctx[k] = v

    @classmethod
    def register(cls,router:Router):
        router.ctx.relate(cls.ctx)
        router.ctx.router = router
        cls.ROUTERS.append(router)

    @classmethod
    def register_preinterceptor(cls,fn):
        cls.PREINTERCEPTOR.append(fn)
        return fn

    #扩展的功能，当然这里只是提供了一个简单函数，
    # 具体的实现还要更复杂，这里没有实现
    @classmethod
    def extend(cls,name,ext):
        cls.ctx[name] = ext

    @classmethod
    def register_postinterceptor(cls,fn):
        cls.POSTINTERCEPTOR.append(fn)
        return fn

    @dec.wsgify
    def __call__(self,request:Request):

        # TODO 做全局请求拦截
        for fn in self.POSTINTERCEPTOR:
            request = fn(self.ctx,request)

        for router in self.ROUTERS:
            logging.info(request.path)
            response = router.match(request)

            if response:
                # TODO 做全局响应拦截
                for fn in self.POSTINTERCEPTOR:
                    response = fn(self.ctx,request,response)

                # 因为这里做了处理，那么在match中找不到可以不返回，这里统一做了处理
                return response
        raise exc.HTTPNotFound("没有找到你想访问的网页")

if __name__ == "__main__":

    server = simple_server.make_server("127.0.0.1",8080,Application())
    router = Router("/person")
    Application.register(router)

    @router.get("/index")
    def index(ctx,request:Request):
        res = Response()
        res.status_code = 200
        res.body = "<h1>index</h1>".encode()
        return res

    @router.get("/user")
    def user(ctx,request: Request) -> Response:
        res = Response()
        res.status_code = 200
        res.body = "<h1>user</h1>".encode()
        return res

    server.serve_forever()
    server.close_request()