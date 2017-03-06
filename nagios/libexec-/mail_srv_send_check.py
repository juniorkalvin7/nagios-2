#!/usr/bin/env python2.6
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
"""
sys.exit(0) OK
sys.exit(1) WARNING
sys.exit(2) CRITICAL
sys.exit(3)UNKNOWN
"""

import poplib,datetime,time,sys

t = datetime.datetime.now()
tempo1 = int("%d" % (time.mktime(t.timetuple())))
temposendmail=open('/tmp/mail.log','r').read()
try:
    M = poplib.POP3('mail.saude.ma.gov.br')
    M = poplib.POP3_SSL('mail.saude.ma.gov.br')
    M.user('monitoramento@saude.ma.gov.br')
    M.pass_('n02N6tE1DaRc')
except Exception,e:
    print "CRITICAL - check",e
    sys.exit(2)
numMessages = len(M.list()[1])
#print numMessages
msg=0
if numMessages > 0:
    for i in range(numMessages):
        M.dele(str(i+1))
    msg=1
M.quit()

t = datetime.datetime.now()
tempo2 = int("%d" % (time.mktime(t.timetuple())))

print 'Checa Email OK checado em %d Checagem entre env/rec %d segundos|tempo=%d temposendrec=%d' % ((tempo2-tempo1),(tempo2-int(temposendmail)),(tempo2-tempo1),(tempo2-int(temposendmail)))
sys.exit(0)

