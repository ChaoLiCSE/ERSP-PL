import os
import json

dir = os.path.abspath(__file__ + '/../')
target = os.path.join(dir, 'summary0001-1000.json')

def analysis(attribute, infile):
  res = []
  with open(infile) as inf:
    for line in inf:
      item = eval(line)
      res.append(item[attribute])
    inf.close()

  return res

#################################################### Main

spansize = analysis('span-fraction', target)
for i in spansize:
  print(int(i * 100))