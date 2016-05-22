import re
import os
import json
import type_annotate

"""
updates from list_of_errors:
1. use 'min' field as well as 'in'
2. fix wierd pairing
3. create timeline for each problem

NOTE: used 'in' for fix but 'min' for bad!!
"""

dir = os.path.abspath(__file__ + '/../')
target = os.path.join(dir, 'sp14-concise')
#target = os.path.join(dir, 'check-concise')

output = os.path.join(dir, 'prob_set')
output3 = os.path.join(dir, 'list_of_errors_ver3.json')
#output3 = os.path.join(dir, 'check.json')

problems_hw1 = ['palindrome', 'listReverse', 'digitalRoot', 'additivePersistence', 'digitsOfInt', 'sumList','???']
problems_hw2 = ['build', 'eval', 'exprToString', 'expr', 'fixpoint', 'wwhile', 'removeDuplicates', 'assoc','???']
problems_hw3 = ['bigMul', 'mulByDigit', 'bigAdd', 'removeZero', 'padZero', 'clone', 'stringOfList', 'sepConcat', 'pipe', 'sqsum','???']

def find_problem_set(hw_num):
  problem_set = list()

  if hw_num == 'hw1':
    problem_set = problems_hw1

  elif hw_num == 'hw2':
    problem_set = problems_hw2

  elif hw_num == 'hw3':
    problem_set = problems_hw3

  return problem_set

def find_all_prob(problem, lines):
  prob_list = list()

  for line in lines:
    item = eval(line)
    for j in item['ocaml']:
      if problem in j['in']:
        prob_list.append(item)
        break
      else:
        continue

      prob_list.append('???')
      break

  return prob_list

def build_dict(hw_num, problem):
  new_dict = dict()
  new_dict['hw'] = hw_num
  new_dict['problem'] = problem
  new_dict['bad'] = []
  new_dict['fix'] = []
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

  #print(i)

  with open(os.path.join(target, i)) as inf:

    lines = inf.readlines()
    print(student)

    problem_set = find_problem_set(hw_num)

    for label in problem_set:

      #if student != 'awfong': continue
      summary = build_dict(hw_num, label)
      events = find_all_prob(label, lines)
      #print(len(events))
      
      index = 0

      # find the first bad program
      while index < len(events) and not events[index]['ocaml'][0]['out']:
        index += 1
        continue

      # find all trailing bad programs until a fix
      while index < len(events):

        print(student, hw_num, label, index)
        #print(summary['bad'])
        '''
        if(student == 'alperez' and label == 'wwhile' and index == '9'):
          index+=1
          continue
        '''

        #print(student == 'awfong' and label == 'fixpoint' and index == 2)
        if(student == 'awfong' and label == 'fixpoint' and index == 2):
          print("here")
          of = open(output, 'a')
          #print(lines)
          of.write(str(lines))
          of.close
          index+=1
          continue

        if label == '???':
          print('?????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????')
          print(events[index])
          print(summary)
        
        # bad programs
        if (events[index]['ocaml'][0]['out'] != ""):
          summary['bad'].append(events[index]['ocaml'][0]['min'])
          count_bads += 1
          index += 1
          print('bad')
          continue
        
        # true fix, write to file
        elif (summary['bad'] != []) and (type_annotate.annotate_and_compile(events[index], label, hw_num) == ""):
          print(type_annotate.annotate_and_compile(events[index], label, hw_num))
          summary['fix'].append(events[index]['ocaml'][0]['min'])
          print('fix')          
          index += 1

          # write to file, ignore empty dicts
          json.dump(summary, of3)
          of3.write('\n')
          count_groups += 1

        # skip false fix
        else:
          #print(events[index])
          summary['bad'].append(events[index]['ocaml'][0]['min'])
          print('skip')
          index += 1

          continue

        # reach end of the list but finds no fix
        if index >= len(events) and summary['bad'] and not summary['fix']:
          summary['fix'].append('')
          count_no_fix += 1
          #print('no fix')

          # write to file
          json.dump(summary, of3)
          of3.write('\n')
          count_groups += 1

        # list is not end, continue
        summary = build_dict(hw_num, label)

    inf.close()

of3.close()
print(count_bads)
print(count_no_fix)
print(count_groups)