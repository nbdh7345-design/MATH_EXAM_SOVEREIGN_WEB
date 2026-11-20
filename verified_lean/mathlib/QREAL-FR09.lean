-- QREAL: FR09 (dung), Lean 4 + Mathlib; dòng khai báo định lý do hệ thống viết.
import Mathlib.Data.Real.Basic
import Mathlib.Tactic.Positivity
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.Ring
import MathExam
set_option autoImplicit false
set_option maxHeartbeats 400000


theorem exam_answer (m : ℕ) (hm_lo : 2 ≤ m) (hm_hi : m ≤ 9) :
    ((m : ℝ)) ^ 2 ≥ 4 := by
  have h : (2 : ℝ) ≤ m := by exact_mod_cast hm_lo
  nlinarith

#print axioms exam_answer
