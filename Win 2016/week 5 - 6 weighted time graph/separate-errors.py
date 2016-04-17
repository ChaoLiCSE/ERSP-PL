import re
import os
import json

"""
1. loop through all files from sp14
2. build dict, key is student name: {'name':{'hw1':[syntax, type]}, 'hw2':[syntax, type], 'hw3':[syntax, type]}}
3. for each file, count the number of errors and fill in corresponding entry
"""

dir = os.path.abspath(__file__ + '/../')
target = os.path.join(dir, 'sp14-hw')
output = os.path.join(dir, 'output_syntax')
output2 = os.path.join(dir, 'output_type')

problems_hw1 = ['???','palindrome', 'listReverse', 'digitalRoot', 'additivePersistence', 'digitsOfInt', 'sumList']
problems_hw2 = ['???','build', 'eval', 'exprToString', 'expr', 'fixpoint', 'wwhile', 'removeDuplicates', 'assoc']
problems_hw3 = ['???', 'bigMul', 'mulByDigit', 'bigAdd', 'removeZero', 'padZero', 'clone', 'stringOfList', 'sepConcat', 'pipe', 'sqsum']

def find_label(problem_set, event):
    for i in problem_set:
        for j in event['ocaml']:
            if i in str.split(j['in']):
                return i
    for j in event['ocaml']:
        print(j['in'])
    return '???'


for i in os.listdir(target):

    if i == '.DS_Store':
        continue

    filename = str.split(i, '.')

    student = filename[0]
    hw_num = filename[1]
    #print(student, hw)
    print(i)



    with open(os.path.join(target, i)) as inf, open(output, 'a') as of1, open(output2, 'a') as of2:

        for line in inf:
            item = eval(line)

            if item['event']['type'] == 'eval':

                if hw_num == 'hw1':
                    label = find_label(problems_hw1, item)

                elif hw_num == 'hw2':
                    label = find_label(problems_hw2, item)

                elif hw_num == 'hw3':
                    label = find_label(problems_hw3, item)

                else:
                    label = 'I dont know'
            
            if item['event']['type'] == 'eval':

                for i in item['ocaml']:
                    if not i['out']:
                        continue
                    elif re.search('Syntax error',i['out'], re.IGNORECASE) is not None:
                        of1.write(label)
                        of1.write('\n')
                        of1.write(i['in'])
                        of1.write('\n')
                        of1.write(i['out'])
                        of1.write('\n')
                        break
                    else:
                        of2.write(label)
                        of2.write('\n')
                        of2.write(i['in'])
                        of2.write('\n')
                        of2.write(i['out'])
                        of2.write('\n')

                        break
        inf.close()
        of1.close()
       

"""
with open(output) as inf:
    for line in inf:
        summary = eval(line)
for key, value in sorted(summary.items()):
    print(key)
for key, value in sorted(summary.items()):
    print(value['hw3'][1])
"""
