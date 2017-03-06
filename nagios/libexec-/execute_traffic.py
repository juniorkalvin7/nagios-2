#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import commands, time

saida = 0

if len(sys.argv) < 8: 
    print "WARNING - Ausencia de parametros"
    print 'Ex: ./execute_traffic.py 172.18.13.15 1 80 90 u3rf0I9b5 m 1000 1000'
    sys.exit(1)
else:
    args = sys.argv[1::]
    
    ip = args[0]
    interface= args[1]
    warning= args[2]
    critical= args[3]
    community= args[4]
    unidade= args[5] #medida
    download= args[6]
    upload= args[7]
    
    #print '/usr/local/nagios/libexec/check_iftraffic64.pl -H %s -i %s -w %s -c %s -C %s -u %s -I %s -O %s '%(ip,interface, warning, critical, community,unidade, download, upload)
    
    #commands.getoutput('/usr/bin/perl /usr/local/nagios/libexec/check_iftraffic64.pl -H %s -i %s -w %s -c %s -C %s -u %s -I %s -O %s '%(ip,interface, warning, critical, community,unidade, download, upload))
    commands.getoutput('/usr/bin/perl /usr/local/nagios/libexec/check_iftraffic3.pl -H %s -i %s -w %s -c %s -C %s -u %s -I %s -O %s -B'%(ip,interface, warning, critical, community,unidade, download, upload))
    time.sleep(2)
    #con = commands.getoutput('/usr/bin/perl /usr/local/nagios/libexec/check_iftraffic64.pl -H %s -i %s -w %s -c %s -C %s -u %s -I %s -O %s'%(ip,interface, warning, critical, community,unidade, download, upload))
    con = commands.getoutput('/usr/bin/perl /usr/local/nagios/libexec/check_iftraffic3.pl -H %s -i %s -w %s -c %s -C %s -u %s -I %s -O %s -B'%(ip,interface, warning, critical, community,unidade, download, upload))
    print con
    
    if 'warning' in str(con).lower():
        saida = 1
    elif 'critical' in str(con).lower(): 
        saida = 2
 
    sys.exit(saida)

