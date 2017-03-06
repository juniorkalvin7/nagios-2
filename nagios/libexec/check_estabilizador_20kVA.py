#!/usr/bin/env python
# -*- coding: utf-8 -*-

import commands
import sys

def executa_snmpwalk(community, ip, mib, divide_10):
  con = commands.getoutput('/usr/bin/snmpwalk -v1 -c %s %s %s'%(community,ip,mib))
  #print 'con %s'%con 
  con = str(con).split(' ')[-1]
  con = int(con)  
  
  if divide_10 == 1:
    return con/10
  else:
    return con

def formata_msg(titulo,string_1,valor1,string_2,valor2,string_3,valor3,string_12,valor11,string_22,valor22,string_33,valor33):
  return "Ok - %s: %s: %s,  %s: %s, %s: %s | %s=%s %s=%s %s=%s"%(titulo,string_1,valor1,string_2,valor2,string_3,valor3,string_1,valor1,string_2,valor2,string_3,valor3)

def formata_msg2(titulo,string_1,valor1,string_12,valor11):
  return "Ok - %s: %s: %s | %s=%s "%(titulo,string_1,valor1,string_12,valor11)


args = sys.argv[1:]
saida = 0

if len(args) <= 0:
  print 'Argumentos do servico no devem seguir o formato:'
  print 'community ip opcao'
  print 'Ex: %s public 8.8.8.8 1'%sys.argv[0]
  print '---------------------------------'
  print 'Por favor informe o que deseja monitorar'
  print '  1 - Tensao de entrada nas fases:'
  print '  2 - Tensao de saida nas fases'
  print '  3 - Corrente de entrada nas fases'
  print '  4 - Corrente de saida nas fases'
  print '  5 - Carga (em kW)' 
  print '  6 - Carga (em %)'
  print '  7 - Temperatura de operacao' 
  print '  8 - Uptime'
  
  saida = 2
  

else:
  community = args[0]  
  ip = args[1]  
  op = int(args[2])
  msg = ''
  #print '%s %s %s'%(community,ip,op) 
  
  if op == 1:
    #print 'op %s'%op 
    valor1 = executa_snmpwalk(community, ip, '.1.3.6.1.4.1.3778.3.3.2.0', 1) 
    valor2 = executa_snmpwalk(community, ip, '.1.3.6.1.4.1.3778.3.3.3.0', 1)
    valor3 = executa_snmpwalk(community, ip, '.1.3.6.1.4.1.3778.3.3.4.0', 1)
    titulo = 'Tensao de entrada nas fases'
    string_1 = "VoltagePhaseR"
    string_2 = "VoltagePhaseS"
    string_3 = "VoltagePhaseT"
    msg = formata_msg(titulo,string_1,valor1,string_2,valor2,string_3,valor3,string_1,valor1,string_2,valor2,string_3,valor3)
  
  elif op == 2:
    valor1 = executa_snmpwalk(community, ip, '.1.3.6.1.4.1.3778.3.4.2.0', 1) 
    valor2 = executa_snmpwalk(community, ip, '.1.3.6.1.4.1.3778.3.4.3.0', 1)
    valor3 = executa_snmpwalk(community, ip, '.1.3.6.1.4.1.3778.3.4.4.0', 1)
    titulo = 'Tensao de saida nas fases'
    string_1 = "OutputVoltagePhaseR"
    string_2 = "OutputVoltagePhaseS"
    string_3 = "OutputVoltagePhaseT"
    msg = formata_msg(titulo,string_1,valor1,string_2,valor2,string_3,valor3,string_1,valor1,string_2,valor2,string_3,valor3)

  elif op == 3:
    valor1 = executa_snmpwalk(community, ip, '.1.3.6.1.4.1.3778.3.3.5.0', 0) 
    valor2 = executa_snmpwalk(community, ip, '.1.3.6.1.4.1.3778.3.3.6.0', 0)
    valor3 = executa_snmpwalk(community, ip, '.1.3.6.1.4.1.3778.3.3.7.0', 0)
    titulo = 'Corrente de entrada nas fases'
    string_1 = "InputCurrentPhaseR"
    string_2 = "InputCurrentPhaseS"
    string_3 = "InputCurrentPhaseT"
    msg = formata_msg(titulo,string_1,valor1,string_2,valor2,string_3,valor3,string_1,valor1,string_2,valor2,string_3,valor3)

  elif op == 4:
    valor1 = executa_snmpwalk(community, ip, '.1.3.6.1.4.1.3778.3.4.5.0', 0) 
    valor2 = executa_snmpwalk(community, ip, '.1.3.6.1.4.1.3778.3.4.6.0', 0)
    valor3 = executa_snmpwalk(community, ip, '.1.3.6.1.4.1.3778.3.4.7.0', 0)
    titulo = 'Corrente de saida nas fases'
    string_1 = "OutputCurrentPhaseR"
    string_2 = "OutputCurrentPhaseS"
    string_3 = "OutputCurrentPhaseT"
    msg = formata_msg(titulo,string_1,valor1,string_2,valor2,string_3,valor3,string_1,valor1,string_2,valor2,string_3,valor3)
  
  elif op == 5:
    valor1 = executa_snmpwalk(community, ip, '.1.3.6.1.4.1.3778.3.4.9.0', 0) 
    valor2 = executa_snmpwalk(community, ip, '.1.3.6.1.4.1.3778.3.4.10.0', 0)
    valor3 = executa_snmpwalk(community, ip, '.1.3.6.1.4.1.3778.3.4.11.0', 0)
    valor1 = valor1 * 100
    valor2 = valor2 * 100
    valor3 = valor3 * 100
    titulo = 'Carga (em W)'
    string_1 = "OutputPowerPhaseR"
    string_2 = "OutputPowerPhaseS"
    string_3 = "OutputPowerPhaseT"
    msg = formata_msg(titulo,string_1,valor1,string_2,valor2,string_3,valor3,string_1,valor1,string_2,valor2,string_3,valor3)

  elif op == 6:
    valor1 = executa_snmpwalk(community, ip, '.1.3.6.1.4.1.3778.3.4.13.0', 0) 
    valor2 = executa_snmpwalk(community, ip, '.1.3.6.1.4.1.3778.3.4.14.0', 0)
    valor3 = executa_snmpwalk(community, ip, '.1.3.6.1.4.1.3778.3.4.15.0', 0)
    titulo = 'Carga (em %)'
    string_1 = "OutputLoadPhaseR"
    string_2 = "OutputLoadPhaseS"
    string_3 = "OutputLoadPhaseT"
    msg = formata_msg(titulo,string_1,valor1,string_2,valor2,string_3,valor3,string_1,valor1,string_2,valor2,string_3,valor3)
  
  elif op == 7:
    valor1 = executa_snmpwalk(community, ip, '.1.3.6.1.4.1.3778.3.2.3.0', 0) 
    titulo = 'Temperatura de operacao'
    string_1 = "Temperature"
    msg = formata_msg2(titulo,string_1,valor1,string_1,valor1)

  elif op == 8:
    mib = '.1.3.6.1.2.1.1.3.0'
    con = commands.getoutput('/usr/bin/snmpwalk -v1 -c %s %s %s'%(community,ip,mib))
    valor1 = str(con).split('=')[-1]
    titulo = 'Uptime'
    string_1 = "Uptime"
    msg = formata_msg2(titulo,string_1,valor1,string_1,valor1)

  print msg

sys.exit(saida)

