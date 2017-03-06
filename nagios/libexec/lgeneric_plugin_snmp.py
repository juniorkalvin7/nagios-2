#!/usr/bin/env python
# -*- coding: utf-8 -*-


from socket import *
import sys,commands,re,zlib,base64

"""
rev:6dec13
adicionado novo padrao para mensagens ALARME tipo == CRITICAL
rev:26nov13
leitura de quebra de linha ao ver <br> ele adiciona quebra de linha
rev:22nov13
adicionado novo padrao para mensagens Alarme tipo == CRITICAL
rev:2aug13
adicionado verificacao de string se contiver "can't open" alerta
rev:27jun12
adicionado verificacao da funcao self.lersnmp() alertar


"""


class genericplugin(object):
  def __init__(self, ip,community,mib,mibCompleto):
    self.ip=ip
    self.community=community
    self.mib=mib
    self.vezes=0
    self.signal=0
    self.outputs=''
    self.mibCompleto=mibCompleto
  def lersnmp(self):
    if self.mibCompleto==False:
      self.comando="/usr/bin/snmpwalk -v 1 -c %s %s %s.101.1" %(self.community,str(self.ip),self.mib)
    else:
      self.comando="/usr/bin/snmpwalk -v 1 -c %s %s %s" %(self.community,str(self.ip),self.mib)
      
    try:
      self.outputs=(commands.getoutput(self.comando))
      self.outputs=self.outputs.split("\"")[1]
    except:
      self.comando="/usr/bin/snmpwalk -v 1 -c %s %s %s" %(self.community,str(self.ip),self.mib)
      self.outputs=(commands.getoutput(self.comando))
      data = self.outputs.replace('\n','quebra')
      #print self.output
      maior=0
      for x in re.findall('= STRING:(.+?)%s'%mib[-8:],data):
        #print x
        if len(x) > maior:
          maior = len(x)
          corpo=x
      
      corpo = corpo.split('quebra')
      corpo = corpo[:-1]
      corpo = "".join(corpo)
      corpo = corpo.replace('"','')

      try:
        corpo=zlib.decompress(base64.decodestring(corpo).rstrip())
      except:
        pass
      self.outputs=corpo
                
      if self.vezes==3:
        print 'CRITICAL ERROR - em capturar informacao 3x'
        sys.exit(1)
      elif self.vezes!=0:
        self.lersnmp()
  def run(self):
    try:
      self.lersnmp()
    except:
      self.outputs='CRITICAL - Erro ao ler valor verifique o comando manualmente\n'+self.comando
    self.outputs=self.outputs.replace('<br>','\n')
    if self.outputs.count('CRITICAL'):self.signal=2
    elif 'ALARME:' in self.outputs and not "OK - " in self.outputs:self.signal=2
    elif 'Alarme:' in self.outputs and not "OK - " in self.outputs:self.signal=2
    elif self.outputs.count('WARNING'):self.signal=1
    elif self.outputs.count('UNKNOWN'):self.signal=3
    elif self.outputs.count("can't open"):self.signal=2
    elif self.outputs.count("No such file or directory"):self.signal=2
    elif self.outputs.count("No such file or directory"):self.signal=2
    elif self.outputs.count("/usr/local/"):self.signal=2
    
    self.output()
    
  def output(self):
    """
    Tipos de saida: 
    0 ok
    2 critical
    1 warning
    3 unknown
    """
    print '%s' % (self.outputs)
    sys.exit(self.signal)
    

if __name__ == "__main__":
  args = sys.argv[1:]
  if len(args)<2:
    print "Centreon Plugin\nGetSnmp Info 3.0 por GemayelLira rev:27jun12"
    print "Argumentos:\npython ./%s IP community MIB" % sys.argv[0]
    print "Mib Exata:\npython ./%s IP community c MIB" % sys.argv[0]
    #print "Ex.\npython ./%s 201.65.222.194 u3fr0I9b5 .1.3.6.1.4.1.2022.11" % sys.argv[0] 
    sys.exit(1)
  else:
    ip=args[0]
    community=args[1]
    mib=args[2]
    if mib=='c':
      mib=args[3]
      mibCompleto=True
    else:mibCompleto=False

  genericplugin(ip,community,mib,mibCompleto).run()

