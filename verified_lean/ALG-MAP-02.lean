-- Lean 4 Formal Verification for ALG-MAP-02 (No Mathlib, Zero Sorry)
def fMap02 (m x1 x2 x3 : Int) : Int × Int × Int :=
  (x1 + 2 * x2 + m * x3,
   2 * x1 + 5 * x2 + (3 * m + 1) * x3,
   3 * x1 + 7 * x2 + (4 * m + 1) * x3)

def aKer (m : Int) : Int := m + 2
def bKer (m : Int) : Int := -(m + 1)
def qTarget (m : Int) : Int := 2 * (aKer m) - (bKer m)

theorem alg_map_02_m3 :
    fMap02 3 (aKer 3) (bKer 3) 1 = (0, 0, 0) ∧ qTarget 3 = 14 := by decide

theorem alg_map_02_grid : (List.range 8).all (fun i =>
  let m := Int.ofNat (i + 2)
  (fMap02 m (aKer m) (bKer m) 1 == (0, 0, 0)) && (qTarget m == 3 * m + 5)) = true := by decide

#eval (aKer 3, bKer 3, qTarget 3)
