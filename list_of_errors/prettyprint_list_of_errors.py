import re
import os
import json

"""
1. loop through all files from sp14
2. build dict for each file {hw: #, problem: p, bad: [], fix: f}
3. flag_end to look for a 'fix': False for evals, True for timer
"""

dir = os.path.abspath(__file__ + '/../../')
target = os.path.join(dir, 'list_of_errors.json')
output = os.path.join(dir, 'list_of_errors.txt')

with open(target) as inf, open(output, 'a') as of3:
    for line in inf:
        item = eval(line)

        of3.write(item['hw'])
        of3.write(' ')
        of3.write(item['problem'])
        of3.write('\n')
        of3.write('\n')

        of3.write('fix:')
        of3.write('\n')
        for i in item['fix']:
            of3.write(i)
            of3.write('\n')
            of3.write('\n')

        of3.write('bad:')
        of3.write('\n')
        for i in range(len(item['bad'])):
            of3.write(item['bad'][i])
            of3.write('\n')
            of3.write(item['message'][i])
            of3.write('\n')
            of3.write('\n')

        of3.write('\n')