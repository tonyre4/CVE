# -*- coding: utf-8 -*-
from Tkinter import *
from mysqlconnect import *
from userData import *
import tkMessageBox

class pswdiag:
    def __init__(self,a,parent):
        self.parent= parent
        self.parent.iconify()
        self.a=a

        self.top = Toplevel(self.parent) #Objeto dialog
        self.top.grab_set()         #Para hacerlo modal
        self.top.title("Administrador: Iniciar Sesión")

        #Widgets constantes
        Label(self.top, text="Usuario").grid(column=0,row=0)
        Label(self.top, text="Contraseña").grid(column=0, row=1)

        #Widgets
        self.eusr = Entry(self.top)
        self.epsw = Entry(self.top,show="*")
        self.okbtn = Button(self.top, text= "Ok",command= self.compare)
        self.canbtn = Button(self.top, text="Cancelar", command= lambda: self.top.destroy())

        #Posicionando los widgets
        self.eusr.grid(column=1,row=0,columnspan=2)
        self.epsw.grid(column=1, row=1,columnspan=2)
        self.okbtn.grid(column=1,row=2)
        self.canbtn.grid(column=2, row=2)

        #binds
        self.eusr.bind('<Return>', lambda x: self.epsw.focus())
        self.epsw.bind('<Return>',self.compare)

        #focus
        self.eusr.focus()
        CENTRE(self.top,300,150)

    def compare(self,*args):
        if ( buscaDat( self.eusr.get() , "pass" ) == self.epsw.get() ) and not None:
            tkMessageBox.showinfo("Acceso permitido", "Bienvenido")
            self.top.destroy()
            self.parent.deiconify()
            self.a.inlog()
        else:
            tkMessageBox.showerror("Acceso denegado", "Usuario/contraseña incorrecto")
            self.eusr.delete(0, END)
            self.epsw.delete(0, END)
            self.eusr.focus()