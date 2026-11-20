-- Lean 4 Core verification for ALG-VEC-03 (Transition Matrix & Coordinate Change)
def detTransition (m : Int) : Int :=
  1 * (1 * 2 - (m + 1) * 1) - 0 * (1 * 2 - (m + 1) * 0) + m * (1 * 1 - 1 * 0)

def wCoordsB (m : Int) : Int × Int × Int :=
  (1 + 0 + m, 1 + 1 + (m + 1), 0 + 1 + 2)

def sumCoordsB (m : Int) : Int :=
  (m + 1) + (m + 3) + 3

theorem alg_vec_03_det (m : Int) : detTransition m = 1 := by unfold detTransition; omega
theorem alg_vec_03_sum (m : Int) : sumCoordsB m = 2 * m + 7 := by unfold sumCoordsB; omega
theorem alg_vec_03_m3 : sumCoordsB 3 = 13 := by decide

#eval (detTransition 3, wCoordsB 3, sumCoordsB 3)
