# -*- coding: utf-8 -*-
import MySQLdb as mdb
import sys
import tkMessageBox

def buscaDat(usr,col):

    if usr is not None:
        l=" WHERE user='%s';" % usr
    else:
        l=";"

    try:
        con = mdb.connect('localhost', 'root', '85491278', 'IDs')
        cur = con.cursor()
        cur.execute("SELECT %s FROM users" % col + l)

        if usr is not None:
            data = cur.fetchone()
        else:
            data = cur.fetchall()

        con.close()

        if data:
            if usr is not None:
                return data[0]
            else:
                l=[]
                for i in range(len(data)):
                    l.append(data[i][0])
                return l
        else:
            return None

    except mdb.Error, e:
        showError(e)


def cambiaDat(usr,par,ndat):

    if type(ndat)==str:
        inst = "UPDATE users SET %s='%s' WHERE user='%s';" % (par,ndat,usr)
    else:
        inst = "UPDATE users SET %s= %d  WHERE user='%s';" % (par, ndat, usr)

    print inst

    try:
        con = mdb.connect('localhost', 'root', '85491278', 'IDs')
        cur = con.cursor()
        cur.execute(inst)
        con.commit()
        con.close()

    except mdb.Error, e:
        showError(e)

def borraDat(usr):

    inst = "DELETE FROM users WHERE user='%s';" % usr

    try:
        con = mdb.connect('localhost', 'root', '85491278', 'IDs')
        cur = con.cursor()
        cur.execute(inst)
        con.commit()
        con.close()

    except mdb.Error, e:
        showError(e)

def addusr(usr, psw, lvl):
    con = mdb.connect('127.0.0.1', 'root', '85491278', 'IDs')
    try:
        with con:
            cur = con.cursor()
            cur.execute("INSERT INTO users (user,pass,level) VALUES ('%s','%s',%i);" % (usr,psw,lvl))
            con.commit()
            con.close()
    except Exception:
        sys.exc_clear()
        try:
            with con:
                cur = con.cursor()
                cur.execute("INSERT INTO users (user,pass,level) VALUES ('%s','%s',%i);" % (usr,psw,lvl))
                con.commit()
                con.close()
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