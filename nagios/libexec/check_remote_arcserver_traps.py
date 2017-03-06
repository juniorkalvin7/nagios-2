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
import sys,re,binascii


args = sys.argv[1:]

if len(args)<2:
  print "Centreon Plugin\nRemote ARCServer status 2.0\nsuporta exec,extend,Hex valores\n  por GemayelLira"
  print " Argumentos:host community"
  print "Ex.\n%s 10.0.0.5 u3fr0I9b5" % sys.argv[0] 
  #print 
  sys.exit(1)
else:
  #print args
  host=args[0]
  community=args[1]
  
try:
  data=(commands.getoutput("/usr/bin/snmpwalk -v 1 -c %s %s .1.3.6.1.4.1.2022.13.3.1.2" %(community,str(host))))
except Exception,e:
  print "CRITICAL - nao consegui capturar valores"
  print e
  sys.exit(1)
if 'Hex-STRING' in data:
  data = data.split('Hex-STRING:')[1]
  data = binascii.unhexlify(''.join(data.replace('\n','').split()))
#sys.exit(1)
if len(data) ==0:
  try:
    data=(commands.getoutput("/usr/bin/snmpwalk -v 1 -c %s %s .1.3.6.1.4.1.2022.13.101" %(community,str(host))))
  except Exception,e:
    print "CRITICAL - nao consegui capturar valores"
    print e
    sys.exit(1)
if len(data) ==0:
  try:
    data=(commands.getoutput("/usr/bin/snmpwalk -v 1 -c %s %s .1.3.6.1.4.1.2022.13" %(community,str(host))))
  except Exception,e:
    print "CRITICAL - nao consegui capturar valores"
    print e
    sys.exit(1)
  data="\n".join(re.findall('"(.+?)"',data)[3:])
#else:
  #data="\n".join(re.findall('"(.+?)"',data))

  #data="\n".join(re.findall('"(.+?)"',data)[3:])
#else:
  #data="\n".join(re.findall('"(.+?)"',data))

  
if data.count('CRITICAL'):
  print data
  sys.exit(2)
elif data.count('WARNING'):
  print data
  sys.exit(1)
elif data.count('UNKNOWN'):
  print data
  sys.exit(3)
else:
  print data
sys.exit(0)  

