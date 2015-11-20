import re
import os
import json
from os.path import basename
from os.path import splitext

dir = os.path.dirname('__file__')

target = os.path.join(dir, 'logs-detail')
output = os.path.join(dir, 'withtag')

problems = ['palindrome', 'listReverse', 'digitalRoot', 'additivePersistence', 'digits', 'digitsOfInt', 'sumList']

def parse(infile, outfile):
  hw = dict()
  with open(infile) as inf, open(outfile,'a') as of:
    for line in inf:
      item = eval(line)
      # only look at 'eval' events
      if item['event']['type'] != 'eval':
        continue
      for i in problems:
        for code in item['ocaml']:
            if i in str.split(code['in']):
                item['tag'] = i
      json.dump(item, of)
      of.write('\n')
  inf.close()
  of.close()

#infile = os.path.join(target, 'alperez.json')
#outfile = os.path.join(directory, 'test')
#parse(infile, outfile)

for i in os.listdir(target):
  if not os.path.exists(output):
    os.makedirs(output)
  print(i)
  # skip anything that is not hw1
  homework = re.search('hw1',i) 
  if homework is None:
    print('skip')
    continue
  infile = os.path.join(target, i)
  outfile = os.path.join(output, i)
  parse(infile, outfile)