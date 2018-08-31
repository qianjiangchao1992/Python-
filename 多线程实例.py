##1.多任务可以由多进程实现，也能通过多线程实现
##2.一个进程至少有一个线程
##3.由于线程是操作系统直接支持的执行单元，因此，高级语言通常都内置多线程的支持，Python也不例外，并且，Python的线程是真正的Posix Thread，而不是模拟出来的线程。
import time,threading
# 新线程执行的代码:
def loop():
	print('thread %s is running...' % threading.current_thread().name)     #current_thread获取当前进程
	n=0
	while n<5:
		n=n+1
		print('thread %s >>>%s'%(threading.current_thread().name,n))
		time.sleep(1)
	print('thread %s is ended'%(threading.current_thread.name))
print('thread %s is ended' %(threading.current_thread.name))
t=threading.Thread(target=loop,name='LoopThread')
t.start()
t.join()
print('thread %s ended.' % threading.current_thread().name)