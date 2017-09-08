#!usr/bin/python
# -*- coding:utf-8 -*-

from XIAOMINOTEPreProcess  import *


class  XIAOMI5PreProcess (BaseDevicePreProcess):

    def __init__(self,tester):
        super(XIAOMI5PreProcess, self).__init__(tester)

    def install_process(self):
        try:
            Log.logger.info(u"设备：%s 启动app并处理GPS弹窗" % self.tester.device.devicename)

            while self.driver.is_app_installed("com.nice.mont") == False:
                time.sleep(2)

            self.driver.launch_app()
        except Exception, e:
            traceback.print_exc()
            DriverManager.quit_driver(self.tester.device.deviceid)

    def get_permission_process(self):
        Log.logger.info(u"设备：%s 获取相机及录音权限" % self.tester.device.devicename)
        try:
            #调起拍摄页面
            self.tester.find_element_by_id_and_tap('com.nice.mont:id/feed_open_camera')

            #各种权限授权
            self.tester.find_element_by_id_and_tap('android:id/button1')
            self.tester.find_element_by_id_and_tap('android:id/button1')
            self.tester.find_element_by_id_and_tap('android:id/button1')

            # 关闭取景框
            self.tester.find_element_by_id_and_tap('com.nice.mont:id/iv_close')

        except Exception, e:
            traceback.print_exc()
            DriverManager.quit_driver(self.tester.device.deviceid)

