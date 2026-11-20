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

theorem equiv_0_1  :
    (∀ A : Set ℝ, A.Nonempty → BddBelow A → (∃ i : ℝ, IsGLB A i) ∧ (∃ s : ℝ, IsLUB {y : ℝ | ∃ x ∈ A, y = -x} s) ∧ ∀ i s : ℝ, IsGLB A i → IsLUB {y : ℝ | ∃ x ∈ A, y = -x} s → i = -s) ↔ (∀ A : Set ℝ, A.Nonempty → BddBelow A → ∃ a s : ℝ, IsGLB A a ∧ IsLUB {y : ℝ | ∃ x ∈ A, y = -x} s ∧ a = -s) := by
  first
    | exact Iff.rfl
    | (simp; done)
    | (constructor <;> intro h <;> first | (simpa using h) | (simp_all; done) | (linarith; done) | (nlinarith; done) | (norm_num at *; done) | (tauto; done) | (aesop; done))
end Chk0
section Chk1

theorem equiv_0_2  :
    (∀ A : Set ℝ, A.Nonempty → BddBelow A → (∃ i : ℝ, IsGLB A i) ∧ (∃ s : ℝ, IsLUB {y : ℝ | ∃ x ∈ A, y = -x} s) ∧ ∀ i s : ℝ, IsGLB A i → IsLUB {y : ℝ | ∃ x ∈ A, y = -x} s → i = -s) ↔ (∀ A : Set ℝ, A.Nonempty → BddBelow A → (∃ a : ℝ, IsGLB A a) ∧ ∀ a : ℝ, IsGLB A a ↔ IsLUB {y : ℝ | ∃ x ∈ A, y = -x} (-a)) := by
  first
    | exact Iff.rfl
    | (simp; done)
    | (constructor <;> intro h <;> first | (simpa using h) | (simp_all; done) | (linarith; done) | (nlinarith; done) | (norm_num at *; done) | (tauto; done) | (aesop; done))
end Chk1
section Chk2

theorem equiv_1_2  :
    (∀ A : Set ℝ, A.Nonempty → BddBelow A → ∃ a s : ℝ, IsGLB A a ∧ IsLUB {y : ℝ | ∃ x ∈ A, y = -x} s ∧ a = -s) ↔ (∀ A : Set ℝ, A.Nonempty → BddBelow A → (∃ a : ℝ, IsGLB A a) ∧ ∀ a : ℝ, IsGLB A a ↔ IsLUB {y : ℝ | ∃ x ∈ A, y = -x} (-a)) := by
  first
    | exact Iff.rfl
    | (simp; done)
    | (constructor <;> intro h <;> first | (simpa using h) | (simp_all; done) | (linarith; done) | (nlinarith; done) | (norm_num at *; done) | (tauto; done) | (aesop; done))
end Chk2
