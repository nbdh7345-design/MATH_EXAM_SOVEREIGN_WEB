-- Lean 4 Core verification for CALC-MV2-05 (chain rule at t = 0, where e^u = e^0 = 1)
def dzdt0 (m : Nat) : Nat := m * 1 * 1 + 2 * 0 * 1 * 1

theorem calc_mv2_05_answer :
    (List.range 8).all (fun k => let m := k + 2; dzdt0 m == m && [1, m + 1, 2 * m, m].Nodup) = true := by decide
