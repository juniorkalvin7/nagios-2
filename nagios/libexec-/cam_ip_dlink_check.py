#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys,base64,os
from socket import *

args = sys.argv[1:]

class Portcheck:
  def __init__(self, host,port):
    self.host = host
    self.port = int(port)
    self.socket = setdefaulttimeout(30)
    self.sd = socket(AF_INET, SOCK_STREAM)
  def run(self):
    try:
      self.sd.connect((self.host, self.port))
      self.sd.close()
      return True
    except:
      return False
if len(args) < 3:
  print "Verificador de Camera IP D-Link\t\t\tpor GemayelLira\nVerifica Conectividade e Captura Imagem da Camera em tempo real\n"
  print "Argumentos:host usuario senha"
  print 'Obs:Caso senha em branco coloque none'
  print "Ex.\n"+os.getcwd()+"/%s 192.168.0.95 admin" % sys.argv[0] 
  sys.exit(1)
else:
  host=args[0]
  usuario=args[1]
  if args[2]=='none':
    senha=''
  else:
    senha=args[2]
  
http_auth=base64.b64encode('%s:%s'%(usuario,senha))
if Portcheck(host,80).run():
  print 'OK - Acesso ao video|ok=1'
  payload="""$opts = array(
  'http'=>array(
    'method'=>"GET",
    'header'=>"Accept-language: en-US,en;q=0.5\r\n" .
              "Cookie: MP_MODE=1\r\n" .
              "Authorization: Basic """+http_auth+"""\r\n"
  )
);
$context = stream_context_create($opts);
$file = file_get_contents('http://"""+host+"""/dms', false, $context);
$str= base64_encode($file);
"""
  print 'Eva:%s'%base64.b64encode(payload)
else:
  print 'CRITICAL - Acesso ao video porta fechada|ok=0'
  sys.exit(2)

  