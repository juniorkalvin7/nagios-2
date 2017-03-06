import sys
import re
arq = sys.argv[1]
#arq = "canopus_conf/hosts.cfg"
data = open(arq,'r').read()
p1="define host{"
p2="\n}\n"
print "Abrindo",arq
while True:
  try:
    inicio = data.index(p1)+len(p1)
  except:break
  fim = data.index(p2)
  l = data[inicio:fim]
  host_name = re.findall("host_name\t\t\t\t(.+?)\n",l)[0]
  if not "hostgroups" in l:continue
  hostgroups = re.findall("hostgroups\t\t\t(.+?)\n",l)[0]
  print "/usr/local/centreon/www/modules/centreon-clapi/core/centreon -u alvin -p abc@123 -o HOST -a gethostgroup -v \"%s;%s\"".decode().encode('utf-8')%(host_name,hostgroups.replace(",","|"))
  print "/usr/local/centreon/www/modules/centreon-clapi/core/centreon -u alvin -p abc@123 -o HOST -a sethostgroup -v \"%s;%s\"".decode().encode('utf-8')%(host_name,hostgroups.replace(",","|"))
  data=data[fim+len(p2):]
