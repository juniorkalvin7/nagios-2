#!/usr/bin/env python
# -*- coding: utf-8 -*-
import commands
import time
import math
import os
import sys

args = sys.argv[1:]

if len(args)<2:
  print "Centreon Plugin\nCheck Port por GemayelLira"
  print "Argumentos:host community MIB"
  print "Ex.\n%s 10.0.0.0 u3fr0I9b5 .1.3.6.1.4.1.2022.20" % sys.argv[0] 
  #print 
  sys.exit(1)
else:
  #print args
  host=args[0]
  community=args[1]
  mib=args[2]
try:
  status=(commands.getoutput("/usr/bin/snmpwalk -t 100000 -v 1 -c %s %s %s.101.1" %(community,str(host),mib))).split("\"")[1]
  
except Exception,e:
  print "CRITICAL - nao consegui capturar valores"
  print e
  sys.exit(2)
if status.count('CLOSED'):
  print "".join(status)
  sys.exit(2)
print "".join(status)
sys.exit(0)

  
