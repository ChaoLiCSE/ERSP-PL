
import re
import os
import json
import pyparsing


dir = os.path.abspath(__file__ + '/../')
target = os.path.join(dir, 'sp14-hw')
output_folder = os.path.join(dir, 'unify_syntax')

if not os.path.exists(output_folder):
    os.makedirs(output_folder)

j = 1
four_digit = '{:04d}'.format(j)

for i in os.listdir(target):

    if i == '.DS_Store':
        continue

    #filename = str.split(i, '.')

    #student = filename[0]
    #hw_num = filename[1]
    #print(student, hw)
    #print(i)

    #j += 1


    with open(os.path.join(target, i)) as inf:

        for line in inf:
            item = eval(line)
            
            if item['event']['type'] == 'eval':

                for i in item['ocaml']:
                    if not i['out']:
                        continue
                    elif re.search('Syntax error',i['out'], re.IGNORECASE) is not None:

                        output = os.path.join(output_folder, 'prog%s.ml' % four_digit) 
                        output2 = os.path.join(output_folder,'prog%s.ml.out' % four_digit) 

                        with open(output, 'a') as of1, open(output2, 'a') as of2:                            

                            #input code
                            code = pyparsing.nestedExpr("(*", "*)").suppress()
                            of1.write(code.transformString(i['in']))
                            
                            #output error message
                            of2.write(i['out'])
                            j += 1
                            four_digit = '{:04d}'.format(j)

                            break
        inf.close()
        of1.close()
        of2.close()




       

