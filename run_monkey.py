#!usr/bin/python
# -*- coding:utf-8 -*-
from Server.Server import Server
from common.DeviceManager import *
from appium import webdriver
from common.PreProManager import *
from common.DriverManager import *
from common.TestCaseManager import *
from common.PublicMethod import *

def run(tester):

    DataProvider.starttime[tester.device.deviceid] = get_format_currenttime()

    # 预处理+monkey
    if PreProManager(tester).device().pre_process():
        Log.logger.info(u"设备：%s -----------------执行monkey脚本-----------------" % tester.device.devicename)
        Tester.create_monkey_result()  # 创建本次monkey结果文件夹
        suite = TestCaseManager(tester).monkey_android()
    else:
        Log.logger.info(u"设备：%s 预处理流程失败，终止相应任务" % tester.device.devicename)

    # # 预处理+自动化case
    # if PreProManager(tester).device().pre_process():
    #     Log.logger.info(u"设备：%s -----------------核心case回归测试-----------------" % tester.device.devicename)
    #
    #     suite = TestCaseManager(tester).compatibility_testsuite()
    #     unittest.TextTestRunner(verbosity=1).run(suite)
    #
    # else:
    #     Log.logger.info(u"设备：%s 预处理流程失败，终止相应任务" % tester.device.devicename)

    DataProvider.stoptime[tester.device.deviceid] = get_format_currenttime()

def init_tester_data(device, which_user):
    desired_caps = {}
    desired_caps['platformName'] = device.platformname
    desired_caps['platformVersion'] = device.platformversion
    desired_caps['deviceName'] = device.devicename
    desired_caps['unicodeKeyboard'] = "true"
    desired_caps['resetKeyboard'] = 'true'
    desired_caps['autoLaunch'] = "false"

    desired_caps['appPackage'] = 'com.nice.mont'
    desired_caps['appActivity'] = 'com.nice.mont.base.MainActivity_'
    desired_caps['udid'] = device.deviceid
    url = "http://%s:%s/wd/hub" % (device.server, device.serverport)
    driver = webdriver.Remote(url, desired_caps)

    testerobject = Tester(driver)
    testerobject.device = device
    testerobject.user = DataProvider.users[which_user]
    testerobject.logger = Log.logger
    DriverManager.drivers[device.deviceid] = driver
    return testerobject


def start_run_test():
    which_user = 0
    threads = []

    for deviceid, device in DeviceManager.serverdevices.iteritems():
        testerobject = init_tester_data(device, which_user)
        DataProvider.testers[device.deviceid] = testerobject
        try:
            thread = threading.Thread(target=run, args=(testerobject,))
            thread.start()
        except Exception, e:
            DataProvider.testers[deviceid].driver.quit()
        which_user = which_user + 1
        threads.append(thread)

    for thread in threads:
        thread.join()


def main(*args):

    # 初始化日志配置
    Log.create_log_file()

    Log.logger.info(u"加载设备及用户配置信息")
    DataProvider.init_data()

    Log.logger.info(u"获得服务器上待测试的设备")
    DeviceManager.get_server_test_device()

    if len(DeviceManager.serverdevices) == 0:
        Log.logger.info(u"服务器上没有可以测试的设备")
        sys.exit()
    else:
        for deviceid, device in DeviceManager.serverdevices.items():
            server = Server(device)
            server.list_connect_devices()

    Log.logger.info(u"开始执行任务...")
    start_run_test()

    Log.logger.info(u"-----------完成全部monkey测试--------------")
    # DriverManager.quit_all_driver()

if __name__ == '__main__':
    main()
