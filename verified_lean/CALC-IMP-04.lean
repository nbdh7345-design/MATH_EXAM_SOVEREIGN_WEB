-- Lean 4 Core verification for CALC-IMP-04 (p-integral with p = m > 1)
-- Options scaled by m (m - 1) (m + 1) to compare as integers
def optionsScaled (m : Nat) : List Nat :=
  [(m - 1) * (m + 1), m * m * (m + 1), m * (m + 1), m * (m - 1)]

theorem calc_imp_04_convergent :
    (List.range 8).all (fun k => let m := k + 2; m > 1) = true := by decide
theorem calc_imp_04_distinct :
    (List.range 8).all (fun k => let m := k + 2; (optionsScaled m).Nodup) = true := by decide
