import threading

"""

    RLock实例锁了多少次必须要解锁多少次
    
    注意：RLock是线程相关的，不能跨线程解锁

"""

def do(lock:threading.RLock):
    lock.release()  #使用另一个线程解锁

lock = threading.RLock()

res = lock.acquire()

print(res)

res1 = lock.acquire()

print(res1)

#RLock是线程相关锁，不能跨线程解锁
threading.Thread(target=do,args=(lock,)).start()

