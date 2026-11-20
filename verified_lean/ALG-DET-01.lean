-- Lean 4 Core verification for ALG-DET-01 (No Mathlib, No sorry)
def detA1 (m : Int) : Int :=
  m * (m * m - 1 * 1) - 1 * (1 * m - 1 * 1) + 1 * (1 * 1 - m * 1)

def closedForm1 (m : Int) : Int :=
  (m - 1) * (m - 1) * (m + 2)

theorem detA1_eq_closed_m3 : detA1 3 = closedForm1 3 := by rfl

theorem detA1_grid_verified :
    (List.range 8).all (fun k =>
      let m : Int := Int.ofNat (k + 2)
      detA1 m == closedForm1 m) = true := by decide

theorem detA1_positive_m3 : detA1 3 = 20 := by decide

#eval (List.range 8).map (fun k =>
  let m : Int := Int.ofNat (k + 2)
  (m, detA1 m, closedForm1 m))
