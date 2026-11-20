-- Lean 4 Core verification for ALG-DET-02 (No Mathlib, No sorry)
def detA2 (m : Int) : Int :=
  m * (m * m - 1 * 1) - 1 * (1 * m - 1 * 0) + 0 * (1 * 1 - m * 0)

def traceAdjA2 (m : Int) : Int :=
  let c11 := m * m - 1
  let c22 := m * m
  let c33 := m * m - 1
  c11 + c22 + c33

def totalS2 (m : Int) : Int :=
  m * m * m + 3 * m * m - 2 * m - 2

theorem alg_det_02_m3 : detA2 3 + traceAdjA2 3 = 46 := by decide

theorem alg_det_02_grid_verified :
    (List.range 8).all (fun k =>
      let m : Int := Int.ofNat (k + 2)
      (detA2 m + traceAdjA2 m) == totalS2 m) = true := by decide

#eval (List.range 8).map (fun k =>
  let m : Int := Int.ofNat (k + 2)
  (m, detA2 m, traceAdjA2 m, totalS2 m))
