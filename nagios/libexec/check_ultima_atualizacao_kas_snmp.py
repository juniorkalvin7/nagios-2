#!/usr/bin/env python
# -*- coding: utf-8 -*-


from socket import *
import sys,commands,re,zlib,base64
import datetime


"""
rev:27jun12
adicionado verificacao da analisa_atualizacao self.lersnmp() alertar


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
    if self.outputs.count('CRITICAL'):self.signal=2
    elif self.outputs.count('WARNING'):self.signal=1
    elif self.outputs.count('UNKNOWN'):self.signal=3
    self.output()
    
  def output(self):
    """
    Tipos de saida: 
    0 ok
    2 critical
    1 warning
    3 unknown
    """
  #  print '%s' % (self.outputs)
   # sys.exit(self.signal)
    
    analisa_atualizacao(self.outputs)
#    analisa_atualizacao('sex abr 19 2013 09:08:18')
    

############################################################################################
def analisa_atualizacao(parametro):
    dicionario_1={'JAN':1, 'FEV':2, 'MAR':3, 'ABR':4, 'MAI':5, 'JUN':6, 'JUL':7, 'AGO':8, 'SET':9, 'OUT':10, 'NOV':11, 'DEZ':12}
    dicionario_2={'JAN':1, 'FEB':2, 'MAR':3, 'APR':4, 'MAY':5, 'JUN':6, 'JUL':7, 'AUG':8, 'SEP':9, 'OCT':10, 'NOV':11, 'DEC':12}
  #  qua abr 24 2013 09:08:18

    data = parametro.split()
    
    ano = int(data[3])
    dia = int(data[2])
    mes1 = data[1].upper()
    
    try:
        mes = dicionario_1[mes1]
    except:
        mes = dicionario_2[mes1]
    
    hora_completa = data[4].split(':')
    hora = int(hora_completa[0])
    minuto = int(hora_completa[1])
    segundo = int(hora_completa[2])
    
    hora_passada = datetime.datetime(ano,mes,dia, hora, minuto, segundo)       
    hora_atual = datetime.datetime.now()
    diferenca = (hora_atual - hora_passada)
  #  print diferenca
    a = str(diferenca)
  
    try:
        b = int(a.split()[0])
    except:
        b=0
  #  print b
    
    if(b>=1 and b<3):
        print 'WARNING - %s' %parametro
        sys.exit(1)
    elif(b>=3):
        print 'CRITICAL - %s'%parametro
        sys.exit(2)
    else:
        print 'OK - %s'%parametro
        sys.exit(0)
 ###################################################################################################################################
    

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
  

