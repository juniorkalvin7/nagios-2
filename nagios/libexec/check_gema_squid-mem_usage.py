#!/usr/bin/env python
# -*- coding: utf-8 -*-
import commands
import time
import math
import os
import sys

args = sys.argv[1:]

if len(args)<2:
  print "Centreon Plugin\nGet Squid - Cache Mem Usage"
  print "Argumentos:host community"
  print "Ex.\n%s 10.0.0.45 u3fr0I9b5" % sys.argv[0] 
  #print 
  sys.exit(1)
else:
  #print args
  host=args[0]
  community=args[1]
try:
  valor=(commands.getoutput("/usr/bin/snmpwalk -t 100000 -v 1 -c %s %s:3401 1.3.6.1.4.1.3495.1.3.1.3" %(community,str(host)))).split(': ')[1]
except Exception,e:
  print "CRITICAL - nao consegui capturar valores"
  print e
  sys.exit(2)

def convertbit(bits):
  bits = float(str(bits)+'.0')/1048576
  if (bits  > 1000):
    bits  = bits  / 1000;
    bits_unit = "G"
  else:
    bits_unit = "M"
  return(bits,bits_unit)

print "Squid - Cache Mem Usage - %s%s|used=%so" % ('%.2f'%(convertbit(valor)[0]),convertbit(valor)[1],valor)
