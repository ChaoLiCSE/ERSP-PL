import re
import subprocess
import os
from difflib import SequenceMatcher

def get_pos(prog):
    error_output = subprocess.run(["ocaml"], input = prog, 
                   stdout=subprocess.PIPE,universal_newlines = True)

    if "rror" in error_output.stdout:
    	m = re.search('(?<=Characters )([1-9][0-9][0-9]|[1-9][0-9]|[0-9])', error_output.stdout)
    	n = re.search('(?<=-)([1-9][0-9][0-9]|[1-9][0-9]|[0-9])', error_output.stdout)
    
    '''
    print(m.group(0))
    print(n.group(0))
    '''
    return[int(m.group(0)),int(n.group(0))]


def err_judge(bad, fix, pos):
    
    '''
    print (bad)
    print (fix)
    print (pos)
    '''

	#get the key word to judge whether it is changed
    to_judge = bad[pos[0]: pos[1]]

	#first find out what are the different place in bad and fix
    s = SequenceMatcher(lambda x: x==" ", bad, fix)
    
    for tag, i1, i2, j1, j2 in s.get_opcodes():
        '''
    	print ("%7s a[%d:%d] (%s) b[%d:%d] (%s)" % 
    		(tag, i1, i2, bad[i1:i2], j1, j2, fix[j1:j2]))
        '''
         
        #the code at that position has been changed
        if tag in ['replace' , 'delete'] and (i1 <= pos[0] or i2 >= pos[1]):
    		#print("correct location")
            return 1

    	#the code at that position has not been changed
        if tag in ['equal'] and (i1 <= pos[0] and i2 >= pos[1]):
            #print ("incorrect location")
            return 0

    print ("cannot decide")
    return -1


dir = os.path.abspath(__file__ + '/../../')
target = os.path.join(dir, 'annotated_6507.json')
target2 = os.path.join(dir, 'problems.txt')
'''
prog = "let rec digitsOfInt n = match n with | ( n mod 10 ) + digitsOfInt ( (failwith "") 10 );;"
for i in get_pos (prog):
    print (i)
'''
total = 0
prev_corr = 0
anno_corr = 0
counter1 = 0

both_correct = 0
both_wrong = 0
only_anno_corr = 0
only_pre_corr = 0

with open (os.path.join(target), 'r') as myfile, open (os.path.join(target2), 'w') as out:
    for line in myfile:
      
      #just test
      '''
      if counter1 > 100:
        break
      counter1= counter1+1
      '''

      item = eval(line)
      #for i in range(len(item["bad"])):
      #print(item["bad"])

      pos = get_pos(item["bad"])
      retVal = err_judge(item["bad"],item["fix"],pos)
        

      if(retVal == -1):
          print('cannot judge at 1')
          out.write('error at: ')
          out.write(item[bad])
          continue

      total = total+1
      if(retVal == 1):
          prev_corr = prev_corr + 1
      
      #deal with annotated
      pos = get_pos(item["annotated"])
      retVal_a = err_judge(item["annotated"], item["annotated_fix"], pos)

      #check strange errors
      if(retVal == -1):
          print('cannot judge at 2')
          out.write('error at: ')
          out.write(item[annotated])
          continue

      if(retVal_a == 1):
          anno_corr = anno_corr+1
      
      #put the output to different categories
      if(retVal_a == 1 and retVal == 1):
            both_correct = both_correct +1
      elif(retVal_a == 1 and retVal == 0):
            only_anno_corr = only_anno_corr + 1
            print('anno correct')
            out.write('only_anno_corr')
            out.write(line)
            out.write('\n')
      elif(retVal_a == 0 and retVal == 1):
            only_pre_corr = only_pre_corr + 1
            print('pre correct')
            out.write('only_pre_corr')
            out.write(line)
            out.write('\n')
      else:
            both_wrong = both_wrong +1

myfile.close() 
s = 'in the total of ' + str(total) + ' programs, both correct is: ' + str(both_correct) + 'only annotated correct is: ' + str(only_anno_corr) + 'only pre correct is: ' + str(only_pre_corr) + 'both wrong is: '+str(both_wrong)

print (s)
