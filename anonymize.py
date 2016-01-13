# dir - current directory
# dir/target - the directory that contains all json files to anonymize

# Replace all comments in the files under target dir.
# The new files will be written to a folder named anonymous.

# Note: this script SKIPs the file tkua.json

import re
import os
import json

dir = os.path.dirname('__file__')

target = os.path.join(dir, 'logs')  # change logs to name of the folder
directory = os.path.join(dir, 'anonymous')

# parse n number of json objects from the system path from a certain start point
def parse(infile, outfile):
  with open(infile) as inf, open(outfile,'w') as of:
    for line in inf:
      item = eval(line)
      result = re.sub('\(\*(.|\n)*?\*\)', replace, item['body'], flags=0)
      item['body'] = result
      json.dump(item, of)
      of.write('\n')
  inf.close()
  of.close()

# replace matched pattern
def replace(match):
  replacement = '(*'
  match = match.group()[2:-2]
  for c in match:
    if c == "\n":
      replacement += "\n"
    else:
      replacement += 'X'
  replacement += '*)'
  return replacement

if not os.path.exists(directory):
    os.makedirs(directory)

for i in os.listdir(target):
  print(i)
  if i == 'tkua.json':
    continue
  infile = os.path.join(target, i)
  outfile = os.path.join(directory, i)
  parse(infile, outfile)