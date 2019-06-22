import socketserver
import threading
import logging


logging.basicConfig(level=logging.INFO,format="%(message)s")


"""
    注意：MyHandler这个类是自己定义的处理请求的类，这个类必须继承socketserver.BaseRequestHandler
    因为，在内部需要调用这个socketserver.BaseRequestHandler类的__init__方法，来初始化MyHandler
    实例，并且。需要MyHandler类重写socketserver.BaseRequestHandler类的setup方法、
    handle()方法、finish()方法
    
    setup()方法做一些初始化工作
    handle()做一些请求处理，比如客户端发来信息，你该怎么处理（逻辑处理）
        注意：在handle中已经做了错误捕获
    finish()做一些收尾工作，关闭socket或者服务器的socket
    
"""

class MyHandler(socketserver.BaseRequestHandler):
    def setup(self):
        self.event = threading.Event()

    #如果这里不用循环接受，哪么当一个客户端请求来以后，处理完，则这个链接就断了
    #所以需要使用循环来处理客户端请求
    def handle(self):
        while not self.event.is_set():
            data = self.request.recv(1024)
            logging.info("{}发来的信息是:{}".format(self.client_address,data.decode("gbk")))

    def finish(self):
        self.event.set()
        self.request.close()


addr = ("127.0.0.1",8080)
server = socketserver.ThreadingTCPServer(addr,MyHandler)
server.serve_forever()
server.close_request()