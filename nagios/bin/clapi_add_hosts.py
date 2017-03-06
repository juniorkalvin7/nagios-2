#!/usr/bin/python
import sys
import re
arq, satelite= sys.argv[1:]
#arq, satelite = "hosts.cfg","Satelite_Rebocadores"
data = open(arq,'r').read()
p1="define host{"
p2="\n}\n"
print "Abrindo",arq
print "Satleite",satelite
while True:
  try:
    inicio = data.index(p1)+len(p1)
    fim = data.index(p2)
    l = data[inicio:fim]
    host_name = re.findall("host_name\t\t\t\t(.+?)\n",l)[0]
    alias = re.findall("alias\t\t\t\t(.+?)\n",l)[0]
    address = re.findall("address\t\t\t\t(.+?)\n",l)[0]
    use = re.findall("use\t\t\t\t(.+?)\n",l)[0]
    print "/usr/local/centreon/www/modules/centreon-clapi/core/centreon -u alvin -p abc@123 -o HOST -a ADD -v \"%s;%s;%s;%s;%s;;\""%(host_name,alias,address,use.replace(",","|"),satelite)
    data=data[fim+len(p2):]
  except:break
