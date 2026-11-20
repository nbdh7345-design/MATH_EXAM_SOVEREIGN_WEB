-- Lean 4 Formal Verification for ALG-MAP-03 (No Mathlib, Zero Sorry)
def fMap03 (m x1 x2 x3 x4 : Int) : Int × Int × Int :=
  (x1 + 2 * x2 - x3 + m * x4,
   2 * x1 + 5 * x2 + (2 * m + 1) * x4,
   (m + 2) * x1 + (2 * m + 5) * x2 - m * x3 + (m * m + 2 * m + 1) * x4)

def lambdaTarget (m : Int) : Int := m + 2

theorem alg_map_03_ker_and_im_m3 :
    fMap03 3 5 (-2) 1 0 = (0, 0, 0)
    ∧ fMap03 3 (2 - 3) (-1) 0 1 = (0, 0, 0)
    ∧ fMap03 3 1 0 0 0 = (1, 2, lambdaTarget 3) := by decide

theorem alg_map_03_grid : (List.range 8).all (fun i =>
  let m := Int.ofNat (i + 2)
  (fMap03 m 5 (-2) 1 0 == (0, 0, 0))
  && (fMap03 m (2 - m) (-1) 0 1 == (0, 0, 0))
  && (fMap03 m 1 0 0 0 == (1, 2, lambdaTarget m))) = true := by decide

#eval (lambdaTarget 3, fMap03 3 (2 - 3) (-1) 0 1, fMap03 3 1 0 0 0)
