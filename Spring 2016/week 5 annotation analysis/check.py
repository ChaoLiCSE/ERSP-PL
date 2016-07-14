#This is a debugging program to show the details of a pair of
#programs

import json
import os
import re
dir = os.path.abspath(__file__ + '/../../')
#target2 = os.path.join(dir, 'anno_not_false_not_rec.json')
#target3 = os.path.join(dir, 'anno_not_false_rec.json')
target = os.path.join(dir, 'problems.json')
target2 = os.path.join(dir, 'problems_lf_no_Failure.txt')
target3 = os.path.join(dir, 'wrong_usage.txt')

count = 0
counter = 0
with open (os.path.join(target), 'r') as myfile, open (os.path.join(target2), 'w') as nof, open (os.path.join(target3), 'w') as use:
    for line in myfile:
        
        if( not ("List.fold_left" in line)):
            count+=1
            continue

        elif("failwith" in line):
            count+=1
            continue

        else:
            
            item = eval(line)
            '''
            nof.write(str(count))
            nof.write('\n')

            nof.write('---------------------bad------------------------')
            nof.write(item["bad"])
            nof.write('--------------------fix-------------------------')

            nof.write(item["fix"])
            nof.write('-------------------anno bad--------------------------')

            nof.write(item["annotated"])
            nof.write('---------------------annofix------------------------')
            nof.write(item["annotated_fix"])

            nof.write('\n')
            title.write(item["prob"])
            title.write('\n')
            '''

            data=(item["bad"].replace('\n', ''))+" "+(item["fix"].replace('\n', ''))
            regex = "((List.fold_left )(\w+\s+){0,1}(\w+\s+){0,1}(\w+){0,1})"
            result = re.findall(regex, data)
            for i in range (0, len(result)):
                if (i == 0):
                    out = result[i]
                else:
                    if(out != result[i]):
                        print(result)

                        counter+=1
                        use.write(str(count))
                        use.write('\n')

                        use.write('---------------------bad------------------------')
                        use.write(item["bad"])
                        use.write('--------------------fix-------------------------')

                        use.write(item["fix"])
                        use.write('-------------------anno bad--------------------------')

                        use.write(item["annotated"])
                        use.write('---------------------anno fix------------------------')
                        use.write(item["annotated_fix"])

                        use.write('\n')



        count += 1

print (counter)
myfile.close()
nof.close()
use.close()
