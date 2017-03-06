#!/usr/bin/python
# -*- coding: utf-8 -*-

#-----------------------------------------------------------------
#Autor: Wagner Dias.                                             |
#Descrição: lista os usuários conectados localmente e no dominio.|
#                                                                |
#-----------------------------------------------------------------

import commands
import sys
import re

ip = sys.argv[1]
name = sys.argv[2]
senha = sys.argv[3]


#-----Dados da Classe Win32_LogonSession-----#
command_line1 = '/usr/bin/wmic -U %s%%%s //%s "select LogonId,LogonType,StartTime from Win32_LogonSession" ' %(name,senha,ip)

status1, x = commands.getstatusoutput(command_line1)

x = x.replace('CLASS: Win32_LogonSession','')
x = x.replace('LogonId|LogonType|StartTime','') #Id do Usuario--Tipo de Conexao

x = x.replace('|0|','--Conta do Sistema--')
x = x.replace('|2|','--Terminal--')
x = x.replace('|3|','--Network--')
x = x.replace('|4|','--Batch--')
x = x.replace('|5|','--Service--')
x = x.replace('|6|','--Proxy--')
x = x.replace('|7|','--Unlock--')
x = x.replace('|8|','--NetworkCleartext--')
x = x.replace('|9|','--NewCredentials--')
x = x.replace('|10|','--Terminal Services--')
x = x.replace('|11|','--CachedInteractive--')
x = x.replace('|12|','--CachedRemoteInteractive--')
x = x.replace('|13|','--Cachedunlock--')

x = x.replace('\n','--')
x = x.split('--')

while x.count(''):
	x.remove('')

#-----Dados da Classe Win32_LoggedOnUser-----#
command_line2 = '/usr/bin/wmic -U %s%%%s //%s "select Antecedent,Dependent from Win32_LoggedOnUser" ' %(name,senha,ip)

status2, y = commands.getstatusoutput(command_line2)

y = y.replace('CLASS: Win32_LoggedOnUser','')
y = y.replace('Antecedent|Dependent','')#'Dominio--Nome do Usuario--Id do Usuario
y = y.replace('\\\\.\\root\\cimv2:Win32_LogonSession.LogonId="','')
y = y.replace('\\\\.\\root\cimv2:Win32_Account.Domain=','')
y = y.replace('Name="','')
y = y.replace('"','')
y = y.replace('\n','|')
y = y.replace(',','|')
y = y.split('|')
#y = '--'.join(y)
#y = y.replace('|','--')

while y.count(''):
	y.remove('')


if status1 != 0 & status2 != 0:
        print "Problemas na obtencao de dados do host"
        sys.exit(1)


#-----Tratar Horário de conexão do usuário-----#
cont1 = 2
while cont1 < (len(x)-1):	
	aux = x[cont1]	
	ano = aux[:4]
	mes = aux[4:6]
	dia = aux[6:8]
	
	hora = aux[8:10]
	minutos = aux[10:12]
	segundos = aux[12:14]	
	
	aux = '%s-%s-%s %s:%s:%s' %(dia,mes,ano,hora,minutos,segundos)	
	x[cont1] = aux
	cont1 = cont1 + 3


#-----Hora no host-----#
command_line = '/usr/bin/wmic -U %s%%%s //%s "SELECT * FROM  Win32_LocalTime" ' %(name,senha,ip)
#print command_line
status2, timeHost = commands.getstatusoutput(command_line)
#print commands.getstatusoutput(command_line)
if status2 != 0:
	print 'Erro na obtencao de horario do host'
	sys.exit(1)

timeHost = timeHost.replace('CLASS: Win32_LocalTime','')
timeHost = timeHost.replace('Day|DayOfWeek|Hour|Milliseconds|Minute|Month|Quarter|Second|WeekInMonth|Year','')
timeHost = timeHost.replace('\n','')
timeHost = timeHost.split('|')

while timeHost.count(''):
	timeHost.remove('')

hostTime = '%s-%s-%s %s:%s:%s' %(timeHost[0],timeHost[5],timeHost[9],timeHost[2],timeHost[4],timeHost[7])



#-----Compara os Ids e junta O tipo de conexão com o nome do usuário-----#
cont1 = 0
while cont1 < (len(x)):
	cont2 = 2
	while cont2 < (len(y)-2):
		if x[cont1] == y[cont2]:
			y[cont2] = "%s|%s|%s" %(y[cont2],x[cont1 + 1],x[cont1 + 2])
		cont2 = cont2 + 3
	cont1 = cont1 + 2


cont2 = 2
while cont2 < (len(y)-2):
	if y[cont2].count('|') == 0:
		y[cont2] = "%s|null|null" %(y[cont2])	
	cont2 = cont2 + 3 


y = '|'.join(y)
y = y.split('|')


#-----Nome do host----#
command_line3 = '/usr/bin/wmic -U %s%%%s //%s "select Name from Win32_ComputerSystem" ' %(name,senha,ip)
status3, hostname  = commands.getstatusoutput(command_line3)

hostname = hostname.replace('CLASS: Win32_ComputerSystem','')
hostname = hostname.replace('Name','')
hostname = hostname.split('\n')

while hostname.count(''):
        hostname.remove('')

#''.join(hostname)


#-----CORPO FINAL-----#
corpo_final = """
                </table>
        </body>
</html>"""



#-----CORPO_LOCAL-----#
corpo_local = """
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">

<head>
        <title>Lista de Processos</title>
        <meta http-equiv="content-type" content="text/html;charset=utf-8" />
</head>

<body>

<table BORDER = 2 align="center">

        <tr>
                <TH align="center" COLSPAN=5>--------------- Lista de Usuarios Logados no host ---------------</TH>
        </tr>
        <tr>
                <TH>Dominio</TH>
                <TH>Nome</TH>
                <TH>Id</TH>
					 <TH>Tipo de Conexao</TH>
					 <TH>Inicio da Conexao</TH>
        </tr>
"""
	
controle_nomes_local = []
cont = 0
hostTime = hostTime.split('-')

while cont < (len(y)-4):
		timeConect = y[cont+4]
	
		if len(timeConect) > 0:
			timeConect = timeConect.split('-')
			
		if (y[cont] == hostname[0]) & ((y[cont+3] == "Conta do Sistema") | (y[cont+3] == "Network")):
				if (controle_nomes_local.count(y[cont+1]) == 0):
					if (timeConect[0] != "null"):
						if (int(hostTime[1]) == int(timeConect[1])) & (int(hostTime[0]) == int(timeConect[0])):
							controle_nomes_local.append(y[cont+1])             	
							corpo_local = corpo_local + '<tr align="Center"> <td>%s</td>              <td>%s</td>             <td>%s</td>				<td>%s</td>				<td>%s</td></tr>' %(y[cont],y[cont+1],y[cont+2],y[cont+3],y[cont+4])
		elif (y[cont] != hostname) & (y[cont+3] == "Terminal Services"):
				if (controle_nomes_local.count(y[cont+1]) == 0):
					if (timeConect[0] != "null"):									
						if (int(hostTime[1]) == int(timeConect[1])) & (int(hostTime[0]) == int(timeConect[0])):
							controle_nomes_local.append(y[cont+1])     		
							corpo_local = corpo_local + '<tr align="Center"> <td>%s</td>              <td>%s</td>             <td>%s</td>           <td>%s</td>				<td>%s</td></tr>' %(y[cont],y[cont+1],y[cont+2],y[cont+3],y[cont+4])
	
		cont = cont + 5


corpo_local = corpo_local + corpo_final


#-----CORPO_DOMINIO-----#
corpo_dominio = """
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">

<head>
        <title>Lista de Processos</title>
        <meta http-equiv="content-type" content="text/html;charset=utf-8" />
</head>

<body>

<table BORDER = 2 align="center">

        <tr>
                <TH align="center" COLSPAN=5>--------------- Lista de Usuarios Logados no dominio ---------------</TH>
        </tr>
        <tr>
                <TH>Dominio</TH>
                <TH>Nome</TH>
                <TH>Id</TH>
                <TH>Tipo de conexao</TH>
                <TH>Inicio da Conexao</TH>
        </tr>
"""


controle_nomes_dominio = []
cont = 0

while cont < (len(y)-4):
	timeConect = y[cont+4]
	if len(timeConect) > 0:
		timeConect = timeConect.split('-')
		
	if (y[cont] != hostname[0]):
		if (controle_nomes_dominio.count(y[cont+1]) == 0):
				if (timeConect[0] != "null"):
					if (int(hostTime[1]) == int(timeConect[1])) & (int(hostTime[0]) == int(timeConect[0])):
						controle_nomes_dominio.append(y[cont+1])
						corpo_dominio = corpo_dominio + '<tr align="Center"> <td>%s</td>              <td>%s</td>             <td>%s</td>		 			<td>%s</td>				<td>%s</td></tr>' %(y[cont],y[cont+1],y[cont+2],y[cont+3],y[cont+4])

	cont = cont + 5

corpo_dominio = corpo_dominio + corpo_final


if ((controle_nomes_dominio.count('Administrador')) > 0):
	print "Administrador conectado no Dominio."
	print "%s\n%s" %(corpo_local.replace('\n',''),corpo_dominio.replace('\n',''))
	sys.exit(1)
else:	
	#if (len(controle_nomes_dominio) > 0):
		print "Numero de usuários conectados no Dominio: %s" %(len(controle_nomes_dominio))
	#else:
	#	print "Numero de usuários conectados Dominio: 0"
	

print "%s\n%s" %(corpo_local.replace('\n',''),corpo_dominio.replace('\n',''))


sys.exit(0)
