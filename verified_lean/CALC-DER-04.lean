-- Lean 4 Core verification for CALC-DER-04 ((ln u)' = u'/u with u = 1 + m x, u(0) = 1)
def uAt0 (m : Nat) : Nat := 1 + m * 0
def uPrime (m : Nat) : Nat := m
def optionsScaled (m : Nat) : List Nat := [1, m, m ^ 3, m ^ 2]   -- options multiplied by m

theorem calc_der_04_answer :
    (List.range 8).all (fun k => let m := k + 2; uPrime m / uAt0 m == m) = true := by decide
theorem calc_der_04_distinct :
    (List.range 8).all (fun k => let m := k + 2; (optionsScaled m).Nodup) = true := by decide
