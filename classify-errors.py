import re
import os
import json

"""
1. loop through all files from sp14
2. build dict, key is student name: {'name':{'hw1':[syntax, type]}, 'hw2':[syntax, type], 'hw3':[syntax, type]}}
3. for each file, count the number of errors and fill in corresponding entry
"""

dir = os.path.abspath(__file__ + '/../../')
target = os.path.join(dir, 'sp14')
output = os.path.join(dir, 'output')

summary = dict()

for i in os.listdir(target):

    filename = str.split(i, '.')

    student = filename[0]
    hw = filename[1]
    #print(student, hw)

    if student not in summary:
        summary[student] = dict()

    with open(os.path.join(target, i), encoding='utf-8') as inf:
        syntax_error = 0
        type_error = 0
        success = 0

        for line in inf:
            item = eval(line)
            
            if item['event']['type'] == 'eval':
                for i in item['ocaml']:
                    if not i['out']:
                        success += 1
                        continue
                    elif re.search('Syntax error',i['out'], re.IGNORECASE) is not None:
                        syntax_error += 1
                        break
                    else:
                        type_error += 1
                        break
        summary[student][hw] = [syntax_error, type_error, success]
        inf.close()

#print(summary)
with open(output, 'a') as of:
    json.dump(summary, of)
    of.close()
"""
with open(output) as inf:
    for line in inf:
        summary = eval(line)

for key, value in sorted(summary.items()):
    print(key)

for key, value in sorted(summary.items()):
    print(value['hw3'][1])
"""
print(summary)