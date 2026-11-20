-- Core Lean 4 verification for ALG-EIG-01 (No Mathlib, No sorry)
def traceA (m : Nat) : Nat := 4 * m
def detA (m : Nat) : Nat := 3 * m * m
def eig1 (m : Nat) : Nat := m
def eig2 (m : Nat) : Nat := 3 * m

def sumSqEigDirect (m : Nat) : Nat := eig1 m * eig1 m + eig2 m * eig2 m
def sumSqEigViete (m : Nat) : Nat := traceA m * traceA m - 2 * detA m
def targetFormula (m : Nat) : Nat := 10 * m * m

theorem alg_eig_01_m3_eq : sumSqEigDirect 3 = 90 := by rfl
theorem alg_eig_01_viete_m3 : sumSqEigViete 3 = targetFormula 3 := by decide

theorem alg_eig_01_grid_check :
    (List.range 8 |>.map (fun i => i + 2) |>.all (fun m =>
      sumSqEigDirect m == targetFormula m &&
      sumSqEigViete m == targetFormula m &&
      eig1 m + eig2 m == traceA m &&
      eig1 m * eig2 m == detA m)) = true := by decide

#eval (sumSqEigDirect 3, sumSqEigViete 3, targetFormula 3)
