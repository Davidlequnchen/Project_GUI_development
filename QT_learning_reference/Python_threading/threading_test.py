import threading
import time

class Job(threading.Thread):
    '''
    This new class inherets the Thread class, with more functionalities
    such as pause the thread, stop the thread, etc
    '''
    def __init__(self, *args, **kwargs):
        super(Job, self).__init__(*args, **kwargs)
        self.__flag = threading.Event()     # a flag to pause thread
        self.__flag.set()       #  set True
        self.__running = threading.Event()      # a notice of pausing thread
        self.__running.set()      # set True
 
    def run(self):
        while self.__running.isSet():
            self.__flag.wait()      # 为True时立即返回, 为False时阻塞直到内部的标识位为True后返回
            print (time.time())
            time.sleep(1)
 
    def pause(self):
        self.__flag.clear()     # 设置为False, 让线程阻塞
 
    def resume(self):
        self.__flag.set()    # 设置为True, 让线程停止阻塞
 
    def stop(self):
        self.__flag.set()       # 将线程从暂停状态恢复, 如果已经暂停的话
        self.__running.clear()        # 设置为False  
        
        
a = Job()
a.start()
time.sleep(3)
a.pause()
time.sleep(3)
a.resume()
time.sleep(3)
a.pause()
time.sleep(2)
a.stop()
