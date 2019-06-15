
"""
    python中的字典是线程安全的

"""

import threading
import time
#
# def work():
#     k = 0
#     for i in range(20):
#         time.sleep(0.00001)
#         k += 1
#
#     print("我是{}线程".format(threading.current_thread()),k,id(k))
#
# for _ in range(10):
#     threading.Thread(target=work).start()
#
# a = threading.local()
#

def add(a,b):
    return a+b

t = threading.Timer(3,add,args=(4,5))
t.start()















