import sys
import re
arq =  sys.argv[1:][0]
#arq  = "udi_conf/contacts.cfg"
data = open(arq,'r').read()
p1="define contact{"
p2="\n}\n"
#print "Abrindo",arq
while True:
  try:
    inicio = data.index(p1)+len(p1)
  except:break
  fim = data.index(p2)
  l = data[inicio:fim]
  contact_name = re.findall("contact_name\t\t\t(.+?)\n",l)[0]
  alias = re.findall("alias\t\t\t\t(.+?)\n",l)[0]
  email = re.findall("email\t\t\t\t(.+?)\n",l)
  if len(email)==0:
    email = re.findall("email\t\t\t\t(.+?)$",l)[0]    
  else:
    email = email[0]
  print "/usr/local/centreon/www/modules/centreon-clapi/core/centreon -u alvin -p abc@123 -o CONTACT -a ADD -v \"%s;%s;%s;;;;pt_BR.UTF-8;local\"".decode().encode('utf-8')%(contact_name,alias,email)
    
  data=data[fim+len(p2):]
