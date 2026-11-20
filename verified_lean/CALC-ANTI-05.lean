-- Lean 4 Core verification for CALC-ANTI-05
-- G'(x) = (1 - cos(m x)) / m ; at x = π/m: cos π = -1  =>  G' = 2/m. Options scaled by m^2.
def cosPi : Int := -1
def numerAtPi : Int := 1 - cosPi

theorem calc_anti_05_value : numerAtPi = 2 := by decide
theorem calc_anti_05_distinct :
    (List.range 8).all (fun k => let m : Int := k + 2; [m, 2 * m, 1, 2 * m ^ 2].Nodup) = true := by decide
