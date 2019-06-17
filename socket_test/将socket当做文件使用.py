import socket,threading,time,logging

logging.basicConfig(level=logging.INFO,format="%(message)s")
ip = "127.0.0.1"
port = 8080
sock = socket.socket()
sock.bind((ip,port))
sock.listen()

def _accept(sock:socket.socket):

    conn,_ = sock.accept()
    f = conn.makefile(mode="rw")  #将socket变成文件，下面操作基于文件操作来操作socket
    while True:
        line = f.read()  #操作socket变成操作文件
        logging.info(line)
        if line == 'quit':
            break
        msg = "recv msg is {}".format(line)

        f.write(msg)  #写入消息到缓冲区
        f.flush()    #开始向客户端发送消息

    f.close()
    sock.close()

threading.Thread(target=_accept,args=(sock,)).start()


