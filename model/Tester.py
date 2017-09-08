#!usr/bin/python
# -*- coding:utf-8 -*-
import os
import subprocess
from appium.webdriver.common.touch_action import TouchAction
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.remote.webelement import *
from common.DataProvider import *
from Server.Server import Server
from common.DeviceManager import *
import time
import platform
import tempfile
import shutil
import math
import operator
# from PIL import Image
from common.PublicMethod import *

PATH = lambda p: os.path.abspath(p)
TEMP_FILE = PATH(tempfile.gettempdir() + "/temp_screen.png")

class Tester(object):
    def __init__(self, driver):
        self._driver = driver
        self._user = None
        self._device = None
        self._logger = None
        self.action = TouchAction(self._driver)
        self._screenshot_path = ""
        self.device_width = self._driver.get_window_size()['width']
        self.device_height = self._driver.get_window_size()['height']

    @property
    def driver(self):
        return self._driver

    @driver.setter
    def driver(self, value):
        self._driver = value

    @property
    def screenshot_path(self):
        return self._screenshot_path

    @screenshot_path.setter
    def screenshot_path(self, value):
        self._screenshot_path = value

    @property
    def user(self):
        return self._user

    @user.setter
    def user(self, value):
        self._user = value

    @property
    def device(self):
        return self._device

    @device.setter
    def device(self, value):
        self._device = value

    @property
    def logger(self):
        return self._logger

    @logger.setter
    def logger(self, value):
        self._logger = value

    def long_press_screen(self, eleid, duration):
        el = self.driver.find_element_by_id(eleid)
        time.sleep(1)
        self.logger.info(u"设备：%s 长按控件 %s %s 毫秒" % (self.device.devicename, eleid, duration))
        self.action.long_press(el).wait(duration).release().perform()

    def tap_screen(self, x, y):
        self.logger.info(u"设备：%s tap screen point at x:%s y:%s" % (self.device.devicename,x,y))
        self.action.tap(None, x, y).perform()

    def find_element_by_id_and_tap(self, eleid, timeout=300):
        self.logger.info(u"设备：%s start tap element id:%s" % (self.device.devicename, eleid))
        if self.wait_element_id_display(self.driver, eleid, eleid, timeout):
            element = self.driver.find_element_by_id(eleid)
            self.action.tap(element).perform()
            self.logger.info(u"设备：%s tap element id:%s success" % (self.device.devicename, eleid))

    def find_element_by_uiautomator_and_tap(self, uiselector, timeout=300):
        self.logger.info(u"设备：%s start tap element uiselector:%s" % (self.device.devicename, uiselector))
        if self.wait_element_uiautormator_display(self.driver, uiselector, uiselector, timeout):
            element = self.driver.find_element_by_android_uiautomator(uiselector)
            self.action.tap(element).perform()
            self.logger.info(u"设备：%s tap element uiselector:%s success" % (self.device.devicename, uiselector))

    def find_element_by_id_and_send_keys(self, eleid, text, timeout=300):
        self.logger.info(u"设备：%s start send_key %s to element id:%s" % (self.device.devicename, text, eleid))
        if self.wait_element_id_display(self.driver, eleid, eleid, timeout):
            element = self.driver.find_element_by_id(eleid)
            element.send_keys(text)
            self.logger.info(u"设备：%s send_key text:%s to element id:%s success "
                             % (self.device.devicename, text, eleid))

    def find_element_by_class_name_and_tap(self, class_name, timeout=300):
        self.logger.info(u"设备：%s start tap element class name:%s" % (self.device.devicename, class_name))
        if self.wait_element_id_display(self.driver, class_name, class_name, timeout):
            element = self.driver.find_element_by_class_name(class_name)
            self.action.tap(element).perform()
            self.logger.info(u"设备：%s tap element id:%s success" % (self.device.devicename, class_name))

    def wait_element_id_display(self, driver, idstr, msg, timeout=300):
        try:
            return WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.ID, idstr)), msg)
        except TimeoutException, e:
            raise

    def wait_element_uiautormator_display(self, driver, uiselector, msg, timeout=300):
        try:
            return WebDriverWait(driver, timeout).until(lambda dr: dr.find_element_by_android_uiautomator(uiselector).is_displayed())
        except TimeoutException, e:
            raise

    def find_element_by_xpath_and_tap(self, xpath):
        self.logger.info(u"设备：%s find by xpath:%s" % (self.device.devicename, xpath))
        element = self.driver.find_element_by_xpath(xpath)
        self.action.tap(element).perform()

    def wait_element(self, eleid, timeout=300):
        self.logger.info(u"设备：%s wait element: %s" % (self.device.devicename, eleid))
        if self.wait_element_id_display(self.driver, eleid, eleid, timeout):
            self.logger.info(u"设备：%s element id have displayed:%s" % (self.device.devicename, eleid))
        else:
            self.logger.info(u"设备：%s Timeout: wait element %s" % (self.device.devicename, eleid))

    def press_keycode(self, keycode, metastate=None):
        """发送keycode到设备中。仅限Android设备
        更多关于keycode请参考
        http://developer.android.com/reference/android/view/KeyEvent.html.

        :Args:
         - keycode - 要发送的keycode值
         - metastate - meta information about the keycode being sent
        :Usage:
            self.tester.press_keycode(24)
        """
        self.logger.info(u"设备：%s [action]按系统按键(keycode='%s')"
                         % (self.device.devicename, keycode))
        self.driver.press_keycode(keycode)

    # 目前系统的keycode按键长按只有500ms，暂时并不符合需求
    def long_press_keycode(self, keycode, metastate=None):
        """发送长按keycode事件到设备中。仅限Android设备
        Android only.

        :Args:
         - keycode - 要发送的keycode值
         - metastate - meta information about the keycode being sent
        :Usage:
            self.tester.long_press_keycode(24)
        """
        self.logger.info(u"设备：%s [action]长按系统按键(keycode='%s')"
                         % (self.device.devicename, keycode))
        self.driver.long_press_keycode(keycode)

    def swipe_left(self, duration=None):
        """Perform a swipe left full screen width

        :Args:
            - None
        :Usage:
            self.tester.swipe_left()
        """
        self.logger.info(u"设备：%s [action]向左滑动屏幕 " % self.device.devicename)
        startx = self.device_width - 10
        starty = self.device_height/2
        endx = 10
        endy = self.device_height/2
        self.driver.swipe(startx, starty, endx, endy)
        time.sleep(2)

    def swipe_right(self, duration=None):
        """Perform a swipe right full screen width

        :Args:
            - None
        :Usage:
            self.tester.swipe_right()
        """
        self.logger.info(u"设备：%s [action]向右滑动屏幕 " % self.device.devicename)
        startx = 10
        starty = self.device_height/2
        endx = self.device_width - 10
        endy = self.device_height/2
        self.driver.swipe(startx, starty, endx, endy)
        time.sleep(2)

    def swipe_down(self, duration=None):
        """Perform a swipe down full screen width

        :Args:
            - None
        :Usage:
            self.tester.swipe_down()
        """
        self.logger.info(u"设备：%s [action]向上滑动屏幕 " % self.device.devicename)
        startx = self.device_width/2
        starty = self.device_height - self.device_height/3
        endx = self.device_width/2
        endy = 10
        self.driver.swipe(startx, starty, endx, endy)
        time.sleep(2)

    def is_element_exist(self, element, timeout=1):
        """判断元素是否存在，存在返回True，不存在返回False
        增加timeout超时等待，默认为1次，可通过传的参数覆盖

        :Args:
            - element - 要查找的元素
        :Usage:
            self.tester.is_element_exist('com.nice.main:id/beauty_auto')  # 美颜按钮
        """
        self.logger.info(u"设备：%s 查找控件 %s" % (self.device.devicename, element))
        count = 0
        while count < timeout:
            source = self.driver.page_source
            if element in source:
                self.logger.info(u"设备：%s 找到控件: %s" % (self.device.devicename, element))
                return True
            else:
                count += 1
                time.sleep(1)
        self.logger.info(u"设备：%s 未找到控件: %s" % (self.device.devicename, element))
        return False

    def get_center_coor_and_tap(self, element):
        x = element.location['x']
        y = element.location['y']
        width = element.size['width']
        height = element.size['height']
        x = x + width / 2
        y = y + height / 2
        time.sleep(1)
        self.tap_screen(x, y)

    def is_autotest_exit(self):
        """初始话设备时，判断是否存在autotest测试图片
        :Usage:
            self.pull_file_to_device  # 美颜按钮
        """
        cmd = "adb -s %s shell ls /sdcard/DCIM/ | grep autotest" % self.device.deviceid
        result = "autotest"
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE,
                             stdin=subprocess.PIPE, shell=True)
        (output, err) = p.communicate()
        if output.strip('\r\n') == result:
            self.logger.info(u"设备：%s SD中存在测试图片 " % self.device.deviceid)
            return True
        else:
            self.logger.info(u"设备：%s SD中不存在测试图片 " % self.device.deviceid)
            return False

    def pull_file_to_device(self):
        """初始话设备时，拷贝图片进入设备
        :Usage:
            self.pull_file_to_device  # 美颜按钮
        """
        path = os.getcwd()+'/res/autotest'
        cmd = "adb -s %s push %s /sdcard/DCIM/" % (self.device.deviceid, path)
        subprocess.Popen(cmd, shell=True)
        time.sleep(10)

    def refresh_test_pic(self):
        """初始话设备时，刷新系统图库，是autotest文件可见
        :Usage:
            self.tester.refresh_test_pic()  # 美颜按钮
        """
        img_src = "/Users/johnhao/Documents/code/autotest/appium_python_android/res/autotest"
        path = get_file_name_from_path(img_src, 'jpg')
        for i in range(len(path)):
            cmd = "adb -s %s shell am broadcast -a android.intent.action.MEDIA_SCANNER_SCAN_FILE -d file:///storage/emulated/0/DCIM/autotest/%s.jpg" % (self.device.deviceid, path[i])
            subprocess.Popen(cmd, shell=True)
            i += 1

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~常用case步骤~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def back_to_feed(self):
        """用户case结束后回到Feed首页
        :Usage:
            self.tester.back_to_feed()
        """
        if self.is_element_exist('com.nice.main:id/btnTabSubscription'):
            time.sleep(1)
        else:
            self.driver.close_app()
            self.logger.info(u"设备：%s close app " % self.device.devicename)
            time.sleep(5)
            self.driver.launch_app()
            self.logger.info(u"设备：%s restart app " % self.device.devicename)
            time.sleep(10)

    def screenshot(self, name):
        path = "%s/%s.png" % (self.screenshot_path, name)
        self.driver.save_screenshot(path)
        self.logger.info(u"设备：%s screen shot at path:%s" % (self.device.devicename, path))

    def screenshot2(self, name):
        path = "%s/%s.jpg" % (self.screenshot_path, name)
        self.driver.save_screenshot(path)
        self.logger.info(u"设备：%s screen shot at path:%s" % (self.device.devicename, path))

    def get_verify_code(self):
        """获取当前手机号的短信验证码
        :Usage:
            self.tester.get_verify_code()
        """
        getverifycode = os.getcwd() + '/getverifycode.sh'
        sinput = "sh %s %s" % (getverifycode, self.user.mobile)
        myproc = subprocess.Popen(sinput, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        strout = myproc.stdout.read().decode("utf-8")
        code = strout.strip()
        self.logger.info(u"设备：%s 登陆验证码为:%s " % (self.device.devicename, code))

        if not code:
            print "获取验证码失败,35s后自动重试！！！"
            self.find_element_by_id_and_tap('com.nice.mont:id/btn_obtain_verify_code')
            time.sleep(35)
            getverifycode = os.getcwd() + '/getverifycode.sh'
            sinput = "sh %s %s" % (getverifycode, self.user.mobile)
            myproc = subprocess.Popen(sinput, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
            strout = myproc.stdout.read().decode("utf-8")
            code = strout.strip()
            self.logger.info(u"设备：%s 登陆验证码为:%s " % (self.device.devicename, code))


        return code

    def longin_with_verifycode(self):
        # 处理登录mont的验证码
        code = self.get_verify_code()
        time.sleep(5)

        self.find_element_by_id_and_send_keys('com.nice.mont:id/verify_code_num', code)
        time.sleep(2)

    def edittextclear(self, text):
        self.driver.keyevent(123)

        for i in range (0,len(text)):
            self.driver.keyevent(67)

    # 定义一个类变量，用于创建monkey结果文件夹
    monkey_result_path = ""

    @classmethod
    def create_monkey_result(cls):
        cls.monkey_result_path = os.getcwd() + '/Monkey_log/%s' % get_format_currenttime()
        os.mkdir(cls.monkey_result_path)

        print '本次monkey结果文件创建成功'

    def run_monkey(self):
        cmd = "adb -s %s shell monkey -p com.nice.mont -v -v --throttle 200 --pct-motion 30 --pct-trackball 30 --pct-touch 10 --pct-appswitch 10 --ignore-crashes --ignore-timeouts --ignore-security-exceptions " \
              "--monitor-native-crashes 50000 >%s/%s.log" % (self.device.deviceid,self.monkey_result_path,self.device.devicename)
        subprocess.call(cmd, shell=True)
        print 'monkey done'