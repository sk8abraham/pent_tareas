#!/usr/bin/python

#############################################
######## Manzano Cruz Isaias Abraham ########
#############################################

import argparse
import random
import ipaddress
from socket import gethostbyname
from scapy.all import ICMP, IP, sr1, TCP
 
def opciones():
	'''
	Funcion que obtiene los argumentos de la linea de comandos
	Regresa: Las opciones que se pasaron por linea de  comandos
	'''
	parser = argparse.ArgumentParser()
	parser.add_argument("-i","--ip", help="Selecciona el/los host(s) a atacar; si son varios usar la notacion CIDR", type= unicode, default=None)
	parser.add_argument("-p","--port", help="Selecciona el/los puerto(s) a conectar; si son varios, separar por coma, sin espacios!", type=str, default=None)
	return parser.parse_args()

def ip_puerto(args):
	'''
	Funcion que obtiene la(s) IP(s) de las opciones y el (los) puerto(s) de las opciones
	Recibe: Los argumentos por linea de comandos y sus valores
	Regresa: Una lista con la(s) IP(s) (son varias si se utilizo notacion CIDR, regresa una si se utilizo nombre de dominioo IP); y una lista con el (los) puerto(s) especificado(s)
	'''
	ports=[]
	for p in args.port.split(","):
		ports.append(int(p))
	try:
		ip_addr = gethostbyname(args.ip)
		ips = ipaddress.ip_network(ip_addr)
	except:
		ips = ipaddress.ip_network(args.ip)
	return ports,ips

def verifica(args):
	'''
	Funcion que verifica que las opciones de entrada no sean nulas, en caso afirmativo, termina el programa con error
	Recibe: Los argumentos pasados por linea de comandos
	'''
	if args.ip == None:
		print "Debes especificar el/las ip(s) o un hostname destino"
		exit(1)
	if args.port == None:
		print "Debes especificar el/los puerto(s) destino"
		exit(1)

def hace_peticiones(ips,ports):
	'''
	Funcion que manda mensajes ICMP a los hosts, y dependiendo su respuesta se establece que estan filtrados o cerrados
	Recibe: Lista de ips y puertos
	'''
	vivos=0
	for host in ips:
		if(host in (ips.network_address, ips.broadcast_address)):
			continue
		print""
		resp = sr1(IP(dst=str(host))/ICMP(), timeout=2, verbose=0, iface='eth0')
		if resp is None:
			print "%s No responde o esta apagado" % (host)
		elif(int(resp.getlayer(ICMP).type) == 3 and int(resp.getlayer(ICMP).code) in [1,2,3,9,10,13]):
			print "%s Esta bloqueando ICMP" % (host)
		else:
			escanea_puerto(str(host),ports)
			vivos+=1
	print "%d/%d hosts prendidos"%(ips.num_addresses,vivos)

def escanea_puerto(host,ports):
	'''
	Funcion que verifica si hay puerto(s) abierto(s) en el host especificado
	Recibe: Un host y una lista de puertos a comprobar
	'''
	for dst_port in ports:
		src_port = random.randint(1025, 65534)
		resp = sr1(IP(dst=host)/TCP(sport=src_port,dport=dst_port,flags="S"),timeout=1,verbose=0)
		if resp is None:
			print "%s:%d filtrado" % (host,dst_port)
		elif(resp.haslayer(TCP)):
			if(resp.getlayer(TCP).flags == 0x12):
				send_rst = sr1(IP(dst=host)/TCP(sport=src_port,dport=dst_port,flags='R'),timeout=1,verbose=0)
				print "%s:%d abierto"%(host,dst_port)
			elif (resp.getlayer(TCP).flags == 0x14):
				print "%s:%d cerrado"%(host,dst_port)
		elif(resp.haslayer(ICMP)):
			if(int(resp.getlayer(ICMP).type) == 3 and int(resp.getlayer(ICMP).code) in (1, 2, 3, 9, 10, 13)):
				print "%s:%d filtrado."%(host,dst_port)
def main():
	'''
	Función principal
	'''
	args = opciones()
	verifica(args)
	ports,ips= ip_puerto(args)
	for i in range (0,ips.num_addresses):
		print(ips[i])
	print ports
	hace_peticiones(ips,ports)

main()
