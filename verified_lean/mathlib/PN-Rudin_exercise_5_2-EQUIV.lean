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
open Set
theorem equiv_0_1  :
    (∀ a b : ℝ, a < b → ∀ f : ℝ → ℝ, (∀ x ∈ Set.Ioo a b, DifferentiableAt ℝ f x ∧ 0 < deriv f x) → ∀ g : ℝ → ℝ, (∀ x ∈ Set.Ioo a b, g (f x) = x) → (∀ y ∈ f '' Set.Ioo a b, f (g y) = y) → StrictMonoOn f (Set.Ioo a b) ∧ ∀ x ∈ Set.Ioo a b, DifferentiableAt ℝ g (f x) ∧ deriv g (f x) = 1 / deriv f x) ↔ (∀ f g : ℝ → ℝ, ∀ a b : ℝ, a < b → (∀ x ∈ Set.Ioo a b, DifferentiableAt ℝ f x ∧ 0 < deriv f x) → (∀ x ∈ Set.Ioo a b, g (f x) = x) → (∀ y ∈ f '' Set.Ioo a b, f (g y) = y) → StrictMonoOn f (Set.Ioo a b) ∧ ∀ x ∈ Set.Ioo a b, DifferentiableAt ℝ g (f x) ∧ deriv g (f x) = 1 / deriv f x) := by
  first
    | exact Iff.rfl
    | (simp; done)
    | (constructor <;> intro h <;> first | (simpa using h) | (simp_all; done) | (linarith; done) | (nlinarith; done) | (norm_num at *; done) | (tauto; done) | (aesop; done))
end Chk0
section Chk1
open Topology
theorem equiv_0_2  :
    (∀ a b : ℝ, a < b → ∀ f : ℝ → ℝ, (∀ x ∈ Set.Ioo a b, DifferentiableAt ℝ f x ∧ 0 < deriv f x) → ∀ g : ℝ → ℝ, (∀ x ∈ Set.Ioo a b, g (f x) = x) → (∀ y ∈ f '' Set.Ioo a b, f (g y) = y) → StrictMonoOn f (Set.Ioo a b) ∧ ∀ x ∈ Set.Ioo a b, DifferentiableAt ℝ g (f x) ∧ deriv g (f x) = 1 / deriv f x) ↔ (∀ a b : ℝ, a < b → ∀ f : ℝ → ℝ, (∀ x ∈ Set.Ioo a b, DifferentiableAt ℝ f x ∧ 0 < deriv f x) → (StrictMonoOn f (Set.Ioo a b) ∧ ∀ g : ℝ → ℝ, (∀ x ∈ Set.Ioo a b, g (f x) = x) → ∀ x ∈ Set.Ioo a b, HasDerivWithinAt g (1 / deriv f x) (f '' Set.Ioo a b) (f x) ∧ derivWithin g (f '' Set.Ioo a b) (f x) = 1 / deriv f x)) := by
  first
    | exact Iff.rfl
    | (simp; done)
    | (constructor <;> intro h <;> first | (simpa using h) | (simp_all; done) | (linarith; done) | (nlinarith; done) | (norm_num at *; done) | (tauto; done) | (aesop; done))
end Chk1
section Chk2
open Set Topology
theorem equiv_1_2  :
    (∀ f g : ℝ → ℝ, ∀ a b : ℝ, a < b → (∀ x ∈ Set.Ioo a b, DifferentiableAt ℝ f x ∧ 0 < deriv f x) → (∀ x ∈ Set.Ioo a b, g (f x) = x) → (∀ y ∈ f '' Set.Ioo a b, f (g y) = y) → StrictMonoOn f (Set.Ioo a b) ∧ ∀ x ∈ Set.Ioo a b, DifferentiableAt ℝ g (f x) ∧ deriv g (f x) = 1 / deriv f x) ↔ (∀ a b : ℝ, a < b → ∀ f : ℝ → ℝ, (∀ x ∈ Set.Ioo a b, DifferentiableAt ℝ f x ∧ 0 < deriv f x) → (StrictMonoOn f (Set.Ioo a b) ∧ ∀ g : ℝ → ℝ, (∀ x ∈ Set.Ioo a b, g (f x) = x) → ∀ x ∈ Set.Ioo a b, HasDerivWithinAt g (1 / deriv f x) (f '' Set.Ioo a b) (f x) ∧ derivWithin g (f '' Set.Ioo a b) (f x) = 1 / deriv f x)) := by
  first
    | exact Iff.rfl
    | (simp; done)
    | (constructor <;> intro h <;> first | (simpa using h) | (simp_all; done) | (linarith; done) | (nlinarith; done) | (norm_num at *; done) | (tauto; done) | (aesop; done))
end Chk2
