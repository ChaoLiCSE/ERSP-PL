import re
import os
import json

def error_by_problem(infile, dic):
    print(infile)

    student = i.split('.')[0]
    hw_num = i.split('.')[1]

    with open(infile) as inf:

        for line in inf:

            item = eval(line)

            # skip events that are not eval events
            if item['event']['type'] != 'eval':
                continue

            if hw_num == 'hw1':
                label = find_label(problems_hw1, item)
                classify_error(item, label, dic)

            elif hw_num == 'hw2':
                label = find_label(problems_hw2, item)
                classify_error(item, label, dic)

            elif hw_num == 'hw3':
                label = find_label(problems_hw3, item)
                classify_error(item, label, dic)

            else:
                print('error identifing which homework')

        inf.close()

def find_label(problem_set, event):
    for i in problem_set:
        for j in event['ocaml']:
            if i in str.split(j['in']):
                return i
    return '???'

def classify_error(event, prob, dictionary):
    for i in event['ocaml']:
        if not i['out']:
            dictionary[prob]['success'] += 1

        elif re.search('Syntax error',i['out'], re.IGNORECASE) is not None:
            dictionary[prob]['syntax'] += 1

        else:
            dictionary[prob]['type'] += 1

############################################################################################################# Main
dir = os.path.abspath(__file__ + '/../../')

target = os.path.join(dir, 'sp14')
write_to = os.path.join(dir, 'summary.txt')

index = 0

problems_hw1 = ['???','palindrome', 'listReverse', 'digitalRoot', 'additivePersistence', 'digitsOfInt', 'sumList']
problems_hw2 = ['???','build', 'eval', 'exprToString', 'expr', 'fixpoint', 'wwhile', 'removeDuplicates', 'assoc']
problems_hw3 = ['???', 'bigMul', 'mulByDigit', 'bigAdd', 'removeZero', 'padZero', 'clone', 'stringOfList', 'sepConcat', 'pipe', 'sqsum']
"""
summary = {'hw1': dict(), 'hw2': dict(), 'hw3': dict()}

for i in os.listdir(target):
    student = i.split('.')[0]
    hw_num = i.split('.')[1]

    if hw_num == 'hw1':
        summary[hw_num][student] = {key: {'syntax': 0, 'type': 0, 'success': 0} for key in problems_hw1}
    elif hw_num == 'hw2':
        summary[hw_num][student] = {key: {'syntax': 0, 'type': 0, 'success': 0} for key in problems_hw2}
    elif hw_num == 'hw3':
        summary[hw_num][student] = {key: {'syntax': 0, 'type': 0, 'success': 0} for key in problems_hw3}

for i in os.listdir(target):
    student = i.split('.')[0]
    hw_num = i.split('.')[1]

    if student == 'heqin':
        continue

    error_by_problem(os.path.join(target, i), summary[hw_num][student])

with open(write_to, 'w') as of:
    json.dump(summary, of)
    of.close()
"""


with open(write_to) as input_file:
    summary = json.load(input_file)

#for i in problems_hw3:
#    print(i)

for i in problems_hw3:
    print(sum(value[i]['syntax'] for key, value in summary['hw3'].items()))
