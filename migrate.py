#!/usr/bin/env python

import yaml
outcfg = []
with open("input.yml", 'r') as stream:
    try:
        origcfg = yaml.load(stream)
    except yaml.YAMLError as exc:
        print(exc)

for vserver,values  in origcfg.iteritems():
  thiscfg = []
  vip = values['vip']
  for port in values['ports']:
    newsg = 'add serviceGroup sg_%s-%s ANY -maxClient 0 -maxReq 0 -cip DISABLED -usip YES -useproxyport NO -cltTimeout 360 -svrTimeout 360 -CKA NO -TCPB YES -CMP NO' %(vserver,port)
    thiscfg.append(newsg)
    newvs = 'add lb vserver lb_%s-%s ANY %s %s -persistenceType NONE -m MAC -state DISABLED -connfailover STATELESS -cltTimeout 120' %(vserver,port,vip,port)
    thiscfg.append(newvs)
    lbsgbind = 'bind lb vserver lb_%s-%s sg_%s-%s' %(vserver,port,vserver,port)
    thiscfg.append(lbsgbind)
  for realserver in values['rs']:
    ip= values['rs'][realserver] 
    newrs = 'add server %s %s -state DISABLED' %(realserver,ip)
    thiscfg.insert(0,newrs)
  if 'bindings' in values.keys():
    for rs,binding in values['bindings'].iteritems():
      for port in binding:
        sgrsbind = 'bind serviceGroup sg_%s-%s %s %s -state DISABLED' %(vserver,port,rs,port)
        thiscfg.append(sgrsbind)
  else:
     for realserver in values['rs']:
       for port in values['ports']:
         sgrsbind = 'bind serviceGroup sg_%s-%s %s %s -state DISABLED' %(vserver,port,realserver,port)
         thiscfg.append(sgrsbind)
  disarp = 'set ns ip %s -arpResponse ALL_VSERVERS' %vip
  thiscfg.append(disarp)

  outcfg.append(thiscfg)

for vserver in outcfg:
  for l in vserver:
    print l
  print '-' *10


