-- Lean 4 Core verification for CALC-MV2-01 (chain rule)
-- z(x, 1) = (x + m)^2 (m x - 1) = m x^3 + (2m^2 - 1) x^2 + (m^3 - 2m) x - m^2
-- => z_x(1, 1) = 3m + 2(2m^2 - 1) + (m^3 - 2m)
def zAlongX (m x : Int) : Int := (x + m) ^ 2 * (m * x - 1)
def zExpanded (m x : Int) : Int := m * x ^ 3 + (2 * m ^ 2 - 1) * x ^ 2 + (m ^ 3 - 2 * m) * x - m ^ 2
def zxAt11 (m : Int) : Int := 3 * m + 2 * (2 * m ^ 2 - 1) + (m ^ 3 - 2 * m)
def chainRule (m : Int) : Int := 2 * (m + 1) * (m - 1) * 1 + (m + 1) ^ 2 * m
def options (m : Int) : List Int :=
  [(m + 1) * (m ^ 2 + 3 * m - 2), (m + 1) * (m ^ 2 + m - 2), (m + 1) * (m ^ 2 + 3 * m), 2 * (m + 1) * (m - 1)]

theorem calc_mv2_01_expand :
    (List.range 8).all (fun k => let m : Int := k + 2;
      (List.range 9).all (fun j => let x : Int := j - 4; zAlongX m x == zExpanded m x)) = true := by decide
theorem calc_mv2_01_value :
    (List.range 8).all (fun k => let m : Int := k + 2;
      zxAt11 m == chainRule m && chainRule m == (m + 1) * (m ^ 2 + 3 * m - 2) && (options m).Nodup) = true := by
  decide

#eval chainRule 3
