#This is a debugging program to show the details of a pair of
#programs

import json
import os
dir = os.path.abspath(__file__ + '/../../')
target = os.path.join(dir, 'pre.json')
target2 = os.path.join(dir, 'pre.txt')
count = 0
with open (os.path.join(target), 'r') as myfile, open (os.path.join(target2), 'w') as out:
    for line in myfile:
        
        item = eval(line)
        out.write(str(count))
        out.write('\n')

        out.write('---------------------bad------------------------')
        out.write(item["bad"])
        out.write('--------------------fix-------------------------')

        out.write(item["fix"])
        out.write('-------------------anno bad--------------------------')

        out.write(item["annotated"])
        out.write('---------------------annofix------------------------')
        out.write(item["annotated_fix"])

        out.write('\n')

        count += 1


myfile.close()
out.close()