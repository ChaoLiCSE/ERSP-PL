import re
import subprocess
import os
from difflib import SequenceMatcher

'''
Modified from:
Simple Diff for Python version 1.0

Annotate two versions of a list with the values that have been
changed between the versions, similar to unix's `diff` but with
a dead-simple Python interface.

(C) Paul Butler 2008-2012 <http://www.paulbutler.org/>
May be used and distributed under the zlib/libpng license
<http://www.opensource.org/licenses/zlib-license.php>

Add the function to differ at which index does the 
words are different from each other.
'''

__all__ = ['diff', 'string_diff', 'html_diff']
__version__ = '1.0'


def diff(old, new, opos, npos):

    '''
    Find the differences between two lists. Returns a list of pairs, where the
    first value is in ['+','-','='] and represents an insertion, deletion, or
    no change for that list. The second value of the pair is the list
    of elements.

    Params:
        old     the old list of immutable, comparable values (ie. a list
                of strings)
        new     the new list of immutable, comparable values
   
    Returns:
        A list of pairs, with the first part of the pair being one of three
        strings ('-', '+', '=') and the second part being a list of values from
        the original old and/or new lists. The first part of the pair
        corresponds to whether the list of values is a deletion, insertion, or
        unchanged, respectively.


    '''

    # Create a map from old values to their indices
    old_index_map = dict()
    for i, val in enumerate(old):
        old_index_map.setdefault(val,list()).append(i)
        
    # Find the largest substring common to old and new.
    # We use a dynamic programming approach here.
    # 
    # We iterate over each value in the `new` list, calling the
    # index `inew`. At each iteration, `overlap[i]` is the
    # length of the largest suffix of `old[:i]` equal to a suffix
    # of `new[:inew]` (or unset when `old[i]` != `new[inew]`).
    #
    # At each stage of iteration, the new `overlap` (called
    # `_overlap` until the original `overlap` is no longer needed)
    # is built from the old one.
    #
    # If the length of overlap exceeds the largest substring
    # seen so far (`sub_length`), we update the largest substring
    # to the overlapping strings.

    overlap = dict()
    # `sub_start_old` is the 3index of the beginning of the largest overlapping
    # substring in the old list. `sub_start_new` is the index of the beginning
    # of the same substring in the new list. `sub_length` is the length that
    # overlaps in both.
    # These track the largest overlapping substring seen so far, so naturally
    # we start with a 0-length substring.
    sub_start_old = 0
    sub_start_new = 0
    sub_length = 0

    for inew, val in enumerate(new):
        _overlap = dict()


        for iold in old_index_map.get(val,list()):
            # now we are considering all values of iold such that
            # `old[iold] == new[inew]`.

            _overlap[iold] = (iold and overlap.get(iold - 1, 0)) + 1
            if(_overlap[iold] > sub_length):
                # this is the largest substring seen so far, so store its
                # indices
                sub_length = _overlap[iold]
                sub_start_old = iold - sub_length + 1
                sub_start_new = inew - sub_length + 1
                old_ind = iold
                new_ind = inew

        overlap = _overlap
        
        
    if sub_length == 0:
        # If no common substring is found, we return an insert and delete...

        return (old and [('-', old, [opos+sub_start_old, opos+sub_start_old+len(old)-1])] or []) + (new and [('+', new, [npos+sub_start_new,npos+sub_start_new+len(new)-1] )] or [])
    else:
        # ...otherwise, the common substring is unchanged and we recursively
        # diff the text before and after that substring
 
        return diff(old[ : sub_start_old], 
                new[ : sub_start_new], opos, 
                npos) + \
               [('=', new[sub_start_new : sub_start_new + sub_length], 
                [opos+ sub_start_old, opos+ sub_start_old+sub_length-1])] + \
                diff(old[sub_start_old + sub_length : ],
                new[sub_start_new + sub_length : ],
                opos+ sub_start_old+sub_length,
                npos+sub_length+sub_start_new)


def string_diff(old, new):
    '''
    Returns the difference between the old and new strings when split on
    whitespace. Considers punctuation a part of the word

    This function is intended as an example; you'll probably want
    a more sophisticated wrapper in practice.

    Params:
        old     the old string
        new     the new string

    Returns:
        the output of `diff` on the two strings after splitting them
        on whitespace (a list of change instructions; see the docstring
        of `diff`)

    Examples:
        >>> string_diff('The quick brown fox', 'The fast blue fox')
        ... # doctest: +NORMALIZE_WHITESPACE
        [('=', ['The'], [0, 0]), 
        ('-', ['quick', 'brown'], [1, 2]), 
        ('+', ['fast', 'blue'], [1, 2]), 
        ('=', ['fox'], [3, 3])]

    '''
    #print(diff(old.split(), new.split(),0,0))
    return diff(old.split(), new.split(),0,0)

       

def get_pos(prog):

    error_output = subprocess.run(["ocaml"], input = prog + ';;', 
                   stdout=subprocess.PIPE,universal_newlines = True)

    if "rror" in error_output.stdout:
    	m = re.search('(?<=Characters )([1-9][0-9][0-9]|[1-9][0-9]|[0-9])', error_output.stdout)
    	n = re.search('(?<=-)([1-9][0-9][0-9]|[1-9][0-9]|[0-9])', error_output.stdout)
    else:
      return([0,0])
    
    '''
    print(m.group(0))
    print(n.group(0))
    '''
    start = int(m.group(0))
    end = int(n.group(0))
    
    start_pos = len(str.split(prog[0:start]))-1
    end_pos = len(str.split(prog[0:end]))-1
    
    #print(str.split(prog[0:start]))
    #print(str.split(prog[0:end]))
    #print([start_pos,end_pos])
    return([start_pos,end_pos])


def err_judge(bad, fix, pos):
    
    
    print('bad:')
    print (bad)
    print('fix:')
    print (fix)
    print (pos)
    
    

    #print(pos)
	#get the key word to judge whether it is changed
    to_judge = bad[pos[0]: pos[1]]

    s = string_diff(bad, fix)
    print(s)
    for i in s:
      
      

      if (i[0] == '-' and 
        ((pos[0] <= i[2][0] and pos[1] >= i[2][0] ) or 
          (pos[0] <= i[2][1] and pos[1] >= i[2][1]) or
          (pos[0] >= i[2][0] and pos[1] <= i[2][1]))):
        
        #print('correct location')
        #print(i)
        return 1

      if(i[2][0] > pos[1] and i[2][1] > pos[1]):
        return 0
    #print('incorrect location')
    return 0



dir = os.path.abspath(__file__ + '/../../../')
#target = os.path.join(dir, 'annotated_6509.json')
target = os.path.join(dir, 'check.json')

target2 = os.path.join(dir, 'problems.txt')


'''
prog = "let rec digitsOfInt n = match n with | ( n mod 10 ) + digitsOfInt ( (failwith "") 10 );;"
for i in get_pos (prog):
    print (i)
'''

total = 0
prev_corr = 0
anno_corr = 0
counter1 = 0

both_correct = 0
both_wrong = 0
only_anno_corr = 0
only_pre_corr = 0

with open (os.path.join(target), 'r') as myfile, open (os.path.join(target2), 'w') as out:
    for line in myfile:

      item = eval(line)
      #for i in range(len(item["bad"])):
      #print(item["bad"])

      pos = get_pos(item["bad"])
      retVal = err_judge(item["bad"],item["fix"],pos)
        

      if(retVal == -1):
          print('cannot judge at 1')
          out.write('error at: ')
          out.write(item[bad])
          continue

      total = total+1
      if(retVal == 1):
          prev_corr = prev_corr + 1
      
      #deal with annotated
      pos = get_pos(item["annotated"] )
      retVal_a = err_judge(item["annotated"], item["annotated_fix"], pos)

      #check strange errors
      if(retVal == -1):
          print('cannot judge at 2')
          out.write('error at: ')
          out.write(item[annotated])
          continue

      if(retVal_a == 1):
          anno_corr = anno_corr+1
      
      #put the output to different categories
      if(retVal_a == 1 and retVal == 1):
            both_correct = both_correct +1
      elif(retVal_a == 1 and retVal == 0):
            only_anno_corr = only_anno_corr + 1
            print('anno correct')
            out.write('only_anno_corr \n')
            out.write(line)
            out.write('\n')
      elif(retVal_a == 0 and retVal == 1):
            only_pre_corr = only_pre_corr + 1
            print('pre correct')
            out.write('only_pre_corr\n')
            out.write(line)
            out.write('\n')
      else:
            both_wrong = both_wrong +1

myfile.close() 
s = 'in the total of ' + str(total) + ' programs, both correct is: ' + str(both_correct) + 'only annotated correct is: ' + str(only_anno_corr) + 'only pre correct is: ' + str(only_pre_corr) + 'both wrong is: '+str(both_wrong)

print (s)

