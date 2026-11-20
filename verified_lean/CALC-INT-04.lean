-- Lean 4 Core verification for CALC-INT-04 (Newton–Leibniz for 2x + 1)
def F (x : Nat) : Nat := x ^ 2 + x
def options (m : Nat) : List Nat := [m ^ 2 + m, m ^ 2, 2 * m ^ 2 + m, m ^ 2 + 2 * m]

-- F(x + 1) - F(x) = 2x + 2 = ∫_x^{x+1} (2t + 1) dt, cộng dồn trên các đoạn đơn vị
theorem calc_int_04_telescoping :
    (List.range 20).all (fun x => F (x + 1) - F x == 2 * x + 2) = true := by decide
theorem calc_int_04_answer :
    (List.range 8).all (fun k => let m := k + 2; F m - F 0 == m ^ 2 + m && (options m).Nodup) = true := by decide
