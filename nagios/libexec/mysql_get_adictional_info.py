#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
sys.exit(1)
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
MIB:
exec .1.3.6.1.4.1.2022.26 portcheck /usr/bin/python /usr/local/nagios/libexec/mysql_get_adictional_info.py /etc/default/mysql user
exec .1.3.6.1.4.1.2022.27 portcheck /usr/bin/python /usr/local/nagios/libexec/mysql_get_adictional_info.py /etc/default/mysql banco


"""
import MySQLdb
import re
import sys

#dependency MySQL-python.i386 centos

def getbd():
  lista=[]
  one=[]
  for i in cursor.fetchall():
    try:
      if i[7].count('show full processlist')==1:
        continue
    except:pass
    if i[3] == None:adict='None'
    else:adict=i[3]
    #if i[3] == None:i[3]='None'
    lista.append('db_'+adict)
    if one.count('db_'+adict)==0:one.append('db_'+adict)
  one1=[]
  sesqt=0
  xx=1
  for i in one:
    one1.append("%s=%d.%d" % (i,lista.count(i),xx))
    sesqt+=lista.count(i)
    xx+=1
  return 'MySQL Base de dados em acesso %d sessoes %d|%s' % (len(one),sesqt,' '.join(one1))


def getusers():
  users=[]
  usersip=[]
  for i in cursor.fetchall():
    try:
      if i[7].count('show full processlist')==1:
        continue
    except:pass
    if users.count('%s=1' % i[1]) ==0 \
       and  users.count('%s=2' % i[1]) ==0\
       and  users.count('%s=3' % i[1]) ==0\
       and  users.count('%s=4' % i[1]) ==0\
       and  users.count('%s=5' % i[1]) ==0\
       and  users.count('%s=6' % i[1]) ==0\
       and  users.count('%s=7' % i[1]) ==0\
       and  users.count('%s=8' % i[1]) ==0\
       and  users.count('%s=9' % i[1]) ==0\
       and  users.count('%s=10' % i[1]) ==0\
       and  users.count('%s=11' % i[1]) ==0\
       and  users.count('%s=12' % i[1]) ==0\
       and  users.count('%s=13' % i[1]) ==0\
       and  users.count('%s=14' % i[1]) ==0\
       and  users.count('%s=15' % i[1]) ==0\
       and  users.count('%s=16' % i[1]) ==0\
       and  users.count('%s=17' % i[1]) ==0\
       and  users.count('%s=18' % i[1]) ==0\
       and  users.count('%s=19' % i[1]) ==0\
       and  users.count('%s=20' % i[1]) ==0\
       and  users.count('%s=21' % i[1]) ==0\
       and  users.count('%s=22' % i[1]) ==0\
       and  users.count('%s=23' % i[1]) ==0\
       and  users.count('%s=24' % i[1]) ==0\
       and  users.count('%s=25' % i[1]) ==0\
       and  users.count('%s=26' % i[1]) ==0\
       and  users.count('%s=27' % i[1]) ==0\
       and  users.count('%s=28' % i[1]) ==0\
       and  users.count('%s=29' % i[1]) ==0\
       and  users.count('%s=30' % i[1]) ==0\
       and  users.count('%s=31' % i[1]) ==0\
       and  users.count('%s=32' % i[1]) ==0\
       and  users.count('%s=33' % i[1]) ==0\
       and  users.count('%s=34' % i[1]) ==0\
       and  users.count('%s=35' % i[1]) ==0\
       and  users.count('%s=36' % i[1]) ==0\
       and  users.count('%s=37' % i[1]) ==0\
       and  users.count('%s=38' % i[1]) ==0\
       and  users.count('%s=39' % i[1]) ==0\
       and  users.count('%s=40' % i[1]) ==0\
       and  users.count('%s=41' % i[1]) ==0\
       and  users.count('%s=42' % i[1]) ==0\
       and  users.count('%s=43' % i[1]) ==0\
       and  users.count('%s=44' % i[1]) ==0\
       and  users.count('%s=45' % i[1]) ==0\
       and  users.count('%s=46' % i[1]) ==0\
       and  users.count('%s=47' % i[1]) ==0\
       and  users.count('%s=48' % i[1]) ==0\
       and  users.count('%s=49' % i[1]) ==0\
       and  users.count('%s=50' % i[1]) ==0\
       and  users.count('%s=51' % i[1]) ==0\
       and  users.count('%s=52' % i[1]) ==0\
       and  users.count('%s=53' % i[1]) ==0\
       and  users.count('%s=54' % i[1]) ==0\
       and  users.count('%s=55' % i[1]) ==0\
       and  users.count('%s=56' % i[1]) ==0\
       and  users.count('%s=57' % i[1]) ==0\
       and  users.count('%s=58' % i[1]) ==0\
       and  users.count('%s=59' % i[1]) ==0:
      users.append('%s=1'% i[1])
      usersip.append('%s=%s' % (i[1],i[2].split(':')[0]))
    else:
      x=0
      #users.sort()
      for user in users:
        if user.count('%s' % i[1].split('=')[0]):
          qt=user.split('=')[1]
          usr=user.split('=')[0]
          users.pop(x)
          users.append('%s=%d' % (usr,int(qt)+1))
          break
        x+=1 
  usersf=[]
  x=0
  xx=0
  for i in range(0,len(users)):
    #if users[i].count('=%d' % x):
    usersf.append('%s.%d' % (users[i],x))
    
    xx+=int(users[i].split('=')[1].split('.')[0])
    x+=1
  if len(usersf) == 0 and xx == 0:
    return 'MySQL Usuarios conectados 0 sessoes 0'
  else:
    return 'MySQL Usuarios conectados %d sessoes %d, %s|%s' % (len(usersf),xx,' ,'.join(usersip),' '.join(usersf))

def uso():
  print "Centreon Plugin\nMysql Adictional info Agent para Centreon por GemayelLira"
  print "Argumentos:mysql-agentdb-file tipo (user,banco)"
  print "Ex.\n%s /etc/default/mysql user" % sys.argv[0] 
  print 'CRITICAL'
  sys.exit(1)
  
args = sys.argv[1:]

if len(args)<2:
  uso()
else:
  #print args
  sqlfile=args[0]
  tipo=args[1]
  
data=open(sqlfile).read()
host=re.findall("host=(.+?)\n",data)[0]
user=re.findall("user=(.+?)\n",data)[0]
passw=re.findall("password=(.+?)\n",data)[0]

try:
  conn = MySQLdb.connect (
                        host = host,
                        user = user,
                        passwd = passw,
                        db = "mysql")
  cursor = conn.cursor ()
  cursor.execute ("show full processlist;")
except:
  print 'CRITICAL - Nao consegui conectar ao banco...'
  sys.exit(1)

if tipo=='user':print getusers()
elif tipo=='banco':print getbd()
else:
  print 'CRITICAL - Opcao invalida!'
  sys.exit(1)
cursor.close()
