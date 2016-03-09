'''
File name: find_min_interval.py
Discription: this is a file which takes in a text based program and
gives out a list of objects in file, out file, and the min interval,
and min_interval protion

TODO: 
Need to change the size to how much the interval is
change the type of the output list, and print in runall
to print the programs correctly
'''

import os
import subprocess
from pygments.token import Token
from pygments.lexers import get_lexer_by_name
import math

"""
This script finds the minimum span size of code that can be replaced by the 
'failwith' to pass ocaml compiler's check
"""

def find_min_interval(directory, filename):


  ans = dict()
  ans['fixed']=[]
  ans['span-size']=[]
  ans['span-fraction'] = []

  with open(os.path.join(directory, filename)) as inf:
    text = inf.read()
    string = text.replace('\n', ' ')
    tokens = to_array(string)
    print(tokens)
    res = min_size_and_fixed_code(tokens)
    for i in range(0,len(res)):
      print(res[i])
    print("see you")
    inf.close()

  ans['in'] = text

  length = len(res)-1
  for i in (0,length):

    print(res[i][0])
    ans['fixed'].append(res[i][0])
    print(res[i][1])
    print("res here")
    ans['span-size'].append(res[i][1])
    ans['span-fraction'].append(res[i][1]/len(tokens))
    print(ans)
    print("ans here")
  return ans

##############################################################################
# HELPER FUNCTIONS ###########################################################
##############################################################################

# given a .ml file, split code into tokens and output the result array
def to_array(text):
  tokens = []
  tokens.append([])
  function = 0

  lexer = get_lexer_by_name('Ocaml', stripall=True)
  li = lexer.get_tokens(text)
  

  for token in li:

    #print typeof(token)
    if token[0] is Token.Text:
      continue

    #devide into several functions
    if(token[1] != ';;'):
      tokens[function].append(token[1])
    else:
      function = function + 1
      tokens.append([])

  return tokens

# given a string of code, check whether it can pass the compiler test
def check_err(string_of_code):
  error_output = subprocess.run(["ocaml"], input = string_of_code, 
                                stdout=subprocess.PIPE,universal_newlines = True)
  if "rror" in error_output.stdout:
    return 1
  return 0

# given an array of tokens, find the min interval of fix
def min_size_and_fixed_code(tokenList):
  
  #length is the program number that tokenList contains
  length = len(tokenList)
  #relist should be [(fixcode1, spanSize1),(fixedcode2, spanSize2)]
  retList = []
  #jump out is a flag to jump out of the loops and get the next program to run
  jumpout = 0

  print("this is length: "+str(length) )

  #for all the programs the tokenList contains
  for k in range(0,length):

    #reinitialize the span size
    spansize = 0
    jumpout = 0

    print("this is i between 0 and length")
    print(k)
    print("this is length " + str(length))

    #the program we are dealing with
    tokens = tokenList[k]

    print("this is tokens")
    print(tokens)

    
    #increment the span size
    while (spansize < len(tokens)):

      #substitude all the tokens one by one
      for i in range(0, len(tokens) - 1):

        j = i + spansize

        if j == len(tokens) - 1:
          code = ' '.join([str(token) for token in tokens[0:i]]) + '(failwith "") ;;'
        else:
          tmp1 = [str(token) for token in tokens[0:i]]
          tmp2 = [str(token) for token in tokens[j + 1:len(tokens)]]
          code = ' '.join(tmp1) + ' (failwith "") ' + ' '.join(tmp2) + ';;'


        #if the span size is bigger than 30, we jump out of the loop, for looking into details
        if spansize < 30:

          print(spansize)
          print(code)

          #sent the program to check whether it contains any error
          value = check_err(code)

          print(value)

          #if no error occurs jump out of the loop, with code 1
          if value == 0:
            
            #print("this is spansize")
            #print(spansize)
            retList.append((code, spansize))
            print(retList)
            print("\n\n\n\n\n\n")
            jumpout = 1;
            break

        #if run out of time, we jump out of the loop with code -1
        else:
          #print("this is spansize")
          #print(spansize)
          print(code)
          spansize += 1
          print (">30 occur")
          print(retList)
          retList.append((code, spansize))
          jumpout = -1
          break

      #when we meet jump out situation, we change a program
      if jumpout != 0:
        break

      spansize += 1
    

    print("this is spansize")
    print(spansize)
  for i in range(0,len(retList)):
    print(retList[i])
  print("before ret")

  return retList