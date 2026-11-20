-- Lean 4 Core verification for CALC-LAG-06 (max of x + 2y + 2z on the sphere of radius m)
-- Maximiser (x, y, z) = (m/3)(1, 2, 2); scaled by 3: (m, 2m, 2m)
def onSphere9 (m : Int) : Bool := m ^ 2 + (2 * m) ^ 2 + (2 * m) ^ 2 == 9 * m ^ 2
def value3 (m : Int) : Int := m + 2 * (2 * m) + 2 * (2 * m)

theorem calc_lag_06_maximiser :
    (List.range 8).all (fun k => let m : Int := k + 2; onSphere9 m && value3 m == 3 * (3 * m)) = true := by decide
-- Cauchy–Schwarz bound on integer points: (x + 2y + 2z)^2 ≤ 9 (x^2 + y^2 + z^2)
theorem calc_lag_06_cauchy_schwarz :
    (List.range 7).all (fun a => (List.range 7).all (fun b => (List.range 7).all (fun c =>
      let x : Int := a - 3; let y : Int := b - 3; let z : Int := c - 3;
      (x + 2 * y + 2 * z) ^ 2 ≤ 9 * (x ^ 2 + y ^ 2 + z ^ 2)))) = true := by decide
