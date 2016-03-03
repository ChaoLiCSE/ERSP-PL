import os
import subprocess
from pygments.token import Token
from pygments.lexers import get_lexer_by_name

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
        code = ' '.join([str(token) for token in tokens[0:i]]) + ('failwith "" ;;')
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
target = os.path.join(dir, 'unify_syntax')

for i in os.listdir(target):
  with open (os.path.join(target, i), 'r') as myfile:
    text = myfile.read().replace('\n', ' ')
    tokens = to_array(text)
    myfile.close()

  print(find_min_interval(tokens))

