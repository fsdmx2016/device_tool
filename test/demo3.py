import os
import time


class ParsFPSInfo(object):
    FPS_queue: list = []  # FPS collect, 每个帧对象的结果都汇集在这里，这里每次只留最后一个不完整的帧
    before_time: list = []  # 存第一秒前3帧的
    PHONE_REAL_TIME_INTERVAL: int = None  # 真实时间和手机时间的相对差值
    start_collect_time: float = None  # 开始时间测试的真实时间

    def __init__(self, surface_info):
        self.lag_number = 0  # 每秒小于24帧的次数
        self.FTIMEGE100 = 0  # 增量耗时
        self.surface_info = surface_info
        self.jank_number = [0]
        self.big_jank_number = [0]
        self.front_FPS_list = []  # 第一个完整的秒的 FPS
        self.FPS_res_info_dict: dict = {}  # 真正返回的FPS结果集 {时间：帧信息, 时间+1s: 帧信息}
        self.FPS = self.get_FPS()
        print("end instance {0}".format(ParsFPSInfo.FPS_queue))


    def get_FPS(self):
        surface_info_resource = self.surface_info.split(os.linesep)
        new_FPS: tuple = self._GetSurfaceFlingerFrameData(surface_info_resource)
        self.add_new_FPS(new_FPS[1])
        print("end get new fps")
        self.get_front_FPS()
        print("log get fps result")
        print(ParsFPSInfo.FPS_queue)
        full_FPS_number = int(1 / new_FPS[0])
        self.full_FPS_number = full_FPS_number
        # return min(full_FPS_number, len(self.front_FPS_list))
        return self.FPS_res_info_dict

    def _GetSurfaceFlingerFrameData(self, results):
        timestamps = []
        if not len(results):
            return (None, None)
        if "TIME" in results[0]:
            results = results[1:]
        nanoseconds_per_second = 1e9
        refresh_period = int(results[0]) / nanoseconds_per_second
        pending_fence_timestamp = (1 << 63) - 1

        for index, line in enumerate(results[1:]):
            fields = line.split()
            if len(fields) != 3:
                continue
            try:
                timestamp = int(fields[1])
            except ValueError as e:
                print(e)
                continue
            if timestamp == pending_fence_timestamp:
                continue
            timestamp /= nanoseconds_per_second
            timestamps.append(timestamp)
        return (refresh_period, timestamps)

    def add_new_FPS(self, new_FPS):
        if ParsFPSInfo.FPS_queue:
            FPS_list_last = ParsFPSInfo.FPS_queue[-1]
            for index, v in enumerate(new_FPS):
                if v == FPS_list_last:
                    self.FPS_queue.extend(new_FPS[index + 1:])
                    print("find result")
                    print("剩余帧{0}".format(len(ParsFPSInfo.FPS_queue)))
                    break
            else:
                if new_FPS and FPS_list_last < new_FPS[0]:
                    ParsFPSInfo.FPS_queue.extend(new_FPS)
                else:
                    print("丢帧！！！！！！！！！！！！！！！！！！！！！！！！！！！！")
                    print(FPS_list_last)
                    print(new_FPS)
            if not ParsFPSInfo.PHONE_REAL_TIME_INTERVAL:
                if len(new_FPS) > 126 and new_FPS[-1] != 0.0:
                    ParsFPSInfo.PHONE_REAL_TIME_INTERVAL = int(time.time()) - new_FPS[-1]
                    print("时间间隔-new-{0}, {1}".format(ParsFPSInfo.PHONE_REAL_TIME_INTERVAL, new_FPS[-1]))
        else:
            ParsFPSInfo.FPS_queue.extend(new_FPS)
            if not ParsFPSInfo.PHONE_REAL_TIME_INTERVAL:
                first_time = 0.0  # 拿到第一个有值的数据和真实时间对应
                for i in ParsFPSInfo.FPS_queue:
                    if float(i) != 0.0 and first_time == 0.0:
                        first_time = i
                print("first_time {0}".format(first_time))
                if first_time != 0.0:
                    if ParsFPSInfo.start_collect_time:
                        ParsFPSInfo.PHONE_REAL_TIME_INTERVAL = ParsFPSInfo.start_collect_time - int(first_time)
                        # ParsFPSInfo.start_collect_time = None, 不会中断开始收集时间有一个就够了
                    else:
                        ParsFPSInfo.PHONE_REAL_TIME_INTERVAL = int(time.time()) - int(first_time)
                    print(
                        "时间间隔 {0} {1} {2} {3}".format(ParsFPSInfo.PHONE_REAL_TIME_INTERVAL, time.time(), first_time,
                                                          ParsFPSInfo.FPS_queue))
                else:
                    ParsFPSInfo.FPS_queue = []
                    ParsFPSInfo.PHONE_REAL_TIME_INTERVAL = None
                    print("第一个时间戳有误")
                    print(ParsFPSInfo.FPS_queue)

    def get_front_FPS(self):
        """
        PerfDog Jank计算方法：
        同时满足两条件，则认为是一次卡顿Jank.
        ①Display FrameTime>前三帧平均耗时2倍。
        ②Display FrameTime>两帧电影帧耗时 (1000ms/24*2=84ms)。
        同时满足两条件，则认为是一次严重卡顿BigJank.
        ①Display FrameTime >前三帧平均耗时2倍。
        ②Display FrameTime >三帧电影帧耗时(1000ms/24*3=125ms)。
        """
        # 拿到了队列里所有的完整帧
        while ParsFPSInfo.FPS_queue:
            print("join get front fps")
            tmp = []
            time_flag = ParsFPSInfo.FPS_queue.pop(0)
            time_second = int(time_flag)
            tmp.append(time_flag)
            while ParsFPSInfo.FPS_queue and int(ParsFPSInfo.FPS_queue[0]) == time_second:
                header_ele = ParsFPSInfo.FPS_queue.pop(0)
                tmp.append(header_ele)
            if not ParsFPSInfo.FPS_queue:
                ParsFPSInfo.FPS_queue.extend(tmp)
                break
            else:
                self.front_FPS_list.append(tmp)
        res_dict = {}
        try:
            for item_list in self.front_FPS_list:
                # print(item_list[0], ParsFPSInfo.PHONE_REAL_TIME_INTERVAL)
                # 如果当前帧都是空就跳过
                if sum(item_list) == 0.0:
                    continue
                first_time_head = None  # 获取第一个帧第一个有时间的值
                for time_head in item_list:
                    first_time_head = time_head if time_head else None
                res_dict[int(first_time_head) + ParsFPSInfo.PHONE_REAL_TIME_INTERVAL] = item_list[0:]
        except Exception as e:
            print(e)
        self.FPS_res_info_dict: dict = res_dict
        self.get_jank(self.FPS_res_info_dict)
    def get_jank(self, FPS_res_info_dict: dict):
        for front_index, (time_number, item_list_v) in enumerate(FPS_res_info_dict.items()):
            for index, v in enumerate(item_list_v):
                if len(ParsFPSInfo.before_time) < 4:
                    ParsFPSInfo.before_time.append(v)
                else:
                    interval = v - ParsFPSInfo.before_time[-1]
                    if interval > 0.1:
                        ParsFPSInfo.FTIMEGE100 = 1
                    else:
                        ParsFPSInfo.FTIMEGE100 = 0
                    if v - ParsFPSInfo.before_time[-1] > sum([
                        ParsFPSInfo.before_time[-1] - ParsFPSInfo.before_time[-2],
                        ParsFPSInfo.before_time[-2] - ParsFPSInfo.before_time[-3],
                        ParsFPSInfo.before_time[-3] - ParsFPSInfo.before_time[-4], ]) / 3 * 2:
                        if interval > 0.125:
                            if len(self.big_jank_number) <= front_index:
                                self.big_jank_number.append(1)
                            else:
                                self.big_jank_number[front_index] += 1
                        elif interval > 0.084:
                            if len(self.jank_number) <= front_index:
                                self.jank_number.append(1)
                            else:
                                self.jank_number[front_index] += 1
                    ParsFPSInfo.before_time.pop(0)
                    ParsFPSInfo.before_time.append(v)

class Demos:
    def get_FPS_info(self,dev):
        """
        通过执行 "dumpsys SurfaceFlinger --list" 命令，您可以获取有关当前正在显示在屏幕上的所有图形元素的详细信息，例如它们的名称、大小、格式、位置和可见性等。
        """
        surface_list_info = dev.shell("dumpsys SurfaceFlinger --list")
        if dev.sdkversion >= 24:
            self.get_FPS_surface_view(surface_list_info,dev)
        else:
            self.get_FPS_surface_view_low_version(surface_list_info,dev)
        """
        通过执行 "dumpsys SurfaceFlinger --latency" 命令，您可以获取有关SurfaceFlinger处理每一帧图像所需的时间的信息，包括处理时间的最小值、最大值、平均值和标准差等。
        """
        surface_info = dev.shell(
            "dumpsys SurfaceFlinger --latency '{0}' ".format(self.m_surface_view_name)).decode()
        pars_FPS_info = ParsFPSInfo(surface_info)
        self.FPS_info = pars_FPS_info
        return pars_FPS_info.FPS, pars_FPS_info.lag_number, pars_FPS_info.full_FPS_number,

    def get_FPS_surface_view(self, surface_info,dev):
        for i in surface_info.split(os.linesep):
            if "SurfaceView" not in i or "Background for" in i or dev.package not in i:
                continue
            if not self.m_surface_view_name or "BLAST" in i:
                self.m_surface_view_name = i
        if self.m_surface_view_name is None:
            self.m_surface_view_name = self.get_surfaceview_activity(dev)
        print("获取到的surface_view信息是：{}".format(self.m_surface_view_name))

    def get_FPS_surface_view_low_version(self, surface_info,dev):
        for i in surface_info.split(os.linesep):
            if dev.package not in i:
                continue
            if not self.m_surface_view_name or "BLAST" in i:
                self.m_surface_view_name = i.strip()
        print("获取到的surface_view信息是：{}".format(self.m_surface_view_name))
    
    def get_surfaceview_activity(self,dev):
        activity_name = ''
        activity_line = ''
        try:
            dumpsys_result = dev.shell(
                'dumpsys SurfaceFlinger --list | {} {}'.format("grep", dev.package)).decode()
            dumpsys_result_list = dumpsys_result.split('\n')
            for line in dumpsys_result_list:
                if line.startswith('SurfaceView') and line.find(dev.package) != -1:
                    activity_line = line.strip()
                    break
            if activity_line:
                if activity_line.find(' ') != -1:
                    activity_name = activity_line.split(' ')[2]
                else:
                    activity_name = activity_line.replace('SurfaceView', '').replace('[', '').replace(']', '')
            else:
                activity_name = dumpsys_result_list[len(dumpsys_result_list) - 1]
                if not activity_name.__contains__(dev.package):
                    print(
                        'get activity name failed, Please provide SurfaceFlinger --list information to the author')
                    print('dumpsys SurfaceFlinger --list info: {}'.format(dumpsys_result))
        except Exception:
            print('get activity name failed, Please provide SurfaceFlinger --list information to the author')
            print('dumpsys SurfaceFlinger --list info: {}'.format(dumpsys_result))
        return activity_name

if __name__ == '__main__':
    from airtest.core.android import Android
    dev = Android()
    dev.shell("dumpsys SurfaceFlinger --latency-clear")
    dev_info=Demos()
    try:
        FPS_info_FPS, FPS_info_lag_number, FPS_full_number = dev_info.get_FPS_info(dev)
    except Exception as e:
        print(e)
    print(
        "fps collect result {0} {1} {2}".format(FPS_info_FPS, FPS_info_lag_number, FPS_full_number))

