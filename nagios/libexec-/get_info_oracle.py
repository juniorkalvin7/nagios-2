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
"""
sys.exit(0) OK
sys.exit(1) WARNING
sys.exit(2) CRITICAL
sys.exit(3)UNKNOWN
"""
import commands,sys,codecs
def any(iterable):
  for item in iterable:
    if item:
      return True
  return False

def uso():
  print "Centreon Plugin\nOracle Agent para Centreon por GemayelLira"
  print "Argumentos:host opcao1 opcao2"
  print 'opcao1'
  print "tablespace,bcache,jobs,users,pools,sga,top"
  print 'opcap2:'
  print 'tablespace:nometablespace'
  print 'pools:shared,large,java'
  print 'sga:bcache,exnoparse,memsort,hitrate,avgnomiss,avgnosleep,cpu'
  print "Ex.\n%s 10.40.1.4 tablespace CWMLITE" % sys.argv[0] 
  #print 
  sys.exit(1)

args = sys.argv[1:]

if args[0].count('help'):
  uso()
else: 
  ip=args[0]
  opcao=args[1]
  try:
    opcao2=args[2]
  except:pass

#last =commands.getoutput('ssh %s@%s last' % (username,ip)).split('\n')
filelog='/var/lib/centreon/centplugins/oracle_ssh_%s.log' % ip
#filelog='data'
#opcao='sga'
#opcao2='avgnosleep'
#data=open(filelog,'r').read()
#data = codecs.open(filelog,'r',"utf-8").read()
data = codecs.open(filelog,'r',"utf-8").read()

infos=data.split('1vini')

if opcao=='tablespace':
  for i in infos[1].split('\n'):
    if i.count(opcao2):
      tbmaximo=i.split()[2]
      extend=i.split()[3]
      tbusado=i.split()[4]
      percent=i.split()[6]
      break
  print 'Oracle - Tablespace %s Extend:%s Utilizado:%s%%|size=%sB tbspaceusado=%sB' % (opcao2,extend,percent,tbmaximo,tbusado)
elif opcao=='bcache':
  #print infos[2].split('\n')
  for i in infos[2].split('\n'):
    if i.count('BEING READ'):
      bcachecur= i.split()[3]
      continue
    elif i.count('READ AND MODIFIED'):
      bcachemod= i.split()[3]
      break
  print 'Oracle - Buffer Cache leitura corrente:%s Lido e modificado:%s|bcachecur=%s bcachemod=%s' % (bcachecur,bcachemod,bcachecur,bcachemod)
elif  opcao=='jobs':
  jobsrunning=infos[3].split('\n')[2].replace('\t','').replace(' ','')
  jobsproblem=infos[4].split('\n')[2].replace('\t','').replace(' ','')
  print 'Oracle - Jobs Running:%s Jobs Problem:%s|jobsrunning=%s jobsproblem=%s' % (jobsrunning,jobsproblem,jobsrunning,jobsproblem)
elif opcao =='users':
  userlogados=infos[5].split('\n')[2].replace('\t','').replace(' ','')
  #print userlogados
  userinativo=infos[6].split('\n')[2].replace('\t','').replace(' ','')
  #print userinativo
  userativo=infos[7].split('\n')[2].replace('\t','').replace(' ','')
  #print userativo
  usermorto=int(userlogados)-(int(userinativo)+int(userativo))
  #print usermorto
  print 'Oracle - Users Logados:%s Inativos:%s Ativos:%s Mortos:%s|userlogados=%s userinativo=%s userativo=%s usermorto=%s' % \
        (userlogados,userinativo,userativo,usermorto,userlogados,userinativo,userativo,usermorto,)
  
elif opcao =='pools':
  if opcao2=='shared':
    size=infos[8].split('\n')[3]
    used=infos[8].split('\n')[8].split()[4]
    print 'Oracle - Shared Pool Tamanho:%sM Usado:%sM|size=%s used=%s' % (int(size)/1024/1024,int(used)/1024/1024,size,used)
  elif opcao2=='large':
    size=infos[9].split('\n')[3]
    used=infos[9].split('\n')[8].split()[4]
    print 'Oracle - Large Pool Tamanho:%sM Usado:%sM|size=%s used=%s' % (int(size)/1024/1024,int(used)/1024/1024,size,used)
  elif opcao2=='java':
    size=infos[10].split('\n')[3]
    used=infos[10].split('\n')[8].split()[4]
    print 'Oracle - Java Pool Tamanho:%sM Usado:%sM|size=%s used=%s' % (int(size)/1024/1024,int(used)/1024/1024,size,used)
elif opcao =='sga':
  if opcao2=='bcache':
    uso=infos[11].split('\n')[2].split()[2]
    print 'Oracle - SGA - Buffer Cache Uso:%s|size=100 sgauso=%s' % (uso,uso)
  elif opcao2=='exnoparse':
    uso=infos[11].split('\n')[3].split()[1]
    print 'Oracle - SGA - Execute/NoParse Uso:%s|size=100 sgauso=%s' % (uso,uso)
  elif opcao2=='memsort':
    uso=infos[11].split('\n')[4].split()[2]
    print 'Oracle - SGA - Memory Sort Uso:%s|size=100 sgauso=%s' % (uso,uso)
  elif opcao2=='hitrate':
    uso=infos[11].split('\n')[5].split()[4]
    print 'Oracle - SGA - SQL Area get hitrate Uso:%s|size=100 sgauso=%s' % (uso,uso)
  elif opcao2=='avgnomiss':
    uso=infos[11].split('\n')[6].split()[5]
    print 'Oracle - SGA - Avg Latch Hit (No Miss) Uso:%s|size=100 sgauso=%s' % (uso,uso)
  elif opcao2=='avgnosleep':
    uso=infos[11].split('\n')[7].split()[5]
    print 'Oracle - SGA - Avg Latch Hit (No Sleep) Uso:%s|size=100 sgauso=%s' % (uso,uso)
elif opcao=='top':
  if opcao2=='cpu':
    ##print 'aa'
    ##print infos[12]
    loginlog='/var/lib/centreon/centplugins/oracle_ssh_%s_top_cpu.log' % ip
    logins=infos[12].split('\n')[2:12]
    logins=[x.lower() for x in logins]

    try:
      names_temp=open(loginlog,'r').read().rstrip().split(',')
    except:
      open(loginlog,'w')
      names_temp=[]
      
    names0=[]
    namesfinal=[]
    for i in names_temp:
      if not any(name == i for name in logins):
        names0.append(i)
    #for i in 
    count=0
    for x in logins:
      namesfinal.append('%s=1.%d' % (x,count))
      count+=1
    for x in names0:
      namesfinal.append('%s=0' % (x))
    print 'Oracle - Top10 CPU Users|%s' % (' '.join(namesfinal))
    data=[]
    for x in namesfinal:
      data.append(x.split('=')[0])
    #=' '.join()
    #print data
    open(loginlog,'w').write(','.join(data))
  elif opcao2=='disco':
    loginlog='/var/lib/centreon/centplugins/oracle_ssh_%s_top_disco.log' % ip
    logins=infos[13].split('\n')[2:12]
    #print logins
    logins=[x.lower() for x in logins]

    try:
      names_temp=open(loginlog,'r').read().rstrip().split(',')
    except:
      open(loginlog,'w')
      names_temp=[]
      
    names0=[]
    namesfinal=[]
    for i in names_temp:
      if not any(name == i for name in logins):
        names0.append(i)
    #for i in 
    count=0
    for x in logins:
      namesfinal.append('%s=1.%d' % (x,count))
      count+=1
    for x in names0:
      namesfinal.append('%s=0' % (x))
    print 'Oracle - Top10 Disco Users|%s' % (' '.join(namesfinal))
    data=[]
    for x in namesfinal:
      data.append(x.split('=')[0])
    #=' '.join()
    #print data
    open(loginlog,'w').write(','.join(data))

#print 'fim'

