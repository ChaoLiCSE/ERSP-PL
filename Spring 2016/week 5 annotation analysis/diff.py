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
        if(len(old) != 0):
            return (old and [('-', old, [opos+sub_start_old, opos+sub_start_old+len(old)-1])] or []) + (new and [('+', new, [opos+sub_start_old,opos+sub_start_old+len(old)-1] )] or [])
        
        return (old and [('-', old, [opos+sub_start_old, opos+sub_start_old+len(old)-1])] or []) + (new and [('+', new, [opos+sub_start_old,opos+sub_start_old+len(old)] )] or [])
   

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


print(string_diff('The me quick red', 'Hi quick fox head paint red'))          

