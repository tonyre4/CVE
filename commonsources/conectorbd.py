# -*- coding: utf-8 -*-
import MySQLdb as mdb
import sys
import tkMessageBox

class DBConn:

    def __init__(self):
        self.server='localhost'
        self.user='admin'
        self.pswd='admin'
        self.conn = None

def buscaDat(usr,col):
    try:
        con = mdb.connect('localhost', 'root', '85491278', 'IDs')
        cur = con.cursor()
        cur.execute("SELECT %s FROM users WHERE user='%s';" % (col,usr))
        data = cur.fetchone()
        con.close()
        if data:
            return data[0]
        else:
            return None

    except mdb.Error, e:
        showError(e)

def cambiaDat(usr,ndat,par):

    if type(ndat)==str:
        inst= "UPDATE users SET %s='%s' WHERE user='%s';" % (par,ndat,usr)
    else:
        inst = "UPDATE users SET %s=%d WHERE user='%s';" % (par, ndat, usr)

    try:
        con = mdb.connect('localhost', 'root', '85491278', 'IDs')
        cur = con.cursor()
        cur.execute(inst)
        con.close()

    except mdb.Error, e:
        showError(e)

def addusr(usr, psw, lvl):
    con = mdb.connect('127.0.0.1', 'root', '85491278', 'IDs')
    try:
        with con:
            cur = con.cursor()
            print "INSERT INTO users (user,pass,level) VALUES ('%s','%s',%i);"% (usr,psw,lvl)
            cur.execute("INSERT INTO users (user,pass,level) VALUES ('%s','%s',%i);" % (usr,psw,lvl))
            con.commit()
            con.close()
            print "exito1"
    except Exception:
        sys.exc_clear()
        try:
            with con:
                cur = con.cursor()
                print "INSERT INTO users (user,pass,level) VALUES ('%s','%s',%i);"% (usr,psw,lvl)
                cur.execute("INSERT INTO users (user,pass,level) VALUES ('%s','%s',%i);" % (usr,psw,lvl))
                con.commit()
                con.close()
                print "exito2"
        except mdb.Error, e:
            #sys.exc_clear()
            print e
            if buscaDat(usr,"pass")==None or e[0]==1062:
                showError(e)
            else:
                showInfo(["Nuevo usuario","Nuevo usuario creado satisfactoriamente"])

def showInfo(e):
    tkMessageBox.showinfo(e[0],e[1])

def showError(e):
    print "Error %d: %s" % (e.args[0], e.args[1])
    tkMessageBox.showerror("Error en base de datos", "Error %d: %s" % (e.args[0], e.args[1]))
    #sys.exit(1)


#addusr('la','a',511)