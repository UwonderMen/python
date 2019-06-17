
import threading
import logging

logging.basicConfig(level=logging.INFO,format="%(thread)d %(threadName)s %(message)s")

def worker(barrier:threading.Barrier):
    logging.info("n_waiting={}".format(barrier.n_waiting))
    try:
        bid = barrier.wait()
        logging.info("after barrier {}".format(bid))
    except threading.BrokenBarrierError:
        logging.info("Broken Barrier in {}".format(threading.current_thread().name))



barrier = threading.Barrier(3)

for x in range(0,8):

    if x == 2:
        barrier.abort()
    if x == 6:
        barrier.reset()
    threading.Event().wait(1)
    threading.Thread(target=worker, args=(barrier,)).start()