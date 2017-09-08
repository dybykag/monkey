#!usr/bin/python
# -*- coding:utf-8 -*-
from common.Log import *
from BaseDevicePreProcess import *
from common.DriverManager import *

class SumSingNote4PreProcess (BaseDevicePreProcess):

    def __init__(self,tester):
        super(SumSingNote4PreProcess, self).__init__(tester)

    def install_process(self):
        try:
            Log.logger.info(u"设备：%s 启动app并处理GPS弹窗" % self.tester.device.devicename)
            while self.driver.is_app_installed("com.nice.main") == False:
                time.sleep(2)

            #点击确认应用程序许可按钮
            self.tester.find_element_by_id_and_tap('com.android.settings:id/button')

            self.driver.launch_app()

        except Exception, e:
            traceback.print_exc()
            DriverManager.quit_driver(self.tester.device.deviceid)

            # 该流程包括点击login按钮到达登录页面，并登录

    def get_permission_process(self):
        try:
            Log.logger.info(u"设备：%s 获取相机及录音权限" % self.tester.device.devicename)

            while self.tester.is_element_exist('com.nice.mont:id/feed_open_camera') == False:
                self.tester.press_keycode(4)

            self.tester.find_element_by_id_and_tap('com.nice.mont:id/feed_open_camera')

            time.sleep(1)

            #关闭取景框
            self.tester.find_element_by_id_and_tap('com.nice.mont:id/iv_close')

        except Exception, e:
            DriverManager.quit_driver(self.tester.device.deviceid)
