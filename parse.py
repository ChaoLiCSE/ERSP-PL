import re

path = r"C:\Users\Yijun\Desktop\OCaml\alperez.json"
out = r"C:\Users\Yijun\Desktop\ERSP-PL\test.json"
out2 = r"C:\Users\Yijun\Desktop\ERSP-PL\after.json"

# parse n number of json objects from the system path from a certain start point
def parse(infile, outfile, n = 0, start = 0):
  #data = []
  count = 0
  index = 0
  with open(infile) as inf, open(outfile,'w') as of:
    if n != 0:
      for line in inf:
        index += 1
        if index < start:
          continue
        item = eval(line)
        result = re.sub('\(\*(.|\n)*?\*\)', replace, item['body'], flags=0)
        of.write(result)
        #data.append(eval(line))
        count += 1
        if count == n:
          break
    #else:
      #for line in f:
        #data.append(eval(line))
  inf.close()
  of.close()
  #return data

# replace 
def replace(match):
  replacement = '(*'
  match = match.group()[2:-2]
  for c in match:
    if c == '\n':
      replacement += '\n'
    else:
      replacement += 'X'
  replacement += '*)'
  return replacement