#!/usr/bin/python
#coding: utf-8

#-------------------------
#Autor: Wagner Dias.     |
#                        |
#-------------------------


import commands
import sys


ip = sys.argv[1]
name = sys.argv[2]
senha = sys.argv[3]

#Total de typeErrors
command_line = '/usr/bin/wmic -U %s%%%s //%s "select Name from  Win32_PerfFormattedData_MSSQLSERVER_SQLServerSQLErrors" ' %(name,senha,ip)
status1, typeErrors = commands.getstatusoutput(command_line)

if status1 != 0:
	print "Não foi possivel obter os dados do servidor"
	sys.exit(1)
else:
	print "OK" 

#Armazena apenas tipos de Erros
typeErrors = typeErrors.replace('CLASS: Win32_PerfFormattedData_MSSQLSERVER_SQLServerSQLErrors','')
typeErrors = typeErrors.replace('Name','')
typeErrors = typeErrors.replace('_Total','')
typeErrors = typeErrors.split('\n')

while typeErrors.count('') > 0:
        typeErrors.remove('')

totalTypeErrors = len(typeErrors)

#----- CORPO -----#
corpo="""
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">

	<head>
		<title>DB Errors</title>
		<meta http-equiv="content-type" content="text/html;charset=utf-8" />
                </head>

	<body> <CENTER> """


cont = 0 
while cont < totalTypeErrors:
	tipo = '\'%s\'' %typeErrors[cont]

	command_line = '/usr/bin/wmic -U %s%%%s //%s " SELECT ErrorsPersec,Timestamp_Object,Timestamp_PerfTime,Timestamp_Sys100NS FROM Win32_PerfFormattedData_MSSQLSERVER_SQLServerSQLErrors WHERE  Name = %s" ' %(name,senha,ip,tipo)
	status1, errors = commands.getstatusoutput(command_line)

	if status1 != 0:
		print "Não foi possivel obter os dados do site %s" %(typeErrors[cont])
		sys.exit(1)

	errors = errors.replace('CLASS: Win32_PerfFormattedData_MSSQLSERVER_SQLServerSQLErrors','')
	errors = errors.replace('ErrorsPersec|Name|Timestamp_Object|Timestamp_PerfTime|Timestamp_Sys100NS','')
	errors = errors.replace('\n','')
	errors  = errors.split('|')

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
	"""	%typeErrors[cont]

	#Insere dados do site na tabela
	corpo = corpo + '<tr align="Center"> <td>%s</td>              <td>%s/sec</td></tr>' %('ErrorsPersec', errors[0])
	corpo = corpo + '<tr align="Center"> <td>%s</td>              <td>%s</td></tr>' %('Timestamp_Object', errors[2])
	corpo = corpo + '<tr align="Center"> <td>%s</td>              <td>%s</td></tr>' %('Timestamp_PerfTime', errors[3])
	corpo = corpo + '<tr align="Center"> <td>%s</td>              <td>%s</td></tr>' %('Timestamp_Sys100NS', errors[4])
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

