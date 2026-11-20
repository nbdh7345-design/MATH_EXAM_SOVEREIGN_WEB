import Mathlib.Data.Real.Basic
import Mathlib.Tactic.Positivity
import Mathlib.Tactic.Linarith
import MathExam
set_option autoImplicit false

section Chk0

theorem eq_mp (m : ℕ) (hm_lo : 2 ≤ m) (hm_hi : m ≤ 9) (h_eq : (m : ℝ) ≥ 2) :
    2 ≤ (m : ℝ) := by
  exact h_eq
end Chk0
section Chk1

theorem eq_mpr (m : ℕ) (hm_lo : 2 ≤ m) (hm_hi : m ≤ 9) (h_eq : 2 ≤ (m : ℝ)) :
    (m : ℝ) ≥ 2 := by
  exact h_eq
end Chk1
section Chk2

theorem ctl_mp (m : ℕ) (hm_lo : 2 ≤ m) (hm_hi : m ≤ 9) (h_eq : True) :
    2 ≤ (m : ℝ) := by
  exact h_eq
end Chk2
section Chk3

theorem ctl_mpr (m : ℕ) (hm_lo : 2 ≤ m) (hm_hi : m ≤ 9) (h_eq : True) :
    (m : ℝ) ≥ 2 := by
  exact h_eq
end Chk3
