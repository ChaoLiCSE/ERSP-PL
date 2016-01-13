import re
import os
import json
from os.path import basename
from os.path import splitext

dir = os.path.dirname('__file__')
target = os.path.join(dir, 'time')

with open(target) as f:
  time = 0
  counter = 0
  for line in f:
  	item = eval(line)
  	if item.has_key('hw3.ml'):
  	  time += item['hw3.ml']
  	  counter += 1
  print time/counter*1.0