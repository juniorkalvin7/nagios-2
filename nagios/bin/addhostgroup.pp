#puppet apply addhostgroup.pp --parser=future
$hosts = 
["disponibilidade_fundacao_emb",
"disponibilidade_fundacao_rnp",
"ad-prod-fjmontello-01",
"app-prod-fjmontello-01",
"app-prod-fjmontello-02",
"bkp-prod-fjmontello-01",
"chat-prod-fjmontello-01",
"colaborador-prod-fjmontello-01",
"cp-agent-prod-fjmontello-01",
"dc-prod-fjmontello-01",
"ecm-awqc00-prod-fjmontello",
"ecm-awqc01-prod-fjmontello",
"ecm-awqc02-prod-fjmontello",
"ecm-sp-prod-fjmontello",
"ecm-sql-prod-fjmontello",
"fw-prod-fjmontello-01",
"hst-ecm-01-prod-fjmontello",
"hst-ecm-02-prod-demonstracao-01",
"hst-ecm-02-prod-fjmontello",
"hw-ipmi-HP-fjmontello-VIRT-01",
"hw-ipmi-HP-fjmontello-VIRT-02",
"hw-ipmi-IBM-fjmontello-N1",
"hw-ipmi-IBM-fjmontello-N2",
"mail-prod-fjmontello-01",
"n1-prod-cluster-fjmontello-01",
"n1-prod-cluster-fjmontello-02",
"rot-prod-fjmontello-01",
"storage-prod-fjmontello-01A",
"storage-prod-fjmontello-01B",
"storage-prod-fjmontello-02A",
"storage-prod-fjmontello-02B",
"sw-prod-fjmontello-01",
"sw-prod-fjmontello-02",
"sw-prod-fjmontello-03",
"sw-prod-fjmontello-04",
"tsensor-fjmontello-01",
"web-prod-fjmontello-01",]
$hosts.each |$index| {
  exec { $index:
    path => "/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games",
    command => "/usr/local/centreon/www/modules/centreon-clapi/core/centreon -u alvin -p abc@123 -o HOST -a addhostgroup -v '$index;FJM-CONTRATADO'" ;
  }
 }
