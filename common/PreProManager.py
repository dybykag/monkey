#!usr/bin/python
# -*- coding:utf-8 -*-

from prepro.MZM2NotePreProcess import *
from prepro.MEITU5PreProcess import *
from prepro.OPPOA59PreProcess import *
from prepro.SumSingS4PreProcess import *
from prepro.XIAOMINOTEPreProcess import *
from prepro.SumSingNote3PreProcess import *
from prepro.XIAOMI5PreProcess import *
from prepro.M57APreProcess import *
from prepro.XIAOMI2PreProcess import *
from prepro.XIAOMI3PreProcess import *
from prepro.MEIZU4PROPreProcess import *
from prepro.M3notePreProcess import *
from prepro.RedMiNote2PreProcess import *
from prepro.Nexus6PreProcess import *
from prepro.MEITUM4PreProcess import *
from prepro.VIVOX5ProPreProcess import *
from prepro.VIVOV3MAXPreProecss import *
from prepro.SumSing9152PreProcess import *
from prepro.VivoX7PreProcess import *
from prepro.HuaWeiG9PreProcess import *
from prepro.XIAOMI4PreProcess import *
from prepro.SumSingNote4PreProcess import *
from prepro.Smartosan1PreProcess import *

class PreProManager(object):

    def __init__(self,tester):
        self.tester = tester
        self.deviceid = self.tester.device.deviceid

    def device(self):
        if self.deviceid == "810EBL22MGP3":
            return MZM2NotePreProcess(self.tester)
        elif self.deviceid == "MIAGLMC6A2100083":
            return MEITU5PreProcess(self.tester)
        elif self.deviceid == "RCKVVCSO99999999":
            return OPPOA59PreProcess(self.tester)
        elif self.deviceid == "4d00f31dba19a02d":
            return SumSingS4PreProcess(self.tester)
        elif self.deviceid == "a42516eb":
            return XIAOMINOTEPreProcess(self.tester)
        elif self.deviceid == 'ee72d34d':
            return SumSingNote3PreProcess(self.tester)
        elif self.deviceid == 'b33aa57c':
            return XIAOMI5PreProcess(self.tester)
        elif self.deviceid == 'A10ABNN76XMP':
            return M57APreProcess(self.tester)
        elif self.deviceid == '4c4bb164':
            return XIAOMI2PreProcess(self.tester)
        elif self.deviceid == '0021119e':
            return XIAOMI3PreProcess(self.tester)
        elif self.deviceid == '76UBBKR224R8':
            return MEIZU4PROPreProcess(self.tester)
        elif self.deviceid == '91QEBPL694VC':
            return M3notePreProcess(self.tester)
        elif self.deviceid == 'K21GAMN5A1901310':
            return MEITUM4PreProcess(self.tester)
        elif self.deviceid == 'ZX1G22HQSB':
            return Nexus6PreProcess(self.tester)
        elif self.deviceid == 'VCOZHE6L99999999':
            return VIVOX5ProPreProcess(self.tester)
        elif self.deviceid == '174034d3':
            return VIVOV3MAXPreProcess(self.tester)
        elif self.deviceid == '91QEBP63ULCD':
            return M3notePreProcess(self.tester)
        elif self.deviceid == '410ac5dd9036c000':
            return SumSing9152PreProcess(self.tester)
        elif self.deviceid == '8d994efc':
            return VivoX7ProPreProcess(self.tester)
        elif self.deviceid == '3DN4C16411014042':
            return HuaWeiG9PreProcess(self.tester)
        elif self.deviceid == 'b3e5b28e':
            return XIAOMI4PreProcess(self.tester)
        elif self.deviceid == '8526c60c':
            return SumSingNote4PreProcess(self.tester)
        elif self.deviceid == '8c9847a5':
            return Smartosan1PreProcess(self.tester)
        elif self.deviceid == 'LJYTZ5D699999999':
            return RedMiNote2PreProcess(self.tester)