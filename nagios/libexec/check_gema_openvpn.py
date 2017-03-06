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
import string 

args = sys.argv[1:]
# /usr/bin/ssh -o ConnectTimeout=30  -q 172.20.0.1 -p 2222 'echo "[1269027045] SCHEDULE_FORCED_SVC_CHECK;nagios-prod-semit-01;OpenVPN;1269027045" >> /usr/local/nagios/var/rw/nagios.cmd'

#loginlog='/tmp/openvpn.logins.log'
#loginlog='/var/log/openvpn-users.log'

if len(args)<2:
  print "Centreon Plugin\nOpenvpn por GemayelLira"
  print "Argumentos:host community"
  print "Ex.\n%s 172.20.0.1 u3fr0I9b5" % sys.argv[0] 
  #print 
  sys.exit(1)
else:
  #print args
  host=args[0]
  community=args[1]
  mib='.1.3.6.1.4.1.2022.12'
try:
  if host == "187.60.120.10":
    status=(commands.getoutput("/usr/bin/snmpwalk -t 100000 -v 1 -c %s %s %s.4.1.2.8.117.115.117.97.114.105.111.115.1" %(community,str(host),mib))).split("\"")[1]
  else:
    status=(commands.getoutput("/usr/bin/snmpwalk -t 100000 -v 1 -c %s %s %s.101.1" %(community,str(host),mib))).split("\"")[1]
  
except Exception,e:
  print "CRITICAL - nao consegui capturar valores"
  print e
  sys.exit(2)
if status.count('CRITICAL'):
  print "".join(status)
  sys.exit(2)
#print status
data =  "\n".join(status.split(':::'))

#try:
  #inicio = data.index('Last Ref')+9
  #fim = data.index('GLOBAL STATS')
#except Exception,e:
  #print "CRITICAL - formato lido errado do host"
  #print e
  #sys.exit(1)

print data
sys.exit(0)
#try:
  #names_temp=open(loginlog,'r').read().rstrip().split(',')
#except:
  #names_temp=[]
  #pass

#nomes_final=[]
#for i in data[inicio:fim].rstrip().split('\n'):
  #if not i.count('Centreon') and not i.count('UNDEF'):
    #nn=string.lower(i.split(',')[1].split('@')[0].split('_')[0].split('-')[0])
    #nomes_final.append(nn+'=1')
#for i in names_temp:
  #if not ",".join(nomes_final).replace('=1','').split(',').count(i):
    #nomes_final.append(i+'=0')#else:

#open(loginlog,'w').write(",".join(nomes_final).replace('=0','').replace('=1',''))
    
#data = data.replace('OpenVPN CLIENT LIST','OpenVPN Logados:%s' % ",".join(nomes_final))
#print "%s|%s" % (data," ".join(nomes_final))


  
