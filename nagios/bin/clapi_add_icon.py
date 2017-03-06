#!/usr/bin/python
import sys
import re
arq =  sys.argv[1:][0]
#arq, satelite = "hosts.cfg","Satelite_Rebocadores"
#arq  = "canopus_conf/hosts.cfg"
data = open(arq,'r').read()
p1="define host{"
p2="\n}\n"
print "Abrindo",arq
while True:
  try:
    inicio = data.index(p1)+len(p1)
    fim = data.index(p2)
    l = data[inicio:fim]
    host_name = re.findall("host_name\t\t\t\t(.+?)\n",l)[0]
    icon_image = re.findall("icon_image\t\t\t(.+?)\n",l)[0]
    statusmap_image = re.findall("icon_image\t\t\t(.+?)\n",l)[0]
    print "/usr/local/centreon/www/modules/centreon-clapi/core/centreon -u alvin -p abc@123 -o HOST -a setparam -v \"%s;icon_image;%s\""%(host_name,icon_image)
    print "/usr/local/centreon/www/modules/centreon-clapi/core/centreon -u alvin -p abc@123 -o HOST -a setparam -v  \"%s;statusmap_image;%s\""%(host_name,statusmap_image)
    data=data[fim+len(p2):]
  except:break
