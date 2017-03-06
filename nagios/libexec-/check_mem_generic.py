#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import commands
"""
Tipos de saida: 
0 ok
1 critical
2 warning
3 unknown
"""
args = sys.argv[1:]
if len(args)<4:
  print "Centreon Plugin\nCheck Generic Memory\n Originalemnte criado para dispositivos MPU por GemayelLira"
  print "Argumentos:host community MIB"
  print "Ex.\n%s 172.18.0.6 u3fr0I9b5 .1.3.6.1.4.1.3709.3.5.201.1.1.11.0 80 90" % sys.argv[0] 
  sys.exit(1)
else:
  host=args[0]
  community=args[1]
  mib=args[2]
  try:
    warn=int(args[3])
    crit=int(args[4])
  except:
    print 'CRITICAL - Valor inserido critico e warning incorreto configure corretamente.'
    sys.exit(2)

try:
  status=(commands.getoutput("/usr/bin/snmpwalk -t 100000 -v 1 -c %s %s %s" % (community,str(host),mib))).split(" ")[3]
except Exception,e:
  print "CRITICAL - nao consegui capturar valores"
  print e
  sys.exit(2)

try:
  st=int(status)
except Exception,e:
  print 'CRITICAL - valor retornado esta incorreto'
  print status
  print e
  sys.exit(2)


if st>=crit :
  print 'CRITICAL - Uso de Memoria %d%%|mem=%d' % (st,st)
  sys.exit(1)
elif st>=warn:
  print 'WARNING - Uso de Memoria %d%%|mem=%d' % (st,st)
  sys.exit(2)
else:
  print 'OK - Uso de Memoria %d%%|mem=%d' % (st,st)
  sys.exit(0)
