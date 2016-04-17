# ###########################File Discription #####################################
#This is a method which read in the original files, and then generates two folders,
# one contains filtered homework, and the other contains an output file with dictionarys
# line by line. The later one contains all eval events with their error type, success, 
# syntax error or type error. And records every session's start time and end time. 
# For all session dicts its form is 
# {"start", "end", session}
# For all error dicts its form is
# {"time","session","problem","error"}
###############################Information##########################################
# modified from Yijun's code, and instructed by Yijun
# Author :Jiani Huang
# Date: Feb. 02, 2016
#####################################################################################


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

      # skip anything that is not hw3
      homework = re.search('hw3',i) 
      if homework is None:
        continue

      # copy the file to new dir
      path = os.path.join(targets, i)
      copy(path, outputs)

# group all the events that completed in a session by adding a group number to the events
def dump_events(infile, outputfile, problems):
    session_numbers = []
    num = 0
    lastcheck = 0
    
    with open(infile, 'r+', encoding="utf8") as inf, open(outputfile,'a') as of:

      for line in inf:
        item = eval(line)
        tag = 0
        done = False
        toStore = dict()

        #a new session starts
        if item['time'] - lastcheck > 62:

            #print(lastcheck)

            #record the last event in the session
            toStore['session'] = num

            #tag the end of a session as end timer event
            toStore['end'] = lastcheck
            toStore['start'] = item['time']
            toStore['type'] = "session"

            lastcheck = item['time']
            num = num + 1
            
            #store the last event of a session
            json.dump(toStore,of)
            of.write('\n')

            continue

        lastcheck = item['time']
        #record every eval session
        if item['event']['type'] == 'eval':
            for i in problems:
                for j in item['ocaml']:
                    
                    #add the type of error for error events
                    if not j['out']:
                        toStore['error'] = "Success"
                    elif re.search('Syntax error',j['out'],re.IGNORECASE) is not None:
                        toStore['error'] = "Syntax error"
                    else:
                        toStore['error'] = "Type error"

                    if i in re.split(' |\(',j['in']):
                        #tag the problem it 
                        tag = problems.index(i)

                        #create a dictionary for every eval event
                        
                        toStore['time'] = item['time']
                        toStore['session'] = num
                        toStore['problem'] = tag
                        toStore['type'] = "error"

                        #dump the event to a file
                        json.dump(toStore, of)
                        of.write('\n')

                        done = True
                        break
                if done: break

    inf.close()
    of.close()


############################################################################################################# Main
dir = os.path.abspath(__file__ + '/../../')

target = os.path.join(dir, 'sp14')
output = os.path.join(dir, 'homework3')
output2 = os.path.join(dir, 'homework3-withtag')

# homework 1 problems
# problems = ['???','palindrome', 'listReverse', 'digitalRoot', 'additivePersistence', 'digitsOfInt', 'sumList']
#homework2 problems
#problems = ['???','build','eval','exprToString','fixpoint','wwhile','removeDuplicates','assoc']
# homework 3 problems
problems = ['???','bigMul','mulByDigit','bigAdd','removeZero', 'padZero', 'clone', 'stringOfList', 'sepConcat', 'pipe', 'sqsum']

findhw(target, output)

if not os.path.exists(output2):
    os.makedirs(output2)

hw1 = list()
for i in os.listdir(output):
    dump_events(os.path.join(target,i), os.path.join(output2,i), problems)
