
"""

    网络编程基础

"""

import socket
import time
import logging

logging.basicConfig(level=logging.INFO,format="%(message)s")

ip = '127.0.0.1'
port = 8080

with socket.socket() as sock:  #1
    addr = (ip,port)  #2
    sock.bind(addr)     #3
    sock.listen()  #4
    logging.info("sever已经开始监听")
    conn,remote_adress = sock.accept()  #5  #默认是阻塞的
    logging.info("客户端地址：{},连接时间是".format(remote_adress,time.ctime()))
    msg = conn.recv(1024)  #5 接受客户端的数据
    logging.info(msg)
    # conn.send()  #6  服务端发送给客户端数据


