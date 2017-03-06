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
import commands
import time
import math
import os
import sys


"""
crie as entradas no snmpd.conf
exec .1.3.6.1.4.1.2023.01 traffic_tunnel /usr/bin/python /usr/local/bin/get_traffic_from_dev.py tun0

/usr/local/bin/get_traffic_from_dev.py
#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
args = sys.argv[1:]
if len(args)<1:
  print "Centreon Plugin\nMedidor de trafego por dispositivo por GemayelLira"
  print "Argumentos: dispositivo"
  print "Ex.\npython %s tun0" % sys.argv[0] 
  sys.exit(1)
else:
  device=args[0]
a=0
for i in open('/proc/net/dev').read().split('\n'):
  if i.count(device):
    i=i.split(":")[1]
    print "%s:%s:%s:%s" % (device,i.split()[0],device,i.split()[8])
    a+=1
if a==0:print "CRITICAL - device nao encontrado"


cheque o mib correto criado para saida do trafego no meu ex:
snmpwalk -v 1 -c u3fr0I9b5 127.0.0.1 .1.3.6.1.4.1.2023.02
snmpwalk -v 1 -c u3fr0I9b5 127.0.0.1 .1.3.6.1.4.1.2023.02.101.1

por gemayellira@gmail.com
"""

args = sys.argv[1:]
if len(args)<3:
  print "Centreon Plugin\nMedidor de trafego por device por GemayelLira"
  print "Argumentos:host community MIB tun0"
  print "Ex.\npython %s 127.0.0.1 u3fr0I9b5 .1.3.6.1.4.1.2023.01" % sys.argv[0] 
  #print 
  sys.exit(1)
else:
  #print args
  host=args[0]
  community=args[1]
  MIB=args[2]
  device=[3]
  #out_mib=args[3]
  #print args
#print "/tmp/traffic_%s_%s_%s" % (str(host),str(in_mib),str(out_mib))
#exit(1)
arquivo="/var/lib/centreon/centplugins/traffic_%s_%s" % (str(host),str(MIB))
#print "snmpwalk -v 1 -c %s %s %s" %(community,str(host),str(out_mib))
try:
  traffic=commands.getoutput("/usr/bin/snmpwalk -v 1 -c %s %s %s.101.1" %(community,str(host),str(MIB))).split("\"")[1].split(':')
  in_bits=int(traffic[1])
  out_bits=int(traffic[3])
except Exception,e:
  print "CRITICAL - nao consegui capturar valores"
  sys.exit(1)

#sys.exit(1)
#print in_bits
#print out_bits
#exit(1)
#out_bits=int(commands.getoutput("snmpget -v 1 -c u3fr0I9b5 brisamar.fromti.com.br .1.3.6.1.2.1.2.2.1.10.4").split()[3])




speed_card=10000000
#tempo = int(format(time.mktime(time.localtime()),'.0f'))
tempo = int(time.mktime(time.localtime()))

#print 'TEMPO:',tempo,"IN_BITS:",in_bits,"OUT_BITS:",out_bits
#exit(1)

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
  open(arquivo,'w').write('%s:%s:%s' % (str(tempo),str(in_bits),str(out_bits)))
  print "Problemas valores negativos criando base novamente..."
  sys.exit(1)
else:
  total = in_bits - last_in_bits
diff = tempo - last_time 
if diff==0:diff=1
pct_in_traffic = math.fabs(float(str(total)+".0")/diff)
in_traffic = pct_in_traffic


if (out_bits - last_out_bits) < 0:
  total= 4294967296 * 8 - last_out_bits + out_bits
  open(arquivo,'w').write('%s:%s:%s' % (str(tempo),str(in_bits),str(out_bits)))
  print "Problemas valores negativos criando base novamente..."
  sys.exit(1)
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
  

#print "uso_placa_IN:",in_uso
#print "IN:%s%s" % (str(format(in_traffic,".2f")),in_prefix)
#print "IN_TOTAL:%s%s" %(str(format(in_bits,".2f")),in_bits_unit)

#print "uso_placa_OUT:",out_uso
#print "OUT:%s%s" % (str(format(out_traffic,".2f")),out_prefix)
#print "OUT_TOTAL:%s%s" %(str(format(out_bits,".2f")),out_bits_unit)
print "Traffic In : %s %sb/s (%s %%), Out : %s %sb/s (%s %%) -" %\
      ('%.2f'%(in_traffic),in_prefix,in_uso,'%.2f'%(out_traffic),out_prefix,out_uso),
print "Total RX Bytes In : %s %sB, Out : %s %sb|traffic_in=%sBytes/s;0;%s traffic_out=%sBytes/s;0;%s" %\
      ('%.2f'%(in_bits),in_bits_unit,'%.2f'%(out_bits),out_bits_unit,\
       ('%.1f'%(pct_in_traffic)).replace('.',','),speed_card,('%.1f'%(pct_out_traffic)).replace('.',','),speed_card)
  
