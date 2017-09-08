#!usr/bin/python
# -*- coding:utf-8 -*-

import sys
import os
sys.path.append('..')
from common.BaseTestCase import *
from common.Log import *

class test_kaka_core_case(BaseTestCase):
    @classmethod
    def setUpClass(cls):
        pass

    def setUp(self):
        pass

    def test_shoot_video(self):

        self.tester.find_element_by_id_and_tap('com.nice.mont:id/feed_open_camera')

        self.tester.long_press_screen('com.nice.mont:id/btn_record',5000)

        self.tester.find_element_by_id_and_tap('com.nice.mont:id/iv_nextstep')

        self.tester.find_element_by_id_and_tap('com.nice.mont:id/btn_publish')



    def tearDown(self):
        pass

    @classmethod
    def tearDownClass(cls):
        pass
