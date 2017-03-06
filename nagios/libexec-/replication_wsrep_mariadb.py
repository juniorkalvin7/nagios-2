#!/usr/bin/python
# -*- coding: utf-8 -*-

import MySQLdb
import re
import sys
import time,datetime
"""
criando uusario somente leitura
CREATE USER 'monitreplicacao'@'127.0.0.1';
GRANT SELECT ON test.* to monitreplicacao@'localhost' IDENTIFIED BY '2lX1fln19';
GRANT SELECT ON test.* to monitreplicacao@'dbnode1' IDENTIFIED BY '2lX1fln19';
GRANT SELECT ON test.* to monitreplicacao@'dbnode2' IDENTIFIED BY '2lX1fln19';
flush privileges; 
"""
t = datetime.datetime.now()
tempo1=time.mktime(t.timetuple())+(t.microsecond/1000000.)


def verificacoes(res,size,index):
  flag=True
  falha=[]
  if res['wsrep_cluster_state_uuid']!=res['wsrep_local_state_uuid']:flag=False;falha.append('uuids')
#  if res['wsrep_local_state_comment']!='bla':flag=False;falha.append('state')
  if res['wsrep_local_state_comment']!='Synced':flag=False;falha.append('state')
  if res['wsrep_ready']!='ON':flag=False;falha.append('ready')
  if res['wsrep_connected']!='ON':flag=False;falha.append('conexao')
  if res['wsrep_cluster_size']!=size:flag=False;falha.append('size')
  if res['wsrep_local_index']!=index:flag=False;falha.append('index')
  if flag==False:
    return ["CRITICAL - Falha em %s "%" ".join(falha),"ok=0"]
  else:
    return ["OK - Banco sincronizado e replicando","ok=1"]
    
args = sys.argv[1:]
if len(args) != 5:
  print "Erro argumentos invalidos"
  print "Uso:"
  print sys.argv[0]+' host usuario senha size index'
  sys.exit(1)
host,user,password,size,index=args

port=3306
sql="SHOW GLOBAL STATUS WHERE `Variable_name` IN ('wsrep_cert_deps_distance','wsrep_local_index', 'wsrep_ready','wsrep_connected','wsrep_cluster_size','wsrep_local_state_comment','wsrep_local_state_uuid','wsrep_cluster_state_uuid');"
conn = MySQLdb.connect (
                      host = host,
                      user = user,
                      passwd = password,
                      port=port,
                      db = "information_schema")
cursor = conn.cursor()
cursor.execute(sql)
res={}
for i in cursor.fetchall():
  res[i[0]]=i[1]
conn.close()

msg = verificacoes(res,size,index)

t = datetime.datetime.now()
tempo2=time.mktime(t.timetuple())+(t.microsecond/1000000.)
diferenca=tempo2-tempo1

msg= "%s timer=%0.3fms dist=%s|%s timer=%0.3fms dist=%s"%(msg[0],diferenca,res['wsrep_cert_deps_distance'],msg[1],diferenca,res['wsrep_cert_deps_distance'])
print msg
for x in res:
  print x,res[x]
print "%s"%datetime.datetime.now()
if 'CRITICAL' in msg:
  sys.exit(2)



