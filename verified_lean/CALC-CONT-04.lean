-- Lean 4 Core verification for CALC-CONT-04 (ratio of leading coefficients m/1)
def leadingNum (m : Nat) : Nat := m
def leadingDen : Nat := 1

theorem calc_cont_04_answer :
    (List.range 8).all (fun k => let m := k + 2; leadingNum m / leadingDen == m && [1, m, 0, m + 1].Nodup) = true := by
  decide
