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
import commands
import time
import math
import os
import sys

args = sys.argv[1:]

if len(args)<2:
  print "Centreon Plugin\nGet DHCP Server Status por Gemayel Lira"
  print "Argumentos:host community"
  print "Ex.\n%s 10.0.0.45 u3fr0I9b5" % sys.argv[0] 
  sys.exit(1)
else:
  #print args
  host=args[0]
  community=args[1]
try:
  data=(commands.getoutput("/usr/bin/snmpwalk -t 100000 -v 1 -c %s %s .1.3.6.1.4.1.311.1.3.1" %(community,str(host)))).split('\n')
except Exception,e:
  print "CRITICAL - nao consegui capturar valores"
  print e
  sys.exit(2)

try:  
  snmp_dhcp_requests=data[2].split('Counter32: ')[1]
  snmp_dhcp_releases=data[3].split('Counter32: ')[1]
  snmp_dhcp_offers=data[4].split('Counter32: ')[1]
  snmp_dhcp_acks=data[5].split('Counter32: ')[1]
  snmp_dhcp_nonacks=data[6].split('Counter32: ')[1]
except:
  print "CRITICAL - DHCP Service - Nao consegui capturar valores, servico provavelmente parou"
  sys.exit(2)

print "DHCP Service - Requests received %s,Releases received %s,Offers sent %s,Acknowledges rec. %s,Non Acknowledges rec. %s|dhcp_requests=%s dhcp_releases=%s dhcp_offers=%s dhcp_acks=%s dhcp_nonacks=%s" % \
      (snmp_dhcp_requests,snmp_dhcp_releases,snmp_dhcp_offers,snmp_dhcp_acks,snmp_dhcp_nonacks,\
       snmp_dhcp_requests,snmp_dhcp_releases,snmp_dhcp_offers,snmp_dhcp_acks,snmp_dhcp_nonacks)
