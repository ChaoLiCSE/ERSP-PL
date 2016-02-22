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

print(sum(i <= 10 for i in summary))
print(sum(i <= 20 for i in summary))
print(sum(i <= 30 for i in summary))
print(sum(i <= 40 for i in summary))
print(sum(i <= 50 for i in summary))
print(sum(i <= 60 for i in summary))
print(sum(i <= 70 for i in summary))
print(sum(i <= 80 for i in summary))
print(sum(i <= 90 for i in summary))
print(sum(i <= 100 for i in summary))
print(sum(i <= 110 for i in summary))
print(sum(i <= 120 for i in summary))
print(sum(i <= 130 for i in summary))
print(sum(i <= 140 for i in summary))
print(sum(i <= 150 for i in summary))
print(sum(i <= 160 for i in summary))
print(sum(i <= 170 for i in summary))
print(sum(i <= 180 for i in summary))
print(sum(i <= 190 for i in summary))
print(sum(i <= 200 for i in summary))
print(sum(i <= 210 for i in summary))
print(sum(i <= 220 for i in summary))
print(sum(i <= 230 for i in summary))
print(sum(i <= 240 for i in summary))
print(sum(i <= 250 for i in summary))
print(sum(i <= 260 for i in summary))
print(sum(i <= 270 for i in summary))
print(sum(i <= 280 for i in summary))
print(sum(i <= 290 for i in summary))
print(sum(i <= 300 for i in summary))
print(sum(i <= 310 for i in summary))
print(sum(i <= 320 for i in summary))
print(sum(i <= 330 for i in summary))
print(sum(i <= 340 for i in summary))
print(sum(i <= 350 for i in summary))
print(sum(i <= 360 for i in summary))
print(sum(i <= 370 for i in summary))
print(sum(i <= 380 for i in summary))
print(sum(i <= 390 for i in summary))
print(sum(i <= 400 for i in summary))



# 7066 'bad' programs
#print(len(summary))

# average 47.9 tokens
#print(sum(summary) * 1.0/len(summary))
