-- VAC: FR09 (mau_thuan), Lean 4 + Mathlib; dòng khai báo định lý do hệ thống viết.
import Mathlib.Data.Real.Basic
import Mathlib.Tactic.Positivity
import Mathlib.Tactic.Linarith
import Mathlib.Analysis.SpecialFunctions.Exp
import MathExam
set_option autoImplicit false
set_option maxHeartbeats 400000


theorem fr08_vacuity :
    ∀ f : ℝ → ℝ, (∀ x, f x ^ 2 < 0) → f 0 = 1 := by
  intro f hf
  exfalso
  have h0 := hf 0
  nlinarith [sq_nonneg (f 0)]

#print axioms fr08_vacuity
