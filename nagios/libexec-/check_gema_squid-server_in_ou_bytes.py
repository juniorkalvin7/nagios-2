#!/usr/bin/env python
# -*- coding: utf-8 -*-
import commands
import time
import math
import os
import sys


args = sys.argv[1:]

if len(args)<2:
  print "Centreon Plugin\nGet Squid - Server In/Out Bytes"
  print "Argumentos:host community"
  print "Ex.\n%s 10.0.0.45 u3fr0I9b5" % sys.argv[0] 
  #print 
  sys.exit(1)
else:
  #print args
  host=args[0]
  community=args[1]
try:
  in_bits=(commands.getoutput("/usr/bin/snmpwalk -t 100000 -v 1 -c %s %s:3401 1.3.6.1.4.1.3495.1.3.2.1.12" %(community,str(host)))).split(': ')[1]
  out_bits=(commands.getoutput("/usr/bin/snmpwalk -t 100000 -v 1 -c %s %s:3401 1.3.6.1.4.1.3495.1.3.2.1.13" %(community,str(host)))).split(': ')[1]
except Exception,e:
  print "CRITICAL - nao consegui capturar valores"
  print e
  sys.exit(2)
in_bits=int(in_bits)
out_bits=int(out_bits)
arquivo="/var/lib/centreon/centplugins/squid_%s_server_in_out_bytes" % (str(host))


speed_card=10000000
tempo = int(time.mktime(time.localtime()))

if os.path.exists(arquivo) == False:
  open(arquivo,'w').write('%s:%s:%s' % (str(tempo),str(in_bits),str(out_bits)))
  print "Primeira execucao armazenando dados..."
  #print ""
  sys.exit(1)
datafile=open(arquivo,'r').read().split(":")
try:
  last_time=int(datafile[0])
  last_in_bits=int(datafile[1])
  last_out_bits=int(datafile[2])
except Exception,e:
  print arquivo,"problem"
  os.system('rm -rf %s' % arquivo)  
  sys.exit(1)
  
open(arquivo,'w').write('%s:%s:%s' % (str(tempo),str(in_bits),str(out_bits)))

if (in_bits - last_in_bits) < 0:
  total= 4294967296 * 8 - last_in_bits + in_bits
else:
  total = in_bits - last_in_bits
diff = tempo - last_time 
if diff==0:diff=1
pct_in_traffic = math.fabs(float(str(total)+".0")/diff)
in_traffic = pct_in_traffic


if (out_bits - last_out_bits) < 0:
  total= 4294967296 * 8 - last_out_bits + out_bits
else:
  total = out_bits - last_out_bits
diff = tempo - last_time 
if diff==0:diff=1
pct_out_traffic = math.fabs(float(str(total)+".0")/diff)
out_traffic = pct_out_traffic

#print pct_in_traffic
#print pct_out_traffic
#print 
#print "A ",str(in_traffic*100/speed_card)
#in_uso=format(in_traffic * 100 / speed_card,'.1f')
in_uso='%.1f'%(in_traffic * 100 / speed_card)
#print in_uso
#exit(1)
in_prefix=""
if (in_traffic > 1000):
    in_traffic = in_traffic / 1000
    in_prefix = "k"
    if(in_traffic > 1000):
      in_traffic = in_traffic / 1000
      in_prefix = "M"
    if(in_traffic > 1000):
      in_traffic = in_traffic / 1000
      in_prefix = "G"    

#out_uso=format(out_traffic * 100 / speed_card,'.1f')
out_uso='%.1f'%(out_traffic * 100 / speed_card)

out_prefix=""
if (out_traffic > 1000):
    out_traffic = out_traffic / 1000
    out_prefix = "k"
    if(out_traffic > 1000):
      out_traffic = out_traffic / 1000
      out_prefix = "M"
    if(out_traffic > 1000):
      out_traffic = out_traffic / 1000
      out_prefix = "G"       
      
in_bits_unit=""
#in_bits = in_bits/1048576
in_bits = float(str(in_bits)+'.0')/1048576
if (in_bits > 1000):
  in_bits = in_bits / 1000;
  in_bits_unit = "G"
else:
  in_bits_unit = "M"
 
out_bits_unit=""
#out_bits = out_bits/1048576
out_bits = float(str(out_bits)+'.0')/1048576
if (out_bits > 1000):
  out_bits = out_bits / 1000;
  out_bits_unit = "G"
else:
  out_bits_unit = "M"  

print "Squid - Server In/Out Bytes Traffic In : %s %sb/s (%s %%), Out : %s %sb/s (%s %%) -" %\
      ('%.2f'%(in_traffic),in_prefix,in_uso,'%.2f'%(out_traffic),out_prefix,out_uso),
print "Total RX Bits In : %s %sB, Out : %s %sb|squidstat=%sBits/s;0;%s squidstatb=%sBits/s;0;%s" %\
      ('%.2f'%(in_bits),in_bits_unit,'%.2f'%(out_bits),out_bits_unit,\
       ('%.1f'%(pct_in_traffic)).replace('.',','),speed_card,('%.1f'%(pct_out_traffic)).replace('.',','),speed_card)
 

