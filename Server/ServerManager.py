#!usr/bin/python
# -*- coding:utf-8 -*-

from common.Log import *
from Server import *
from common.DeviceManager import *
import threading

class ServerManager:
    def __init__(self):

        self.testdevices = DeviceManager.testdevices
        self.serverobjects = []
        self.threads = []

    def start_all_server(self):
        for deviceid,device in self.testdevices.iteritems():
            server = Server(device)
            self.serverobjects.append(server)
            thread1 = threading.Thread(target=server.start)
            thread1.start()

    def stop_all_server(self):
        for server in self.serverobjects:
            server.stop()

    def list_devices(self):
        for deviceid,device in self.testdevices.iteritems():
            server = Server(device)
            server.list_connect_devices()



