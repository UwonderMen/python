
import threading
import logging
import time
logging.basicConfig(level=logging.INFO,format="%(message)s")

"""
    当
"""

def work(event:threading.Event):
    event.wait()
    logging.info("{}开始执行".format(threading.current_thread().name))

event = threading.Event()

lst = []

for i in range(3):
    p = threading.Thread(target=work,args=(event,))
    p.start()
    lst.append(p)

# for t in lst:
#     t.join()
logging.info(event.is_set())
event.wait(5)
event.set()
logging.info(event.is_set())
