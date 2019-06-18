import threading
import logging
import socket
logging.basicConfig(level=logging.INFO,format="%(message)s")

class UDPClient:

    def __init__(self,port=8080,ip="127.0.0.1"):
        self.ip = ip
        self.port = port
        self.socket = socket.socket(type=socket.SOCK_DGRAM)
        self.addr = (ip,port)
        self.event = threading.Event()

    def start(self):
        #注意：使用socket.connect()方法，服务端并不知道客户端已经连接
        #而只有调用了一次socket.sendto()方法后才知道客户端已经连接
        self.socket.connect(self.addr)
        self.sendMsg("come")
        threading.Thread(target=self.recv).start()

    def sendMsg(self,val):
        self.socket.sendto(val.encode("gbk"),self.addr)

    def recv(self):
        while not self.event.is_set():
            data,addr = self.socket.recvfrom(1024)
            logging.info("得到远程服务器{}回复：{}".format(self.socket.getpeername(), data.decode("gbk")))

    def stop(self):
        self.socket.close()
        self.event.set()


c = UDPClient()
c.start()

while True:
    data = input("请输入你想说的话:")
    if data.strip() == "quit":
        c.stop()
        break
    c.sendMsg(data)