#!/usr/bin/python
# -*- coding: utf-8 -*-

import MySQLdb
import re
import sys
import time,datetime
"""
arquivo com credencial
/etc/default/mysql
host=localhost
port=3306
user=root
password=labsecur1t1
"""
t = datetime.datetime.now()
tempo1=time.mktime(t.timetuple())+(t.microsecond/1000000.)

args = sys.argv[1:]
if len(args) != 2:
  print "Erro argumentos invalidos"
  print "Uso:"
  print sys.argv[0]+' /etc/default/mysql all,databasename'
  print """exemplo do arquivo de credencial:
host=localhost
port=3306
user=root
password=senha
  """
  sys.exit(1)
  

arquivo,tipo=args
data=open(arquivo,'r').read()
if 'mysql_host' in data:
  host=re.findall('mysql_host = "(.+?)"',data)[0]
  user=re.findall('mysql_user = "(.+?)"',data)[0]
  password=re.findall('mysql_passwd = "(.+?)"',data)[0]
else:
  host=re.findall('host=(.+?)\n',data)[0]
  user=re.findall('user=(.+?)\n',data)[0]
  password=re.findall('password=(.+?)\n',data)[0]

#print host,user,password
#sys.exit(1)

if tipo=='all':
  sql='SELECT table_schema, SUM( data_length + index_length) / 1024 / 1024 "size" FROM information_schema.TABLES GROUP BY table_schema;'
else:
  sql="""SELECT table_name AS "Tables", 
  round(((data_length + index_length) / 1024 / 1024), 2) "Size in MB" 
  FROM information_schema.TABLES 
  WHERE table_schema = '"""+tipo+"';"
  
port=3306
conn = MySQLdb.connect (
                      host = host,
                      user = user,
                      passwd = password,
                      port=port)
cursor = conn.cursor()
cursor.execute(sql)
res=[]
for i in cursor.fetchall():
  #res[i[0]]=float(i[1])
  res.append("%s=%sMB"%(i[0],float(i[1])))
  #print i
conn.close()
if len(res)==0:
  print "CRITICAL - Banco nao retorou resultado"
  sys.exit(2)

t = datetime.datetime.now()
tempo2=time.mktime(t.timetuple())+(t.microsecond/1000000.)
diferenca=tempo2-tempo1 
  
if tipo=='all':
  print "Databases %s timer=%0.3fms|%s timer=%0.3fms"%(len(res),diferenca," ".join(res),diferenca)
else:
  print "Tabelas do banco %s quantidade %s timer=%0.3fms|%s timer=%0.3fms"%(tipo,len(res),diferenca," ".join(res),diferenca)

  
