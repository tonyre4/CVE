# -*- coding: utf-8 -*-
from conectorbd import *

class userData:

    def __init__(self):
        self.logeado = False
        self.usr = ""
        self.psw = ""
        self.lvl = 0

    def defineUPL(self,usr,psw):
        self.usr = usr
        self.psw = psw
        self.lvl = buscaLvl(self.usr)

    def printall (self):
        print ("Logueado = ", self.logeado)
        print ("User = ", self.usr)
        print ("Pass = ", self.psw)
        print ("Lvl = ", self.lvl)

    def testing(self):
        self.logeado = True
        self.usr = "admin"
        self.psw = "admin"
        self.lvl = 511