

"""
    信号量也相当于锁，具有和锁相同的方法
    ，初始化信号量有一个信号量的值，每次线程
    获得一把锁以后，信号量就减一，当减为0时，后面的线程
    向获取就不能获取了，只能阻塞。每当线程释放锁，那么信号量
    就加1,。

    注意：
    1、初始化信号量不能为负数，否则报错
    2、信号量如果没有调用acquire()，可以调用release()方法，并且
        信号量也会增加。那么这样会造成一个问题：多次调用release()，那么信号量
        会无限增多，因此，我们将Semaphore信号改为使用BoundedSemaphore信号
        量类来初始化，这个BoundedSemaphore如果超过了定义的边界值，那么会报错



"""

import threading
import logging

logging.basicConfig(level=logging.INFO,format="%(thread)d %(threadName)s %(message)s")


def work(semp:threading.Semaphore):
    logging.info("in work")
    semp.acquire()
    logging.info("获取得锁")


s = threading.Semaphore(3)

logging.info(s.acquire())
logging.info(s.acquire())
logging.info(s.acquire())


threading.Thread(target=work,args=(s,)).start()

logging.info("-------{}".format(s.acquire(False)))
logging.info("--{}".format(s.acquire(timeout=3)))

s.release()

logging.info("main thread end")


s = threading.Semaphore(3)
s.release()
s.release()
s.release()
s.release()
s.release()
s.release()
print(s.__dict__)

s1 = threading.BoundedSemaphore(3)

s1.acquire()
s1.acquire()
s1.acquire()

s1.release()
s1.release()
s1.release()


