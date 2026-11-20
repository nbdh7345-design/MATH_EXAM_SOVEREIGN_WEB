-- Lean 4 Core verification for CALC-LAG-04 (stationary point of L = xy + λ(m - x - y)), scaled by 2
def x2 (m : Int) : Int := m
def y2 (m : Int) : Int := m
def lam2 (m : Int) : Int := m

theorem calc_lag_04_stationary :
    (List.range 8).all (fun k => let m : Int := k + 2;
      y2 m - lam2 m == 0 && x2 m - lam2 m == 0 && 2 * m - x2 m - y2 m == 0) = true := by decide
theorem calc_lag_04_distinct :
    (List.range 8).all (fun k => let m : Int := k + 2; [4 * m, 2 * m, m, 8 * m].Nodup) = true := by decide
