-- Lean 4 Core verification for ALG-QUAD-01 (No Mathlib, No sorry)
def delta1 (_m : Int) : Int := 2
def delta2 (m : Int) : Int := 2 * (m + 2) - 2 * 2
def delta3 (m : Int) : Int := (m + 1) * (delta2 m) - 2 * 1
def target_delta3 (m : Int) : Int := 2 * m * m + 2 * m - 2

theorem delta2_identity (m : Int) : delta2 m = 2 * m := by
  unfold delta2
  omega

theorem delta3_at_default : delta3 4 = target_delta3 4 := by rfl

theorem sylvester_pos_at_default :
    delta1 4 > 0 ∧ delta2 4 > 0 ∧ delta3 4 > 0 := by decide

#eval (delta1 4, delta2 4, delta3 4, target_delta3 4)
