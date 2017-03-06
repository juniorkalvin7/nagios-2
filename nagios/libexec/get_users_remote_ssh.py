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
import commands,sys
args = sys.argv[1:]

username=args[0]
ip=args[1]

last =commands.getoutput('ssh %s@%s last' % (username,ip)).split('\n')
filelog='/var/lib/centreon/centplugins/ssh_users_%s.log' % ip
logados=[]
rootips=[]
logadosuniq=[]
for i in last:
  if i.count('logged') and not i.count('root'):
    logados.append(i.split()[0])
  if i.count('logged') and i.count('root'):
    logados.append(i.split()[0])
    rotip=i.split()[2]
    if rootips.count(rotip)==0:
      rootips.append(rotip)
try:
  logadosarquivo=open(filelog,'r').read().split('\n')
except:
  open(filelog,'w')
  sys.exit(1)
for i in logados:
  if logadosuniq.count(i)==0:
    logadosuniq.append(i)
    if logadosarquivo.count(i)==0:
      open(filelog,'a').write(i+'\n')
    
logadoszerado=[]
for i in logadosarquivo:
  if logadosuniq.count(i)==0 and len(i)>2:
    
    logadoszerado.append('%s=0 '% i)

listafinal=[]
x=1
for i in logadosuniq:
  listafinal.append('%s=%d.%d' % (i,logados.count(i),x))
  x+=1
if logadosuniq.count('root'):
  print 'CRITICAL ROOT - Usuarios no sistema: %s RootIP:%s|%s %s' % (','.join(logadosuniq),','.join(rootips),' '.join(listafinal),''.join(logadoszerado))
  sys.exit(2)
else:
  print 'Usuarios no sistema: %s|%s %s' % (','.join(logadosuniq),' '.join(listafinal),''.join(logadoszerado))
  sys.exit(0)
    
