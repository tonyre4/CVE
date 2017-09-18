##EDITAR LAS CONFIGURACIONES (ALADO DE RUN)
##Y PONER COMO PARAMETROS build_ext -i

import subprocess


def compile(option, obf):
    subprocess.check_output(['rm -rf files ; touch output.py || true'], shell=True)
    subprocess.check_output(['mkdir files || true'], shell=True)
    subprocess.check_output(['cp ../commonsources/*.py files/ || true'], shell=True)

    if option == 1:
        subprocess.check_output(['cp ../admin/*.py files/ || true'], shell=True)
        main = "adminMain.py"
    if option == 2:
        subprocess.check_output(['cp ../bombas/*.py files/ || true'], shell=True)
        main = "bombasMain.py"
    if option == 3:
        subprocess.check_output(['cp ../Crono/*.py files/ || true'], shell=True)
        subprocess.check_output(['cp ../Crono/*.png . || true'], shell=True)
        main = "cronoMain.py"

    files = subprocess.check_output(['ls files/'], shell=True)
    files = files.split()

    files.remove(main)
    files2 = list()

    for x in files:
        files2.append(x[:-3])

    subprocess.check_output(['mv files/%s files/building.py|| true' % main], shell=True)

    retry = True

    ##BUCLE PARA AnADIR LIBRERIAS EN LA LINEA QUE ENCUENTRE
    while retry:
        output = open("output.py", "wb")
        retry = False
        with open('files/building.py', 'r') as archivo:
            for linea in archivo:
                printea = True
                for x in files2:
                    if linea.startswith("from %s" % x):
                        output.write('\n##########inicio %s########################\n' % x)
                        try:
                            with open('files/%s.py' % x, 'r') as f2:
                                for l2 in f2:
                                    output.write(l2)
                        except e:
                            pass
                        printea = False
                        output.write('\n###########final %s########################\n' % x)
                        files2.remove(x)
                if printea:
                    output.write(linea)
                else:
                    retry = True
        output.close()
        subprocess.check_output(['rm files/building.py ; mv output.py files/building.py ; touch output.py || true'],
                                shell=True)
    ############################TERMINA BUCLE

    ##BUCLE PARA QUITAR LIBRERIAS PROPIAS y sys
    for x in files:
        files2.append(x[:-3])

    for x in files2:
        # print subprocess.check_output(['grep  "from %s" files/building.py || true' % x] , shell = True)
        subprocess.check_output(['grep -v "from %s" files/building.py > output.py || true' % x], shell=True)
        subprocess.check_output(['rm files/building.py ; mv output.py files/building.py || true'],
                                shell=True)
    ##Parte que quita sys
    subprocess.check_output(['grep -v "sys" files/building.py > output.py || true'], shell=True)
    subprocess.check_output(['rm files/building.py ; mv output.py files/building.py || true'], shell=True)
    ############################TERMINA BUCLE

    subprocess.check_output(['grep -e "import" -e "utf" files/building.py > imports.py || true'],
                            shell=True)
    subprocess.check_output(['grep -v "import" files/building.py | grep -v "utf" > preout.py || true'],
                            shell=True)

    imports = list()
    with open('imports.py', 'r') as f1:
        for l1 in f1:
            imports.append(l1)
    imports = set(imports)

    ##Acomodar imports el utf primero
    imports2 = list()
    for x in imports:
        if x.startswith("#"):
            imports2.append(x)
    for x in imports:
        if not x.startswith("#"):
            imports2.append(x)
    imports = imports2
    del imports2

    ##GENERA EL ARCHIVO FINAL CON IMPORTS Y EL CODIGO SIN IMPORTS
    if obf:
        output = open('obf.py', 'w+')
    else:
        output = open('final.py', 'w+')
    for x in imports:
        output.write(x)

    with open('preout.py', 'r') as f:
        for x in f:
            output.write(x)
    output.close()

    if obf:
        subprocess.check_output(['pyobfuscate obf.py > final.py || true'],
                                shell=True)

    clean(option)
    return main[:-3]


#####################################################################################
def clean(option):
    subprocess.check_output(['rm -r files/ | rm -r build/ || true'], shell=True)
    if option == 3:
        # print subprocess.check_output(['ls | grep -v ".png" | grep -v "cConver" | grep -v "final"|| true'], shell=True)
        subprocess.check_output(['ls | grep -v ".png" | grep -v "cConver" | grep -v "final" | xargs rm || true'],
                                shell=True)
    else:
        # print subprocess.check_output(['ls | grep -v "cConver" | grep -v "final" || true'], shell=True)
        subprocess.check_output(['ls | grep -v "cConver" | grep -v "final" | xargs rm || true'], shell=True)


#####################################################################################

# opcion,ofuscar?
main = compile(1, False)

##COMPILADOR
from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext

ext_modules = [Extension(main, ['final.py'], )]
setup(
    name="Set 1 of Functions",
    cmdclass={'build_ext': build_ext},
    ext_modules=ext_modules
)

__import__(main)
