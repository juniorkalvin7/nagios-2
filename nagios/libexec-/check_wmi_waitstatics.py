#!/usr/bin/python
#coding: utf-8

import commands
import sys


ip = sys.argv[1]
name = sys.argv[2]
senha = sys.argv[3]

#Tipos
command_line = '/usr/bin/wmic -U %s%%%s //%s "SELECT Name FROM Win32_PerfFormattedData_MSSQLSERVER_SQLServerWaitStatistics" ' %(name,senha,ip)
status1, tipos = commands.getstatusoutput(command_line)

if status1 != 0:
	print "Não foi possivel obter os dados do servidor"
	sys.exit(1)
else:
	print "OK" 

#Armazena apenas os valores
tipos = tipos.replace('CLASS: Win32_PerfFormattedData_MSSQLSERVER_SQLServerWaitStatistics','')
tipos = tipos.replace('Name','')
tipos = tipos.split('\n')

while tipos.count('') > 0:
        tipos.remove('')

total = len(tipos)

#----- CORPO -----#
corpo="""
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">

	<head>
		<title>Sites</title>
		<meta http-equiv="content-type" content="text/html;charset=utf-8" />
                </head>

	<body> <CENTER> """


cont = 1 
while cont < total:
	nome = '\'%s\'' %tipos[cont]

	command_line = '/usr/bin/wmic -U %s%%%s //%s "SELECT Frequency_Object,Frequency_PerfTime,Frequency_Sys100NS,Lockwaits,Logbufferwaits,Logwritewaits,Memorygrantqueuewaits,NetworkIOwaits,NonPagelatchwaits,PageIOlatchwaits,Pagelatchwaits,Threadsafememoryobjectswaits,Timestamp_Object,Timestamp_PerfTime,Timestamp_Sys100NS,Transactionownershipwaits,Waitfortheworker,Workspacesynchronizationwaits FROM Win32_PerfFormattedData_MSSQLSERVER_SQLServerWaitStatistics WHERE  Name = %s" ' %(name,senha,ip,nome)
	status1, dados = commands.getstatusoutput(command_line)

	if status1 != 0:
		print "Não foi possivel obter os dados de %s" %(tipos[cont])
		'''sys.exit(1)'''

	dados = dados.replace('CLASS: Win32_PerfFormattedData_MSSQLSERVER_SQLServerWaitStatistics','')
	dados = dados.replace('Frequency_Object|Frequency_PerfTime|Frequency_Sys100NS|Lockwaits|Logbufferwaits|Logwritewaits|Memorygrantqueuewaits|Name|NetworkIOwaits|NonPagelatchwaits|PageIOlatchwaits|Pagelatchwaits|Threadsafememoryobjectswaits|Timestamp_Object|Timestamp_PerfTime|Timestamp_Sys100NS|Transactionownershipwaits|Waitfortheworker|Workspacesynchronizationwaits','')
	dados = dados.replace('\n','')
	dados  = dados.split('|')

	corpo = corpo + """
		<br><br>
		<table BORDER = 2 align="center">

			<tr>
				<TH align="center" COLSPAN=2>---------------  %s  ---------------</TH>
			</tr>
			<tr>
				<TH>Variavel</TH>
				<TH>Valor</TH>
			</tr>
	"""	%tipos[cont]

	#Insere dados do site na tabela
	corpo = corpo + '<tr align="Center"> <td>%s</td>              <td>%s</td></tr>' %('Frequency_Object', dados[0])
	'''corpo = corpo + '<tr align="Center"> <td>%s</td>              <td>%s</td></tr>' %('Frequency_PerfTime', dados[1])'''
	corpo = corpo + '<tr align="Center"> <td>%s</td>              <td>%s</td></tr>' %('Frequency_Sys100NS', dados[2])
	corpo = corpo + '<tr align="Center"> <td>%s</td>              <td>%s</td></tr>' %('Lockwaits', dados[3])
	corpo = corpo + '<tr align="Center"> <td>%s</td>              <td>%s</td></tr>' %('Logbufferwaits',dados[4])
	corpo = corpo + '<tr align="Center"> <td>%s</td>              <td>%s</td></tr>' %('Logwritewaits',dados[5])	
	corpo = corpo + '<tr align="Center"> <td>%s</td>              <td>%s</td></tr>' %('Memorygrantqueuewaits',dados[6])
	corpo = corpo + '<tr align="Center"> <td>%s</td>              <td>%s</td></tr>' %('NetworkIOwaits',dados[8])
	corpo = corpo + '<tr align="Center"> <td>%s</td>              <td>%s</td></tr>' %('NonPagelatchwaits',dados[9])
	corpo = corpo + '<tr align="Center"> <td>%s</td>              <td>%s</td></tr>' %('PageIOlatchwaits',dados[10])
	corpo = corpo + '<tr align="Center"> <td>%s</td>              <td>%s</td></tr>' %('Pagelatchwaits',dados[11])
	corpo = corpo + '<tr align="Center"> <td>%s</td>              <td>%s</td></tr>' %('Threadsafememoryobjectswaits',dados[12])
	corpo = corpo + '<tr align="Center"> <td>%s</td>              <td>%s</td></tr>' %('Timestamp_Object',dados[13])
	corpo = corpo + '<tr align="Center"> <td>%s</td>              <td>%s</td></tr>' %('Timestamp_PerfTime',dados[14])
	corpo = corpo + '<tr align="Center"> <td>%s</td>              <td>%s</td></tr>' %('Timestamp_Sys100NS',dados[15])
	corpo = corpo + '<tr align="Center"> <td>%s</td>              <td>%s</td></tr>' %('Transactionownershipwaits',dados[16])
	corpo = corpo + '<tr align="Center"> <td>%s</td>              <td>%s</td></tr>' %('Waitfortheworker',dados[17])
	corpo = corpo + '<tr align="Center"> <td>%s</td>              <td>%s</td></tr>' %('Workspacesynchronizationwaits',dados[18])	
	corpo = corpo +  """
		</table>"""

	cont = cont + 1



#----- CORPO FINAL -----#
corpo_final = """
	</CENTER></body>
</html>"""

corpo = corpo + corpo_final

print "%s\n" %(corpo.replace('\n',''))

sys.exit(0)

