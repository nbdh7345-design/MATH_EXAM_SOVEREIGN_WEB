-- Lean 4 Formal Verification for ALG-SYS-01 (Core Lean 4)
def det3 (a11 a12 a13 a21 a22 a23 a31 a32 a33 : Int) : Int :=
  a11 * (a22 * a33 - a23 * a32) - a12 * (a21 * a33 - a23 * a31) + a13 * (a21 * a32 - a22 * a31)

theorem cramer_det_is_one : det3 1 1 1 1 2 3 1 3 6 = 1 := by decide

theorem alg_sys_01_m3 :
  let m : Int := 3
  let x : Int := m
  let y : Int := 2 * m
  let z : Int := 3 * m
  (x + y + z = 6 * m) ∧ (x + 2 * y + 3 * z = 14 * m) ∧ (x + 3 * y + 6 * z = 25 * m) ∧ (2 * x + y + z = 7 * m) := by decide

#eval det3 1 1 1 1 2 3 1 3 6
