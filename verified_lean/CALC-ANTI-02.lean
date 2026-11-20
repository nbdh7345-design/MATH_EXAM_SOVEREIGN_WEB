-- Lean 4 Core verification for CALC-ANTI-02 (variable upper limit + L'Hospital)
-- sin(m t^2) = m t^2 + o(t^2)  =>  ∫_0^x sin(m t^2) dt = m x^3 / 3 + o(x^3)
-- All option values scaled by 6
def leading6 (m : Nat) : Nat := 6 * m / 3
def options6 (m : Nat) : List Nat := [6 * m, m, 3 * m, 2 * m]

theorem calc_anti_02_leading :
    (List.range 8).all (fun k => let m := k + 2; leading6 m == 2 * m) = true := by decide
theorem calc_anti_02_distinct :
    (List.range 8).all (fun k => let m := k + 2; (options6 m).Nodup) = true := by decide

#eval leading6 3
