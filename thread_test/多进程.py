
import multiprocessing
import datetime
import logging

logging.basicConfig(level=logging.INFO,format="%(message)s")

def calc():
    sum = 0
    for _ in range(100000000):
        sum += 1

#这个必须要求写在__main__里边

if __name__ ==  '__main__':

    start = datetime.datetime.now()
    lst = []
    for i in range(3):
        p = multiprocessing.Process(target=calc,name="proceess-{}".format(i))
        p.start()
        lst.append(p)

    for p in lst:
        p.join()
    delta = (datetime.datetime.now() - start).total_seconds()
    logging.info(delta)




