#!/usr/bin/python
# encoding=utf-8

"""
@Author  :  SunPeng
@Date    :  2023/11/10 13:08
@Desc    :
"""
import tidevice
import common


class App_Manager(object):
    # def __init__(self, device_id):
    #     self.device_Id = device_id

    # 获取应用
    def get_app_list(self):
        rsp = common.raw_shell("tidevice applist").split("\n")[:-1]
        app_list=[]
        for i in rsp:
            app_info = {"app_package_name": "", "app_name": "", "app_version": ""}
            app_info["app_package_name"]=i.split(" ")[0]
            app_info["app_name"]=i.split(" ")[1]
            app_info["app_version"]=i.split(" ")[2]
            app_list.append(app_info)
        return app_list

    # app安装
    def install_app(self,file_path):
        rsp = common.raw_shell("tidevice install"+file_path)

    # app卸载
    def un_install_app(self,file_path):
        rsp = common.raw_shell("tidevice uninstall"+file_path)


if __name__ == '__main__':
    app_m = App_Manager()
    print(app_m.get_app_list())
