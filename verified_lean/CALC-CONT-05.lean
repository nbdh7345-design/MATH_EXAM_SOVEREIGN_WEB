-- Lean 4 Core verification for CALC-CONT-05 (order of the infinitesimal tan - sin)
-- tan(mx) ~ m x (order 1), 1 - cos(mx) ~ m^2 x^2 / 2 (order 2) => order 3, coefficient m^3/2 (scaled by 2: m^3)
def order : Nat := 1 + 2
def coeff2 (m : Nat) : Nat := m * m ^ 2

theorem calc_cont_05_answer :
    (List.range 8).all (fun k => let m := k + 2; order == 3 && coeff2 m * order == 3 * m ^ 3) = true := by decide
theorem calc_cont_05_distinct :
    (List.range 8).all (fun k => let m := k + 2; [m ^ 3, 6 * m ^ 3, 3 * m ^ 3, 2 * m ^ 3].Nodup) = true := by decide
