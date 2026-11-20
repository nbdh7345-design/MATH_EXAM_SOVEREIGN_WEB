-- Lean 4 Core verification for ALG-DET-03 (No Mathlib, No sorry)
def detA3 (m : Int) : Int :=
  1 * (m * (m * m) - 1 * 1) - 1 * (1 * (m * m) - 1 * 1) + 1 * (1 * 1 - m * 1)

def sumAdjA3 (m : Int) : Int :=
  let c11 := m * m * m - 1
  let c12 := 1 - m * m
  let c13 := 1 - m
  let c21 := 1 - m * m
  let c22 := m * m - 1
  let c23 := 0
  let c31 := 1 - m
  let c32 := 0
  let c33 := m - 1
  c11 + c12 + c13 + c21 + c22 + c23 + c31 + c32 + c33

def factoredDet3 (m : Int) : Int :=
  (m - 1) * (m - 1) * (m + 1)

theorem alg_det_03_m3 : detA3 3 = 16 ∧ sumAdjA3 3 = 16 := by decide

theorem alg_det_03_grid_verified :
    (List.range 8).all (fun k =>
      let m : Int := Int.ofNat (k + 2)
      (detA3 m == factoredDet3 m) && (sumAdjA3 m == detA3 m)) = true := by decide

#eval (List.range 8).map (fun k =>
  let m : Int := Int.ofNat (k + 2)
  (m, detA3 m, sumAdjA3 m, factoredDet3 m))
