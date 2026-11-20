import Mathlib.Data.Real.Basic
import Mathlib.Tactic.Positivity
import Mathlib.Tactic.Linarith
import Mathlib.Analysis.SpecialFunctions.Exp
import MathExam
set_option autoImplicit false

section Chk0

theorem vacuity_llm  :
    ∀ x : ℝ, x > 1 → x ^ 2 > 1 := by
  intro x h
  exfalso
  linarith
end Chk0
