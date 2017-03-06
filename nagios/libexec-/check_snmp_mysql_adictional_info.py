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

#mysqllogbanco='/tmp/mysqllogbanco.log'

if len(args)<2:
  print "Centreon Plugin\nMysql Adictional Info por GemayelLira"
  print "Argumentos:host community tipo(user,banco)"
  print "Ex.\n%s 192.168.3.161 u3fr0I9b5 user" % sys.argv[0] 
  sys.exit(1)
else:
  host=args[0]
  community=args[1]
  mysqllogusers='/var/lib/centreon/centplugins/'+host.replace('.','_')+'_mysqllogusers.log'
  mysqllogbanco='/var/lib/centreon/centplugins/'+host.replace('.','_')+'_mysqllogbanco.log'
  
  if args[2] == 'user':mib='.1.3.6.1.4.1.2022.26.3.1.1.9.112.111.114.116.99.104.101.99.107'
  elif args[2] == 'banco':mib='.1.3.6.1.4.1.2022.27.3.1.1.9.112.111.114.116.99.104.101.99.107'
try:
  status=(commands.getoutput("/usr/bin/snmpwalk -t 100000 -v 1 -c %s %s %s" % (community,str(host),mib))).split("\"")[1]
except Exception,e:
  print "CRITICAL - nao consegui capturar valores"
  print e
  sys.exit(2)

  
if args[2]=='user':
  try:
    totalusers=open(mysqllogusers).read().rstrip().split('\n')
  except:
    open(mysqllogusers,'w').write('')
    sys.exit(1)
  if status.count('CRITICAL'):
    print "".join(status)
    sys.exit(2)
  elif status.count('root'):
    msg1=status.split('|')[0]
    users=status.split('|')[1]
    usersc=users
    for i in totalusers:
      if users.count(i)==0:
        usersc+=' %s=0' % i
    uu=users.split(' ')
    for i in uu:
      if totalusers.count(i.split('=')[0]) == 0:
        open(mysqllogusers,'a').write(i.split('=')[0]+'\n')
    print 'CRITICAL - Acesso root - %s|%s' % (msg1,usersc)
    sys.exit(2)
  
  msg1=status.split('|')[0]
  try:
    users=status.split('|')[1]
  except:
    print '%s' % (msg1)  
    sys.exit(0)
  usersc=users
  for i in totalusers:
    if users.count(i)==0:
      usersc+=' %s=0' % i
  uu=users.split(' ')
  for i in uu:
    if totalusers.count(i.split('=')[0]) == 0:
      open(mysqllogusers,'a').write(i.split('=')[0]+'\n')
  print '%s|%s' % (msg1,usersc)  
  sys.exit(0)
elif args[2] == 'banco':
  try:
    totalusers=open(mysqllogbanco).read().rstrip().split('\n')
  except:
    open(mysqllogbanco,'w').write('')
    sys.exit(1)
  if status.count('CRITICAL'):
    print "".join(status)
    sys.exit(2)
  elif status.count('root'):
    msg1=status.split('|')[0]
    users=status.split('|')[1]
    usersc=users
    for i in totalusers:
      if users.count(i)==0:
        usersc+=' %s=0' % i
    uu=users.split(' ')
    for i in uu:
      if totalusers.count(i.split('=')[0]) == 0:
        open(mysqllogusers,'a').write(i.split('=')[0]+'\n')
    print 'CRITICAL - Acesso root - %s|%s' % (msg1,usersc)
    sys.exit(2)
  
  msg1=status.split('|')[0]
  users=status.split('|')[1]
  usersc=users
  for i in totalusers:
    if users.count(i)==0:
      usersc+=' %s=0' % i
  uu=users.split(' ')
  for i in uu:
    if totalusers.count(i.split('=')[0]) == 0:
      open(mysqllogbanco,'a').write(i.split('=')[0]+'\n')
  print '%s|%s' % (msg1,usersc)  
  sys.exit(0)
else:
  print 'opcao invalida!'

