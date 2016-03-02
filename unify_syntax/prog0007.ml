let _= additivePersistence 987623444;

(* uncomment and run AFTER you have implemented additivePersistence  

let _ = additivePersistence 9876

*)

(* NOTE: assume that digitalRoot is only called with positive numbers *)
let rec sum n = 
if n <= 0 
then 0
else (n mod 10) + sum (n/10)