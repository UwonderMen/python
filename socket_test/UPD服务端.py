import socket,threading,time,logging
logging.basicConfig(level=logging.INFO,format="%(message)s")

class UDPServer:

    def __init__(self,ip="127.0.0.1",port=8080):
        self.person = set()
        self.ip = ip
        self.port = port
        self.socket = socket.socket(type=socket.SOCK_DGRAM)
        self.event = threading.Event()

    def start(self):
        self.socket.bind((self.ip,self.port))
        logging.info("server is start at {}".format(time.ctime()))
        threading.Thread(target=self._rec).start()

    def stop(self):
        self.socket.close()
        self.event.set()

    def _rec(self):
        while not self.event.is_set():
            # recvfrom返回值是一个元祖（包含客户端数据和客户端地址）
            data,addr = self.socket.recvfrom(1024)
            logging.info("{}发来信息：{}".format(addr,data.decode("gbk")))

            #通过客户端服务端约束刚连接时的一些话语，明白客户端连接上了
            if data == "come":
                self.person.add(addr)
                continue

            if data == "quit":
                self.person.remove(addr)
                continue
            self.person.add(addr)
            self._broadcast(data,addr)  #广播给其他用户

    def _broadcast(self,msg,addr):
        o = set()
        o.add(addr) #排除自身
        p = self.person ^ o
        for c in p:
            self.socket.sendto(msg,c)

s = UDPServer()
s.start()





