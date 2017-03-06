#!/usr/bin/env python
# -*- coding: utf-8 -*-
import commands
import sys


def MyISAMIndexes():#MyISAMIndexes
  myKeyReadRequests=(commands.getoutput("/usr/bin/snmpwalk -t 100000 -v 1 -c  %s %s .1.3.6.1.4.1.20267.200.1.1" %(community,str(host)))).split(":")[3].replace(' ','')
  myKeyReads=(commands.getoutput("/usr/bin/snmpwalk -t 100000 -v 1 -c  %s %s .1.3.6.1.4.1.20267.200.1.2" %(community,str(host)))).split(":")[3].replace(' ','')
  myKeyWriteRequests=(commands.getoutput("/usr/bin/snmpwalk -t 100000 -v 1 -c  %s %s .1.3.6.1.4.1.20267.200.1.3" %(community,str(host)))).split(":")[3].replace(' ','')
  myKeyWrites=(commands.getoutput("/usr/bin/snmpwalk -t 100000 -v 1 -c  %s %s .1.3.6.1.4.1.20267.200.1.4" %(community,str(host)))).split(":")[3].replace(' ','')
  tt=int(myKeyReadRequests)+int(myKeyReads)+int(myKeyWriteRequests)+int(myKeyWrites)
  print 'MySQL ISAM Indexes %d|myKeyReadRequests=%s myKeyReads=%s myKeyWriteRequests=%s myKeyWrites=%s' % (\
  tt,myKeyReadRequests,myKeyReads,myKeyWriteRequests,myKeyWrites)
  
def MyCommandCounters():#MySQL Command Counters
  myQuestions=(commands.getoutput("/usr/bin/snmpwalk -t 100000 -v 1 -c  %s %s .1.3.6.1.4.1.20267.200.1.75" %(community,str(host)))).split(":")[3].replace(' ','')
  myComSelect=(commands.getoutput("/usr/bin/snmpwalk -t 100000 -v 1 -c  %s %s .1.3.6.1.4.1.20267.200.1.78" %(community,str(host)))).split(":")[3].replace(' ','')
  myComDelete=(commands.getoutput("/usr/bin/snmpwalk -t 100000 -v 1 -c  %s %s .1.3.6.1.4.1.20267.200.1.79" %(community,str(host)))).split(":")[3].replace(' ','')
  myComInsert=(commands.getoutput("/usr/bin/snmpwalk -t 100000 -v 1 -c  %s %s .1.3.6.1.4.1.20267.200.1.77" %(community,str(host)))).split(":")[3].replace(' ','')
  myComUpdate=(commands.getoutput("/usr/bin/snmpwalk -t 100000 -v 1 -c  %s %s .1.3.6.1.4.1.20267.200.1.76" %(community,str(host)))).split(":")[3].replace(' ','')
  myComReplace=(commands.getoutput("/usr/bin/snmpwalk -t 100000 -v 1 -c  %s %s .1.3.6.1.4.1.20267.200.1.80" %(community,str(host)))).split(":")[3].replace(' ','')
  myComLoad=(commands.getoutput("/usr/bin/snmpwalk -t 100000 -v 1 -c  %s %s .1.3.6.1.4.1.20267.200.1.81" %(community,str(host)))).split(":")[3].replace(' ','')
  myComDeleteMulti=(commands.getoutput("/usr/bin/snmpwalk -t 100000 -v 1 -c  %s %s .1.3.6.1.4.1.20267.200.1.84" %(community,str(host)))).split(":")[3].replace(' ','')
  myComInsertSelect=(commands.getoutput("/usr/bin/snmpwalk -t 100000 -v 1 -c  %s %s .1.3.6.1.4.1.20267.200.1.83" %(community,str(host)))).split(":")[3].replace(' ','')
  myComUpdateMulti=(commands.getoutput("/usr/bin/snmpwalk -t 100000 -v 1 -c  %s %s .1.3.6.1.4.1.20267.200.1.82" %(community,str(host)))).split(":")[3].replace(' ','')
  myComReplaceSelect=(commands.getoutput("/usr/bin/snmpwalk -t 100000 -v 1 -c  %s %s .1.3.6.1.4.1.20267.200.1.85" %(community,str(host)))).split(":")[3].replace(' ','')
  tt=int(myQuestions)+int(myComSelect)+int(myComDelete)+int(myComInsert)+int(myComUpdate)+\
    int(myComReplace)+int(myComLoad)+int(myComDeleteMulti)+int(myComInsertSelect)+int(myComUpdateMulti)+int(myComReplaceSelect)  
  print 'MySQL Command Counters %d|myQuestions=%s myComSelect=%s myComDelete=%s myComInsert=%s myComUpdate=%s myComReplace=%s myComLoad=%s myComDeleteMulti=%s myComInsertSelect=%s myComUpdateMulti=%s myComReplaceSelect=%s' % (\
    tt,myQuestions,myComSelect,myComDelete,myComInsert,myComUpdate,myComReplace,myComLoad,myComDeleteMulti,myComInsertSelect,myComUpdateMulti,myComReplaceSelect)
  
def MyConnections():#MySQL Connections
  myMaxConnections=(commands.getoutput("/usr/bin/snmpwalk -t 100000 -v 1 -c  %s %s .1.3.6.1.4.1.20267.200.1.58" %(community,str(host)))).split(":")[3].replace(' ','')
  myMaxUsedConnectins=(commands.getoutput("/usr/bin/snmpwalk -t 100000 -v 1 -c  %s %s .1.3.6.1.4.1.20267.200.1.52" %(community,str(host)))).split(":")[3].replace(' ','')
  myAbortedClients=(commands.getoutput("/usr/bin/snmpwalk -t 100000 -v 1 -c  %s %s .1.3.6.1.4.1.20267.200.1.50" %(community,str(host)))).split(":")[3].replace(' ','')
  myAbortedConnects=(commands.getoutput("/usr/bin/snmpwalk -t 100000 -v 1 -c  %s %s .1.3.6.1.4.1.20267.200.1.51" %(community,str(host)))).split(":")[3].replace(' ','')
  myThreadsConnected=(commands.getoutput("/usr/bin/snmpwalk -t 100000 -v 1 -c  %s %s .1.3.6.1.4.1.20267.200.1.55" %(community,str(host)))).split(":")[3].replace(' ','')
  myConnections=(commands.getoutput("/usr/bin/snmpwalk -t 100000 -v 1 -c  %s %s .1.3.6.1.4.1.20267.200.1.60" %(community,str(host)))).split(":")[3].replace(' ','')
  tt=int(myMaxConnections)+int(myMaxUsedConnectins)+int(myAbortedClients)+int(myAbortedConnects)+int(myThreadsConnected)+int(myConnections)
  print "MySQL Connections %d|myMaxConnections=%s myMaxUsedConnectins=%s myAbortedClients=%s myAbortedConnects=%s myThreadsConnected=%s myConnections=%s" % (\
  tt,myMaxConnections,myMaxUsedConnectins,myAbortedClients,myAbortedConnects,myThreadsConnected,myConnections)
  
def MyTableLocks():#MySQL Table Locks
  myTableLocksImmedit=(commands.getoutput("/usr/bin/snmpwalk -t 100000 -v 1 -c  %s %s .1.3.6.1.4.1.20267.200.1.42" %(community,str(host)))).split(":")[3].replace(' ','')
  myTableLocksWaited=(commands.getoutput("/usr/bin/snmpwalk -t 100000 -v 1 -c  %s %s .1.3.6.1.4.1.20267.200.1.41" %(community,str(host)))).split(":")[3].replace(' ','')
  mySlowQueries=(commands.getoutput("/usr/bin/snmpwalk -t 100000 -v 1 -c  %s %s .1.3.6.1.4.1.20267.200.1.43" %(community,str(host)))).split(":")[3].replace(' ','')
  print "MySQL Table Locks: TableLocksImmedit %s ,TableLocksWaited %s ,SlowQueries %s|myTableLocksImmedit=%s myTableLocksWaited=%s mySlowQueries=%s" % (
  myTableLocksImmedit,myTableLocksWaited,mySlowQueries,myTableLocksImmedit,myTableLocksWaited,mySlowQueries)
  

def MyBinary():#MySQL Binary/Relay Logs
  myBinlogCacheUse=(commands.getoutput("/usr/bin/snmpwalk -t 100000 -v 1 -c  %s %s .1.3.6.1.4.1.20267.200.1.107" %(community,str(host)))).split(":")[3].replace(' ','')
  myBinlogCacheDiskUs=(commands.getoutput("/usr/bin/snmpwalk -t 100000 -v 1 -c  %s %s .1.3.6.1.4.1.20267.200.1.106" %(community,str(host)))).split(":")[3].replace(' ','')
  myBinaryLogSpace=(commands.getoutput("/usr/bin/snmpwalk -t 100000 -v 1 -c  %s %s .1.3.6.1.4.1.20267.200.1.108" %(community,str(host)))).split(":")[3].replace(' ','')
  myRelayLogSpace=(commands.getoutput("/usr/bin/snmpwalk -t 100000 -v 1 -c  %s %s .1.3.6.1.4.1.20267.200.1.104" %(community,str(host)))).split(":")[3].replace(' ','')
  tt=int(myBinlogCacheUse)+int(myBinlogCacheDiskUs)+int(myBinaryLogSpace)+int(myRelayLogSpace)
  print "MySQL Binary/Relay Logs %d|myBinlogCacheUse=%s myBinlogCacheDiskUs=%s myBinaryLogSpace=%s myRelayLogSpace=%s" % (
  tt,myBinlogCacheUse,myBinlogCacheDiskUs,myBinaryLogSpace,myRelayLogSpace)
  
def MyFiles():#MySQL Files and Tables
  myTableCache=(commands.getoutput("/usr/bin/snmpwalk -t 100000 -v 1 -c  %s %s .1.3.6.1.4.1.20267.200.1.49" %(community,str(host)))).split(":")[3].replace(' ','')
  myOpenTables=(commands.getoutput("/usr/bin/snmpwalk -t 100000 -v 1 -c  %s %s .1.3.6.1.4.1.20267.200.1.45" %(community,str(host)))).split(":")[3].replace(' ','')
  myOpenFiles=(commands.getoutput("/usr/bin/snmpwalk -t 100000 -v 1 -c  %s %s .1.3.6.1.4.1.20267.200.1.44" %(community,str(host)))).split(":")[3].replace(' ','')
  myOpenedTables=(commands.getoutput("/usr/bin/snmpwalk -t 100000 -v 1 -c  %s %s .1.3.6.1.4.1.20267.200.1.46" %(community,str(host)))).split(":")[3].replace(' ','')
  tt=int(myTableCache)+int(myOpenTables)+int(myOpenFiles)+int(myOpenedTables)
  print "MySQL Files and Tables %d|myTableCache=%s myOpenTables=%s myOpenFiles=%s myOpenedTables=%s" % (
  tt,myTableCache,myOpenTables,myOpenFiles,myOpenedTables)

def MyProcesslist():#MySQL Processlist
  myStateClosingTabls=(commands.getoutput("/usr/bin/snmpwalk -t 100000 -v 1 -c  %s %s .1.3.6.1.4.1.20267.200.1.109" %(community,str(host)))).split(":")[3].replace(' ','')
  myStateCpyngTTmpTbl=(commands.getoutput("/usr/bin/snmpwalk -t 100000 -v 1 -c  %s %s .1.3.6.1.4.1.20267.200.1.110" %(community,str(host)))).split(":")[3].replace(' ','')
  myStateEnd=(commands.getoutput("/usr/bin/snmpwalk -t 100000 -v 1 -c  %s %s .1.3.6.1.4.1.20267.200.1.111" %(community,str(host)))).split(":")[3].replace(' ','')
  myStateFreeingItems=(commands.getoutput("/usr/bin/snmpwalk -t 100000 -v 1 -c  %s %s .1.3.6.1.4.1.20267.200.1.112" %(community,str(host)))).split(":")[3].replace(' ','')
  myStateInit=(commands.getoutput("/usr/bin/snmpwalk -t 100000 -v 1 -c  %s %s .1.3.6.1.4.1.20267.200.1.113" %(community,str(host)))).split(":")[3].replace(' ','')
  myStateLocked=(commands.getoutput("/usr/bin/snmpwalk -t 100000 -v 1 -c  %s %s .1.3.6.1.4.1.20267.200.1.114" %(community,str(host)))).split(":")[3].replace(' ','')
  myStateLogin=(commands.getoutput("/usr/bin/snmpwalk -t 100000 -v 1 -c  %s %s .1.3.6.1.4.1.20267.200.1.115" %(community,str(host)))).split(":")[3].replace(' ','')
  myStatePreparing=(commands.getoutput("/usr/bin/snmpwalk -t 100000 -v 1 -c  %s %s .1.3.6.1.4.1.20267.200.1.116" %(community,str(host)))).split(":")[3].replace(' ','')
  myStateReadingFrmNt=(commands.getoutput("/usr/bin/snmpwalk -t 100000 -v 1 -c  %s %s .1.3.6.1.4.1.20267.200.1.117" %(community,str(host)))).split(":")[3].replace(' ','')
  myStateSendingData=(commands.getoutput("/usr/bin/snmpwalk -t 100000 -v 1 -c  %s %s .1.3.6.1.4.1.20267.200.1.118" %(community,str(host)))).split(":")[3].replace(' ','')
  myStateSortingReslt=(commands.getoutput("/usr/bin/snmpwalk -t 100000 -v 1 -c  %s %s .1.3.6.1.4.1.20267.200.1.119" %(community,str(host)))).split(":")[3].replace(' ','')
  myStateStatistics=(commands.getoutput("/usr/bin/snmpwalk -t 100000 -v 1 -c  %s %s .1.3.6.1.4.1.20267.200.1.120" %(community,str(host)))).split(":")[3].replace(' ','')
  myStateUpdating=(commands.getoutput("/usr/bin/snmpwalk -t 100000 -v 1 -c  %s %s .1.3.6.1.4.1.20267.200.1.121" %(community,str(host)))).split(":")[3].replace(' ','')
  myStateWritingToNet=(commands.getoutput("/usr/bin/snmpwalk -t 100000 -v 1 -c  %s %s .1.3.6.1.4.1.20267.200.1.122" %(community,str(host)))).split(":")[3].replace(' ','')
  myStateNone=(commands.getoutput("/usr/bin/snmpwalk -t 100000 -v 1 -c  %s %s .1.3.6.1.4.1.20267.200.1.123" %(community,str(host)))).split(":")[3].replace(' ','')
  myStateOther=(commands.getoutput("/usr/bin/snmpwalk -t 100000 -v 1 -c  %s %s .1.3.6.1.4.1.20267.200.1.124" %(community,str(host)))).split(":")[3].replace(' ','')
  tt=int(myStateClosingTabls)+int(myStateCpyngTTmpTbl)+int(myStateEnd)+int(myStateFreeingItems)+int(myStateInit)+\
  int(myStateLocked)+int(myStateLogin)+int(myStatePreparing)+int(myStateReadingFrmNt)+int(myStateSendingData)+int(myStateSortingReslt)+\
  int(myStateStatistics)+int(myStateUpdating)+int(myStateWritingToNet)+int(myStateNone)+int(myStateOther)
  print "MySQL Processlist %d|myStateClosingTabls=%s myStateCpyngTTmpTbl=%s myStateEnd=%s myStateFreeingItems=%s myStateInit=%s myStateLocked=%s myStateLogin=%s myStatePreparing=%s myStateReadingFrmNt=%s myStateSendingData=%s myStateSortingReslt=%s myStateStatistics=%s myStateUpdating=%s myStateWritingToNet=%s myStateNone=%s myStateOther=%s" % (\
  tt,myStateClosingTabls,myStateCpyngTTmpTbl,myStateEnd,myStateFreeingItems,myStateInit,myStateLocked,myStateLogin,myStatePreparing,myStateReadingFrmNt,myStateSendingData,myStateSortingReslt,myStateStatistics,myStateUpdating,myStateWritingToNet,myStateNone,myStateOther)
  
def MyQuery():#MySQL Query Cache
  myQcacheQuerisInCch=(commands.getoutput("/usr/bin/snmpwalk -t 100000 -v 1 -c  %s %s .1.3.6.1.4.1.20267.200.1.72" %(community,str(host)))).split(":")[3].replace(' ','')
  myQcacheHits=(commands.getoutput("/usr/bin/snmpwalk -t 100000 -v 1 -c  %s %s .1.3.6.1.4.1.20267.200.1.68" %(community,str(host)))).split(":")[3].replace(' ','')
  myQcacheInserts=(commands.getoutput("/usr/bin/snmpwalk -t 100000 -v 1 -c  %s %s .1.3.6.1.4.1.20267.200.1.69" %(community,str(host)))).split(":")[3].replace(' ','')
  myQcacheNotCached=(commands.getoutput("/usr/bin/snmpwalk -t 100000 -v 1 -c  %s %s .1.3.6.1.4.1.20267.200.1.71" %(community,str(host)))).split(":")[3].replace(' ','')
  myQcacheLowmemPruns=(commands.getoutput("/usr/bin/snmpwalk -t 100000 -v 1 -c  %s %s .1.3.6.1.4.1.20267.200.1.70" %(community,str(host)))).split(":")[3].replace(' ','')
  tt=int(myQcacheQuerisInCch)+int(myQcacheHits)+int(myQcacheInserts)+int(myQcacheNotCached)+int(myQcacheLowmemPruns)
  print "MySQL Query Cache %d|myQcacheQuerisInCch=%s myQcacheHits=%s myQcacheInserts=%s myQcacheNotCached=%s myQcacheLowmemPruns=%s" % (\
  tt,myQcacheQuerisInCch,myQcacheHits,myQcacheInserts,myQcacheNotCached,myQcacheLowmemPruns)
  
def MyQueryMemory():#MySQL Query Cache Memory
  myQueryCacheSize=(commands.getoutput("/usr/bin/snmpwalk -t 100000 -v 1 -c  %s %s .1.3.6.1.4.1.20267.200.1.74" %(community,str(host)))).split(":")[3].replace(' ','')
  myQcacheFreeMemory=(commands.getoutput("/usr/bin/snmpwalk -t 100000 -v 1 -c  %s %s .1.3.6.1.4.1.20267.200.1.67" %(community,str(host)))).split(":")[3].replace(' ','')
  myQcacheTotalBlocks=(commands.getoutput("/usr/bin/snmpwalk -t 100000 -v 1 -c  %s %s .1.3.6.1.4.1.20267.200.1.73" %(community,str(host)))).split(":")[3].replace(' ','')
  myQcacheFreeBlocks=(commands.getoutput("/usr/bin/snmpwalk -t 100000 -v 1 -c  %s %s .1.3.6.1.4.1.20267.200.1.66" %(community,str(host)))).split(":")[3].replace(' ','')
  tt=int(myQueryCacheSize)+int(myQcacheFreeMemory)+int(myQcacheTotalBlocks)+int(myQcacheFreeBlocks)
  print "MySQL Query Cache Memory %d|myQueryCacheSize=%s myQcacheFreeMemory=%s myQcacheTotalBlocks=%s myQcacheFreeBlocks=%s" % (\
  tt,myQueryCacheSize,myQcacheFreeMemory,myQcacheTotalBlocks,myQcacheFreeBlocks)

def MySelectType():#MySQL Select Types
  mySelectFullJoin=(commands.getoutput("/usr/bin/snmpwalk -t 100000 -v 1 -c  %s %s .1.3.6.1.4.1.20267.200.1.86" %(community,str(host)))).split(":")[3].replace(' ','')
  mySelectFullRangeJn=(commands.getoutput("/usr/bin/snmpwalk -t 100000 -v 1 -c  %s %s .1.3.6.1.4.1.20267.200.1.87" %(community,str(host)))).split(":")[3].replace(' ','')
  mySelectRange=(commands.getoutput("/usr/bin/snmpwalk -t 100000 -v 1 -c  %s %s .1.3.6.1.4.1.20267.200.1.88" %(community,str(host)))).split(":")[3].replace(' ','')
  mySelectRangeCheck=(commands.getoutput("/usr/bin/snmpwalk -t 100000 -v 1 -c  %s %s .1.3.6.1.4.1.20267.200.1.89" %(community,str(host)))).split(":")[3].replace(' ','')
  mySelectScan=(commands.getoutput("/usr/bin/snmpwalk -t 100000 -v 1 -c  %s %s .1.3.6.1.4.1.20267.200.1.90" %(community,str(host)))).split(":")[3].replace(' ','')
  tt=int(mySelectFullJoin)+int(mySelectFullRangeJn)+int(mySelectRange)+int(mySelectRangeCheck)+int(mySelectScan)
  print "MySQL Select Types %d|mySelectFullJoin=%s mySelectFullRangeJn=%s mySelectRange=%s mySelectRangeCheck=%s mySelectScan=%s" % (\
  tt,mySelectFullJoin,mySelectFullRangeJn,mySelectRange,mySelectRangeCheck,mySelectScan)
  
def MySorts():#MySQL Sorts
  mySortRows=(commands.getoutput("/usr/bin/snmpwalk -t 100000 -v 1 -c  %s %s .1.3.6.1.4.1.20267.200.1.93" %(community,str(host)))).split(":")[3].replace(' ','')
  mySortRange=(commands.getoutput("/usr/bin/snmpwalk -t 100000 -v 1 -c  %s %s .1.3.6.1.4.1.20267.200.1.92" %(community,str(host)))).split(":")[3].replace(' ','')
  mySortMergePasses=(commands.getoutput("/usr/bin/snmpwalk -t 100000 -v 1 -c  %s %s .1.3.6.1.4.1.20267.200.1.91" %(community,str(host)))).split(":")[3].replace(' ','')
  mySortScan=(commands.getoutput("/usr/bin/snmpwalk -t 100000 -v 1 -c  %s %s .1.3.6.1.4.1.20267.200.1.94" %(community,str(host)))).split(":")[3].replace(' ','')
  tt=int(mySortRows)+int(mySortRange)+int(mySortMergePasses)+int(mySortScan)
  print "MySQL Sorts %d|mySortRows=%s mySortRange=%s mySortMergePasses=%s mySortScan=%s" % (\
  tt,mySortRows,mySortRange,mySortMergePasses,mySortScan)
  
def MyTemporary():#MySQL Temporary Objects
  myCreatedTmpTables=(commands.getoutput("/usr/bin/snmpwalk -t 100000 -v 1 -c  %s %s .1.3.6.1.4.1.20267.200.1.95" %(community,str(host)))).split(":")[3].replace(' ','')
  myCreatedTmpDskTbls=(commands.getoutput("/usr/bin/snmpwalk -t 100000 -v 1 -c  %s %s .1.3.6.1.4.1.20267.200.1.96" %(community,str(host)))).split(":")[3].replace(' ','')
  myCreatedTmpFiles=(commands.getoutput("/usr/bin/snmpwalk -t 100000 -v 1 -c  %s %s .1.3.6.1.4.1.20267.200.1.97" %(community,str(host)))).split(":")[3].replace(' ','')
  tt=int(myCreatedTmpTables)+int(myCreatedTmpTables)+int(myCreatedTmpDskTbls)+int(myCreatedTmpFiles)
  print "MySQL Temporary Objects %d|myCreatedTmpTables=%s myCreatedTmpDskTbls=%s myCreatedTmpFiles=%s" % (\
  tt,myCreatedTmpTables,myCreatedTmpDskTbls,myCreatedTmpFiles)

def MyThreads():#MySQL Threads
  myThreadCacheSize=(commands.getoutput("/usr/bin/snmpwalk -t 100000 -v 1 -c  %s %s .1.3.6.1.4.1.20267.200.1.59" %(community,str(host)))).split(":")[3].replace(' ','')
  myThreadsCreated=(commands.getoutput("/usr/bin/snmpwalk -t 100000 -v 1 -c  %s %s .1.3.6.1.4.1.20267.200.1.56" %(community,str(host)))).split(":")[3].replace(' ','')
  print "MySQL Threads myThreadCacheSize %s ,myThreadsCreated %s|myThreadCacheSize=%s myThreadsCreated=%s" % (\
  myThreadCacheSize,myThreadsCreated,myThreadCacheSize,myThreadsCreated)


def uso():
  print "Centreon Plugin\nMysql Agent para Centreon por GemayelLira"
  print "Argumentos:host community tipo:"
  print "MyISAMIndexes,MyCommandCounters,MyConnections,MyTableLocks,MyBinary,"
  print "MyFiles,MyProcesslist,MyQuery,MyQueryMemory,MySelectType"
  print "MySorts,MyTemporary,MyThreads,"
  print "Ex.\n%s 192.168.3.161 u3fr0I9b5 MyISAMIndexes" % sys.argv[0] 
  #print 
  sys.exit(1)

args = sys.argv[1:]

if len(args)<3:
  uso()
else:
  #print args
  host=args[0]
  community=args[1]
  tipo=args[2]


if tipo == 'MyISAMIndexes':MyISAMIndexes()
elif tipo == 'MyCommandCounters':MyCommandCounters()
elif tipo == 'MyConnections':MyConnections()
elif tipo == 'MyTableLocks':MyTableLocks()
elif tipo == 'MyBinary':MyBinary()
elif tipo == 'MyFiles':MyFiles()
elif tipo == 'MyProcesslist':MyProcesslist()
elif tipo == 'MyQuery':MyQuery()
elif tipo == 'MyQueryMemory':MyQueryMemory()
elif tipo == 'MySelectType':MySelectType()
elif tipo == 'MySorts':MySorts()
elif tipo == 'MyTemporary':MyTemporary()
elif tipo == 'MyThreads':MyThreads()
else:print "Mencione um tipo valido!";uso()

  
  
#host='192.168.3.161'
#community='u3fr0I9b5'
#status=(commands.getoutput("/usr/bin/snmpwalk -t 100000 -v 1 -c  %s %s .1.3.6.1.4.1.20267.200.1.1" %(community,str(host)))).split(":")[3].replace(' ','')
#print '%s' % status