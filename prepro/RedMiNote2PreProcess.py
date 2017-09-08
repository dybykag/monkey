#!usr/bin/python
# -*- coding:utf-8 -*-

from BaseDevicePreProcess import *
import subprocess
from common.DataProvider import *

class RedMiNote2PreProcess (BaseDevicePreProcess):

    def __init__(self,tester):
        super(RedMiNote2PreProcess, self).__init__(tester)

    def install_app(self):
        cmd = "adb -s %s install -r %s" % (self.tester.device.deviceid,DataProvider.niceapk)
        subprocess.call(cmd,shell=True)

    def install_process(self):
        try:
            Log.logger.info(u"设备：%s 安装app并处理GPS弹窗" % self.tester.device.devicename)

            #启动app
            while self.driver.is_app_installed("com.nice.mont") == False:
                time.sleep(2)

            self.driver.launch_app()
        except Exception, e:
            traceback.print_exc()
            DriverManager.quit_driver(self.tester.device.deviceid)
            # 该流程包括点击login按钮到达登录页面，并登录

    def get_permission_process(self):
        try:
            Log.logger.info(u"设备：%s 获取相机及录音权限" % self.tester.device.devicename)

            #点击拍摄按钮，进入拍摄页面
            self.tester.find_element_by_id_and_tap('com.nice.mont:id/feed_open_camera')

            #获取语音和摄像头权限
            self.tester.find_element_by_id_and_tap('com.lbe.security.miui:id/accept')
            self.tester.find_element_by_id_and_tap('com.lbe.security.miui:id/accept')

            #点击左上角的返回按钮
            self.tester.find_element_by_id_and_tap('com.nice.mont:id/iv_close')


        except Exception, e:
            traceback.print_exc()
            DriverManager.quit_driver(self.tester.device.deviceid)