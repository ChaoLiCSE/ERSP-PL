import os
import json

dir = os.path.abspath(__file__ + '/../')
target = os.path.join(dir, 'annotated_6507.json')
output = os.path.join(dir, 'annotated_6507.txt')

with open(target) as inf, open(output, 'w') as of:
  for line in inf:
    item = eval(line)

    of.write('fix:')
    of.write('\n')
    of.write(item['fix'])
    of.write('\n')
    of.write('\n')

    of.write('bad:')
    of.write('\n')
    of.write(item['bad'])
    of.write('\n')
    of.write('\n')

    of.write('annotated:')
    of.write('\n')
    of.write(item['annotated'])
    of.write('\n')
    of.write('\n')

    of.write('annotated_fix:')
    of.write('\n')
    of.write(item['annotated_fix'])
    of.write('\n')
    of.write('\n')

    of.write('\n')

  inf.close()
  of.close()