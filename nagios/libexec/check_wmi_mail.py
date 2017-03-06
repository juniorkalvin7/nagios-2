#!/usr/bin/python
# ** coding: utf-8 **

import commands
import sys

ip = sys.argv[1]
name = sys.argv[2]
senha = sys.argv[3]

command_line = '/usr/bin/wmic -U %s%%%s //%s "SELECT Name,SessionsInUse FROM Win32_PerfRawData_ESE_MSExchangeDatabaseInstances" ' %(name,senha,ip)

status, x = commands.getstatusoutput(command_line)


if status != 0:
        print "Problemas na obtenção de dados do host"
        sys.exit(1)
else:	
	print "OK"

x = x.replace('CLASS: Win32_PerfRawData_ESE_MSExchangeDatabaseInstances','')
x = x.replace('Name|SessionsInUse','')
x = x.split('|')
x = '\n '.join(x)
x = x.split('\n')


while x.count('') > 0:
        x.remove('')


#-----CORPO FINAL-----#
corpo_final = """
		</center></body>
</html>"""


#-----CORPO-----#
corpo = """
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">

	<head>
		<title>Usuarios do dominio</title>
      	  	<meta http-equiv="content-type" content="text/html;charset=utf-8" />
	</head>

	<body><center>
"""


#----- Tabela1 -----#
tabela1 = """
		<table BORDER = 2 align="center">

			<tr>
            	    		<TH align="center" COLSPAN=2>--------------- Lista de Bancos Instanciados ---------------</TH>
        		</tr>
        		<tr>
            	    		<TH>Nome</TH>
               	 		<TH>Sessoes em uso</TH>
        		</tr>
"""


cont = 0
while cont < len(x)-1:
        tabela1 = tabela1 + '<tr align="Center"> <td>%s</td>              <td>%s</td></tr>' %(x[cont],x[cont+1])
        cont = cont + 2


#---- Fim Tabela ----#
fimTabela = """
			</table>
"""

tabela1 = tabela1 + fimTabela


#----- Tabela2 -----# 
command_line = '/usr/bin/wmic -U %s%%%s //%s "SELECT ConnectionsCreatedPersec,MessagesReceivedPersec FROM Win32_PerfRawData_MSExchangeTransportSmtpReceive_MSExchangeTransportSmtpReceive" ' %(name,senha,ip)

status, y = commands.getstatusoutput(command_line)

y = y.replace('CLASS: Win32_PerfRawData_MSExchangeTransportSMTPReceive_MSExchangeTransportSMTPReceive','')
y = y.replace('ConnectionsCreatedPersec|MessagesReceivedPersec|Name','')
y = y.split('|')
y = '\n '.join(y)
y = y.split('\n')

while y.count('') > 0:
        y.remove('')


tabela2 = """
		<table BORDER = 2 align="center">

			<tr>
            	    		<TH align="center" COLSPAN=3>--------------- Recive ---------------</TH>
        		</tr>
        		<tr>
				<TH>Nome</TH>		
            	    		<TH>Conexoes Criadas</TH>
               	 		<TH>Mensagens Recebidas por segundo</TH>
        		</tr>
"""

cont = 0
while cont < len(y)-2:
        tabela2 = tabela2 + '<tr align="Center"> <td>%s</td>              <td>%s</td>              <td>%s</td></tr>' %(y[cont+2],y[cont],y[cont+1])
        cont = cont + 3


tabela2 = tabela2 + fimTabela


#-----Tabela3----#
command_line = '/usr/bin/wmic -U %s%%%s //%s "SELECT ConnectionsCreatedPersec,MessagesSentPersec FROM Win32_PerfRawData_MSExchangeTransportSmtpSend_MSExchangeTransportSmtpSend" ' %(name,senha,ip)

status, z = commands.getstatusoutput(command_line)

z = z.replace('CLASS: Win32_PerfRawData_MSExchangeTransportSmtpSend_MSExchangeTransportSmtpSend','')
z = z.replace('ConnectionsCreatedPersec|MessagesSentPersec|Name','')
z = z.split('|')
z = '\n '.join(z)
z = z.split('\n')

while z.count('') > 0:
        z.remove('')

tabela3 = """
		<table BORDER = 2 align="center">

			<tr>
            	    		<TH align="center" COLSPAN=3>--------------- Send ---------------</TH>
        		</tr>
        		<tr>
				<TH>Nome</TH>		
            	    		<TH>Conexoes Criadas</TH>
               	 		<TH>Mensagens Enviadas por segundo</TH>
        		</tr>
"""

cont = 0
while cont < len(z)-2:
        tabela3 = tabela3 + '<tr align="Center"> <td>%s</td>              <td>%s</td>              <td>%s</td></tr>' %(z[cont+2],z[cont],z[cont+1])
        cont = cont + 3

tabela3 = tabela3 + fimTabela


corpo = corpo + tabela1 + tabela2 + tabela3 + corpo_final
print "%s" %(corpo.replace('\n',''))


sys.exit(0)
