#!/usr/bin/python

import commands
import sys

ip = sys.argv[1]
name = sys.argv[2]
senha = sys.argv[3]

#Dados da Classe Win32_PerfFormattedData_DHCPServer_DHCPServer
command_line = '/usr/bin/wmic -U %s%%%s //%s "select AcksPersec,ActiveQueueLength,ConflictCheckQueueLength,DeclinesPersec,Deniedduetomatch,Deniedduetononmatch,DiscoversPersec,DuplicatesDroppedPersec,Frequency_Object,Frequency_PerfTime,Frequency_Sys100NS,InformsPersec,MillisecondsperpacketAvg,NacksPersec,OfferQueueLength,OffersPersec,PacketsExpiredPersec,PacketsReceivedPersec,ReleasesPersec,RequestsPersec,Timestamp_Object,Timestamp_PerfTime,Timestamp_Sys100NS from Win32_PerfFormattedData_DHCPServer_DHCPServer" ' %(name,senha,ip)

status1, x = commands.getstatusoutput(command_line)

x = x.replace('CLASS: Win32_PerfFormattedData_dhcpserver_DHCPServer','')
x = x.replace('AcksPersec|ActiveQueueLength|ConflictCheckQueueLength|DeclinesPersec|Deniedduetomatch|Deniedduetononmatch|DiscoversPersec|DuplicatesDroppedPersec|Frequency_Object|Frequency_PerfTime|Frequency_Sys100NS|InformsPersec|MillisecondsperpacketAvg|NacksPersec|OfferQueueLength|OffersPersec|PacketsExpiredPersec|PacketsReceivedPersec|ReleasesPersec|RequestsPersec|Timestamp_Object|Timestamp_PerfTime|Timestamp_Sys100NS','')

x = x.replace('\n','')
x = x.split('|')


nomes = "AcksPersec|ActiveQueueLength|ConflictCheckQueueLength|DeclinesPersec|Deniedduetomatch|Deniedduetononmatch|DiscoversPersec|DuplicatesDroppedPersec|Frequency_Object|Frequency_PerfTime|Frequency_Sys100NS|InformsPersec|MillisecondsperpacketAvg|NacksPersec|OfferQueueLength|OffersPersec|PacketsExpiredPersec|PacketsReceivedPersec|ReleasesPersec|RequestsPersec|Timestamp_Object|Timestamp_PerfTime|Timestamp_Sys100NS" 

nomes = nomes.split('|')


if status1 == 0:
	print "Ok"
else:
	print "Erro na obtencao de dados."
	sys.exit(1)

i = 0 
while i < len(x):
	print "%s--%s" %(nomes[i],x[i])
	i = i + 1


sys.exit(0)
