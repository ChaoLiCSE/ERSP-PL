let rec listReverse l = match l with
| [] -> []
| hd::tl -> let x = last tl