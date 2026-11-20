-- Lean 4 Core verification for CALC-APP-04 (area under y = m x^2 on [0, 1]); options scaled by 6
def area6 (m : Nat) : Nat := 6 * m / 3

theorem calc_app_04_area :
    (List.range 8).all (fun k => let m := k + 2; area6 m == 2 * m) = true := by decide
theorem calc_app_04_distinct :
    (List.range 8).all (fun k => let m := k + 2; [3 * m, 2 * m, 6 * m, m].Nodup) = true := by decide
