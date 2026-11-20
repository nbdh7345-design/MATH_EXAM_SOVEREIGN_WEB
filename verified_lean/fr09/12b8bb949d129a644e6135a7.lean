-- EQ: FR09 (dung), Lean 4 + Mathlib; dòng khai báo định lý do hệ thống viết.
import Mathlib.Data.Real.Basic
import Mathlib.Tactic.Positivity
import Mathlib.Tactic.Linarith
import Mathlib.Analysis.SpecialFunctions.Exp
import MathExam
set_option autoImplicit false
set_option maxHeartbeats 400000


theorem fr08_eq_mpr (h_eq : ∀ x : ℝ, 0 ≤ x ^ 2) :
    ∀ x : ℝ, x ^ 2 ≥ 0 := by
  intro x
  exact h_eq x

#print axioms fr08_eq_mpr
