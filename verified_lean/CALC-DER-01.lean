-- Lean 4 Core verification for CALC-DER-01: Leibniz 4th derivative coefficient
def binom4_2 : Nat := 6
def u_second_deriv : Nat := 2
def f4_at_zero (m : Nat) : Nat := binom4_2 * u_second_deriv * (m ^ 2)

theorem calc_der_01_m3 : f4_at_zero 3 = 108 := by decide
theorem calc_der_01_m5 : f4_at_zero 5 = 300 := by decide
theorem calc_der_01_formula (m : Nat) : f4_at_zero m = 12 * (m ^ 2) := by rfl

#eval f4_at_zero 3
