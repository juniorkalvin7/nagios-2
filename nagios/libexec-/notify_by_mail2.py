#!/usr/bin/python

import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email import Encoders
import os,sys,getopt,datetime
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
 * THIS SOFTWARE IS PROVIDED BY THE NETBSD FOUNDATION, INC. AND CONTRIBUTORS
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
"""
./notify_by_mail2.py -z 1 -s 200.253.157.14 -u "monitoramento@intechne.com.br" -p labsecur1t1 -c "gemayel@intechne.com.br" -o "$HOSTSTATE$" -n "$NOTIFICATIONTYPE$" -h "$HOSTNAME$" -d "$SERVICEDESC$" -e "$SERVICESTATE$" -t "$SERVICEOUTPUT$" -a "$HOSTADDRESS$" -q "$HOSTOUTPUT$"


$USER1$/notify_by_mail.py -z 1 -s 200.253.157.14 -u "monitoramento@intechne.com.br" -p labsecur1t1 -o "$HOSTSTATE$" -n "$NOTIFICATIONTYPE$" -h "$HOSTNAME$" -d "$SERVICEDESC$" -e "$SERVICESTATE$" -t "$SERVICEOUTPUT$" -a "$HOSTADDRESS$" -q "$HOSTOUTPUT$"
$USER1$/notify_by_mail.py -z 1 -s 201.18.32.29 -u "suporte@saude.ma.gov.br" -p Sup0rtE2@@9 -o "$HOSTSTATE$" -n "$NOTIFICATIONTYPE$" -h "$HOSTNAME$" -d "$SERVICEDESC$" -e "$SERVICESTATE$" -t "$SERVICEOUTPUT$" -a "$HOSTADDRESS$" -q "$HOSTOUTPUT$"
$USER1$/notify_by_mail.py -z 0 -s 189.16.255.180 -u "suportesemit@saoluis.ma.gov.br" -p 1ntechne -o "$HOSTSTATE$" -n "$NOTIFICATIONTYPE$" -h "$HOSTNAME$" -d "$SERVICEDESC$" -e "$SERVICESTATE$" -t "$SERVICEOUTPUT$" -a "$HOSTADDRESS$" -q "$HOSTOUTPUT$"

python notify_by_mail.py -z 1 -s 201.18.32.29 -u "suporte@saude.ma.gov.br" -p Sup0rtE2@@9 -to "" -o HOSTSTATE -n NOTIFICATIONTYPE -h HOSTNAME -d "SERVICEDESC opcoes" -e SERVICESTATE -t SERVICEOUTPUT -a 10.0.0.1 -q "HOSTOUTPUT segunda via"
python notify_by_mail.py -z 1 -s 200.253.157.14 -u "monitoramento@intechne.com.br" -p labsecur1t1 -o HOSTSTATE -n NOTIFICATIONTYPE -h HOSTNAME -d "SERVICEDESC opcoes" -e SERVICESTATE -t SERVICEOUTPUT -a 10.0.0.1 -q "HOSTOUTPUT segunda via"
python notify_by_mail.py -z 0 -s 189.16.255.180 -u "suportesemit@saoluis.ma.gov.br" -p 1ntechne -o HOSTSTATE -n NOTIFICATIONTYPE -h HOSTNAME -d "SERVICEDESC opcoes" -e SERVICESTATE -t SERVICEOUTPUT -a 10.0.0.1 -q "HOSTOUTPUT segunda via"
"""

def mail(IPSMTPSRV, USERMAIL, SENHAMAIL,subject,text,tlsvar,to):
  #to='suporte@intechne.com.br'
  #to='samuel@intechne.com.br'
  if ':' in to:
    toto = to.split(':')
    for to in toto:
      msg = MIMEMultipart()
      msg['From'] = USERMAIL
      msg['To'] = to
      msg['Subject'] = subject
      msg.attach(MIMEText(text))
      mailServer = smtplib.SMTP(IPSMTPSRV, 25)
      mailServer.ehlo()
      if tlsvar=='1':
        mailServer.starttls()
        mailServer.ehlo()
      mailServer.login(USERMAIL, SENHAMAIL)
      mailServer.sendmail(USERMAIL, to, msg.as_string())
      mailServer.close()
  else:
    to=to
    msg = MIMEMultipart()
    msg['From'] = USERMAIL
    msg['To'] = to
    msg['Subject'] = subject
    msg.attach(MIMEText(text))
    mailServer = smtplib.SMTP(IPSMTPSRV, 25)
    mailServer.ehlo()
    if tlsvar=='1':
      mailServer.starttls()
      mailServer.ehlo()
    mailServer.login(USERMAIL, SENHAMAIL)
    mailServer.sendmail(USERMAIL, to, msg.as_string())
    mailServer.close()

def usage():
  print 'Modo de uso\n\
python notify_by_mail2.py\n\
  -z 1 or 0 se o servidor usa autenticacao tls\n\
  -s $IPSMTPSRV ip do servidor de email\n\
  -u $USERMAIL usuario do email\n\
  -p $SENHAMAIL senha do email\n\
  -c $email da pessoa\n\
  -o $HOSTSTATE$ variavelis abaixo sao do NAGIOS\n\
  -n "$NOTIFICATIONTYPE$" \n\
  -h "$HOSTNAME$" \n\
  -d "$SERVICEDESC$" \n\
  -e "$SERVICESTATE$" \n\
  -t "$SERVICEOUTPUT$" \n\
  -b "$HOSTOUTPUT$" \n\
  -a "$HOSTADDRESS$" \n\
   -q "$HOSTOUTPUT$" \n'

#print len(sys.argv)
#if not len(sys.argv) == 23:
  #usage()
  #sys.exit()

try:
  options = getopt.getopt(sys.argv[1:], 'z:s:u:p:c:o:n:h:d:e:t:a:q:')[0]
except getopt.GetoptError, err:
  print err
  usage()
  sys.exit()
for option, value in options:
  print option,value
  if option == '-z':
    tlsvar  = value
  if option == '-s':
    IPSMTPSRV  = value
  if option == '-u':
    USERMAIL  = value
  if option == '-p':
    SENHAMAIL  = value      
  if option == '-c':
    to  = value      
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
  #print option,value
#sys.exit(1)
try:
  
  subject='Host '+HOSTSTATE+' Alerta para '+HOSTNAME+' monitoramento'
  text="\
  Tipo:"+NOTIFICATIONTYPE+"\n\
  Host: "+HOSTNAME+"\n\
  Descricao de Servico:"+SERVICEDESC+"\n\
  Status do Host: "+HOSTSTATE+"\n\
  "+SERVICESTATE+"\n\
  Address: "+HOSTADDRESS+"\n\
  Info: "+HOSTOUTPUT+"\n\
  "+SERVICEOUTPUT
  #print subject
  #print text
except Exception,e:
  print e
  usage()
  sys.exit(1)
#192.168.0.70_InfoCRITICAL-HostUnreachable192.168.0.70
#nao =0
#try:
  #nomefiletmp='/var/lib/centreon/centplugins/alert_%s_%s_%s' %(HOSTADDRESS,SERVICEDESC,HOSTSTATE)
  #nomefiletmp = nomefiletmp.replace(')','').replace('(','').replace(':','').replace(' ','_').replace('$','1')
  #tempo = open(nomefiletmp,'r').read()
  #atual = datetime.datetime(int(tempo.split()[0].split("-")[0]),\
                            #int(tempo.split()[0].split("-")[1]),\
                            #int(tempo.split()[0].split("-")[2]),\
                            #int(tempo.split()[1].split(":")[0]),\
                            #int(tempo.split()[1].split(":")[1]),\
                            #int(tempo.split()[1].split(":")[2].split(".")[0]),\
                            #int(tempo.split()[1].split(":")[2].split(".")[1]))


  #resultado = atual-datetime.datetime.now() + datetime.timedelta(days=1)
  #if ''.join(str(resultado)).count("-7 day"):
    ##print 'passou uma semana'
    #os.system('echo "passou uma semana %s ">> /tmp/lognotfy.log' % ''.join(str(resultado)))
    #os.system('echo removendo %s >> /tmp/lognotfy.log' % nomefiletmp)
    #os.system('rm -rf %s' % nomefiletmp)
  #else:
    ##print 'nao passou uma semana'
    #os.system('echo nao passou uma semana %s >> /tmp/lognotfy.log' % HOSTNAME)

    #nao=1
#except Exception,e:
  ##print 'nao existe criando.'
  #os.system('echo nao existe criando %s >> /tmp/lognotfy.log' % e)

  #nao=0
  #timeatual=''.join(str(datetime.datetime.now()))
  #open(nomefiletmp,'w').write(timeatual)

#if nao==0:
mail(IPSMTPSRV, USERMAIL, SENHAMAIL,subject,text,tlsvar,to)
  #print 'Email enviado'
  #os.system('echo Email enviado %s >> /tmp/lognotfy.log' % HOSTNAME)

#else:
  ##print 'nao enviar'
  #os.system('echo nao enviar >> /tmp/lognotfy.log')

  
  
  
