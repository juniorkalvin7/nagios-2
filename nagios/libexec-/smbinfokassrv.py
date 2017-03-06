#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
#os.environ['DISPLAY']=':0.0'
import numpy as np
#import matplotlib
#matplotlib.use('Agg')
#import matplotlib.pyplot as plt
#import pylab
import datetime
import sys

import commands,codecs,time
from lxml import etree
from unicodedata import normalize 
import dateutil.relativedelta
import calendar

import pickle



"""
requer no minimo python 2.5
requer:
apt-get install python-dateutil

requer no centos:
python-numpy.i386 0:1.0.1-1.el5.rf
python-matplotlib.i386
python-lxml.i386

/etc/sudoers
nagios   ALL=NOPASSWD: /usr/bin/smbmount

centos:
nagios   ALL=NOPASSWD: /bin/mount

Tipos de saida: 
0 ok
1 warning
2 critical
3 unknown
"""
xmlfile='/media/kas/report_kas_dia.xml'#intechne
#xmlfile='/media/kas/report_kav_dia.xml'#saude

def incrementafile(logfile,zerar):#incrementa nomes de maquina/virus no monitoramento
  
  if os.path.isfile(logfile):
    lastatu_old=open(logfile,'r').readlines()[-1]
    
    if zerar==1:
      #print 'Zerando'
      dict1=pickle.load(open(logfile))
      for item in dict1: dict1[item] = 0
      pickle.dump(dict1,open(logfile,"wb"))
      open(logfile,'a').write('\n'+lastatu_old)
      return

    #print 'Existe'
    #lista=[]
    #print lastatu_old
    #sys.exit(1)
    if len(virus) == 0:
      #print 'Sem virus novo'
      return
    lastatu=virus[0]
    if lastatu_old == lastatu:
      #print 'Nao houve atualizacao no arquivo'
      return
    
    try:
      virus.pop(0)
    except:print 'sem virus para remover l:73'

    dict1=pickle.load(open(logfile))

    #try: 
        #dict1[virus[0]]=1
    #except:
        #dict1[
    #print dict1
    for item in set(virus):
      try:
        dict1[item] = dict1[item]+virus.count(item)
      except:
        dict1[item] = virus.count(item)
    #print dict1
    pickle.dump(dict1,open(logfile,"wb"))
    open(logfile,'a').write('\n'+lastatu)
    #os.system('rm -rf %s' % logfile)
  
  else:
    #lista=[]
    lastatu=virus[0]
    try:
      virus.pop(0)
    except:print 'sem virus para remover l:94'
    dict1= {}
    for item in set(virus): dict1[item] = virus.count(item)
    #print dict1
    #open(logfile,'w').write(str(dict1))
    pickle.dump(dict1,open(logfile,"wb"))
    open(logfile,'a').write('\n'+lastatu)
    #dict1['pedro']=10
    #print dict1
    
def lerviruslog(tipo):#ler arquivo xml
  def asciize(s):
    """ 
    Converts a entire string to a ASCII only string.
   
    string
        The string to be converted.
    """
    _table = {
      "á" : "a", "à" : "a", "â" : "a", "ä" : "a", "ã" : "a", "å" : "a",
      "é" : "e", "è" : "e", "ê" : "e", "ë" : "e",
      "í" : "i", "ì" : "i", "î" : "i", "ï" : "i",
      "ó" : "o", "ò" : "o", "ô" : "o", "ö" : "o", "õ" : "o", "ø" : "o", 
      "ú" : "u", "ù" : "u", "û" : "u", "ü" : "u",
      "ñ" : "n", "ç" : "c",
      "Á" : "A", "À" : "A", "Â" : "A", "Ä" : "A", "Ã" : "A", "Å" : "A",
      "É" : "E", "È" : "E", "Ê" : "E", "Ë" : "E", 
      "Í" : "I", "Ì" : "I", "Î" : "I", "Ï" : "I", 
      "Ó" : "O", "Ò" : "O", "Ô" : "O", "Ö" : "O", "Õ" : "O", "Ø" : "O",
      "Ú" : "U", "Ù" : "U", "Û" : "U", "Ü" : "U", 
      "Ñ" : "N", "Ç" : "C",
      "ß" : "ss", "Þ" : "d" , "æ" : "ae"
    }
  
    for original, plain in _table.items():
      s = s.replace(original, plain)
    return s
  virus=[]
  if os.path.isfile(xmlfile):
    root = etree.fromstring(asciize(codecs.open(xmlfile, 'r',"utf-8").read().encode('utf8')))
    qtelements=len(list(root.iter()))
    limite=(113)
    i=0
    salto=0
    ok=0
    for element in root.iter():#rotina de leitura de infeccoes
      if i ==84:#ultima atu
        virus.append(element.text)
      if element.text != None and element.text.count('IP address'):ok=1      
      if ok>0:ok+=1    
      if ok>3:
        salto+=1
        if salto==2 and tipo =='maquina':
          nome_machine=element.text
          virus.append(nome_machine)
        if salto==4 and tipo =='virus':
          nome_virus=element.text
          virus.append(nome_virus)
        if salto==13:
          salto=0
      i+=1
    return virus
  else:
    
    #return 'CRITICAL NAO CONSEGUI LER ARQUIVO XML DE VIRUS'
    print 'CRITICAL NAO CONSEGUI LER ARQUIVO XML DE VIRUS'
    sys.exit(1)






args = sys.argv[1:]

if len(args)<1:
  print "Centreon Plugin\nTop Kaspersky V&iacute;rus por GemayelLira"
  print "Argumentos:hostname tipo"
  print "tipo 1 #top virus quantidade"
  print "tipo 2 #top virus por nome"
  print "Ex.\n%s 1" % sys.argv[0] 
  #print 
  sys.exit(1)
else:
  #print args
  ip=args[0]
  tipo=args[1]

data1=commands.getoutput('mount')
if not data1.count('PORT'):
  os.system('sudo smbmount //192.168.0.230/KAS-REPPORT /media/kas/ -o username=report,password=2nt3cHn3')#intechne
  #os.system('sudo mount -t cifs -o username=kaspersky,password=suportesaude  //192.168.3.188/KAV-REPORT /media/kas/')#saude
  data1=commands.getoutput('mount')
  if not data1.count('PORT'):
    print 'CRITICAL - SMB-KAS Nao consegui montar particao'
    sys.exit(1)
os.system('rm -rf /media/kas/*.png')

pathlogs='/var/lib/centreon/centplugins/'

def graphparserpizza(filename):#responsavel pela criacao do grafico
  if filename.count('7dias'):
    titulo='Relat&oacute;rio &Uacute;ltimos 7 Dias'
  elif filename.count('ano'):
    titulo='Relat&oacute;rio Anual'
  elif filename.count('mes'):
    titulo='Relat&oacute;rio M&ecirc;s'
  else:
    titulo='Padrao desconhecido Titulo incorreto'
  dict1=pickle.load(open(filename))
  labels=[]
  fracs=[]
  explode=[]
  exitcounter=0
  for i in sorted(dict1.items(), cmp=lambda x,y: int(y[1]) - int(x[1])):
    labels.append(i[0].replace('Backdoor','BD').replace('Win32','W32'))
    fracs.append(i[1])
    explode.append(0)
    if exitcounter >=9:break
    else:exitcounter=exitcounter+1
  fig = plt.figure()
  ax = fig.add_subplot(111)
  ax.set_xlabel('gerado em %s' % datetime.datetime.now())  
  ax.set_title(titulo)
  if filename.count('vir'):
    ax.text(1.00, -1.1,'BD = Backdoor\nW32 = Win32',
            horizontalalignment = 'left',
            verticalalignment = 'center')
  
  pylab.pie(fracs, explode=explode, labels=labels, autopct='%1.1f%%', shadow=False,labeldistance=1.02)
  #plt.show() 
  plt.savefig(filename+'.png', dpi=80)

  
def graphparser(filename):#responsavel pela criacao do grafico #modificado para gerar xml
  if filename=='QUANTITATIVODIA':
    titulo='Relat&#243;rio Dia'
  if filename.count('graph_7dias'):
    titulo='Relat&#243;rio &#218;ltimos 7 Dias'
  elif filename.count('graph_ano'):
    titulo='Relat&#243;rio Anual'
  elif filename.count('graph_mes'):
    titulo='Relat&#243;rio M&#234;s'
  else:
    titulo='Padrao desconhecido Titulo incorreto'
  if filename == 'QUANTITATIVODIA':
    filename='%skas_%s_graph_dia_' % (pathlogs,ip)
    
    vir=open('%skas_%s_top_dia_susp' % (pathlogs,ip)).read().split(':::')[0]
    susp=open('%skas_%s_top_dia_vir' % (pathlogs,ip)).read().split(':::')[0]
    xmldata="""<chart caption='Relat&#243;rio do Dia' shownames='1' showvalues='0' decimals='0' numberPrefix=''><categories>
<category label='Dia'/></categories>
<dataset seriesName='V&#237;rus' color='AFD8F8' showValues='0'>
<set value='"""+vir+"""' /></dataset>
<dataset seriesName='Suspeitos' color='F6BD0F' showValues='0'>
<set value='"""+susp+"""' /></dataset>
</chart>
"""
    open(filename+'.xml','w').write(xmldata)

  else:
    data=open(filename,'r').read()
    N = data.count(';')
    labels=list('<category label=\'%s\'/>' % i.split(',')[2] for i in data.split(';')[:-1])
    virus=list('<set value=\'%s\' />' % (i.split(',')[0]) for i in data.split(';')[:-1])
    susp=list('<set value=\'%s\' />' % (i.split(',')[1]) for i in data.split(';')[:-1])

    virusStd=[]
    for i in virus:
      if i>=1 and i<10:virusStd.append(0)
      elif i>0 and i>=10:virusStd.append(2)
      else:virusStd.append(0)
      
    suspStd=[]
    for i in susp:
      if i>=1 and i<10:suspStd.append(0)
      elif i>0 and i>=10:suspStd.append(2)
      else:suspStd.append(0)
    
    data="<chart caption='%s' shownames='1' showvalues='0' decimals='0' numberPrefix=''><categories>\n" % titulo
    data+=''.join(labels)+'</categories>\n'
    data+="<dataset seriesName='V&#237;rus' color='AFD8F8' showValues='0'>\n"
    data+=''.join(virus)+'</dataset>\n'
    data+="<dataset seriesName='Suspeitos' color='F6BD0F' showValues='0'>\n"
    data+=''.join(susp)+'</dataset>\n'
    data+='</chart>'
  
    open(filename+'.xml','w').write(data)
  
    
  ###ind = np.arange(N)  # the x locations for the groups
  ###width = 0.35       # the width of the bars
  
  ###fig = plt.figure()
  ###ax = fig.add_subplot(111)
  ###rects1 = ax.bar(ind, virus, width, color='r', yerr=virusStd)
  ###rects2 = ax.bar(ind+width, susp, width, color='y', yerr=suspStd)
  #### add some
  ###ax.set_ylabel('Incidencia de V&iacute;rus')
  ###ax.set_title(titulo)
  ###ax.set_xticks(ind+width)
  ####ax.set_xticklabels( ('Seg', 'Ter', 'Qua', 'Qui', 'Sex','Sab', 'Dom') )
  ###ax.set_xticklabels( labels )
  ###ax.set_xlabel('gerado em %s' % datetime.datetime.now())
  
  ###ax.legend( (rects1[0], rects2[0]), ('Infectado', 'Suspeitos') )
  
  ###def autolabel(rects):
    #### attach some text labels
    ###for rect in rects:
      ###height = rect.get_height()
      ###ax.text(rect.get_x()+rect.get_width()/2., 1.05*height, '%d'%int(height), 
      ###ha='center', va='bottom')
      
  ###autolabel(rects1)
  ###autolabel(rects2)
  ###plt.savefig(filename+'.png', dpi=80)  
  #plt.show()

def convertdia(dia):
  if   dia=='Monday':return 'Seg'
  elif dia=='Tuesday':return 'Ter'
  elif dia=='Wednesday':return 'Qua'
  elif dia=='Thursday':return 'Qui'
  elif dia=='Friday':return 'Sex'
  elif dia=='Saturday':return 'Sab'
  elif dia=='Sunday':return 'Dom'
  else:return 'DIA INVALIDO %s' % dia
  
def convertmes(mes):
  if mes == 'janeiro':return '1'
  elif mes =='fevereiro':return '2'
  elif mes.count("mar"):return '3'
  elif mes == 'abril':return '4'
  elif mes == 'maio':return '5'
  elif mes == 'junho':return '6'
  elif mes == 'julho':return '7'
  elif mes == 'agosto':return '8'
  elif mes == 'setembro':return '9'
  elif mes == 'outubro':return '10'
  elif mes == 'novembro':return '11'
  elif mes == 'dezembro':return '12'
  else:return 'PROBLEMA NO PADRAO MES %s' % mes


if tipo=='1':#5min

  #rotina alimentacao/renovacao diaria
  def lancadia():
    def geradiavir():
      try:
	tvirusdia=open('%skas_%s_top_dia_vir' % (pathlogs,ip),'r').read().split(':::')[0]#pega total virus do dia
      except:
	print 'Arquivo tvirusdia nao criado ainda'
	tvirusdia='0'
      try:
	tsuspdia=open('%skas_%s_top_dia_susp' % (pathlogs,ip),'r').read().split(':::')[0]#pega total suspeitos do dia
      except:tsuspdia='0'
      #rotina 7dias
      strdia=convertdia((datetime.datetime.now()+dateutil.relativedelta.relativedelta(days=-1)).strftime("%A"))
      if os.path.isfile('%skas_%s_graph_7dias' % (pathlogs,ip)):#se o arquivo existe
	data=open('%skas_%s_graph_7dias' % (pathlogs,ip),'r').read().rstrip()#ler e adiciona mais um dia
	if data.count(';')==7:
	  open('%skas_%s_graph_7dias' % (pathlogs,ip),'w').write('%s,%s,%s;' % (tvirusdia,tsuspdia,strdia))
	else:
	  open('%skas_%s_graph_7dias' % (pathlogs,ip),'w').write(data+'%s,%s,%s;' % (tvirusdia,tsuspdia,strdia))
      else:
	open('%skas_%s_graph_7dias' % (pathlogs,ip),'w').write('%s,%s,%s;' % (tvirusdia,tsuspdia,strdia))
	
      #rotina M&ecirc;s 30dias
      strdia=str((datetime.datetime.now()+dateutil.relativedelta.relativedelta(days=-1)).strftime("%d"))#pega dia da semana
      if os.path.isfile('%skas_%s_graph_mes' % (pathlogs,ip)):#se o arquivo existe
	data=open('%skas_%s_graph_mes' % (pathlogs,ip),'r').read().rstrip()#ler e adiciona mais um dia
	if strdia=='01':#se dia 01 cria novo mes
	  open('%skas_%s_graph_mes' % (pathlogs,ip),'w').write('%s,%s,%s;' % (tvirusdia,tsuspdia,strdia))
	else:
	  open('%skas_%s_graph_mes' % (pathlogs,ip),'w').write(data+'%s,%s,%s;' % (tvirusdia,tsuspdia,strdia))
      else:
	open('%skas_%s_graph_mes' % (pathlogs,ip),'w').write('%s,%s,%s;' % (tvirusdia,tsuspdia,strdia))
      
      #rotina ano 365dias
      strmes=str((datetime.datetime.now()+dateutil.relativedelta.relativedelta(days=-1)).strftime("%B"))#pega mes
      if os.path.isfile('%skas_%s_graph_ano' % (pathlogs,ip)):#se o arquivo existe
	data=open('%skas_%s_graph_ano' % (pathlogs,ip),'r').read().rstrip()#ler e adiciona mais um dia
	vet1=data.split(';')[:-1]
	vet2=vet1[-1].split(',')
	icrvir=int(vet2[0])+int(tvirusdia)
	incrsusp=int(vet2[1])+int(tsuspdia)
	
	if data.count(';') ==12:#se dia 01 cria novo mes
	  open('%skas_%s_graph_ano' % (pathlogs,ip),'w').write('%s,%s,%s;' % (tvirusdia,tsuspdia,strmes))
	elif data.count(';') ==1:#se dia 01 cria novo mes
	  if vet1[-1].split(',')[2] == strmes:
	    open('%skas_%s_graph_ano' % (pathlogs,ip),'w').write('%s,%s,%s;' % (icrvir,incrsusp,strmes))	    
	  else:
	    open('%skas_%s_graph_ano' % (pathlogs,ip),'w').write(';'.join(vet1)+';%s,%s,%s;' % (tvirusdia,tsuspdia,strmes))	    	      
	else:
	  if len(vet1[:-1]) ==0:
	    open('%skas_%s_graph_ano' % (pathlogs,ip),'w').write(';'.join(vet1)+';%s,%s,%s;' % (icrvir,incrsusp,strmes))
	  else:
	    if vet1[-1].split(',')[2] == strmes:
	      open('%skas_%s_graph_ano' % (pathlogs,ip),'w').write(';'.join(vet1[:-1])+';%s,%s,%s;' % (icrvir,incrsusp,strmes))	    
	    else:
	      open('%skas_%s_graph_ano' % (pathlogs,ip),'w').write(';'.join(vet1)+';%s,%s,%s;' % (tvirusdia,tsuspdia,strmes))	    	      
      else:
	open('%skas_%s_graph_ano' % (pathlogs,ip),'w').write('%s,%s,%s;' % (tvirusdia,tsuspdia,strmes))

      graphparser('%skas_%s_graph_7dias' % (pathlogs,ip))
      graphparser('%skas_%s_graph_mes' % (pathlogs,ip))
      graphparser('%skas_%s_graph_ano' % (pathlogs,ip))
      
      #graphparserpizza('%skas_name_%s_top_7dias_maq' % (pathlogs,ip))
      #graphparserpizza('%skas_name_%s_top_ano_maq' % (pathlogs,ip))
      #graphparserpizza('%skas_name_%s_top_mes_maq' % (pathlogs,ip))
      
      #graphparserpizza('%skas_name_%s_top_mes_vir' % (pathlogs,ip))
      #graphparserpizza('%skas_name_%s_top_7dias_vir' % (pathlogs,ip))
      #graphparserpizza('%skas_name_%s_top_ano_vir' % (pathlogs,ip))
      
      ano=int(datetime.date.today().strftime("%y"))
      dia=int(datetime.date.today().strftime("%d"))
      mes=int(datetime.date.today().strftime("%m"))
      #int("%d" % (time.mktime(datetime.datetime(ano, mes, dia+1, 0, 0, 0, 0).timetuple())))
      data=datetime.datetime(ano+2000, mes, dia, 0, 0, 0, 0)+dateutil.relativedelta.relativedelta(days=+1)
      open('%skas_%s_top_dia_vir' % (pathlogs,ip),'w').write('0:::%s' % str(data))
      virusdia=open('%skas_%s_top_dia_vir' % (pathlogs,ip),'r').read().split(':::')[1]
      
    try:
      virusdia=open('%skas_%s_top_dia_vir' % (pathlogs,ip),'r').read().split(':::')[1]
    except:
      geradiavir()
    
    ano=int(virusdia.split()[0].split('-')[0])
    mes=int(virusdia.split()[0].split('-')[1])
    dia=int(virusdia.split()[0].split('-')[2])
    virusdia=time.mktime(datetime.datetime(ano,mes,dia,0,0,0,0 ).timetuple())
    if int((time.mktime(datetime.datetime.now().timetuple()))) > int(virusdia):
      geradiavir()
      virus=lerviruslog('virus')
      incrementafile('%skas_name_%s_top_dia_vir' % (pathlogs,ip),1)#1 para zerar o incremento
      virus=lerviruslog('maquina')
      incrementafile('%skas_name_%s_top_dia_maq' % (pathlogs,ip),1)#1 para zerar o incremento

    def geradiasusp():
      ano=int(datetime.date.today().strftime("%y"))
      dia=int(datetime.date.today().strftime("%d"))
      mes=int(datetime.date.today().strftime("%m"))
      #int("%d" % (time.mktime(datetime.datetime(ano, mes, dia+1, 0, 0, 0, 0).timetuple())))
      data=datetime.datetime(ano+2000, mes, dia, 0, 0, 0, 0)+dateutil.relativedelta.relativedelta(days=+1)
      open('%skas_%s_top_dia_susp' % (pathlogs,ip),'w').write('0:::%s' % str(data))
      suspdia=open('%skas_%s_top_dia_susp' % (pathlogs,ip),'r').read().split(':::')[1]

    try:
      suspdia=open('%skas_%s_top_dia_susp' % (pathlogs,ip),'r').read().split(':::')[1]
    except:
      geradiasusp()
    ano=int(suspdia.split()[0].split('-')[0])
    mes=int(suspdia.split()[0].split('-')[1])
    dia=int(suspdia.split()[0].split('-')[2])
    suspdia=time.mktime(datetime.datetime(ano,mes,dia,0,0,0,0 ).timetuple())
    if int("%d" % (time.mktime(datetime.datetime.now().timetuple()))) > int(suspdia):
      geradiasusp()
  lancadia()
  #rotina alimentacao/renovacao semanal
  def lencasemana():
    def gera7diasvir():
      ano=int(datetime.date.today().strftime("%y"))
      dia=int(datetime.date.today().strftime("%d"))
      mes=int(datetime.date.today().strftime("%m"))
      #int("%d" % (time.mktime(datetime.datetime(ano, mes, dia+1, 0, 0, 0, 0).timetuple())))
      data=datetime.datetime(ano+2000, mes, dia, 0, 0, 0, 0)+dateutil.relativedelta.relativedelta(weekday=calendar.SUNDAY)#soma sempre ate proximo domingo
      open('%skas_%s_top_7dias_vir' % (pathlogs,ip),'w').write('0:::%s' % str(data))    
      virusdia=open('%skas_%s_top_7dias_vir' % (pathlogs,ip),'r').read().split(':::')[1]

    try:
      virusdia=open('%skas_%s_top_7dias_vir' % (pathlogs,ip),'r').read().split(':::')[1]
    except:
      gera7diasvir()
    ano=int(virusdia.split()[0].split('-')[0])
    mes=int(virusdia.split()[0].split('-')[1])
    dia=int(virusdia.split()[0].split('-')[2])
    virusdia=time.mktime(datetime.datetime(ano,mes,dia,0,0,0,0 ).timetuple())
    if int("%d" % (time.mktime(datetime.datetime.now().timetuple()))) > int(virusdia):
      gera7diasvir()
      virus=lerviruslog('virus')
      incrementafile('%skas_name_%s_top_7dias_vir' % (pathlogs,ip),1)#1 para zerar o incremento
      virus=lerviruslog('maquina')
      incrementafile('%skas_name_%s_top_7dias_maq' % (pathlogs,ip),1)#1 para zerar o incremento

    def gera7diassusp():
      ano=int(datetime.date.today().strftime("%y"))
      dia=int(datetime.date.today().strftime("%d"))
      mes=int(datetime.date.today().strftime("%m"))
      #int("%d" % (time.mktime(datetime.datetime(ano, mes, dia+1, 0, 0, 0, 0).timetuple())))
      data=datetime.datetime(ano+2000, mes, dia, 0, 0, 0, 0)+dateutil.relativedelta.relativedelta(weekday=calendar.SUNDAY)#soma sempre ate proximo domingo
      open('%skas_%s_top_7dias_susp' % (pathlogs,ip),'w').write('0:::%s' % str(data))
      virusdia=open('%skas_%s_top_7dias_susp' % (pathlogs,ip),'r').read().split(':::')[1]

    try:
      virusdia=open('%skas_%s_top_7dias_susp' % (pathlogs,ip),'r').read().split(':::')[1]
    except:
      gera7diassusp()
    ano=int(virusdia.split()[0].split('-')[0])
    mes=int(virusdia.split()[0].split('-')[1])
    dia=int(virusdia.split()[0].split('-')[2])
    virusdia=time.mktime(datetime.datetime(ano,mes,dia,0,0,0,0 ).timetuple())
    if int("%d" % (time.mktime(datetime.datetime.now().timetuple()))) > int(virusdia):
      gera7diassusp()
  lencasemana()
  #rotina alimentacao/renovacao mensal
  def lancames():
    def geramesvir():
      ano=int(datetime.date.today().strftime("%y"))
      #dia=int(datetime.date.today().strftime("%d"))
      mes=int(datetime.date.today().strftime("%m"))
      data=datetime.datetime(ano+2000, mes, 1, 0, 0, 0, 0)+dateutil.relativedelta.relativedelta(months=+1)#soma sempre ate proximo mes
      #int("%d" % (time.mktime(datetime.datetime(ano, mes, dia+1, 0, 0, 0, 0).timetuple())))      
      open('%skas_%s_top_mes_vir' % (pathlogs,ip),'w').write('0:::%s' % str(data)) 
      virusdia=open('%skas_%s_top_mes_vir' % (pathlogs,ip),'r').read().split(':::')[1]

    try:
      virusdia=open('%skas_%s_top_mes_vir' % (pathlogs,ip),'r').read().split(':::')[1]
    except:
      geramesvir()
    ano=int(virusdia.split()[0].split('-')[0])
    mes=int(virusdia.split()[0].split('-')[1])
    dia=int(virusdia.split()[0].split('-')[2])
    virusdia=time.mktime(datetime.datetime(ano,mes,dia,0,0,0,0 ).timetuple())
    if int("%d" % (time.mktime(datetime.datetime.now().timetuple()))) > int(virusdia):
      geramesvir()
      virus=lerviruslog('virus')
      incrementafile('%skas_name_%s_top_mes_vir' % (pathlogs,ip),1)#1 para zerar o incremento
      virus=lerviruslog('maquina')
      incrementafile('%skas_name_%s_top_mes_maq' % (pathlogs,ip),1)#1 para zerar o incremento

      
    def geramessusp():#
      ano=int(datetime.date.today().strftime("%y"))
      dia=int(datetime.date.today().strftime("%d"))
      mes=int(datetime.date.today().strftime("%m"))
      data=datetime.datetime(ano+2000, mes, 1, 0, 0, 0, 0)+dateutil.relativedelta.relativedelta(months=+1)#soma sempre ate proximo mes
      open('%skas_%s_top_mes_susp' % (pathlogs,ip),'w').write('0:::%s' % str(data))
      virusdia=open('%skas_%s_top_mes_susp' % (pathlogs,ip),'r').read().split(':::')[1]

    try:
      virusdia=open('%skas_%s_top_mes_susp' % (pathlogs,ip),'r').read().split(':::')[1]
    except:
      geramessusp()
    ano=int(virusdia.split()[0].split('-')[0])
    mes=int(virusdia.split()[0].split('-')[1])
    dia=int(virusdia.split()[0].split('-')[2])
    virusdia=time.mktime(datetime.datetime(ano,mes,dia,0,0,0,0 ).timetuple())
    if int("%d" % (time.mktime(datetime.datetime.now().timetuple()))) > int(virusdia):
      geramessusp()
  lancames()
    #rotina alimentacao/renovacao anual
  def lancaano():
    def geraanovir():
      ano=int(datetime.date.today().strftime("%y"))
      data=datetime.datetime(ano+2000, 1, 1, 0, 0, 0, 0)+dateutil.relativedelta.relativedelta(years=+1)#soma sempre ate proximo ano
      open('%skas_%s_top_ano_vir' % (pathlogs,ip),'w').write('0:::%s' % str(data))    
      virusdia=open('%skas_%s_top_ano_vir' % (pathlogs,ip),'r').read().split(':::')[1]
	    
    try:
      virusdia=open('%skas_%s_top_ano_vir' % (pathlogs,ip),'r').read().split(':::')[1]
    except:
      geraanovir()
    ano=int(virusdia.split()[0].split('-')[0])
    mes=int(virusdia.split()[0].split('-')[1])
    dia=int(virusdia.split()[0].split('-')[2])
    virusdia=time.mktime(datetime.datetime(ano,mes,dia,0,0,0,0 ).timetuple())
    if int("%d" % (time.mktime(datetime.datetime.now().timetuple()))) > int(virusdia):
      geraanovir()
      virus=lerviruslog('virus')
      incrementafile('%skas_name_%s_top_ano_vir' % (pathlogs,ip),1)#1 para zerar o incremento
      virus=lerviruslog('maquina')
      incrementafile('%skas_name_%s_top_ano_maq' % (pathlogs,ip),1)#1 para zerar o incremento

    def geraanosusp():#
      ano=int(datetime.date.today().strftime("%y"))
      data=datetime.datetime(ano+2000, 1, 1, 0, 0, 0, 0)+dateutil.relativedelta.relativedelta(years=+1)#soma sempre ate proximo ano
      open('%skas_%s_top_ano_susp' % (pathlogs,ip),'w').write('0:::%s' % str(data))   
      virusdia=open('%skas_%s_top_ano_susp' % (pathlogs,ip),'r').read().split(':::')[1]

    try:
      virusdia=open('%skas_%s_top_ano_susp' % (pathlogs,ip),'r').read().split(':::')[1]
    except:
      geraanosusp()
    ano=int(virusdia.split()[0].split('-')[0])
    mes=int(virusdia.split()[0].split('-')[1])
    dia=int(virusdia.split()[0].split('-')[2])
    virusdia=time.mktime(datetime.datetime(ano,mes,dia,0,0,0,0 ).timetuple())
    if int("%d" % (time.mktime(datetime.datetime.now().timetuple()))) > int(virusdia):
      geraanosusp()
      
  lancaano()
  
  
  #graphparser('%skas_%s_graph_dia' % (pathlogs,ip))#executado de 1 em 1 min
  
  #rotina para alimentacao dos arquivos que sao a base de xml
  virus=lerviruslog('virus')
  incrementafile('%skas_name_%s_top_dia_vir' % (pathlogs,ip),0)#1 para zerar o incremento
  virus=lerviruslog('virus')
  incrementafile('%skas_name_%s_top_7dias_vir' % (pathlogs,ip),0)#1 para zerar o incremento
  virus=lerviruslog('virus')
  incrementafile('%skas_name_%s_top_mes_vir' % (pathlogs,ip),0)#1 para zerar o incremento
  virus=lerviruslog('virus')
  incrementafile('%skas_name_%s_top_ano_vir' % (pathlogs,ip),0)#1 para zerar o incremento

  virus=lerviruslog('maquina')
  incrementafile('%skas_name_%s_top_dia_maq' % (pathlogs,ip),0)#1 para zerar o incremento
  virus=lerviruslog('maquina')
  incrementafile('%skas_name_%s_top_7dias_maq' % (pathlogs,ip),0)#1 para zerar o incremento
  virus=lerviruslog('maquina')
  incrementafile('%skas_name_%s_top_mes_maq' % (pathlogs,ip),0)#1 para zerar o incremento
  virus=lerviruslog('maquina')
  incrementafile('%skas_name_%s_top_ano_maq' % (pathlogs,ip),0)#1 para zerar o incremento

  
  virus5min=open('/media/kas/virus_counter_infect','r').read()
  susp5min=open('/media/kas/virus_counter_suspicious','r').read()

  if int(virus5min) > 0 or int(susp5min) > 0:

    #rotina dia
    data=open('%skas_%s_top_dia_vir' % (pathlogs,ip)).read().split(':::')
    virus=data[0]
    rvirus=data[1]
    data=open('%skas_%s_top_dia_susp' % (pathlogs,ip)).read().split(':::')
    susp=data[0]
    rsusp=data[1]
    virusdia=int(virus)+int(virus5min)
    suspdia=int(susp)+int(susp5min)
    open('%skas_%s_top_dia_vir' % (pathlogs,ip),'w').write('%s:::%s'  % (virusdia,rvirus))
    open('%skas_%s_top_dia_susp' % (pathlogs,ip),'w').write('%s:::%s' % (suspdia,rsusp))
    
    #rotina 7dias
    data=open('%skas_%s_top_7dias_vir' % (pathlogs,ip)).read().split(':::')
    virus=data[0]
    rvirus=data[1]
    data=open('%skas_%s_top_7dias_susp' % (pathlogs,ip)).read().split(':::')
    susp=data[0]
    rsusp=data[1]
    virusdia=int(virus)+int(virus5min)
    suspdia=int(susp)+int(susp5min)
    open('%skas_%s_top_7dias_vir' % (pathlogs,ip),'w').write('%s:::%s'  % (virusdia,rvirus))
    open('%skas_%s_top_7dias_susp' % (pathlogs,ip),'w').write('%s:::%s' % (suspdia,rsusp))
    
    #rotina mes
    data=open('%skas_%s_top_mes_vir' % (pathlogs,ip)).read().split(':::')
    virus=data[0]
    rvirus=data[1]
    data=open('%skas_%s_top_mes_susp' % (pathlogs,ip)).read().split(':::')
    susp=data[0]
    rsusp=data[1]
    virusdia=int(virus)+int(virus5min)
    suspdia=int(susp)+int(susp5min)
    open('%skas_%s_top_mes_vir' % (pathlogs,ip),'w').write('%s:::%s'  % (virusdia,rvirus))
    open('%skas_%s_top_mes_susp' % (pathlogs,ip),'w').write('%s:::%s' % (suspdia,rsusp))
  
    #rotina ano
    data=open('%skas_%s_top_ano_vir' % (pathlogs,ip)).read().split(':::')
    virus=data[0]
    rvirus=data[1]
    data=open('%skas_%s_top_ano_susp' % (pathlogs,ip)).read().split(':::')
    susp=data[0]
    rsusp=data[1]
    virusdia=int(virus)+int(virus5min)
    suspdia=int(susp)+int(susp5min)
    open('%skas_%s_top_ano_vir' % (pathlogs,ip),'w').write('%s:::%s'  % (virusdia,rvirus))
    open('%skas_%s_top_ano_susp' % (pathlogs,ip),'w').write('%s:::%s' % (suspdia,rsusp))
    
    graphparser('QUANTITATIVODIA')#executado de 5 em 5 min

    
    
  open('/media/kas/virus_counter_infect','w').write('0')
  open('/media/kas/virus_counter_suspicious','w').write('0')

  print 'Kaspersky-Total V&iacute;rus 5min virus=%s suspicious=%s|virus5min=%s susp5min=%s' % \
        (str(virus5min),str(susp5min),\
         str(virus5min),str(susp5min))

elif tipo == '2':#dia
  data=open('%skas_%s_top_dia_vir' % (pathlogs,ip)).read().split(':::')
  virusdia=data[0]
  rvirus=data[1]
  data=open('%skas_%s_top_dia_susp' % (pathlogs,ip)).read().split(':::')
  suspdia=data[0]
  rsusp=data[1]
  print 'Kaspersky-Total V&iacute;rus Dia virus=%s suspicious=%s|virus5min=%s susp5min=%s' % \
        (str(virusdia),str(suspdia),\
         str(virusdia),str(suspdia))
  print 'Reset virus stats em:%s'%rvirus
  print 'Reset suspe stats em:%s'%rsusp
  
elif tipo == '3':#7dias
  data=open('%skas_%s_top_7dias_vir' % (pathlogs,ip)).read().split(':::')
  virusdia=data[0]
  rvirus=data[1]
  data=open('%skas_%s_top_7dias_susp' % (pathlogs,ip)).read().split(':::')
  suspdia=data[0]
  rsusp=data[1]

  print 'Kaspersky-Total V&iacute;rus Semana virus=%s suspicious=%s|virus7dias=%s susp7dias=%s' % \
        (str(virusdia),str(suspdia),\
         str(virusdia),str(suspdia))
  print 'Reset virus stats em:%s'%rvirus
  print 'Reset suspe stats em:%s'%rsusp

elif tipo == '4':#mes
  data=open('%skas_%s_top_mes_vir' % (pathlogs,ip)).read().split(':::')
  virusdia=data[0]
  rvirus=data[1]
  data=open('%skas_%s_top_mes_susp' % (pathlogs,ip)).read().split(':::')
  suspdia=data[0]
  rsusp=data[1]

  print 'Kaspersky-Total V&iacute;rus M&ecirc;s virus=%s suspicious=%s|virusmes=%s suspmes=%s' % \
        (str(virusdia),str(suspdia),\
         str(virusdia),str(suspdia))
  print 'Reset virus stats em:%s'%rvirus
  print 'Reset suspe stats em:%s'%rsusp

elif tipo == '5':#ano
  data=open('%skas_%s_top_ano_vir' % (pathlogs,ip)).read().split(':::')
  virusdia=data[0]
  rvirus=data[1]
  data=open('%skas_%s_top_ano_susp' % (pathlogs,ip)).read().split(':::')
  suspdia=data[0]
  rsusp=data[1]

  print 'Kaspersky-Total V&iacute;rus Ano virus=%s suspicious=%s|virusano=%s suspano=%s' % \
        (str(virusdia),str(suspdia),\
         str(virusdia),str(suspdia))
  print 'Reset virus stats em:%s'%rvirus
  print 'Reset suspe stats em:%s'%rsusp

#elif tipo == '6':#ano
  #ultimas infeccoes


elif tipo == '6':#top 20 atividades
  root = etree.fromstring(open('/media/kas/report_kas_dia.xml','r').read())
  #root = etree.fromstring(open('report_kas.xml','r').read())
  qtelements=len(list(root.iter()))
  #13 qtcolunas 15qt incidente
  #limite=qtelements-(13*20)
  limite=(113)
  i=0
  salto=0
  virus=[]

  for element in root.iter():
    if i > limite:
      salto+=1
      #if salto==1:
	#print 'UM VIRUS'
      if salto==2:
	nome_machine=element.text
      if salto==4:
	nome_virus=element.text
      if salto==6:
	data_infect=element.text
	data_infect=data_infect.split(' ')[1:]
	dia=data_infect[0]
	mes=data_infect[2]
	mes=convertmes(mes)
	ano=data_infect[4]
	hora=data_infect[5]
	data_infect='%s/%s/%s %s' % (dia,mes,ano,hora)

      if salto==8:
	file_infect=element.text
      if salto==12:
	ip=element.text
      if salto==13:
	#print "%s %s %s %s %s" % (nome_machine,nome_virus,data_infect,file_infect.replace(' ',''),ip)
	virus.append("%s %s %s %s %s" % (nome_machine,nome_virus,data_infect,file_infect.replace(' ',''),ip))
	#virus.append()
	salto=0
      #print("%s - %s" % (element.tag, element.text))  
    #if i==60:
      #break
    i+=1

  print 'Kaspersky-Ultimas 20 Atividades'
  x=0
  for i in virus:
    print i
    x+=1
    if x==20:break
  #print '\n'.join(virus)
  #print 'Manutencao sera corrigido'
  
elif tipo == '7':#top virus dia
  logfile='%skas_name_%s_top_dia_vir' % (pathlogs,ip)
  dict1=pickle.load(open(logfile))
  lastatu_old = open(logfile,'r').readlines()[-1]
  one=[]
  for i in dict1:one.append('%s=%s' % (i,dict1[i]))
  
  #print 'Kaspersky Top V&iacute;rus Dia|%s' % (' '.join(one))
  print 'Kaspersky Top Vírus Dia' 
  print 'Top20 &Uacute;ltimo incidente %s' % lastatu_old
  for i in sorted(dict1.items(), cmp=lambda x,y: int(y[1]) - int(x[1])):
    print ('V&iacute;rus - <a href="http://www.google.com.br/search?hl=pt-BR&q=%s">%s</a> %s'% (i[0],i[0],i[1]))

elif tipo == '8':#top virus mes
  logfile='%skas_name_%s_top_mes_vir' % (pathlogs,ip)
  dict1=pickle.load(open(logfile))
  lastatu_old = open(logfile,'r').readlines()[-1]
  one=[]
  for i in dict1:one.append('%s=%s' % (i,dict1[i]))
  
  print 'Kaspersky Top Vírus Mês'
  #print 'Kaspersky Top V&iacute;rus M&ecirc;s|%s' % (' '.join(one))
  print 'Top20 &Uacute;ltimo incidente %s' % lastatu_old
  for i in sorted(dict1.items(), cmp=lambda x,y: int(y[1]) - int(x[1])):
    print ('V&iacute;rus - <a href="http://www.google.com.br/search?hl=pt-BR&q=%s">%s</a> %s'% (i[0],i[0],i[1]))
    
elif tipo == '9':#top virus ano

  logfile='%skas_name_%s_top_ano_vir' % (pathlogs,ip)
  dict1=pickle.load(open(logfile))
  lastatu_old = open(logfile,'r').readlines()[-1]
  one=[]
  for i in dict1:one.append('%s=%s' % (i,dict1[i]))
  
  #print 'Kaspersky Top V&iacute;rus Ano|%s' % (' '.join(one))
  print 'Kaspersky Top V&iacute;rus Ano' 
  print 'Top20 &Uacute;ltimo incidente %s' % lastatu_old
  for i in sorted(dict1.items(), cmp=lambda x,y: int(y[1]) - int(x[1])):
    print ('V&iacute;rus - <a href="http://www.google.com.br/search?hl=pt-BR&q=%s">%s</a> %s'% (i[0],i[0],i[1]))

elif tipo == '10':#top virus semana

  logfile='%skas_name_%s_top_7dias_vir' % (pathlogs,ip)
  dict1=pickle.load(open(logfile))
  lastatu_old = open(logfile,'r').readlines()[-1]
  one=[]
  for i in dict1:one.append('%s=%s' % (i,dict1[i]))
  
  print 'Kaspersky Top V&iacute;rus Semana' 
  #print 'Kaspersky Top V&iacute;rus Semana|%s' % (' '.join(one))
  print 'Top20 &Uacute;ltimo incidente %s' % lastatu_old
  for i in sorted(dict1.items(), cmp=lambda x,y: int(y[1]) - int(x[1])):
    print ('V&iacute;rus - <a href="http://www.google.com.br/search?hl=pt-BR&q=%s">%s</a> %s'% (i[0],i[0],i[1]))
    
elif tipo == '11':#top maquina dia

  #virus=lerviruslog('virus')
  #incrementafile('%skas_name_%s_top_dia_vir' % (pathlogs,ip),1)#1 para zerar o incremento
  #virus=lerviruslog('maquina')
  #incrementafile('%skas_name_%s_top_dia_maq' % (pathlogs,ip),1)#1 para zerar o incremento

  
  logfile='%skas_name_%s_top_dia_maq' % (pathlogs,ip)
  dict1=pickle.load(open(logfile))
  lastatu_old = open(logfile,'r').readlines()[-1]
  one=[]
  for i in dict1:one.append('%s=%s' % (i,dict1[i]))
  
  #print 'Kaspersky Top M&aacute;quina Dia|%s' % (' '.join(one))
  print 'Kaspersky Top M&aacute;quina Dia'
  print 'Top20 &Uacute;ltimo incidente %s' % lastatu_old
  for i in sorted(dict1.items(), cmp=lambda x,y: int(y[1]) - int(x[1])):
    print ('M&aacute;quina - %s %s'% (i[0],i[1]))

elif tipo == '12':#top maquina semana

  logfile='%skas_name_%s_top_7dias_maq' % (pathlogs,ip)
  dict1=pickle.load(open(logfile))
  lastatu_old = open(logfile,'r').readlines()[-1]
  one=[]
  for i in dict1:one.append('%s=%s' % (i,dict1[i]))
  
  #print 'Kaspersky Top M&aacute;quina Semana|%s' % (' '.join(one))
  print 'Kaspersky Top M&aacute;quina Semana' 
  print 'Top20 &Uacute;ltimo incidente %s' % lastatu_old
  for i in sorted(dict1.items(), cmp=lambda x,y: int(y[1]) - int(x[1])):
    print ('M&aacute;quina - %s %s'% (i[0],i[1]))
    
elif tipo == '13':#top maquina mes
  logfile='%skas_name_%s_top_mes_maq' % (pathlogs,ip)
  dict1=pickle.load(open(logfile))
  lastatu_old = open(logfile,'r').readlines()[-1]
  one=[]
  for i in dict1:one.append('%s=%s' % (i,dict1[i]))
  
  #print 'Kaspersky Top M&aacute;quina M&ecirc;s|%s' % (' '.join(one))
  print 'Kaspersky Top M&aacute;quina M&ecirc;s'
  print 'Top20 &Uacute;ltimo incidente %s' % lastatu_old
  for i in sorted(dict1.items(), cmp=lambda x,y: int(y[1]) - int(x[1])):
    print ('M&aacute;quina - %s %s'% (i[0],i[1]))


  
elif tipo == '14':#top maquina Ano

  logfile='%skas_name_%s_top_ano_maq' % (pathlogs,ip)
  dict1=pickle.load(open(logfile))
  lastatu_old = open(logfile,'r').readlines()[-1]
  one=[]
  for i in dict1:one.append('%s=%s' % (i,dict1[i]))
  
  #print 'Kaspersky Top M&aacute;quina Ano|%s' % (' '.join(one))
  print 'Kaspersky Top M&aacute;quina Ano'
  print 'Top20 &Uacute;ltimo incidente %s' % lastatu_old
  for i in sorted(dict1.items(), cmp=lambda x,y: int(y[1]) - int(x[1])):
    print ('M&aacute;quina - %s %s'% (i[0],i[1]))

elif tipo == '15':#Kaspersky Total V&iacute;rus Gr&aacute;ficos

  print 'Kaspersky Total Virus Graficos'
  
  if os.path.isfile('%skas_%s_graph_7dias.xml' % (pathlogs,ip)):#se o arquivo existe
    print '<embed src="http://50.56.99.4/cmp/data/MSColumn3D.swf" flashVars="&dataURL=http://50.56.99.4/cmp/data/%s" quality="high" width="600" height="470" name="Column3D" type="application/x-shockwave-flash"/>' % ('kas_%s_graph_7dias.xml' % (ip))
    #print '<iframe width=\"600\" height=\"470\" src=\"http://50.56.99.4/cmp/data/%s\" scrolling=\"no\" ></iframe><br>' % ('kas_%s_graph_7dias.png' % (ip))
  if os.path.isfile('%skas_%s_graph_mes.xml' % (pathlogs,ip)):#se o arquivo existe 
    print '<embed src="http://50.56.99.4/cmp/data/MSColumn3D.swf" flashVars="&dataURL=http://50.56.99.4/cmp/data/%s" quality="high" width="600" height="470" name="Column3D" type="application/x-shockwave-flash"/>' % ('kas_%s_graph_mes.xml' % (ip))
    #print '<iframe  width=\"600\" height=\"470\" src=\"http://50.56.99.4/cmp/data/%s\" scrolling=\"no\" ></iframe><br>' % ('kas_%s_graph_mes.png' % (ip))
  if os.path.isfile('%skas_%s_graph_ano.xml' % (pathlogs,ip)):#se o arquivo existe 
    print '<embed src="http://50.56.99.4/cmp/data/MSColumn3D.swf" flashVars="&dataURL=http://50.56.99.4/cmp/data/%s" quality="high" width="600" height="470" name="Column3D" type="application/x-shockwave-flash"/>' % ('kas_%s_graph_ano.xml' % (ip))
    #print '<iframe  width=\"600\" height=\"470\" src=\"http://50.56.99.4/cmp/data/%s\" scrolling=\"no\" ></iframe><br>' % ('kas_%s_graph_ano.png' % (ip))

    
elif tipo == '16':#Gera Gr&aacute;ficos Manualmente

  graphparser('%skas_%s_graph_7dias' % (pathlogs,ip))
  print ('%skas_%s_graph_7dias.xml' % (pathlogs,ip))
  graphparser('%skas_%s_graph_mes' % (pathlogs,ip))
  print ('%skas_%s_graph_mes.xml' % (pathlogs,ip))
  graphparser('%skas_%s_graph_ano' % (pathlogs,ip))
  print ('%skas_%s_graph_ano.xml' % (pathlogs,ip))

  ###graphparserpizza('%skas_name_%s_top_7dias_maq' % (pathlogs,ip))
  ###print ('%skas_name_%s_top_7dias_maq' % (pathlogs,ip))
  ###graphparserpizza('%skas_name_%s_top_ano_maq' % (pathlogs,ip))
  ###print ('%skas_name_%s_top_ano_maq' % (pathlogs,ip))
  ###graphparserpizza('%skas_name_%s_top_mes_maq' % (pathlogs,ip))
  ###print ('%skas_name_%s_top_mes_maq' % (pathlogs,ip))
  
  ###graphparserpizza('%skas_name_%s_top_mes_vir' % (pathlogs,ip))
  ###print ('%skas_name_%s_top_mes_vir' % (pathlogs,ip))
  ###graphparserpizza('%skas_name_%s_top_7dias_vir' % (pathlogs,ip))
  ###print ('%skas_name_%s_top_7dias_vir'  % (pathlogs,ip))
  ###graphparserpizza('%skas_name_%s_top_ano_vir' % (pathlogs,ip))
  ###print ('%skas_name_%s_top_ano_vir' % (pathlogs,ip))
  
  
elif tipo =='17':#5min

  #rotina alimentacao/renovacao diaria
  def lancadia():
    def geradiavir(): 
      tvirusdia='12'#pega total virus do dia
      tsuspdia='9'#pega total suspeitos do dia
      #tvirusdia=open('%skas_%s_top_dia_vir' % (pathlogs,ip),'r').read().split(':::')[0]#pega total virus do dia
      #tsuspdia=open('%skas_%s_top_dia_susp' % (pathlogs,ip),'r').read().split(':::')[0]#pega total suspeitos do dia
      #rotina 7dias
      ###strdia=convertdia((datetime.datetime.now()+dateutil.relativedelta.relativedelta(days=-1)).strftime("%A"))
      ###if os.path.isfile('%skas_%s_graph_7dias' % (pathlogs,ip)):#se o arquivo existe
	###data=open('%skas_%s_graph_7dias' % (pathlogs,ip),'r').read().rstrip()#ler e adiciona mais um dia
	###if data.count(';')==7:
	  ###print 'geradiavir contem 7;','%s,%s,%s;' % (tvirusdia,tsuspdia,strdia)
	  ###open('%skas_%s_graph_7dias' % (pathlogs,ip),'w').write('%s,%s,%s;' % (tvirusdia,tsuspdia,strdia))
	###else:
	  ###print 'geradiavir contem nao contem 7;','%s%s,%s,%s;' % (data,tvirusdia,tsuspdia,strdia)
	  ###open('%skas_%s_graph_7dias' % (pathlogs,ip),'w').write(data+'%s,%s,%s;' % (tvirusdia,tsuspdia,strdia))
      ###else:
	###print 'arquivo novo','%s,%s,%s;' % (tvirusdia,tsuspdia,strdia)
	###open('%skas_%s_graph_7dias' % (pathlogs,ip),'w').write('%s,%s,%s;' % (tvirusdia,tsuspdia,strdia))
	
      ####rotina M&ecirc;s 30dias
      ###strdia=str((datetime.datetime.now()+dateutil.relativedelta.relativedelta(days=+1)).strftime("%d"))#pega dia da semana
      ###if os.path.isfile('%skas_%s_graph_mes' % (pathlogs,ip)):#se o arquivo existe
	###data=open('%skas_%s_graph_mes' % (pathlogs,ip),'r').read().rstrip()#ler e adiciona mais um dia
	###if strdia=='01':#se dia 01 cria novo mes
	  ###print 'geradiavir dia he 01','%s,%s,%s;' % (tvirusdia,tsuspdia,strdia)
	  ###open('%skas_%s_graph_mes' % (pathlogs,ip),'w').write('%s,%s,%s;' % (tvirusdia,tsuspdia,strdia))
	###else:
	  ###print 'geradiavir contem nao he dia 01','%s,%s,%s;' % (tvirusdia,tsuspdia,strdia)
	  ###open('%skas_%s_graph_mes' % (pathlogs,ip),'w').write(data+'%s,%s,%s;' % (tvirusdia,tsuspdia,strdia))
      ###else:
	###print 'Arquivo novo','%s,%s,%s;' % (tvirusdia,tsuspdia,strdia)
	###open('%skas_%s_graph_mes' % (pathlogs,ip),'w').write('%s,%s,%s;' % (tvirusdia,tsuspdia,strdia))
      
      #rotina ano 365dias
      strmes=str((datetime.datetime.now()+dateutil.relativedelta.relativedelta(days=-1)).strftime("%B"))#pega mes
      if os.path.isfile('%skas_%s_graph_ano' % (pathlogs,ip)):#se o arquivo existe
	data=open('%skas_%s_graph_ano' % (pathlogs,ip),'r').read().rstrip()#ler e adiciona mais um dia
	vet1=data.split(';')[:-1]
	vet2=vet1[-1].split(',')
	icrvir=int(vet2[0])+int(tvirusdia)
	incrsusp=int(vet2[1])+int(tsuspdia)
	
	if data.count(';') ==12:#se dia 01 cria novo mes
	  print 'deu 12;','%s,%s,%s;' % (tvirusdia,tsuspdia,strmes)
	  open('%skas_%s_graph_ano' % (pathlogs,ip),'w').write('%s,%s,%s;' % (tvirusdia,tsuspdia,strmes))
	elif data.count(';') ==1:#se dia 01 cria novo mes
	  print '1mes no arquivo'
	  if vet1[-1].split(',')[2] == strmes:
	    print 'M&ecirc;s igual ','%s,%s,%s;' % (icrvir,incrsusp,strmes)
	    open('%skas_%s_graph_ano' % (pathlogs,ip),'w').write('%s,%s,%s;' % (icrvir,incrsusp,strmes))	    
	  else:
	    print 'M&ecirc;s Mudou'
	    open('%skas_%s_graph_ano' % (pathlogs,ip),'w').write(';'.join(vet1)+';%s,%s,%s;' % (tvirusdia,tsuspdia,strmes))	    	      
	else:
	  if len(vet1[:-1]) ==0:
	    print ' a nao deu 12;','%s,%s,%s;' % (tvirusdia,tsuspdia,strmes),'len ',len(vet1)
	    open('%skas_%s_graph_ano' % (pathlogs,ip),'w').write(';'.join(vet1)+';%s,%s,%s;' % (icrvir,incrsusp,strmes))
	  else:
	    print 'a nao deu 12;','%s,%s,%s;' % (tvirusdia,tsuspdia,strmes),'len ',len(vet1[:-1])
	    print vet1
	    if vet1[-1].split(',')[2] == strmes:
	      print 'M&ecirc;s igual ',';'.join(vet1[:-1])+';%s,%s,%s;' % (icrvir,incrsusp,strmes)
	      open('%skas_%s_graph_ano' % (pathlogs,ip),'w').write(';'.join(vet1[:-1])+';%s,%s,%s;' % (icrvir,incrsusp,strmes))	    
	    else:
	      print 'M&ecirc;s Mudou'
	      open('%skas_%s_graph_ano' % (pathlogs,ip),'w').write(';'.join(vet1)+';%s,%s,%s;' % (tvirusdia,tsuspdia,strmes))	    	      
      else:
	print 'arquivo novo','%s,%s,%s;' % (tvirusdia,tsuspdia,strmes)
	open('%skas_%s_graph_ano' % (pathlogs,ip),'w').write('%s,%s,%s;' % (tvirusdia,tsuspdia,strmes))

      ###graphparser('%skas_%s_graph_7dias' % (pathlogs,ip))
      ###graphparser('%skas_%s_graph_mes' % (pathlogs,ip))
      ###graphparser('%skas_%s_graph_ano' % (pathlogs,ip))
	
      ano=int(datetime.date.today().strftime("%y"))
      dia=int(datetime.date.today().strftime("%d"))
      mes=int(datetime.date.today().strftime("%m"))
      #int("%d" % (time.mktime(datetime.datetime(ano, mes, dia+1, 0, 0, 0, 0).timetuple())))
      data=datetime.datetime(ano+2000, mes, dia, 0, 0, 0, 0)+dateutil.relativedelta.relativedelta(days=+1)
      open('%skas_%s_top_dia_vir' % (pathlogs,ip),'w').write('0:::%s' % str(data))
      virusdia=open('%skas_%s_top_dia_vir' % (pathlogs,ip),'r').read().split(':::')[1]
      
    try:
      virusdia=open('%skas_%s_top_dia_vir' % (pathlogs,ip),'r').read().split(':::')[1]
    except:
      geradiavir()
    
    ano=int(virusdia.split()[0].split('-')[0])
    mes=int(virusdia.split()[0].split('-')[1])
    dia=int(virusdia.split()[0].split('-')[2])
    virusdia=time.mktime(datetime.datetime(ano,mes,dia,0,0,0,0 ).timetuple())
    #if int((time.mktime(datetime.datetime.now().timetuple()))) > int(virusdia):
    geradiavir()
    
    def geradiasusp():
      ano=int(datetime.date.today().strftime("%y"))
      dia=int(datetime.date.today().strftime("%d"))
      mes=int(datetime.date.today().strftime("%m"))
      #int("%d" % (time.mktime(datetime.datetime(ano, mes, dia+1, 0, 0, 0, 0).timetuple())))
      data=datetime.datetime(ano+2000, mes, dia, 0, 0, 0, 0)+dateutil.relativedelta.relativedelta(days=+1)
      open('%skas_%s_top_dia_susp' % (pathlogs,ip),'w').write('0:::%s' % str(data))
      suspdia=open('%skas_%s_top_dia_susp' % (pathlogs,ip),'r').read().split(':::')[1]

    ###try:
      ###suspdia=open('%skas_%s_top_dia_susp' % (pathlogs,ip),'r').read().split(':::')[1]
    ###except:
      ###geradiasusp()
    ###ano=int(suspdia.split()[0].split('-')[0])
    ###mes=int(suspdia.split()[0].split('-')[1])
    ###dia=int(suspdia.split()[0].split('-')[2])
    ###suspdia=time.mktime(datetime.datetime(ano,mes,dia,0,0,0,0 ).timetuple())
    ####if int("%d" % (time.mktime(datetime.datetime.now().timetuple()))) > int(suspdia):
    ###geradiasusp()
  lancadia()
  #rotina alimentacao/renovacao semanal
  def lencasemana():
    def gera7diasvir():
      ano=int(datetime.date.today().strftime("%y"))
      dia=int(datetime.date.today().strftime("%d"))
      mes=int(datetime.date.today().strftime("%m"))
      #int("%d" % (time.mktime(datetime.datetime(ano, mes, dia+1, 0, 0, 0, 0).timetuple())))
      data=datetime.datetime(ano+2000, mes, dia, 0, 0, 0, 0)+dateutil.relativedelta.relativedelta(weekday=calendar.SUNDAY)#soma sempre ate proximo domingo
      open('%skas_%s_top_7dias_vir' % (pathlogs,ip),'w').write('0:::%s' % str(data))    
      virusdia=open('%skas_%s_top_7dias_vir' % (pathlogs,ip),'r').read().split(':::')[1]

    try:
      virusdia=open('%skas_%s_top_7dias_vir' % (pathlogs,ip),'r').read().split(':::')[1]
    except:
      gera7diasvir()
    ano=int(virusdia.split()[0].split('-')[0])
    mes=int(virusdia.split()[0].split('-')[1])
    dia=int(virusdia.split()[0].split('-')[2])
    virusdia=time.mktime(datetime.datetime(ano,mes,dia,0,0,0,0 ).timetuple())
    if int("%d" % (time.mktime(datetime.datetime.now().timetuple()))) > int(virusdia):
      gera7diasvir()
      
    def gera7diassusp():
      ano=int(datetime.date.today().strftime("%y"))
      dia=int(datetime.date.today().strftime("%d"))
      mes=int(datetime.date.today().strftime("%m"))
      #int("%d" % (time.mktime(datetime.datetime(ano, mes, dia+1, 0, 0, 0, 0).timetuple())))
      data=datetime.datetime(ano+2000, mes, dia, 0, 0, 0, 0)+dateutil.relativedelta.relativedelta(weekday=calendar.SUNDAY)#soma sempre ate proximo domingo
      open('%skas_%s_top_7dias_susp' % (pathlogs,ip),'w').write('0:::%s' % str(data))
      virusdia=open('%skas_%s_top_7dias_susp' % (pathlogs,ip),'r').read().split(':::')[1]

    try:
      virusdia=open('%skas_%s_top_7dias_susp' % (pathlogs,ip),'r').read().split(':::')[1]
    except:
      gera7diassusp()
    ano=int(virusdia.split()[0].split('-')[0])
    mes=int(virusdia.split()[0].split('-')[1])
    dia=int(virusdia.split()[0].split('-')[2])
    virusdia=time.mktime(datetime.datetime(ano,mes,dia,0,0,0,0 ).timetuple())
    if int("%d" % (time.mktime(datetime.datetime.now().timetuple()))) > int(virusdia):
      gera7diassusp()
  #lencasemana()
  #rotina alimentacao/renovacao mensal
  def lancames():
    def geramesvir():
      ano=int(datetime.date.today().strftime("%y"))
      #dia=int(datetime.date.today().strftime("%d"))
      mes=int(datetime.date.today().strftime("%m"))
      data=datetime.datetime(ano+2000, mes, 1, 0, 0, 0, 0)+dateutil.relativedelta.relativedelta(months=+1)#soma sempre ate proximo mes
      #int("%d" % (time.mktime(datetime.datetime(ano, mes, dia+1, 0, 0, 0, 0).timetuple())))      
      open('%skas_%s_top_mes_vir' % (pathlogs,ip),'w').write('0:::%s' % str(data)) 
      virusdia=open('%skas_%s_top_mes_vir' % (pathlogs,ip),'r').read().split(':::')[1]

    try:
      virusdia=open('%skas_%s_top_mes_vir' % (pathlogs,ip),'r').read().split(':::')[1]
    except:
      geramesvir()
    ano=int(virusdia.split()[0].split('-')[0])
    mes=int(virusdia.split()[0].split('-')[1])
    dia=int(virusdia.split()[0].split('-')[2])
    virusdia=time.mktime(datetime.datetime(ano,mes,dia,0,0,0,0 ).timetuple())
    if int("%d" % (time.mktime(datetime.datetime.now().timetuple()))) > int(virusdia):
      geramesvir()
      
    def geramessusp():#
      ano=int(datetime.date.today().strftime("%y"))
      dia=int(datetime.date.today().strftime("%d"))
      mes=int(datetime.date.today().strftime("%m"))
      data=datetime.datetime(ano+2000, mes, 1, 0, 0, 0, 0)+dateutil.relativedelta.relativedelta(months=+1)#soma sempre ate proximo mes
      open('%skas_%s_top_mes_susp' % (pathlogs,ip),'w').write('0:::%s' % str(data))
      virusdia=open('%skas_%s_top_mes_susp' % (pathlogs,ip),'r').read().split(':::')[1]

    try:
      virusdia=open('%skas_%s_top_mes_susp' % (pathlogs,ip),'r').read().split(':::')[1]
    except:
      geramessusp()
    ano=int(virusdia.split()[0].split('-')[0])
    mes=int(virusdia.split()[0].split('-')[1])
    dia=int(virusdia.split()[0].split('-')[2])
    virusdia=time.mktime(datetime.datetime(ano,mes,dia,0,0,0,0 ).timetuple())
    if int("%d" % (time.mktime(datetime.datetime.now().timetuple()))) > int(virusdia):
      geramessusp()
  #lancames()
    #rotina alimentacao/renovacao anual
  def lancaano():
    def geraanovir():
      ano=int(datetime.date.today().strftime("%y"))
      data=datetime.datetime(ano+2000, 1, 1, 0, 0, 0, 0)+dateutil.relativedelta.relativedelta(years=+1)#soma sempre ate proximo ano
      open('%skas_%s_top_ano_vir' % (pathlogs,ip),'w').write('0:::%s' % str(data))    
      virusdia=open('%skas_%s_top_ano_vir' % (pathlogs,ip),'r').read().split(':::')[1]
	    
    try:
      virusdia=open('%skas_%s_top_ano_vir' % (pathlogs,ip),'r').read().split(':::')[1]
    except:
      geraanovir()
    ano=int(virusdia.split()[0].split('-')[0])
    mes=int(virusdia.split()[0].split('-')[1])
    dia=int(virusdia.split()[0].split('-')[2])
    virusdia=time.mktime(datetime.datetime(ano,mes,dia,0,0,0,0 ).timetuple())
    if int("%d" % (time.mktime(datetime.datetime.now().timetuple()))) > int(virusdia):
      geraanovir()
      
    def geraanosusp():#
      ano=int(datetime.date.today().strftime("%y"))
      data=datetime.datetime(ano+2000, 1, 1, 0, 0, 0, 0)+dateutil.relativedelta.relativedelta(years=+1)#soma sempre ate proximo ano
      open('%skas_%s_top_ano_susp' % (pathlogs,ip),'w').write('0:::%s' % str(data))   
      virusdia=open('%skas_%s_top_ano_susp' % (pathlogs,ip),'r').read().split(':::')[1]

    try:
      virusdia=open('%skas_%s_top_ano_susp' % (pathlogs,ip),'r').read().split(':::')[1]
    except:
      geraanosusp()
    ano=int(virusdia.split()[0].split('-')[0])
    mes=int(virusdia.split()[0].split('-')[1])
    dia=int(virusdia.split()[0].split('-')[2])
    virusdia=time.mktime(datetime.datetime(ano,mes,dia,0,0,0,0 ).timetuple())
    if int("%d" % (time.mktime(datetime.datetime.now().timetuple()))) > int(virusdia):
      geraanosusp()
      
  #lancaano()

  
  #virus5min=open('/media/kas/virus_counter_infect','r').read()
  #susp5min=open('/media/kas/virus_counter_suspicious','r').read()
  virus5min='10'
  susp5min='7'

  if int(virus5min) > 0 or int(susp5min) > 0:
    #rotina dia
    data=open('%skas_%s_top_dia_vir' % (pathlogs,ip)).read().split(':::')
    virus=data[0]
    rvirus=data[1]
    data=open('%skas_%s_top_dia_susp' % (pathlogs,ip)).read().split(':::')
    susp=data[0]
    rsusp=data[1]
    virusdia=int(virus)+int(virus5min)
    suspdia=int(susp)+int(susp5min)
    open('%skas_%s_top_dia_vir' % (pathlogs,ip),'w').write('%s:::%s'  % (virusdia,rvirus))
    open('%skas_%s_top_dia_susp' % (pathlogs,ip),'w').write('%s:::%s' % (suspdia,rsusp))
    
    #rotina 7dias
    data=open('%skas_%s_top_7dias_vir' % (pathlogs,ip)).read().split(':::')
    virus=data[0]
    rvirus=data[1]
    data=open('%skas_%s_top_7dias_susp' % (pathlogs,ip)).read().split(':::')
    susp=data[0]
    rsusp=data[1]
    virusdia=int(virus)+int(virus5min)
    suspdia=int(susp)+int(susp5min)
    open('%skas_%s_top_7dias_vir' % (pathlogs,ip),'w').write('%s:::%s'  % (virusdia,rvirus))
    open('%skas_%s_top_7dias_susp' % (pathlogs,ip),'w').write('%s:::%s' % (suspdia,rsusp))
    
    #rotina mes
    data=open('%skas_%s_top_mes_vir' % (pathlogs,ip)).read().split(':::')
    virus=data[0]
    rvirus=data[1]
    data=open('%skas_%s_top_mes_susp' % (pathlogs,ip)).read().split(':::')
    susp=data[0]
    rsusp=data[1]
    virusdia=int(virus)+int(virus5min)
    suspdia=int(susp)+int(susp5min)
    open('%skas_%s_top_mes_vir' % (pathlogs,ip),'w').write('%s:::%s'  % (virusdia,rvirus))
    open('%skas_%s_top_mes_susp' % (pathlogs,ip),'w').write('%s:::%s' % (suspdia,rsusp))
  
    #rotina ano
    data=open('%skas_%s_top_ano_vir' % (pathlogs,ip)).read().split(':::')
    virus=data[0]
    rvirus=data[1]
    data=open('%skas_%s_top_ano_susp' % (pathlogs,ip)).read().split(':::')
    susp=data[0]
    rsusp=data[1]
    virusdia=int(virus)+int(virus5min)
    suspdia=int(susp)+int(susp5min)
    open('%skas_%s_top_ano_vir' % (pathlogs,ip),'w').write('%s:::%s'  % (virusdia,rvirus))
    open('%skas_%s_top_ano_susp' % (pathlogs,ip),'w').write('%s:::%s' % (suspdia,rsusp))

  #open('/media/kas/virus_counter_infect','w').write('0')
  #open('/media/kas/virus_counter_suspicious','w').write('0')

  print 'Kaspersky-Total V&iacute;rus 5min virus=%s suspicious=%s|virus5min=%s susp5min=%s' % \
        (str(virus5min),str(susp5min),\
         str(virus5min),str(susp5min))
elif tipo == '18':#Kaspersky Top M&aacute;quina Gr&aacute;ficos

  print 'Kaspersky Top Maquinas'
    
  logfile='%skas_name_%s_top_dia_maq' % (pathlogs,ip)
  dict1=pickle.load(open(logfile))
  lastatu_old = open(logfile,'r').readlines()[-1]
  one=[]
  for i in dict1:one.append('%s=%s' % (i,dict1[i]))
  exitcounter=0
  swfdata='&title=Relatório do Dia,{font-size:20px; color: #FFFFFF; margin: 5px; background-color: #505050; padding:5px; padding-left: 20px; padding-right: 20px;}&&x_axis_steps=1&&y_ticks=5,10,5&&line=3,#87421F&&y_min=0&&y_max=20&&bg_colour=#FDF0D5&&pie=60,#505050,#000000&&colours=#1E90FF,#BC8F8F,#00FFFF,#7A67EE,#FA8072,#7FFFD4,#00FF7F,#FF7F50,#FFFF00,#FF00FF&&links=&&tool_tip=#val#'
  intvalues=[]
  strvalues=[]
  showgraph=True
  print '&Uacute;ltimo incidente %s' % lastatu_old
  for i in sorted(dict1.items(), cmp=lambda x,y: int(y[1]) - int(x[1])):
    if int(i[1]) >0:
      strvalues.append(i[0])
      intvalues.append(str(i[1]))
      showgraph=True
      if exitcounter >=9:break
      else:exitcounter=exitcounter+1
  swfdata+='\n&values=%s&' % ','.join(intvalues)
  swfdata+='\n&pie_labels=%s&' % ','.join(strvalues)
  open('%skas_name_%s_top_dia_maq.xml' % (pathlogs,ip),'w').write(swfdata)

  if showgraph is True:
    print '<embed width="600" height="470" flashvars="data=http://50.56.99.4/cmp/data/%s" allowscriptaccess="sameDomain" quality="high" bgcolor="#FFFFFF" name="chart" id="chart" src="http://50.56.99.4/cmp/img/animations/open-flash-chart.swf" type="application/x-shockwave-flash">' % ('kas_name_%s_top_dia_maq.xml' % (ip))
    for i in sorted(dict1.items(), cmp=lambda x,y: int(y[1]) - int(x[1])):
      if i[1] >0:
	print ('M&aacute;quina - %s %s'% (i[0],i[1]))
	

  #print '<embed width="350" height="220" flashvars="data=http://50.56.99.4/cmp/data/test.txt" allowscriptaccess="sameDomain" quality="high" bgcolor="#FFFFFF" name="chart" id="chart" src="http://50.56.99.4/cmp/img/animations/open-flash-chart.swf" type="application/x-shockwave-flash">'
    
    
  if os.path.isfile('%skas_name_%s_top_7dias_maq.xml' % (pathlogs,ip)):#se o arquivo existe  
    print '<embed width="600" height="470" flashvars="data=http://50.56.99.4/cmp/data/%s" allowscriptaccess="sameDomain" quality="high" bgcolor="#FFFFFF" name="chart" id="chart" src="http://50.56.99.4/cmp/img/animations/open-flash-chart.swf" type="application/x-shockwave-flash">' % ('kas_name_%s_top_7dias_maq.xml' % (ip))
  logfile='%skas_name_%s_top_7dias_maq' % (pathlogs,ip)
  dict1=pickle.load(open(logfile))
  lastatu_old = open(logfile,'r').readlines()[-1]
  one=[]
  for i in dict1:one.append('%s=%s' % (i,dict1[i]))
  exitcounter=0
  swfdata='&title=Relatório Últimos 7 Dias,{font-size:20px; color: #FFFFFF; margin: 5px; background-color: #505050; padding:5px; padding-left: 20px; padding-right: 20px;}&&x_axis_steps=1&&y_ticks=5,10,5&&line=3,#87421F&&y_min=0&&y_max=20&&bg_colour=#FDF0D5&&pie=60,#505050,#000000&&colours=#1E90FF,#BC8F8F,#00FFFF,#7A67EE,#FA8072,#7FFFD4,#00FF7F,#FF7F50,#FFFF00,#FF00FF&&links=&&tool_tip=#val#'
  intvalues=[]
  strvalues=[]
  print 'Top M&aacute;quina Semana'
  for i in sorted(dict1.items(), cmp=lambda x,y: int(y[1]) - int(x[1])):
    print ('M&aacute;quina - %s %s'% (i[0],i[1]))
    strvalues.append(i[0])
    intvalues.append(str(i[1]))
    if exitcounter >=9:break
    else:exitcounter=exitcounter+1
  swfdata+='\n&values=%s&' % ','.join(intvalues)
  swfdata+='\n&pie_labels=%s&' % ','.join(strvalues)
  open('%skas_name_%s_top_7dias_maq.xml' % (pathlogs,ip),'w').write(swfdata)

  
  if os.path.isfile('%skas_name_%s_top_mes_maq.xml' % (pathlogs,ip)):#se o arquivo existe
    print '<embed width="600" height="470" flashvars="data=http://50.56.99.4/cmp/data/%s" allowscriptaccess="sameDomain" quality="high" bgcolor="#FFFFFF" name="chart" id="chart" src="http://50.56.99.4/cmp/img/animations/open-flash-chart.swf" type="application/x-shockwave-flash">' % ('kas_name_%s_top_mes_maq.xml' % (ip))

  logfile='%skas_name_%s_top_mes_maq' % (pathlogs,ip)
  dict1=pickle.load(open(logfile))
  lastatu_old = open(logfile,'r').readlines()[-1]
  one=[]
  for i in dict1:one.append('%s=%s' % (i,dict1[i]))
  exitcounter=0
  swfdata='&title=Relatório do Mês,{font-size:20px; color: #FFFFFF; margin: 5px; background-color: #505050; padding:5px; padding-left: 20px; padding-right: 20px;}&&x_axis_steps=1&&y_ticks=5,10,5&&line=3,#87421F&&y_min=0&&y_max=20&&bg_colour=#FDF0D5&&pie=60,#505050,#000000&&colours=#1E90FF,#BC8F8F,#00FFFF,#7A67EE,#FA8072,#7FFFD4,#00FF7F,#FF7F50,#FFFF00,#FF00FF&&links=&&tool_tip=#val#'
  intvalues=[]
  strvalues=[]
  print 'Top M&aacute;quina M&ecirc;s'
  for i in sorted(dict1.items(), cmp=lambda x,y: int(y[1]) - int(x[1])):
    print ('M&aacute;quina - %s %s'% (i[0],i[1]))
    strvalues.append(i[0])
    intvalues.append(str(i[1]))
    if exitcounter >=9:break
    else:exitcounter=exitcounter+1
  swfdata+='\n&values=%s&' % ','.join(intvalues)
  swfdata+='\n&pie_labels=%s&' % ','.join(strvalues)
  open('%skas_name_%s_top_mes_maq.xml' % (pathlogs,ip),'w').write(swfdata)
    
  if os.path.isfile('%skas_name_%s_top_ano_maq.xml' % (pathlogs,ip)):#se o arquivo existe 
    print '<embed width="600" height="470" flashvars="data=http://50.56.99.4/cmp/data/%s" allowscriptaccess="sameDomain" quality="high" bgcolor="#FFFFFF" name="chart" id="chart" src="http://50.56.99.4/cmp/img/animations/open-flash-chart.swf" type="application/x-shockwave-flash">' % ('kas_name_%s_top_ano_maq.xml' % (ip))
  logfile='%skas_name_%s_top_ano_maq' % (pathlogs,ip)
  dict1=pickle.load(open(logfile))
  lastatu_old = open(logfile,'r').readlines()[-1]
  one=[]
  for i in dict1:one.append('%s=%s' % (i,dict1[i]))
  exitcounter=0
  swfdata='&title=Relatório do Ano,{font-size:20px; color: #FFFFFF; margin: 5px; background-color: #505050; padding:5px; padding-left: 20px; padding-right: 20px;}&&x_axis_steps=1&&y_ticks=5,10,5&&line=3,#87421F&&y_min=0&&y_max=20&&bg_colour=#FDF0D5&&pie=60,#505050,#000000&&colours=#1E90FF,#BC8F8F,#00FFFF,#7A67EE,#FA8072,#7FFFD4,#00FF7F,#FF7F50,#FFFF00,#FF00FF&&links=&&tool_tip=#val#'
  intvalues=[]
  strvalues=[]
  print 'Top M&aacute;quina Ano'
  for i in sorted(dict1.items(), cmp=lambda x,y: int(y[1]) - int(x[1])):
    print ('M&aacute;quina - %s %s'% (i[0],i[1]))
    strvalues.append(i[0])
    intvalues.append(str(i[1]))
    if exitcounter >=9:break
    else:exitcounter=exitcounter+1
  swfdata+='\n&values=%s&' % ','.join(intvalues)
  swfdata+='\n&pie_labels=%s&' % ','.join(strvalues)
  open('%skas_name_%s_top_ano_maq.xml' % (pathlogs,ip),'w').write(swfdata)

elif tipo == '19':#Kaspersky Top V&iacute;rus Gr&aacute;ficos

  print 'Kaspersky Top Virus'
  
  logfile='%skas_name_%s_top_dia_vir' % (pathlogs,ip)
  dict1=pickle.load(open(logfile))
  lastatu_old = open(logfile,'r').readlines()[-1]
  one=[]
  for i in dict1:one.append('%s=%s' % (i,dict1[i]))
  exitcounter=0
  swfdata='&title=Relatório do Dia,{font-size:20px; color: #FFFFFF; margin: 5px; background-color: #505050; padding:5px; padding-left: 20px; padding-right: 20px;}&&x_axis_steps=1&&y_ticks=5,10,5&&line=3,#87421F&&y_min=0&&y_max=20&&bg_colour=#FDF0D5&&pie=60,#505050,#000000&&colours=#1E90FF,#BC8F8F,#00FFFF,#7A67EE,#FA8072,#7FFFD4,#00FF7F,#FF7F50,#FFFF00,#FF00FF&&links=&&tool_tip=#val#'
  intvalues=[]
  strvalues=[]
  showgraph=True#rotina showgraph em desuso
  print '&Uacute;ltimo incidente %s' % lastatu_old
  for i in sorted(dict1.items(), cmp=lambda x,y: int(y[1]) - int(x[1])):
    if int(i[1]) >0:
      strvalues.append(i[0])
      intvalues.append(str(i[1]))
      showgraph=True
      if exitcounter >=9:break
      else:exitcounter=exitcounter+1
  swfdata+='\n&values=%s&' % ','.join(intvalues)
  swfdata+='\n&pie_labels=%s&' % ','.join(strvalues)
  open('%skas_name_%s_top_dia_vir.xml' % (pathlogs,ip),'w').write(swfdata)

  if showgraph is True:
    print '<embed width="600" height="470" flashvars="data=http://50.56.99.4/cmp/data/%s" allowscriptaccess="sameDomain" quality="high" bgcolor="#FFFFFF" name="chart" id="chart" src="http://50.56.99.4/cmp/img/animations/open-flash-chart.swf" type="application/x-shockwave-flash">' % ('kas_name_%s_top_dia_vir.xml' % (ip))  
    for i in sorted(dict1.items(), cmp=lambda x,y: int(y[1]) - int(x[1])):
      if i[1] >0:
	print ('V&iacute;rus - <a href="http://www.google.com.br/search?hl=pt-BR&q=%s">%s</a> %s'% (i[0],i[0],i[1]))

  
  #print 'Kaspersky Top V&iacute;rus Gr&aacute;ficos'
  if os.path.isfile('%skas_name_%s_top_7dias_vir.xml' % (pathlogs,ip)):#se o arquivo existe  
    print '<embed width="600" height="470" flashvars="data=http://50.56.99.4/cmp/data/%s" allowscriptaccess="sameDomain" quality="high" bgcolor="#FFFFFF" name="chart" id="chart" src="http://50.56.99.4/cmp/img/animations/open-flash-chart.swf" type="application/x-shockwave-flash">' % ('kas_name_%s_top_7dias_vir.xml' % (ip))
  logfile='%skas_name_%s_top_7dias_vir' % (pathlogs,ip)
  dict1=pickle.load(open(logfile))
  lastatu_old = open(logfile,'r').readlines()[-1]
  one=[]
  for i in dict1:one.append('%s=%s' % (i,dict1[i]))
  exitcounter=0
  swfdata='&title=Relatório Últimos 7 Dias,{font-size:20px; color: #FFFFFF; margin: 5px; background-color: #505050; padding:5px; padding-left: 20px; padding-right: 20px;}&&x_axis_steps=1&&y_ticks=5,10,5&&line=3,#87421F&&y_min=0&&y_max=20&&bg_colour=#FDF0D5&&pie=60,#505050,#000000&&colours=#1E90FF,#BC8F8F,#00FFFF,#7A67EE,#FA8072,#7FFFD4,#00FF7F,#FF7F50,#FFFF00,#FF00FF&&links=&&tool_tip=#val#'
  intvalues=[]
  strvalues=[]
  print 'Top V&iacute;rus Semana'
  for i in sorted(dict1.items(), cmp=lambda x,y: int(y[1]) - int(x[1])):
    #print ('V&iacute;rus - %s %s'% (i[0],i[1]))
    print ('V&iacute;rus - <a href="http://www.google.com.br/search?hl=pt-BR&q=%s">%s</a> %s'% (i[0],i[0],i[1]))
    strvalues.append(i[0])
    intvalues.append(str(i[1]))
    if exitcounter >=9:break
    else:exitcounter=exitcounter+1
  swfdata+='\n&values=%s&' % ','.join(intvalues)
  swfdata+='\n&pie_labels=%s&' % ','.join(strvalues)
  open('%skas_name_%s_top_7dias_vir.xml' % (pathlogs,ip),'w').write(swfdata)
    
    
  if os.path.isfile('%skas_name_%s_top_mes_vir.xml' % (pathlogs,ip)):#se o arquivo existe  
    print '<embed width="600" height="470" flashvars="data=http://50.56.99.4/cmp/data/%s" allowscriptaccess="sameDomain" quality="high" bgcolor="#FFFFFF" name="chart" id="chart" src="http://50.56.99.4/cmp/img/animations/open-flash-chart.swf" type="application/x-shockwave-flash">' % ('kas_name_%s_top_mes_vir.xml' % (ip))    
  logfile='%skas_name_%s_top_mes_vir' % (pathlogs,ip)
  dict1=pickle.load(open(logfile))
  lastatu_old = open(logfile,'r').readlines()[-1]
  one=[]
  for i in dict1:one.append('%s=%s' % (i,dict1[i]))
  exitcounter=0
  swfdata='&title=Relatório do Mês,{font-size:20px; color: #FFFFFF; margin: 5px; background-color: #505050; padding:5px; padding-left: 20px; padding-right: 20px;}&&x_axis_steps=1&&y_ticks=5,10,5&&line=3,#87421F&&y_min=0&&y_max=20&&bg_colour=#FDF0D5&&pie=60,#505050,#000000&&colours=#1E90FF,#BC8F8F,#00FFFF,#7A67EE,#FA8072,#7FFFD4,#00FF7F,#FF7F50,#FFFF00,#FF00FF&&links=&&tool_tip=#val#'
  intvalues=[]
  strvalues=[]
  print 'Top V&iacute;rus M&ecirc;s'
  for i in sorted(dict1.items(), cmp=lambda x,y: int(y[1]) - int(x[1])):
    #print ('V&iacute;rus - %s %s'% (i[0],i[1]))
    print ('V&iacute;rus - <a href="http://www.google.com.br/search?hl=pt-BR&q=%s">%s</a> %s'% (i[0],i[0],i[1]))
    strvalues.append(i[0])
    intvalues.append(str(i[1]))
    if exitcounter >=9:break
    else:exitcounter=exitcounter+1
  swfdata+='\n&values=%s&' % ','.join(intvalues)
  swfdata+='\n&pie_labels=%s&' % ','.join(strvalues)
  open('%skas_name_%s_top_mes_vir.xml' % (pathlogs,ip),'w').write(swfdata)
  
  if os.path.isfile('%skas_name_%s_top_ano_vir.xml' % (pathlogs,ip)):#se o arquivo existe  
    print '<embed width="600" height="470" flashvars="data=http://50.56.99.4/cmp/data/%s" allowscriptaccess="sameDomain" quality="high" bgcolor="#FFFFFF" name="chart" id="chart" src="http://50.56.99.4/cmp/img/animations/open-flash-chart.swf" type="application/x-shockwave-flash">' % ('kas_name_%s_top_ano_vir.xml' % (ip))
  logfile='%skas_name_%s_top_ano_vir' % (pathlogs,ip)
  dict1=pickle.load(open(logfile))
  lastatu_old = open(logfile,'r').readlines()[-1]
  one=[]
  for i in dict1:one.append('%s=%s' % (i,dict1[i]))
  exitcounter=0
  swfdata='&title=Relatório do Ano,{font-size:20px; color: #FFFFFF; margin: 5px; background-color: #505050; padding:5px; padding-left: 20px; padding-right: 20px;}&&x_axis_steps=1&&y_ticks=5,10,5&&line=3,#87421F&&y_min=0&&y_max=20&&bg_colour=#FDF0D5&&pie=60,#505050,#000000&&colours=#1E90FF,#BC8F8F,#00FFFF,#7A67EE,#FA8072,#7FFFD4,#00FF7F,#FF7F50,#FFFF00,#FF00FF&&links=&&tool_tip=#val#'
  intvalues=[]
  strvalues=[]
  print 'Top V&iacute;rus Ano'
  for i in sorted(dict1.items(), cmp=lambda x,y: int(y[1]) - int(x[1])):
    #print ('V&iacute;rus - %s %s'% (i[0],i[1]))
    print ('V&iacute;rus - <a href="http://www.google.com.br/search?hl=pt-BR&q=%s">%s</a> %s'% (i[0],i[0],i[1]))
    strvalues.append(i[0])
    intvalues.append(str(i[1]))
    if exitcounter >=9:break
    else:exitcounter=exitcounter+1
  swfdata+='\n&values=%s&' % ','.join(intvalues)
  swfdata+='\n&pie_labels=%s&' % ','.join(strvalues)
  open('%skas_name_%s_top_ano_vir.xml' % (pathlogs,ip),'w').write(swfdata)


else:
  print 'CRITICAL - TIPO INVALIDO'
  sys.exit(1)
