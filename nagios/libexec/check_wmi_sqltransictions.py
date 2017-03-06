#!/usr/bin/python	

#-------------------------
#Autor: Wagner Dias.     |
#                        |
#-------------------------


import commands
import sys


ip = sys.argv[1]
name = sys.argv[2]
senha = sys.argv[3]

#Win32_PerfFormattedData_MSSQLSERVER_SQLServerTransactions
command_line = '/usr/bin/wmic -U %s%%%s //%s "SELECT Description,FreeSpaceintempdbKB,LongestTransactionRunningTime,NonSnapshotVersionTransactions,SnapshotTransactions,Transactions,Updateconflictratio,UpdateSnapshotTransactions,VersionCleanuprateKBPers,VersionGenerationrateKBPers,VersionStoreSizeKB,VersionStoreunitcount,VersionStoreunitcreation,VersionStoreunittruncation FROM Win32_PerfFormattedData_MSSQLSERVER_SQLServerTransactions" '  %(name,senha,ip)


status1, x = commands.getstatusoutput(command_line)

x = x.replace('CLASS: Win32_PerfFormattedData_MSSQLSERVER_SQLServerTransactions','')
x = x.replace('Description|FreeSpaceintempdbKB|LongestTransactionRunningTime|NonSnapshotVersionTransactions|SnapshotTransactions|Transactions|Updateconflictratio|UpdateSnapshotTransactions|VersionCleanuprateKBPers|VersionGenerationrateKBPers|VersionStoreSizeKB|VersionStoreunitcount|VersionStoreunitcreation|VersionStoreunittruncation','')
x = x.replace('\n','')
x = x.split('|')


nomes = "Description|FreeSpaceintempdbKB|LongestTransactionRunningTime|NonSnapshotVersionTransactions|SnapshotTransactions|Transactions|Updateconflictratio|UpdateSnapshotTransactions|VersionCleanuprateKBPers|VersionGenerationrateKBPers|VersionStoreSizeKB|VersionStoreunitcount|VersionStoreunitcreation|VersionStoreunittruncation"

nomes = nomes.split('|')


if status1 == 0:
        print "Ok"
else:
        print "Erro na obtencao de dados."
        sys.exit(1)


#-----CORPO-----#
corpo="""
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">

<head>
        <title> Statiticas de Buffer de Banco de dados SQL</title>
        <meta http-equiv="content-type" content="text/html;charset=utf-8" />
</head>

<body>

<table BORDER = 2 align="center">

        <tr>
                <TH align="center" COLSPAN=2>---------------Transictions Statistics ---------------</TH>
        </tr>
        <tr>
                <TH>Property</TH>
                <TH>Value</TH>
        </tr>
"""

cont = 0
while cont < (len(x)):
	corpo = corpo + '<tr align="Center"> <td>%s</td>              <td>%s</td></tr>' %(nomes[cont],x[cont]) 
        cont = cont + 1



#-----CORPO FINAL-----#
corpo_final = """
                </table>
        </body>
</html>"""


corpo = corpo + corpo_final


print "%s" %(corpo.replace('\n',''))
sys.exit(0)
