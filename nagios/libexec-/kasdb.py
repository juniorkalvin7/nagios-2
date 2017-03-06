#!/usr/bin/env python
# *-* coding:utf-8 *-*

import _mssql
import sys, os,datetime
from socket import *
#requer instalacao do pymssql 1.0.2
#http://pypi.python.org/packages/source/p/pymssql/pymssql-1.0.2.tar.gz#md5=04dc4aa591acacbc8f183daeea21b690
#dependencias pra compilacao 
#debian:apt-get install freetds-dev #centos:yum install freetds-devel.i386 ou freetds-devel.x86_64


class Portcheck:
  def __init__(self, host,port):
    self.host = host
    self.port = port
    self.socket = setdefaulttimeout(30)
    self.sd = socket(AF_INET, SOCK_STREAM)
  def run(self):
    try:
      self.sd.connect((self.host, self.port))
      #res="%s:%d OPEN|ok=1" % (self.host, self.port)
      self.sd.close()
      return True
    except: 
      #res="%s:%d CLOSED|ok=0" % (self.host, self.port)
      #sys.exit(1)
      return False
      #pass



now = datetime.datetime.now()
ano = now.year
mes = now.month

##print """Top Usuarios mais identificados
##<div id="chartdiv"></div>
##<script type="text/javascript">
##var myChart = new FusionCharts("http://cmp.intechne.com.br/cmp/modules/cmp2otrs/MSBar3D.swf", "myChartId", "600", "470", "0", "0");
##myChart.setDataXML("<chart baseFontSize='12' canvasBgAlpha='0' exportEnabled='1' exportAtClient='1' exportAction='download' exportHandler='http://50.56.99.4/cmp/img/animations/stage2.php' palette='2' animation='1' formatNumberScale='0' showValues='1' numDivLines='4' legendPosition='BOTTOM'><categories><category label='SystemAccount' /><category label='NTCOMERCIAL\\Fábio Silva' /><category label='SystemAccount' /><category label='SystemAccount' /><category label='SystemAccount' /><category label='SystemAccount' /><category label='SystemAccount' /></categories><dataset seriesName=''><set value='12' /><set value='8' /><set value='6' /><set value='6' /><set value='5' /><set value='2' /><set value='1' /></dataset></chart>");
##myChart.render("chartdiv");																			 
##</script></div>
##"""
##sys.exit(0)

def topuser():
  #print usuarioDB
  #conexao = _mssql.connect(user=usuarioDB, password=senhaDB, server='%s:%s'%(ipDB,portaDB), database=databaseDB)
  conexao = _mssql.connect('%s:%s'%(ipDB,portaDB),usuarioDB, senhaDB)
  conexao.select_db(databaseDB)
  conexao.execute_query("""
  Select TOP 10 
         ISNULL(dbo.rpt_viract_index.wstrAccount,'SystemAccount') as Nome, 
         count(dbo.rpt_viract_index.nHostId) as Quantidade 
         From dbo.Hosts    JOIN dbo.rpt_viract_index  
          on dbo.Hosts.nId = dbo.rpt_viract_index.nHostId 
         where MONTH(dbo.rpt_viract_index.tmVirusFoundTime) = """+str(mes)+"""  and YEAR(dbo.rpt_viract_index.tmVirusFoundTime) = """+str(ano)+"""
         group by dbo.rpt_viract_index.nHostId, dbo.rpt_viract_index.wstrAccount 
          order by Quantidade desc
          
          """)
  infect_list=[]
  print "Top Usuarios mais identificados"
  for row in conexao:
    #print str(row['Nome']),str(row['Quantidade'])
    infect_list.append([str(row['Nome']).replace('\\','\\\\'),str(row['Quantidade'])])
  corpo="""<div id="chartdiv"></div>\n"""
  corpo+="""<script type="text/javascript">\n"""
  corpo+="""var myChart = new FusionCharts("http://cmp.intechne.com.br/cmp/modules/cmp2otrs/Bar2D.swf","""+\
       """"myChartId", "600", "470", "0", "0");\n"""
  corpo+="""myChart.setDataXML("<chart baseFontSize='12' canvasBgAlpha='0' exportEnabled='1' exportAtClient='1' """+\
       """exportAction='download' exportHandler='http://50.56.99.4/cmp/img/animations/stage2.php' """+\
       """palette='2' animation='1' formatNumberScale='0' showValues='1' numDivLines='4' """+\
       """legendPosition='BOTTOM'>"""
  #for x in infect_list:
    #corpo+="<category label='"+x[0]+"' />"
  #corpo+="</categories>"
  #corpo+="<dataset seriesName=''>"
 # print 'infect_list %s'%len(infect_list)
  if len(infect_list) == 0:
    corpo = """<span color='green'>Não Foram Encontradas Ameaças!</span>"""
  else:
    for x in infect_list:
  #    print 'Aqui %s %s'%(x[0],x[1])
      corpo+="<set label='"+x[0]+"' value='"+x[1]+"' />"

    corpo+="""</chart>");
    myChart.render("chartdiv");
</script></div>"""
  print corpo
  
def topmaq():
  #print usuarioDB
  #conexao = _mssql.connect(user=usuarioDB, password=senhaDB, server='%s:%s'%(ipDB,portaDB), database=databaseDB)
  conexao = _mssql.connect('%s:%s'%(ipDB,portaDB),usuarioDB, senhaDB)
  conexao.select_db(databaseDB)
  conexao.execute_query("""
  Select TOP 10 
       dbo.Hosts.strWinHostName as Nome, 
       count(dbo.rpt_viract_index.nHostId) as Quantidade 
       From dbo.Hosts JOIN dbo.rpt_viract_index  
        on dbo.Hosts.nId = dbo.rpt_viract_index.nHostId 
        where MONTH(dbo.rpt_viract_index.tmVirusFoundTime) = """+str(mes)+"""  and YEAR(dbo.rpt_viract_index.tmVirusFoundTime) = """+str(ano)+"""
       group by dbo.Hosts.strWinHostName,dbo.rpt_viract_index.nHostId
        order by Quantidade desc
          
          """)
  infect_list=[]
  print "Top Maquinas mais identificadas"
  for row in conexao:
    #print str(row['Nome']),str(row['Quantidade'])
    infect_list.append([str(row['Nome']).replace('\\','\\\\'),str(row['Quantidade'])])
  corpo="""<div id="chartdiv"></div>\n"""
  corpo+="""<script type="text/javascript">\n"""
  corpo+="""var myChart = new FusionCharts("http://cmp.intechne.com.br/cmp/modules/cmp2otrs/Bar2D.swf","""+\
       """"myChartId", "600", "470", "0", "0");\n"""
  corpo+="""myChart.setDataXML("<chart baseFontSize='12' canvasBgAlpha='0' exportEnabled='1' exportAtClient='1' """+\
       """exportAction='download' exportHandler='http://50.56.99.4/cmp/img/animations/stage2.php' """+\
       """palette='2' animation='1' formatNumberScale='0' showValues='1' numDivLines='4' """+\
       """legendPosition='BOTTOM'>"""
  #for x in infect_list:
    #corpo+="<category label='"+x[0]+"' />"
  #corpo+="</categories>"
  #corpo+="<dataset seriesName=''>"
  if len(infect_list) == 0:
    corpo = """<span color='green'>Não Foram Encontradas Ameaças!</span>"""
  else:
    for x in infect_list:
        corpo+="<set label='"+x[0]+"' value='"+x[1]+"' />"
    corpo+="""</chart>");
    myChart.render("chartdiv");
</script></div>"""
  print corpo
  
def topvir():
  #print usuarioDB
  #conexao = _mssql.connect(user=usuarioDB, password=senhaDB, server='%s:%s'%(ipDB,portaDB), database=databaseDB)
  conexao = _mssql.connect('%s:%s'%(ipDB,portaDB),usuarioDB, senhaDB)
  conexao.select_db(databaseDB)
  conexao.execute_query("""
  Select  TOP 10 wstrVirusName as Nome,count(wstrVirusName) as Quantidade 
        From dbo.rpt_viract_index
        where MONTH(dbo.rpt_viract_index.tmVirusFoundTime) = """+str(mes)+"""  and YEAR(dbo.rpt_viract_index.tmVirusFoundTime) = """+str(ano)+"""
        group by wstrVirusName 
        order by Quantidade desc
          """)
  infect_list=[]
  print "Top Virus identificados no mes"
  for row in conexao:
    #print str(row['Nome']),str(row['Quantidade'])
    infect_list.append([str(row['Nome']).replace('\\','\\\\'),str(row['Quantidade'])])
  corpo="""<div id="chartdiv"></div>\n"""
  corpo+="""<script type="text/javascript">\n"""
  corpo+="""var myChart = new FusionCharts("http://cmp.intechne.com.br/cmp/modules/cmp2otrs/Bar2D.swf","""+\
       """"myChartId", "600", "470", "0", "0");\n"""
  corpo+="""myChart.setDataXML("<chart baseFontSize='12' canvasBgAlpha='0' exportEnabled='1' exportAtClient='1' """+\
       """exportAction='download' exportHandler='http://50.56.99.4/cmp/img/animations/stage2.php' """+\
       """palette='2' animation='1' formatNumberScale='0' showValues='1' numDivLines='4' """+\
       """legendPosition='BOTTOM'>"""
  #for x in infect_list:
    #corpo+="<category label='"+x[0]+"' />"
  #corpo+="</categories>"
  #corpo+="<dataset seriesName=''>"
  if len(infect_list) == 0:
    corpo = """<span color='green'>Não Foram Encontradas Ameaças!</span>"""
  else:
    for x in infect_list:
        corpo+="<set label='"+x[0]+"' value='"+x[1]+"' />"
    corpo+="""</chart>");
    myChart.render("chartdiv");
</script></div>"""
  print corpo


  
    
    
args = sys.argv[1:]
def helpmsg():
  print "Centreon Plugin\nGetDB Info 1.1 por GemayelLira"
  print 'Args:\ntopvir Top de Virus mais identificados Mes'
  print 'topuser Top de Usuarios mais identificados Mes'
  print 'topmaq Top de Maquinas mais identificadas Mes'
  print "Argumentos:\npython ./%s ipDB usuarioDB senhaDB portaDB databaseDB infotype" % sys.argv[0]
  print "Ex.\npython ./%s 192.168.0.230 monitoramento Labsecur1t1 57743 KAV topvir" % sys.argv[0] 
  sys.exit(1)

if len(args)<5:
  helpmsg()
else:
  ipDB=args[0]
  if ipDB=='--help':helpmsg()
  usuarioDB=args[1]
  senhaDB=args[2]
  portaDB=args[3]
  databaseDB=args[4]
  infotype=args[5]
  
res=Portcheck(ipDB,int(portaDB)).run()
if res is False:
  print 'CRITICAL - Porta do banco %s fechada, verifique ou mude manualmente' % portaDB
  sys.exit(1)

try:
  eval('%s()'%infotype)
except Exception,e:
  print 'CRITICAL - Metodo incorreto!\n',e
  sys.exit(2)


#print 'feito!'
