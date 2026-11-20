-- Core Lean 4 verification for CALC-SER-02 (Radius of Convergence R(m) = m*(m+1))
def radiusConvergence (m : Nat) : Nat := m * (m + 1)
def optionC (m : Nat) : Nat := m + 1
def optionD (m : Nat) : Nat := m * m

theorem calc_ser_02_default_m3 : radiusConvergence 3 = 12 := by rfl

theorem calc_ser_02_strict_ordering :
    (List.range 8 |>.map (fun i =>
      let m := i + 2
      (optionC m < optionD m) && (optionD m < radiusConvergence m))).all (· == true) = true := by
  decide

theorem calc_ser_02_algebraic_grid :
    (List.range 8 |>.map (fun i => let m := i + 2; radiusConvergence m == m * m + m)).all (· == true) = true := by
  decide

theorem calc_ser_02_lower_bound (m : Nat) (h : m ≥ 2) : optionC m ≥ 3 := by
  unfold optionC; omega

#eval (List.range 8).map (fun i => let m := i + 2; (m, radiusConvergence m))
