This is a set of programs deal with the data set, trying to pair each type
error program with a fix. We first use list of errors to generate 
bad program and fixed program pairs with annotated version. Then we
use week 5 annotation analysis to perform a diff on the bad and fix
program pairs to check how does type annotation out performs not
annotated version. 


PART 1 ： auto analysis
The order of using programs is:
1. run generate_concise in ~\ERSP-PL\Spring 2016\list_of_errors_ver3
   to generate a concise version which only contains the information we
   want from the total data set
2. run list_of_errors_ver3 in ~\ERSP-PL\Spring 2016\list_of_errors_ver3
   to generate a json dict contains a list of bad programs and their fixed 
   version
3. run type_annotate in ~\ERSP-PL\Spring 2016\list_of_errors_ver3
   to produce a json dict paired with bad, bad_anno, fix, fix_anno programs
4. run compare_errs in ~\ERSP-PL\Spring 2016\week 5 annotation analysis
   to get a report on how does annotation performs against no annotation 
   versions

WARNING:
The list_of_error is still under debuging. It is possible to get some buggy
message right now.

PART2: manual analysis
The randomly chosen 100 pairs of bad and fixed program is in the folder sample.
We did a manual comparation on how the error message improve with annotations.