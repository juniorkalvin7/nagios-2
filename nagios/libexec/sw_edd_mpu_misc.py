#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
  (0) OK
  (1) WARNING
  (2) CRITICAL
  (3)UNKNOWN
"""
import sys,commands
args = sys.argv[1:]
if __name__ == "__main__":
  args = sys.argv[1:]
  if len(args)<3:
    print "Centreon Plugin\nMisc Info Switch EDD,MPU por GemayelLira"
    print 'Opcoes:'
    print 'users -usuarios logados'
    print 'temp  -temperatura'
    print 'fonte  -Fonte'
    print 'cooler  -Coolers'
    print 'mpumode -Modo Mpu'
    print 'eaps - num ex:eaps1'    
    print "Argumentos:\npython ./%s IP community opcao" % sys.argv[0]
    sys.exit(1)
  else:
    ip=args[0]
    community=args[1]
    opcao=args[2]


    
if opcao=='users':
  mib='.1.3.6.1.4.1.3709.3.5.201.1.19.6.3.0'    
    
  try:
    result=(commands.getoutput("/usr/bin/snmpwalk -t 100000 -v 1 -c %s %s %s" % (community,str(ip),mib))).split(" ")[3]
  except Exception,e:
    print "CRITICAL - nao consegui capturar valores"
    print e
    sys.exit(2)
  usr_table={16:'localUse0',
             17:'localUse1',
             18:'localUse2',
             19:'localUse3',
             20:'localUse4',
             21:'localUse5',
             22:'localUse6',
             23:'localUse7'}
  try:
    if int(result) == 0:
      print 'OK - Nenhum Usuario logado no switch|ok=1'
    else:
      print 'CRITICAL - Usuario logado no switch %s|ok=0 %s=1' % (usr_table[int(result)],usr_table[int(result)])
      print 'Res:',result
      #sys.exit(1)
  except Exception,e:
    print 'CRITICAL - Valor capturado invalido|ok=0'
    print e
    sys.exit(1)
elif opcao=='temp':
  mib='.1.3.6.1.4.1.3709.3.5.201.1.1.2.1.12.1'    
    
  try:
    result=(commands.getoutput("/usr/bin/snmpwalk -t 100000 -v 1 -c %s %s %s" % (community,str(ip),mib))).split(" ")[3]
  except Exception,e:
    print "CRITICAL - nao consegui capturar valores"
    print e
    sys.exit(2)
  try:
    print 'OK - Temperatura %s|ok=1 temp=%s' % (result,result)
      #print 'CRITICAL - Usuario logado no switch %s|ok=0 %s=1' % (usr_table[int(result)],usr_table[int(result)])
      #print 'Res:',result
      #sys.exit(1)
  except Exception,e:
    print 'CRITICAL - Valor capturado invalido|ok=0'
    print e
    sys.exit(1)
elif opcao=='fonte':
  mib='.1.3.6.1.4.1.3709.3.5.201.1.1.4.1.3'    
  st=[]  
  try:
    result=(commands.getoutput("/usr/bin/snmpwalk -t 100000 -v 1 -c %s %s %s" % (community,str(ip),mib))).split('\n')
    num=0
    for x in result:
      st.append(int(result[num].split('INTEGER: ')[1]))
      num+=1
      
  except Exception,e:
    print "CRITICAL - nao consegui capturar valores"
    print e
    sys.exit(2)

  power_table={1:'Inoperante',
               2:'Operacional',
               3:'Sem Alimentacao'}
  sinal=0
  for x in st:
    if x==1:sinal=2
    elif x==3:sinal=2
  
  
  if sinal==0:
    print 'OK - Fonte Celulas %d, Status Operacional |ok=1' % (len(result))
  else:
    srtf=[]
    for x in st:
      srtf.append(power_table[x])
    print 'CRITICAL - Fonte Celulas %d, Status %s|ok=0' % (len(result),','.join(srtf))
    sys.exit(2)

elif opcao=='cooler':
  mib='.1.3.6.1.4.1.3709.3.5.201.1.1.5.1.3.1'    
  st=[]  
  try:
    result=(commands.getoutput("/usr/bin/snmpwalk -t 100000 -v 1 -c %s %s %s" % (community,str(ip),mib))).split('\n')
    num=0
    for x in result:
      st.append(int(result[num].split('INTEGER: ')[1]))
      num+=1
      
  except Exception,e:
    print "CRITICAL - nao consegui capturar valores"
    print e
    sys.exit(2)

  sinal=0
  for x in st:
    if x==1:sinal=2
  
  
  if sinal==0:
    print 'OK - Coolers %d |ok=1' % (len(result))
  else:
    #srtf=[]
    #for x in st:
      #srtf.append(power_table[x])
    print 'CRITICAL - Cooler Down|ok=0' % (len(result))
    sys.exit(2)
elif opcao=='mpumode':
  mib='.1.3.6.1.4.1.3709.3.5.201.1.1.14.1.3'    
  st=[]  
  try:
    result=(commands.getoutput("/usr/bin/snmpwalk -t 100000 -v 1 -c %s %s %s" % (community,str(ip),mib))).split('\n')
    num=0
    for x in result:
      st.append((result[num].split('INTEGER: ')[1]))
      num+=1
      
  except Exception,e:
    print "CRITICAL - nao consegui capturar valores"
    print e
    sys.exit(2)

  
  if int(st[0])==1:#modo de operacao diz q o primeiro sempre he 1 para esta ok
    print 'OK - Modo de Operacao MPU OK 1,2|ok=1'
  else:
    print 'CRITICAL - Modo de operacao MPU %s|ok=0' % (','.join(st))
    sys.exit(2)
elif 'eaps' in opcao:
  try:
    num=int(opcao.replace('eaps',''))-1
  except:
    print 'CRITICAL - ERRO ao ler o valor numerico do eaps'
    sys.exit(2)

  mib='.1.3.6.1.4.1.3709.3.5.201.1.24.1.1.4.%d'%num
  #st=[] 
  statustable={0:'idle',
               1:'complete',
               2:'failed',
               3:'linksup ',
               4:'linkdown',
               5:'preforwarding',
               6:'init'}
  try:
    result=int((commands.getoutput("/usr/bin/snmpwalk -t 100000 -v 1 -c %s %s %s" % (community,str(ip),mib))).split('INTEGER: ')[1])
      
  except Exception,e:
    print "CRITICAL - nao consegui capturar valor via snmp"
    print e
    sys.exit(2)

  #print result
  if result == 1 or result==3:
    print 'OK - Eaps %d status %s %s|status=%d' % (num+1,result,statustable[result],result)
  else:
    print 'CRITICAL - Eaps %d status %s %s|status=%d' % (num+1,result,statustable[result],result)
    sys.exit(2)

  #if int(st[0])==1 or int(st[0]):#modo de operacao diz q o primeiro sempre he 1 para esta ok
    #print 'OK - Modo de Operacao MPU OK 1,2|ok=1'
  #else:
    #print 'CRITICAL - Modo de operacao MPU %s|ok=0' % (','.join(st))
    #sys.exit(2)
        
else:
  print 'CRITICAL - Opcao inserida invalida'
  sys.exit(1)
