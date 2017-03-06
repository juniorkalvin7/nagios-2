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
import sys,urllib,urllib2,re,cookielib,os

#Plugin para captura de informacoes do Radio Motorola CANOPY 10.3 BH-DES

def tent1():
  try:
    if infor=='link':
      upower=re.findall('LocalPowerLevel\'>(.+?)</span>\r\n dBm',data)[0]
      ujitter=re.findall('id=\'LocalJitter\'>(.+?)</span>',data)[0]
      dpower=re.findall('id=\'RemotePowerLevel\'>(.+?)</span>',data)[0]
      djitter=re.findall('id=\'RemoteJitter\'>(.+?)</span>',data)[0]
      if int(upower) >= limit_sensrec or int(dpower) >= limit_sensrec:
        print 'CRITICAL - SIGNAL - Power Level :Up %sdBm Jitter %s, Down %sdBm Jitter %s|upower=%sdBm;ujitter=%s;dpower=%sdBm;djitter=%s;;' % (
          upower,ujitter,dpower,djitter,\
          upower.replace('-',''),ujitter,dpower.replace('-',''),djitter)
        sys.exit(2)
      elif int(ujitter) >= limit_jitter or int(djitter) >= limit_jitter:
        print 'CRITICAL - JITTER - Power Level :Up %sdBm Jitter %s, Down %sdBm Jitter %s|upower=%sdBm;ujitter=%s;dpower=%sdBm;djitter=%s;;' % (
          upower,ujitter,dpower,djitter,\
          upower.replace('-',''),ujitter,dpower.replace('-',''),djitter)
        sys.exit(2)
      else:
        print 'Power Level :Up %sdBm Jitter %s, Down %sdBm Jitter %s|upower=%sdBm;ujitter=%s;dpower=%sdBm;djitter=%s;;' % (
          upower,ujitter,dpower,djitter,\
          upower.replace('-',''),ujitter,dpower.replace('-',''),djitter)      
    elif infor=='ber':
      ber=re.findall('id=\'RemoteBERResults\'>(.+?)</span>',data)[0]
      #print 'BER Results:%s Jitter %s|uplink=%sdBm;ujiter=%s;;' % (
      print 'BER Results %s|ber=%s;' % (ber,ber.split('-')[0])
  except:
    tent2()
def tent2():
  try:
    if infor=='link':
      upower=re.findall('RemotePowerLevel\'>(.+?)</span>\r\n dBm',data)[0]
      ujitter=re.findall('id=\'RemoteJitter\'>(.+?)</span>',data)[0]
      dpower=re.findall('id=\'PowerLevelCurrent\'>(.+?)</span>',data)[0]
      dpower=dpower.replace(' dBm','')
      djitter=re.findall('id=\'JitterCurrent\'>(.+?)</span>',data)[0]
      
      if int(upower) >= limit_sensrec or int(dpower) >= limit_sensrec:
        print 'CRITICAL - SIGNAL - Power Level :Up %sdBm Jitter %s, Down %sdBm Jitter %s|upower=%sdBm;ujitter=%s;dpower=%sdBm;djitter=%s;;' % (
          upower,ujitter,dpower,djitter,\
          upower.replace('-',''),ujitter,dpower.replace('-',''),djitter)
        sys.exit(2)
      elif int(ujitter) >= limit_jitter or int(djitter) >= limit_jitter:
        print 'CRITICAL - JITTER - Power Level :Up %sdBm Jitter %s, Down %sdBm Jitter %s|upower=%sdBm;ujitter=%s;dpower=%sdBm;djitter=%s;;' % (
          upower,ujitter,dpower,djitter,\
          upower.replace('-',''),ujitter,dpower.replace('-',''),djitter)
        sys.exit(2)
      else:
        print 'Power Level :Up %sdBm Jitter %s, Down %sdBm Jitter %s|upower=%sdBm;ujitter=%s;dpower=%sdBm;djitter=%s;;' % (
          upower,ujitter,dpower,djitter,\
          upower.replace('-',''),ujitter,dpower.replace('-',''),djitter)    
      
    elif infor=='ber':
      ber=re.findall('id=\'LocalBERResults\'>(.+?)</span>',data)[0]
      print 'BER Results %s|ber=%s;' % (ber,ber.split('-')[0])
  except Exception,e:
    print 'CRITICAL - Erro grave',e
    sys.exit(2)

    
args = sys.argv[1:]

limit_term=75
limit_sensrec=80
limit_jitter=4
"""
  (0) OK
  (1) WARNING
  (2) CRITICAL
  (3)UNKNOWN
"""
if len(args) != 4:
  print "Local Centreon Plugin\t\t\tpor GemayelLira\nCaptura informacoes de Radio CANOPY Motorola\nvercoes suportadas:10.3 BH-DES\n"
  print "Argumentos:host usuario senha informacao"
  print "Tipos de informacao:temperatura,link,ber"
  print "Ex.\n"+os.getcwd()+"/%s 192.168.3.177 root @ps3s#177 temperatura" % sys.argv[0] 
  sys.exit(1)
else:
  host=args[0]
  usuario=args[1]
  senha=args[2]
  infor=args[3]
  
cj = cookielib.CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
url="http://"+host+"/login.cgi"
values = {'CanopyUsername': usuario,\
          'CanopyPassword': senha,\
          'login' : 'Login',\
          'webguisubmit' : 'submit'}
data = urllib.urlencode(values)
req = urllib2.Request(url,data)
try:
  data = urllib2.urlopen(req).read()
except:
  print 'CRITICAL ERROR - provavel senha incorreta'
  sys.exit(2)
sessao=re.findall('pageindex=0&amp;Session=(.+?)">Copyright',data)[0]
esn=re.findall('mac_esn=(.+?)&amp;',data)[0]
url = "http://"+host+"/main.cgi?mac_esn="+sessao
data = opener.open(url).read()
if infor=='temperatura':
  temperatura=re.findall('id=\'boxTemperatureC\'>(.+?)</span>\r\n &deg',data)[0]
  if int(temperatura) >= limit_term:
    print 'CRITICAL - TEMP - Temperatura sensor : %sC|temperatura=%sC;;'%(temperatura,temperatura)
    sys.exit(2)
  else:
    print 'Temperatura sensor : %sC|temperatura=%sC;;'%(temperatura,temperatura)
  #print 'Temperatura sensor : %sC|temperature=%sC;30;40;;'%(temperatura,temperatura)
  sys.exit(0)

url='http://'+host+'/main.cgi?mac_esn='+esn+'&catindex=3&pageindex=22&Session='+sessao
#print 'abrindo pagina',url
data = opener.open(url).read()
tent1()

sys.exit(0)
