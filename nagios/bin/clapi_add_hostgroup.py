#!/usr/bin/python
import sys
import re
arq =  sys.argv[1:][0]
#arq, satelite = "hosts.cfg","Satelite_Rebocadores"
#arq  = "canopus_conf/hostgroups.cfg"
data = open(arq,'r').read()
p1="define hostgroup{"
p2="\n}\n"
while True:
    try:
        inicio = data.index(p1)+len(p1)
        fim = data.index(p2)
        l = data[inicio:fim]
        hostgroup_name = re.findall("hostgroup_name\t\t\t(.+?)\n",l)[0]
        service_description = re.findall("alias\t\t\t\t(.+?)$",l)[0]
        print "\"%s;%s\""%(hostgroup_name,service_description)
        data=data[fim+len(p2):]
    except:break
