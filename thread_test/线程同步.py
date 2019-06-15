"""

    线程同步解决方式：
        事件（event）


    event事件是线程通信机制中最简单的实现，使用一个内部的标记flag
    ，通过flag的True或False的变化来进行操作

"""


"""
    问题：
        工人和老板问题

"""

import  threading
import logging
import time

logging.basicConfig(level=logging.INFO,format="%(message)s")
root = logging.getLogger()
root.setLevel(logging.INFO)
n = 0

def boss():
    global n
    while True:
        c = logging.getLogger("c")
        c.info("{}{}".format("boss来查看杯子：", n))
        if n == 10:
            log = logging.getLogger("a")
            log.info("{}{}".format("boss:","得到10个杯子"))
            break


def worker():
    global n
    time.sleep(2)
    n += 1
    w = logging.getLogger("b")
    w.info("{}{}".format("工人生产出",n))

threading.Thread(target=boss,daemon=True).start()

while True:
    time.sleep(2)
    worker()


