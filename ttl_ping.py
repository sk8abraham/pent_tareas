import argparse
import subprocess
import re
def opciones():
	'''
	Funcion que obtiene los argumentos de la linea de comandos
	Devuelve: Las opciones que se pasaron por linea de  comandos
	'''
	parser = argparse.ArgumentParser()
	parser.add_argument("-i","--ip", help="Selecciona el host", type= unicode, default=None)
	return parser.parse_args()


def verifica(opt):
    '''
    Funcion que valida las opciones de entrada, en caso de que no sea valido, se termina el programa
    Recibe: opt --> Opciones
    Regresa: None
    '''
    if opt.ip == None:
        print 'Error: Debes especificar una ip\nEjecutar con la opcion -h para obtener ayuda'
        exit(0)

def main():
    '''
    Funcion principal
    '''
    opt = opciones()
    verifica(opt)
    p = subprocess.Popen(["ping", opt.ip,"-c","1"], stdout=subprocess.PIPE)
    res = p.communicate()[0]
    if p.returncode > 0:
        print 'No responde'
    else:
        rex = r'ttl=([0-9]+)'
        ttl = int(re.search(rex,str(res).lower()).group(1))
        if ttl <= 128 and ttl > 66:
            print '%s es Windows'%opt.ip
        else:
            print '%s es Linux'%opt.ip
main()
