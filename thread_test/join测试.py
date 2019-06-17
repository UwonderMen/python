

import threading
import time
import logging

logging.basicConfig(level=logging.INFO)

def work():

    for i in range(100):
        time.sleep(2)
        logging.info("{}{}".format(threading.current_thread().name,i))

lst = []

for i in range(5):
    t = threading.Thread(target=work,name="{}".format(i))
    t.start()
    lst.append(t)
    # t.join()   join不能写在这，否则要等待第一个线程结束才开启第二个线程，这样就变成串行了

for t in lst:
    t.join()

logging.info("end")

