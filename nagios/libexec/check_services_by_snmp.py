#!/usr/bin/env python
# coding: utf-8

# Autor: Arinaldo Araujo/Gemayel Lira/Samuel Costa
# Data: 31/10/11

"""extend .1.3.6.1.4.1.2024.34 mic_host /usr/bin/python /usr/local/bin/check_services_by_name.py apache2 dhcp named sshd ntpd squid"""

import sys, commands

parametros = sys.argv[1:]
saida = 0
if ( len(parametros)< 3 ):
	print "Argumentos:\npython %s IP community MIB" % sys.argv[0]
	print "Ex: python %s 200.172.84.2 u3fr0I9b5 .1.3.6.1.4.1.2024.34" % sys.argv[0] 
	sys.exit(1)
else:
	ip=parametros[0]
	community=parametros[1]
	mib=parametros[2] 

data = commands.getoutput("/usr/bin/snmpwalk -v 1 -c %s %s %s.3.1.2" %(community,str(ip),mib) )
if "WARNING" in data:
	saida = 1
a=data.split('"');
b=a[1];
print (b)

sys.exit( saida )

