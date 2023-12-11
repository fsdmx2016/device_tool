import threading

def task1():
    print("Task 1 started")
    # 执行任务1的代码
    print("Task 1 completed")

def task2():
    print("Task 2 started")
    # 执行任务2的代码
    print("Task 2 completed")

if __name__ == "__main__":
    # 创建并启动线程
    thread1 = threading.Thread(target=task1)
    thread2 = threading.Thread(target=task2)
    thread1.start()
    thread2.start()
