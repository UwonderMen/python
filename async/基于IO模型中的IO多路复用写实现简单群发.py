import selectors,logging,socket,threading

logging.basicConfig(level=logging.INFO,format="%(message)s")


class ChatServer:

    clients = {}

    def __init__(self,port,ip):
        self.port = port
        self.ip = ip
        self.address = (self.ip,self.port)
        self.socket = socket.socket()
        self.selector = selectors.DefaultSelector()
        self.event =threading.Event()

    def start(self):
        self.socket.bind(self.address)
        self.socket.listen()
        self.socket.setblocking(False)
        self.reg(self.socket,selectors.EVENT_READ, self._accept)
        logging.info("服务器已经启动，监听在{}上".format(self.address))

    def reg(self,fileobj,event,fn):
        _ = self.selector.register(fileobj,event,fn)  #将IO事件的是否完成交给操作系统

    def run(self):
        threading.Thread(target=self._run).start()

    def _run(self):
        while not self.event.is_set():
            events = self.selector.select() #阻塞
            if events:
                for key,mask in events:
                    logging.info(mask)
                    callback = key.data
                    callback(key.fileobj,mask)



    def _accept(self,obj,mask):
        conn,client = self.socket.accept()
        self.clients[client] = conn
        logging.info("存在的客户端:{}".format(self.clients))
        self.reg(conn,selectors.EVENT_READ,self._recv)


    def _recv(self,conn:socket.socket,mask):
        data = conn.recv(1024)
        logging.info("来自{}的信息是：{}".format(conn.getsockname(),data.decode("gbk")))
        self._send(data,conn)

    def _send(self,data,conn:socket.socket):
        for (c,port),con in self.clients.items():
            if c != conn.getsockname():
                con.send(data)
                logging.info("发送消息给{}，他的端口号是：{}".format(c,port))


    def stop(self):
        for conn in self.clients.values():
            conn.close()
        self.event.set()
        self.socket.close()

c = ChatServer(8080,"127.0.0.1")

c.start()
c.run()


