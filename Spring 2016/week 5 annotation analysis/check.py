import json
import os
dir = os.path.abspath(__file__ + '/../../')
target = os.path.join(dir, 'sample.json')

with open (os.path.join(target), 'r') as myfile:
    for line in myfile:
    	item = eval(line)
    	print('---------------------------------------------')
    	print(item["bad"])
    	print('---------------------------------------------')

    	print(item["fix"])
    	print('---------------------------------------------')

    	print(item["annotated"])
    	print('---------------------------------------------')

    	print(item["annotated_fix"])