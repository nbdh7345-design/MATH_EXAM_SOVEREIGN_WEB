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
    (∀ a b : ℝ, a < b → ∀ f : ℝ → ℝ, ContinuousOn f (Set.Ioo a b) → (∀ x ∈ Set.Ioo a b, ∀ y ∈ Set.Ioo a b, f ((x + y) / 2) ≤ (f x + f y) / 2) → ConvexOn ℝ (Set.Ioo a b) f) ↔ (∀ a b : ℝ, ∀ f : ℝ → ℝ, a < b → ContinuousOn f (Set.Ioo a b) → (∀ x ∈ Set.Ioo a b, ∀ y ∈ Set.Ioo a b, f ((x + y) / 2) ≤ (f x + f y) / 2) → ConvexOn ℝ (Set.Ioo a b) f) := by
  first
    | exact Iff.rfl
    | (simp; done)
    | (constructor <;> intro h <;> first | (simpa using h) | (simp_all; done) | (linarith; done) | (nlinarith; done) | (norm_num at *; done) | (tauto; done) | (aesop; done))
end Chk0
