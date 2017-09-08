#coding=utf-8
from BaseDevicePreProcess import *


class XIAOMI2PreProcess (BaseDevicePreProcess):

    def __init__(self,tester):
        super(XIAOMI2PreProcess, self).__init__(tester)

    def install_app(self):
        cmd = "adb -s %s install -r %s" % (self.tester.device.deviceid,DataProvider.niceapk)
        subprocess.call(cmd,shell=True)

    def install_process(self):

        self.tester.find_element_by_id_and_tap('com.miui.securitycenter:id/do_not_ask_checkbox')
        self.tester.find_element_by_id_and_tap('android:id/button2')

        try:
            Log.logger.info(u"设备：%s 启动app并处理GPS弹窗" % self.tester.device.devicename)
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
            # 点击拍摄按钮，进入拍摄页面
            self.tester.find_element_by_id_and_tap('com.nice.mont:id/feed_open_camera')

            # 录音权限
            self.tester.find_element_by_id_and_tap('android:id/button1')

            #相机开启失败，点击知道了
            self.tester.find_element_by_id_and_tap('com.nice.mont:id/btn_ok')

        except Exception, e:
            traceback.print_exc()
            DriverManager.quit_driver(self.tester.device.deviceid)

