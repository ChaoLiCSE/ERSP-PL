import re
import os
import json

"""
1. loop through all files from sp14
2. build dict for each file {hw: #, problem: p, bad: [], fix: f}
3. flag_end to look for a 'fix': False for evals, True for timer
"""

dir = os.path.abspath(__file__ + '/../../')
target = os.path.join(dir, 'sp14')
output3 = os.path.join(dir, 'list_of_errors.json')

problems_hw1 = ['???','palindrome', 'listReverse', 'digitalRoot', 'additivePersistence', 'digitsOfInt', 'sumList']
problems_hw2 = ['???','build', 'eval', 'exprToString', 'expr', 'fixpoint', 'wwhile', 'removeDuplicates', 'assoc']
problems_hw3 = ['???', 'bigMul', 'mulByDigit', 'bigAdd', 'removeZero', 'padZero', 'clone', 'stringOfList', 'sepConcat', 'pipe', 'sqsum']

def find_label(problem_set, event):
    for i in problem_set:
        for j in event['ocaml']:
            if i in j['in']:
                return i
    return '???'

for i in os.listdir(target):

    filename = str.split(i, '.')

    student = filename[0]
    hw_num = filename[1]

    print(i)
    if i == 'heqin.hw2.ml.json' or i == 'ksl012.hw2.ml.json':
        continue

    with open(os.path.join(target, i)) as inf, open(output3, 'a') as of3:

        flag_end = False
        lines = inf.readlines()
        index = 0


        while index < len(lines):

            item = eval(lines[index])

            # ignore timer and other events
            if item['event']['type'] != 'eval':
                index = index + 1
                continue

            # ignore successful builds that are not fix
            if flag_end == True:
                cont = False
                for i in item['ocaml']:
                    if not i['out']:
                        cont = True
                if cont == True:
                    index = index + 1
                    continue

            # which hw it is?
            if hw_num == 'hw1':
                label = find_label(problems_hw1, item)

            elif hw_num == 'hw2':
                label = find_label(problems_hw2, item)

            elif hw_num == 'hw3':
                label = find_label(problems_hw3, item)

            summary = dict()
            summary['hw'] = hw_num
            summary['problem'] = label
            summary['bad'] = []
            summary['fix'] = []

            flag_end = False

            while (flag_end == False and index < len(lines)): 

                item = eval(lines[index])

                # ignore not timer and other events
                if item['event']['type'] != 'eval':
                    index = index + 1
                    continue

                # ignore not timer and other events
                if item['event']['type'] != 'eval':
                    index = index + 1
                    flag_end = True
                    continue

                # which hw it is?
                if hw_num == 'hw1':
                    new_label = find_label(problems_hw1, item)

                elif hw_num == 'hw2':
                    new_label = find_label(problems_hw2, item)

                elif hw_num == 'hw3':
                    new_label = find_label(problems_hw3, item)

                if new_label != label:
                    index = index - 1
                    break

                # hit 'fix' event
                hit = False
                for i in item['ocaml']:
                    if not i['out']:
                        hit = True

                if hit == True:
                    if summary['bad'] == []:
                        flag_end = True
                        break

                    for i in item['ocaml']:
                        summary['fix'].append(i['in'])
                    
                    json.dump(summary, of3)
                    of3.write('\n')
                    flag_end = True
                    
                    break

                # normal error
                for i in item['ocaml']:
                    summary['bad'].append(i['in'])
                    """
                    if re.search('Syntax error', i['out'], re.IGNORECASE) is not None:
                        summary['bad'].append(i['out'])
                    
                    else:
                        summary['bad'].append(i['out'])
                    """
                index = index + 1

            index = index + 1

    inf.close()
    of3.close()
