import os
import json
import min_interval
import random

def runOnRandomPrograms(fun, directory,num, prog_num):
  j=0
  while(j<num):
    i = random.choice(os.listdir(directory))
    #print (i)
    #print("num is")
    #print(j)

    if not i.lower().endswith( '.ml'):
      continue

    #print("prog is")
    #print(i)
    j=j+1

    print("dealing with the " + str(i)+" program in the directory")
    yield fun(directory, i)



def runOnAllPrograms(fun, directory):
  for i in os.listdir(directory):
    if not i.lower().endswith('.ml'):
      continue

    print("dealing with the " + str(i)+" program in the directory")
    yield fun(directory, i)

######################################################## Main
dir = os.path.abspath(__file__ + '/../../')
target = os.path.join(dir, 'unify_syntax')
target2 = os.path.join(__file__ + '/../../../yunounderstand/data/sp14/prog/unify')
summary = os.path.join(target, 'dictionary.json')
pretty_print = os.path.join(target, 'summary.txt')
index = 0

#result = runOnRandomPrograms(min_interval.find_min_interval, target2, 1,4874)
result = runOnAllPrograms(min_interval.find_min_interval, target2)

with open(summary, 'w') as of:
  for i in result:
    #print("this is i")
    #print (i)
    json.dump(i, of)
    of.write('\n')
  of.close()

with open(summary, 'r') as inf, open(pretty_print, 'w') as of2:
  

  for line in inf:
    item = eval(line)

    of2.write('file no.: ' + str(index) + '\n')
    of2.write('original code: \n' + item['in'] + ' \n')
    of2.write('fixed code: \n' + str(item['fixed']) + ' \n')
    of2.write('span size: \n' + str(item['span-size']) + ' \n')
    of2.write('span fraction: \n' + str(item['span-fraction']) + ' \n')

    of2.write('\n')

  of2.close()
