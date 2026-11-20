-- VAC: FR09 (mau_thuan), Lean 4 + Mathlib; dòng khai báo định lý do hệ thống viết.
import Mathlib.Data.Real.Basic
import Mathlib.Tactic.Positivity
import Mathlib.Tactic.Linarith
import Mathlib.Analysis.SpecialFunctions.Exp
import MathExam
set_option autoImplicit false
set_option maxHeartbeats 400000


theorem fr08_vacuity :
    ∀ x : ℝ, Real.exp x < 0 → x = 7 := by
  intro x h
  exfalso
  linarith [Real.exp_pos x]

#print axioms fr08_vacuity
