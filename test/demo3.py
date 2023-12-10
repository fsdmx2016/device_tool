import time

file_path = "D:\WorkDemo\My_Work\device_tool_git\Android\script_file\step.txt"
with open(file_path, 'r') as f_input:
    for line in f_input:
        # 判断是不是首行
        first_time = 1
        if line.__contains__("first_line"):
            first_time = line.split(" ")[3]
            latest_time = first_time
        else:
            # 等待时间为2次click的间隔
            time.sleep(float(line.split(' ')[2]) - float(latest_time))
            first_time = float(line.split(' ')[2])
            print(first_time)
