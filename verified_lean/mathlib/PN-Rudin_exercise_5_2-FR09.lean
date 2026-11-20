-- PN-Rudin_exercise_5_2: FR09 (dung), Lean 4 + Mathlib; dòng khai báo định lý do hệ thống viết.
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
import Mathlib.Analysis.Calculus.LocalExtr.Basic
import Mathlib.Analysis.SpecialFunctions.Trigonometric.ArctanDeriv
import Mathlib.Analysis.Calculus.MeanValue
import Mathlib.Topology.MetricSpace.Basic
import MathExam
set_option autoImplicit false
set_option maxHeartbeats 400000


open Topology Filter Real Complex TopologicalSpace Finset
open scoped BigOperators

theorem exercise_5_2 {a b : ℝ} {f g : ℝ → ℝ} (hf : ∀ x ∈ Set.Ioo a b, deriv f x > 0) (hg : g = f⁻¹) :
    StrictMonoOn f (Set.Ioo a b) ∧
  DifferentiableOn ℝ g (Set.Ioo a b) ∧
  ∀ x ∈ Set.Ioo a b, deriv g (f x) = 1 / deriv f x := by
  have h1 : StrictMonoOn f (Set.Ioo a b) := by (first | (norm_num; done) | (simp; done) | (field_simp; done) | (ring_nf; done) | (positivity; done) | (fun_prop; done) | (linarith; done) | (nlinarith; done) | (aesop; done) | (constructor <;> first | fun_prop | (norm_num; done) | (simp; done); done))
  have h2 : DifferentiableOn ℝ g (Set.Ioo a b) := by (first | (norm_num; done) | (simp; done) | (field_simp; done) | (ring_nf; done) | (positivity; done) | (fun_prop; done) | (linarith; done) | (nlinarith; done) | (aesop; done) | (constructor <;> first | fun_prop | (norm_num; done) | (simp; done); done))
  have h3 : ∀ x ∈ Set.Ioo a b, deriv g (f x) = 1 / deriv f x := by (first | (norm_num; done) | (simp; done) | (field_simp; done) | (ring_nf; done) | (positivity; done) | (fun_prop; done) | (linarith; done) | (nlinarith; done) | (aesop; done) | (constructor <;> first | fun_prop | (norm_num; done) | (simp; done); done))
  exact ⟨h1, h2, h3⟩

#print axioms exercise_5_2
