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
import sys
from socket import *

#def portcheck(host,port):
class Portcheck:
  def __init__(self, host,port):
    self.host = host
    self.port = int(port)
    self.socket = setdefaulttimeout(3)
    self.sd = socket(AF_INET, SOCK_STREAM)
  def run(self):
    try:
      self.sd.connect((self.host, self.port))
      #print "%s:%d OPEN|ok=1" % (self.host, self.port)
      self.sd.close()
      st='OPEN'
    except:
      #print "%s:%d CLOSED|ok=0" % (self.host, self.port)
      st='CLOSED'
      pass
    return st


status=[]
args = sys.argv[1:]
if len(args)<2:
  print "Centreon Plugin\nChecagem Multipla de portas de email por GemayelLira"
  print "Opcoes:fila"
  print "Argumentos:host portas"
  print "Ex.\n%s 127.0.0.1 80 443" % sys.argv[0] 
  #print 
  sys.exit(1)
else:
  host=args[0]
  #print host
  ports=args[1:]
  #print ports
if ' ' in ports[0]:
  ports = ports[0].split()
  
for i in ports:
  ss=Portcheck(host,i).run()
  if i=='10024':i='amavisd'
  elif i=='3310':i='clamd'
  elif i=='22':i='ssh'
  elif i=='2222':i='ssh'
  elif i=='9090':i='stunnel'
  elif i=='1863':i='msnproxy'
  elif i=='1723':i='pptp'
  elif i=='9292':i='vshield'
  elif i=='7071':i='console'
  elif i=='5668':i='ndo2db'
  elif i=='3306':i='mysql'
  elif i=='80':i='http'
  elif i=='995':i='pop3s'
  elif i=='110':i='pop3'
  elif i=='143':i='imap'
  elif i=='25':i='smtp'  
  if ss=='OPEN':
    a='%s=OPEN' % i
  else:
    a='%s=CLOSED' % i
  status.append(a)

tamanho=len(status)
x=0
status2=[]
msg1='MPortCheck '
for i in status:
  if i.count('OPEN'):
    a='p%s=1.%s' % (i.replace('=OPEN',''),x)
    x+=1
  else:
    a='p%s=0' % (i.replace('=CLOSED',''))
    msg1='CRITICAL - MPortCheck '
  status2.append(a)
  #print a
m = '%s- %s %s|%s' % (msg1,host,' '.join(status),' '.join(status2))
print m
if 'CRITICAL' in m:  
  sys.exit(2)
  
  