let rec last l = match l with 
| [] -> []
| _::tl -> last tl :: _