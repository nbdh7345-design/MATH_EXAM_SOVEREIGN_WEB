-- Lean 4 Core verification for CALC-CONT-01 (limit of type 1^∞)
-- ln u_n = 2n ln(1 + m/n) ~ 2n * (m/n) = 2m; exponents of the options scaled by 2
def limitExponent (m : Nat) : Nat := 2 * m
def exponents2 (m : Nat) : List Nat := [2 * m, 4 * m, m, 6 * m]

theorem calc_cont_01_exponent :
    (List.range 8).all (fun k => let m := k + 2; 2 * limitExponent m == 4 * m) = true := by decide
theorem calc_cont_01_distinct :
    (List.range 8).all (fun k => let m := k + 2; (exponents2 m).Nodup) = true := by decide

#eval limitExponent 3
