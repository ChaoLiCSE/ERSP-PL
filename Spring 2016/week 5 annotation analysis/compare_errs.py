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

        #return (old and [('-', old, [opos+sub_start_old, opos+sub_start_old+len(old)-1])] or []) + (new and [('+', new, [opos+sub_start_old,opos+sub_start_old+len(new)-1] )] or [])
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
    return diff(old.split(), new.split(),0,0)

       

def get_pos(prog):
    
    to_run = prog.split(';;')
    to_con = ""
    #print("printing parts!")
    count = 0
    #print(to_run)
    for part in to_run:
        #print(count)
        #print(part)
        to_con += ';;'
        to_con += part

        error_output = subprocess.run(["ocaml"], input = to_con+';;', 
                   stdout=subprocess.PIPE,universal_newlines = True)
        #print(error_output)

        if "rror" in error_output.stdout:
            m = re.search('(?<=Characters )([1-9][0-9][0-9]|[1-9][0-9]|[0-9])', error_output.stdout) 
            n = re.search('(?<=-)([1-9][0-9][0-9]|[1-9][0-9]|[0-9])', error_output.stdout)
            break
        else:
            count+=len(part)
            continue
    

    #print(m.group(0))
    #print(n.group(0))
    try:
        if(m != None and n != None):
            start = int(m.group(0)) + count
            end = int(n.group(0)) + count
        else:
            print(to_run)
            print(error_output)
            return [-1,-1]
    except UnboundLocalError:
        print(to_run)
        print(error_output)
        return([-1,-1])

    #print(prog[0:start])
    #print(prog[0:end])
    start_pos = len(str.split(prog[0:start]))-1
    end_pos = len(str.split(prog[0:end]))-1
    
    #print(str.split(prog[0:start]))
    #print(str.split(prog[0:end]))
    #print([start_pos,end_pos])
    return([start_pos,end_pos])

#the function to expand the length of the token span
def expand(end, pos):
    #print('this is pos')
    #print (pos)
    if(pos[0]>0 and (pos[1] == end)):
        epos = [pos[0]-1, pos[1]]
    
    elif(pos[0]>0 and (pos[1] != end)):
        epos = [pos[0]-1, pos[1]+1]
    elif((pos[0] == 0) and (pos[1] == end)):
        epos = pos
    else:
        epos = [0, pos[1]+1]

    #print("this is epos:")
    #print(epos)
    return epos

def find_new_pos(bad, fix, pos):

    s = string_diff(bad, fix)
    #print(s)
    new_pos_start = 0
    old_pos_start = 0
    for i in s:


        if(i[0] == '+'):

            new_pos_start = new_pos_start + (i[2][1] - i[2][0] + 1)
            if(old_pos_start >= pos[0]):

                new_pos_start = new_pos_start-(old_pos_start- pos[0])
                #new_pos_start = pos[0]-old_pos_start+new_pos_start
                break


        if(i[0] == '='):
            new_pos_start = new_pos_start + (i[2][1] - i[2][0] + 1)
            old_pos_start = old_pos_start + (i[2][1] - i[2][0] + 1)

            if(old_pos_start >= pos[0]):
                new_pos_start = new_pos_start -1
                old_pos_start = old_pos_start -1
                new_pos_start = new_pos_start-(old_pos_start- pos[0])
                break


        if(i[0] == '-'):
            
            if((pos[0] <= i[2][0] and pos[1] >= i[2][0] ) or 
          (pos[0] <= i[2][1] and pos[1] >= i[2][1]) or
          (pos[0] >= i[2][0] and pos[1] <= i[2][1])):
               return [-1,-1]

            #new_pos_start = new_pos_start - (i[2][1] - i[2][0] + 1)
            old_pos_start = old_pos_start + (i[2][1] - i[2][0] + 1)
            if(old_pos_start >= pos[0]):
                new_pos_start = new_pos_start-(old_pos_start- pos[0])
                #new_pos_start = pos[0]-old_pos_start+new_pos_start
                break
    '''
    print('old comp')
    print(pos)
    print([new_pos_start, new_pos_start+pos[1] - pos[0]])
    '''
    return [new_pos_start, new_pos_start+pos[1] - pos[0]]

def err_judge(bad, fix, pos):
    
    '''
    print('bad:')
    print (bad)
    print('fix:')
    print (fix)
    print (pos)
    '''



    end = len(bad.split())-1
    new_pos_start = 0
    pos_it = 0

    #print(pos)
	#get the key word to judge whether it is changed
    ex_pos = expand(len(bad), pos)
    new_pos = find_new_pos(bad, fix, pos)
    ex_new_pos = expand(len(bad),new_pos)


    '''
    print('poses:')
    print(pos)
    print(ex_pos)
    print(new_pos)
    print(ex_new_pos)
    '''

    if(new_pos == [-1,-1]):
        #print('-1-1 correct')
        return 1

    s= string_diff(bad,fix)

    
    for i in s:
      
      if (i[0] == '=' and ex_pos[0] >= i[2][0] and ex_pos[1] <= i[2][1] and (ex_pos[1]-ex_pos[0] >=2)):
        #print('incorrect location1')
        return 0

      if (i[0] == '-' and 
        ((ex_pos[0] <= i[2][0] and ex_pos[1] >= i[2][0] ) or 
          (ex_pos[0] <= i[2][1] and ex_pos[1] >= i[2][1]) or
          (ex_pos[0] >= i[2][0] and ex_pos[1] <= i[2][1]))):
        
        #print('correct location2')
        #print(i)
        return 1

      if(i[0] == '+' and
        ((ex_new_pos[0] <= i[2][0] and ex_new_pos[1] >= i[2][0] ) or 
          (ex_new_pos[0] <= i[2][1] and ex_new_pos[1] >= i[2][1]) or
          (ex_new_pos[0] >= i[2][0] and ex_new_pos[1] <= i[2][1]))):
        
        #print('correct location3')
        #print(i)
        return 1

    #print('incorrect location4')
    return 0



dir = os.path.abspath(__file__ + '/../../')
#target = os.path.join(dir, 'list_of_errors_ver3.json')
#target = os.path.join(dir, 'sample.json')
target = os.path.join(dir, 'check.json')

target2 = os.path.join(dir, 'problems.txt')

total = 0
prev_corr = 0
anno_corr = 0
counter1 = 0

both_correct = 0
both_wrong = 0
only_anno_corr = 0
only_pre_corr = 0
no_fix = 0

with open (os.path.join(target), 'r') as myfile, open (os.path.join(target2), 'w') as out:
    for line in myfile:
    
      item = eval(line)
      i=item["bad"]
      #for i in item["bad"]:
      '''
      print(i)
      print(item["fix"])
      print(item["annotated"])
      print(item["annotated_fix"])
'''
      if(item["fix"] == ""):
        print('no fix')
        no_fix = no_fix+1
        total = total +1
        continue
      
      #print(i)
      pos = get_pos(i)

      if(pos==[-1,-1]):
        print (item)

      retVal = err_judge(i,item["fix"],pos)
      #print(retVal)

      if(retVal == -1):
          print('cannot judge at 1')
          out.write('error at: ')
          out.write(i)
          continue

      total = total+1
      if(retVal == 1):
          prev_corr = prev_corr + 1
      
      #deal with annotated
      pos = get_pos(item["annotated"] )

      if(pos==[-1,-1]):
        print (item)

      retVal_a = err_judge(item["annotated"], item["annotated_fix"], pos)


      #check strange errors
      if(retVal == -1):
          print('cannot judge at 2')
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
s = 'in the total of ' + str(total) + ' programs, both correct is: ' + str(both_correct) + 'only annotated correct is: ' \
     + str(only_anno_corr) + 'only pre correct is: ' + str(only_pre_corr) + 'both wrong is: '+str(both_wrong) +\
     ' no fix: ' + str(no_fix)

print (s)



#print(find_new_pos('red fox pop', 'Hi hello world quick red',[2,2]))

#print(err_judge('quick red ', 'Hi hello world quick red', [0,0]))
#--->1

#print(err_judge('world quick red ', 'Hi hello world quick red', [1,1]))
#--->0

#print(err_judge('quick red ', 'Hi hello world quick red', [1,1]))
#--->0    

#print(err_judge(' quick red fox dog', 'Hi quick fox head paint red', [1,1]))          
#--->1

#print(err_judge('a b c m d e', 'p m n c m d e q', [3,4]))
#--->0

#print(err_judge('quick red ', 'Hi hello world quck red', [0,0])) 
#--->0

#print(err_judge('world quick red ', 'Hi hello world quick red', [1,1]))
#--->0
