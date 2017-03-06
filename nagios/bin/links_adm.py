#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
import sys
try:
    import MySQLdb
except:
    print "Impossivel continuar nao tenho modulo mysql",e
    sys.exit(1)
    
try:
    db = MySQLdb.connect(host="174.138.65.251",    # your host, usually localhost
                         user="argus",         # your username
                         passwd="labs3cur1t1",  # your password
                         db="argus")
    cursor = db.cursor()
except Exception,e:
    logging.info("Erro ao conectar ao banco %s"%e)        
    sys.exit(1)


args = sys.argv[1:]
if len(args)<1:
    print "Links Adm to FLOW"
    print "list"
    print "check cliente"
    print 'insert "cliente" "ifacecoleta" "ipcoleta" "nome" "speed" "img" "nomecmp" "ipcmp" "type" "ord" "hostname_cmp" "cmp_disp_host" "cmp_disp_service" "valorlink"'
    print "del cliente #vai deleta toda info do cliente"
    sys.exit(1)
else:
    tipo = args[0]
    
if tipo == "list":
    sql = "select id,cliente,ifacecoleta,ipcoleta,nome,speed,img,nomecmp,ipcmp,type,ord,hostname_cmp,cmp_disp_host,cmp_disp_service,valorlink from links"
    cursor.execute(sql)    
    print "id|cliente|ifacecoleta|ipcoleta|nome|speed|img|nomecmp|ipcmp|type|ord|hostname_cmp|cmp_disp_host|cmp_disp_service|valorlink"
    for x in cursor.fetchall():
        id,cliente,ifacecoleta,ipcoleta,nome,speed,img,nomecmp,ipcmp,type,ord,hostname_cmp,cmp_disp_host,cmp_disp_service,valorlink = x
        
        print id,"%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s"%(cliente,ifacecoleta,ipcoleta,nome,speed,img,nomecmp,ipcmp,type,ord,hostname_cmp,cmp_disp_host,cmp_disp_service,valorlink)
elif tipo == "insert":
    try:
        cliente,ifacecoleta,ipcoleta,nome,speed,img,nomecmp,ipcmp,type,ord,hostname_cmp,cmp_disp_host,cmp_disp_service,valorlink = args[1:]
        ord = int(ord);
    except Exception,e:
        print "Erro argumento invalido,",e
        sys.exit(1)
    sql = "insert into links (cliente,ifacecoleta,ipcoleta,nome,speed,img,nomecmp,ipcmp,type,ord,hostname_cmp,cmp_disp_host,cmp_disp_service,valorlink) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)";    
    cursor.execute(sql,(cliente,ifacecoleta,ipcoleta,nome,speed,img,nomecmp,ipcmp,type,ord,hostname_cmp,cmp_disp_host,cmp_disp_service,valorlink))    
    print "Valor inserido"
elif tipo == "check":
    name = args[1]    
    sql = "select cliente from links where cliente=%s limit 1"
    cursor.execute(sql,(name))    
    e=0
    for x in cursor.fetchall():
        print "Existe"
        e=1
    if  e==0:
        print "nao existe"
       
elif tipo == "del":
    name = args[1]
    sql = "delete from links where cliente = %s"
    cursor.execute(sql,(name))
    print "Deletando id",id
else:
    print "Opcao invalida"
    sys.exit(1)
db.commit()
db.close()

