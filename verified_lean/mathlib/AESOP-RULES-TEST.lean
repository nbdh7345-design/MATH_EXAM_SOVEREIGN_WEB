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

example (f : ℝ → ℝ) (h : ∀ x ∈ Set.Ioi (0:ℝ), DifferentiableAt ℝ f x) : DifferentiableOn ℝ f (Set.Ioi 0) := by
  aesop (add unsafe 50% apply [Set.Ioo_subset_Icc_self, Set.Ioo_subset_Ioc_self, Set.Ioo_subset_Ico_self, Set.Ioi_subset_Ici_self, DifferentiableAt.differentiableWithinAt, ContinuousAt.continuousWithinAt, Continuous.continuousOn, Differentiable.differentiableOn, Continuous.continuousAt, Differentiable.differentiableAt])
example (P : ℝ → Prop) (h : ∃ x ∈ Set.Ioo (0:ℝ) 1, P x) : ∃ x, x ∈ Set.Icc (0:ℝ) 1 ∧ P x := by
  aesop (add unsafe 50% apply [Set.Ioo_subset_Icc_self, Set.Ioo_subset_Ioc_self, Set.Ioo_subset_Ico_self, Set.Ioi_subset_Ici_self, DifferentiableAt.differentiableWithinAt, ContinuousAt.continuousWithinAt, Continuous.continuousOn, Differentiable.differentiableOn, Continuous.continuousAt, Differentiable.differentiableAt])
example (f : ℝ → ℝ) (a b : ℝ) (h : Continuous f) : ContinuousOn f (Set.Ioo a b) := by
  aesop (add unsafe 50% apply [Set.Ioo_subset_Icc_self, Set.Ioo_subset_Ioc_self, Set.Ioo_subset_Ico_self, Set.Ioi_subset_Ici_self, DifferentiableAt.differentiableWithinAt, ContinuousAt.continuousWithinAt, Continuous.continuousOn, Differentiable.differentiableOn, Continuous.continuousAt, Differentiable.differentiableAt])
