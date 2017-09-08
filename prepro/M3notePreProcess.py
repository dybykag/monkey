#!usr/bin/python
# -*- coding:utf-8 -*-

from BaseDevicePreProcess import *
import subprocess
from common.DataProvider import *

class M3notePreProcess (BaseDevicePreProcess):

    def __init__(self,tester):
        super(M3notePreProcess, self).__init__(tester)

    #魅族情况太特殊，安装都得继承然后单独处理,弹出的adb安装权限直接阻塞了Server运行
    def install_app(self):
        cmd = "adb -s %s install -r %s" % (self.tester.device.deviceid,DataProvider.niceapk)
        subprocess.call(cmd,shell=True)

    def install_process(self):
        try:
            Log.logger.info(u"设备：%s 安装app并处理GPS弹窗" % self.tester.device.devicename)
            time.sleep(1)

            #adb安装权限
            try:
                if self.tester.is_element_exist('android:id/button1',10):
                    self.tester.find_element_by_id_and_tap('android:id/button1')
            except:
                Log.logger('没出现USB确认弹框')
            finally:
                #启动app
                while self.driver.is_app_installed("com.nice.mont") == False:
                    time.sleep(2)

                self.driver.launch_app()

        except Exception, e:
            traceback.print_exc()
            DriverManager.quit_driver(self.tester.device.deviceid)

    def get_permission_process(self):
        try:
            Log.logger.info(u"设备：%s 获取相机及录音权限" % self.tester.device.devicename)


            self.tester.find_element_by_id_and_tap('com.nice.mont:id/feed_open_camera')

            #通讯录权限
            self.tester.find_element_by_id_and_tap('android:id/button1')
            #录音权限
            self.tester.find_element_by_id_and_tap('android:id/button1')

            #关闭取景框
            self.tester.find_element_by_id_and_tap('com.nice.mont:id/iv_close')

        except Exception, e:
            traceback.print_exc()
            DriverManager.quit_driver(self.tester.device.deviceid)
