# -*- coding: utf-8 -*-
from Tkinter import *
import ttk
import tkMessageBox
sys.path.append('../commonsources')
from CMmysqlconnect import *

class adminctas:

    def __init__(self,parent,lvl):
        self.parent = parent
        self.lvl = "{0:09b}".format(lvl)
        self.subool = False
        if self.lvl[0] == '1':
            self.subool = True  ##Variable de super user

        self.top = Toplevel(self.parent)  # Objeto dialog
        self.top.grab_set()  # Para hacerlo modal
        self.top.title("Administrador de cuentas")

        self.lf1=LabelFrame(self.top,text= "Nueva cuenta")

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



        if not self.subool:
            self.chksu.config(state=DISABLED)

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

        # Widgets constantes
        Label(self.lf1, text="Nombre").grid(column=0, row=0)
        Label(self.lf1, text="Contraseña").grid(column=0, row=1)
        Label(self.lf1, text="Confirmar").grid(column=0, row=2)
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

        # Widgets
        self.lusr  = ttk.Combobox(self.lf2, state='readonly', postcommand= self.updl)
        self.lpss = Entry(self.lf2,show='*') #pass actual
        if self.subool:
            self.lpss.config(state=DISABLED)
        self.cpss = Entry(self.lf2,show='*') #cambio pass
        self.cpssc = Entry(self.lf2,show='*') #confirmar pass
        self.chbtn = Button(self.lf2, text="Cambio", command=self.chngusr)
        self.clrbtn = Button(self.lf2, text="Borrar", command=self.delusr)
        if not self.subool:
            self.clrbtn.config(state=DISABLED)
        self.lblp  = LabelFrame(self.lf2, text= "Permisos")
        self.usu=BooleanVar()
        self.usuchk = Checkbutton(self.lf2,text="Super usuario",variable=self.usu)
        if not self.subool:
            self.usuchk.config(state=DISABLED)

        #Binds
        self.lusr.bind("<<ComboboxSelected>>", self.getparms)


        self.C2 = [[0 for x in range(self.q)] for y in range(2)]
        self.Cvar2 = [[0 for x in range(self.q)] for y in range(2)]
        ##Tabla de permisos
        for i in range (0,self.q):
            Label(self.lblp, text=self.nombres[i]).grid(column=0, row=i) ##Setea el nombre del permiso

            self.Cvar2[0][i] = BooleanVar()
            self.C2[0][i] = Checkbutton(self.lblp, text="Leer", variable=self.Cvar2[0][i], command=self.prmchk2)
            self.C2[0][i].grid(column=1, row=i)

            self.Cvar2[1][i] = BooleanVar()
            self.C2[1][i] = Checkbutton(self.lblp, text="Escribir", variable=self.Cvar2[1][i], command=self.prmchk2)
            self.C2[1][i].grid(column=2, row=i)

            if not self.subool:  # checa si es su
                if self.lvl[(i * 2) + 1] == '0':
                    self.C2[0][i].config(state=DISABLED)
                if self.lvl[(i + 1) * 2] == '0':
                    self.C2[1][i].config(state=DISABLED)

        # Widgets constantes
        Label(self.lf2, text="Usuario").grid(column=0, row=0)
        Label(self.lf2, text="Cont. Actual").grid(column=0, row=1)
        Label(self.lf2, text="Contraseña").grid(column=0, row=2)
        Label(self.lf2, text="Confirmar").grid(column=0, row=3)
        # Posicionando los widgets
        self.lusr.grid  (column=1, row=0, columnspan=3)
        self.lpss.grid  (column=1, row=1, columnspan=3)
        self.cpss.grid  (column=1, row=2, columnspan=3)
        self.cpssc.grid (column=1, row=3, columnspan=3)
        self.lblp.grid  (column=0, row=4, columnspan=4)
        self.usuchk.grid(column=0, row=5)
        self.clrbtn.grid(column=2, row=5)
        self.chbtn.grid (column=3, row=5)

        self.lf2.grid()

##############################################################
    ##############FUNCIONES DE CUENTA EXISTENTE

    def updl(self):
        self.lusr['values'] = buscaDat(None,"user")

    def getparms(self,*args):
        u=self.lusr.get()
        l='{0:09b}'.format(buscaDat(u,"level"))

        self.usuchk.deselect()
        for i in range(0, self.q):
            self.C2[0][i].deselect()
            self.C2[1][i].deselect()

        if l[0]=='1':
            self.usuchk.select()
        else:
            for i in range (0,self.q):
                if l[(i*2)+1]=='1':
                    self.C2[0][i].select()
                if l[(i+1)*2]=='1':
                    self.C2[1][i].select()

    def chngusr(self):
        u,pa,pn,pnc= self.lusr.get(),self.lpss.get(),self.cpss.get(),self.cpssc.get()
        l=self.glvl(self.usu.get(),self.Cvar2)

        r = tkMessageBox.askyesno("Cambio en usuario", "Estas seguro de hacerle un cambio a la cuenta '%s'?" % u )

        if r:
            if not self.subool: #CHECA CONTRASEÑA ACTUAL
                if buscaDat(u,"pass")!=pa:
                    tkMessageBox.showerror("Error de autenticación","La contraseña actual de la cuenta no es correcta")
                    return
            if not (pn=="" and pnc==""):
                if pn != pnc :
                    tkMessageBox.showerror("Error de confirmacion","Las contraseñas no coinciden")
                    return
                else:
                    cambiaDat(u,"pass",pn)

            if l==0:
                tkMessageBox.showerror("Error de permisos", "No se puede dejar una cuenta sin permisos")
            else:
                cambiaDat(u,"level",l)

    def delusr(self):
        u = self.lusr.get()
        if not u=="":
            r= tkMessageBox.askyesno("Borrado de cuenta","Estas seguro de borrar al usuario '%s'?" % u)
            if r:
                borraDat(u)

##############################################################
##############################################################

###############################################################################################
#FUNCIONES DE NUEVA CUENTA
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
        l = self.glvl(self.chk.get(),self.Cvar)

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

    def prmchk2(self): ##Checa parametros de leer y escribir
        for i in range(self.q):
            if not self.Cvar2[0][i].get() and self.Cvar2[1][i].get():
                self.C2[0][i].deselect()
                self.C2[1][i].deselect()

    def chkchks(self):
        if self.chk.get():
            x=DISABLED
        else:
            x=ACTIVE
        for i in range (0,self.q):
            self.C[0][i].config(state=x)
            self.C[1][i].config(state=x)

###############################################################################################
###############################################################################################
###################################################
        #FUNCIONES COMUNES
    def glvl(self,su,C):  #Genera nivel
        l=0
        if su:
            l += 1 << self.q * 2
        else:
            for i in range(self.q):
                l += C[0][i].get() << 7 - (i * 2)
                l += C[1][i].get() << 7 - (i * 2) - 1
        return l