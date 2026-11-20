-- Lean 4 Core verification for CALC-INT-02: 2nd derivative coefficient and distinctness
def leibniz_num (k : Nat) : Nat :=
  match k with
  | 0 => 1
  | n + 1 => (n + 1) * leibniz_num n

theorem calc_int_02_factorial_2 : leibniz_num 2 = 2 := by rfl
theorem calc_int_02_distinct_options :
  List.all [2, 3, 4, 5, 6, 7, 8, 9] (fun m => (2 * (m + 1)^3 != 2 * m^3) && (2 * m^2 != 2 * m^3)) = true := by decide

#eval [2, 3, 4, 5, 6, 7, 8, 9].map (fun m => (m, leibniz_num 2, m^3))
