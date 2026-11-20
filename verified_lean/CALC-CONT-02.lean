-- Lean 4 Core verification for CALC-CONT-02 (equivalent infinitesimals)
-- numerator ~ m x^2, denominator ~ x^2/2 => ratio of leading coefficients m / (1/2) = 2m
-- All quantities scaled by 2 to stay in Nat
def numCoeff2 (m : Nat) : Nat := 2 * m
def denCoeff2 : Nat := 1
def options2 (m : Nat) : List Nat := [2 * m, m, 4 * m, 8 * m]

theorem calc_cont_02_ratio :
    (List.range 8).all (fun k => let m := k + 2; numCoeff2 m / denCoeff2 == 2 * m) = true := by decide
theorem calc_cont_02_distinct :
    (List.range 8).all (fun k => let m := k + 2; (options2 m).Nodup) = true := by decide

#eval numCoeff2 3 / denCoeff2
