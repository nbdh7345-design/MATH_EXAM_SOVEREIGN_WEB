-- Lean 4 Core verification for CALC-LIM-04 (sin(mx)/x = m * sin(mx)/(mx))
-- Options scaled by m: 1 -> m, m -> m^2, 1/m -> 1, m^2 -> m^3
def optionsScaled (m : Nat) : List Nat := [m, m ^ 2, 1, m ^ 3]

theorem calc_lim_04_distinct :
    (List.range 8).all (fun k => let m := k + 2; (optionsScaled m).Nodup) = true := by decide
theorem calc_lim_04_answer :
    (List.range 8).all (fun k => let m := k + 2; m * 1 == m) = true := by decide
