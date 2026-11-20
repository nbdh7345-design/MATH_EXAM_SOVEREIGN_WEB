-- Lean 4 Core verification for CALC-MV2-04 (|∇f|^2 = 2^2 + m^2)
def gradSq (m : Nat) : Nat := 2 ^ 2 + m ^ 2
-- squares of the options: (m + 2)^2, m^2 + 4, m^2 + 2, (m^2 + 4)^2
theorem calc_mv2_04_answer :
    (List.range 8).all (fun k => let m := k + 2; gradSq m == m ^ 2 + 4
      && [(m + 2) ^ 2, m ^ 2 + 4, m ^ 2 + 2, (m ^ 2 + 4) ^ 2].Nodup) = true := by decide
