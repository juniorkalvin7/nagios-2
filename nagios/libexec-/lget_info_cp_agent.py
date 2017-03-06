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
import sys,urllib2,re,os,commands

    
args = sys.argv[1:]

"""
  (0) OK
  (1) WARNING
  (2) CRITICAL
  (3)UNKNOWN
"""
if len(args) != 2:
  print "Local Centreon Plugin\t\t\tpor GemayelLira\nCaptura informacoes CP Agent Nobreak\n"
  print "Argumentos:host tipo"
  print "Tipos de informacao:tentrada,\ntentradacorrente,\ntsaida,\ntsaidacorrente,\ntpotenciaaparente,\ntpotenciaativa,\ntemperatura,\ntbateria,\ncargaatual,\ntraptrap"
  print "Ex.\n"+os.getcwd()+"/%s 192.168.0.238 temperatura" % sys.argv[0] 
  sys.exit(1)
else:
  host=args[0]
  infor=args[1]
  
opener = urllib2.build_opener()
url = "http://%s/monitora.html" % host
data = opener.open(url).read()
try:
  tentrada=re.findall('id="v_8">(.+?)&nbsp;</td></tr>',data)[0]
  tentradacorrente=re.findall('id="v_19">(.+?)&nbsp;</td></tr>',data)[0]
  
  tsaida=re.findall('id="v_12">(.+?)&nbsp;</td></tr>',data)[0]
  tsaidacorrente=re.findall('id="v_23">(.+?)&nbsp;</td></tr>',data)[0]
  tpotenciaaparente=re.findall('id="v_45">(.+?)&nbsp;</td></tr>',data)[0]
  tpotenciaativa=re.findall('id="v_41">(.+?)&nbsp;</td></tr>',data)[0]
  
  temperatura=re.findall('id="v_50">(.+?)&nbsp;</td></tr>',data)[0]
  
  tbateria=re.findall('id="v_11">(.+?)&nbsp;</td></tr>',data)[0]
  #cargaatual=re.findall('id="v_54">(.+?)&nbsp;</td></tr>',data)[0]
except:
  
  print 'WARNING - nao consegui capturar informacoes do cp-agent'
  sys.exit(1)
  
if infor=='tentrada':
  if int(tentrada.split(',')[0]) > 190:
    print 'CP Agent - Tensao de entrada %s|tentrada=%s' % (tentrada,tentrada)
  else:
    print 'CRITICAL - CP Agent - Tensao de entrada %s|tentrada=%s' % (tentrada,tentrada)
    sys.exit(2)
elif infor =='tentradacorrente':
  print 'CP Agent - Corrente de entrada %s|tentradacorrente=%s' % (tentradacorrente,tentradacorrente)
elif infor =='tsaida':
  print 'CP Agent - Tensao de saida %s|tsaida=%s' % (tsaida,tsaida)
elif infor =='tsaidacorrente':
  print 'CP Agent - Corrente de saida %s|tsaidacorrente=%s' % (tsaidacorrente,tsaidacorrente)
elif infor =='temperatura':
  if int(temperatura.split(',0')[0]) >= 36:
    print 'CRITICAL - CP Agent - Temperatura do Nobreak ELEVADA %s,0C|temperatura=%s,0C;;' % (temperatura.split(',0')[0],temperatura.split(',0')[0])
    sys.exit(2)
  else:
    print 'CP Agent - Temperatura do Nobreak %s,0C|temperatura=%s,0C;;' % (temperatura.split(',0')[0],temperatura.split(',0')[0])
elif infor =='tbateria':
  print 'CP Agent - Tensao da Bateria %s|tbateria=%s' % (tbateria,tbateria)
#elif infor =='cargaatual':
  #print 'CP Agent - Baterias Carga Atual %s|cargaatual=%s' % (cargaatual,cargaatual)
elif infor=='tpotenciaaparente':
  tpotenciaaparentet=tpotenciaaparente.replace('KVA','').replace(',','.')  
  tpotenciaaparentet=float(float(tpotenciaaparentet)/3*100)
  print 'CP Agent - Potencia Aparente %s %4.2f%% Max 3Kva|tpotenciaaparente=%4.2f size=100' % (tpotenciaaparente,tpotenciaaparentet,tpotenciaaparentet)
elif infor=='tpotenciaativa':
  tpotenciaativat=tpotenciaativa.replace('KW','').replace(',','.')  
  tpotenciaativat=float(float(tpotenciaativat)/1.95*100)
  print 'CP Agent - Potencia Ativa %s %4.2f%% Max 1.95Kva|tpotenciaativa=%4.2f size=100' % (tpotenciaativa,tpotenciaativat,tpotenciaativat)
elif infor=='traptrap':
  if len(open('/var/log/cpagentlog.log').read().split('\n')) >3:
    data=commands.getoutput('tail -n3 /var/log/cpagentlog.log').split('\n')
    if data[2].count('CRITICAL'):
      print '%s|%s' % (data[2],"\n".join(data))
      sys.exit(2)
    elif data[2].count('WARNING'):
      print '%s' % (data[2])
      sys.exit(1)
    else:
      print '%s|%s' % (data[2],"\n".join(data))
  else:
    print 'Trap Vazio'

sys.exit(0)

