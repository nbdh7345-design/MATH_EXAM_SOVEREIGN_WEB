-- Lean 4 Core verification for ALG-QUAD-02 (No Mathlib, No sorry)
def q2_delta1 : Int := 1
def q2_delta2 : Int := 1 * 5 - 2 * 2
def q2_delta3 (m k : Int) : Int := k - m * m
def k_min (m : Int) : Int := m * m + 1

theorem q2_delta2_pos : q2_delta2 = 1 := by rfl

theorem q2_delta3_at_kmin (m : Int) : q2_delta3 m (k_min m) = 1 := by
  unfold q2_delta3 k_min
  omega

theorem q2_sylvester_at_default :
    q2_delta1 > 0 ∧ q2_delta2 > 0 ∧ q2_delta3 4 (k_min 4) > 0 := by decide

#eval (q2_delta1, q2_delta2, k_min 4, q2_delta3 4 (k_min 4))
