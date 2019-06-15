

"""

    使用锁来解决多个线程去取同一个值的问题

"""

import logging
import threading

logging.basicConfig(level=logging.INFO,format="%(message)s")
lock = threading.Lock()
cpus = []
def work():

    while True:
        lock.acquire()  #上锁
        count = len(cpus)
        logging.info("杯子数量:{}".format(count))
        if len(cpus) >= 100:
            lock.release()
            break   #如果这里break了，那么锁还没有释放，造成程序还在运行
        cpus.append(1)
        lock.release()  #解锁
        logging.info("{}线程生产出1个杯子".format(threading.current_thread().name))

    logging.info("杯子总数为:{}".format(len(cpus)))


for x in range(10):

    threading.Thread(target=work,name="{}----线程".format(x)).start()

