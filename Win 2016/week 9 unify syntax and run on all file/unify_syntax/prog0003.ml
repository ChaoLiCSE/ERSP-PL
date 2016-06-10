let rec digitsOfInt n = match n with
| (n mod 10) + digitsOfInt  (n/10)