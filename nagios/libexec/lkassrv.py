#!/usr/bin/env python
# -*- coding: utf-8 -*-

from socket import *
import sys,commands

#
# rev:25jun12 gemayellira
# Verificacao de retorno do comando 
# snmpwalk e impressao de erro
#
# Última alteração:30 de Maio de 2012
# por: Raul Barros e Arinaldo Araujo 
# para alarmar se o numero de host
# desatualizados for diferente de 0
#

#class genericplugin():
class genericplugin:
  def __init__(self, ip,community,kasarg):
    self.ip=ip
    self.community=community
    self.kasarg=kasarg
    
    self.signal=0
    self.outputs=''
    if   self.kasarg=='qthosts':      self.mib='.1.3.6.1.4.1.23668.1093.1.1.3'
    elif self.kasarg=='qtsav':        self.mib='.1.3.6.1.4.1.23668.1093.1.1.2.1'
    elif self.kasarg=='atu':          self.mib='.1.3.6.1.4.1.23668.1093.1.2.1.0'
    elif self.kasarg=='outbreak':     self.mib='.1.3.6.1.4.1.23668.1093.1.3.2.6.0'
    
  def run(self):
    comando = "/usr/bin/snmpwalk -v 1 -c %s %s %s" %(self.community,str(self.ip),self.mib)
    self.outputs=(commands.getoutput(comando))
    #print self.outputs
    #try:
    self.kasreader()
    #except Exception,e:
     # print 'Erro em coleta, valor retornado invalido'
      #print 'Erro:',e
     # print 'Tente executar manualmente:',comando
     # sys.exit(2)

    #self.outputs=self.outputs.split("\"")[1]
    #if self.outputs.count('CRITICAL'):self.signal=1
    #elif self.outputs.count('WARNING'):self.signal=2
    #elif self.outputs.count('UNKNOWN'):self.signal=3
    #self.output()
  
  def kasreader(self):
    if self.kasarg == 'qthosts':
      qt=self.outputs.split(' ')[3]
#      print 'Kaspersky - Total de Hosts Gerenciados %s|kasqt=%s' % (qt,qt)
#      qt=int(0)
      if int(qt) == 0:
       print 'WARNING - Kaspersky - Total de Hosts Gerenciados %s|kasqt=%s' % (qt,qt)
       sys.exit(1)
      else: 
       print 'Kaspersky - Total de Hosts Gerenciados %s|kasqt=%s' % (qt,qt)

    elif self.kasarg == 'qtsav':
      qt=self.outputs.split(' ')[3]
      #qt = 1
      if int(qt) != 0:
        print 'WARNING - Kaspersky - Total de Hosts Sem Antivirus %s|kasqt=%s' % (qt,qt)
        sys.exit(1)
      else:
        print 'Kaspersky - Total de Hosts Sem Antivirus %s|kasqt=%s' % (qt,qt)

#      print 'Kaspersky - Total de Hosts Sem Antivirus %s|kasqt=%s' % (qt,qt)
    elif self.kasarg == 'atu':
      qt=self.outputs.split(' ')[3]
#     qt=1
      print 'Kaspersky - Hosts para Atualizar Assinaturas %s|kasqt=%s' % (qt,qt)
      if int(qt) != 0:
        sys.exit(1)
    elif self.kasarg == 'outbreak':
      qt=self.outputs.split(' ')[3]
      if int(qt) == 1:
        print 'CRITICAL - Kaspersky - OutBreak %s|kasqt=%s' % (qt,qt)
        sys.exit(2)
      else:
        print 'Kaspersky - OutBreak %s|kasqt=%s' % (qt,qt)

  def output(self):
    """
    Tipos de saida: 
    0 ok
    1 warning
    2 critical
    3 unknown
    """
    print '%s' % (self.outputs)
    sys.exit(self.signal)
    

if __name__ == "__main__":
  args = sys.argv[1:]
  if len(args)<2:
    print "Centreon Plugin\nGetSnmp Info 1.0 por GemayelLira"
    print 'Args:\nqthosts quantidade de hosts gerenciados'
    print 'qtsav quantidade de hosts sem av'
    print 'atu verifica atualizacao'
    print "Argumentos:\npython ./%s IP community arg" % sys.argv[0]
    print "Ex.\npython ./%s 192.168.0.230 u3fr0I9b5 qthosts" % sys.argv[0] 
    sys.exit(1)
  else:
    ip=args[0]
    community=args[1]
    kasarg=args[2]

  genericplugin(ip,community,kasarg).run()
