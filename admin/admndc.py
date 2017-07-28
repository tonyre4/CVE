# -*- coding: utf-8 -*-
from Tkinter import *
import ttk
import tkMessageBox
sys.path.append('../commonsources')
from conectorbd import *

class adminctas:

    def __init__(self,parent,lvl):
        self.parent = parent
        self.lvl = "{0:b}".format(lvl)
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
        self.clbtn  = Button(self.lf1, text="Borrar", command=self.nuborrar)
        self.chk=BooleanVar()
        self.chksu  = Checkbutton(self.lf1, text= "Super Usuario", variable = self.chk )
        if self.lvl[0]=='0':
            self.chksu.config(state=DISABLED)


        #permisos
        #Nombres de programas
        self.nombres = list()
        self.nombres.append("Administrador")
        self.nombres.append("Bombas")
        self.nombres.append("Tanques")
        self.nombres.append("Crono")
        #Arreglo de checks
        self.q=len(self.nombres)
        self.C=[[0 for x in range(self.q)] for y in range(2)]
        self.Cvar = [[0 for x in range(self.q)] for y in range(2)]
        # #Frame para que se vea bien
        self.lfx = LabelFrame(self.lf1,text="Permisos")

        for i in range (0,self.q):
            Label(self.lfx, text=self.nombres[i]).grid(column=0, row=i)
            self.Cvar[0][i]=BooleanVar()
            self.C[0][i] = Checkbutton(self.lfx, text="Leer",variable = self.Cvar[0][i],command=self.prmchk)
            self.C[0][i].grid(column=1,row=i)
            if self.lvl[i + 1]=='0':
                self.C[0][i].config(state=DISABLED)
            self.Cvar[1][i] = BooleanVar()
            self.C[1][i] = Checkbutton(self.lfx, text="Escribir",variable = self.Cvar[1][i],command=self.prmchk)
            self.C[1][i].grid(column=2, row=i)
            if self.lvl[i + 2] == '0':
                self.C[1][i].config(state=DISABLED)

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
        print self.chk.get()
        print type(self.chk.get())


    def nuborrar(self):
        for i in range (0,self.q):
            self.C[0][i].deselect()
            self.C[1][i].deselect()
        self.chksu.deselect()
        self.enusr.delete (0, END)
        self.enpsw.delete (0, END)
        self.enpswc.delete(0, END)
        self.enusr.focus()

    def nucrear(self,*args):
        l=0
        for i in range(self.q):
            l += self.Cvar[0][i].get() << 7 - (i * 2)
            l += self.Cvar[1][i].get() << 7 - (i * 2) - 1
        l+= self.chk.get()<<self.q*2

        if l==0:
            tkMessageBox.showerror("Error de cuenta", "No puede ser creada una cuenta sin permisos")
            self.nuborrar()
        else:
            if self.enpsw.get()==self.enpswc.get():
                addusr(self.enusr.get(),self.enpsw.get(),l)
            else:
                tkMessageBox.showerror("Confirmacion de contraseña", "La confirmacion de contraseña no coincide")
                self.nuborrar()


    def prmchk(self): ##Checa parametros de leer y escribir
        for i in range(self.q):
            if not self.Cvar[0][i].get() and self.Cvar[1][i].get():
                self.C[0][i].deselect()
                self.C[1][i].deselect()