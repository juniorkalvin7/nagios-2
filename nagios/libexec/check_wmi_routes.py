#!/usr/bin/python
# -*- coding: utf-8 -*-


#-------------------------
#Autor: Wagner Dias.     |
#                        |
#-------------------------

import commands
import sys
import re

ip = sys.argv[1]
name = sys.argv[2]
senha = sys.argv[3]


#-----tabelaRotas-----#
command_line1 = '/usr/bin/wmic -U %s%%%s //%s "SELECT Description FROM Win32_IP4RouteTable" ' %(name,senha,ip)

status1, tabelaRotas = commands.getstatusoutput(command_line1)

tabelaRotas = tabelaRotas.replace('CLASS: Win32_IP4RouteTable','')
tabelaRotas = tabelaRotas.replace('Description|Destination|InterfaceIndex|Mask|NextHop','') 
tabelaRotas = tabelaRotas.split('\n')

while tabelaRotas.count('') > 0:
	tabelaRotas.remove('')

#-----Intefaces de rede-----#
command_line2 = '/usr/bin/wmic -U %s%%%s //%s "SELECT InterfaceIndex,IPAddress FROM Win32_NetworkAdapterConfiguration" ' %(name,senha,ip)

status2, listaInterfaces = commands.getstatusoutput(command_line2)

listaInterfaces = listaInterfaces.replace('CLASS: Win32_NetworkAdapterConfiguration','')
listaInterfaces = listaInterfaces.replace('Index|InterfaceIndex|IPAddress','') 
listaInterfaces = listaInterfaces.split('\n')

while listaInterfaces.count('') > 0:
             listaInterfaces.remove('')


if ((status1 !=0)|(status2 != 0)):
	print "Problemas na obtenção de dados do host"
	sys.exit(1)


#-----CORPO-----#
corpo="""
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">

<head>
        <title>Rotas</title>
        <meta http-equiv="content-type" content="text/html;charset=utf-8" />
</head>

<body>

<table BORDER=2 align="center">

        <tr>
                <TH align="center" COLSPAN=4>--------------- Tabela de Rotas IPv4  ---------------</TH>
        </tr>
        <tr>
                <TH>Endereco de Rede</TH>
                <TH>Mascara</TH>
                <TH>Gateway</TH>
                <TH>Interface</TH>
        </tr>
"""


auxIfaces = []
cont1 = 0
while cont1 < (len(tabelaRotas)):
	auxIfaces.append('(127.0.0.1)')
	cont1 = cont1 + 1


cont1 = 0
while cont1 < (len(tabelaRotas)):
	rota = str(tabelaRotas[cont1])
	rota = rota.split('|')

	cont2 = 0	
	while cont2 < (len(listaInterfaces)):
		interface = str(listaInterfaces[cont2])
		interface = interface.split('|')
		
		if (rota[2] == interface[1]):
			auxIfaces[cont1] = interface[2]	
		
		cont2 = cont2 + 1

	cont1 = cont1 + 1
	

cont1 = 0		
while cont1 < (len(tabelaRotas)):
	rota = str(tabelaRotas[cont1])
	rota = rota.split('|')
	
	decRota = str(rota[0])		
	decRota = decRota.split('-')
	
	corpo = corpo + '<tr align="Center"> <td>%s</td>              <td>%s</td>              <td>%s</td>              <td>%s</td></tr>' %(decRota[0],decRota[1],decRota[2],auxIfaces[cont1])				
	
	cont1 = cont1 + 1				
	
	
#-----CORPO FINAL-----#
corpo_final = """
                </table>
        </body>
</html>"""

corpo = corpo + corpo_final

print 'Numero de rotas ativas: %s' %(len(tabelaRotas))
print "%s" %(corpo.replace('\n',''))
sys.exit(0)
