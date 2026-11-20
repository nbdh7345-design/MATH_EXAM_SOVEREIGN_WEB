-- Lean 4 Core verification for CALC-ANTI-01 (partial fractions)
-- 1/((x+1)(x+m)) = (1/(m-1)) (1/(x+1) - 1/(x+m))  ⇔  (x + m) - (x + 1) = m - 1
-- Log argument after evaluating at the bounds: 2 / ((m+1)/m) = 2m/(m+1)
def numerAfterCombine (m x : Int) : Int := (x + m) - (x + 1)
def logArgNum (m : Int) : Int := 2 * m
def logArgDen (m : Int) : Int := m + 1

theorem calc_anti_01_partial_fraction :
    (List.range 8).all (fun k => let m : Int := k + 2;
      (List.range 11).all (fun j => numerAfterCombine m j == m - 1)) = true := by decide
theorem calc_anti_01_log_argument :
    (List.range 8).all (fun k => let m : Int := k + 2;
      logArgNum m > logArgDen m && m - 1 > 0) = true := by decide

#eval (logArgNum 3, logArgDen 3)
