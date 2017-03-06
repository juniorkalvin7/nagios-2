#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
import MySQLdb
import urllib2
import sys
import time
import datetime


def uso():
  print "Monitor de disponibilidade v1.0 verifica mes atual\n"
  print "%s --help ou -h para ver modo de uso" % sys.argv[0]
  print "Modo de uso:\n"
  print "%s -L \t para ver grupo de host disponiveis" % sys.argv[0]  
  print 'ex:\n%s "SEMIT,90,80;SEMED,90,80" \t hostgroup,warn,crit;' % sys.argv[0]
  exit(1)
try:
  argumento=  sys.argv[1]#"Equatorial"
except:
  uso()
if '-h' in argumento or '--help' in argumento:
  uso()

  
conf_file='/etc/centreon/conf.pm'#configuravel
data=open(conf_file,'r').read()
host=re.findall('mysql_host = "(.+?)"',data)[0]
user=re.findall('mysql_user = "(.+?)"',data)[0]
password=re.findall('mysql_passwd = "(.+?)"',data)[0]

conn = MySQLdb.connect (host,user,password,"centreon")
cursor = conn.cursor()
  
  
if argumento=="-L":
  print "Grupos de Host Disponiveis:"
  cursor.execute ("""select hg_name from hostgroup""")
  for x in cursor.fetchall():
    print x[0]
  sys.exit(1)

hgs={}
grupos=""
if ':' in argumento:
  for x in argumento.split(':'):
    hg_name=x.split(',')[0]
    warn=x.split(',')[1]
    crit=x.split(',')[2]
    hgs[hg_name]=[warn,crit]
    grupos+="'%s' ,"%hg_name
elif ',' in argumento:
  hg_name=argumento.split(',')[0]
  warn=argumento.split(',')[1]
  crit=argumento.split(',')[2]
  hgs[hg_name]=[warn,crit]
  grupos+="'%s' ,"%hg_name
  
  
cursor.execute("select hg_id,hg_name from hostgroup where hg_name in (%s)" % grupos[:-2])
for x in cursor.fetchall():
  hg_id=x[0]
  hg_name=x[1]
  hgs[hg_name].append(int(hg_id))

#sempre inicio do mes atual
start=("%d" % (time.mktime(datetime.datetime(datetime.datetime.now().year, datetime.datetime.now().month, 1, 0, 0).timetuple())))
#ate momento atual
end=("%d" % (time.mktime(datetime.datetime(datetime.datetime.now().year, datetime.datetime.now().month, datetime.datetime.now().day, 0, 0).timetuple())))

cursor.execute ("""select session_id from centreon.session order by last_reload desc limit 1""")
session_id=cursor.fetchone()[0]

for x in hgs:
  #print x
  url = "http://cmp.intechne.com.br/cmp/include/reporting/dashboard/csvExport/csv_HostGroupLogs.php?sid=%s&hostgroup=%s&start=%s&end=%s" % (session_id,hgs[x][2],start,end)
  #print url
  #sys.exit(1)
  opener = urllib2.build_opener()
  opener.addheaders = [('Cookie', "PHPSESSID=%s"% session_id)]
  data = opener.open(url).read()
  #open('/tmp/data.html','w').write(data)
  if 'need session id' in data:
    print "CRITICAL - Nao consegui capturar session_id para extrair informacao"
    sys.exit(1)
  #print data
  #sys.exit(1)
  disp=re.findall('\nUP;(.+?);',data)[0]
  hgs[x].append(disp)

  
sinal=0
head=""
corpo=""
grapfico=""
for x in hgs:
  warn=float(hgs[x][0])
  crit=float(hgs[x][1])
  media=float(hgs[x][3])
  #print warn,crit,media,x
  if media > warn and media > crit:
    sinal=0
  elif media<crit:
    sinal=2
  elif media<warn and sinal!=2:    
    sinal=1
    
  head+="%s %s, " % (x,str(media))
  grapfico+=" %s=%s" % (x.lower(),str(media))
  corpo+="%s  Disponibilidade: %s\n" % (x,str(media))
  
if sinal==1:
  print "WARNING - %s|%s" % (head[:-2],grapfico)
elif sinal==2:
  print "CRITICAL - %s|%s" % (head[:-2],grapfico)
else:
  print "OK - %s|%s" % (head[:-2],grapfico)
print corpo
sys.exit(sinal)

