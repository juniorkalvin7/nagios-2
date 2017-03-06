#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib2
import urllib
import time
import datetime
import cookielib
import re
import socket

import sys
#gemayellira IMF!
class Portcheck:
  def __init__(self, host,port):
    self.host = host
    self.port = port
    self.socket = socket.setdefaulttimeout(20)
    self.sd = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  def run(self):
    try:
      self.sd.connect((self.host, self.port))
      res="OK - %s:%d OPEN|ok=1" % (self.host, self.port)
      self.sd.close()
      return res
    except: 
      res="CRITICAL - %s:%d CLOSED|ok=0" % (self.host, self.port)
      #sys.exit(1)
      return res
      #pass

def timecalc(t):#calculo de tempo
  min=(int(t)/60)
  sec=int(t-(min*60))
  return "%d min %d sec" % (min,sec)

def linksparser(url,dados):#parser gera link de objetos
  data=dados.split('\n')
  if url.count('https'):
    path='https://'+re.findall('//(.+?)/',url)[0]+'/'
  else:
    path='http://'+re.findall('//(.+?)/',url)[0]+'/'
  #path='http://www.saoluis.ma.gov.br/'
  #data = urllib.urlopen(url).read().split('\n')
  links=[]
  for i in data:
    if i.count('<script ') or i.count('<img ') or i.count('<input '):
      links+=re.findall('src=\"(.+?)"',i)
      links+=re.findall('src=\'(.+?)\'',i)
    if i.count('<link '):
      links+=re.findall('href=\"(.+?)"',i)
      links+=re.findall('href=\'(.+?)\'',i)
    if i.count('<param '):
      for x in re.findall('value=\"(.+?)"',i):
        if x.count('/'):links.append(x)
      for x in re.findall('value=\'(.+?)\'',i):
        if x.count('/'):links.append(x)
  linksf=[]
  for i in links:
    if 'http' not in i:
      linksf.append(path+i)
    else:
      linksf.append(i)
  return linksf

args = sys.argv[1:]
head2=''
if len(args)<1 or args[0].count('help'):
  print "Centreon Plugin\nCaptura tempo de acesso ao relatorio de estoque por GemayelLira"
  print "IP informado deve ser do stok, proxy nao obrigatorio"
  print "Argumentos:ip proxy"
  print "Ex.\n%s 172.16.2.66 10.0.0.45:81" % sys.argv[0] 
  sys.exit(1)
else:
  ip=args[0]
  try:
    proxy=args[1]
    if 'sem' in proxy:proxy=False
  except:
    proxy=False
    
cj = cookielib.CookieJar()
if proxy==True:
  try:
    http_proxy = urllib2.ProxyHandler({"http" : "http://%s" % proxy}) #PARA PROXY NO PROGRAMA
    head2= ' Usando Proxy:%s ' % proxy
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj),http_proxy)
  except:
    print 'CRITICAL - PROXY ERROR', proxy
    sys.exit(1)
else:
  opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))

urllib2.install_opener(opener)

t = datetime.datetime.now()
tempo_inicial=time.mktime(t.timetuple())+(t.microsecond/1000000.)

res=Portcheck(ip,8080).run()
if res.count('CRITICAL'):
  print res
  sys.exit(1)

#redirect inicial da pagina de login
url1='http://'+ip+':8080/stok/'
obj0=1
try:
  data = opener.open(url1).read()
except Exception,e:
  print 'CRITICAL ERROR - ',e,url1
  sys.exit(2)
linkes=linksparser(url1,data)
for i in linkes:
  
  try:
    obj0+=1
    opener.open(i).read()
  except:pass
  
t = datetime.datetime.now()
redir_inicial=time.mktime(t.timetuple())+(t.microsecond/1000000.)
redir_inicial_final=redir_inicial-tempo_inicial


#abertura da pagina de login
url='http://'+ip+':8080/stok/Logar.do'
obj1=1
try:
  data = opener.open(url).read()
except Exception,e:
  print 'CRITICAL ERROR - ',e,url
  sys.exit(2)
linkes=linksparser(url,data)
for i in linkes:
  
  try:
    obj1+=1
    opener.open(i).read()
  except:pass



t = datetime.datetime.now()
tempo_abertura_inicial=time.mktime(t.timetuple())+(t.microsecond/1000000.)
tempo_abertura_inicial_final=tempo_abertura_inicial-redir_inicial

#logando no sistema
url_inicial='http://'+ip+':8080/stok/Logar.do'
usuario='intechne'
senha='intechne'
values = {'login': usuario,\
          'password': senha,\
          'acao' : 'logar',\
          'x' : '40',\
          'y':'9'}
data = urllib.urlencode(values)
req = urllib2.Request(url_inicial,data)
try:
  data = urllib2.urlopen(req).read()
except Exception,e:
  print 'CRITICAL ERROR - ',e
  sys.exit(2)
linkes=linksparser(url_inicial,data)
obj2=1
for i in linkes:
  try:
    opener.open(i).read()
    obj2+=1
  except:pass
  
t = datetime.datetime.now()
tempo_login=time.mktime(t.timetuple())+(t.microsecond/1000000.)
tempo_login_final=tempo_login-tempo_abertura_inicial

#abrindo pagina de relatorio
url = "http://"+ip+":8080/stok/RSE.do"
req = urllib2.Request(url)
try:
  data = urllib2.urlopen(req).read()
except Exception,e:
  print 'CRITICAL ERROR - ',e,url
  sys.exit(2)
try:
  depositos=re.findall('name="depositos" value="(.+?)" ',data)
except Exception,e:
  print 'CRITICAL ERROR - nao consigo capturar numero de depositos',e
  sys.exit(2)
linkes=linksparser(url_inicial,data)
obj3=1
for i in linkes:
  try:
    opener.open(i).read()
    obj3+=1
  except:pass
t = datetime.datetime.now()
tempo_abertura_relatorio=time.mktime(t.timetuple())+(t.microsecond/1000000.)
tempo_abertura_relatorio_final=tempo_abertura_relatorio-tempo_login


#captura pdf
tempo = datetime.datetime.now().strftime("%d/%m/%Y")
values2="""acao=imprimir
&todos=on
&classificacaoPai=
&classificacao.id=
&insumo.descricao=
&insumo.id=
&d0.referencia=178&d0.date="""+tempo+"""
&inibirZerados=on"""
values={}
for x in values2.replace('\n','').split('&'):
  values[x.split('=')[0]]=x.split('=')[1]
post=urllib.urlencode(values)
for x in depositos:
  post+="&depositos=%s"%x
req = urllib2.Request(url,post)
timeout=15
socket.timeout(timeout)
try:
  data = urllib2.urlopen(req).read()
except Exception,e:
  print 'CRITICAL ERROR - ',e,url
  sys.exit(2)

t = datetime.datetime.now()
tempo_pdf=time.mktime(t.timetuple())+(t.microsecond/1000000.)
tempo_pdf_final=tempo_pdf-tempo_abertura_relatorio

total_tempos=tempo_pdf-tempo_inicial

#tempos
#pagina inicial
#pagina login
#pagina relatorio
#captura pdf
#total de tempos final

msg = head2+"Tempos de acesso Stok, redirecionamento  %0.2fs, inicial %0.2fs, login %0.2fs, relatorio %0.2fs, pdf %0.2fs, total %0.2fs|access1=%0.6fs;;;0.000000 access2=%0.6fs;;;0.000000 access3=%0.6fs;;;0.000000 access4=%0.6fs;;;0.000000 access5=%0.6fs;;;0.000000 total=%0.6fs;;;0.000000 " %\
    (redir_inicial_final,tempo_abertura_inicial_final,tempo_login_final,tempo_abertura_relatorio_final,tempo_pdf_final,total_tempos,redir_inicial_final,tempo_abertura_inicial_final,tempo_login_final,tempo_abertura_relatorio_final,tempo_pdf_final,total_tempos)
corpo="Acessos realizados em:%s\n" %url1
corpo+="Tempos de acesso a paginas:\n"
corpo+="Pagina Inicial redirecionamento em %0.3f segundos %d objetos\n"%(redir_inicial_final,obj0)
corpo+="Pagina Inicial acessada em %0.3f mile segundos %d objetos\n"%(tempo_abertura_inicial_final,obj1)
corpo+="Pagina Logon realizado em %0.3f mile segundos %d objetos\n"%(tempo_login_final,obj2)
corpo+="Pagina Acesso ao link relatorio em %0.3f mile segundos %d objetos\n"%(tempo_abertura_relatorio_final,obj3)
corpo+="Pagina Download pdf do relatorio em %0.3f mile segundos 1 objeto\n"%tempo_pdf_final
corpo+="Duracao total dos acessos em %s"%timecalc(total_tempos)

print msg
print corpo

