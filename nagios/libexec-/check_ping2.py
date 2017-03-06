#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
 * Copyright (c) 2005 Gemayel Alves de Lira (gemayellira@gmail.com.br)
 * All rights reserved.                                                                
 *            Intechne Information Technologies                                        
 *            version 0.1 -             
 *
 * Redistribution and use in source and binary forms, with or without
 * modification, are permitted provided that the following conditions
 * are met:
 * 1. Redistributions of source code must retain the above copyright
 *    notice, this list of conditions and the following disclaimer.
 * 2. Redistributions in binary form must reproduce the above copyright
 *    notice, this list of conditions and the following disclaimer in the
 *    documentation and/or other materials provided with the distribution.
 *
 * THIS SOFTWARE IS PROVIDED BY THE INTECHNE INFORMATION TECNOLOGIES, INC. AND CONTRIBUTORS
 * ``AS IS'' AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED
 * TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
 * PURPOSE ARE DISCLAIMED.  IN NO EVENT SHALL THE FOUNDATION OR CONTRIBUTORS
 * BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
 * CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
 * SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
 * INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
 * CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
 * ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
 * POSSIBILITY OF SUCH DAMAGE.
"""


import commands
import time
import math
import os
import sys
import re,time,datetime
"""
sys.exit(0) OK
sys.exit(1) WARNING
sys.exit(2) CRITICAL
sys.exit(3)UNKNOWN
"""
args = sys.argv[1:]

if len(args)<3:
  print "Centreon Plugin\nCheck ping Latencia por GemayelLira"
  print "Argumentos:host community"
  print "IP WARN CRIT NPING"
  print "Ex.\n%s 10.10.10.253 400 600 3" % sys.argv[0] 
  #print 
  sys.exit(1)
else:
  #print args
  host=args[0]
  warning=args[1]
  critcal=args[2]
  cpint=args[3]
  
perdasave="/var/lib/centreon/centplugins/ping2_perda_%s" % host
t = datetime.datetime.now()
tempo1=time.mktime(t.timetuple())+(t.microsecond/1000000.)

saida=commands.getoutput('/bin/ping -n -c %s -i 1 %s ' % (cpint,host))
#saida=open('ping').read().rstrip()
#print saida
t = datetime.datetime.now()
tempo2=time.mktime(t.timetuple())+(t.microsecond/1000000.)
diferenca=str(tempo2-tempo1)

lastline = saida.split('\n')
qtlastline=len(lastline)
lastline = lastline[qtlastline-1]
perda= re.findall(", (.+?)%",saida)[0].split(', ')
perda=perda[len(perda)-1]
#print perda
#perda = '20'
#sys.exit()
if int(perda) > 0:
  if int(perda)==100:
      #print "GPING CRITICAL - %s|time=0 ok=0"% (saida.split('\n')[qtlastline-2],perda)
      print "GPING CRITICAL - %s|time=0 ok=0"% (perda)
      open(perdasave,'w').write('%s:%s' % (perda,diferenca))
      sys.exit(2)
  #if lastline.count('pipe'):
      #print "GPING CRITICAL - %s" % (saida.split('\n')[len(saida.split('\n'))-2])
  lll=saida.split('\n')[qtlastline-1]
  
  print "GPING CRITICAL - %s|time=%sms ok=1"% (lll,lll.split('mdev = ')[1].split('/')[1])
  open(perdasave,'w').write('%s:%s' % (perda,diferenca))
  sys.exit(2)

checkwarn=saida.replace(' ms','').split('\n')[qtlastline-1].split('mdev = ')[1].split('/')
warn=0
crit=0
lll = saida.split('\n')[qtlastline-1]
for i in checkwarn:
  val=int(i.split('.')[0])
  if val >= int(warning):
    if val >=int(critcal):
      crit=1
    warn=1
#print checkwarn

if crit==1:
  print "GPING CRITICAL - %s|time=%sms;20;50;; ok=1" % (lll,lll.split('mdev = ')[1].split('/')[1])
  open(perdasave,'w').write('0:%s' %diferenca)
  sys.exit(2)
if warn==1:
  print "GPING WARNING - %s|time=%sms;20;50;; ok=1" % (lll,lll.split('mdev = ')[1].split('/')[1])
  open(perdasave,'w').write('0:%s' %diferenca)
  sys.exit(1)
  
print "GPING OK - %s|time=%sms;20;50;; ok=1" % (lll,lll.split('mdev = ')[1].split('/')[1])
open(perdasave,'w').write('0:%s' % diferenca)
sys.exit(0)
#perda=perda[len(perda)-1]
#print perda
#print lastline

#print saida



