#!usr/bin/python
# -*- coding:utf-8 -*-

from BaseDevicePreProcess import *

class HuaWeiG9PreProcess (BaseDevicePreProcess):

    def __init__(self,tester):
        super(HuaWeiG9PreProcess, self).__init__(tester)

    def install_app(self):
        cmd = "adb -s %s install -r %s" % (self.tester.device.deviceid, DataProvider.niceapk)
        subprocess.call(cmd, shell=True)

    # 开始预处理流程
    def pre_process(self):
        Log.logger.info(u"设备：%s 开始预处理流程..." % self.tester.device.devicename)
        driver = self.tester.driver
        try:
            if driver.is_app_installed('com.nice.mont'):
                Log.logger.info(u"设备：%s 卸载老的nice包" % self.tester.device.devicename)
                driver.remove_app('com.nice.mont')

            time.sleep(5)
            if self.tester.is_element_exist('android:id/button1'):
                self.tester.find_element_by_id_and_tap('android:id/button1')

            Log.logger.info(u"设备：%s 开始安装测试的nice包" % self.tester.device.devicename)
            thread = threading.Thread(target=self.install_process)
            thread.start()
            self.install_app()
            thread.join()
            Log.logger.info(u"设备：%s 启动成功" % self.tester.device.devicename)
            self.login_process()
            Log.logger.info(u"设备：%s 登录成功" % self.tester.device.devicename)
            self.login_success_process()
            self.get_permission_process()

        except  Exception, e:
            traceback.print_exc()
            DriverManager.quit_driver(self.tester.device.deviceid)
            return False
        return True

    def install_process(self):
        try:
            Log.logger.info(u"设备：%s 启动app并处理GPS弹窗" % self.tester.device.devicename)

            if self.tester.is_element_exist('com.android.packageinstaller:id/decide_to_continue',10) == True:
                self.tester.find_element_by_id_and_tap('com.android.packageinstaller:id/decide_to_continue')
                self.tester.find_element_by_id_and_tap('com.android.packageinstaller:id/goinstall')

            elif self.tester.is_element_exist('com.android.packageinstaller:id/ok_button',10) == True:
                self.tester.find_element_by_id_and_tap('com.android.packageinstaller:id/ok_button')

            else :
                print 'error!'
        except Exception,e:
            traceback.print_exc()

        finally:
            while self.driver.is_app_installed("com.nice.mont") == False:
                time.sleep(2)

            self.driver.launch_app()

            #获取定位权限
            self.tester.find_element_by_id_and_tap('com.huawei.systemmanager:id/btn_allow')

    def login_success_process(self):
        pass

    def get_permission_process(self):
        Log.logger.info(u"设备：%s 获取相机及录音权限" % self.tester.device.devicename)
        try:

            self.tester.find_element_by_id_and_tap('com.nice.mont:id/feed_open_camera')

            self.tester.find_element_by_id_and_tap('com.android.packageinstaller:id/do_not_ask_checkbox')
            self.tester.find_element_by_id_and_tap('com.android.packageinstaller:id/permission_allow_button')

            self.tester.find_element_by_id_and_tap('com.android.packageinstaller:id/do_not_ask_checkbox')
            self.tester.find_element_by_id_and_tap('com.android.packageinstaller:id/permission_allow_button')

            self.tester.find_element_by_id_and_tap('com.android.packageinstaller:id/do_not_ask_checkbox')
            self.tester.find_element_by_id_and_tap('com.android.packageinstaller:id/permission_allow_button')

            time.sleep(2)

            # 关闭取景框
            self.tester.find_element_by_id_and_tap('com.nice.mont:id/iv_close')


        except Exception, e:
            traceback.print_exc()
            DriverManager.quit_driver(self.tester.device.deviceid)