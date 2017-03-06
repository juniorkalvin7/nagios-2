#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re,urllib2,sys,time,datetime
import socket

"""
sys.exit(0) OK
sys.exit(1) WARNING
sys.exit(2) CRITICAL
sys.exit(3)UNKNOWN
"""

def linksparser(url,dados):
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

if len(args)<1 or args[0].count('help'):
  print "Centreon Plugin\nLocal Check Tempo de abertura de paginas GemayelLira"
  print "proxy e timeout nao sao obrigatorios"
  print "Argumentos:url proxy timeout"
  print "Ex.\n%s http://189.23.232.246/ 10.0.0.45:81 timeout" % sys.argv[0] 
  sys.exit(1)
else:
  url=args[0]
  try:
    proxy=args[1]
    if ':' not in proxy:
      try:
        timeout=int(proxy)
        proxy='sem'
      except:
        proxy='sem'
  except:
    proxy='sem'
  try:
    if proxy!='sem':
      timeout=int(args[2])
  except:
    timeout=15
  if proxy != 'sem':
    logfile='http_%s_proxy_%s.log' % (url.split('//')[1].split('/')[0],proxy.replace(':','_'))      
  else:
    logfile='http_%s.log' % url.split('//')[1].split('/')[0]
    

try:
  socket.timeout(timeout)
except:
  timeout=15
  socket.timeout(timeout)


head2=''

t = datetime.datetime.now()
tempo1=time.mktime(t.timetuple())+(t.microsecond/1000000.)

if proxy.count(':'):
  http_proxy = urllib2.ProxyHandler({"http" : "http://%s" % proxy}) #PARA PROXY NO PROGRAMA
  opener = urllib2.build_opener(http_proxy)
  head2= ' Usando Proxy:%s ' % proxy
elif proxy ==  'sem':
  opener = urllib2.build_opener()
else:
  print 'CRITICAL - PROXY ERROR', proxy
  sys.exit(1)
  
opener.addheaders = [('User-agent', 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)')]
ok=0
sinal=3
try:
  dados = opener.open(url,timeout=timeout).read()
  #print '\nDIRETORIO/ARQUIVO EXISTE, %s' % url
  head='OK - ACESSO HTTP '
  ok=1
  sinal=0
except urllib2.HTTPError, e:
  if e.code == 110:
    #print "\nacesso negado %s"  % self.url
    head='CRITICAL - TIMEOUT '
    sinal=2
  elif e.code == 111:
    #print "\nacesso negado %s"  % self.url
    head='CRITICAL - ACESSO NEGADO FW OU CONECTIVIDADE '
    sinal=2
  elif e.code == 403:
    #print "\nacesso negado %s"  % self.url
    head='CRITICAL - ACESSO NEGADO '
    sinal=2
  elif e.code == 104:
    #print "\nconexao reiniciada pelo host %s " % url
    head='CRITICAL - CONEXAO REINICIADA PELO HOST '
    sinal=2
  elif e.code == 504:
    #print "\nGateway Timeout 504 %s" % url
    head='CRITICAL - TIMEOUT '
    sinal=3
  else:
    head='CRITICAL - ERRO DESCONHECIDO 1 %s' % e
    sinal=3
  dados=''
except urllib2.URLError,e:
  if e[0][0] == 110:
    #print "\nacesso negado %s"  % self.url
    head='CRITICAL - TIMEOUT '
    sinal=2
  elif e[0][0] == 111:
    #print "\nacesso negado %s"  % self.url
    head='CRITICAL - ACESSO NEGADO FW OU CONECTIVIDADE '
    sinal=2
  else:
    head= "CRITICAL - ERRO DESCONHECIDO 2 %s" % e
  dados=''
except Exception,e:
  head='CRITICAL - TIMEOUT - %s' % e
  sinal=2
  dados=''
  


linkes=linksparser(url,dados)
for i in linkes:
  try:
    opener.open(i).read()
  except:pass
  
t = datetime.datetime.now()
tempo2=time.mktime(t.timetuple())+(t.microsecond/1000000.)
diferenca=tempo2-tempo1
mensagem = head+head2+'- resposta em %0.3f mile segundos %d objetos acessados|time=%0.6fs;;;0.000000 ok=%d'  % (diferenca,len(linkes)+1,diferenca,ok)
mensagem+='\nAcessado %s' % url
print mensagem
print "timeout,%d"%timeout
open('/tmp/%s' % logfile ,'w').write(mensagem)
sys.exit(sinal)
