"""

    concurrent包是3.2版本引入

    解决了异步并行任务编程模块，提供了一个高级的异步可执行的遍历接口


    提供了2个池执行器

    ThreadPoolExecutor 异步调用的线程池的Executor

    ProcessPoolExecutor  异步调用的进程池的Executor

    ThreadPoolExecutor和ProcessPoolExecutor创建一个可执行器都有一个线程池或者
    进程池的最大限度,即max_workers参数，这个参数控制了，最大创建线程或者
    进程个数。

    ThreadPoolExecutor和ProcessPoolExecutor返回的实例执行了submit()方法
    将待执行的方法交给线程或者进程做时，会返回一个Future实例，这个实例可以监听
    线程或者进程的状态，比如：监听是否执行成功，得到返回结果等

    ThreadPoolExecutor和ProcessPoolExecutor返回的实例的方法
        submit()    将方法或者任务交给线程或者进程
        shutdown()  清理进程或者线程池

    Future实例的方法：
        done()  查看线程是否执行成功或者执行是否完成，如果执行成功或者执行完成返回True
        result()  查看执行函数的返回结果
        cancel()  取消执行这个函数
        running（）  是否在运行中
        exception() 获取执行中的错误


    注意：线程池中可重用的线程的线程名不能被修改了

"""

import logging
import threading
import time
from  concurrent import futures

logging.basicConfig(level=logging.INFO,format="%(thread)d %(threadName)s %(message)s")


def work():
    logging.info("{} is start working".format(threading.current_thread().name))
    time.sleep(5)
    logging.info("{} is end working".format(threading.current_thread().name))




if __name__ == "__main__":
    executor = futures.ProcessPoolExecutor(max_workers=3)  #进程池的使用
    # executor = futures.ThreadPoolExecutor(max_workers=3)  #线程池的使用

    fs = []

    for i in range(3):
        f = executor.submit(work)  #将任务交给线程去做，返回一个Future的实例
        fs.append(f)

    for i in range(3,6):
        f = executor.submit(work)  # 将任务交给线程去做，返回一个Future的实例
        fs.append(f)

    while True:
        time.sleep(2)
        logging.info(threading.enumerate())
        flag = True
        for f in fs:
            flag = flag and f.done()

        if flag:
            executor.shutdown()
            logging.info("线程池被清理")
            break

