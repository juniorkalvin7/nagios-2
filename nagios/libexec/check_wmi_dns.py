#!/usr/bin/python	
# -*- coding: utf-8 -*-

#-------------------------
#Autor: Wagner Dias.     |
#                        |
#-------------------------

import commands
import sys

ip = sys.argv[1]
name = sys.argv[2]
senha = sys.argv[3]
warning = int(sys.argv[4])
critical = int(sys.argv[5])


#Dados da Classe Win32_PerfFormattedData_DNS_DNS

command_line = '/usr/bin/wmic -U %s%%%s //%s "select TotalQueryReceived,TotalResponseSent from Win32_PerfFormattedData_DNS_DNS" ' %(name,senha,ip)
status1, x = commands.getstatusoutput(command_line)

#Armazena apenas os valores
x = x.replace('CLASS: Win32_PerfFormattedData_DNS_DNS','')
x = x.replace('TotalQueryReceived|TotalResponseSent','') 
x = x.replace('\n','')
x = x.split('|')

nomes = "TotalQueryReceived|TotalResponseSent"
nomes = nomes.split('|')

if status1 != 0:
        print "Erro na obtencao de dados."
        sys.exit(1)


#------ARMAZENAR EM ARQUIVO------#
command_line = '/usr/bin/wmic -U %s%%%s //%s "select Name from Win32_ComputerSystem" ' %(name,senha,ip)
status1, hostname = commands.getstatusoutput(command_line)

if status1 == 1:
        print "Erro na obtencao de dados."
        sys.exit(1)

hostname = hostname.replace('CLASS: Win32_ComputerSystem','')
hostname = hostname.replace('Name','')
hostname = hostname.split('\n')

while hostname.count('') > 0:
	hostname.remove('')


#Garante a existencia do aqruivo wmi_dns_values.txt em /tmp
arquivo = open('/tmp/wmi_dns_values.txt','a')
#arquivo.close()

#Nomes a serem inserido no arquivo
temp_recive = '%s' %(hostname[0]) +'_recive'
temp_response = '%s' %(hostname[0])+'_response' 

#Valores atuais 
recive = int(x[0])
response = int(x[1])

#Pegar valores do arquivo
arquivo = open('/tmp/wmi_dns_values.txt','r')
conteudo = arquivo.read()
conteudo = conteudo.split(',')
#arquivo.close()

#Se ja estiver no arquivo
if (conteudo.count(temp_recive) != 0) & (conteudo.count(temp_response) != 0):
	index1 = conteudo.index(temp_recive)
	index2 = conteudo.index(temp_response)
	
	#Valores antigos
	old_recive = int(conteudo[int(index1)+1])
	old_response = int(conteudo[int(index2)+1])
	
	dif_recive = recive - old_recive
	dif_response = response - old_response

	if (dif_recive != 0) & (dif_response != 0):	
		percent_erro = 100-((100*dif_response)/dif_recive)
	
		#Substitui valores do arquivo
		conteudo[int(index1)+1] = str(recive)
		conteudo[int(index2)+1] = str(response)
		#','.join(conteudo)
		arquivo = open('/tmp/wmi_dns_values.txt','w')
		arquivo.write(','.join(conteudo))
		arquivo.close()
	else:
		percent_erro = 0 
			

#Caso não estaja no arquivo		
elif (conteudo.count(temp_recive) == 0) & (conteudo.count(temp_response) == 0):
	arquivo = open('/tmp/wmi_dns_values.txt','a')
	arquivo.write(','+temp_recive)
	arquivo.write(','+str(recive))
	arquivo.write(','+temp_response)
	arquivo.write(','+str(response))
	arquivo.close()

	dif_recive = recive
	dif_response = response
	
	if dif_response != 0:
		percent_erro = 100-((100*dif_response)/dif_recive)
	else:
		percent_erro = 0	

#-----CORPO-----#
corpo="""
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">

<head>
        <title>Lista de Processos</title>
        <meta http-equiv="content-type" content="text/html;charset=utf-8" />
</head>

<body>

<table BORDER = 2 align="center">

        <tr>
                <TH align="center" COLSPAN=2>--------------- DNS  ---------------</TH>
        </tr>
        <tr>
                <TH>Variaveis</TH>
                <TH>Valor</TH>
        </tr>
"""

corpo = corpo + '<tr align="Center"> <td>%s</td>              <td>%d</td></tr>' %(nomes[0],dif_recive)
corpo = corpo + '<tr align="Center"> <td>%s</td>              <td>%d</td></tr>' %(nomes[1],dif_response)


#-----CORPO FINAL-----#
corpo_final = """
                </table>
        </body>
</html>"""


corpo = corpo + corpo_final


if (percent_erro >= warning)&(percent_erro < critical):
	print "O servico encontra-se com %d%% de erro" %(percent_erro)
	print "%s" %(corpo.replace('\n',''))
	sys.exit(1)
elif (percent_erro >= critical):
	print "O servico encontra-se com %d%% de erro" %(percent_erro)
	print "%s" %(corpo.replace('\n',''))
	sys.exit(2)  
else:
	print "O servico encontra-se com %d%% de erro" %(percent_erro)
	print "%s" %(corpo.replace('\n',''))
	sys.exit(0)



