#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import sys
import commands

def executa_snmpwalk(community,ip, mib):
  con = commands.getoutput("/usr/bin/snmpwalk -v1 -c %s %s %s"%(community,ip, mib))
  if 'Timeout: No Response' in str(con):
    print 'CRITICAL - Não foi possível realizar comunicação via snmp com elemento %s'%(ip)
    print con
    sys.exit(2)
  
  return filtraSaidaSnmp(con)

def filtraSaidaSnmp(con):
  vet = []
  lista = con.splitlines() 
  for l in lista:
    #print l
    vet.append(l.split(': ')[1].replace('"',""))
  
  return vet
 
def imprimeVetor(vet):
  for v in vet:
    print v
  print '\n\n'

if len(sys.argv) < 5:
  print 'CRITICAL - Ausência de parâmetros detectada.\n  Deve-se informar ip community modelo opcao'
  print '    Modelos aceitos: x3630M4 ou x3550M4'
  print '    Possíveis opções: fan, temperatura, fonte'
  sys.exit(2)

ip = sys.argv[1] 
community = sys.argv[2]
modelo = sys.argv[3]
opcao = sys.argv[4]
saida = 0
#print 'ip %s community %s modelo %s opcao %s'%(ip,community,modelo,opcao)

if opcao == 'temperatura':

  ### checagem de temperatura
  if modelo == 'x3630M4' or modelo == 'x3550M4':
    temp_desc = '.1.3.6.1.4.1.2.3.51.3.1.1.2.1.2'
    temp_atual = '.1.3.6.1.4.1.2.3.51.3.1.1.2.1.3'
    temp_lim_warning = '.1.3.6.1.4.1.2.3.51.3.1.1.2.1.7'
    temp_lim_critical = '.1.3.6.1.4.1.2.3.51.3.1.1.2.1.6'

    vet_temp_desc = []
    vet_temp_atual = []
    vet_temp_lim_warning = []
    vet_temp_lim_critical = []
    
    vet_temp_desc = executa_snmpwalk(community,ip, temp_desc)
    vet_temp_atual = executa_snmpwalk(community,ip, temp_atual)
    vet_temp_lim_warning = executa_snmpwalk(community,ip, temp_lim_warning)
    temp_lim_critical = executa_snmpwalk(community,ip, temp_lim_critical)

    tabela = '<html> <head><meta charset="utf-8"></head><body> <table border="1" align="center"> <tr> <th>Descri&#231&#227o</th> <th>Atual</th> <th>Warning</th> <th>Critical</th> </tr>'
    saida = 0
    msg = 'OK - Temperatura do elemento dentro da normalidade.'
    perf = ''
    for i in range(0,len(vet_temp_desc)):
      if (int(vet_temp_atual[i]) >= int(vet_temp_lim_warning[i])) and (int(vet_temp_atual[i]) < int(temp_lim_critical[i])) and int(vet_temp_atual[i]) > 0:
        linha = '<tr bgcolor="yellow" align="center"> <td>%s</td> <td>%s</td> <td>%s</td> <td>%s</td>'%(vet_temp_desc[i],vet_temp_atual[i], vet_temp_lim_warning[i], temp_lim_critical[i])
        saida = 1 
      elif (int(vet_temp_atual[i]) >= int(temp_lim_critical[i]))  and int(vet_temp_atual[i]) > 0:
        linha = '<tr bgcolor="red" align="center"> <td>%s</td> <td>%s</td> <td>%s</td> <td>%s</td>'%(vet_temp_desc[i],vet_temp_atual[i], vet_temp_lim_warning[i], temp_lim_critical[i])
        saida = 2
      else:
        linha = '<tr align="center"> <td>%s</td> <td>%s</td> <td>%s</td> <td>%s</td>'%(vet_temp_desc[i],vet_temp_atual[i], vet_temp_lim_warning[i], temp_lim_critical[i])

      #if saida == 1:
      #  linha = '<tr bgcolor="yellow" align="center"> <td>%s</td> <td>%s</td> <td>%s</td> <td>%s</td>'%(vet_temp_desc[i],vet_temp_atual[i], vet_temp_lim_warning[i], temp_lim_critical[i])
      #if saida == 2:
      #  linha = '<tr bgcolor="red" align="center"> <td>%s</td> <td>%s</td> <td>%s</td> <td>%s</td>'%(vet_temp_desc[i],vet_temp_atual[i], vet_temp_lim_warning[i], temp_lim_critical[i])
      #if saida == 0:
      #  linha = '<tr align="center"> <td>%s</td> <td>%s</td> <td>%s</td> <td>%s</td>'%(vet_temp_desc[i],vet_temp_atual[i], vet_temp_lim_warning[i], temp_lim_critical[i])
      
      tabela += linha

      perf += ' ' + vet_temp_desc[i].replace(" ",'_') + '=%s'%vet_temp_atual[i]

    tabela += '</table> </body> </html>'
 
    if saida == 1:
      msg = "WARNING - Temperatura do elemento em niveis de atencao."
    if saida == 2:
      msg = "CRITICAL - Temperatura do elemento em niveis criticos."

    print msg +'\n' + tabela + " | " + perf 

elif opcao == 'fan':
  ### checagem do fan
  if modelo == 'x3630M4' or modelo == 'x3550M4':
    fan_desc = '.1.3.6.1.4.1.2.3.51.3.1.3.2.1.2'
    fan_speed_atual = '.1.3.6.1.4.1.2.3.51.3.1.3.2.1.3'
    fan_state = '.1.3.6.1.4.1.2.3.51.3.1.3.2.1.10'
   
    vet_fan_desc = []
    vet_fan_speed_atual = []
    vet_fan_state = []

    vet_fan_desc = executa_snmpwalk(community,ip, fan_desc)
    vet_fan_speed_atual =  executa_snmpwalk(community,ip,fan_speed_atual)
    vet_fan_state = executa_snmpwalk(community,ip, fan_state)
   
    tabela = '<html> <head><meta charset="utf-8"></head><body> <table border="1" align="center"> <tr> <th>Descri&#231&#227o</th> <th>% de uso do Fan</th> <th>Estado atual</th> </tr>'
    saida = 0
    msg = 'OK - Velocidade dos fans dentro da normalidade.' 
    perf = ''
  
    for i in range(0,len(vet_fan_desc)):
      
      if "Normal" not in str(vet_fan_state[i]) and "Unknown" not in str(vet_fan_state[i]):
        linha = '<tr bgcolor="red" align="center"> <td>%s</td> <td>%s</td> <td>%s</td>'%(vet_fan_desc[i],vet_fan_speed_atual[i], vet_fan_state[i])
        saida = 2
      else:
        linha = '<tr align="center"> <td>%s</td> <td>%s</td> <td>%s</td> '%(vet_fan_desc[i],vet_fan_speed_atual[i], vet_fan_state[i]) 
    
      tabela += linha
      perf += ' ' + vet_fan_desc[i].replace(" ",'_') + '=%s'%(str(vet_fan_speed_atual[i]).replace('% of maximum','').replace(' ','').replace('offline','0')) 

    tabela += '</table> </body> </html>'

    if saida == 2:
      msg = "CRITICAL - Velocidade do(s) fan(s) em niveis criticos."

    print msg +'\n' + tabela + " | " + perf    

elif opcao == 'fonte':
  if modelo == 'x3630M4' or modelo == 'x3550M4':
    fonte_desc = '.1.3.6.1.4.1.2.3.51.3.1.11.2.1.2'
    fonte_state = '.1.3.6.1.4.1.2.3.51.3.1.11.2.1.6'

    vet_fonte_desc = []
    vet_fonte_state = []

    vet_fonte_desc = executa_snmpwalk(community,ip, fonte_desc)
    vet_fonte_state = executa_snmpwalk(community,ip, fonte_state)  

    tabela = '<html> <head><meta charset="utf-8"></head><body> <table border="1" align="center"> <tr> <th>Descri&#231&#227o</th> <th>Estado atual</th> </tr>'
    saida = 0
    msg = 'OK - Estado das fontes dentro da normalidade.' 
    perf = ''
 
    for i in range(0,len(vet_fonte_desc)):
      if "Normal" not in str(vet_fonte_state[i]):
        linha = '<tr bgcolor="red" align="center"> <td>%s</td> <td>%s</td>'%(vet_fonte_desc[i],vet_fonte_state[i])
        saida = 2        
      else:
        linha = '<tr align="center"> <td>%s</td> <td>%s</td> '%(vet_fonte_desc[i],vet_fonte_state[i])
   
      tabela += linha
      perf += ' ' + vet_fonte_desc[i].replace(" ",'_') + '=%s'%(str(vet_fonte_state[i]).replace('Normal','1').replace('Critical','0'))
    
    tabela += '</table> </body> </html>'
    
    if saida == 2:
      msg = "CRITICAL - Problema detectado na(s) fonte(s)."
   
    print msg +'\n' + tabela + " | " + perf  

else:
  print 'CRITICAL - Parâmetros informados de forma incorreta.\n  Deve-se informar ip community modelo opcao'
  print '    Modelos aceitos: x3630M4 ou x3550M4'
  print '    Possíveis opções: fan, temperatura, fonte'
  saida = 2


sys.exit(saida)

