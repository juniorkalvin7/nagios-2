#!/usr/bin/python
import sys
import re
arq =  sys.argv[1:][0]
#arq, satelite = "hosts.cfg","Satelite_Rebocadores"
#arq  = "udi_conf/checkcommands.cfg"
data = open(arq,'r').read()
p1="define command{"
p2="\n}\n"
#print "Abrindo",arq
while True:
  try:
    inicio = data.index(p1)+len(p1)
  except:break
  fim = data.index(p2)
  l = data[inicio:fim]
  command_name = re.findall("command_name\t\t\t(.+?)\n",l)[0]
  command_line = re.findall("command_line\t\t\t(.+?)\n",l)
  if len(command_line) ==0:
    command_line = re.findall("command_line\t\t\t(.+?)$",l)[0]
  else:
    command_line = command_line[0]
  print "/usr/local/centreon/www/modules/centreon-clapi/core/centreon -u alvin -p abc@123 -o CMD -a ADD -v \"%s;check;%s\""%(command_name,command_line)
    
  data=data[fim+len(p2):]
