-- PB-calculus__p3: FR09 (dung), Lean 4 + Mathlib; dòng khai báo định lý do hệ thống viết.
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


set_option autoImplicit true
/-
The local maximum of the function f(x)=x^4/4 - x^3/3 - 2x^2 + 4x + 5 on the interval
[-3,3] is 41 / 4  and is attained at x=3, and
the local minimum is -13/3 and it is attained for x=-2.
-/

noncomputable def f (x : ℝ) : ℝ := x^4 / 4 - x^3 / 3 - 2 * x^2 + 4 * x + 5

theorem extrema_on_interval :
    ¬ ((∃ x : ℝ, x ∈ Set.Icc (-3) 3 ∧ (∀ y ∈ Set.Icc (-3) 3, f y ≤ f x) ∧ f x = 41/4 ∧ x = 3) ∧
  (∃ z : ℝ, z ∈ Set.Icc (-3) 3 ∧ (∀ y ∈ Set.Icc (-3) 3, f z ≤ f y) ∧ f z = - 13 / 3 ∧ z = -2)) := by
  intro h
  have h₁ : f 3 = 41/4 := by norm_num [f]
  have h₂ : f (-2) = -13/3 := by norm_num [f]
  have h₃ : False := by (first | (norm_num; done) | (simp; done) | (field_simp; done) | (ring_nf; done) | (positivity; done) | (fun_prop; done) | (linarith; done) | (nlinarith; done) | (aesop; done) | (constructor <;> first | fun_prop | (norm_num; done) | (simp; done); done))
  exact h₃

#print axioms extrema_on_interval
