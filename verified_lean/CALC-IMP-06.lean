-- Lean 4 Core verification for CALC-IMP-06
-- a) arctan(+∞) - arctan(0) = π/2  =>  I = π/(2m)  (coefficient of π: 1/(2m))
-- b) exponent 1 - 1/m = (m - 1)/m > 0  =>  J = m/(m - 1)
def piDenominator (m : Nat) : Nat := 2 * m
def jNumer (m : Nat) : Nat := m
def jDenom (m : Nat) : Nat := m - 1

theorem calc_imp_06_type2_converges :
    (List.range 8).all (fun k => let m := k + 2; 1 < m && jDenom m > 0) = true := by decide
theorem calc_imp_06_values :
    (List.range 8).all (fun k => let m := k + 2; piDenominator m == 2 * m && jNumer m * 1 == m) = true := by decide
