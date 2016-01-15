import re
import os
import json
from shutil import copy

# find all student files for a homework, and copy the files into a new dir
def findhw(targets, outputs):
    if not os.path.exists(outputs):
      os.makedirs(outputs)

    for i in os.listdir(targets):
      print(i)

      # skip anything that is not hw1
      homework = re.search('hw1',i) 
      if homework is None:
        continue

      # copy the file to new dir
      path = os.path.join(targets, i)
      copy(path, outputs)

# group all the events that completed in a session by adding a group number to the events
def group_sessions(infile,  problems):
    session_numbers = []
    with open(infile, 'r+') as inf:
      num = 0
      lastcheck = 0
      for line in inf:
        item = eval(line)
        tag = 0
        done = False
        if item['time'] - lastcheck > 62:
            num += 1
            lastcheck = item['time']
        if item['event']['type'] == 'eval':
            for i in problems:
                for j in item['ocaml']:
                    if i in str.split(j['in']):
                        tag = problems.index(i)
                        done = True
                        break
                if done: break
        session_numbers.append([item['event']['type'], num, tag])
    return session_numbers

# for each infile, writes the following foramt to the outfile:
# {'tag': #, 'time': #}
# where 'tag' is the index of the problem in list problems,
# and 'time' is the unix time stamp
def label_problems(infile, outfile, problems, groups):
    index = 0
    with open(infile) as inf, open(outfile,'a') as of:
        for line in inf:
            item = eval(line)
            toStore = dict()
            toStore['time'] = item['time']

            if item['event']['type'] == 'eval' and groups[index][2] != 0:
                toStore['tag'] = groups[index][2]
            else:
                flag = False
                for i in range(index, len(groups)):
                    if groups[i][0] == 'eval'and groups[i][2] != 0:
                        toStore['tag'] = groups[i][2]
                        flag = True
                        break
                if flag == False: toStore['tag'] = 0

            json.dump(toStore, of)
            of.write('\n')
            index += 1
    inf.close()
    of.close()


############################################################################################################# Main
dir = os.path.abspath(__file__ + '/../../')

target = os.path.join(dir, 'sp14')
output = os.path.join(dir, 'homework1')
output2 = os.path.join(dir, 'homework1-withtag')

# homework 1 problems
problems = ['???','palindrome', 'listReverse', 'digitalRoot', 'additivePersistence', 'digitsOfInt', 'sumList']

findhw(target, output)

if not os.path.exists(output2):
    os.makedirs(output2)

hw1 = list()
for i in os.listdir(output):
    session_numbers = group_sessions(os.path.join(target,i), problems)
    label_problems(os.path.join(target,i), os.path.join(output2,i), problems, session_numbers)
