#!/usr/bin/python
#coding: utf-8

import commands
import sys


ip_AD = sys.argv[1]
ip_host = sys.argv[2]
name = sys.argv[3]
senha = sys.argv[4]

#Hora no AD
command_line = '/usr/bin/wmic -U %s%%%s //%s "SELECT * FROM  Win32_LocalTime" ' %(name,senha,ip_AD)
status1, time1 = commands.getstatusoutput(command_line)

if status1 != 0:
	print 'Erro na obtencao de dados do host'
	sys.exit(1)

#Hora no host
command_line = '/usr/bin/wmic -U %s%%%s //%s "SELECT * FROM  Win32_LocalTime" ' %(name,senha,ip_host)
status2, time2 = commands.getstatusoutput(command_line)

if status2 != 0:
	print 'Erro na obtencao de dados do host'
	sys.exit(1)

time1 = time1.replace('CLASS: Win32_LocalTime','')
time1 = time1.replace('Day|DayOfWeek|Hour|Milliseconds|Minute|Month|Quarter|Second|WeekInMonth|Year','')
time1 = time1.split('|')

while time1.count(''):
	time1.remove('')

T1 = '%s:%s:%s - %s de %s de %s' %(time1[2],time1[4],time1[7],time1[0],time1[5],time1[9])


time2 = time2.replace('CLASS: Win32_LocalTime','')
time2 = time2.replace('Day|DayOfWeek|Hour|Milliseconds|Minute|Month|Quarter|Second|WeekInMonth|Year','')
time2 = time2.split('|')

while time2.count(''):
	time2.remove('')

T2 = '%s:%s:%s - %s de %s de %s' %(time2[2],time2[4],time2[7],time2[0],time2[5],time2[9])

#-----CORPO-----#
corpo="""
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">

<head>
        <title>Horarios</title>
        <meta http-equiv="content-type" content="text/html;charset=utf-8" />
</head>

	<body>

		<table BORDER = 2 align="center">

        		<tr>
                		<TH align="center" COLSPAN=2>--------------- Horarios  ---------------</TH>
        		</tr>
        		<tr>
            		   <TH>Hora AD</TH>
                		<TH>Hora Host</TH>
        		</tr>
"""

corpo = corpo + '<tr align="Center"> <td>%s</td>              <td>%s</td></tr>' %(T1,T2)

#-----CORPO FINAL-----#
corpo_final = """
                </table>
        </body>
</html>"""

corpo = corpo + corpo_final

if time1[2] == time2[2]:
	minuto1 = int(time1[4])
	minuto2 = int(time2[4])
	
	if (minuto1 >= minuto2):
		dif = minuto1 - minuto2
		if (dif >= 0) & (dif <= 5 ):
			if (time1[0] == time2[0]) & (time1[5] == time2[5]) & (time1[9] == time2[9]):
				print 'O horario do host corresponde ao horario do Controlador de Dominio: %s' %(T2.replace('\n',''))
				print "%s" %(corpo.replace('\n',''))
				sys.exit(0)	
	
	elif (minuto1 < minuto2):
		dif = minuto2 - minuto1
		if (dif >= 1) & (dif <= 5):
			if (time1[0] == time2[0]) & (time1[5] == time2[5]) & (time1[9] == time2[9]):
				print 'O horario do host corresponde ao horario do Controlador de Dominio: %s' %(T2.replace('\n',''))
				print "%s" %(corpo.replace('\n',''))
				sys.exit(0)	

										
print 'O horario do host nao corresponde ao horario do Controlador de Dominio.' 
print "%s" %(corpo.replace('\n',''))
sys.exit(1)
