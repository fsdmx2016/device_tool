from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import datetime

mem_X = []
mem_Y = []


class AppInfoMethod:
    def __init__(self, dev, label):
        self.dev = dev
        self.label = label

    def get_app_cpu_info(self, package_name: str):
        app_pid = self.dev.shell("pidof " + package_name)
        cpu_info = self.dev.shell("cat /proc/" + app_pid + "/sta")
        return cpu_info

    # 获取应用的内存信息
    def get_app_memory(self, package_name: str):
        output = self.dev.shell("dumpsys meminfo " + package_name + "")
        if output:
            # 解析输出并提取内存信息
            lines = output.splitlines()
            for line in lines:
                if line.__contains__("TOTAL"):
                    memory_info = line.split()[1]
                    return int(int(memory_info) / 1024)
            return None

    def get_mem_info(self, layout, package_name):
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)
        self.package_name = package_name
        self.timer = self.canvas.new_timer(interval=1000)  # 每秒更新一次
        self.timer.add_callback(self.update_plot)
        self.timer.start()

    def update_plot(self):
        global mem_X, mem_Y
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        current_time = datetime.datetime.now().strftime("%H:%M:%S")
        mem_X.append(current_time)
        # 绘制折线图.
        mem_Y.append(AppInfoMethod.get_app_memory(self, self.package_name))
        if len(mem_X) > 5:
            mem_X = mem_X[-5:]
            mem_Y = mem_Y[-5:]
        # 设置X轴标签
        ax.set_xlabel('Time')
        # 设置Y轴标签
        ax.set_ylabel('Memory')
        ax.plot(mem_X, mem_Y)
        # 刷新图形
        self.canvas.draw()
