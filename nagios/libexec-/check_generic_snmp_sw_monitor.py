#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys,commands


if len(sys.argv)<6:
  print "CRITICAL - Serviço configurado de forma errada. Ausência de parâmetros."
  print "Servico de Monitoramento. Desenvolvido por Raul Barros em 28 de janeiro de 2014"
  print "\nExemplos de Uso:\npython %s IP community MIB Mensagem versao_snmp" % sys.argv[0]
  print 'Ex.\npython %s 10.0.0.59 u3fr0I9b5 1.3.6.1.4.1.9.9.10.1.1.3.1.1.3.1.1 "Descricao do Switch" 1 ' % sys.argv[0] 
  print 'Ex.\npython %s 10.0.0.59 u3fr0I9b5 1.3.6.1.4.1.9.9.10.1.1.3.1.1.3.1.1 "Descricao do Switch" 2 ' % sys.argv[0]
  sys.exit(2)

ip = sys.argv[1]
community = sys.argv[2]
mib = sys.argv[3]
msg = sys.argv[4]
saida = 0

if int(sys.argv[5]) == 2:
  versao_snmp = str(sys.argv[5]) + 'c'

else: 
  versao_snmp = sys.argv[5]
#print '/usr/bin/snmpwalk -v%s -c %s %s %s'%(versao_snmp,community,ip,mib)
con = commands.getoutput('/usr/bin/snmpwalk -v%s -c %s %s %s'%(versao_snmp,community,ip,mib))

if "timeout" in str(con).lower():
  print "CRITICAL - Não foi possível realizar comunicação com o host."
  print '%s'%con
  saida = 2

else:
  #SNMPv2-SMI::enterprises.9.9.10.1.1.3.1.1.3.1.1 = STRING: "AMD or Intel FLASH chip"
  saida_msg = str(con).split(":")[-1]
  msg = " %s:%s"%(msg,saida_msg)
  print "OK - %s"%msg.replace('"','')
  print con

sys.exit(saida)
