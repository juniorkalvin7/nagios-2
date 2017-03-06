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
  print "Centreon Plugin\nGet Squid - Current Swap Size"
  print "Argumentos:host community"
  print "Ex.\n%s 10.0.0.45 u3fr0I9b5" % sys.argv[0] 
  #print 
  sys.exit(1)
else:
  #print args
  host=args[0]
  community=args[1]
try:
  valor=(commands.getoutput("/usr/bin/snmpwalk -t 100000 -v 1 -c %s %s:3401 1.3.6.1.4.1.3495.1.3.2.1.14" %(community,str(host)))).split(': ')[1]
  #maxvalor=(commands.getoutput("/usr/bin/snmpwalk -t 100000 -v 1 -c %s %s:3401 .1.3.6.1.4.1.3495.1.2.5.2" %(community,str(host)))).split(': ')[1]
except Exception,e:
  print "CRITICAL - nao consegui capturar valores"
  print e
  sys.exit(2)

def convertbit(bits):
  bits = float(str(bits)+'.0')/1048576
  if (bits  > 1000):
    bits  = bits  / 1000;
    bits_unit = "G"
  else:
    bits_unit = "M"
  return(bits,bits_unit)

def mega2bit(maxvalor):
  bits = float(str(maxvalor)+'.0')*1048576
  return(bits)
  
#print convertbit('%.0f' % mega2bit(maxvalor))
print "Squid - Current Swap Size - %s%s|used=%sB" % ('%.2f'%(convertbit(valor)[0]),convertbit(valor)[1],valor)
