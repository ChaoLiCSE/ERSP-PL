import os
import json
import min_interval

def runOnAllPrograms(fun, directory):
  for i in os.listdir(directory):
    if not i.lower().endswith('.ml'):
      continue

    yield fun(directory, i)

######################################################## Main
dir = os.path.abspath(__file__ + '/../../')
target = os.path.join(dir, 'unify_syntax')
summary = os.path.join(target, 'dictionary.json')
pretty_print = os.path.join(target, 'summary.txt')

result = runOnAllPrograms(min_interval.find_min_interval, target)
with open(summary, 'w') as of:
  for i in result:
    json.dump(i, of)
    of.write('\n')
  of.close()

with open(summary, 'r') as inf, open(pretty_print, 'w') as of2:
  index = 0

  for line in inf:
    item = eval(line)

    of2.write('file no.: ' + str(index) + '\n')

    of2.write('original code: \n' + item['in'] + ' \n')
    of2.write('fixed code: \n' + item['fixed'] + ' \n')
    of2.write('span size: \n' + str(item['span-size']) + ' \n')
    of2.write('span fraction: \n' + str(item['span-fraction']) + ' \n')

    of2.write('\n')

  of2.close()
