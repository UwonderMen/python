import socket
import time
import logging
import threading

logging.basicConfig(level=logging.INFO,format="%(message)s")

class ChatServer:

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
            self.person[addr] = client
            logging.info("{} is connect on server".format(addr))
            threading.Thread(target=self._rec,args=(client,addr,)).start()

    def _rec(self,client:socket.socket,addr):
        while not self.event.is_set():
            try:
                # 这里如果不进行异常处理，当一个客户端断开以后，其他客户端可能会受到影响，同时，在windows下可能因为，
                # 客户端强行端开后，第二次连接不能再使用recv()方法
                msg = client.recv(1024)
                msg = msg.decode("gbk")
            except Exception as e:
                logging.info(e)
                msg = "quit"

            if msg == "quit":
                client.close()
                break
            logging.info("{}发送的群消息是：{}，发送的时间是：{}".format(addr,msg,time.ctime()))
            self._broadcast(addr,msg.encode("gbk"))

    def _broadcast(self,addr,msg):
        for caddr,client in self.person.items():
            if caddr is not addr:
                client.send(msg)



c = ChatServer()
c.start()