#!/usr/bin/python
# -*- coding: utf-8 -*-

import commands
import sys

ip = sys.argv[1]
name = sys.argv[2]
senha = sys.argv[3]

#-----Nome do host----#
command_line3 = '/usr/bin/wmic -U %s%%%s //%s "select Name from Win32_ComputerSystem" ' %(name,senha,ip)
status3, hostname  = commands.getstatusoutput(command_line3)

hostname = hostname.replace('CLASS: Win32_ComputerSystem','')
hostname = hostname.replace('Name','')
hostname = hostname.split('\n')

while hostname.count(''):
        hostname.remove('')


#-----Diretóris Compartilhados----#
command_line = '/usr/bin/wmic -U %s%%%s //%s "SELECT * FROM Win32_ShareToDirectory" ' %(name,senha,ip)

status, dados = commands.getstatusoutput(command_line)


if status != 0:
        print "Problemas na obtenção de dados do host"
        sys.exit(1)

x = '\\\\%s\\root\\CIMV2:Win32_Directory.Name="' %(hostname[0])
dados = dados.replace('CLASS: Win32_ShareToDirectory','')
dados = dados.replace('Share|SharedElement','')
dados = dados.replace(x,'')
dados = dados.split('\n')

while dados.count(''):
	 dados.remove('')


#-----CORPO-----#
corpo="""
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">

<head>
        <title>Pastas Compartilhadas</title>
        <meta http-equiv="content-type" content="text/html;charset=utf-8" />
</head>

<body>

	<table BORDER=2 align="center">

        	<tr>
                	<TH align="center" COLSPAN=1>--------------- Pastas Compartilhadas  ---------------</TH>
        	</tr>
                
        
"""

cont = 0
while cont < len(dados):
	aux = dados[cont]
	aux = aux.split('|')
	aux[1] = aux[1].replace('"','')
	aux[1] = aux[1].replace('\\\\','\\')
	#aux[1] = aux[1].replace('c:\\','c:\\\\')
	dados[cont] = aux[1]
	corpo = corpo + '<tr> <td>%s</td> </tr>' %(dados[cont])	
					
	cont = cont + 1


#----- CORPO FINAL -----#
corpo_final = """
		</table>
	</body>
</html>"""

corpo = corpo + corpo_final

print 'Pastas compartilhadas: %s' %(dados)
print "%s\n" %(corpo.replace('\n','')) 
sys.exit(0)
