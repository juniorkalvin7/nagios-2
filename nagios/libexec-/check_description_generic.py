#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import commands
import os.path
"""
Tipos de saida: 
0 ok
1 critical
2 warning
3 unknown
"""
args = sys.argv[1:]
if len(args)<3:
  print "Centreon Plugin\nGeneric Captura Descricao do Dispositivo por GemayelLira"
  print "Argumentos:host community MIB"
  print "Ex.\n%s 172.18.0.6 u3fr0I9b5 .1.3.6.1.4.1.3709.3.5.201.1.1.3.3.0" % sys.argv[0] 
  sys.exit(1)
else:
  host=args[0]
  community=args[1]
  mib=args[2]
cookie_file='/var/lib/centreon/centplugins/description_%s'%host
try:
  status=(commands.getoutput("/usr/bin/snmpwalk -t 100000 -v 1 -c %s %s %s" % (community,str(host),mib))).split("\"")[1]
except Exception,e:
  print "CRITICAL - nao consegui capturar valores"
  print e
  sys.exit(2)

  
if os.path.isfile(cookie_file):
  st=open(cookie_file,'r').read().rstrip()
  if st!=status:
    print 'CRITICAL - Descricao do dispositivo modificada, original: %s atual: %s|ok=0' % (st,status)
    print 'Info:cookie_file = %s'%cookie_file
    sys.exit(1)
  else:
    print 'OK - Descricao: %s|ok=1' % status
else:
  print 'WARNING - Criando cookie_file com descricao do dispositivo'
  open(cookie_file,'w').write(status)
  sys.exit(2)
