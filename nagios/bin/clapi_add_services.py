#!/usr/bin/python
import sys
import re
arq =  sys.argv[1:][0]
#arq, satelite = "hosts.cfg","Satelite_Rebocadores"
#arq  = "udi_conf/services.cfg"
data = open(arq,'r').read()
p1="define service{"
p2="\n}\n"
print "Abrindo",arq
while True:
  try:
    inicio = data.index(p1)+len(p1)
  except:break
  fim = data.index(p2)
  l = data[inicio:fim]
  host_name = re.findall("host_name\t\t\t\t(.+?)\n",l)[0]
  service_description = re.findall("service_description\t\t(.+?)\n",l)[0]
  if "use" in l:
    use = re.findall("use\t\t\t\t(.+?)\n",l)
    if len(use)==0:
      use = re.findall("use\t\t\t\t(.+?)$",l)[0]
    else:
      use = use[0]
    #print "1-",host_name,service_description,use
    print "centreon -u alvin -p abc@123 -o SERVICE -a add -v '%s;%s;%s'"%(host_name,service_description,use)
  
  if "check_command" in l:
    check_command1 = re.findall("check_command\t\t\t(.+?)!",l)
    if len(check_command1) ==0:
      check_command1 = re.findall("check_command\t\t\t(.+?)$",l)
      if len(check_command1)==0:
        check_command1 = re.findall("check_command\t\t\t(.+?)\n",l)[0]
      else:
        check_command1 = check_command1[0]
    else:
      check_command1 = check_command1[0]
      
    #print "2-",host_name,service_description,"check_command",check_command1
    print "centreon -u alvin -p abc@123 -o SERVICE -a setparam -v '%s;%s;%s;%s'"%(host_name,service_description,"check_command",check_command1)
    if "%s!"%check_command1 in l:
      check_command2 = re.findall("%s!(.+?)$"%check_command1,l)
      if len(check_command2)==0:
        check_command2 = re.findall("%s!(.+?)\n"%check_command1,l)[0]
      else:
        check_command2 = check_command2[0]
      print "centreon -u alvin -p abc@123 -o SERVICE -a setparam -v '%s;%s;%s;!%s'"%(host_name,service_description,"check_command_arguments",check_command2)
    
  data=data[fim+len(p2):]
