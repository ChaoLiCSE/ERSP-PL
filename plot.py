import os
import json

#import numpy as np
#import matplotlib.pyplot as plt

def build_dict(infile, problems):
    student = dict()
    with open(infile) as inf:
        for line in inf:
            item = eval(line)
            current = item['time']

            if item['tag'] == 0: 
                continue

            problemID = problems[item['tag']]

            if problemID not in student:
                student[problemID] = {'duration': 0, 'lastcheck': current}

            if item['time'] - student[problemID]['lastcheck'] <= 62:
                student[problemID]['duration'] += current - student[problemID]['lastcheck']

            student[problemID]['lastcheck'] = current

    return student

################################################################################################### Main

dir = os.path.dirname('__file__')
infile = os.path.join(dir, 'homework1-withtag')

# homework 1 problems
problems = ['???','palindrome', 'listReverse', 'digitalRoot', 'additivePersistence', 'digits', 'digitsOfInt', 'sumList']

hw1 = list()
for i in os.listdir(infile):
    hw1.append(build_dict(os.path.join(infile,i), problems))

#print hw1

"""
summary = dict()
for i in problems:
    if i == '???': continue
    summary[i] = sum(item[i]['duration'] for item in hw1 if item.has_key(i))
print summary
"""

summary = dict()
for i in problems:
    if i == '???': continue
    summary[i] = [int(item[i]['duration'])/60 for item in hw1 if item.has_key(i)]

#print summary
#print max([max(summary[i]) for i in summary])

#for i in summary['palindrome']:
    #print(i)

for c in range(1, 800):
    print sum(i < c for i in summary['palindrome'])
    c += 30