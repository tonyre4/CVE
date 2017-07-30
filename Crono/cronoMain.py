# -*- coding: utf-8 -*-
from Tkinter import *
import tkMessageBox
import sys
sys.path.append('../commonsources')
from pswDiag import *
from userData import *
import ScrolledText
from logTool import logO
from eventExe import *

class cronoMain:

    def __init__(self):
        #objeto de usuario
        self.UD = userData()
        #Objeto para ejecutar tareas
        self.ex= evExecuter()
        self.ex.addEvt(self.hello,'0')

        #Declaracion de la ventana
        self.root = Tk()
        #self.root.iconify()##COMENTAR
        self.root.title("egas - crono")

        #Dibujado de menus
        self.drawMenu()
        self.inlog()

        #Dibuja ventana
        self.drawWin()

        #Ejecutar el dialogo de password al iniciar
        ##self.oppsw() #DESCOMENTAR

        #Se activa el loop para detectar eventos
        self.root.mainloop()

    def hello (self):
        print "hola"
        self.log.printlog("Hola!")

    def drawWin(self):

        #Entry para el log
        self.logWin = ScrolledText.ScrolledText(self.root,state='disabled')
        self.logWin.pack(fill=X,side='bottom')
        self.log = logO(self.logWin) #objeto para loggear

        #self.log.printlog("string") ##instruccion para imprimir en el log


    def drawMenu(self):
        # Delcaracion del menus
        self.menubar = Menu(self.root)  # Objeto principal de menus
        self.cuentamenu = Menu(self.menubar, tearoff=0)  # Objeto de menu para la cascada
        self.ayudamenu = Menu(self.menubar, tearoff=0)  # Objeto del menu para la cascada

        if not self.UD.logeado:

            self.cuentamenu.add_command(label="Iniciar sesión", command=self.oppsw)
            self.cuentamenu.add_command(label="Salir", command=self.close)
            self.ayudamenu.add_command(label="Acerca de...")
            self.ayudamenu.add_command(label="Tutoriales")
            self.menubar.add_cascade(label="Cuenta", menu=self.cuentamenu)
            self.menubar.add_cascade(label="Ayuda", menu=self.ayudamenu)

        else:
            self.cuentamenu.add_command(label="Cerrar sesión", command=self.unlog)
            self.cuentamenu.add_command(label="Configuracion de crono", command= self.hello)
            self.cuentamenu.add_command(label="Salir", command=self.close)
            self.ayudamenu.add_command(label="Acerca de...")
            self.ayudamenu.add_command(label="Tutoriales")
            self.menubar.add_cascade(label="Cuenta", menu=self.cuentamenu)
            self.menubar.add_cascade(label="Ayuda", menu=self.ayudamenu)

        self.root.config(menu=self.menubar)  # Se declara menubar como el menu del frame root

    def inlog(self):
        #self.root.deiconify()
        self.UD.logeado = True
        self.drawMenu()

    def unlog(self):
        self.UD.logeado=False
        tkMessageBox.showinfo("Cierre de sesión", "El usuario ha cerrado la sesión")
        self.drawMenu()

    def oppsw (self):
        self.root.iconify()
        a = pswdiag(self,self.root)

    def close (self):
        self.root.destroy()

a = cronoMain()