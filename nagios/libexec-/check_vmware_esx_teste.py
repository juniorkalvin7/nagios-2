#! /usr/bin/env python
# **coding: utf-8 **

import commands, sys

def convert_bytes(bytes):
        bytes = float(bytes)
        if bytes >= 1099511627776:
                terabytes = bytes / 1099511627776
                size = '%.2fT' % terabytes
        elif bytes >= 1073741824:
                gigabytes = bytes / 1073741824
                size = '%.2fG' % gigabytes
        elif bytes >= 1048576:
                megabytes = bytes / 1048576
                size = '%.2fM' % megabytes
        elif bytes >= 1024:
                kilobytes = bytes / 1024
                size = '%.2fK' % kilobytes
        else:
                size = '%.2fb' % bytes
        return size

args = sys.argv[1::]

warning  = 80
critical = 90
    
saida = 0

#print args
versao = "sysDesc"
memoria_total = "hrStorageSize"
memoria_usada = "hrStorageUsed"
uptime = "hrSystemUptime" 
estado_nome_virt = '.1.3.6.1.4.1.6876.2.1.1.2'
estado_virt = '.1.3.6.1.4.1.6876.2.1.1.6'
disco = 'hrStorage'
cpu = '.1.3.6.1.2.1.25.3.3.1.2'

if len(args) == 5:
        community = args[0]
        ip = args[1]
        mib = args[2]
        if str(args[3]).lower() != "none": 
            warning = float(args[3])
            
        if str(args[4]).lower() != "none":
            critical = float(args[4])

        if str(mib) == "versao":
                con = commands.getoutput('snmpwalk -v 2c -c %s %s %s'%(community,ip, versao))
                #print con
                string = str(con)[str(con).find('STRING: ')+8::]
                #print string
                print 'OK - A versão foi lida com sucesso: %s'%string

        elif str(mib) == "memoria":
                num_memoria_total = str(commands.getoutput('snmpwalk -v 2c -c %s %s %s'%(community,ip, memoria_total))).split('\n')[-1]
                num_memoria_total = num_memoria_total[num_memoria_total.find('INTEGER: ')+9::].replace(' ', '')

                num_memoria_usada = str(commands.getoutput('snmpwalk -v 2c -c %s %s %s'%(community,ip, memoria_usada))).split('\n')[-1]
                num_memoria_usada = num_memoria_usada[num_memoria_usada.find('INTEGER: ')+9::].replace(' ', '')
                #print "num_memoria_total: %s num_memoria_usada: %s"%(num_memoria_total, num_memoria_usada)

                warning = int(num_memoria_total)*80/100
                critical = int(num_memoria_total)*90/100
                #print 'warning: %s critical: %s'%(warning,critical)
                if int(num_memoria_usada) >= warning and int(num_memoria_usada) < critical:
                        saida = 1
                        print 'WARNING - Consumo de memória alto!',
                elif int(num_memoria_usada) >= critical:
                        print 'CRITICAL - Consumo de memoria alto!',
                        saida = 2
                else:
                        print 'OK - Consumo de memória normal!',
                print "Memoria_total: %s Memoria_usada: %s | memoria_total=%s memoria_usada=%s"%(convert_bytes(int(num_memoria_total)*1024),convert_bytes(int(num_memoria_usada)*1024),convert_bytes(int(num_memoria_total)*1024),convert_bytes(int(num_memoria_usada)*1024))

        elif str(mib) == 'uptime':
                con = commands.getoutput('snmpwalk -v 2c -c %s %s %s'%(community,ip, uptime))
                #print con
                string = str(con)[str(con).find('HOST-RESOURCES-MIB::hrSystemUptime.0 = ')+39::]
                print 'OK - Uptime do host: %s '%(string)

        elif str(mib) == "estado":
                string = """
                <table BORDER = 2 align=\"center\">
                        <tr>
                                <TH align=\"center\" COLSPAN=2>--------------------------- Estado das VMs ---------------------------</TH>
                        </tr>

                        <tr>
                                <TH>Nome</TH>
                                <TH>Estado</TH>
                        </tr>
                """

                con = commands.getoutput('snmpwalk -v 2c -c %s %s %s'%(community,ip,estado_nome_virt))
                lista_nome_virt = str(con).split('\n')

                con = commands.getoutput('snmpwalk -v 2c -c %s %s %s'%(community,ip,estado_virt))
                lista_virt = str(con).split('\n')

                #print 'lista_nome_virt %s lista_virt %s'%(len(lista_nome_virt), len(lista_virt))
                #print lista_nome_virt
                #print lista_virt

                if len(lista_nome_virt) == len(lista_virt):
                        for l in range(0,len(lista_nome_virt)):
                                nome = str(lista_nome_virt[l])[str(lista_nome_virt[l]).find('"')+1:len(str(lista_nome_virt[l]))-1]
                                estado = str(lista_virt[l])[str(lista_virt[l]).find('"')+1:len(str(lista_virt[l]))-1]
                                string = string + '<tr align=\"Center\"> <td>%s</td> <td>%s</td>  </tr>'%(nome, estado)

                string = string + '</table>'
                string = string.replace('\n','')

                print 'OK - Estado das VMs lido com sucesso! \n %s '%(string)
                saida = 0

        elif str(mib) == "disco":
                con = commands.getoutput('snmpwalk -v 2c -c %s %s %s'%(community,ip,disco))
                if "No Response" in str(con):
                        print "CRITICAL - Sem comunicação via snmp: %s"%str(con)
                        saida = 2

                else:
                        lista = str(con).split('\n')
                        lista_nome_disco = []
                        lista_tam_total = []
                        lista_tam_usado = []
                        for l in lista:
                                if "FixedDisk" in l:
                                        numero_disco = str(str(l.split(':')[2]).split()[0]).split('.')[-1]
                                        lista_nome_disco.append(numero_disco)



                        #print lista_nome_disco
                        for l in lista_nome_disco:
                                for x in lista:
                                        if "hrStorageSize.%s"%l == str(x.split('::')[1]).split()[0]:
                                                #print "hrStorageSize.%s x = %s"%(l,x)
                                                lista_tam_total.append(str(x.split('::')[1]).split()[-1])
                                        if "hrStorageUsed.%s"%l == str(x.split('::')[1]).split()[0]:
                                                #print "hrStorageUsed.%s x %s= "%(l,x)
                                                lista_tam_usado.append(str(x.split('::')[1]).split()[-1])

                        string = """
                        <!doctype html>
                        <head>  <meta charset="UTF-8"> </head>
                        <body>
                                <table BORDER = 2 align=\"center\">
                                        <tr>
                                                <TH align=\"center\" COLSPAN=4>--------------------------- Ocupa&ccedil;&atilde;o dos Discos ---------------------------</TH>
                                        </tr>

                                        <tr>
                                                <TH>Identifica&ccedil;&atilde;o</TH>
                                                <TH>Tamanho total</TH>
                                                <TH>Tamanho usado</TH>
                                                <TH>Porcentagem de Ocupa&ccedil;&atilde;o</TH>
                                        </tr>
                        """
                        msg = ""
                        graf = ""
                        if (len(lista_nome_disco) == len(lista_tam_total) == len(lista_tam_usado)):
                                for i in range(0, len(lista_nome_disco)):
                                        nome = lista_nome_disco[i]
                                        tam_total = lista_tam_total[i]
                                        tam_usado = lista_tam_usado[i]
                                        porcentagem = (float(lista_tam_usado[i])*100)/float(lista_tam_total[i])
                                        #print "nome disco hrStorageIndex-FixedDisk.%s tam total %s tam usado %s porcentagem %.2f"%(nome,tam_total,tam_usado, porcentagem)
                                        string = string + '<tr align=\"Center\"> <td>hrStorageIndex-FixedDisk.%s</td> <td>%.2f GB</td>  <td>%.2f GB</td> <td>%.2f%%</td> </tr>'%(nome, float(tam_total)/1024,float(tam_usado)/1024, porcentagem)

                                        if float(porcentagem) >= float(warning) and porcentagem < float(critical) and saida !=2:
                                                #print porcentagem
                                                saida = 1
                                        elif float(porcentagem) >= float(critical):
                                                saida = 2
                                        #msg = msg + " -- disco: hrStorageIndex-FixedDisk.%s - porcentagem %.2f%%, "%(nome,porcentagem)
                                        graf = graf + " hrStorageIndex-FixedDisk.%s=%.2f;; "%(nome,porcentagem)
                        if saida == 1:
                                msg = "WARNING - Disco(s) com %s%% de ocupação | "%warning +graf
                        if saida == 2:
                                msg = "CRITICAL - Disco(s) com %s%% de ocupa&#231&#227o | "%critical +graf
                        if saida == 0:
                                msg = "OK - Disco(s) com valores de ocupa&#231&#227o dentro do esperado. | "+graf

                        #msg = msg.replace(" - -- ","-").replace(' -- ','')
                        string = string + '</table> </body>'

                        string = string.replace('\n','')
                        print msg.replace(',  |  ',' | ').replace('  ',' ')
                        print string
                        #print "lista_tam_total %s"%lista_tam_total
                        #print "lista_tam_usado %s"%lista_tam_usado

        elif str(mib) == "cpu":
                #num_memoria_total = str(commands.getoutput('snmpwalk -v 2c -c %s %s %s'%(community,ip, cpu))).split('\n')[-1]
                lista_cpus = str(commands.getoutput('snmpwalk -v 2c -c %s %s %s'%(community,ip, cpu)))
		
		if 'timeout' in lista_cpus.lower():
			print "WARNING - Timeout ao tentar comunicacao."
			print "Parametros possivelmente incorretos:\n  ip=%s \n  Community:%s \n  mib_cpu:%s"%(community,ip, cpu)
			sys.exit(1)
		lista_cpus = lista_cpus.split('\n')
		cont = 1
		string = ''
                string_perf = ''
		for l in lista_cpus:
           		string = string + 'core%s='%cont + str(l.split(': ')[1]) +'%\n'
			string_perf = string_perf + 'core%s='%cont + str(l.split(': ')[1]) +'% '
                        cont += 1
                print "OK - Dados de cpu lidos com sucesso.\n%s | %s"%(string, string_perf)
		saida = 0

                #        print 'OK - Consumo de memória normal!',
                #print "Memoria_total: %s Memoria_usada: %s | memoria_total=%s memoria_usada=%s"%(convert_bytes(int(num_memoria_total)*1024),convert_bytes(int(num_memoria_usada)*1024),convert_bytes(int(num_memoria_total)*1024),convert_bytes(int(num_memoria_usada)*1024))

                         
else: 
        print 'WARNING - Parâmetros digitados de forma incorreta.\nDigite no seguinte formato:\n %s community ip mib valor_warning valor_critico'%sys.argv[0]
	print 'mibs possiveis: versao, memoria, estado, disco, uptime'

#print saida

sys.exit(saida)

