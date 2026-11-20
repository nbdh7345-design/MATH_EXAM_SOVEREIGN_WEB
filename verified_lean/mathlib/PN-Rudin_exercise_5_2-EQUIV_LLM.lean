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
theorem eq_mp  (h_eq : ∀ a b : ℝ, a < b → ∀ f : ℝ → ℝ, (∀ x ∈ Set.Ioo a b, DifferentiableAt ℝ f x ∧ 0 < deriv f x) → ∀ g : ℝ → ℝ, (∀ x ∈ Set.Ioo a b, g (f x) = x) → (∀ y ∈ f '' Set.Ioo a b, f (g y) = y) → StrictMonoOn f (Set.Ioo a b) ∧ ∀ x ∈ Set.Ioo a b, DifferentiableAt ℝ g (f x) ∧ deriv g (f x) = 1 / deriv f x) :
    ∀ f g : ℝ → ℝ, ∀ a b : ℝ, a < b → (∀ x ∈ Set.Ioo a b, DifferentiableAt ℝ f x ∧ 0 < deriv f x) → (∀ x ∈ Set.Ioo a b, g (f x) = x) → (∀ y ∈ f '' Set.Ioo a b, f (g y) = y) → StrictMonoOn f (Set.Ioo a b) ∧ ∀ x ∈ Set.Ioo a b, DifferentiableAt ℝ g (f x) ∧ deriv g (f x) = 1 / deriv f x := by
  intro f g a b hab hd hg1 hg2; exact h_eq a b hab f hd g hg1 hg2
end Chk0
section Chk1
open Set
theorem eq_mpr  (h_eq : ∀ f g : ℝ → ℝ, ∀ a b : ℝ, a < b → (∀ x ∈ Set.Ioo a b, DifferentiableAt ℝ f x ∧ 0 < deriv f x) → (∀ x ∈ Set.Ioo a b, g (f x) = x) → (∀ y ∈ f '' Set.Ioo a b, f (g y) = y) → StrictMonoOn f (Set.Ioo a b) ∧ ∀ x ∈ Set.Ioo a b, DifferentiableAt ℝ g (f x) ∧ deriv g (f x) = 1 / deriv f x) :
    ∀ a b : ℝ, a < b → ∀ f : ℝ → ℝ, (∀ x ∈ Set.Ioo a b, DifferentiableAt ℝ f x ∧ 0 < deriv f x) → ∀ g : ℝ → ℝ, (∀ x ∈ Set.Ioo a b, g (f x) = x) → (∀ y ∈ f '' Set.Ioo a b, f (g y) = y) → StrictMonoOn f (Set.Ioo a b) ∧ ∀ x ∈ Set.Ioo a b, DifferentiableAt ℝ g (f x) ∧ deriv g (f x) = 1 / deriv f x := by
  intro a b hab f hd g hg1 hg2; exact h_eq f g a b hab hd hg1 hg2
end Chk1
section Chk2
open Set
theorem ctl_mp  (h_eq : True) :
    ∀ f g : ℝ → ℝ, ∀ a b : ℝ, a < b → (∀ x ∈ Set.Ioo a b, DifferentiableAt ℝ f x ∧ 0 < deriv f x) → (∀ x ∈ Set.Ioo a b, g (f x) = x) → (∀ y ∈ f '' Set.Ioo a b, f (g y) = y) → StrictMonoOn f (Set.Ioo a b) ∧ ∀ x ∈ Set.Ioo a b, DifferentiableAt ℝ g (f x) ∧ deriv g (f x) = 1 / deriv f x := by
  intro f g a b hab hd hg1 hg2; exact h_eq a b hab f hd g hg1 hg2
end Chk2
section Chk3
open Set
theorem ctl_mpr  (h_eq : True) :
    ∀ a b : ℝ, a < b → ∀ f : ℝ → ℝ, (∀ x ∈ Set.Ioo a b, DifferentiableAt ℝ f x ∧ 0 < deriv f x) → ∀ g : ℝ → ℝ, (∀ x ∈ Set.Ioo a b, g (f x) = x) → (∀ y ∈ f '' Set.Ioo a b, f (g y) = y) → StrictMonoOn f (Set.Ioo a b) ∧ ∀ x ∈ Set.Ioo a b, DifferentiableAt ℝ g (f x) ∧ deriv g (f x) = 1 / deriv f x := by
  intro a b hab f hd g hg1 hg2; exact h_eq f g a b hab hd hg1 hg2
end Chk3
