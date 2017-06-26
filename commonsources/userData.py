# -*- coding: utf-8 -*-
from conectorbd import *

class userData:

    def __init__(self,usr,psw):
        self.usr=usr
        self.psw=psw
        self.lvl=buscaLvl(self.usr)
        self.logeado = False
