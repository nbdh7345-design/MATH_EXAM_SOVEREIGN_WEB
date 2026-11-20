-- Core Lean 4 verification for ALG-EIG-02 (No Mathlib, No sorry)
def eigB1 (m : Nat) : Nat := m
def eigB2 (m : Nat) : Nat := m + 3
def eigB3 (m : Nat) : Nat := 2 * m

def traceB (m : Nat) : Nat := (m + 1) + (m + 2) + 2 * m
def detB (m : Nat) : Nat := 2 * m * m * m + 6 * m * m
def invT (m : Nat) : Nat := eigB1 m * eigB2 m * eigB3 m + (eigB1 m + eigB2 m + eigB3 m)
def formulaB (m : Nat) : Nat := 2 * m * m * m + 6 * m * m + 4 * m + 3

theorem alg_eig_02_m3 : invT 3 = 123 := by rfl
theorem alg_eig_02_formula_m3 : invT 3 = formulaB 3 := by decide

theorem alg_eig_02_grid_check :
    (List.range 8 |>.map (fun i => i + 2) |>.all (fun m =>
      invT m == formulaB m &&
      eigB1 m + eigB2 m + eigB3 m == traceB m &&
      eigB1 m * eigB2 m * eigB3 m == detB m)) = true := by decide

#eval (invT 3, formulaB 3, traceB 3, detB 3)
