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
import re
"""
Se faz necessario trabalhar com Selinux
sys.exit(0) OK
sys.exit(1) WARNING
sys.exit(2) CRITICAL
sys.exit(3)UNKNOWN
"""
args = sys.argv[1:]

if len(args)<1:
  print "Centreon Plugin\nCheck Latency Perda por GemayelLira"
  print "Argumentos:host"
  print "Ex.\n%s 201.18.153.231" % sys.argv[0] 
  #print 
  sys.exit(1)
else:
  #print args
  host=args[0]

  

perdasave="/var/lib/centreon/centplugins/ping2_perda_%s" % host
perda=open(perdasave,'r').read().rstrip()
if ':' in perda:
  perda1=perda.split(':')[0]
  tempo=perda.split(':')[1]
  perda=perda1
  
  if int(perda) >0:
    print "PERDA CRITICAL - %s%%|perda=%s\nDuracao %0.6fs"% (perda,perda,float(tempo))
    sys.exit(2)
  else:
    print "PERDA %s%%|perda=0\nDuracao %0.6fs"% (perda,float(tempo))
    sys.exit(0)
else:
  if int(perda) >0:
    print "PERDA CRITICAL - %s%%|perda=%s"% (perda,perda)
    sys.exit(2)
  else:
    print "PERDA %s%%|perda=0"% (perda)
    sys.exit(0)

