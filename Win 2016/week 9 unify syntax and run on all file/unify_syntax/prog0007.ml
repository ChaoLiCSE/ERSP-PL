let _= additivePersistence 987623444;




let rec sum n = 
if n <= 0 
then 0
else (n mod 10) + sum (n/10)