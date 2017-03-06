#!/usr/bin/python	
import commands
import sys

ip = sys.argv[1]
name = sys.argv[2]
senha = sys.argv[3]

#Dados da Classe Win32_PerfRawData_MSSQLSERVER_SQLServerSQLStatistic
command_line = '/usr/bin/wmic -U %s%%%s //%s "select ActiveTempTables,ConnectionResetPersec,Description,EventNotificationsDelayedDrop,Frequency_Object,Frequency_PerfTime,Frequency_Sys100NS,HTTPAuthenticatedRequests,LogicalConnections,LoginsPersec,LogoutsPersec,MarsDeadlocks,Name,Nonatomicyieldrate,Processesblocked,SOAPEmptyRequests,SOAPMethodInvocations,SOAPSessionInitiateRequests,SOAPSessionTerminateRequests,SOAPSQLRequests,SOAPWSDLRequests,SQLTraceIOProviderLockWaits,Tempdbrecoveryunitid,Tempdbrowsetid,TempTablesCreationRate,TempTablesForDestruction,Timestamp_Object,Timestamp_PerfTime,Timestamp_Sys100NS,TraceEventNotificationQueue,Transactions,UserConnections from Win32_PerfRawData_MSSQLSERVER_SQLServerGeneralStatistics" '  %(name,senha,ip)


status1, x = commands.getstatusoutput(command_line)

x = x.replace('CLASS: Win32_PerfRawData_MSSQLSERVER_SQLServerGeneralStatistics','')
x = x.replace('ActiveTempTables|ConnectionResetPersec|Description|EventNotificationsDelayedDrop|Frequency_Object|Frequency_PerfTime|Frequency_Sys100NS|HTTPAuthenticatedRequests|LogicalConnections|LoginsPersec|LogoutsPersec|MarsDeadlocks|Name|Nonatomicyieldrate|Processesblocked|SOAPEmptyRequests|SOAPMethodInvocations|SOAPSessionInitiateRequests|SOAPSessionTerminateRequests|SOAPSQLRequests|SOAPWSDLRequests|SQLTraceIOProviderLockWaits|Tempdbrecoveryunitid|Tempdbrowsetid|TempTablesCreationRate|TempTablesForDestruction|Timestamp_Object|Timestamp_PerfTime|Timestamp_Sys100NS|TraceEventNotificationQueue|Transactions|UserConnections','')
x = x.replace('\n','')
x = x.split('|')


nomes = "ActiveTempTables|ConnectionResetPersec|Description|EventNotificationsDelayedDrop|Frequency_Object|Frequency_PerfTime|Frequency_Sys100NS|HTTPAuthenticatedRequests|LogicalConnections|LoginsPersec|LogoutsPersec|MarsDeadlocks|Name|Nonatomicyieldrate|Processesblocked|SOAPEmptyRequests|SOAPMethodInvocations|SOAPSessionInitiateRequests|SOAPSessionTerminateRequests|SOAPSQLRequests|SOAPWSDLRequests|SQLTraceIOProviderLockWaits|Tempdbrecoveryunitid|Tempdbrowsetid|TempTablesCreationRate|TempTablesForDestruction|Timestamp_Object|Timestamp_PerfTime|Timestamp_Sys100NS|TraceEventNotificationQueue|Transactions|UserConnections"

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
        <title> Statiticas de Banco de dados SQL</title>
        <meta http-equiv="content-type" content="text/html;charset=utf-8" />
</head>

<body>

<table BORDER = 2 align="center">

        <tr>
                <TH align="center" COLSPAN=2>--------------- Statisticas ---------------</TH>
        </tr>
        <tr>
                <TH>Variaveis</TH>
                <TH>Valor</TH>
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
