import Mathlib.Data.Real.Basic
import Mathlib.Tactic.Positivity
import Mathlib.Tactic.Linarith
import Mathlib.Analysis.SpecialFunctions.Exp
import MathExam
set_option autoImplicit false

section Chk0

theorem vacuity_0  :
    ∀ a b : ℝ, a < b → b < a → a = 0 := by
  intros
  exfalso
  first
    | (simp_all; done)
    | (linarith; done)
    | (nlinarith; done)
    | (norm_num at *; done)
    | (tauto; done)
    | (aesop; done)
end Chk0
section Chk1

theorem vacuity_1  :
    ∀ x : ℝ, Real.exp x < 0 → x = 7 := by
  intros
  exfalso
  first
    | (simp_all; done)
    | (linarith; done)
    | (nlinarith; done)
    | (norm_num at *; done)
    | (tauto; done)
    | (aesop; done)
end Chk1
section Chk2

theorem vacuity_2  :
    ∀ f : ℝ → ℝ, (∀ x, f x ^ 2 < 0) → f 0 = 1 := by
  intros
  exfalso
  first
    | (simp_all; done)
    | (linarith; done)
    | (nlinarith; done)
    | (norm_num at *; done)
    | (tauto; done)
    | (aesop; done)
end Chk2
section Chk3

theorem vacuity_3  :
    ∀ x : ℝ, x > 1 → x ^ 2 > 1 := by
  intros
  exfalso
  first
    | (simp_all; done)
    | (linarith; done)
    | (nlinarith; done)
    | (norm_num at *; done)
    | (tauto; done)
    | (aesop; done)
end Chk3
section Chk4

theorem vacuity_4  :
    ∀ x : ℝ, x > 1 → x ^ 2 > 1 := by
  intros
  exfalso
  first
    | (simp_all; done)
    | (linarith; done)
    | (nlinarith; done)
    | (norm_num at *; done)
    | (tauto; done)
    | (aesop; done)
end Chk4
