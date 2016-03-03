import os
import subprocess
from pygments.token import Token
from pygments.lexers import get_lexer_by_name
import math

"""
1. loop through all files
2. for each file, separate the string of code into tokens
3. use a nested loop to test the minimum interval of fix that will allow the program to pass compiler check
"""
# Ocaml lexer, strip all leading and trailing whitespace from the input 
lexer = get_lexer_by_name('Ocaml', stripall=True)

# given a .ml file, split code into tokens and output the result array
def to_array(text):
  tokens = []
  li = lexer.get_tokens(text)

  for token in li:
    if token[0] is Token.Text:
      continue
    tokens.append(token[1])

  return tokens

#suppose I got a string of code, I will run the string as a piece
#of ocaml code, and return 1 if I capture an error, 0 if no error
def check_err(string_of_code):
  #print([string_of_code])
  error_output = subprocess.run(["ocaml"], input = string_of_code, 
                                stdout=subprocess.PIPE,universal_newlines = True)
  if "rror" in error_output.stdout:
    return 1
  return 0

# given an array of tokens, find the min interval of fix
def find_min_interval(tokens):
  min_val = float('inf')
  counter = 1
  i = 0
  
  tmp1 = [str(token) for token in tokens[0:len(tokens)]]
  print (' '.join(tmp1) + ';;')


  while (counter < len(tokens)):
    for i in range(0, len(tokens) - 1):
      
      j = i+counter

      if j == len(tokens) - 1:
        code = ' '.join([str(token) for token in tokens[0:i]]) + (' (failwith "") ;;')
      else:
        tmp1 = [str(token) for token in tokens[0:i]]
        tmp2 = [str(token) for token in tokens[j + 1:len(tokens)]]
        code = ' '.join(tmp1) + ' (failwith "") ' + ' '.join(tmp2) + ';;'

      if (check_err(code) == 0):
        print (code)
        return counter

    counter = counter+1


################################################ MAIN

dir = os.path.abspath(__file__ + '/../../')
target = os.path.join(dir, 'list_of_errors.json')
target2 = os.path.join(dir, 'problems.txt')

list_of_num = []
counter1 = 0

with open (os.path.join(target), 'r') as myfile:
    for line in myfile:

      if counter1 > 100:
        break
      counter1= counter1+1

      item = eval(line)
      for i in range(len(item["bad"])):
        text = item["bad"][i].replace('\n', ' ')
        tokens = to_array(text)

        #only deal with the token < 40 situations
        if(len(tokens) < 40):
          num = (find_min_interval(tokens))
          list_of_num.append(num)
        

    myfile.close() 

'''
with open(os.path.join(target2), 'a') as of:
  of.write(''.join(list_of_num))
  of.write('\n')
output.close()
'''

print (list_of_num)

list_of_bin=[0,0,0,0,0,0,0,0,0]

for i in range (len(list_of_num)):
  
  if(list_of_num[i] != None):
    bin = math.floor(list_of_num[i]/5)
    list_of_bin[bin]= list_of_bin[bin]+1
  else:
    #case is None
    list_of_bin[8]= list_of_bin[8]+1


print(list_of_bin)
#print(find_min_interval(tokens))

