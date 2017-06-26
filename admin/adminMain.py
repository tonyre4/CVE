# -*- coding: utf-8 -*-
from Tkinter import *
import sys
sys.path.append('../commonsources')
from pswDiag import *

class adminMain:

    def __init__(self):
        #Declaracion de la ventana
        self.root = Tk()
        self.root.title("egas - admin")
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

a = adminMain()
