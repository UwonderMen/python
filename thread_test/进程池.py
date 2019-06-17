
import multiprocessing
import datetime
import logging

logging.basicConfig(level=logging.INFO,format="%(message)s")

def calc():
    sum = 0
    logging.info(multiprocessing.current_process())
    for _ in range(100000000):
        sum += 1


if __name__ ==  '__main__':

    start = datetime.datetime.now()
    p = multiprocessing.Pool(3)
    for i in range(3):
        p.apply_async(calc)
    p.close()  #如果没有关闭，进程池还可以复用,这里我们选择关闭
    p.join()  #这个进程必须等待其它进程完毕，才继续往下执行
    delta = (datetime.datetime.now() - start).total_seconds()
    logging.info(delta)




