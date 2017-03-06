#!/usr/bin/env python
# -*- coding: utf-8 -*-
import string 
import sys
import re

#caminho antigo
#logfile='/etc/openvpn/servers/canopus/logs/openvpn-status.log'

# caminho novo
# alterado por Raul Barros 11/04/2013
# link simbolico
logfile= '/var/log/check/openvpn-status.log'

loginlog='/var/log/openvpn-users.log'


try:
  data = open(logfile,'r').read()
  #print len(data)
except:
  print 'CRITICAL - erro ao ler arquivo'
  sys.exit(1)

try:
  inicio = data.index('Last Ref')+9
  #print inicio
  fim = data.index('GLOBAL STATS')
  #print fim
except Exception,e:
  print "CRITICAL - formato de arquivo errado"
  print e
  sys.exit(1)

try:
  names_temp=open(loginlog,'r').read().rstrip().split(',')
  #print names_temp
except:
  names_temp=[]
  pass

nomes_final=[]
user_conectados_prov = []
user_conectados=[]
pf=0
data_final=[]

#print data[inicio:fim].rstrip().split('\n')

for i in data[inicio:fim].rstrip().split('\n'):
  if not i.count('Centreon') and not i.count('UNDEF'):
    
 #   print 'i %s'%i 
    try:
      #Versao antiga Gemayel
      #nn=i.split(',')[1].split('@')[0]
      
      #Alterado por Raul Barros 11/04/2013
      #print i.split(',')[1].split('@')[0] +'('+(i.split(',')[2].split('@')[0]).split(':')[0] +')' 
      nn = i.split(',')[1].split('@')[0] +'('+(i.split(',')[2].split('@')[0]).split(':')[0] +')'
      ####################

      nomes_final.append(nn+'=1.%d' % pf)
      if nn not in user_conectados_prov:
          user_conectados_prov.append(nn)
          user_conectados.append(nn+'=1.%d' % pf)
	  pf+=1
      data_final.append(i)
    except:
      nn =0 
for i in names_temp:
  if not ",".join(nomes_final)\
     .replace('=1.0','')\
     .replace('=1.1','')\
     .replace('=1.2','')\
     .replace('=1.3','')\
     .replace('=1.4','')\
     .replace('=1.5','')\
     .replace('=1.6','')\
     .replace('=1.7','')\
     .replace('=1.8','')\
     .replace('=1.9','')\
     .replace('=1.10','')\
     .replace('=1.11','').split(',').count(i):
    if i not in nomes_final:
      nomes_final.append(i+'=0')#else:

names_temp=[]
for i in nomes_final:
  if i.count('=1'):
    a = i.split('=')[0]
    if a not in names_temp:
        names_temp.append(i.split('=')[0])
       
open(loginlog,'w').write(",".join(nomes_final).replace('=0','')\
                         .replace('=1.0','')\
                         .replace('=1.1','')\
                         .replace('=1.2','')\
                         .replace('=1.3','')\
                         .replace('=1.4','')\
                         .replace('=1.5','')\
                         .replace('=1.6','')\
                         .replace('=1.7','')\
                         .replace('=1.8','')\
                         .replace('=1.9','')\
                         .replace('=1.10','')\
                         .replace('=1.11',''))

if len(names_temp) == 0:
  data = data.replace('OpenVPN CLIENT LIST','OpenVPN Logados: Nenhum')
  print data[0:23]
else:
  data1 = 'OpenVPN Logados:%s' % (",".join(names_temp))
  data2 = ':%s' % ("\n".join(data_final))
 # print 'else ' + data1
#  print data1
  user_conectados_final = []
  for j in user_conectados:
    try:
      nome = j.split('(')[0]
      numeroAcesso = str(j.split(')')[1])
      string=nome +numeroAcesso
      user_conectados_final.append(nome+numeroAcesso)	  
    except:
      string = ''
  df = "%s|%s %s %s" % (data1, " ".join(user_conectados_final),"\n", data2 )
 
  print df.split(':')[0]+df.split(':')[1]


sys.exit(0)

