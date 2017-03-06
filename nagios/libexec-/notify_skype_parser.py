#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
$USER1$/notify_skype_parser.py -c "$CONTACTADDRESS1$" -o "$HOSTSTATE$" -n "$NOTIFICATIONTYPE$" -h "$HOSTNAME$" -d "$SERVICEDESC$" -e "$SERVICESTATE$" -t "$SERVICEOUTPUT$" -a "$HOSTADDRESS$" -q "$HOSTOUTPUT$" -f "$HOSTACKAUTHOR$" -x "$HOSTACKCOMMENT$" -z "$SERVICEACKAUTHOR$" -k "$SERVICEACKCOMMENT$"  -p "$LASTHOSTCHECK$"  -l "$LASTSERVICECHECK$"

python /usr/local/nagios/libexec/notify_skype_parser.py -c gemayellira -o "UP" -n "RECOVERY" -h "Centreon-Server" -d "MportCheck" -e "OK" -t "MPortCheck - 127.0.0.1 http=OPEN ssh=OPEN" -a "127.0.0.1" -q "OK - 127.0.0.1: rta 0.056ms, lost 0%"  -f "$HOSTACKAUTHOR$" -x "$HOSTACKCOMMENT$" -z "$SERVICEACKAUTHOR$" -k "$SERVICEACKCOMMENT$"  -p "$LASTHOSTCHECK$"  -l "$LASTSERVICECHECK$"


"""
import sys
import logging
import urllib2
import urllib
import getopt
import datetime

syslogfile='/tmp/notify.skype.log'
logging.basicConfig(level=logging.DEBUG,
                  format='%(asctime)s %(message)s',
                  filename=syslogfile,filemode='a')



def usage():
  print 'Modo de uso\n\
python notify_skype_parser.py\n\
  -c $CONTACTADDRESS1$ login do skype\n\
  -o $HOSTSTATE$ variavelis abaixo sao do NAGIOS\n\
  -n "$NOTIFICATIONTYPE$" \n\
  -h "$HOSTNAME$" \n\
  -d "$SERVICEDESC$" \n\
  -e "$SERVICESTATE$" \n\
  -a "$HOSTADDRESS$" \n\
  -q "$HOSTOUTPUT$" \n\
  -f "$HOSTACKAUTHOR$" \n\
  -x "$HOSTACKCOMMENT$" \n\
  -p "$LASTHOSTCHECK$" \n\
  -l "$LASTSERVICECHECK$" \n\
  -z "$SERVICEACKAUTHOR$" \n\
  -k "$SERVICEACKCOMMENT$" \n'

  #print len(sys.argv)
#if not len(sys.argv) == 23:
  #usage()
  #sys.exit()

try:
  options = getopt.getopt(sys.argv[1:], 'z:s:u:p:c:o:n:h:d:e:t:a:q:f:x:z:k::p:l:')[0]
except getopt.GetoptError, err:
  print err
  usage()
  sys.exit()

HOSTACKAUTHOR=''
HOSTACKCOMMENT=''
SERVICEACKAUTHOR=''
SERVICEACKCOMMENT=''  
  
for option, value in options:
  #print option,value
  if option == '-c':
    skypecontato  = value      
  if option == '-o':
    HOSTSTATE  = value
  if option == '-n':
    NOTIFICATIONTYPE  = value
  if option == '-h':
    HOSTNAME  = value
  if option == '-d':
    SERVICEDESC  = value
  if option == '-e':
    SERVICESTATE  = value
  if option == '-t':
    SERVICEOUTPUT  = value  
  if option == '-a':
    HOSTADDRESS  = value
  if option == '-q':
    HOSTOUTPUT  = value
  if option == '-f':
    HOSTACKAUTHOR  = value
  if option == '-x':
    HOSTACKCOMMENT  = value
  if option == '-z':
    SERVICEACKAUTHOR  = value
  if option == '-k':
    SERVICEACKCOMMENT  = value
  if option == '-p':
    LASTHOSTCHECK  = value
  if option == '-l':
    LASTSERVICECHECK  = value
    
  
#open('/tmp/type.txt','a').write(NOTIFICATIONTYPE+'\n')

if "RECOVERY" in NOTIFICATIONTYPE:
  NOTIFICATIONTYPE="RESOLVIDO"
elif 'ACKNOWLEDGEMENT' in NOTIFICATIONTYPE:
  NOTIFICATIONTYPE="RECONHECIDO"  
else:
  NOTIFICATIONTYPE="INCIDENTE"

#SAIDA DE HOST
if "Host unreachable" in HOSTOUTPUT:
  #f=HOSTOUTPUT
  if '@' in HOSTOUTPUT:
    HOSTOUTPUT=HOSTOUTPUT.split('@')[0]
  HOSTOUTPUT=HOSTOUTPUT.replace("Host unreachable","Elemento de rede inalcancavel")
    
if "(Host Check Timed Out)" in HOSTOUTPUT:
  f=HOSTOUTPUT
  HOSTOUTPUT=HOSTOUTPUT.replace("(Host Check Timed Out)",u"Nao foi possivel contatar o elemento de rede de destino %s"%f)
if "CRITICAL" in HOSTOUTPUT:
  HOSTOUTPUT=HOSTOUTPUT.replace('CRITICAL','CRITICO')

#SAIDA DE SERVICO
if "(Service Check Timed Out)" in SERVICEOUTPUT:
  f=SERVICEOUTPUT
  SERVICEOUTPUT=SERVICEOUTPUT.replace("(Service Check Timed Out)",u"Nao foi possivel contatar o elemento de rede de destino %s"%f)
if "CRITICAL" in SERVICEOUTPUT:
  SERVICEOUTPUT=SERVICEOUTPUT.replace('CRITICAL','CRITICO')
    
    
if '$' in SERVICEDESC:tipomensagem='host'
else:tipomensagem='service'

try:
  if tipomensagem=='service':#se for servico
    #text
    if NOTIFICATIONTYPE=='INCIDENTE':#com problema
      text=str(datetime.datetime.fromtimestamp(int(LASTSERVICECHECK)))+' '+NOTIFICATIONTYPE+" Alerta identificado:"+SERVICEOUTPUT+" \nServico com problema:"+SERVICEDESC+" \nElemento:"+HOSTNAME+"("+HOSTADDRESS+") "+HOSTSTATE
    elif NOTIFICATIONTYPE=='RECONHECIDO':
      text=str(datetime.datetime.fromtimestamp(int(LASTSERVICECHECK)))+' '+NOTIFICATIONTYPE+" Servico:"+SERVICEDESC+" \nPor:"+SERVICEACKAUTHOR+" \nComentario:"+SERVICEACKCOMMENT+" \nElemento:"+HOSTNAME+"("+HOSTADDRESS+") "+HOSTSTATE
    else:
        #resolvido
      text=str(datetime.datetime.fromtimestamp(int(LASTSERVICECHECK)))+' '+NOTIFICATIONTYPE+" Aviso de retorno:"+SERVICEOUTPUT+" \nServico Restaurado:"+SERVICEDESC+" \nElemento:"+HOSTNAME+"("+HOSTADDRESS+") "+HOSTSTATE

  
  else:#se for host
    if NOTIFICATIONTYPE=='INCIDENTE':#com problema
      text=str(datetime.datetime.fromtimestamp(int(LASTHOSTCHECK)))+' '+NOTIFICATIONTYPE+" Alerta identificado:"+HOSTOUTPUT+" \nElemento de rede impactado:"+HOSTNAME+"("+HOSTADDRESS+") \nStatus:"+HOSTSTATE
    elif NOTIFICATIONTYPE=='RECONHECIDO':
      text=str(datetime.datetime.fromtimestamp(int(LASTHOSTCHECK)))+' '+NOTIFICATIONTYPE+" Elemento:"+HOSTNAME+"("+HOSTADDRESS+") "+HOSTSTATE+" \nPor:"+HOSTACKAUTHOR+" \nComentario:"+HOSTACKCOMMENT
    else:#resolvido
      text=str(datetime.datetime.fromtimestamp(int(LASTHOSTCHECK)))+' '+NOTIFICATIONTYPE+" Aviso de retorno:"+HOSTOUTPUT+" \nElemento de rede impactado:"+HOSTNAME+"("+HOSTADDRESS+") \nStatus:"+HOSTSTATE

except Exception,e:
  print e
  usage()
  sys.exit(1)
    

  
opener = urllib2.build_opener() 
headers = {'User-Agent': 'SmsAgent1.0'}
urllib2.install_opener(opener)
url = "https://184.106.240.186/skype.php"
values = {'s': text,'l':skypecontato}
data = urllib.urlencode(values)
req = urllib2.Request(url,data,headers)
data = urllib2.urlopen(req).read()

f=skypecontato+" "+text+NOTIFICATIONTYPE

logging.info(f.replace('\n',''))



