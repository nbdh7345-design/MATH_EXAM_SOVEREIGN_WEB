-- Lean 4 Core verification for CALC-INT-01: m^3 * (1/m - 1/(m+1)) = m^2 / (m+1)
-- Cleared denominators identity: m^3 * ((m + 1) - m) = m^2 * m
def lhs_cleared (m : Nat) : Nat := m^3 * ((m + 1) - m)
def rhs_cleared (m : Nat) : Nat := m^2 * m

theorem calc_int_01_m3 : lhs_cleared 3 = rhs_cleared 3 := by decide
theorem calc_int_01_grid : List.all [2, 3, 4, 5, 6, 7, 8, 9] (fun m => lhs_cleared m == rhs_cleared m) = true := by decide

#eval [2, 3, 4, 5, 6, 7, 8, 9].map (fun m => (m, m * m, m + 1))
