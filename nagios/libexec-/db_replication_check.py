#!/usr/bin/env python
# -*- coding: utf-8 -*-

import MySQLdb
import re
import sys
import datetime

'''notas
cmp1 50.56.99.4
cmp2 184.106.81.76

GRANT ALL PRIVILEGES ON *.* TO mmm_monitor2@'10.181.170.209' IDENTIFIED BY 'l4bs3curity' WITH GRANT OPTION;flush privileges;
GRANT ALL PRIVILEGES ON *.* TO mmm_monitor2@'10.181.161.195' IDENTIFIED BY 'l4bs3curity' WITH GRANT OPTION;flush privileges;

'''
#id1=['cmp.cloud.1','50.56.99.4','mmm_monitor2','l4bs3curity']
#id2=['cmp.cloud.2','184.106.81.76','mmm_monitor2','l4bs3curity']
id1=['CMP.CLOUD.1','10.181.170.209','mmm_monitor2','l4bs3curity']
id2=['CMP.CLOUD.2','10.181.161.195','mmm_monitor2','l4bs3curity']
corpo=''
status,ok,warn,crit=(0,0,0,0)

try:
  conn1 = MySQLdb.connect(host = id1[1],user = id1[2],passwd =id1[3],db = "mysql")
  conn2 = MySQLdb.connect(host = id2[1],user = id2[2],passwd =id2[3],db = "mysql")
except Exception,e:
  print 'Erro grave nao consigo em connectar no banco de dados',e
  print 'CHAME GEMAYEL'
  sys.exit(1)
  
cursor1 = conn1.cursor()
cursor1.execute("show slave status")
resultado1_1=cursor1.fetchall()[0]
cursor1.execute("show master status")
resultado1_2=cursor1.fetchall()[0]
#cursor1.close()


cursor2 = conn2.cursor()
cursor2.execute("show slave status")
resultado2_1=cursor2.fetchall()[0]
cursor2.execute("show master status")
resultado2_2=cursor2.fetchall()[0]
#cursor2.close()
 
def check1():
  global corpo,status,ok,warn,crit,cursor1,conn1

  corpo+= 'Verificacao %s\n' % id1[0]
  if len(resultado1_1)==40:
    corpo+= 'OK - Resultado Select 1\n'
    ok+=1
  else:
    corpo+= 'CRITICAL - Resultado Select 1 \n'
    #sys.exit(1)
    crit+=1
    status=2

    return
  
  if len(resultado1_2)==4:
    corpo+= 'OK - Resultado Select 2\n'
    ok+=1
  else:
    corpo+= 'CRITICAL - Resultado Select 2 \n'
    crit+=1
    #sys.exit(1)
    status=2

    return
  
  if resultado2_2[0] ==resultado1_1[5] :
    corpo+= 'OK - Master_log\n'
    ok+=1
  else:
    corpo+= 'CRITICAL - Master_log %s , %s\n' % (resultado1_1[5],resultado2_2[0])
    status=2
    crit+=1

  if resultado2_2[1] == resultado1_1[6]:
    corpo+= 'OK - Position_Master_Log OK\n'
    ok+=1
  else:
    corpo+= 'WARNING - Position_Master_Log %s , %s\n' % (resultado1_1[6],resultado2_2[1])
    #status=2
    warn+=1
    
  if 'Waiting for master to send event' in resultado1_1[0]:
    corpo+= 'OK - Slave_IO_State Aguardando evento...\n'
    ok+=1
  else:
    corpo+= 'WARNING - Slave_IO_State %s\n' % resultado1_1[0]
    status=1
    warn+=1
    
  if 'Yes' in resultado1_1[10]:
    corpo+= 'OK - Slave_IO_Running Executando\n'
    ok+=1
  else:
    corpo+= 'WARNING - Slave_IO_Running DOWN\n'
    status=1
    warn+=1

  if 'Yes' in resultado1_1[11]:
    corpo+= 'OK - Slave_SQL_Running Executando\n'
    ok+=1
  else:
    corpo+= 'WARNING - Slave_SQL_Running DOWN\n'
    status=1
    warn+=1
    
  if 'Error' in resultado1_1[19]:
    corpo+= 'OK - CRITICAL - Last_Error, %s \n'%resultado1_1[19]
    status=2
    crit+=1
  else:
    corpo+= 'OK - Last_Error None\n'
    ok+=1
    
  if 'Error' in resultado1_1[37]:
    corpo+= 'CRITICAL - Last_SQL_Error, %s\n'%resultado1_1[37]
    status=2
    crit+=1
    if 'Cannot add or update a child row' in resultado1_1[37]:
      #corpo+="Possivel solucao:stop slave;CHANGE MASTER TO MASTER_LOG_FILE='%s', MASTER_LOG_POS=%s;start slave;" % (resultado2_2[0],resultado2_2[1])
      corpo+="Tentando corrigir..." 
      cm = "stop slave;CHANGE MASTER TO MASTER_LOG_FILE='%s', MASTER_LOG_POS=%s;start slave;"% (resultado2_2[0],resultado2_2[1])
      open('/var/log/db_replication_fix.log','a').write("%s Tentando correcao no banco cmp2 MASTER_LOG_FILE=%s MASTER_LOG_POS=%s\n" % (datetime.datetime.now(),resultado2_2[0],resultado2_2[1]))
      cursor1.execute(cm)
      conn1.commit()

  else:
    corpo+= 'OK - Last_SQL_Error None\n'
    ok+=1
    
def check2():
  global corpo,status,ok,warn,crit,cursor2,conn2

  corpo+= 'Verificacao %s \n'%id2[0]
  if len(resultado2_1)==40:
    corpo+= 'OK - Resultado Select 1\n'
    ok+=1
  else:
    corpo+= 'CRITICAL - Resultado Select 1 \n'
    status=2
    crit+=1
    #sys.exit(1)
    return
  if len(resultado2_2)==4:
    corpo+= 'OK - Resultado Select 2\n'
    ok+=1
  else:
    corpo+= 'CRITICAL - Resultado Select 2 \n'
    status=2
    crit+=1
    return
    #sys.exit(1)
  
  if resultado1_2[0] ==resultado2_1[5] :
    corpo+= 'OK - Master_log\n'
    ok+=1
  else:
    corpo+= 'CRITICAL - Master_log %s , %s\n'%(resultado2_1[5],resultado1_2[0])
    status=2
    crit+=1

  if resultado1_2[1] == resultado2_1[6]:
    corpo+= 'OK - Position_Master_Log\n'
    ok+=1
  else:
    corpo+= 'WARNING - Position_Master_Log %s , %s\n' % (resultado2_1[6],resultado1_2[1])
    #status=2
    warn+=1
  if 'Waiting for master to send event' in resultado2_1[0]:
    corpo+= 'OK - Slave_IO_State Aguardando evento...\n'
    ok+=1
  else:
    corpo+= 'WARNING - Slave_IO_State %s\n' % resultado2_1[0]
    status=1
    warn+=1

  if 'Yes' in resultado2_1[10]:
    corpo+= 'OK - Slave_IO_Running Executando\n'
    ok+=1
  else:
    corpo+= 'WARNING - Slave_IO_Running DOWN\n'
    status=1
    warn+=1

  if 'Yes' in resultado2_1[11]:
    corpo+= 'OK - Slave_SQL_Running Executando\n'
    ok+=1
  else:
    corpo+= 'WARNING - Slave_SQL_Running DOWN\n'
    status=1
    warn+=1

  if 'Error' in resultado2_1[19]:
    corpo+= 'CRITICAL - Last_Error, %s\n' % resultado2_1[19]
    status=2 
    crit+=1
  else:
    corpo+= 'OK - Last_Error None\n'
    ok+=1
  if 'Error' in resultado2_1[37]:
    corpo+= 'CRITICAL - Last_SQL_Error, %s\n' % resultado2_1[37]
    status=2
    crit+=1
    if 'Cannot add or update a child row' in resultado2_1[37]:
      corpo+="Tentando corrigir..." 
      cm = "stop slave;CHANGE MASTER TO MASTER_LOG_FILE='%s', MASTER_LOG_POS=%s;start slave;"% (resultado1_2[0],resultado1_2[1])
      open('/var/log/db_replication_fix.log','a').write("%s Tentando correcao no banco cmp2 MASTER_LOG_FILE=%s MASTER_LOG_POS=%s\n" % (datetime.datetime.now(),resultado1_2[0],resultado1_2[1]))
      cursor2.execute(cm)
      conn2.commit()
  else:
    corpo+= 'OK - Last_SQL_Error None\n'
    ok+=1

check1()
check2()

cursor1.close()
cursor2.close()
if status==0:
  print 'Replication Status ok=%d warn=%d crit=%d|ok=%d warn=%d crit=%d\n%s' % (ok,warn,crit,ok,warn,crit,corpo)
  #print corpo
  sys.exit(0)
else:
  print 'Replication Status ok=%d warn=%d crit=%d|ok=%d warn=%d crit=%d\n%s' % (ok,warn,crit,ok,warn,crit,corpo)
  #print corpo
  #print '<pre>'+corpo+'</pre>'
  sys.exit(status)


#print 'Master_log',resultado1_2[0]
#print 'Position_Master_Log',resultado1_2[1]
#print 'Slave_IO_State:',resultado1_1[0]
#print 'Master_Log_File:',resultado1_1[5]
#print 'Read_Master_Log_Pos:',resultado1_1[6]
#print 'Slave_IO_Running:',resultado1_1[10]
#print 'Slave_SQL_Running:',resultado1_1[11]
#print 'Last_Error:',resultado1_1[19]
#print 'Last_SQL_Error:',resultado1_1[37]



