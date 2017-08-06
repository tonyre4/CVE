##EDITAR LAS CONFIGURACIONES (ALADO DE RUN)
##Y PONER COMO PARAMETROS build_ext -i

import subprocess

def compile(option):
    subprocess.check_output(['rm -rf files ; rm output.py ; touch output.py || true'],shell=True)
    subprocess.check_output(['mkdir files || true'],shell=True)
    subprocess.check_output(['cp ../commonsources/*.py files/ || true'],shell=True)
    #subprocess.check_output(['touch sources.pyx || true'],shell=True)

    if option==1:
        subprocess.check_output(['cp ../admin/*.py files/ || true'],shell=True)
        main = "adminMain.py"
    if option==2:
        subprocess.check_output(['cp ../bombas/*.py files/ || true'],shell=True)
        main = "bombasMain.py"
    if option==3:
        subprocess.check_output(['cp ../Crono/*.py files/ || true'],shell=True)
        main= "cronoMain.py"

    files = subprocess.check_output(['ls files/'],shell=True)
    files = files.split()


    files.remove(main)
    files2 = list()

    for x in files:
        files2.append(x[:-3])

    subprocess.check_output(['mv files/%s files/building.py|| true' % main],shell=True)

    retry= True

    while retry:
        output= open("output.py","wb")
        retry= False
        with open('files/building.py','r') as archivo:
            for linea in archivo:
                printea = True
                for x in files2:
                    if linea.startswith("from %s" % x):
                        output.write('\n##########inicio %s########################\n' % x)
                        try:
                            with open('files/%s.py' % x,'r') as f2:
                                for l2 in f2:
                                    output.write(l2)
                        except e:
                            pass
                        printea = False
                        output.write('\n###########final %s########################\n' %x)
                        files2.remove(x)
                if printea:
                    output.write(linea)
                else:
                    retry= True
        output.close()
        subprocess.check_output(['rm files/building.py ; mv output.py files/building.py ; touch output.py || true'],shell=True)


    retry= True
    subprocess.check_output(['grep -e "import" -e "sys" -e "utf" files/building.py >> files/check.py || true'],shell=True)


    with open('files/check.py','r') as archivo:
        for linea in archivo:
            output= open("output.py","wb")
            with open('files/building.py') as archivo2:
                printed=False
                for linea2 in archivo2:
                    if linea==linea2:
                        if not printed:
                            output.write(linea2)
                            printed=True
                    else:
                        output.write(linea2)
            subprocess.check_output(['rm files/building.py ; mv output.py files/building.py ; touch output.py || true'],shell=True)

    subprocess.check_output(['mv files/building.py final.pyx|| true'],shell=True)

def clean():
    subprocess.check_output(['rm -r files/ || true'], shell=True)
    #subprocess.check_output(['ls | grep -v "cConver" | grep -v "final" | grep "*.py" | xargs rm  || true'], shell=True)


compile(1)
clean()

from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext

ext_modules = [Extension('test', ['final.pyx'],)]

setup(
    name="Set 1 of Functions",
    cmdclass={'build_ext': build_ext},
    ext_modules=ext_modules
)


import test
