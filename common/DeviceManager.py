#!usr/bin/python
# -*- coding:utf-8 -*-
import os
import re
from DataProvider import *
from Log import *
import requests

class DeviceManager(object):

    #连接的设备ID
    connectdeviceid = []

    #待测的设备对象
    testdevices = {}

    #已建立服务的设备
    serverdevices = {}

    logger = None

    @classmethod
    def get_connect_deviceid(cls):
        p = os.popen('adb devices')
        outstr = p.read()
        cls.connectdeviceid = re.findall(r'(\w+)\s+device\s',outstr)
        if 0 == len(cls.connectdeviceid):
            Log.logger.warn(u'没有adb连接的设备')
        else:
            return cls.connectdeviceid

    # Server用来获得已链接自己的服务器
    @classmethod
    def get_test_device(cls):
        for deviceid in cls.connectdeviceid:
            if DataProvider.devices.has_key(deviceid):
                cls.testdevices[deviceid] = DataProvider.devices[deviceid]
            else:
                Log.logger.warn(u'设备: %s 不在配置列表中' % deviceid)

        if len(cls.testdevices) == 0:
            Log.logger.warn(u'没有待测试的设备')


    # 客户端用来获取server上已经建立好服务的设备
    @classmethod
    def get_server_test_device(cls):
        for deviceid,device in DataProvider.devices.iteritems():
            url = "http://%s:%s/wd/hub" % (device.server,device.serverport)
            response = None
            try:
                response = requests.request("get", url)
            except requests.RequestException,e:
                pass
            if response != None:
                cls.serverdevices[deviceid] = device


if __name__ == "__main__":
    DeviceManager.get_connect_deviceid()



