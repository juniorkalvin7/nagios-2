#!/usr/bin/env python
# -*- coding: utf-8 -*-
import commands,sys
cmd='/usr/local/nagios/libexec/check_snmp'
a = " ".join(sys.argv[1:])
try:
  res=commands.getoutput('%s %s' %(cmd,a))
except Exception,e:
  print "CRITICAL - Erro na execucao do plugin",e
  sys.exit(1)
  
if 'noperf' in a:
  print res.split('|')[0]
else:
  print res
