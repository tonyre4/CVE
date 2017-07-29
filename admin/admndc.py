# -*- coding: utf-8 -*-
from Tkinter import *
import ttk
import tkMessageBox
sys.path.append('../commonsources')
from conectorbd import *

class adminctas:

    def __init__(self,parent,lvl):
        self.parent = parent
        self.lvl = "{0:09b}".format(lvl)
        #self.lvl = "11111111"

        self.top = Toplevel(self.parent)  # Objeto dialog
        self.top.grab_set()  # Para hacerlo modal
        self.top.title("Administrador de cuentas")

        self.lf1=LabelFrame(self.top,text= "Nueva cuenta")

        # Widgets constantes
        Label(self.lf1, text="Nuevo usuario").grid(column=0, row=0)
        Label(self.lf1, text="Nueva contraseña").grid(column=0, row=1)
        Label(self.lf1, text="Confirmar contraseña").grid(column=0, row=2)

        # Widgets
        self.enusr  = Entry(self.lf1)
        self.enpsw  = Entry(self.lf1, show="*")
        self.enpswc = Entry(self.lf1, show="*")
        self.crbtn  = Button(self.lf1, text="Crear", command=self.nucrear)
        self.clbtn  = Button(self.lf1, text="Borrar", command= lambda: self.nuborrar(True))
        self.chk=BooleanVar()
        self.chksu  = Checkbutton(self.lf1, text= "Super Usuario", variable = self.chk,command = self.chkchks)


        #permisos
        #Nombres de programas
        self.nombres = list()
        self.nombres.append("Administrador")
        self.nombres.append("Bombas")
        self.nombres.append("Tanques")
        self.nombres.append("Crono")
        #Arreglo de checks
        self.q=len(self.nombres)
        self.q2=self.q*2
        self.C=[[0 for x in range(self.q)] for y in range(2)]
        self.Cvar = [[0 for x in range(self.q)] for y in range(2)]
        # #Frame para que se vea bien
        self.lfx = LabelFrame(self.lf1,text="Permisos")

        if self.lvl[0]=='0':
            self.subool = False  ##Variable de super user
            self.chksu.config(state=DISABLED)
        else:
            self.subool = True

        for i in range (0,self.q):
            Label(self.lfx, text=self.nombres[i]).grid(column=0, row=i) ##Setea el nombre del permiso

            self.Cvar[0][i] = BooleanVar()
            self.C[0][i] = Checkbutton(self.lfx, text="Leer", variable=self.Cvar[0][i], command=self.prmchk)
            self.C[0][i].grid(column=1, row=i)

            self.Cvar[1][i] = BooleanVar()
            self.C[1][i] = Checkbutton(self.lfx, text="Escribir", variable=self.Cvar[1][i], command=self.prmchk)
            self.C[1][i].grid(column=2, row=i)

            if not self.subool: # checa si es su
                if self.lvl[(i*2)+1]=='0':
                    self.C[0][i].config(state=DISABLED)
                if self.lvl[(i+1)*2] == '0':
                    self.C[1][i].config(state=DISABLED)

        self.q2+=1

        # Posicionando los widgets
        self.enusr.grid (column=1, row=0, columnspan=2)
        self.enpsw.grid (column=1, row=1, columnspan=2)
        self.enpswc.grid(column=1, row=2, columnspan=2)
        self.lfx.grid   (column=0, row=3, columnspan=3)
        self.chksu.grid (column=0, row=4)
        self.crbtn.grid (column=1, row=4)
        self.clbtn.grid (column=2, row=4)

        ##Binds
        self.enusr.bind('<Return>', lambda x: self.enpsw.focus())
        self.enpsw.bind('<Return>', lambda x: self.enpswc.focus())
        self.enpswc.bind('<Return>', self.nucrear)

        self.lf1.grid()

        #######################################################
        ##Recuaddro
        self.lf2 = LabelFrame(self.top, text="Cuenta existente")

        # Widgets constantes
        Label(self.lf2, text="Usuario").grid(column=0, row=0)

        # Widgets
        self.lusr  = ttk.Combobox(self.lf2, state='readonly')
        self.ceeusr = Entry(self.lf2)
        self.chbtn = Button(self.lf2, text="Cambio", command=self.oa)
        self.upbtn = Button(self.lf2, text="Actualizar", command=self.oa)

        # Posicionando los widgets
        self.lusr.grid(column=1, row=0, columnspan=2)
        self.ceeusr.grid(column=2,row=1)
        self.chbtn.grid(column=1, row=2)
        self.upbtn.grid(column=2, row=2)

        self.lf2.grid()


    def oa(self):
        print self.ceeusr.get()
        print type(self.ceeusr.get())


    def nuborrar(self,a):
        if a:
            for i in range (0,self.q):
                self.C[0][i].deselect()
                self.C[1][i].deselect()
            self.chksu.deselect()
            self.enusr.delete(0, END)
            self.enusr.focus()
        else:
            self.enpsw.focus()
        self.enpsw.delete (0, END)
        self.enpswc.delete(0, END)
        self.chkchks()


    def nucrear(self,*args):
        ##GENERADOR DE NIVEL
        l = 0
        if self.chk.get():
            l += 1 << self.q * 2
        else:
            for i in range(self.q):
                l += self.Cvar[0][i].get() << 7 - (i * 2)
                l += self.Cvar[1][i].get() << 7 - (i * 2) - 1
            ####################

        if l==0:
            tkMessageBox.showerror("Error de cuenta", "No puede ser creada una cuenta sin permisos")
            self.nuborrar(False)
        else:
            u, p, pc = self.enusr.get(), self.enpsw.get(), self.enpswc.get()
            pl = len(p)

            if p == pc and p != "" and pl>7 and pl<30:
                if self.chk.get():
                    yn = tkMessageBox.askquestion("Nuevo super usuario","¿Desea que el nuevo usuario tenga permisos de super usuario? (Un super usuario puede modificar todo tipo de registros)",icon='warning')
                    if yn=='yes':
                        addusr(u,p,l)
                else:
                    addusr(u, p, l)
                self.nuborrar(True)
            else:
                tkMessageBox.showerror("Confirmacion de contraseña", "La confirmacion de contraseña no coincide o no se introdució una contraseña válida")
                self.nuborrar(False)


    def prmchk(self): ##Checa parametros de leer y escribir
        for i in range(self.q):
            if not self.Cvar[0][i].get() and self.Cvar[1][i].get():
                self.C[0][i].deselect()
                self.C[1][i].deselect()

    def chkchks(self):
        if self.chk.get():
            x=DISABLED
        else:
            x=ACTIVE
        for i in range (0,self.q):
            self.C[0][i].config(state=x)
            self.C[1][i].config(state=x)

