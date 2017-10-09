##A este hay que hacer como una tipo clase validadora para no estar sobreescribiendo mucho codigo
# -*- coding: utf-8 -*-
from Tkinter import *
# import Tkinter
# import tkMessageBox
import re
import tkMessageBox
import ttk
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
        self.ncCalle = Entry(self.lf1)
        vcmd[9] = 'num'
        self.ncNumero = Entry(self.lf1, validate="key", validatecommand=vcmd)
        self.ncColonia = Entry(self.lf1)
        vcmd[9] = 'CP'
        self.ncCP = Entry(self.lf1, validate="key", validatecommand=vcmd)
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
        Label(self.lf1, text="Calle").grid(column=0, row=3)
        Label(self.lf1, text="Numero").grid(column=1, row=3)
        Label(self.lf1, text="Colonia").grid(column=2, row=3)
        Label(self.lf1, text="C.P.").grid(column=3, row=3)
        Label(self.lf1, text="Teléfono").grid(column=0, row=5)
        Label(self.lf1, text="Correo electrónico").grid(column=2, row=5)

        # Posicion de widgets
        self.ncNombre.grid(column=0, row=2, columnspan=2)
        self.ncRFC.grid(column=2, row=2, columnspan=2)
        self.ncCalle.grid(column=0, row=4)
        self.ncNumero.grid(column=1, row=4)
        self.ncColonia.grid(column=2, row=4)
        self.ncCP.grid(column=3, row=4)
        self.ncTel.grid(column=0, row=6)
        self.ncEmail.grid(column=2, row=6)
        self.nccrbtn.grid(column=4, row=7)
        self.ncclbtn.grid(column=3, row=7)

        self.lf1.grid()

        #Parte de Cliente existente
        self.lf2 = LabelFrame(self.top, text="Cliente existente")

        vcmd = [self.lf2.register(validador),
                '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W','']
        # Widgets
        # Nombre,RFC,Direccion,Telefono,email
        self.B = StringVar()
        self.ceBuscar = Entry(self.lf2,textvariable = self.B)
        self.ceRes = ttk.Combobox(self.lf2)
        ##initRadioButtons
        self.radioB = LabelFrame(self.lf2, text="Buscar por:")
        MODES = [
            ("Nombre", "nombre"),
            ("RFC", "rfc")
        ]
        self.v = StringVar()
        self.v.set("nombre")  # initialize

        for text, mode in MODES:
            b = Radiobutton(self.radioB, text=text,
                            variable=self.v, value=mode)
            b.pack(anchor=W)
        ##endRadioButtons
        self.ceNombre = Entry(self.lf2)
        vcmd[9] = 'RFC'
        self.ceRFC = Entry(self.lf2, validate="key", validatecommand=vcmd)
        self.ceCalle = Entry(self.lf2)
        vcmd[9] = 'num'
        self.ceNumero = Entry(self.lf2, validate="key", validatecommand=vcmd)
        self.ceColonia = Entry(self.lf2)
        vcmd[9] = 'CP'
        self.ceCP = Entry(self.lf2, validate="key", validatecommand=vcmd)
        vcmd[9] = 'tel'
        self.ceTel = Entry(self.lf2, validate="key", validatecommand=vcmd)
        vcmd[9] = 'email'
        self.ceEmail = Entry(self.lf2, validate="key", validatecommand=vcmd)
        self.cecrbtn = Button(self.lf2, text="Registrar", command=self.regcli)
        self.ceclbtn = Button(self.lf2, text="Borrar campos")#, command=self.ceborrar)

        #Binds
        self.ceRes.bind("<<ComboboxSelected>>", lambda x: self.searchPattern('box'))
        self.ceBuscar.bind("<KeyRelease>", lambda x: self.searchPattern('key'))

        # Widgets constantes
        Label(self.lf2, text="Resultados").grid(column=3, row=0)
        Label(self.lf2, text="Buscar").grid(column=0, row=1)
        Label(self.lf2, text="Nombre").grid(column=0, row=2)
        Label(self.lf2, text="RFC").grid(column=3, row=2)
        Label(self.lf2, text="Calle").grid(column=0, row=4)
        Label(self.lf2, text="Numero").grid(column=1, row=4)
        Label(self.lf2, text="Colonia").grid(column=2, row=4)
        Label(self.lf2, text="C.P.").grid(column=3, row=4)
        Label(self.lf2, text="Teléfono").grid(column=0, row=6)
        Label(self.lf2, text="Correo electrónico").grid(column=2, row=6)

        # Posicion de widgets
        self.radioB.grid(column = 3, row = 1)
        self.ceBuscar.grid(column=1, row=1)
        self.ceRes.grid(column=3, row=1)
        self.radioB.grid(column=4,row=1)
        self.ceNombre.grid(column=0, row=3, columnspan=2)
        self.ceRFC.grid(column=2, row=3, columnspan=2)
        self.ceCalle.grid(column=0, row=5)
        self.ceNumero.grid(column=1, row=5)
        self.ceColonia.grid(column=2, row=5)
        self.ceCP.grid(column=3, row=5)
        self.ceTel.grid(column=0, row=7)
        self.ceEmail.grid(column=2, row=7)
        self.cecrbtn.grid(column=4, row=8)
        self.ceclbtn.grid(column=3, row=8)

        self.lf2.grid()

    def regcli(self):
        #Obtencion de los datos
        #Ismael Antonio Davila Rodriguez = 31
        #Jesus Guadalupe Portales Zuñiga = 31

        nombre = self.ncNombre.get()
        rfc = self.ncRFC.get()
        rfc = rfc.upper()
        calle = self.ncCalle.get()
        num = self.ncNumero.get()
        cp = self.ncCP.get()
        col = self.ncColonia.get()
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

        agregaDat(['nombre','rfc','calle','num','col','cp','tel','email'],[nombre,rfc,calle,num,col,cp,tel,email],'clients','IDs')
        tkMessageBox.showinfo('Datos validos','Cliente agregado a la base de datos')
        self.ncborrar()

    def searchPattern(self,event):
        #Detecta el evento
        v = self.v.get()
        up = True
        if event=='box': #Si es seleccion del combobox
            patt= self.ceRes.get()

        else: #Si es por escribir en el buscador
            patt = self.B.get()
            l = buscaDat(None,'',v,'clients','IDs')  #Enlista todos los clientes, 'v' es para saber si es rfc o nombre
            lf = []

            if patt == '': #Si no hay nada en la barra de busqueda los enlista todos
                lf=l
            else:   #Si no busca patrones dentro
                for e in l:
                    if e.find(patt)>-1:
                        lf.append(e)

            if lf: #Si hay una lista pone todas las que hicieron match y el primer valor lo escribe en el combobox
                patt = lf[0]
                self.ceRes['values'] = lf
                self.ceRes.delete(0,'end')
                self.ceRes.insert(0,lf[0])
            else:
                up= False
                self.ceRes['values'] = []
                self.ceRes.delete(0,'end')
                self.ceRes.insert(0,'No hay resultados')



        if up:
            self.updvals(patt,v) #Para hacer update de los datos segun el patron final elegido

    def updvals(self,patt,v):
        self.ceborrar()#Borra lo que este dentro de los entrys

        if v == 'nombre': #Si el dato es un nombre
            self.ceNombre.insert(0, patt)
            self.ceRFC.insert(0,buscaDat(patt,v,'rfc','clients','IDs'))
        else: #Si es RFC
            self.ceRFC.insert(0, patt)
            self.ceNombre.insert(0,buscaDat(patt,v,'nombre','clients','IDs'))

        names = ['calle','num','col','cp','tel','email']
        data = []
        for n in names:
            data.append(buscaDat(patt,v,n,'clients','IDs'))
        for d,dd in enumerate(data):
            if not data[d]:
                data[d] = ''

        self.ceCalle.insert(0, data[0])
        self.ceNumero.insert(0, data[1])
        self.ceColonia.insert(0, data[2])
        self.ceCP.insert(0,data[3])
        self.ceTel.insert(0,data[4])
        self.ceEmail.insert(0,data[5])


    def ncborrar(self):
        self.ncNombre.delete(0,'end')
        self.ncRFC.delete(0,'end')
        self.ncCalle.delete(0,'end')
        self.ncNumero.delete(0,'end')
        self.ncColonia.delete(0,'end')
        self.ncCP.delete(0,'end')
        self.ncTel.delete(0,'end')
        self.ncEmail.delete(0,'end')

    def ceborrar(self):
        self.ceNombre.delete(0,'end')
        self.ceRFC.delete(0,'end')
        self.ceCalle.delete(0,'end')
        self.ceNumero.delete(0,'end')
        self.ceColonia.delete(0,'end')
        self.ceCP.delete(0,'end')
        self.ceTel.delete(0,'end')
        self.ceEmail.delete(0,'end')


def validador(d, i, P, s, S, v, V, W,type):
    print "d='%s'\n" % d,
    print "i='%s'\n" % i,
    print "P='%s'\n" % P, #Retorna la cadena completa
    print "s='%s'\n" % s,
    print "S='%s'\n" % S,
    print "v='%s'\n" % v,
    print "V='%s'\n" % V,
    print "W='%s'\n" % W,
    print type
    print '#\n\n'
# Disallow anything but lowercase letters
    if type=='RFC':
        return vOnlyLetters(S, P, 14, False)
    if type=='email':
        return vEmail(S,P)
    if type=='tel':
        return vOnlyNums(S, P, 11)
    if type=='CP' or type=='num':
        return vOnlyNums(S, P, 6)
    return True

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

def vOnlyNums(S, P, s):
    nc = len(P)
    if nc < s:
        if S.isdigit():
            return True
    return False

def vOnlyLetters(S, P, s,space):
    nc = len(P)
    if nc < s:
        if S.isdigit() or S.islower() or S.isupper() or (space and S==' '):
            return True

    return False
