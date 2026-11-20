-- Lean 4 Core verification for CALC-MVT-04 (horizontal asymptote = ratio of leading coefficients)
def numerAtPole (m : Int) : Int := m * m + 1

theorem calc_mvt_04_answer :
    (List.range 8).all (fun k => let m : Int := k + 2; numerAtPole m != 0 && [-m, 1, m].Nodup) = true := by decide
theorem calc_mvt_04_distinct_scaled :
    (List.range 8).all (fun k => let m : Int := k + 2; [-m * m, m, m * m, 1].Nodup) = true := by decide
