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

  with open(os.path.join(directory, filename)) as inf:
    text = inf.read()
    string = text.replace('\n', ' ')
    tokens = to_array(string)
    res = min_size_and_fixed_code((tokens))

    inf.close()

  ans['in'] = text
  ans['fixed'] = res[0]
  ans['span-size'] = res[1]
  ans['span-fraction'] = res[1]/len(tokens)

  return ans

##############################################################################
# HELPER FUNCTIONS ###########################################################
##############################################################################

# given a .ml file, split code into tokens and output the result array
def to_array(text):
  tokens = []

  lexer = get_lexer_by_name('Ocaml', stripall=True)
  li = lexer.get_tokens(text)

  for token in li:
    if token[0] is Token.Text:
      continue
    tokens.append(token[1])

  return tokens

# given a string of code, check whether it can pass the compiler test
def check_err(string_of_code):
  error_output = subprocess.run(["ocaml"], input = string_of_code, 
                                stdout=subprocess.PIPE,universal_newlines = True)
  if "rror" in error_output.stdout:
    return 1
  return 0

# given an array of tokens, find the min interval of fix
def min_size_and_fixed_code(tokens):
  spansize = 1

  while (spansize < len(tokens)):
    for i in range(0, len(tokens) - 1):

      j = i + spansize

      if j == len(tokens) - 1:
        code = ' '.join([str(token) for token in tokens[0:i]]) + '(failwith "");;'
      else:
        tmp1 = [str(token) for token in tokens[0:i]]
        tmp2 = [str(token) for token in tokens[j + 1:len(tokens)]]
        code = ' '.join(tmp1) + ' (failwith "") ' + ' '.join(tmp2) + ';;'
 
      if check_err(code) is 0:
        # print(code)
        return (code, spansize)

    spansize += 1