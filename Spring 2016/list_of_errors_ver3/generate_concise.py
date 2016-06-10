#This is a program which generate a concise version of all the data sets

import re
import os
import json

"""
1. ignore all events that is not an 'eval' event
2. if there are multiple 'in' fields in one event, only record the first compiled program and all the bad programs
3. ignore all method calls, such as "let _ ="
"""

dir = os.path.abspath(__file__ + '/../')
target = os.path.join(dir, '../../../sp14 (1)')
output3 = os.path.join(dir, 'sp14-concise')

problems_hw1 = ['???','palindrome', 'listReverse', 'digitalRoot', 'additivePersistence', 'digitsOfInt', 'sumList']
problems_hw2 = ['???','build', 'eval', 'exprToString', 'expr', 'fixpoint', 'wwhile', 'removeDuplicates', 'assoc']
problems_hw3 = ['???', 'bigMul', 'mulByDigit', 'bigAdd', 'removeZero', 'padZero', 'clone', 'stringOfList', 'sepConcat', 'pipe', 'sqsum']

#find which homework function they are working on
def find_label(hw_num, event):
  if hw_num == 'hw1':
    problem_set = problems_hw1

  elif hw_num == 'hw2':
    problem_set = problems_hw2

  elif hw_num == 'hw3':
    problem_set = problems_hw3

  label = ''
  for i in problem_set:
    if i in event['in']:
      label = i
  if not label:
    label = '???'

  return label


#####################MAIN######################################
for i in os.listdir(target):
    filename = str.split(i, '.')
    hw_num = filename[1]
    print(i)

    if i == 'heqin.hw2.ml.json':
        continue

    nfile = os.path.join(output3, i)
    
    with open(os.path.join(target, i), 'r') as inf, open(nfile, 'w') as of:

      for line in inf:
        item = eval(line)

        if item['event']['type'] != 'eval':
          continue

        ocaml_l = list()

        first_compiled_or_error = True
        for i in item['ocaml']:
          if 'Syntax error' in i['out']:
            continue

          label = find_label(hw_num, i)
          if label == '???':
            #print(i['in'])
            continue

          if first_compiled_or_error and not i['in'].startswith('let _'):
            ocaml_l.append(i)

          if not i['out']:
            first_compiled_or_error = False

        if not ocaml_l:
          continue

        summary = dict()
        summary['ocaml'] = ocaml_l
        summary['event'] = item['event']['type']

        #print(summary)

        json.dump(summary, of)
        of.write('\n')

      inf.close()
      of.close()