-- Lean 4 Core verification for CALC-LIM-05 (Maclaurin coefficient m^3 / 3!)
def fact : Nat → Nat
  | 0 => 1
  | n + 1 => (n + 1) * fact n
def options6 (m : Nat) : List Nat := [2 * m ^ 3, 3 * m ^ 3, m ^ 3, m ^ 2]

theorem calc_lim_05_factorial : fact 3 = 6 := by decide
theorem calc_lim_05_distinct :
    (List.range 8).all (fun k => let m := k + 2; (options6 m).Nodup) = true := by decide
