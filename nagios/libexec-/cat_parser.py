#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys,commands
try:
  host= sys.argv[1:][0]
except:
  print 'nenhum resultado no momento'
  sys.exit(0)
  

#host = 'fw-prod-saude-01_eth0'  
files = commands.getoutput('ls /var/lib/centreon/centplugins/top*%s'% host).split('\n')

  
  
  
file_to_open=files[0]
data=open(file_to_open).read().split('\n')
print data[0]
print """Ultimos 10 Minutos
<table style="border: 1px solid black;">
<tr><td style="border: 1px solid black;">Ip Origem e Porta</td>
<td style="border: 1px solid black;">Bytes Enviados</td>
<td style="border: 1px solid black;">Ip Destino e Porta</td>
<td style="border: 1px solid black;">Bytes Recebidos</td>
</tr>"""
for x in data[1:]:
  if x=='':break
  print """<tr>
  <td style="border: 1px solid black;">"""+x.split()[0]+"""</td>
  <td style="border: 1px solid black;text-align: right;" >"""+x.split()[1]+"""</td>
  <td style="border: 1px solid black;">"""+x.split()[2]+"""</td>
  <td style="border: 1px solid black;text-align: right;" >"""+x.split()[3]+"""</td></tr>"""
print "</table>"

file_to_open=files[1]
data=open(file_to_open).read().split('\n')
#print data[0]
print """<br>Ultimos 60 Minutos
<table style="border: 1px solid black;">
<tr><td style="border: 1px solid black;">Ip Origem e Porta</td>
<td style="border: 1px solid black;">Bytes Enviados</td>
<td style="border: 1px solid black;">Ip Destino e Porta</td>
<td style="border: 1px solid black;">Bytes Recebidos</td>
</tr>"""
for x in data[1:]:
  if x=='':break
  print """<tr>
  <td style="border: 1px solid black;">"""+x.split()[0]+"""</td>
  <td style="border: 1px solid black;text-align: right;" >"""+x.split()[1]+"""</td>
  <td style="border: 1px solid black;">"""+x.split()[2]+"""</td>
  <td style="border: 1px solid black;text-align: right;" >"""+x.split()[3]+"""</td></tr>"""
print "</table>"

