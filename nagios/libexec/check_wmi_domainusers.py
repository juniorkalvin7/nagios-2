#!/usr/bin/python	
# -*- coding: utf-8 -*-

import commands
import sys

ip = sys.argv[1]
name = sys.argv[2]
senha = sys.argv[3]

command_line = '/usr/bin/wmic -U %s%%%s //%s "select Name from Win32_UserAccount" ' %(name,senha,ip)

status, x = commands.getstatusoutput(command_line)


if status == 0:
        print "Listagem de todas as contas do Dominio"
else:
        print "Problemas na obtenção de dados do host"
	sys.exit(1) 

x = x.replace('CLASS: Win32_UserAccount','')
x = x.replace('Domain|Name','')
x = x.split('|')
x = '\n '.join(x)
x = x.split('\n')


while x.count('') > 0:
	x.remove('')


#-----CORPO FINAL-----#
corpo_final = """
                </table>
        </body>
</html>"""



#-----CORPOL-----#
corpo = """
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">

<head>
        <title>Usuarios do dominio</title>
        <meta http-equiv="content-type" content="text/html;charset=utf-8" />
</head>

<body>

<table BORDER = 2 align="center">

        <tr>
                <TH align="center" COLSPAN=2>--------------- Lista de Usuarios do Dominio ---------------</TH>
        </tr>
        <tr>
                <TH>Dominio</TH>
                <TH>Nome</TH>
        </tr>
"""

cont = 0
while cont < len(x)-1:
	corpo = corpo + '<tr align="Center"> <td>%s</td>              <td>%s</td></tr>' %(x[cont],x[cont+1])
	cont = cont + 2 

corpo = corpo + corpo_final
print "%s" %(corpo.replace('\n','')) 


sys.exit(0)
