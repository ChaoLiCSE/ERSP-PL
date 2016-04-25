import os
import re
import json

hw1 = ['???','sumList','digitsOfInt', 'additivePersistence', 'digitalRoot', 'listReverse', 'palindrome']
hw2 = ['???','assoc','removeDuplicates', 'wwhile','fixpoint', 'exprToString', 'eval', 'build']
hw3 = ['???','sqsum', 'pipe', 'sepConcat', 'stringOfList', 'clone', 'padZero', 'removeZero', 'bigAdd', 'mulByDigit', 'bigMul']

annotation_hw1 = ["",\
	" : int list -> int", \
	" : int -> int list", \
	" : int -> int", \
	" : int -> int", \
	" : 'a list -> 'a list", \
	" : string -> bool"]

annotation_hw2 = ["",\
	" : 'a * 'b * ('b * 'a) list -> 'a ", \
	" : 'a list -> 'a list", \
	" : ('a -> 'a * bool) * 'a -> 'a", \
	": ('a -> 'a) * 'a -> 'a", \
	" : expr -> string", \
	" : expr * float * float -> float", \
	": ((int * int -> int) * int) -> expr"]

annotation_hw3 = ["",\
	" : int list -> int ", \
	" : ('a -> 'a) list -> ('a -> 'a)", \
	" : string -> string list -> string", \
	" : ('a -> string) -> 'a list -> string", \
	" : 'a -> int -> 'a list", \
	" : int list -> int list -> int list  * int list", \
	" : int list -> int list", \
	" : int list -> int list -> int list", \
	" : int -> int list -> int list ", \
	" : int list -> int list -> int list"]

def add_annotation(annotation, problem_name, code):
	# match the variables
	var_regex = '(?<=' + problem_name + ')(.*)(?=\=)'
	var = re.search(var_regex, code)
	# match the string to replace
	my_regex = '(?<=' + problem_name + ')(.*)\='
	result = re.sub(my_regex, lambda match: replace(match, var.group(), annotation), code)
	return result

def replace(match, variables, annotation):
	replacement = annotation
	replacement += ' = fun '
	replacement += variables
	replacement += ' -> '
	return replacement

###
dir = os.path.abspath(__file__ + '/../../')
target = os.path.join(dir, 'Win 2016\week 7 list_of_errors\list_of_errors.json')
output = os.path.join(dir, r'Spring 2016\annotated_6509.json')

with open(target, 'r') as myfile, open(output, 'w') as of:

	for line in myfile:
		item = eval(line)

		# skip bad dictionaries
		if item['problem'] is '???' or item['problem'] is 'expr':
			continue

		# find corresponding annotations
		annotation = ''
		if item['hw'] is 'hw1':
			annotation = annotation_hw1[hw1.index(item['problem'])]
		elif item['hw'] is 'hw2':
			annotation = annotation_hw2[hw2.index(item['problem'])]
		elif item['hw'] is 'hw3':
			annotation = annotation_hw3[hw3.index(item['problem'])]

		# if annotation is not successful for any reason, skip it
		if not annotation:
			continue

		# build dict with bad programs, annotated programs, and fixed programs
		for bad in item['bad']:
			dic = dict()
			dic['bad'] = bad
			dic['annotated'] = add_annotation(annotation, item['problem'], bad)
			dic['fix'] = item['fix'][0]
			dic['annotated_fix'] = add_annotation(annotation, item['problem'], dic['fix'])
			json.dump(dic, of)
			of.write('\n')

	myfile.close()
	of.close()