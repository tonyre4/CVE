# -*- coding: utf-8 -*-
import MySQLdb as mdb
import sys
import tkMessageBox

def transactionIn(inst):
    try:
        con = mdb.connect('localhost', 'root', '85491278', 'IDs')
        cur = con.cursor()
        cur.execute(inst)
        con.commit()
        con.close()

    except mdb.Error, e:
        showError(e)

def transactionOut(inst,list):
    con = mdb.connect('localhost', 'root', '85491278', 'IDs')
    try:
        with con:
            cur = con.cursor()
            cur.execute(inst)
            data=cur.fetchall()

            if data==None: return None
            else:
                if list:
                    l=[]
                    k= len(data)
                    for i in range(k):
                        l.append(data[i][0])
                    return l
                else:
                    return data[0][0]
    except mdb.Error, e:
        showError(e)

def showError(e):
    print "Error %d: %s" % (e.args[0], e.args[1])
    tkMessageBox.showerror("Error en base de datos", "Error %d: %s" % (e.args[0], e.args[1]))
    #sys.exit(1)



def buscaDat(usr,par):
    if usr is not None:
        l=" WHERE user='%s';" % usr
        list=False
    else:
        l=";"
        list=True
    inst = "SELECT %s FROM users" % par + l
    return transactionOut(inst,list)

def cambiaDat(usr,par,ndat):
    if type(ndat)==str:
        inst = "UPDATE users SET %s='%s' WHERE user='%s';" % (par,ndat,usr)
    else:
        inst = "UPDATE users SET %s= %d  WHERE user='%s';" % (par, ndat, usr)
    transactionIn(inst)

def borraDat(usr):
    inst = "DELETE FROM users WHERE user='%s';" % usr
    transactionIn(inst)

def addusr(usr, psw, lvl):
    inst = "INSERT INTO users (user,pass,level) VALUES ('%s','%s',%i);" % (usr,psw,lvl)
    transactionIn(inst)
