from airtest.core.api import *
from poco.drivers.ios import iosPoco
# https://www.python100.com/html/FQ7R847CI8W1.html
# 连接设备
auto_setup(__file__)
connect_device("ios:///x.x.x.x:8100")
#
# # 初始化iOS原生poco
# poco = iosPoco()
#
# # 点击Home键
# keyevent("HOME")
# 截屏
snapshot()
# # 滑动操作
# swipe(Template(r"tpl1561985939879.png", record_pos=(0.356, -0.174), resolution=(750.0, 1334.0)), vector=[-0.685, 0.0481])
#
# # 点击app Safari
# poco("Safari").click()
# # 点击浏览器的搜索框
# poco("URL").click()
# # 输入“airtest”
# text("airtest")
#
# # poco的滑动
# poco("People also search for").swipe([-0.0541, -0.4206])
# # 判断是否存在某个截图目标
# exists(Template(r"tpl1560844284543.png", record_pos=(-0.292, 0.688), resolution=(750, 1334)))

