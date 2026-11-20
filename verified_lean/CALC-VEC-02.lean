-- Lean 4 Core Verification for CALC-VEC-02 (Conservative Field Potential in R^3)
def potentialU (m x y z : Nat) : Nat :=
  m * x * x * y + x * z * z + y * y * z + m * z * z * z

def workAB (m : Nat) : Nat :=
  potentialU m 1 2 1 - potentialU m 0 0 0

theorem calc_vec_02_formula (m : Nat) : workAB m = 3 * m + 5 := by
  simp [workAB, potentialU]
  omega

theorem calc_vec_02_m3 : workAB 3 = 14 := by
  decide

theorem calc_vec_02_grid :
    (List.range 8).all (fun k =>
      let m := k + 2
      workAB m == 3 * m + 5) = true := by
  decide

#eval workAB 3
