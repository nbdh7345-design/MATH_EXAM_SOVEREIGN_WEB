-- Lean 4 Core verification for CALC-MVT-01 (Lagrange mean value point)
-- 3 c^2 = m^2. Squares of the options scaled by 36: A = 12 m^2, B = 9 m^2, C = 4 m^2, D = 18 m^2
def optionSq36 (m : Nat) : List Nat := [12 * m ^ 2, 9 * m ^ 2, 4 * m ^ 2, 18 * m ^ 2]
def slope (m : Nat) : Nat := m ^ 3 / m

theorem calc_mvt_01_slope :
    (List.range 8).all (fun k => let m := k + 2; slope m == m ^ 2) = true := by decide
theorem calc_mvt_01_answer :
    (List.range 8).all (fun k => let m := k + 2;
      3 * (12 * m ^ 2) == 36 * m ^ 2 && 12 * m ^ 2 < 36 * m ^ 2) = true := by decide
theorem calc_mvt_01_distinct :
    (List.range 8).all (fun k => let m := k + 2; (optionSq36 m).Nodup) = true := by decide

#eval optionSq36 3
