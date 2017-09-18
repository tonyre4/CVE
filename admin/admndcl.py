##A este hay que hacer como una tipo clase validadora para no estar sobreescribiendo mucho codigo
# -*- coding: utf-8 -*-
from Tkinter import *
# import Tkinter
# import tkMessageBox
import re
import tkMessageBox
sys.path.append('../commonsources')
from CMmysqlconnectV2 import *

class adminclien:
    def __init__(self, parent, lvl):
        self.lvl = '{0:09b}'.format(lvl)
        self.subool = False  ##Variable de super user
        if self.lvl[0] == '1':
            self.subool = True  ##Variable de super user
            self.read = True
            self.write = True
        else:
            self.read = False
            self.write = False
            if self.lvl[1] == '1':
                self.read = True  ##Variable de super user
                if self.lvl[2] == '1':
                    self.write = True  ##Variable de super user
        self.parent = parent
        self.top = Toplevel(self.parent)
        self.top.grab_set()
        self.top.title('Administrador de clientes')

        self.lf1 = LabelFrame(self.top, text="Nuevo cliente")

        vcmd = [self.lf1.register(validador),
                '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W','']
        # Widgets
        # Nombre,RFC,Direccion,Telefono,email
        self.ncNombre = Entry(self.lf1)
        vcmd[9] = 'RFC'
        self.ncRFC = Entry(self.lf1, validate="key", validatecommand=vcmd)
        self.ncDir = Entry(self.lf1)
        vcmd[9] = 'tel'
        self.ncTel = Entry(self.lf1, validate="key", validatecommand=vcmd)
        vcmd[9] = 'email'
        self.ncEmail = Entry(self.lf1, validate="key", validatecommand=vcmd)
        self.nccrbtn = Button(self.lf1, text="Registrar", command=self.regcli)
        self.ncclbtn = Button(self.lf1, text="Borrar campos", command=self.ncborrar)

        # Widgets constantes
        Label(self.lf1, text="(*) Campos obligatorios").grid(column=4, row=0)
        Label(self.lf1, text="Nombre *").grid(column=0, row=1)
        Label(self.lf1, text="RFC *").grid(column=3, row=1)
        Label(self.lf1, text="Dirección *").grid(column=0, row=3)
        Label(self.lf1, text="Teléfono").grid(column=0, row=5)
        Label(self.lf1, text="Correo electrónico").grid(column=2, row=5)

        # Posicion de widgets
        self.ncNombre.grid(column=0, row=2, columnspan=2)
        self.ncRFC.grid(column=2, row=2, columnspan=2)
        self.ncDir.grid(column=0, row=4, columnspan=4)
        self.ncTel.grid(column=0, row=6)
        self.ncEmail.grid(column=2, row=6)
        self.nccrbtn.grid(column=4, row=7)
        self.ncclbtn.grid(column=3, row=7)

        self.lf1.grid()

    def regcli(self):
        #Obtencion de los datos
        #Ismael Antonio Davila Rodriguez = 31
        #Jesus Guadalupe Portales Zuñiga = 31
        #Benjamin Hernandez Flores
        
        nombre = self.ncNombre.get()
        rfc = self.ncRFC.get()
        rfc = rfc.upper()
        dir = self.ncDir.get()
        tel = self.ncTel.get()
        email = self.ncEmail.get()

        e = []

        #Checar que todos los datos esten bien
        if True:
            if not validEmail(email):
                #print 'patron de email no valido'
                e.append('Correo electrónico no válido')
            if not len(tel)==0 and len(tel)<10:
                #print 'numero de tel no valido'
                e.append('El numero de telefono debe de tener 10 digitos')
            if not validRFC(rfc):
                #print 'RFC no valido'
                e.append('El RFC introducido es inválido')

            if e:
                msg = 'Verifique lo siguiente:\n'
                for err in e:
                    msg += '*'+ err + '\n'
                tkMessageBox.showerror("Error al introducir datos", msg)
                return

        agregaDat(['nombre','rfc','dir','tel','email'],[nombre,rfc,dir,tel,email],'clients','IDs')
        tkMessageBox.showinfo('Datos validos','Cliente agregado a la base de datos')
        self.ncborrar()





    def ncborrar(self):
        self.ncNombre.delete(0,'end')
        self.ncRFC.delete(0,'end')
        self.ncDir.delete(0,'end')
        self.ncTel.delete(0,'end')
        self.ncEmail.delete(0,'end')


def validador(d, i, P, s, S, v, V, W,type):
##       print "d='%s'\n" % d,
##       print "i='%s'\n" % i,
##       print "P='%s'\n" % P,
##       print "s='%s'\n" % s,
##       print "S='%s'\n" % S,
##       print "v='%s'\n" % v,
##       print "V='%s'\n" % V,
##       print "W='%s'\n" % W,
##       print '#################################\n\n'
# Disallow anything but lowercase letters
    if type=='RFC':
        return vRFC(S, P)
    if type=='email':
        return vEmail(S,P)
    if type=='tel':
        return vTel(S, P)

def vEmail(S,P):
    allowed = ['@', '.', '_', '-']
    if S=='@':
        r = len(P)
        P = P.replace('@','')
        if r-len(P)>1:
            return False
    if S.islower() or S.isupper() or S.isdigit():
        return True
    for a in allowed:
        if a == S:
            return True
    return False

def validEmail(e):
    pattern = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
    if re.match(pattern, e):
        return True
    else:
        return False

def validRFC(e):
    pattern = r'^([A-ZÑ\x26]{3,4}([0-9]{2})(0[1-9]|1[0-2])(0[1-9]|1[0-9]|2[0-9]|3[0-1]))((-)?([A-Z\d]{3}))?$'
    if re.match(pattern,e):
        return True
    else:
        return False

def vTel(S, P):
    nc = len(P)
    if nc < 11:
        if S.isdigit():
            return True
    return False

def vRFC(S,P):
    nc = len(P)
    if nc < 14:
        if S.isdigit() or S.islower() or S.isupper():
            return True
    return False
