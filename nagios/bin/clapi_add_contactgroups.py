import sys
import re
arq =  sys.argv[1:][0]
#arq  = "canopus_conf/contactgroups.cfg"
data = open(arq,'r').read()
p1="define contactgroup{"
p2="\n}\n"
while True:
  try:
    inicio = data.index(p1)+len(p1)
  except:break
  fim = data.index(p2)
  l = data[inicio:fim]
  contactgroup_name = re.findall("contactgroup_name\t\t\t(.+?)\n",l)[0]
  alias = re.findall("alias\t\t\t\t(.+?)\n",l)
  if len(alias) == 0:
    alias = re.findall("alias\t\t\t\t(.+?)$",l)[0]    
  else:
    alias = alias[0]
  print "/usr/local/centreon/www/modules/centreon-clapi/core/centreon -u alvin -p abc@123 -o CG -a ADD -v \"%s;%s\""%(contactgroup_name,alias)
  data=data[fim+len(p2):]
