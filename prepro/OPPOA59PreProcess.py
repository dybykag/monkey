#!usr/bin/python
# -*- coding:utf-8 -*-

from BaseDevicePreProcess import *
import subprocess

class OPPOA59PreProcess (BaseDevicePreProcess):

    def __init__(self,tester):
        super(OPPOA59PreProcess, self).__init__(tester)

    def install_process(self):
        Log.logger.info(u"设备：%s 处理安装中各种弹窗" % self.tester.device.devicename)
        try:
            self.tester.find_element_by_id_and_tap('com.android.packageinstaller:id/bottom_button_two')
        except TimeoutException,e:
            traceback.print_exc()
        finally:
            try:
                # 启动app
                while self.driver.is_app_installed("com.nice.mont") == False:
                    time.sleep(2)

                self.driver.launch_app()

            except Exception, e:
                traceback.print_exc()
                DriverManager.quit_driver(self.tester.device.deviceid)
    def login_success_process(self):
        pass

    def get_permission_process(self):
        Log.logger.info(u"设备：%s 获取相机及录音权限" % self.tester.device.devicename)
        try:
            self.tester.find_element_by_id_and_tap('com.nice.mont:id/feed_open_camera')

            #摄像机权限
            self.tester.find_element_by_id_and_tap('oppo:id/remember_cb')
            self.tester.find_element_by_id_and_tap('android:id/button1')

            #录音权限
            self.tester.find_element_by_id_and_tap('oppo:id/remember_cb')
            self.tester.find_element_by_id_and_tap('android:id/button1')

            #关闭取景框
            self.tester.find_element_by_id_and_tap('com.nice.mont:id/iv_close')

        except Exception, e:
            traceback.print_exc()
            DriverManager.quit_driver(self.tester.device.deviceid)
