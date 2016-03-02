let rec digitsOfInt n = match n with
| n < 0 -> []
| _     -> n%10 digitsOfInt  n/10