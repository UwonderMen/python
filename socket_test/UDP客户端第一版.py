import threading
import logging
import socket

logging.basicConfig(level=logging.INFO,format="%(message)s")
sock = socket.socket(type=socket.SOCK_DGRAM)
ip = "127.0.0.1"
port = 3000
data = "你好".encode("gbk")
sock.connect((ip,port))
sock.sendto(data,(ip,port))
#这里会阻塞
result = sock.recvfrom(1024)
logging.info("得到远程服务器{}回复：{}".format(sock.getpeername(),data.decode("gbk")))

