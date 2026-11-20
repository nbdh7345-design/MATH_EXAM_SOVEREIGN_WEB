-- Lean 4 Core verification for CALC-IMP-05 (comparison test: converges ⇔ m - a > 1)
def converges (m a : Nat) : Bool := decide (a + 1 < m)
def countConvergent (m : Nat) : Nat := ((List.range (m + 10)).filter (fun a => converges m a)).length
def options (m : Nat) : List Int := [m, (m : Int) - 2, m + 1, (m : Int) - 1]

theorem calc_imp_05_count :
    (List.range 8).all (fun k => let m := k + 2; countConvergent m == m - 1) = true := by decide
theorem calc_imp_05_distinct :
    (List.range 8).all (fun k => let m := k + 2; (options m).Nodup) = true := by decide
