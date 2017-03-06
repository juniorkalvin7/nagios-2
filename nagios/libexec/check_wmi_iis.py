#!/usr/bin/python
#coding: utf-8

import commands
import sys


ip = sys.argv[1]
name = sys.argv[2]
senha = sys.argv[3]

#Total de sites
command_line = '/usr/bin/wmic -U %s%%%s //%s "select Name from Win32_PerfRawData_W3SVC_WebService" ' %(name,senha,ip)
status1, sites = commands.getstatusoutput(command_line)

#http://support.microsoft.com/kb/313064/pt-br

if status1 != 0:
	print "Não foi possivel obter os dados do servidor"
	sys.exit(1)
 

#Armazena apenas os valores
sites = sites.replace('CLASS: Win32_PerfRawData_W3SVC_WebService','')
sites = sites.replace('Name','')
sites = sites.replace('_Total', '')
sites = sites.split('\n')

while sites.count('') > 0:
        sites.remove('')

totalSites = len(sites)

#----- CORPO -----#
corpo="""
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">

	<head>
		<title>Sites</title>
		<meta http-equiv="content-type" content="text/html;charset=utf-8" />
        </head>

	<body> <CENTER> """


cont = 0 
while cont < totalSites:
	
	nomeSite = '\'%s\'' %sites[cont]	
	
	command_line = '/usr/bin/wmic -U %s%%%s //%s " SELECT BytesReceivedPerSec,BytesSentPerSec,ConnectionAttemptsPerSec,CurrentAnonymousUsers,CurrentConnections,FilesPerSec,FilesReceivedPerSec,FilesSentPerSec,LockedErrorsPerSec,NotFoundErrorsPerSec,PostRequestsPerSec FROM Win32_PerfRawData_W3SVC_WebService WHERE  Name = %s" ' %(name,senha,ip,nomeSite)
	status1, dadosSite = commands.getstatusoutput(command_line)
	
	if status1 != 0:
		print "Não foi possivel obter os dados do site %s" %(sites[cont])
		sys.exit(1)
	
	dadosSite = dadosSite.replace('CLASS: Win32_PerfRawData_W3SVC_WebService','')
	dadosSite = dadosSite.replace('BytesReceivedPersec|BytesSentPersec|ConnectionAttemptsPersec|CurrentAnonymousUsers|CurrentConnections|FilesPersec|FilesReceivedPersec|FilesSentPersec|LockedErrorsPersec|Name|NotFoundErrorsPersec|PostRequestsPersec','')
	dadosSite = dadosSite.replace('\n','')
	dadosSite  = dadosSite.split('|')
	
	corpo = corpo + """
		<br><br>
		<table BORDER = 2 align="center">
	
			<tr>
				<TH align="center" COLSPAN=2>--------------- Site %s  ---------------</TH>
			</tr>
			<tr>
				<TH>Variavel</TH>
				<TH>Valor</TH>
			</tr>
	"""	%sites[cont]
	
	#Insere dados do site na tabela
	#corpo = corpo + '<tr align="Center"> <td>%s</td>              <td>%s/sec</td></tr>' %('AnonymousUsersPersec', dadosSite[0])
	corpo = corpo + '<tr align="Center"> <td>%s</td>              <td>%s/sec</td></tr>' %('BytesReceivedPersec', dadosSite[0])
	corpo = corpo + '<tr align="Center"> <td>%s</td>              <td>%s/sec</td></tr>' %('BytesSentPersec', dadosSite[1])
	corpo = corpo + '<tr align="Center"> <td>%s</td>              <td>%s/sec</td></tr>' %('ConnectionAttemptsPersec', dadosSite[2])
	corpo = corpo + '<tr align="Center"> <td>%s</td>              <td>%s</td></tr>' %('CurrentAnonymousUsers', dadosSite[3])
	corpo = corpo + '<tr align="Center"> <td>%s</td>              <td>%s</td></tr>' %('CurrentConnections',dadosSite[4])
	corpo = corpo + '<tr align="Center"> <td>%s</td>              <td>%s/sec</td></tr>' %('FilesPersec',dadosSite[5])
	corpo = corpo + '<tr align="Center"> <td>%s</td>              <td>%s/sec</td></tr>' %('FilesReceivedPersec',dadosSite[6])
	corpo = corpo + '<tr align="Center"> <td>%s</td>              <td>%s/sec</td></tr>' %('FilesSentPersec',dadosSite[7])
	corpo = corpo + '<tr align="Center"> <td>%s</td>              <td>%s/sec</td></tr>' %('LockedErrorsPersec',dadosSite[8])
	corpo = corpo + '<tr align="Center"> <td>%s</td>              <td>%s/sec</td></tr>' %('NotFoundErrorsPersec',dadosSite[10])
	corpo = corpo + '<tr align="Center"> <td>%s</td>              <td>%s/sec</td></tr>' %('PostRequestsPersec',dadosSite[11])
	corpo = corpo +  """
		</table>"""
	
	cont = cont + 1


#----- CORPO FINAL -----#
corpo_final = """
	</CENTER></body>
</html>"""

corpo = corpo + corpo_final

print 'número de sites: %d' %(totalSites) 
print "%s\n" %(corpo.replace('\n',''))

sys.exit(0)

