import re
import os
import json
from os.path import basename
from os.path import splitext

dir = os.path.dirname('__file__')

target = os.path.join(dir, 'logs')

def parse(infile, outfile):
  hw = dict()
  with open(infile) as inf, open(outfile,'a') as of:
    for line in inf:
      item = eval(line)
      filename = item['file']
      current = item['time']
      # ignore empty events
      if filename == 'New ml file' and item['body'] == "" and item['cursor'] == 0:
        continue
      # ignore eval events
      if item['event'] == {"type":"eval"}:
        continue
      # ignore non homework events
      if filename != 'hw1.ml' and filename !='hw2.ml' and filename !='hw3.ml':
        continue
      # add an event (new hw)
      if filename not in hw:
        hw[filename] = {'start': current, 'duration': 0, 'lastcheck': current}
      # record time
      elif current - hw[filename]['lastcheck'] < 31:
        hw[filename]['duration'] += current - hw[filename]['lastcheck']
        hw[filename]['lastcheck'] = current
      # skip break
      else:
        hw[filename]['lastcheck'] = current
    student = dict()
    student['name'] = splitext(basename(infile))[0]
    if hw.has_key('hw1.ml'):
      student['hw1.ml'] = hw['hw1.ml']['duration']
    if hw.has_key('hw2.ml'):
      student['hw2.ml'] = hw['hw2.ml']['duration']
    if hw.has_key('hw3.ml'):
      student['hw3.ml'] = hw['hw3.ml']['duration']
    json.dump(student, of)
    of.write('\n')
  inf.close()
  of.close()

#infile = os.path.join(target, 'alperez.json')
#outfile = os.path.join(directory, 'test')
#parse(infile, outfile)

for i in os.listdir(target):
  print i
  if i == 'tkua.json':
    continue
  infile = os.path.join(target, i)
  outfile = os.path.join(dir, 'time')
  parse(infile, outfile)