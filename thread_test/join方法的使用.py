

"""
    线程中join方法的使用

        join方法：在那个线程中调用了join方法，那么表示在此线程中与创建的线程
        存在等待关系，即：调用join的线程等待再此线程中创建的子线程

        注意：有了join方法以后，创建线程中的daemon属性不管用了
"""

import threading
import logging
import time

logging.basicConfig(level=logging.INFO)


def work():
    for x in range(20):
        msg = "我是{}线程".format(threading.current_thread())
        logging.info(msg)
        # threading.Thread(target=work1,daemon=True).start()
        t = threading.Thread(target=work1,daemon=True)
        t.start()
        t.join()   #如果在子线程中创建子子线程，并且指定了daemon为
                    #True，那么，在子线程结束后不会等待子子线程结束
                    #除非使用join方法

def work1():
    for x in range(10):
        time.sleep(2)
        logging.info("我是work1方法，我是第{}线程".format(threading.current_thread()))



t = threading.Thread(target=work,daemon=True)

t.start()
t.join()
# t.join()  #使用join方法以后daemon的设置不管用了
# time.sleep(0.5)
# time.sleep(0.5)
print("我是主线程:",threading.current_thread())


