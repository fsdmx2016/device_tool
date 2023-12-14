import threading

def task1():
    while True:
        print("111")

def task2():
    while True:
        print("22222")

if __name__ == "__main__":
    # 创建并启动线程
    thread1 = threading.Thread(target=task1)
    thread2 = threading.Thread(target=task2)
    thread1.start()
    thread2.start()
