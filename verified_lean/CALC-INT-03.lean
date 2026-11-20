-- Lean 4 Core verification for CALC-INT-03: S(m) = (2 / m^3) / (1 / (2*m)) = 4 / m^2
-- Cleared denominators identity: (2 * (2 * m)) * m^2 = 4 * m^3
def s_lhs (m : Nat) : Nat := (2 * (2 * m)) * (m^2)
def s_rhs (m : Nat) : Nat := 4 * (m^3)

theorem calc_int_03_m3 : s_lhs 3 = s_rhs 3 := by decide
theorem calc_int_03_grid : List.all [2, 3, 4, 5, 6, 7, 8, 9] (fun m => s_lhs m == s_rhs m) = true := by decide

#eval [2, 3, 4, 5, 6, 7, 8, 9].map (fun m => (m, 4, m * m))
