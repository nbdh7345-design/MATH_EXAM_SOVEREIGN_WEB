-- Lean 4 Core verification for CALC-MUL-04 (partial derivatives at (1, 1))
def fx (m : Nat) (x : Nat) : Nat := m * x ^ (m - 1)
def fy (m : Nat) (y : Nat) : Nat := 2 * m * y

theorem calc_mul_04_answer :
    (List.range 8).all (fun k => let m := k + 2; fx m 1 + fy m 1 == 3 * m) = true := by decide
theorem calc_mul_04_distinct :
    (List.range 8).all (fun k => let m := k + 2; [2 * m, 3 * m, m, 4 * m].Nodup) = true := by decide
