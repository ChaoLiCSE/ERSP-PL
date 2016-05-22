import random
import os
import json
import type_annotate as ta

def sample_without_replacement(data, num):
  sample = list()
  i = 0
  nn = num
  nr = len(data)
  for row in data:
    k = random.random()
    if k < nn/nr:
      sample.append(data[i])
      nn = nn - 1
    nr = nr - 1
    i += 1

  return sample


### MAIN

dir = os.path.abspath(__file__ + '/../')
target = os.path.join(dir, 'list_of_errors_ver3.json')

#target = os.path.join(dir, 'check.json')
output = os.path.join(dir, 'sample.json')

random.seed(1)

inf = open(target, 'r')
of = open(output, 'w')
lines = inf.readlines()

data = list()

for i in lines:
  item = json.loads(i)
  print(item['problem'])
  # skip bad dictionaries
  if (item['problem'] == 'expr'):
    continue

  # find corresponding annotations
  annotation = ta.find_annotation(item)

  # if annotation is not successful for any reason, skip it
  if not annotation:
    print("CAUTION: skipping unsuccessful annotation")
    continue

  # build dict with bad programs, annotated programs, and fixed programs
  for bad in item['bad']:
    dic = ta.build_dict(bad, annotation, item)
    data.append(dic)

sample = sample_without_replacement(data, 6507)
for i in sample:
  json.dump(i, of)
  of.write('\n')