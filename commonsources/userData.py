# -*- coding: utf-8 -*-
from mysqlconnect import *

class userData:

    def __init__(self):
        self.logeado = False
        self.usr = ""
        self.psw = ""
        self.lvl = 0

    def defineUPL(self,usr,psw):
        self.usr = usr
        self.psw = psw
        self.lvl = buscaDat(self.usr,'level')

    def printall (self):
        print ("Logueado = ", self.logeado)
        print ("User = ", self.usr)
        print ("Pass = ", self.psw)
        print ("Lvl = ", self.lvl)

    def testing(self):
        self.logeado = True
        self.usr = "admin"
        self.psw = "admin"
        self.lvl = 256


from Tkinter import *


def CENTRE(win,width=300, height=200):
    # get screen width and height
    screen_width = win.winfo_screenwidth()
    screen_height = win.winfo_screenheight()

    # calculate position x and y coordinates
    x = (screen_width/2) - (width/2)
    y = (screen_height/2) - (height/2)
    win.geometry('%dx%d+%d+%d' % (width, height, x, y))




