import os
from pygments.token import Token
from pygments.lexers import get_lexer_by_name

dir = os.path.abspath(__file__ + '/../')
target = os.path.join(dir, 'list_of_errors.json')

# Ocaml lexer, strip all leading and trailing whitespace from the input 
lexer = get_lexer_by_name('Ocaml', stripall=True)

# length of all 'bad' programs
summary = []

with open(target) as inf:
  for line in inf:
    item = eval(line)

    for text in item['bad']:
      num = 0
      v = lexer.get_tokens(text)
      for i in v:
        if i[0] != Token.Text:
          num += 1
      summary.append(num)

for i in summary:
  print(i)