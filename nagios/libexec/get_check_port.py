#!/usr/bin/python
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
from socket import *
import sys

class Portcheck:
  def __init__(self, host,port):
    self.host = host
    self.port = port
    self.socket = setdefaulttimeout(30)
    self.sd = socket(AF_INET, SOCK_STREAM)
  def run(self):
    try:
      self.sd.connect((self.host, self.port))
      res="OK - %s:%d OPEN|ok=1" % (self.host, self.port)
      self.sd.close()
      return res
    except: 
      res="CRITICAL - %s:%d CLOSED|ok=0" % (self.host, self.port)
      #sys.exit(1)
      return res
      #pass

args = sys.argv[1:]
if len(args)<2:
  print "Centreon Plugin\nPort check Status 1.0 por GemayelLira"
  print "Argumentos:\npython ./%s HOST PORT" % sys.argv[0]
  print "Ex.\npython ./%s 127.0.0.1 80" % sys.argv[0] 
  sys.exit(1)
else:
  host=args[0]
  port=int(args[1])

res=Portcheck(host,port).run()
if res.count('OPEN'):
  print res
  sys.exit(0)
else:
  print res
  sys.exit(1)
