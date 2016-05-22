import os
import re
import json
import subprocess,shlex
from threading import Timer

hw1 = ['???','sumList','digitsOfInt', 'additivePersistence', 'digitalRoot', 'listReverse', 'palindrome']
hw2 = ['???','assoc','removeDuplicates', 'wwhile','fixpoint','expr', 'exprToString', 'eval', 'build']
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
  var_regex = '(?<=' + problem_name + ' )(.*?)(?=\=)'
  var = re.search(var_regex, code)
  # match the string to replace
  my_regex = '(?<=' + problem_name + ' )(.*?)\='
  result = re.sub(my_regex, lambda match: replace(match, var.group(), annotation), code,1)
  #print (result)
  return result

def replace(match, variables, annotation):
  replacement = annotation
  replacement += ' = fun '
  replacement += variables
  replacement += ' -> '
  return replacement

def find_annotation(indice):
  
  annotation = ''
  if(indice['problem'] == '???'):
    print("helper method here")
    return(annotation)

  if (indice['hw'] == 'hw1'):
    annotation = annotation_hw1[hw1.index(indice['problem'])]
  elif (indice['hw'] == 'hw2'):
    annotation = annotation_hw2[hw2.index(indice['problem'])]
  elif (indice['hw'] == 'hw3'):
    annotation = annotation_hw3[hw3.index(indice['problem'])]
  return(annotation)

def build_dict(bad, annotation, indice):

  dic = dict()
  dic['bad'] = bad
  dic['annotated'] = add_annotation(annotation, indice['problem'], bad)
  if not indice['fix']:
    dic['fix'] = ''
  else:
    dic['fix'] = indice['fix'][0]
  dic['annotated_fix'] = add_annotation(annotation, indice['problem'], dic['fix'])
  return dic

def find_annotation_with_label(hw_num, label):
  #print(hw_num)
  #print(label)
  annotation = ''
  if (hw_num == 'hw1'):
    annotation = annotation_hw1[hw1.index(label)]
  elif (hw_num =='hw2'):
    annotation = annotation_hw2[hw2.index(label)]
  elif (hw_num == 'hw3'):
    #print(hw3.index(label))
    annotation = annotation_hw3[hw3.index(label)]
  return(annotation)

def run(cmd, timeout_sec):
  proc = subprocess.Popen(["python"], stdout=subprocess.PIPE, 
  stderr=subprocess.PIPE,universal_newlines = True)
  print(cmd)
  print(proc.communicate("while True: print('hello')\n", timeout = timeout_sec)[0])

  '''
  stdout = proc.stdout.readline()
  proc.communicate(timeout = timeout_sec)
  #stdout = proc.stdout.read()
  print(stdout)
  #print(stderr)
  '''

def annotate_and_compile(indice, label, hw_num):
  #print(label)
  annotation = find_annotation_with_label( hw_num, label)
  #print(annotation)
  annotated_prog = add_annotation(annotation, label, indice['ocaml'][0]['min'])
  #print (annotated_prog)
  #annotated_prog = add_annotation( ": ('a -> 'a * bool) * 'a -> 'a",'wwhile',"let rec wwhile (f,b) = let (b',c') = f b in if c' then wwhile (f, b') else b';;\n let _ = let f x = let xx = (x * x) * x in (xx, (xx < 100)) in wwhile (f, 1);;")
  #annotated_prog = "let rec wwhile  : ('a -> 'a * bool) * 'a -> 'a = fun (f,b)  ->  let c' = f b in if c' = b then c' else wwhile (f, c');;"
  
  try:
    error_output = subprocess.run(["ocaml"], input = annotated_prog, 
                             stdout=subprocess.PIPE,universal_newlines = True, timeout=2)
    #print(error_output)
  except subprocess.TimeoutExpired:
    #print('timeout')
    error_output = 'Expired'

  '''
  try:
      error_output =run(annotated_prog, 1)
  except subprocess.TimeoutExpired:
      print('timeout')
  '''

  #print(error_output)
  
  if(error_output == 'Expired'):
    #print()
    #print("logic")
    return "logic error"

  #print(error_output)
  if "rror" in error_output.stdout:
    return error_output.stdout
  else:
    return ""


#obj = 'buildob= 1, build = 1'
#anno = add_annotation('hello', 'build', obj)
#print (anno)


#obj = {"event": "eval", "ocaml": [{"type": "other", "in": "let rec mulByDigit i l = \nmatch (List.rev l) with\n| []   -> 0\n| h::t -> ( (h*i)/10 + List.rev i t )", "min": "\nlet rec mulByDigit i l =\n  match List.rev l with | [] -> 0 | h::t -> ((h * i) / 10) + (List.rev i t);;\n", "out": "Characters 85-93:\n  | h::t -> ( (h*i)/10 + List.rev i t );;\n                         ^^^^^^^^\nError: This function has type 'a list -> 'a list\n       It is applied to too many arguments; maybe you forgot a `;'.\n"}]}
#print(annotate_and_compile(obj,'mulByDigit','hw3'))