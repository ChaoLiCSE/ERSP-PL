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
  var_regex = '(?<=' + problem_name + ')(.*?)(?=\=)'
  var = re.search(var_regex, code)
  # match the string to replace
  my_regex = '(?<=' + problem_name + ')(.*?)\='
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
  if indice['hw'] is 'hw1':
    annotation = annotation_hw1[hw1.index(indice['problem'])]
  elif indice['hw'] is 'hw2':
    annotation = annotation_hw2[hw2.index(indice['problem'])]
  elif indice['hw'] is 'hw3':
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