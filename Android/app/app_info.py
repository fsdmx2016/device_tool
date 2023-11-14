class AppInfoMethod:
    def __init__(self, dev, label):
        self.dev = dev
        self.label = label

    def get_app_cpu_info(self, package_name: str):
        app_pid = self.dev.shell("pidof " + package_name)
        cpu_m = self.dev.shell("adb shell cat /proc/" + app_pid + "/sta")
        # cpu_m = "adb shell cat /proc/<PID>/sta"

    def get_app_mem_info(self, package_name: str):
        mem_ = self.dev.shell("adb shell dumpsys meminfo " + package_name + "")
