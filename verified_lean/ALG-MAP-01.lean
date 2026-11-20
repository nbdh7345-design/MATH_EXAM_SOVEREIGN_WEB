-- Lean 4 Formal Verification for ALG-MAP-01 (No Mathlib, Zero Sorry)
def det3 (a11 a12 a13 a21 a22 a23 a31 a32 a33 : Int) : Int :=
  a11 * (a22 * a33 - a23 * a32)
  - a12 * (a21 * a33 - a23 * a31)
  + a13 * (a21 * a32 - a22 * a31)

def kTarget (m : Int) : Int := m * m + m - 1

def detMap01 (m k : Int) : Int :=
  det3 1 1 m 2 3 (3 * m + 1) 1 m k

theorem alg_map_01_m3 : detMap01 3 (kTarget 3) = 0 ∧ kTarget 3 = 11 := by decide
theorem alg_map_01_grid : (List.range 8).all (fun i =>
  let m := Int.ofNat (i + 2)
  detMap01 m (kTarget m) == 0) = true := by decide

#eval (kTarget 3, detMap01 3 (kTarget 3))
