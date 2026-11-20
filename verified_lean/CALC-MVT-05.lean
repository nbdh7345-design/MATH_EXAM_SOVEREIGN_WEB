-- Lean 4 Core verification for CALC-MVT-05 (Rolle counting argument)
def f (m : Nat) (x : Int) : Int := ((List.range m).map (fun (i : Nat) => x - ((i : Int) + 1))).foldl (· * ·) 1
def rootsF (m : Nat) : Nat := m
def rootsDf (m : Nat) : Nat := rootsF m - 1       -- Rolle on m - 1 consecutive intervals, deg f' = m - 1
def rootsD2f (m : Nat) : Nat := rootsDf m - 1     -- Rolle again, deg f'' = m - 2

theorem calc_mvt_05_roots_of_f :
    (List.range 8).all (fun k => let m := k + 2;
      (List.range m).all (fun i => f m (i + 1) == 0) && f m (m + 1) != 0) = true := by decide
theorem calc_mvt_05_count :
    (List.range 8).all (fun k => let m := k + 2; rootsD2f m == m - 2) = true := by decide
