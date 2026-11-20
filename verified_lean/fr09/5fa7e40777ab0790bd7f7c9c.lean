-- EQ: FR09 (dung), Lean 4 + Mathlib; dòng khai báo định lý do hệ thống viết.
import Mathlib.Data.Real.Basic
import Mathlib.Tactic.Positivity
import Mathlib.Tactic.Linarith
import Mathlib.Analysis.SpecialFunctions.Exp
import MathExam
set_option autoImplicit false
set_option maxHeartbeats 400000


theorem fr08_eq_mpr (m : ℕ) (hm_lo : 2 ≤ m) (hm_hi : m ≤ 9) (h_eq : 2 ≤ (m : ℝ)) :
    (m : ℝ) ≥ 2 := by
  exact h_eq

#print axioms fr08_eq_mpr
