import os
from difflib import SequenceMatcher

def err_judge(bad, fix, pos):
    print (type (bad))
    print (type (fix))
    print (type(pos))

	#get the key word to judge whether it is changed
    to_judge = bad[pos[0]: pos[1]]

	#first find out what are the different place in bad and fix
    s = SequenceMatcher(lambda x: x==" ", bad, fix)
    
    for tag, i1, i2, j1, j2 in s.get_opcodes():

    	print ("%7s a[%d:%d] (%s) b[%d:%d] (%s)" % 
    		(tag, i1, i2, bad[i1:i2], j1, j2, fix[j1:j2]))

    	#the code at that position has been changed
    	if tag in ['replace' , 'delete'] and (i1 <= pos[0] or i2 >= pos[1]):
    		print("correct location")
    		return 1

    	#the code at that position has not been changed
    	if tag in ['equal'] and (i1 <= pos[0] and i2 >= pos[1]):
            print ("incorrect location")
            return 0

    print ("cannot decide")
    return -1


bad = "let bigAdd l1 l2 = \nlet add (l1, l2) = \nlet f a x = in\nlet base = ([],[]) in\nlet args = f l1 l2 in\nlet (_, res) = List.fold_left f base args in\nres\nin \nremoveZero (add (padZero l1 l2))"
fix = "let bigAdd l1 l2 = \nlet add (l1, l2) = \nlet f a x = () in\nlet base = ([],[]) in\nlet args = f l1 l2 in\nlet (_, res) = List.fold_left f base args in\nres\nin \nremoveZero (add (padZero l1 l2))"
annotated_bad = "let bigAdd : int list -> int list -> int list = fun  l1 l2  ->  \nlet add (l1, l2) = \nlet f a x = in\nlet base = ([],[]) in\nlet args = f l1 l2 in\nlet (_, res) = List.fold_left f base args in\nres\nin \nremoveZero (add (padZero l1 l2))"
annotated_fix = "let bigAdd : int list -> int list -> int list = fun  l1 l2  ->  \nlet add (l1, l2) = \nlet f a x = () in\nlet base = ([],[]) in\nlet args = f l1 l2 in\nlet (_, res) = List.fold_left f base args in\nres\nin \nremoveZero (add (padZero l1 l2))"
pos = [52, 54]
retVal = err_judge(bad, fix, pos)
print (retVal)

pos = [97, 99]
retVal = err_judge(annotated_bad, annotated_fix, pos)
print (retVal)