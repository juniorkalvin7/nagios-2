#!/usr/bin/env python
# -*- coding: utf-8 -*-
import commands
import time
import math
import os
import sys

args = sys.argv[1:]

if len(args)<2:
  print "Centreon Plugin\nGet Squid - Server Requests"
  print "Argumentos:host community"
  print "Ex.\n%s 10.0.0.45 u3fr0I9b5" % sys.argv[0] 
  #print 
  sys.exit(1)
else:
  #print args
  host=args[0]
  community=args[1]
try:
  status=(commands.getoutput("/usr/bin/snmpwalk -t 100000 -v 1 -c %s %s:3401 1.3.6.1.4.1.3495.1.3.2.1.10" %(community,str(host)))).split('INTEGER: ')[1]
except Exception,e:
  print "CRITICAL - nao consegui capturar valores"
  print e
  sys.exit(2)

arquivo="/var/lib/centreon/centplugins/squid_%s_server_requests" % (str(host))
  
if os.path.exists(arquivo) == False:
  open(arquivo,'w').write('%s' % (str(status)))
  print "Primeira execucao armazenando dados..."
  #print ""
  sys.exit(1)

status_old=open(arquivo,'r').read().rstrip()
open(arquivo,'w').write('%s' % (str(status)))
valor=int(status)-int(status_old)
print "Squid - Server HTTP Requests - %d|squidstat=%d squidstatb=%d" % (valor,valor,valor)

