-- VAC: FR09 (mau_thuan), Lean 4 + Mathlib; dòng khai báo định lý do hệ thống viết.
import Mathlib.Data.Real.Basic
import Mathlib.Tactic.Positivity
import Mathlib.Tactic.Linarith
import Mathlib.Analysis.SpecialFunctions.Exp
import MathExam
set_option autoImplicit false
set_option maxHeartbeats 400000


theorem fr08_vacuity :
    ∀ x : ℝ, x > 1 → x ^ 2 > 1 := by
  intro x h
  exfalso
  linarith

#print axioms fr08_vacuity
