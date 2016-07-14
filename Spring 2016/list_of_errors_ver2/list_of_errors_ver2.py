import re
import os
import json

"""
updates from list_of_errors:
1. use 'min' field as well as 'in'
2. fix wierd pairing

NOTE: used 'in' for fix but 'min' for bad!!
"""

dir = os.path.abspath(__file__ + '/../')
target = os.path.join(dir, 'sp14-concise')
output3 = os.path.join(dir, 'list_of_errors_ver2.json')

problems_hw1 = ['???','palindrome', 'listReverse', 'digitalRoot', 'additivePersistence', 'digitsOfInt', 'sumList']
problems_hw2 = ['???','build', 'eval', 'exprToString', 'expr', 'fixpoint', 'wwhile', 'removeDuplicates', 'assoc']
problems_hw3 = ['???', 'bigMul', 'mulByDigit', 'bigAdd', 'removeZero', 'padZero', 'clone', 'stringOfList', 'sepConcat', 'pipe', 'sqsum']

def find_label(hw_num, event):
  if hw_num == 'hw1':
    problem_set = problems_hw1

  elif hw_num == 'hw2':
    problem_set = problems_hw2

  elif hw_num == 'hw3':
    problem_set = problems_hw3

  for j in event['ocaml']:
    for i in problem_set:
      if i in j['in']:
        return i
  return '???'

def build_dict(hw_num):
  new_dict = dict()
  new_dict['hw'] = hw_num
  new_dict['problem'] = ''
  new_dict['bad'] = []
  new_dict['bad_in'] = []
  new_dict['fix'] = []
  new_dict['message'] = []
  return new_dict

### MAIN
of3 = open(output3, 'a')
count_bads = 0
count_groups = 0
count_no_fix = 0

for i in os.listdir(target):

  filename = str.split(i, '.')

  student = filename[0]
  hw_num = filename[1]

  print(i)

  with open(os.path.join(target, i)) as inf:

    lines = inf.readlines()
    index = 0

    while index < len(lines):

      summary = build_dict(hw_num)
      problem = ''

      # find the label of the first bad program
      while index < len(lines):
        item = eval(lines[index])

        if not item['ocaml'][0]['min']:
          index += 1
          continue

        problem = find_label(hw_num, item)
        summary['problem'] = problem
        summary['bad'].append(item['ocaml'][0]['min'])
        summary['bad_in'].append(item['ocaml'][0]['in'])
        summary['message'].append(item['ocaml'][0]['out'])
        count_bads += 1
        index += 1
        break

      # find all bad programs under the same label until we find hit a new label or find a fix
      while index < len(lines):
        item = eval(lines[index])

        # break if no fix is found
        if find_label(hw_num, item) != problem:
          count_no_fix += 1
          break

        # break if found a fix
        if not item['ocaml'][0]['min']:
          summary['fix'].append(item['ocaml'][0]['in'])
          index += 1
          break

        # append bad programs
        summary['bad'].append(item['ocaml'][0]['min'])
        summary['bad_in'].append(item['ocaml'][0]['in'])
        summary['message'].append(item['ocaml'][0]['out'])
        count_bads += 1
        index += 1

      # ignore empty dicts
      if summary['problem']:
        json.dump(summary, of3)
        of3.write('\n')
        count_groups += 1

    inf.close()

of3.close()
print(count_bads)
print(count_no_fix)
print(count_groups)