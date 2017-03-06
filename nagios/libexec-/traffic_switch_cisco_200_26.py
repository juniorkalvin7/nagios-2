#!/usr/bin/env python
# -*- coding: utf-8 -*-
#SG 200-26
import sys,urllib,urllib2,re,cookielib,os,time,math

"""
  (0) OK
  (1) WARNING
  (2) CRITICAL
  (3)UNKNOWN
"""

def seconds_to_dhms(seconds):
  days = seconds // (3600 * 24)
  hours = (seconds // 3600) % 24
  minutes = (seconds // 60) % 60
  seconds = seconds % 60
  foo=''
  if days>0:foo+="%d dias(s), "%days
  if hours>0:foo+="%d hora(s), "%hours
  if minutes>0:foo+="%d minuto(s), "%minutes
  if seconds>0:foo+="e %d segundo(s)"%seconds
  return foo,days


nettable={'GE1':'49',
          'GE2':'50',
          'GE3':'51',
          'GE4':'52',
          'GE5':'53',
          'GE6':'54',
          'GE7':'55',
          'GE8':'56',
          'GE9':'57',
          'GE10':'58',
          'GE11':'59',
          'GE12':'60',
          'GE13':'61',
          'GE14':'62',
          'GE15':'63',
          'GE16':'64',
          'GE17':'65',
          'GE18':'66',
          'GE19':'67',
          'GE20':'68',
          'GE21':'69',
          'GE22':'70',
          'GE23':'71',
          'GE24':'72',
          'GE25':'73',
          'GE26':'74'}

args = sys.argv[1:]
if len(args) != 4:
  print "Network Plugin para Switch Cisco SG 200-26\t\t\tpor GemayelLira\nCaptura informacoes de interfaces\n"
  print "Argumentos:host usuario senha interface ou uptime"
  print "Tipos de interfaces suportadas:"
  cnt=0
  for x in nettable:
    sys.stdout.write('%s,'%x)
    if cnt==10:
      print
      cnt=0
    else:cnt+=1
  print "\nEx.\n"+os.getcwd()+"/%s 192.168.0.96 cisco cisco GE1" % sys.argv[0] 
  sys.exit(1)
else:
  host=args[0]
  usuario=args[1]
  senha=args[2]
  interface=args[3]
  

#acompanhamento de cookie
cj = cookielib.CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
cookie_file='/tmp/cookie_%s'%host

if not os.path.isfile(cookie_file):
  request = urllib2.Request("http://%s/cs2ba8c18f/config/System.xml?action=login&user=%s&password=%s"%(host,usuario,senha))
  response = urllib2.urlopen(request)
  resposta=response.read()
  if 'statusString>OK</statusString' in resposta:
    #print 'Logado'
    sessionID = response.info().getheader('sessionID')
  elif 'Bad User or Password' in resposta:
    print 'CRITICAL - Usuario e senha invalido'
    sys.exit(2)
  else:
    print 'WARNING - Erro ao logar na pagina renovando cookies\n',response.info().getheader('sessionID'),resposta
    sys.exit(1)
  opener.addheaders.append(('Cookie', 'usernme=%s;userStatus=ok;sessionID=%s' % (usuario,sessionID)))
  open(cookie_file,'w').write('usernme=%s;userStatus=ok;sessionID=%s' % (usuario,sessionID))
else:
  opener.addheaders.append(('Cookie',open(cookie_file,'r').read()))

if interface=="uptime":
  url = "http://%s/cs2ba8c18f/sysinfo/system_general_description_m.htm" % (host)
  data = opener.open(url).read()
  open('/tmp/data.html','w').write(data)
  
  if 'sysUpTime' in data:
    uptime=data.split('name="sysUpTime" disabled   value="')[1].split('" SIZE')[0]
    uptime=seconds_to_dhms(int(uptime)/100)
    print "Uptime %s|uptime=%dday(s)" % (uptime)
  else:
    print "Uptime erro"
    os.system('rm -rfv %s' % cookie_file)

    sys.exit(1)
  sys.exit(0)
else:
  url = "http://%s/cs2ba8c18f/IfStats/statist_interfaceStat_interface_m.htm?Query:ifIndex=%s" % (host,nettable[interface])
data = opener.open(url).read()
try:
  in_bits = int(re.findall('writeFormattedNumber\("(.+?)",pgTkn,"TotalBytesNum"',data)[0])#recebido
  out_bits  = int(re.findall('writeFormattedNumber\("(.+?)",pgTkn,"TotalBytesBottomNum"',data)[0])#enviado
except Exception,e:
  #print 'CRITICAL - Erro na leitura de trafego'
  print 'WARNING - Renovando cookie',e
  #print 'Data:',data
  os.system('rm -rfv %s' % cookie_file)
  sys.exit(1)
arquivo="/var/lib/centreon/centplugins/traffic_switch_%s_%s" % (str(host),str(interface))
#arquivo='traf'

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
  

#print "uso_placa_IN:",in_uso
#print "IN:%s%s" % (str(format(in_traffic,".2f")),in_prefix)
#print "IN_TOTAL:%s%s" %(str(format(in_bits,".2f")),in_bits_unit)

#print "uso_placa_OUT:",out_uso
#print "OUT:%s%s" % (str(format(out_traffic,".2f")),out_prefix)
#print "OUT_TOTAL:%s%s" %(str(format(out_bits,".2f")),out_bits_unit)
print "Traffic In : %s %sb/s (%s %%), Out : %s %sb/s (%s %%) -" %\
      ('%.2f'%(in_traffic),in_prefix,in_uso,'%.2f'%(out_traffic),out_prefix,out_uso),
print "Total RX Bits In : %s %sB, Out : %s %sb|traffic_in=%sBits/s;0;%s traffic_out=%sBits/s;0;%s" %\
      ('%.2f'%(in_bits),in_bits_unit,'%.2f'%(out_bits),out_bits_unit,\
       ('%.1f'%(pct_in_traffic)).replace('.',','),speed_card,('%.1f'%(pct_out_traffic)).replace('.',','),speed_card)
  
