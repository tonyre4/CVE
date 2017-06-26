# -*- coding: utf-8 -*-
from Tkinter import *
import tkMessageBox
import sys
sys.path.append('../commonsources')
from conectorbd import *



class adminMain:

    def __init__(self):
        #Declaracion de la ventana
        self.root = Tk()
        self.root.title("egas - bombas")
        #Delcaracion del menu
        self.menubar = Menu(self.root) #Objeto principal de menus
        self.cuentamenu= Menu(self.menubar,tearoff=0) #Objeto de menu para la cascada
        self.cuentamenu.add_command(label="Iniciar sesión", command=self.oppsw)
        self.cuentamenu.add_command(label="Salir", command=self.close)
        self.ayudamenu= Menu(self.menubar,tearoff=0)#Objeto del menu para la cascada
        self.ayudamenu.add_command(label= "Acerca de...")
        self.ayudamenu.add_command(label= "Tutoriales")
        self.menubar.add_cascade(label="Cuenta", menu=self.cuentamenu)
        self.menubar.add_cascade(label= "Ayuda", menu=self.ayudamenu)
        self.root.config(menu = self.menubar) #Se declara menubat como el menu del frame root

        #Ejecutar el dialogo de password al iniciar
        self.oppsw()

        #Se activa el loop para detectar eventos
        self.root.mainloop()

    def hello (self):
        print "hola"

    def oppsw (self):
        a = pswdiag(self.root)

    def close (self):
        self.root.destroy()

class pswdiag:
    def __init__(self,parent):
        self.top = Toplevel(parent) #Objeto dialog
        self.top.grab_set()         #Para hacerlo modal
        self.top.title("Administrador: Iniciar Sesión")
        #Widgets constantes
        Label(self.top, text="Usuario").grid(column=0,row=0)
        Label(self.top, text="Contraseña").grid(column=0, row=1,sticky=tk.E)

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

    def compare(self,*args):
        if ( buscaPass( self.eusr.get() ) == self.epsw.get() ) and not None:
            tkMessageBox.showinfo("Acceso permitido", "Bienvenido")
            self.top.destroy()
        else:
            tkMessageBox.showerror("Acceso denegado", "Usuario/contraseña incorrecto")
            self.eusr.delete(0, END)
            self.epsw.delete(0, END)
            self.eusr.focus()

a = adminMain()
