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

command_line = '/usr/bin/wmic -U %s%%%s //%s "SELECT Name,SerialNumber,InstallDate FROM Win32_OperatingSystem" ' %(name,senha,ip)
status1, dados = commands.getstatusoutput(command_line)

if status1 != 0:
	print "Não foi possivel obter os dados do servidor"
	sys.exit(1)

#Armazena apenas tipos de Erros
dados = dados.replace('CLASS: Win32_OperatingSystem','')
dados = dados.replace('InstallDate|Name|SerialNumber','')
dados = dados.replace('\n','')
dados = dados.split('|')


while dados.count('') > 0:
        dados.remove('')


#----- CORPO -----#
corpo="""
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">

	<head>
		<title>DB Errors</title>
		<meta http-equiv="content-type" content="text/html;charset=utf-8" />
                </head>

	<body> <CENTER> """


data = str(dados[0])


corpo = corpo + """
		<br><br>
		<table BORDER = 2 align="center">

			<tr>
				<TH align="center" COLSPAN=2>---------------  Descricao  ---------------</TH>
			</tr>
			<tr>
				<TH>Variavel</TH>
				<TH>Valor</TH>
			</tr>
"""	


#Insere dados do site na tabela
corpo = corpo + '<tr align="Center"> <td>%s</td>              <td>%s</td></tr>' %('Sistema Oparacional', dados[1])
corpo = corpo + '<tr align="Center"> <td>%s</td>              <td>%s</td></tr>' %('Serial', dados[3])
corpo = corpo + '<tr align="Center"> <td>%s</td>              <td>%s-%s-%s</td></tr>' %('Data de Instalacao', data[:4],data[4:6],data[6:8])
corpo = corpo +  """
		</table>"""


#----- CORPO FINAL -----#
corpo_final = """
	</CENTER></body>
</html>"""

corpo = corpo + corpo_final

print "Sistema Operacional: %s" %(dados[1]) 
print "%s\n" %(corpo.replace('\n',''))

sys.exit(0)

