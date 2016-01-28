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
output1 = os.path.join(dir, 'output-type')
output2 = os.path.join(dir, 'output-syntax')

summary = dict()

#print(summary)
if not os.path.exists(output1):
    os.makedirs(output1)


if not os.path.exists(output2):
    os.makedirs(output2)
    

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

        with open(output1, 'a') as of1:
            with open(output2, 'a') as of2:

                for line in inf:
                    item = eval(line)
                    
                    if item['event']['type'] == 'eval':
                        for i in item['ocaml']:
                            if not i['out']:
                                success += 1
                                continue
                            elif re.search('Syntax error',i['out'], re.IGNORECASE) is not None:
                                syntax_error += 1
                                json.dump(item, of1)
                                break
                            else:
                                json.dump(item, of2)
                                type_error += 1
                                break
        summary[student][hw] = [syntax_error, type_error, success]
        inf.close()

of1.close()
of2.close()
       

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
