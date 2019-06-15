
import threading
import time

class Counter:

    n = 0

    def __init__(self):
        self.__lock = threading.Lock()

    def add(self):

        try:
            self.__lock.acquire()
            self.n += 1
        finally:
            self.__lock.release()

    def reduce(self):
        with self.__lock:
            self.n -= 1

    @property
    def value(self):
        with self.__lock:
            return self.n

l = threading.Lock()

def do(c:Counter,count=100):

    for _ in range(count):
        l.acquire()
        for i in range(-50,50):
            if i < 0:
                c.add()
            else:
                c.reduce()
        l.release()


t_count = 100
c1 = Counter()
c = 1000

for _ in range(t_count):
    threading.Thread(target=do,args=(c1,c)).start()


while True:
    time.sleep(1)
    print(threading.enumerate())
    print(c1.value)


