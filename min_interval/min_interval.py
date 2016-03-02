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


# given an array of tokens, find the min interval of fix
def find_min_interval(tokens):
  min_val = float('inf')
  
  for i in range(0, len(tokens) - 1):
    for j in range(i + 1, len(tokens)):
    
      if j == len(tokens) - 1:
        code = ' '.join([str(token) for token in tokens[0:i]]) + 'failwith ""'
      else:
        tmp1 = [str(token) for token in tokens[0:i]]
        tmp2 = [str(token) for token in tokens[j + 1:len(tokens)]]
        code = ' '.join(tmp1) + ' failwith "" ' + ' '.join(tmp2)

      f = open('sample.ml', 'w')
      f.write(code)
      f.close()
 
      result = subprocess.call(['ocamlc', 'sample.ml'], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)

      if result is 0:
        if j - i < min_val:
          min_val = j - i

  return min_val

################################################ MAIN
dir = os.path.abspath(__file__ + '/../../')
target = os.path.join(dir, 'unify_syntax')

for i in os.listdir(target):
  with open (os.path.join(target, i), 'r') as myfile:
    text = myfile.read().replace('\n', ' ')
    tokens = to_array(text)
    myfile.close()

  print(find_min_interval(tokens))