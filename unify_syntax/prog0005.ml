let rec digitsOfInt n = match true with
| n<0 -> 0
| _ -> (n mod 10) + digitsOfInt  (n/10)