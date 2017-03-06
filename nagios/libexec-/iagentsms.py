#!/usr/bin/env python
# -*- coding: utf-8 -*-
import urllib2,re,sys,logging,urllib,getopt,os,datetime

"""
$USER1$/iagentsms.py  -c "$CONTACTPAGER$" -o "$HOSTSTATE$" -n "$NOTIFICATIONTYPE$" -h "$HOSTNAME$" -d "$SERVICEDESC$" -e "$SERVICESTATE$" -t "$SERVICEOUTPUT$" -b "$HOSTOUTPUT$" -a "$HOSTADDRESS$" -f "$LONGSERVICEOUTPUT$" -l "$LASTSERVICECHECK$"

python iagentsms.py -c 559881747881 -o HOSTSTATE -n NOTIFICATIONTYPE -h HOSTNAME -d "SERVICEDESC opcoes" -e SERVICESTATE -t SERVICEOUTPUT -b HOSTOUTPUT -a HOSTADDRESS -q "HOSTOUTPUT segunda via"

smart-sms
$USER1$/iagentsms.py \
-a "$CONTACTPAGER$" \
-b "$HOSTSTATE$" \
-c "$NOTIFICATIONTYPE$" \
-d "$HOSTNAME$" \
-e "$SERVICEDESC$" \
-f "$SERVICESTATE$" \
-g "$SERVICEOUTPUT$" \
-h "$HOSTOUTPUT$" \
-i "$HOSTADDRESS$" \
-j "$LONGSERVICEOUTPUT$" \
-k "$LASTSERVICECHECK$" \
-l "$CONTACTADDRESS2$"

"""
syslogfile='/var/log/notify.sms.log'
pluginspath='/var/lib/centreon/centplugins/'

try:
  logging.basicConfig(level=logging.DEBUG,
                      format='%(asctime)s %(message)s',
                      filename=syslogfile,filemode='a')
except:
  print "Permicao negada para arquivo de log /var/log/notify.sms.log"
  sys.exit(1)
  
def seconds_to_dhms(seconds):
  days = seconds // (3600 * 24)
  hours = (seconds // 3600) % 24
  minutes = (seconds // 60) % 60
  seconds = seconds % 60
  return days, hours, minutes, seconds

def usage():
  print 'Modo de uso\n\
python iagentsms.py\n\
  -a $CONTACTPAGER$ numero telefonico do cliente 5598xxxxxxxx\n\
  -b $HOSTSTATE$ variavelis abaixo sao do NAGIOS\n\
  -c "$NOTIFICATIONTYPE$" \n\
  -d "$HOSTNAME$" \n\
  -e "$SERVICEDESC$" \n\
  -f "$SERVICESTATE$" \n\
  -g "$SERVICEOUTPUT$" \n\
  -h "$HOSTOUTPUT$" \n\
  -i "$HOSTADDRESS$" \n\
  -j "$LONGSERVICEOUTPUT$" \n\
  -k "$LASTSERVICECHECK$" \n\
  -l "$CONTACTADDRESS2$" \n\n'


try:
  options = getopt.getopt(sys.argv[1:], 'a:b:c:d:e:f:g:h:i:j:k:l:')[0]
except getopt.GetoptError, err:
  print err
  usage()
  sys.exit()
  
for option, value in options:
  if option == '-a':CONTACTPAGER  = value      
  if option == '-b':HOSTSTATE  = value
  if option == '-c':NOTIFICATIONTYPE  = value
  if option == '-d':HOSTNAME  = value
  if option == '-e':SERVICEDESC  = value
  if option == '-f':SERVICESTATE  = value
  if option == '-g':SERVICEOUTPUT  = value  
  if option == '-h':HOSTOUTPUT  = value
  if option == '-i':HOSTADDRESS  = value
  if option == '-j':LONGSERVICEOUTPUT  = value
  if option == '-k':LASTSERVICECHECK  = value
  if option == '-l':CONTACTADDRESS2  = value
  

try:
  int(CONTACTPAGER)
except:
  print "Numero telefonico invalido"
  sys.exit(1)
  
if '$' in SERVICEDESC:
  print "Notificacao de host ainda nao implementada"
  sys.exit(1)
  

filename_log='%s%s_%s_incidente_sms'%(pluginspath,HOSTNAME,SERVICEDESC)
filename_log=filename_log.replace(' ','')


if 'RECOVERY' in NOTIFICATIONTYPE:
  start_time=open(filename_log,'r').read()    
  if 'onlysm4rtsys' in start_time:#se log contiver sintax sys adiciona ao LONGSERVICEOUTPUT para que ele saiba que he uma notificacoa privilegiada
    start_time=start_time.replace('onlysm4rtsys','')
    if 'onlysm4rtsys' not in LONGSERVICEOUTPUT:
      LONGSERVICEOUTPUT+='onlysm4rtsys'
    
  end_time=LASTSERVICECHECK
  tf=seconds_to_dhms(int(end_time)-int(start_time))
  tempofora=''      
  if tf[0]>0:tempofora+="%dd "%tf[0]
  if tf[1]>0:tempofora+="%dh "%tf[1]
  if tf[2]>0:tempofora+="%dm "%tf[2]
  if tf[3]>0:tempofora+="%ds"%tf[3]
else:
  if 'onlysm4rtsys' in LONGSERVICEOUTPUT:#se mensagem critica for so para grupo sys adiciona grupo no arquivo de tempo
    open(filename_log,'w').write(LASTSERVICECHECK+"onlysm4rtsys")
  else:
    open(filename_log,'w').write(LASTSERVICECHECK)


if '/sms' in LONGSERVICEOUTPUT:
  sms=re.findall('sms(.+?)/sms',LONGSERVICEOUTPUT)[0].split(':::')
  
  if 'RECOVERY' in NOTIFICATIONTYPE:
    
    mensagem=sms[1]
    if 'XXX' in mensagem:
      mensagem=mensagem.replace('XXX',tempofora)
    else:
      mensagem+=" %s"%tempofora
  else:
    print filename_log
    if 'onlysm4rtsys' in LONGSERVICEOUTPUT:#se mensagem critica for so para grupo sys adiciona grupo no arquivo de tempo
      open(filename_log,'w').write(LASTSERVICECHECK+"onlysm4rtsys")
    else:
      open(filename_log,'w').write(LASTSERVICECHECK)
    mensagem=sms[0]
else:
  if 'PROBLEM' in NOTIFICATIONTYPE:NOTIFICATIONTYPE='INCIDENTE'
  if 'RECOVERY' in NOTIFICATIONTYPE:NOTIFICATIONTYPE='RESTAURADO'
  if 'Service Check Timed Out' in SERVICEOUTPUT:
    SERVICEOUTPUT='Problema no link de internet, execucao do plugin atingiu limite de tempo impossivel efetuar testes inteligentes'
  else:
    SERVICEOUTPUT=HOSTNAME+" "+SERVICEDESC+" "+SERVICEOUTPUT
  mensagem=SERVICESTATE+" "+SERVICEOUTPUT



if 'onlysm4rtsys' in LONGSERVICEOUTPUT and not 'sys' in CONTACTADDRESS2:
  logging.info("%s nao faz parte do grupo envio privilegiado %s"%(CONTACTPAGER,mensagem))
  sys.exit(1)
  
#open("/tmp/msg.sms",'a').write(NOTIFICATIONTYPE+"\n")
#open("/tmp/msg.sms",'a').write(SERVICESTATE+"\n")
#open("/tmp/msg.sms",'a').write(SERVICEOUTPUT+"\n")
#open("/tmp/msg.sms",'a').write(re.findall('(+.?)',LONGSERVICEOUTPUT)+"\n"+"\n")
#sys.exit(3)

opener = urllib2.build_opener() 
headers = {'User-Agent': 'Intechne smsAgent 1.0 to iagentsms'}
urllib2.install_opener(opener)
url="http://www.iagentesms.com.br/webservices/http.php"


corpo=[]
#n=150
#print len(mensagens)
#for mensagem in (mensagens[i:i+n] for i in xrange(0, len(mensagens), n)):
mensagem = mensagem[:150]

values = {'metodo'  : 'envio',
        'usuario' : 'intechne',
        'senha'   : '19092013',
        'mensagem':  mensagem,
        'celular' :  CONTACTPAGER          
        }

data = urllib.urlencode(values)
req = urllib2.Request(url,data,headers)
data = urllib2.urlopen(req).read()
#print data
logging.info(str(CONTACTPAGER)+" "+mensagem+" Res:"+data)


