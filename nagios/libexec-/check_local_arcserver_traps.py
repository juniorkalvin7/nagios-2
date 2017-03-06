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
#import commands
import sys

args = sys.argv[1:]
if len(args)<1 or args[0].count('help'):
  print "Centreon Plugin\n Local ARCServer status por GemayelLira"
  print "Argumentos:host"
  print "Ex.\n%s 10.0.0.5" % sys.argv[0] 
  #print 
  sys.exit(1)
else:
  #print args
  host=args[0]
  #community=args[1]
logfile='/var/log/arclog_status_%s.log' % host.replace('.','_')
try:
  data=open(logfile,'r').read()
except:
  print 'CRITICAL - Nao consegui abrir arquivos de log dos traps'
  sys.exit(3)

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

