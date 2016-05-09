import os
import json

dir = os.path.abspath(__file__ + '/../')
target = os.path.join(dir, 'sample.json')
output = os.path.join(dir, 'sample.txt')

inf = open(target, 'r')
of = open(output, 'w')

lines = inf.readlines()

for i in range(len(lines)):
  item = eval(lines[i])


  of.write('fix:')
  of.write('\n')
  of.write(item['fix'])
  of.write('\n')
  of.write('\n')

  of.write('bad: ')
  of.write('\n')
  of.write(item['bad'])
  of.write('\n')
  of.write('\n')

  of.write('annotated: ')
  of.write('\n')
  of.write(item['annotated'])
  of.write('\n')
  of.write('\n')

  of.write('annotated_fix:')
  of.write('\n')
  of.write(item['annotated_fix'])
  of.write('\n')
  of.write('\n')

  of.write('************** PROGRAM #')
  of.write(str(i+1))
  of.write(' ENDS HERE **************')

  of.write('\n')