#!/usr/bin/env python

import yaml

with open("input.yml", 'r') as stream:
    try:
        origcfg = yaml.load(stream)
    except yaml.YAMLError as exc:
        print(exc)

for vserver,values  in origcfg.iteritems():
  print vserver
  #get real servers
  for r in values['rs']:
    print values['rs'][r]

