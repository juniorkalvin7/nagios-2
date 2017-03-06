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

#Total de bancos
command_line = '/usr/bin/wmic -U %s%%%s //%s "SELECT Name FROM Win32_PerfRawData_MSSQLSERVER_SQLSERVERDatabases" ' %(name,senha,ip)
status1, bancos = commands.getstatusoutput(command_line)

if status1 != 0:
        print "Não foi possivel obter os dados do servidor"
        sys.exit(1)
else:
        print "OK"

#Armazena apenas os valores
bancos = bancos.replace('CLASS: Win32_PerfRawData_MSSQLSERVER_SQLServerDatabases','')
bancos = bancos.replace('Name','')
bancos = bancos.split('\n')

while bancos.count('') > 0:
        bancos.remove('')

totalBancos = len(bancos)
#----- CORPO -----#
corpo="""
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">

        <head>
                <title>Bancos Instanciados</title>
                <meta http-equiv="content-type" content="text/html;charset=utf-8" />
                </head>

        <body> <CENTER>"""


cont = 0
while cont < totalBancos:
        nomeBanco = '\'%s\'' %bancos[cont]

        command_line = '/usr/bin/wmic -U %s%%%s //%s "SELECT DataFilesSizeKB, Committableentries, ActiveTransactions, LogFilesSizeKB FROM Win32_PerfRawData_MSSQLSERVER_SQLSERVERDatabases where Name = %s" ' %(name,senha,ip,nomeBanco)
        status1, dadosBanco = commands.getstatusoutput(command_line)

        if status1 != 0:
                print "Não foi possivel obter os dados do banco %s" %(bancos[cont])
                sys.exit(1)

        dadosBanco = dadosBanco.replace('CLASS: Win32_PerfRawData_MSSQLSERVER_SQLServerDatabases','')
        dadosBanco = dadosBanco.replace('ActiveTransactions|Committableentries|DataFilesSizeKB|LogFilesSizeKB|Name','')
        dadosBanco = dadosBanco.replace('\n','')
        dadosBanco = dadosBanco.split('|')

        corpo = corpo + """
			<br><br>
                <table BORDER = 2 align="center">

                        <tr>
                                <TH align="center" COLSPAN=2>--------------- Banco %s  ---------------</TH>
                        </tr>
                        <tr>
                                <TH>Variavel</TH>
                                <TH>Valor</TH>
                        </tr>
        """     %bancos[cont]

        #Insere dados do site na tabela
        corpo = corpo + '<tr align="Center"> <td>%s</td>              <td>%s</td></tr>' %('DataFilesSizeKB',dadosBanco[2])
        corpo = corpo + '<tr align="Center"> <td>%s</td>              <td>%s</td></tr>' %('LogFilesSizeKB',dadosBanco[3])
        corpo = corpo + '<tr align="Center"> <td>%s</td>              <td>%s</td></tr>' %('ActiveTransactions',dadosBanco[0])
        corpo = corpo + '<tr align="Center"> <td>%s</td>              <td>%s</td></tr>' %('Committableentries',dadosBanco[1])

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



