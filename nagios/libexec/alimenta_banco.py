#!/usr/bin/env python
# -*- coding: utf-8 -*-
from calendar import monthrange
import datetime, time
import MySQLdb

def realiza_consulta(c,sql):
  c.execute(sql)
  return c.fetchall()

cliente_cmp = "Maciel"

#con = MySQLdb.connect(host='23.253.160.254', user='relatorio', passwd='W2bVC6oFZP',db='centreon') 
con = MySQLdb.connect(host='127.0.0.1', user='relatorio', passwd='',db='centreon')
#con = MySQLdb.connect(host='23.253.160.254', user='relatorio',db='centreon')


c = con.cursor()

#
#Selecionando os nomes dos grupos de um determinado cliente
#
sql = '''select hg_id,hg_name, hg_alias,hg_comment  from centreon.hostgroup where hg_name like "%'''+cliente_cmp+'''%" order by hg_name''';
grupos = realiza_consulta(c,sql)

aux_elementos = []
elementos = []
elementos_grupos = []
grupos_filtragem = []

for r in grupos:
  #print str(r[0]) + ' ' + str(r[1])
  id_grupo = str(r[0])
  nome_grupo = str(r[1])
  alias_grupo = str(r[2])
  comment = str(r[3])
  #
  # Selecionando todos os elementos de um determinado grupo
  #
  sql = '''select host_name,current_state,alias, address,host_comment from centstatus.nagios_hosts join centstatus.nagios_hoststatus 
	   join centreon.host
           on centstatus.nagios_hosts.host_object_id = centstatus.nagios_hoststatus.host_object_id 
	   and centreon.host.host_name = centstatus.nagios_hosts.display_name
           where centstatus.nagios_hosts.display_name in (    select host_name from centreon.host where host_id in (
           select host_host_id from centreon.hostgroup_relation where hostgroup_hg_id in (
	   select hg_id from centreon.hostgroup where hg_name = "'''+nome_grupo+'''"))) ORDER BY alias'''
  grupos_elementos = realiza_consulta(c,sql)
  
  #
  #Selecionando o estado de cada servico de cada elemento do grupo
  #
  
  qtd_ok = 0;
  qtd_critical = 0;
  cont_ok_total = 0;
  cont_problema_total = 0;
  for re in grupos_elementos:
   # print str(re[0]) + ' ' + str(re[1])  + ' ' + str(re[2]) + ' ' + str(re[3])
    display_name = re[0] ;
    current_state = re[1];
    alias = re[2];
    address =  re[3];
    comentario = re[4];
    sql = '''select current_state,count(current_state) from centstatus.nagios_servicestatus as t1 
	      join centstatus.nagios_services as t2 join centstatus.nagios_hosts as t3 
	      on t1.service_object_id = t2.service_object_id and t2.host_object_id = t3.host_object_id  
	      where t3.display_name = "'''+ display_name +'''" and last_check >= (now() - INTERVAL 5 MINUTE) group by current_state;'''
    #print sql
    estado_atual_servicos = realiza_consulta(c,sql)
    
    cont_ok = 0
    cont_problema = 0
    for estado in estado_atual_servicos:
      if (estado[0] == 0):
	cont_ok +=  estado[1]
      else:
	cont_problema +=  estado[1]

    cont_ok_total +=  cont_ok
    cont_problema_total += cont_problema
    
    if current_state == 0:
      qtd_ok +=  1
    if current_state == 1: 
      qtd_critical +=1
      
    if display_name not in aux_elementos: 
      #print 
      if len(display_name) > 5:
	aux_elementos.append(display_name)
	elementos.append(display_name + '*' + str(current_state) +'*'+ str(alias) +'*'+ str(address) + '*' + ("critico;" if str(comentario).find('critico')!=-1 else '-'));
	elementos_grupos.append(display_name + '*' + str(nome_grupo) + '*' + str(current_state) + '*' + str(alias) + '*' + str(address) + '*' + ("critico;" if str(comentario).find('critico')!=-1 else '-') + '*' + (str(cont_ok) if cont_ok > 0 else '-') + '*' + (str(cont_problema) if cont_problema > 0 else '-'))
   
  grupos_filtragem.append(str(id_grupo) + '*' +str(nome_grupo) + '*' + str(alias_grupo) + '*' + (str(comment) if len(comment)>0 else "-") + '*' + (str(qtd_ok) if qtd_ok > 0 else '-') +'*'+ (str(qtd_critical) if qtd_critical > 0 else '-') +'*'+ (str(cont_ok_total) if cont_ok_total > 0 else '-') + '*' + (str(cont_problema_total) if cont_problema_total > 0 else '-'))

print len(elementos)    
elementos = list(set(elementos))
# numero de elementos
numero_monitorados = len(elementos)
print numero_monitorados

#
# Grafico Pie: Disponibilidade
#
hoje = datetime.datetime.now()
ano = hoje.year
qtd_dias_mes = monthrange(ano,hoje.month)[1]
date_start = datetime.datetime(hoje.year, hoje.month , 1, 0,0,0)
date_end = datetime.datetime(hoje.year, hoje.month , qtd_dias_mes, 23,59,59)
print str(date_start)
print str(date_end)
dtt = date_start.timetuple()
date_start = time.mktime(dtt)

dtt = date_end.timetuple()
date_end = time.mktime(dtt)


sql = '''SELECT sum(`UPTimeScheduled`) as UP_TOTAL,       
       sum(`DOWNTimeScheduled`) as DOWN_TOTAL,       
       sum(`UNREACHABLETimeScheduled`) as UNREACHABLE_TOTAL,      
       sum(`UNDETERMINEDTimeScheduled`) as UNDETERMINED_TOTAL,
       sum(UPTimeScheduled)+sum(DOWNTimeScheduled)+sum(UNREACHABLETimeScheduled)+sum(UNDETERMINEDTimeScheduled) as TOTALTIME,
       count(host_name) as num_eventos,
        FROM_UNIXTIME(date_end,'''+" '%Y' '%m'"+''') as meses,
        FROM_UNIXTIME(date_end,'''+"'%M'"+''') as mesesName,
        sum(`DOWNnbEvent`) as DOWN_TOTAL_Eventos
            FROM centreon.hostgroup_relation as t1 
                join centreon.host as t2
                join centstorage.log_archive_host as t3
            on t2.host_id = t1.host_host_id 
            and t3.host_id = t2.host_id
            WHERE t1.hostgroup_hg_id = (select hg_id from centreon.hostgroup where hg_name = '''+'''"'''+cliente_cmp+'''"'''+''')
               AND `date_start` >= '''+ '"' +str(date_start) +''' "  
               AND `date_end` <= '''+'"'+str(date_end)+'''"
      group by FROM_UNIXTIME(date_end,'''+ "'%Y' '%m'"+''');''';
print sql
tupla_grafico_pie = realiza_consulta(c,sql)
for t in tupla_grafico_pie:
  for t1 in t:
    print str(t1) + " ",
  print 

print str(date_start)
print str(date_end)
print qtd_dias_mes

###
### FIM Grafico Pie: Disponibilidade
###


#
# Grafico Stacked: stacked
#
hoje = datetime.datetime.now()
ano = hoje.year
qtd_dias_mes = monthrange(ano,hoje.month)[1]
date_start = datetime.datetime(hoje.year, hoje.month-3 , 1, 0,0,0)
date_end = datetime.datetime(hoje.year, hoje.month , qtd_dias_mes, 23,59,59)
print str(date_start)
print str(date_end)
dtt = date_start.timetuple()
date_start = time.mktime(dtt)

dtt = date_end.timetuple()
date_end = time.mktime(dtt)

sql='SELECT sum(`UPTimeScheduled`) as UP_TOTAL,       \
       sum(`DOWNTimeScheduled`) as DOWN_TOTAL,       \
       sum(`UNREACHABLETimeScheduled`) as UNREACHABLE_TOTAL,      \
       sum(`UNDETERMINEDTimeScheduled`) as UNDETERMINED_TOTAL,\
       sum(UPTimeScheduled)+sum(DOWNTimeScheduled)+sum(UNREACHABLETimeScheduled)+sum(UNDETERMINEDTimeScheduled) as TOTALTIME,\
       count(host_name) as num_eventos,       \
        convert(binary convert(FROM_UNIXTIME(date_end,'+" '%Y' '%m'"+') using latin1) using utf8) as meses,\
        FROM_UNIXTIME(date_end,'+"'%M'"+') as mesesName,\
        sum(`DOWNnbEvent`) as DOWN_TOTAL_Eventos\
            FROM centreon.hostgroup_relation as t1 \
                join centreon.host as t2\
                join centstorage.log_archive_host as t3\
            on t2.host_id = t1.host_host_id \
            and t3.host_id = t2.host_id\
            \
            WHERE t1.hostgroup_hg_id = (select hg_id from centreon.hostgroup where hg_name = '+'"'+cliente_cmp+'"'+')\
               AND `date_start` >= '+ '"'+str(date_start)+'"  \
               AND `date_end` <= '+'"'+str(date_end)+'"\
      group by FROM_UNIXTIME(date_end,'+ "'%Y' '%m'"+');';

print sql
tupla_grafico_stacked = realiza_consulta(c,sql)

for t in tupla_grafico_stacked:
  for t1 in t:
    print str(t1) + " ",
  print 
print str(date_start)
print str(date_end)
print qtd_dias_mes


#
# capturando a disponibilidade, estatus atual, servicos ok e com problema de cada um dos elementos
#
for e in elementos_grupos:
  linha_grupos_hosts = e.split('*')
  #for lg in linha_grupos_hosts:
  #  print lg
  nome_grupo = linha_grupos_hosts[1];
  nome_elemento = linha_grupos_hosts[0]; 
  estado_atual = linha_grupos_hosts[2];
  alias = linha_grupos_hosts[3];
  comentarios = linha_grupos_hosts[5];
  ok = linha_grupos_hosts[6];
  problema = linha_grupos_hosts[7];

  sql = 'SELECT  host_name, \
	        sum( `UPTimeScheduled` ) as UPTimeScheduled,\
                avg(`UPTimeScheduled`) as UP_TOTAL_AVG,       \
                sum(`UNREACHABLETimeScheduled`) as UNREACHABLE_TOTAL,\
		sum(`DOWNTimeScheduled`) as DOWN_TOTAL,\
		sum( `MaintenanceTime`) as Manuntencao,\
                sum(`UNDETERMINEDTimeScheduled`) as UNDETERMINED_TOTAL,\
                sum(UPTimeScheduled)+sum(DOWNTimeScheduled)+sum(UNREACHABLETimeScheduled)+sum(UNDETERMINEDTimeScheduled) as TOTALTIME,\
                count(host_name) as num_eventos,\
                FROM_UNIXTIME(date_end,'+"'%Y %m %d'"+') as meses,\
                FROM_UNIXTIME(date_end,'+"'%d'"+') as mesesName,\
                sum(`DOWNnbEvent`) as DOWN_TOTAL_Eventos\
                    FROM centreon.hostgroup_relation as t1 \
                        join centreon.host as t2\
                        join centstorage.log_archive_host as t3\
                    on t2.host_id = t1.host_host_id \
                    and t3.host_id = t2.host_id\
                    WHERE t1.hostgroup_hg_id = (select hg_id from centreon.hostgroup where hg_name = "'+nome_grupo +'")\
                       AND `date_start` >= "'+str(date_start)+'" and t2.host_name = "' +nome_elemento+ '"\
                       AND `date_end` <= "'+str(date_end)+'"\
                group by FROM_UNIXTIME(date_end,'+"'%Y %m %d'"+') ';
  
  print sql
  tupla_elementos = realiza_consulta(c,sql)
  
  cont_total_down = 0;
  cont_total_manutencao = 0;
  cont_total_total = 0;
  cont_total_UNREACHABLE_TOTAL = 0;
  
  tupla_linha_final = [];
  
  for t in tupla_elementos:
    cont_total_down += t[4];
    cont_total_manutencao += t[5];
    cont_total_total += t[7];
    cont_total_UNREACHABLE_TOTAL += t[3];
    cont_total_down += t[6]; #$tupla[$t][6] cont_UNDETERMINED_TOTAL
    cont_total_down += cont_total_UNREACHABLE_TOTAL;
    cont_total_down += cont_total_manutencao;

  
