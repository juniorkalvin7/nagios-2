#!/usr/bin/env python
# -*- coding: utf-8 -*-
import commands
import pickle
import sys

#logfile='/media/cloud-remotefs/var/log/instance_atu_db_sit.dic2'
logfile='/var/log/instance_atu_db_sit.dic'
sit_geral = pickle.load(open(logfile))
status=[]
pollers=[]
statusoff=[]
crit=0
for i in sit_geral:
  if int(sit_geral[i][1])==0:
    crit=1
    statusoff.append('%s=%s' % (i,sit_geral[i][1]))
  else:
    status.append('%s=%s' % (i,sit_geral[i][1]))
    pollers.append(i.split('_')[1])
if crit==0:
  print 'OK - %d Satelites Encontrados %s|%s' % (len(pollers),','.join(pollers),' '.join(status))
  print 'Mensagem da verificacao:'
  for i in sit_geral:
    print '%s %s' % (i,sit_geral[i][0])
  print 'Ultimas 10 Linhas de log:'
  print commands.getoutput('tail -n10 /var/log/instance_atu.log')
else:
  print 'CRITICAL - Satelite %s DOWN %d UP|%s %s' % (','.join(statusoff).replace('=0','').replace('Satelite_',''),len(pollers),' '.join(status),' '.join(statusoff))
  print 'Mensagem da verificacao:'
  for i in sit_geral:
    print '%s %s' % (i,sit_geral[i][0])
  print 'Ultimas 10 Linhas de log:'
  print commands.getoutput('tail -n10 /var/log/instance_atu.log')
  sys.exit(2)
