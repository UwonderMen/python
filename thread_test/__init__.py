
import threading
import time
import logging  #这个模块时线程安全的，是一个日志输出模块

"""
    线程结束的方式：
        1、遇到异常
        2、函数结束
    
    
    threading.Tread(target="",args=(,),kwargs={},daemon=True,name="")
        target：表示线程执行的函数
        args：传递给函数的位置参数
        kwargs：传递给函数的key-word参数或者key-word only参数
        name:表示给线程起的名字,多个线程名字可以相同
        daemon：如果是True表示当主线程结束那么不会等待子线程结束，就直接杀掉子线程
            如果为False，那么主线程要等待子线程结束才结束
            注意：主线程是一个non-daemon ，子线程是不是一个daemon，那么
            要看你创建线程时是否指定daemon属性为True
            
            daemon应用场景：为True时，做一些检查，一些数据处理不重要的操作
                            为False时，执行一些数据处理，不允许没完成就关闭的操作
"""


class Test:
    def __init__(self):
        self.thead = threading.Thread(target=self.work,daemon=True)
    n = 0

    def run(self):
        self.thead.start()

    def work(self):
        while True:
            time.sleep(1)
            self.n += 1;
            print("我是:",threading.current_thread(),"我拿到的n是：",self.n)
            if self.n == 50:
                break


t  = Test()
t1 = Test()
t.run()
t1.run()
time.sleep(2)  #主线程通过睡觉验证当cpu切换到其它线程后，执行一会儿，又
                #交给主线程执行时，如果主线程发现没有non-daemon，那么就会杀掉
                #所有线程，退出程序
# raise Exception("出错啦")


print("--------我是:",threading.current_thread())




