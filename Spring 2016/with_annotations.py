import os
import subprocess
from pygments.token import Token
from pygments.lexers import get_lexer_by_name



hw1 = ['???','sumList','digitsOfInt', 'additivePersistence', 'digitalRoot', 'listReverse', 'palindrome']
hw2 = ['???','assoc','removeDuplicates', 'wwhile','fixpoint', 'exprToString', 'eval', 'build', 'doRandomGray', 'doRandomColor']
hw3 = ['???','sqsum', 'pipe', 'sepConcat', 'stringOfList', 'clone', 'padZero', 'removeZero', 'bigAdd', 'mulByDigit', 'bigMul']

annotation_hw1 = ["",\
	"val sumList : int list -> int", \
	"val digitsOfInt : int -> int list", \
	"val additivePersistence : int -> int", \
	"val digitalRoot : int -> int", \
	"val listReverse : 'a list -> 'a list", \
	"val palindrome : string -> bool"]

annotation_hw2_1 = ["",\
	"val assoc : int * string * (string * int) list -> int ",\
	"val assoc : 'a * 'b * ('b * 'a) list -> 'a ", \
	"val removeDuplicates : int list -> int list", \
	"val wwhile : (int -> int * bool) * int -> int", \
	"val fixpoint: (int -> int) * int -> int", \
	"val exprToString : expr -> string", \
	"val eval : expr * float * float -> float", \
	"val build: ((int * int -> int) * int) -> expr", \
	"val doRandomGray : int * int * int -> unit", \
	"val doRandomColor : int * int * int -> unit"]

annotation_hw2_2 = ["",\
	"val assoc : int * string * (string * int) list -> int ",\
	"val assoc : 'a * 'b * ('b * 'a) list -> 'a ", \
	"val removeDuplicates : 'a list -> 'a list", \
	"val wwhile : ('a -> 'a * bool) * 'a -> 'a", \
	"val fixpoint: ('a -> 'a) * 'a -> 'a", \
	"val exprToString : expr -> string", \
	"val eval : expr * float * float -> float", \
	"val build: ((int * int -> int) * int) -> expr", \
	"val doRandomGray : int * int * int -> unit", \
	"val doRandomColor : int * int * int -> unit"]

annotation_hw3 = ["",\
	"val sqsum : int list -> int ", \
	"val pipe : ('a -> 'a) list -> ('a -> 'a)", \
	"val sepConcat : string -> string list -> string", \
	"val stringOfList : ('a -> string) -> 'a list -> string", \
	"val clone : 'a -> int -> 'a list", \
	"val padZero : int list -> int list -> int list  * int list", \
	"val removeZero : int list -> int list", \
	"val bigAdd : int list -> int list -> int list", \
	"val mulByDigit : int -> int list -> int list ", \
	"val bigMul : int list -> int list -> int list"]

"""
build dictionaries for problem name and annotation pair
"""

def build_dict(problem, annotation):

	problem_dict = {}
	problem_dict = dict(zip(problem, annotation))
	return problem_dict

dict_one = build_dict(hw1,annotation_hw1)
dict_two = build_dict(hw2,annotation_hw2_1)
dict_three = build_dict(hw3,annotation_hw3)



#suppose I got a string of code, I will run the string as a piece
#of ocaml code, and return 1 if I capture an error, 0 if no error
def check_err(string_of_code):
	#print([string_of_code])
	error_output = subprocess.run(["ocaml"], input = string_of_code, 
                                stdout=subprocess.PIPE,universal_newlines = True)
	if "rror" in error_output.stdout:
		return 1
	return 0


def find_label(problem_set, code):
	if code != []:
		split = code.split()
		for i in problem_set:
			if i in code.split():
				return i
	return '???'


#######################################################

dir = os.path.abspath(__file__ + '/../')
target = os.path.join(dir, 'sp14')
outputFile = os.path.join(dir, 'new_errors.txt')


for i in os.listdir(target):

	if i == '.DS_Store':
		continue
		
	with open (os.path.join(target,i), 'r') as myfile:
		name = str.split(i, '.')

		student = name[0]
		hw_num = name[1]
		

		for line in myfile:
			# str -> dict
			item = eval(line)

			# only process the ones with "in" field
			if item["ocaml"] != []:

				if(hw_num == "hw1"):
					for p in item["ocaml"]:
						problem_name = find_label(hw1, p['in'])

				elif(hw_num == "hw2"):
					for p in item["ocaml"]:
						problem_name = find_label(hw2, p['in'])	

				elif(hw_num == "hw3"):
					for p in item["ocaml"]:
						problem_name = find_label(hw3, p['in'])
		
			# with problem name, find which annotation to append in the 'in' field
			# call function that evaluates the code with subprocess and get the new error message

		myfile.close() 





