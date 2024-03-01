# import time
# import tidevice
# from tidevice._perf import DataType
#
# t = tidevice.Device("00008030-0006250A362B802E")
# perf = tidevice.Performance(t, [DataType.CPU, DataType.MEMORY, DataType.NETWORK, DataType.FPS, DataType.PAGE, DataType.SCREENSHOT, DataType.GPU])
# #  tidevice version <= 0.4.16:
# #  perf = tidevice.Performance(t)
#
# def callback(_type: tidevice.DataType, value: dict):
#     print("R:", _type.value, value)
#
# perf.start("com.meitu.mtxx", callback=callback)
# time.sleep(10)
# perf.stop()
# import sqlite3  # 导入sqlite3
# conn = sqlite3.connect("ios_performance.db")  # 打开或创建数据库文件
# print("Opened database successfully!")
# c = conn.cursor()  # 获取游标
# # 创建数据库表头
# sql = '''
# create table company
#         (id int primary key autoincrement,
#         name text not null,
#         age int not null,
#         address char(50),
#         salary real);
# '''
# c.execute(sql)  # 执行sql语句
import time

import tidevice


def test_get_myZtest():
    app_bundle_id = "com.meitu.mtxx"
    t = tidevice.Device("00008030-0006250A362B802E")  # iOS设备
    perf = tidevice.Performance(t, perfs=list(tidevice.DataType))
    perf.start(app_bundle_id, callback=callback)
    time.sleep(10)  # 测试时长
    perf.stop()


def callback(_type: tidevice.DataType, value: dict):
    if _type.value == "cpu":
        # print('CPU打印',value)
        ss = str(value)  # 转成str
        use_cpu = ss.split("'value':")[1][0:6].split("}")[0]
        sys_cpu = ss.split("'sys_value':")[1][0:7].split("}")[0]
        count_cpu = ss.split("'count':")[1].split("}")[0]

    if _type.value == "memory":
        ss = str(value)
        memory = ss.split("'value':")[1][0:6].split("}")[0]
        file = "/Users/sunpeng/Documents/review/device_tool/iOS/performance/mem.txt"
        with open(file,"a+") as f:
            f.writelines(memory.strip())
        f.close()

if __name__ == '__main__':
    file = "/Users/sunpeng/Documents/review/device_tool/iOS/performance/mem.txt"

    with open(file,"r") as f:
        data_list=list(str(f.readlines()).split(" "))
        x=[x for  x in data_list if x.__contains__(".") and len(x.split("."))==2]
        print(x)
