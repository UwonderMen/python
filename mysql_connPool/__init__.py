
from queue import Queue
from pymysql import connect
from pymysql.connections import Connection
import threading

class ConnPool:
    def __init__(self,size,*args,**kwargs):
        self.size = size
        self._local = threading.local()
        self._pool = Queue(size)
        for i in range(size):
            conn = connect(*args,**kwargs)
            self._pool.put(conn)

    def get_conn(self):
        conn = self._pool.get()
        self._local.conn = conn
        return conn #当链接拿完后会阻碍

    def return_conn(self,conn:Connection):
        if isinstance(conn,Connection):
            self._pool.put(conn)
            self._local.conn = None

    @property
    def szie(self):
        return self._pool.qsize()

    def __enter__(self):
        if getattr(self._local,"conn",None) is None:
            self._local.conn = self.get_conn()
        ##返回一个游标,注意：数据库连接没有再次使用get方法拿到，只能拿到一次链接
        #解决方法是：在这个链接上使用多个游标，即连接在这个线程中得到了复用
        return self._local.conn.cursor()

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            self._local.conn.rollback()
        else:
            self._local.conn.commit()
        self.return_conn(self._local.conn)
        self._local.conn = None



pool = ConnPool(5,"127.0.0.1","root","123456","my1",3306)


with pool as cursor:
    with cursor:
        line = cursor.execute("show processlist")
        print(cursor.fetchall())
