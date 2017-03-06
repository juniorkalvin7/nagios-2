#!/usr/bin/python
# -*- coding: utf-8 -*-

#-------------------------
#Autor: Wagner Dias.     |
#                        |
#-------------------------


import commands
import sys
import time

ip = sys.argv[1]
name = sys.argv[2]
senha = sys.argv[3]

#------Memoria fisica total------#
command_line = '/usr/bin/wmic -U %s%%%s //%s "select TotalPhysicalMemory from Win32_ComputerSystem" ' %(name,senha,ip)

status, mem = commands.getstatusoutput(command_line)

if status != 0:
        print "Nao foi possivel obter a quantidade de memoria fisica dos host."
	sys.exit(1)

mem = mem.replace('CCLASS: Win32_ComputerSystem','')
mem = mem.replace('Name|TotalPhysicalMemory','')

mem = mem.split('|')

while mem.count(''):	
	mem.remove('')

memory = mem[1]


#------Processos ativos------#
command_line = '/usr/bin/wmic -U %s%%%s //%s "select Name,WorkingSetSize from Win32_Process" ' %(name,senha,ip)

status, x = commands.getstatusoutput(command_line)

if status != 0:
	print "Nao foi possivel obter a listagem de processos ativos."
	sys.exit(1)

x = x.replace('CLASS: Win32_Process','')
x = x.replace('Handle|Name|WorkingSetSize','')

x = x.replace('\n','|')
x = x.split('|')


while x.count(''):	
	x.remove('')

"""
#------Numero de Nucleos------#
command_line = '/usr/bin/wmic -U %s%%%s //%s "select NumberOfCores from Win32_Processor" ' %(name,senha,ip)

status, cores = commands.getstatusoutput(command_line)

if status != 0:
        print "Nao foi possivel identificar o numero de nucleos do processador."
	sys.exit(1)

cores = cores.replace('CLASS: Win32_Processor','')
cores = cores.replace('DeviceID|NumberOfCores','')

cores = cores.replace('\n','|')
cores = cores.split('|')
#x = ' -- '.join(x)

while x.count(''):	
	x.remove('')

num_cores = cores[1]
"""

#------Processamento por processo------#
command_line = '/usr/bin/wmic -U %s%%%s //%s "select Timestamp_Sys100NS, PercentProcessorTime, IDProcess from  Win32_PerfRawData_PerfProc_Process" ' %(name,senha,ip)
status, process1 =  commands.getstatusoutput(command_line)
process1 = process1.replace('CLASS: Win32_PerfRawData_PerfProc_Process','')
process1 = process1.replace('IDProcess|Name|PercentProcessorTime|Timestamp_Sys100NS','')
process1 = process1.split('\n')

while process1.count(''):	
	process1.remove('')

	
time.sleep(2)
	
status, process2 =  commands.getstatusoutput(command_line)
process2 = process2.replace('CLASS: Win32_PerfRawData_PerfProc_Process','')
process2 = process2.replace('IDProcess|Name|PercentProcessorTime|Timestamp_Sys100NS','')
process2 = process2.split('\n')
	
	
while process2.count(''):	
	process2.remove('')

	
#Calculo da diferencas entre Timestamp e PercentProcessorTime de process1 e process2
process_dif = []

cont = 0
while cont < len(process1):
	auxp1 = process1[cont]
	auxp2 = process2[cont]
	
	auxp1 = auxp1.split('|')
	auxp2 = auxp2.split('|')
	
	d1 = int(auxp1[2])
	n1 = int(auxp1[3])
	d2 = int(auxp2[2])
	n2 = int(auxp2[3])
	
	dn = d2 - d1
	nn = n2 - n1

	process_dif.append(auxp1[0])
	process_dif.append(dn)
	process_dif.append(nn)
		
	cont = cont + 1

corpo = """
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">

<head>
        <title>Lista de Processos</title>
        <meta http-equiv="content-type" content="text/html;charset=utf-8" />
</head>

<body>

<table BORDER = 2 align="center">

        <tr>
                <TH align="center" COLSPAN=5>--------------- Lista de Prcessos em execucao ---------------</TH>
        </tr>
        <tr>
                <TH>Id</TH>
                <TH>Nome</TH>
                <TH>Uso de memoria</TH>
		<TH>Uso de memoria(porcentagem)</TH>
		<TH>Uso de processamento(porcentagem)</TH>
        </tr>

"""	

cont = 0
cont_10 = 0
while cont < (len(x)-3):
	#Porcentagem
	mem_percent = float(x[cont+2]) * 100 / float(memory)
	
	#Processamento por processo
	for i in range (0, len(process_dif)): 
		if x[cont] == process_dif[i]:
			pross_percent = float(process_dif[i+1] / process_dif[i+2])		
		i = i + 3
	
	process_mem = int(x[cont+2])
	if process_mem >= 1024:
		process_mem = int(process_mem)/1024
		x[cont+2] = '%i Kb' %(process_mem)
		if process_mem > 1024:
			process_mem = int(process_mem)/1024
			x[cont+2] = '%i Mb' %(process_mem)
	else:		
		x[cont+2] = '%i bytes' %(process_mem)	
		
	corpo = corpo + '<tr align="Center"> <td>%s</td>              <td>%s</td>             <td>%s</td>		<td>%0.3f%%</td>		<td>%0.2f%%</td></tr>' %(x[cont],x[cont+1],x[cont+2],mem_percent,pross_percent)
	cont = cont + 3 
	
        cont_10 = cont_10+1
        if cont_10 >= 10:
            break

corpo_final = """
                </table>
        </body>
</html>"""


corpo = corpo + corpo_final
print "Numero de processos ativos: %s" %(len(x)/3)
print "%s" %(corpo.replace('\n',''))
sys.exit(0)
