# -*- coding: utf-8 -*-
from Tkinter import *
import tkMessageBox
import sys
sys.path.append('../commonsources')
from pswDiag import *
from userData import *
from admndc import *

class adminMain:

    def __init__(self):
        #objeto de usuario
        self.UD = userData()
        #Declaracion de la ventana
        self.root = Tk()
        #self.root.iconify()
        #self.admndcdiag()
        self.root.title("egas - admin")

        #Dibujado de menus
        self.drawMenu()

        #Ejecutar el dialogo de password al iniciar
        self.oppsw()

        #Se activa el loop para detectar eventos
        self.root.mainloop()

    def hello (self):
        print "hola"
        print "otra cosa"

    def drawMenu(self):
        # Delcaracion del menus
        self.menubar = Menu(self.root)  # Objeto principal de menus
        self.cuentamenu = Menu(self.menubar, tearoff=0)  # Objeto de menu para la cascada
        self.ayudamenu = Menu(self.menubar, tearoff=0)  # Objeto del menu para la cascada

        if not self.UD.logeado:

            self.cuentamenu.add_command(label="Iniciar sesión", command=self.oppsw)
            #self.cuentamenu.add_command(label="Administrador de cuentas", command= self.admndcdiag)##QUITAR
            self.cuentamenu.add_command(label="Salir", command=self.close)
            self.ayudamenu.add_command(label="Acerca de...")
            self.ayudamenu.add_command(label="Tutoriales")
            self.menubar.add_cascade(label="Cuenta", menu=self.cuentamenu)
            self.menubar.add_cascade(label="Ayuda", menu=self.ayudamenu)

        else:
            self.cuentamenu.add_command(label="Cerrar sesión", command=self.unlog)
            self.cuentamenu.add_command(label="Administrador de cuentas", command= self.admndcdiag)
            self.cuentamenu.add_command(label="Salir", command=self.close)
            self.ayudamenu.add_command(label="Acerca de...")
            self.ayudamenu.add_command(label="Tutoriales")
            self.menubar.add_cascade(label="Cuenta", menu=self.cuentamenu)
            self.menubar.add_cascade(label="Ayuda", menu=self.ayudamenu)

        self.root.config(menu=self.menubar)  # Se declara menubar como el menu del frame root

    def inlog(self):
        self.root.deiconify()
        self.UD.logeado = True
        self.drawMenu()

    def unlog(self):
        self.UD.logeado=False
        tkMessageBox.showinfo("Cierre de sesión", "El usuario ha cerrado la sesión")
        self.drawMenu()

    def admndcdiag(self):
        self.UD.testing()
        b = adminctas(self.root,self.UD.lvl)

    def oppsw (self):
        self.root.iconify()
        a = pswdiag(self,self.root)

    def close (self):
        self.root.destroy()

a = adminMain()
