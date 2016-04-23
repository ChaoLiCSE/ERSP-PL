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
    
    print(m.group(0))
    print(n.group(0))
    return[int(m.group(0)),int(n.group(0))]


def err_judge(bad, fix, pos):
	
    print (bad)
    print (fix)
    print (pos)


	#get the key word to judge whether it is changed
    to_judge = bad[pos[0]: pos[1]]

	#first find out what are the different place in bad and fix
    s = SequenceMatcher(lambda x: x==" ", bad, fix)
    
    for tag, i1, i2, j1, j2 in s.get_opcodes():

    	print ("%7s a[%d:%d] (%s) b[%d:%d] (%s)" % 
    		(tag, i1, i2, bad[i1:i2], j1, j2, fix[j1:j2]))

    	#the code at that position has been changed
    	if tag in ['replace' , 'delete'] and (i1 <= pos[0] or i2 >= pos[1]):
    		print("correct location")
    		return 1

    	#the code at that position has not been changed
    	if tag in ['equal'] and (i1 <= pos[0] and i2 >= pos[1]):
            print ("incorrect location")
            return 0

    print ("cannot decide")
    return -1


dir = os.path.abspath(__file__ + '/../../')
target = os.path.join(dir, 'list_of_errors.json')
target2 = os.path.join(dir, 'problems.txt')
'''
prog = "let rec digitsOfInt n = match n with | ( n mod 10 ) + digitsOfInt ( (failwith "") 10 );;"
for i in get_pos (prog):
    print (i)
'''
total = 0
prev_corr = 0
add_corr = 0
counter1 = 0

with open (os.path.join(target), 'r') as myfile:
    for line in myfile:
      
      #just test
      if counter1 > 100:
        break
      counter1= counter1+1

      item = eval(line)
      for i in range(len(item["bad"])):
        print(type(item["bad"][i]))
        pos = get_pos(item["bad"][i])
        
        retVal = err_judge(item["bad"][i],item["fix"][0],pos)
        
        total = total+1
        if(retVal == 1):
           prev_corr = prev_corr + 1       

myfile.close() 
s = 'in the total of ' + str(total) + ' prev_corr is: ' + str(prev_corr)
print (s)
