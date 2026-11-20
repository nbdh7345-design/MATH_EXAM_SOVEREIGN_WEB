import Mathlib.Tactic
import Mathlib.Analysis.SpecialFunctions.Integrals.Basic
import Mathlib.Analysis.SpecialFunctions.Pow.Deriv
import Mathlib.Analysis.SpecialFunctions.Trigonometric.Deriv
import Mathlib.Analysis.SpecialFunctions.Log.Deriv
import Mathlib.Analysis.SpecificLimits.Basic
import Mathlib.Analysis.Calculus.Taylor
import Mathlib.Analysis.Calculus.LHopital
import Mathlib.Analysis.Calculus.Deriv.Pow
import Mathlib.MeasureTheory.Integral.IntegralEqImproper
import Mathlib.Topology.Algebra.InfiniteSum.Real
import Mathlib.LinearAlgebra.Matrix.Determinant.Basic
import Mathlib.LinearAlgebra.Matrix.Rank
import Mathlib.LinearAlgebra.Matrix.Charpoly.Basic
import Mathlib.LinearAlgebra.Matrix.PosDef
import Mathlib.Analysis.InnerProductSpace.GramSchmidtOrtho
import Mathlib.Analysis.Convex.Function
import Mathlib.Analysis.Convex.Deriv
import Mathlib.Topology.Bornology.Basic
import Mathlib.Topology.UniformSpace.UniformConvergence
import Mathlib.Order.LiminfLimsup
import Mathlib.Data.EReal.Basic
import Mathlib.Data.PNat.Basic
import Mathlib.Analysis.Calculus.Deriv.Inverse
import Mathlib.Topology.Order.IntermediateValue
import MathExam
set_option autoImplicit false

section Chk0

theorem eq_mp  (h_eq : ∀ A : Set ℝ, A.Nonempty → BddBelow A → (∃ i : ℝ, IsGLB A i) ∧ (∃ s : ℝ, IsLUB {y : ℝ | ∃ x ∈ A, y = -x} s) ∧ ∀ i s : ℝ, IsGLB A i → IsLUB {y : ℝ | ∃ x ∈ A, y = -x} s → i = -s) :
    ∀ A : Set ℝ, A.Nonempty → BddBelow A → ∃ a s : ℝ, IsGLB A a ∧ IsLUB {y : ℝ | ∃ x ∈ A, y = -x} s ∧ a = -s := by
  intro A hne hbdd
  obtain ⟨⟨i, hi⟩, ⟨s, hs⟩, hk⟩ := h_eq A hne hbdd
  exact ⟨i, s, hi, hs, hk i s hi hs⟩
end Chk0
section Chk1

theorem eq_mpr  (h_eq : ∀ A : Set ℝ, A.Nonempty → BddBelow A → ∃ a s : ℝ, IsGLB A a ∧ IsLUB {y : ℝ | ∃ x ∈ A, y = -x} s ∧ a = -s) :
    ∀ A : Set ℝ, A.Nonempty → BddBelow A → (∃ i : ℝ, IsGLB A i) ∧ (∃ s : ℝ, IsLUB {y : ℝ | ∃ x ∈ A, y = -x} s) ∧ ∀ i s : ℝ, IsGLB A i → IsLUB {y : ℝ | ∃ x ∈ A, y = -x} s → i = -s := by
  intro A hne hbdd
  obtain ⟨a, s, ha, hs, has⟩ := h_eq A hne hbdd
  refine ⟨⟨a, ha⟩, ⟨s, hs⟩, ?_⟩
  intro i s' hi hs'
  have hi' : i = a := hi.unique ha
  have hs'' : s' = s := hs'.unique hs
  rw [hi', hs'']
  exact has
end Chk1
section Chk2

theorem ctl_mp  (h_eq : True) :
    ∀ A : Set ℝ, A.Nonempty → BddBelow A → ∃ a s : ℝ, IsGLB A a ∧ IsLUB {y : ℝ | ∃ x ∈ A, y = -x} s ∧ a = -s := by
  intro A hne hbdd
  obtain ⟨⟨i, hi⟩, ⟨s, hs⟩, hk⟩ := h_eq A hne hbdd
  exact ⟨i, s, hi, hs, hk i s hi hs⟩
end Chk2
section Chk3

theorem ctl_mpr  (h_eq : True) :
    ∀ A : Set ℝ, A.Nonempty → BddBelow A → (∃ i : ℝ, IsGLB A i) ∧ (∃ s : ℝ, IsLUB {y : ℝ | ∃ x ∈ A, y = -x} s) ∧ ∀ i s : ℝ, IsGLB A i → IsLUB {y : ℝ | ∃ x ∈ A, y = -x} s → i = -s := by
  intro A hne hbdd
  obtain ⟨a, s, ha, hs, has⟩ := h_eq A hne hbdd
  refine ⟨⟨a, ha⟩, ⟨s, hs⟩, ?_⟩
  intro i s' hi hs'
  have hi' : i = a := hi.unique ha
  have hs'' : s' = s := hs'.unique hs
  rw [hi', hs'']
  exact has
end Chk3
