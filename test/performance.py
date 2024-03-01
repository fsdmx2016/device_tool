#!/usr/bin/python
# encoding=utf-8

"""
@Author  :  SunPeng
@Date    :  2024/3/1 17:36
@Desc    :
"""
import threading
import time
import tidevice


def collect_and_store_data(perf, app_bundle_id, output_file):
    def callback(_type: tidevice.DataType, value: dict):
        if _type.value == "memory":
            ss = str(value)
            print(ss)
            memory = ss.split("'value':")[1][0:6].split("}")[0]

            with open(output_file, "a+") as f:
                f.writelines(memory)
    perf.start(app_bundle_id, callback=callback)


def process_collected_data(input_file):
    # 这个函数将在另一个线程中执行，等待数据收集完成后再处理
    time.sleep(5)  # 延迟一段时间，以便收集一些数据（请根据实际情况调整）
    with open(input_file, "r") as f:
        data_list = list(str(f.readlines()).split(" "))
        final_list = [x for x in data_list if x.__contains__(".") and len(x.split(".")) == 2]
    print(final_list[-1])


def main():
    uuid = "00008030-0006250A362B802E"
    app_bundle_id = "com.meitu.mtxx"
    t = tidevice.Device(uuid)
    perf = tidevice.Performance(t, perfs=list(tidevice.DataType))
    path="/Users/sunpeng/Documents/review/device_tool/iOS/performance/mem.txt"
    with open(path,"w") as f:
        f.write("")
    collector_thread = threading.Thread(target=collect_and_store_data, args=(
    perf, app_bundle_id, "/Users/sunpeng/Documents/review/device_tool/iOS/performance/mem.txt"))
    collector_thread.start()
    # # 在开启收集线程后，立即开始处理数据的线程
    time.sleep(5)
    processor_thread = threading.Thread(target=process_collected_data,
                                        args=("/Users/sunpeng/Documents/review/device_tool/iOS/performance/mem.txt",))
    processor_thread.start()
    time.sleep(20)
    perf.stop()

    # （可选）如果你需要等待两个线程都完成，可以调用join方法
    # collector_thread.join()
    # processor_thread.join()

    # 注意：由于线程间的并发执行，final_list的获取可能并非在主线程中立刻可用
    # 若要主线程等待获取final_list，需要在processor_thread中存储结果，并通过线程间通信方式传递给主线程


if __name__ == "__main__":
    main()