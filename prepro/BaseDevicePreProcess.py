#!usr/bin/python
# -*- coding:utf-8 -*-

from common.DataProvider import *
from common.Log import *

import threading
import traceback
from common.DriverManager import *
from appium.webdriver.common.touch_action import TouchAction
import time
from appium.webdriver.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from model.Tester import *


class BaseDevicePreProcess(object):

    def __init__(self,tester):
        self.tester = tester
        self.driver = self.tester.driver
        self.action = TouchAction(self.driver)
        self.user = self.tester.user


    # 开始预处理流程
    def pre_process(self):
        Log.logger.info(u"设备：%s 开始预处理流程..." % self.tester.device.devicename)
        driver = self.tester.driver
        try:
            # print 'debug ing '
            if driver.is_app_installed('com.nice.mont'):
                Log.logger.info(u"设备：%s 卸载老的nice包" % self.tester.device.devicename)
                driver.remove_app('com.nice.mont')
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

            Log.logger.info(u"设备：%s 预处理成功，开始执行Monkey测试" % self.tester.device.devicename)
        except  Exception, e:
            traceback.print_exc()
            DriverManager.quit_driver(self.tester.device.deviceid)
            return False
        return True

    # 安装流程
    def install_app(self):
        self.driver.install_app(DataProvider.niceapk)

    # 该流程包括处理安装及启动过程中的各种弹窗，一直到可以点击login按钮
    def install_process(self):
        pass

    # 该流程包括点击login按钮到达登录页面，并登录
    def login_process(self):
        Log.logger.info(u"设备：%s 开始登录，使用账号:%s" % (self.tester.device.devicename, self.tester.user.mobile))
        try:

            time.sleep(2)
            if self.tester.is_element_exist('com.nice.mont:id/img',3) == True:
                self.tester.press_keycode(4)  # 如果有引导，则干掉引导

            # 调起手机号登录页面
            self.tester.find_element_by_id_and_tap('com.nice.mont:id/circle_avatar')
            self.tester.find_element_by_id_and_tap('com.nice.mont:id/btn_phone_login')

            if self.tester.is_element_exist('com.nice.mont:id/phone_number',5):
                print 'you zhege zhi!!!!!!'

            #login_phone_number_element = self.tester.find_element_by_id('com.nice.main:id/phone_number', 2)

            # 输入手机号，点击获取验证码
            #login_phone_number_element.send_keys(self.user.mobile)
            self.tester.find_element_by_id_and_tap('com.nice.mont:id/phone_number')
            time.sleep(1)

            self.tester.find_element_by_id_and_send_keys('com.nice.mont:id/phone_number', self.user.mobile)

            #点击获取验证码
            self.tester.find_element_by_id_and_tap('com.nice.mont:id/btn_obtain_verify_code')

            # 获取验证码后输入验证码
            time.sleep(1)
            self.tester.find_element_by_id_and_send_keys('com.nice.mont:id/verify_code_num','123456')

            # 点击登录按钮
            time.sleep(1)
            self.tester.find_element_by_id_and_tap('com.nice.mont:id/login')

        except Exception, e:
            raise

    # 该流程包括登录成功后，对各种自动弹出对话框进行处理
    def login_success_process(self):
        pass

    # 对所有需要的权限进行处理，例如：相机、录音
    def get_permission_process(self):
        pass








