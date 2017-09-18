from Tkinter import *


class cronConfigDiag:

    def __init__(self,parent,lvl):
        #Constantes
        self.root = parent
        self.lvl='{0:09b}'.format(lvl)

        #Checar permisos de escritura o superuser
        if lvl[0]=='1' or lvl[0]=='1': #checar el otro permiso
            self.enabled = True
        else:
            self.enabled = False

        ##Configuraciones del dialogo
        self.top = Toplevel(self.root)
        self.top.grab_set()
        self.top.title("Configuraciones de Cron")


