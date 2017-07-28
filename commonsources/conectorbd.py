# -*- coding: utf-8 -*-
import MySQLdb as mdb
import sys
import tkMessageBox

def buscaPass(usr):
    try:
        con = mdb.connect('localhost', 'admin', 'admin', 'IDs')
        cur = con.cursor()
        cur.execute("SELECT pass FROM users WHERE user='%s';" % usr)
        data = cur.fetchone()
        con.close()
        if data:
            return data[0]
        else:
            return None

    except mdb.Error, e:
        showError(e)

def buscaLvl(usr):
    try:
        con = mdb.connect('localhost', 'admin', 'admin', 'IDs')
        cur = con.cursor()
        cur.execute("SELECT level FROM users WHERE user='%s';" % usr)
        data = cur.fetchone()
        con.close()
        if data:
            return data[0]
        else:
            return None

    except mdb.Error, e:
        showError(e)

def cambiaPass(usr,nPsw):
    try:
        con = mdb.connect('localhost', 'admin', 'admin', 'IDs')
        cur = con.cursor()
        cur.execute("UPDATE users SET pass='%s' WHERE user='%s';" % (nPsw,usr))
        con.close()

    except mdb.Error, e:
        showError(e)

def showError(e):
    print "Error %d: %s" % (e.args[0], e.args[1])
    tkMessageBox.showerror("Error en base de datos", "Error %d: %s" % (e.args[0], e.args[1]))
    sys.exit(1)

def addusr(a,b,c):
    print a,b,c