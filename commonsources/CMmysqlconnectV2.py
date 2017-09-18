# -*- coding: utf-8 -*-
import MySQLdb as mdb
import tkMessageBox

sqlserver = 'localhost'
sqluser = 'root'
sqlpsw = '85491278'

def transactionIn(inst,database):
    try:
        con = mdb.connect(sqlserver, sqluser, sqlpsw, database)
        cur = con.cursor()
        cur.execute(inst)
        con.commit()
        con.close()

    except mdb.Error, e:
        showError(e)

def transactionOut(inst, list, database):
    con = mdb.connect(sqlserver, sqluser, sqlpsw, database)
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


def buscaDat(pattern, colpattern, column, table, database):
##What pattern,what column has the pattern,column of desired data,table that is located,database where is located
    inst = "SELECT %s FROM %s" % (column,table)
    if pattern is not None or pattern == '':
        inst = inst + " WHERE %s='%s'" % (colpattern,pattern)
        list=False
    else:
        list=True
    inst = inst + ";"
    return transactionOut(inst,list,database)

def cambiaDat(pattern, colpattern, column, newdata, table, database):
    if switchforstrings(column):
        newdata = addcoutes(newdata)
    if switchforstrings(colpattern):
        pattern = addcoutes(pattern)
    inst = 'UPDATE %s SET %s=%s WHERE %s=%s;' % (table, column, newdata, colpattern, pattern)
    transactionIn(inst,database)

##Arreglar esto con otra funcion que saque el tipo de dato desde mysql
def switchforstrings(column):
    strtypes = ('user','pass','nombre','rfc','dir','tel','email')  ## AGREGAR AQUI TODOS LOS TIPOS DE DATOS QUE SERAN STRs
    for t in strtypes:
        if column == t:
            return True
    else:
        return False

def addcoutes(string):
    return "'" + str(string) + "'"

def borraDat(pattern, colpattern, table, database):
    inst = "DELETE FROM %s WHERE %s='%s';" % (table, colpattern,pattern)
    transactionIn(inst,database)

def agregaDat(names, values, table, database):

    inst = "INSERT INTO %s (" % table
    strflags = []

    first=True
    for n in names:
        strflags.append(switchforstrings(n))
        if first:
            b=''
        else:
            b=','
        inst = inst + b + str(n)
        first = False

    inst= inst + ") VALUES ("

    for i in range(len(values)):
        if i == 0:
            b=''
        else:
            b=','

        values[i] = str(values[i])
        if strflags[i]:
            values[i] = addcoutes(values[i])

        inst = inst + b + values[i]

    inst = inst + ");"
    print inst
    transactionIn(inst,database)

