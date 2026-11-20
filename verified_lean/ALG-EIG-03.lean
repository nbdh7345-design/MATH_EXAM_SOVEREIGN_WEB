-- Core Lean 4 verification for ALG-EIG-03 (No Mathlib, No sorry)
def eigC1 (m : Nat) : Nat := m + 1
def eigC2 (m : Nat) : Nat := m + 3
def eigC3 (m : Nat) : Nat := 3 * m + 1

def sumSqEigC (m : Nat) : Nat :=
  eigC1 m * eigC1 m + eigC2 m * eigC2 m + eigC3 m * eigC3 m

def formulaC (m : Nat) : Nat := 11 * m * m + 14 * m + 11

theorem alg_eig_03_m3 : sumSqEigC 3 = 152 := by rfl
theorem alg_eig_03_formula_m3 : sumSqEigC 3 = formulaC 3 := by decide
theorem alg_eig_03_strict_order_m3 : eigC1 3 < eigC2 3 ∧ eigC2 3 < eigC3 3 := by decide

theorem alg_eig_03_grid_check :
    (List.range 8 |>.map (fun i => i + 2) |>.all (fun m =>
      sumSqEigC m == formulaC m &&
      eigC1 m < eigC2 m &&
      eigC2 m < eigC3 m)) = true := by decide

#eval (eigC1 3, eigC2 3, eigC3 3, sumSqEigC 3, formulaC 3)
