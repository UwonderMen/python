import socket,threading,time,logging
logging.basicConfig(level=logging.INFO,format="%(message)s")

class Server:

    def __init__(self,ip="127.0.0.1",port=8080):
        self.person = {}
        self.ip = ip
        self.port = port
        self.socket = socket.socket()
        self.event = threading.Event()

    def start(self):
        self.socket.bind((self.ip,self.port))
        self.socket.listen()
        logging.info("server is start at {}".format(time.ctime()))
        threading.Thread(target=self._accept).start()

    def stop(self):
        for _,client in self.person.items():
            client.close()
        self.socket.close()
        self.event.set()

    def _accept(self):
        while not self.event.is_set():
            client,addr = self.socket.accept()
            f = client.makefile(mode="rw")
            # self.person[addr] = client  #改成文件形式
            self.person[addr] = f
            logging.info("{} is connect on server".format(addr))
            threading.Thread(target=self._rec,args=(f,addr,)).start()

    def _rec(self,f,addr):
        while not self.event.is_set():
            try:
                # 这里如果不进行异常处理，当一个客户端断开以后，其他客户端可能会受到影响，同时，在windows下可能因为，
                # 客户端强行端开后，第二次连接不能再使用recv()方法
                # msg = f.recv(1024)

                msg = f.readline()
                # 当客户端主动断开连接后，无法读取到消息，
                # 因此为空，那么判断是否为空作为结束条件，但是这样很牵强
                if msg == '':break
            except Exception as e:
                logging.info(e)
                msg = "quit"

            if msg == "quit":
                # client.close()
                f.close()
                break
            logging.info("{}发送的群消息是：{}，发送的时间是：{}".format(addr,msg,time.ctime()))
            self._broadcast(addr,msg)

    def _broadcast(self,addr,msg):
        for caddr,f in self.person.items():
            if caddr is not addr:
                f.write(msg)

s = Server()

s.start()





