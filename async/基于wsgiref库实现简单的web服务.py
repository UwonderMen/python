from wsgiref.simple_server import make_server,demo_app
from webob import Request,Response,dec

# def application(environ,start_response):
#     start_response("200 ok",[("Content-Type","text/html;charset=utf8")])
#     return ["<html><head><title>my site</title></head><body><h1>hhh</h1></body></html>".encode()]

ROUTETABLE = {}

def index(request:Request):
    res = Response()
    res.status_code = 200
    res.body = "<h1>index</h1>".encode()
    return res

def user(request:Request):
    res = Response()
    res.status_code = 200
    res.body = "<h1>user</h1>".encode()
    return res

def notFound(request:Request):
    res = Response()
    res.status_code = 404
    res.body = "<h1>notFound</h1>".encode()
    return res

def register(path,handler):
    ROUTETABLE[path] = handler

register("/",index)
register("/user",user)

@dec.wsgify
def app(request:Request):
    return ROUTETABLE.get(request.path,notFound)(request)



ip = "127.0.0.1"
port = 8080
server = make_server(ip,port,app)
# server = make_server(ip,port,demo_app)

server.serve_forever()
server.close_request()

