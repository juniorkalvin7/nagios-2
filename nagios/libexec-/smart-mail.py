#!/usr/bin/python
# -*- coding: utf-8 -*-
#por gemayellira 4dec13
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email import Encoders
import os,sys,getopt,datetime,re
import logging
"""
#informacoes administrativas in
Tag para formatacao em negrito no email Bbi Bbo
CONTACTADDRESS2 especifica tipo de usuario sys=sistema ou cliente = cliente
se houver sm4rtsys no SERVICEOUTPUT so manda se o usuario contiver sys em seu CONTACTADDRESS2
#informacoes administrativas eof



$USER1$/notify_by_mail2.py -z 1 -s smtp.live.com -u "alerta@fromti.com.br" -p 113lkx09b1 -c "$CONTACTEMAIL$" -o "$HOSTSTATE$" -n "$NOTIFICATIONTYPE$" -h "$HOSTNAME$" -d "$SERVICEDESC$" -e "$SERVICESTATE$" -t "$SERVICEOUTPUT$" -a "$HOSTADDRESS$" -q "$HOSTOUTPUT$"
./notify_by_mail2.py -z 1 -s 200.253.157.14 -u "monitoramento@intechne.com.br" -p labsecur1t1 -c "gemayel@intechne.com.br" -o "$HOSTSTATE$" -n "$NOTIFICATIONTYPE$" -h "$HOSTNAME$" -d "$SERVICEDESC$" -e "$SERVICESTATE$" -t "$SERVICEOUTPUT$" -a "$HOSTADDRESS$" -q "$HOSTOUTPUT$"
$USER1$/notify_skype_parser.py -c "$CONTACTADDRESS1$" -o "$HOSTSTATE$" -n "$NOTIFICATIONTYPE$" -h "$HOSTNAME$" -d "$SERVICEDESC$" -e "$SERVICESTATE$" -t "$SERVICEOUTPUT$" -a "$HOSTADDRESS$" -q "$HOSTOUTPUT$" -f "$HOSTACKAUTHOR$" -x "$HOSTACKCOMMENT$" -z "$SERVICEACKAUTHOR$" -k "$SERVICEACKCOMMENT$"
$USER1$/smart-mail.py -z 1 -s smtp.intechne.com.br -u "monitoramento@intechne.com.br" -p labsecur1t1 -c "$CONTACTEMAIL$" -o "$HOSTSTATE$" -n "$NOTIFICATIONTYPE$" -h "$HOSTNAME$" -d "$SERVICEDESC$" -e "$SERVICESTATE$" -t "$SERVICEOUTPUT$" -a "$HOSTADDRESS$" -q "$HOSTOUTPUT$" -l "$LONGSERVICEOUTPUT$" -f "$LASTSERVICECHECK$" -g "$LASTHOSTCHECK$"

CONTACTADDRESS2 especifica tipo de usuario sys=sistema ou cliente = cliente

smart-sms
$USER1$/smart-mail.py \
-a 1 \
-b smtp.intechne.com.br \
-c "monitoramento@intechne.com.br" \
-d labsecur1t1 \
-e "$CONTACTEMAIL$" \
-f "$HOSTSTATE$" \
-g "$NOTIFICATIONTYPE$" \
-h "$HOSTNAME$" \
-i "$SERVICEDESC$" \
-j "$SERVICESTATE$" \
-k "$SERVICEOUTPUT$" \
-l "$HOSTOUTPUT$" \
-m "$HOSTADDRESS$" \
-n "$LONGSERVICEOUTPUT$" \
-o "$LASTSERVICECHECK$" \
-p "$LASTHOSTCHECK$" \
-q "$CONTACTADDRESS2$"

"""

def seconds_to_dhms(seconds):
  days = seconds // (3600 * 24)
  hours = (seconds // 3600) % 24
  minutes = (seconds // 60) % 60
  seconds = seconds % 60
  return days, hours, minutes, seconds

def mail(IPSMTPSRV, USERMAIL, SENHAMAIL,subject,text,tlsvar,to):
  if ':' in to:
    toto = to.split(':')
    for to in toto:
      try:
        msg = MIMEMultipart()
        msg['From'] = USERMAIL
        msg['To'] = to
        msg['Subject'] = subject
        msg["Content-type"] = "text/html"
        msg.attach(MIMEText(text,'html'))
        mailServer = smtplib.SMTP(IPSMTPSRV, 25)
        mailServer.ehlo()
        if tlsvar=='1':
          mailServer.starttls()
          mailServer.ehlo()
        mailServer.login(USERMAIL, SENHAMAIL)
        mailServer.sendmail(USERMAIL, to, msg.as_string())
        mailServer.close()
        logging.info("%s %s"%(to,subject))
      except Exception,e:
        logging.info("%s %s erro:%s"%(to,subject,e))

  else:
    to=to
    try:
      msg = MIMEMultipart()
      msg['From'] = USERMAIL
      msg['To'] = to
      msg['Subject'] = subject
      msg["Content-type"] = "text/html"
      msg.attach(MIMEText(text,'html'))
      mailServer = smtplib.SMTP(IPSMTPSRV, 25)
      mailServer.ehlo()
      if tlsvar=='1':
        mailServer.starttls()
        mailServer.ehlo()
      mailServer.login(USERMAIL, SENHAMAIL)
      mailServer.sendmail(USERMAIL, to, msg.as_string())
      mailServer.close()
      logging.info("%s %s"%(to,subject))
    except Exception,e:
      logging.info("%s %s erro:%s"%(to,subject,e))

def usage():
  print 'Modo de uso\n\
python smart-mail.py\n\
  -a 1 or 0 se o servidor usa autenticacao tls\n\
  -b $IPSMTPSRV ip do servidor de email\n\
  -c $USERMAIL usuario do email\n\
  -d $SENHAMAIL senha do email\n\
  -e $email da pessoa\n\
  -f $HOSTSTATE$ variavelis abaixo sao do NAGIOS\n\
  -g "$NOTIFICATIONTYPE$" \n\
  -h "$HOSTNAME$" \n\
  -i "$SERVICEDESC$" \n\
  -j "$SERVICESTATE$" \n\
  -k "$SERVICEOUTPUT$" \n\
  -l "$HOSTOUTPUT$" \n\
  -m "$HOSTADDRESS$" \n\
  -n "$LONGSERVICEOUTPUT$"\n\
  -o "$LASTSERVICECHECK$" \n\
  -p "$LASTHOSTCHECK$" \n\
  -q "$CONTACTADDRESS2$"\n'
  
try:
  options = getopt.getopt(sys.argv[1:], 'a:b:c:d:e:f:g:h:i:j:k:l:m:n:o:p:q:')[0]
except getopt.GetoptError, err:
  print err
  usage()
  sys.exit()
  
for option, value in options:#carregando opcoes
  print option,value
  if option == '-a':tlsvar  = value
  if option == '-b':IPSMTPSRV  = value
  if option == '-c':USERMAIL  = value
  if option == '-d':SENHAMAIL  = value      
  if option == '-e':to  = value      
  if option == '-f':HOSTSTATE  = value
  if option == '-g':NOTIFICATIONTYPE  = value
  if option == '-h':HOSTNAME  = value
  if option == '-i':SERVICEDESC  = value
  if option == '-j':SERVICESTATE  = value
  if option == '-k':SERVICEOUTPUT  = value  
  if option == '-l':HOSTOUTPUT  = value
  if option == '-m':HOSTADDRESS  = value
  if option == '-n':LONGSERVICEOUTPUT=value
  if option == '-o':LASTSERVICECHECK=value
  if option == '-p':LASTHOSTCHECK=value
  if option == '-q':CONTACTADDRESS2=value
  

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(message)s',
                    filename='/tmp/notify.mail.log',
                    filemode='a')

pluginspath='/var/lib/centreon/centplugins/'

#Custom messages reader in
tmp=open('/usr/local/nagios/libexec/msg-custom','r').read()
#tmp=open('msg-custom','r').read()
#print msgs_custom
msgs_custom={}
cont1=0
while 1:		
  try:
    inicio = tmp.index('{') + 1
    fim = tmp.index('}')
  except:break
  msgdata = tmp[inicio:fim]
  string=msgdata.split('\n')[0].replace('strings=','')
  strings=string.split(';')  
  alerta=msgdata.split('\n')[1].replace('Alerta=','')
  causas=msgdata.split('\n')[2].replace('Causas=','')
  restore=msgdata.split('\n')[3].replace('Restore=','')
  msgs_custom[cont1]=[strings,alerta,causas,restore]
  cont1 +=1	
  tmp = tmp[fim + 1:]
#print msgs_custom
#print "SERVICEOUTPUT",SERVICEOUTPUT
for x in msgs_custom:
  teve=0
  for xx in msgs_custom[x][0]:
    #print "verificando ",xx
    if ',' in xx and '[' in xx:
      for xxx in xx.replace('[','').replace(']','').split(','):
        #print "verificando xxx",xxx
        if xxx in SERVICEOUTPUT:
          alerta=msgs_custom[x][1]
          causas=msgs_custom[x][2]
          #restore=
          teve=1
          break
    elif not ',' in xx and xx in SERVICEOUTPUT:
      #string=
      alerta=msgs_custom[x][1]
      causas=msgs_custom[x][2]
      #restore=
      teve=1
      
  if teve==1:break
#sys.exit(1)
if teve==0:
  alerta='N&#227;o cadastrado'
  causas='N&#227;o cadastrado'
  
#Custom messages reader eof
#print 'teve',teve
#print alerta
#print causas
#sys.exit(1)

#TRADUCOES
try:
  
  #ACKNOWLEDGEMENT
  if "RECOVERY" in NOTIFICATIONTYPE:
    NOTIFICATIONTYPE="RESOLVIDO"
  else:
    NOTIFICATIONTYPE="INCIDENTE"
    
  #SAIDA DE HOST
  if "Host unreachable" in HOSTOUTPUT:
    #f=HOSTOUTPUT
    if '@' in HOSTOUTPUT:
      HOSTOUTPUT=HOSTOUTPUT.split('@')[0]
    HOSTOUTPUT=HOSTOUTPUT.replace("Host unreachable","Elemento de rede inalcan&ccedil;&aacute;vel")
      
  if "(Host Check Timed Out)" in HOSTOUTPUT:
    f=HOSTOUTPUT
    HOSTOUTPUT=HOSTOUTPUT.replace("(Host Check Timed Out)","N&atilde;o foi poss&iacute;vel contatar o elemento de rede de destino %s"%f)
  if "CRITICAL" in HOSTOUTPUT:
    HOSTOUTPUT=HOSTOUTPUT.replace('CRITICAL','CR&Iacute;TICO')

  #SAIDA DE SERVICO
  if "(Service Check Timed Out)" in SERVICEOUTPUT:
    f=SERVICEOUTPUT
    SERVICEOUTPUT=SERVICEOUTPUT.replace("(Service Check Timed Out)","N&atilde;o foi poss&iacute;vel contatar o elemento de rede de destino %s"%f)
  if "CRITICAL" in SERVICEOUTPUT:
    SERVICEOUTPUT=SERVICEOUTPUT.replace('CRITICAL','CR&#205;TICO')
    
    
  #escolha de assunto
  if '$' in SERVICEDESC:
    tipomensagem='host'
    #host
    if 'INCIDENTE' == NOTIFICATIONTYPE:
      subject=NOTIFICATIONTYPE+': Alerta no elemento de rede ['+HOSTNAME+']'
    else:
      subject=NOTIFICATIONTYPE+': O elemento de rede ['+HOSTNAME+'] foi restaurado'

  else:
    tipomensagem='service'
    #service
    if 'INCIDENTE' == NOTIFICATIONTYPE:
      subject=NOTIFICATIONTYPE+u': Alerta para o serviço ['+SERVICEDESC+'] do elemento de rede ['+HOSTNAME+']'
    else:
      subject=NOTIFICATIONTYPE+u': O serviço ['+SERVICEDESC+'] do elemento de rede ['+HOSTNAME+'] foi restaurado'
      
except Exception,e:
  print e
  usage()
  sys.exit(1)
  
#  <br><img alt="" src="data:image/gif;base64,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

#acentuacoes nas mensagens:
replaces_body=[['Bbi','<b>'],
          ['Bbo','</b>'],
          ['ervico','ervi&ccedil;o'],
          ['dentificacao','dentifica&ccedil;&atilde;o'],          
          ['umero','&uacute;mero'],          
          ['olucoes','olu&ccedil;&otilde;es'],
          ['anutencao ','anuten&ccedil;&atilde;o '],
          ['isica ','&iacute;sica '],
          ['undancia','und&#226;ncia'],
          ['tecnica','t&#233;cnica'],
          ['atelite','at&#233;lite']
          ]
replaces_subject=[['ervico','erviço'],
          ['possivel','possível'],
          ['atelite','at&#233;lite']
          ]
for repla in replaces_body:
  if repla[0] in LONGSERVICEOUTPUT:LONGSERVICEOUTPUT=LONGSERVICEOUTPUT.replace(repla[0],repla[1])
for repla in replaces_subject:
  if repla[0] in SERVICEOUTPUT:SERVICEOUTPUT=SERVICEOUTPUT.replace(repla[0],repla[1])
for repla in replaces_body:
  if repla[0] in SERVICEDESC:SERVICEDESC=SERVICEDESC.replace(repla[0],repla[1])
#acentuacoes nas mensagens eof:
  
  
#calculo do tempofora
if tipomensagem=='service':
  filename_log='%s%s_%s_incidente_mail'.replace(' ','_').replace('$','_')%(pluginspath,HOSTNAME,SERVICEDESC)
  if 'RESOLVIDO' != NOTIFICATIONTYPE:
    if 'onlysm4rtsys' in LONGSERVICEOUTPUT:#se mensagem critica for so para grupo sys adiciona grupo no arquivo de tempo
      open(filename_log,'w').write(LASTSERVICECHECK+"onlysm4rtsys")
    else:
      open(filename_log,'w').write(LASTSERVICECHECK)
  start_time=open(filename_log,'r').read()
  if 'onlysm4rtsys' in start_time:#se log contiver sintax sys adiciona ao LONGSERVICEOUTPUT para que ele saiba que he uma notificacoa privilegiada
    start_time=start_time.replace('onlysm4rtsys','')
    if 'onlysm4rtsys' not in LONGSERVICEOUTPUT:
      LONGSERVICEOUTPUT+='onlysm4rtsys'
  end_time=LASTSERVICECHECK
else:
  filename_log='%s%s_%s_incidente_mail'.replace(' ','_').replace('$','_')%(pluginspath,HOSTNAME,SERVICEDESC)
  if 'RESOLVIDO' != NOTIFICATIONTYPE:
    open(filename_log,'w').write(LASTHOSTCHECK)
  start_time=open(filename_log,'r').read()
  end_time=LASTHOSTCHECK

tf=seconds_to_dhms(int(end_time)-int(start_time))
#tempofora="%d dia(s) %d hora(s) %d minuto(s) %s segundo(s)"
tempofora=''      
if tf[0]>0:tempofora+="%d dia(s) "%tf[0]
if tf[1]>0:tempofora+="%d hora(s) "%tf[1]
if tf[2]>0:tempofora+="%d minuto(s) "%tf[2]
if tf[3]>0:tempofora+="%d segundo(s) "%tf[3]
#calculo do tempofora eof  


if '-Alarmes-' in HOSTNAME:
  #if 'INCIDENTE' ==NOTIFICATIONTYPE:
  #subject=HOSTNAME+" : "+SERVICEOUTPUT.replace('Alarme:','').replace('OK -','')
  subject=SERVICEOUTPUT.replace('Alarme:','').replace('OK -','')
  #else:
    #subject=HOSTNAME+" : "+SERVICEOUTPUT
  
  if 'sys' != CONTACTADDRESS2 and 'sm4rtsysin' in LONGSERVICEOUTPUT and 'sm4rtsyseof' in LONGSERVICEOUTPUT:#limpa mensagem se nao fizer parte do grupo sys
    x1=LONGSERVICEOUTPUT.find('sm4rtsysin')+len('sm4rtsysin')
    x2=LONGSERVICEOUTPUT.find('sm4rtsyseof')
    LONGSERVICEOUTPUT=LONGSERVICEOUTPUT.replace(LONGSERVICEOUTPUT[x1:x2],'')
  LONGSERVICEOUTPUT=LONGSERVICEOUTPUT.replace('sm4rtsysin','').replace('sm4rtsyseof','')
  
  if 'sys' != CONTACTADDRESS2 and 'onlysm4rtsys' in LONGSERVICEOUTPUT:#impede que mensagem seja enviada a grupo diferente de sys
    logging.info("%s nao faz parte do grupo envio privilegiado %s"%(to,subject))
    sys.exit(1)
  subject=subject.replace('onlysm4rtsys','')
  LONGSERVICEOUTPUT=LONGSERVICEOUTPUT.replace('onlysm4rtsys','')

  if 'RESOLVIDO' in NOTIFICATIONTYPE:
    text="""<html><head><meta http-equiv="Content-Type" content="text/html; charset=iso-8859-1"></head>
    <body style="word-wrap: break-word; -webkit-nbsp-mode: space; -webkit-line-break: after-white-space; ">
    <div><span>"""
    text+="<div><b><font size=\"4\">O tempo de indisponibilidade foi de:&nbsp;</font></b>"+tempofora
    if 'check:' in LONGSERVICEOUTPUT:
      text+="""<br><br><b><font size="4">Data da gera&ccedil;&atilde;o do alarme:</font></b>&nbsp;"""+LONGSERVICEOUTPUT.split('check:')[1].split('div style=')[0]
    text+="""<br></body></html>"""
      
    mail(IPSMTPSRV, USERMAIL, SENHAMAIL,subject,text,tlsvar,to)
    sys.exit(0)
  else:
    text="""<html><head><meta http-equiv="Content-Type" content="text/html; charset=iso-8859-1"></head>
      <body style="word-wrap: break-word; -webkit-nbsp-mode: space; -webkit-line-break: after-white-space; ">
      <div><span><font size="4">"""
    if 'check:' in LONGSERVICEOUTPUT:
      text+=LONGSERVICEOUTPUT.split('check:')[0].replace('\\n','<br>')+"</font>"
      text+="""<br><br><b><font size="4">Data da gera&ccedil;&atilde;o do alarme:</font></b>&nbsp;"""+LONGSERVICEOUTPUT.split('check:')[1].split('div style=')[0]
    else:
      text+=LONGSERVICEOUTPUT.split('div style=display')[0].replace('\\n','<br>')+"</font>"
    text+="""<br></body></html>"""
      
    mail(IPSMTPSRV, USERMAIL, SENHAMAIL,subject,text,tlsvar,to)
    sys.exit(0)
    

    
try:
  if tipomensagem=='service':
    #if '<br>' in COMBO:
    #  s=''
    #  for x in COMBO.split('<br>'):
    #    if len(x)==10:
    #      s+=datetime.datetime.fromtimestamp(int(x)).strftime('%Y-%m-%d %H:%M:%S')
    #    else:
    #      s+=x
    #    s+='<br>'
    #  COMBO=s      
    if 'DOWN' == HOSTSTATE:sys.exit(0)#se o host tiver fora nao notifica servicos
    #text    
    #print filename_log,NOTIFICATIONTYPE,LASTSERVICECHECK
    if NOTIFICATIONTYPE=='INCIDENTE':#com problema
      
      #print filename_log,NOTIFICATIONTYPE,LASTSERVICECHECK

      
      
      #sys.exit(1)
      text="""<html><head><meta http-equiv="Content-Type" content="text/html; charset=iso-8859-1"></head>
              <body style="word-wrap: break-word; -webkit-nbsp-mode: space; -webkit-line-break: after-white-space; ">
              <div><span>
              <b><font size="4">Tipo do Alerta:</font></b>"""+NOTIFICATIONTYPE+"""
              <br><br><br>
              <b><font size="4">Servi&ccedil;o:</font></b>
              <br><br>
              <b><i>Alerta identificado:</i><font size=3D"4">&nbsp;</font></b>"""+alerta+"""</div>
              <b><i>Poss&#237;veis causas:</i><font size=3D"4">&nbsp;</font></b>"""+causas+"""</div>
              <b><i>Mensagem t&#233;cnica do servi&ccedil;o:</i><font size=3D"4">&nbsp;</font></b><<<i>"""+SERVICEOUTPUT+"""</i>>></div>
              <div><b><i>Nome do servi&ccedil;o com problema</i>:&nbsp;</b>"""+SERVICEDESC+"""</div><div>
              <br></div><div><br></div>
              <div><b><font size="4">Este servi&ccedil;o pertence ao elemento:</font></b>
              <br><br><b><i>Nome do elemento de rede:</i></b> """+HOSTNAME+"""&nbsp;</div>
              <div><b><i>Endere&ccedil;o IP: </i></b>"""+HOSTADDRESS+"""&nbsp;</div>
              <div><b><i>Status:</i></b>"""+HOSTSTATE+""" &nbsp; &nbsp;</div>
              <div><b><i>Desempenho do elemento:&nbsp;</i></b>"""+HOSTOUTPUT+"""</div>
              </span></div>
              <bre>
              <br></body></html>"""
    else:
        #resolvido
      #print filename_log,NOTIFICATIONTYPE,LASTSERVICECHECK

      text="""<html><head><meta http-equiv="Content-Type" content="text/html; charset=iso-8859-1"></head>
        <body style="word-wrap: break-word; -webkit-nbsp-mode: space; -webkit-line-break: after-white-space; ">
        <div><span>
        <b><font size="4">Tipo do Alerta:</font></b>&nbsp;"""+NOTIFICATIONTYPE+"""
        <br><br><br>
        <b><font size="4">Servi&ccedil;o:</font></b>
        <br><br><b>
        <i>Aviso de retorno:</i><font size=3D"4">&nbsp;</font></b><<<i>"""+SERVICEOUTPUT+"""</i>>></div>
        <div><b><i>Nome do servi&ccedil;o restaurado:</i>&nbsp;</b>"""+SERVICEDESC+"""</div><div>
        <br></div><div><br></div>
        <div><b><font size="4">Este servi&ccedil;o pertence ao elemento:</font></b>
        <br><br><b><i>Nome do elemento de rede:</i></b> """+HOSTNAME+"""&nbsp;</div>
        <div><b><i>Endere&ccedil;o IP: </i></b>"""+HOSTADDRESS+"""&nbsp;</div>
        <div><b><i>Status:</i></b>"""+HOSTSTATE+""" &nbsp; &nbsp;</div>
        <div><b><i>Desempenho do elemento:&nbsp;</i></b>"""+HOSTOUTPUT+"""</div>
        <div><b><i>Tempo fora:&nbsp;</i></b>"""+tempofora+"""
        </span></div>
        <br>
        <br></body></html>"""
# 
    
  else:
    if NOTIFICATIONTYPE=='INCIDENTE':#com problema
      text="""<html><head><meta http-equiv="Content-Type" content="text/html; charset=iso-8859-1"></head>
  <body style="word-wrap: break-word; -webkit-nbsp-mode: space; -webkit-line-break: after-white-space; ">
  <div><span>
  <b><font size="4">Tipo do Alerta:</font></b>&nbsp;"""+NOTIFICATIONTYPE+"""
  <br><br><br>
  <b><i>Alerta identificado:</i></b><font size="4">&nbsp;</font></b><<<i>"""+HOSTOUTPUT+"""</i>>></div>
  <br></div><div><br></div>
  <div><b><font size="4">Elemento de rede impactado:</font></b>
  <br><br><b><i>Nome do elemento de rede:</i></b> """+HOSTNAME+"""&nbsp;</div>
  <div><b><i>Endere&ccedil;o IP: </i></b>"""+HOSTADDRESS+"""&nbsp;</div>
  <div><b><i>Status:</i></b>"""+HOSTSTATE+""" &nbsp; &nbsp;</div>
  </span></div>
  <br>
  <br></body></html>"""
    else:#resolvido
      text="""<html><head><meta http-equiv="Content-Type" content="text/html; charset=iso-8859-1"></head>
  <body style="word-wrap: break-word; -webkit-nbsp-mode: space; -webkit-line-break: after-white-space; ">
  <div><span>
  <b><font size="4">Tipo do Alerta:</font></b>&nbsp;"""+NOTIFICATIONTYPE+"""
  <br><br><br>
  <b><i>Aviso de retorno:</i></b><font size="4">&nbsp;</font></b><<<i>"""+HOSTOUTPUT+"""</i>>></div>
  <br></div><div><br></div>
  <div><b><font size="4">Elemento de rede que foi impactado:</font></b>
  <br><br><b><i>Nome do elemento de rede:</i></b> """+HOSTNAME+"""&nbsp;</div>
  <div><b><i>Endere&ccedil;o IP: </i></b>"""+HOSTADDRESS+"""&nbsp;</div>
  <div><b><i>Status:</i></b>"""+HOSTSTATE+""" &nbsp; &nbsp;</div>
  <div><b><i>Tempo fora:&nbsp;</i></b>"""+tempofora+"""
  </span></div>
  <br>
  <br></body></html>"""
      
      
except Exception,e:
  print e
  usage()
  sys.exit(1)
  
mail(IPSMTPSRV, USERMAIL, SENHAMAIL,subject,text,tlsvar,to)

  

