#!/usr/bin/env python
# coding: utf-8

# Autor: Arinaldo Araujo/Raul Barros
# Data: 04/12



import sys, commands
import base64,zlib

parametros = sys.argv[1:]
saida = 0
if ( len(parametros)< 3 ):
	print "Argumentos:\npython %s IP community MIB" % sys.argv[0]
	print "Ex: python %s 192.168.0.20 u3fr0I9b5 .1.3.6.1.4.1.2024.43" % sys.argv[0] 
	sys.exit(1)
else:
	ip=parametros[0]
	community=parametros[1]
	mib=parametros[2] 

data = commands.getoutput("/usr/bin/snmpwalk -v 1 -c %s %s %s" %(community,str(ip),mib) )

string_final = ''

cont  = 0

data = data.replace('STRING: "','*').replace('::','*')


aux = 0
string_aux = ''
for d in range(0, len(data)):
	string_parcial = ''
	if data[d] == '*' and cont == 0:
		inicio = d + 1
		cont = 1
	elif data[d] == '*' and cont == 1:
		fim = d
		cont = 2
		aux_fim = fim
		flag = 0
		string_aux = ''
		while flag != 1:
			if data[aux_fim] == '"':
				string_aux = string_aux + data[aux_fim]
				string_aux = string_aux[::-1]
				flag = 1
			else:
				string_aux = string_aux + data[aux_fim]
				aux_fim = aux_fim - 1 
	if cont == 2:
		string_parcial = data[inicio:fim]
		if len(string_parcial) > len(string_final):
			string_final = string_parcial
		cont = 0

string_aux = string_aux.replace('*','')
string_final = string_final.replace(string_aux,'')

if string_final.find('DOCTYPE') == -1:
	string = ''
	for i in range(string_final.find('"'),len(string_final)):
		string = string + str(string_final[i])
	string_final = string_final.replace(string,'')

try:

	string_final = zlib.decompress(base64.b64decode(string_final))

except:
	x = 1

if string_final.find("Possivelmente Repetido") != -1:
	string_final = string_final.replace("WARNING","OK")
	saida = 0

print string_final		

if "WARNING" in string_final:
	saida = 1
elif "CRITICAL" in string_final:
	saida = 2


sys.exit( saida )

