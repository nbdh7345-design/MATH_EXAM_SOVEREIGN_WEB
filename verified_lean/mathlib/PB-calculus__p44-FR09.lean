-- PB-calculus__p44: FR09 (dung), Lean 4 + Mathlib; dòng khai báo định lý do hệ thống viết.
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
The limit of the function \[\lim_{x\to 0}\frac{1-(\cos x)^{\sin x}}{x^3}\] is 1/2.
-/

open Filter Topology

theorem aux_f_zero : (1 - (Real.cos 0)^(Real.sin 0)) / (0:ℝ)^3 = 0 := by
  simp

theorem limit_of_function_at_zero :
    Tendsto (fun x => (1 - (Real.cos x)^(Real.sin x)) / x^3) (𝓝 0) (𝓝 (1 / 2)) := by
  have h0 : (1 - (Real.cos 0)^(Real.sin 0)) / (0:ℝ)^3 = 0 := aux_f_zero
    have hpunct : Tendsto (fun x : ℝ => (1 - (Real.cos x)^(Real.sin x)) / x^3) (𝓝[≠] 0) (𝓝 (1 / 2)) := by (first | (norm_num; done) | (simp; done) | (field_simp; done) | (ring_nf; done) | (positivity; done) | (fun_prop; done) | (linarith; done) | (nlinarith; done) | (aesop; done) | (constructor <;> first | fun_prop | (norm_num; done) | (simp; done); done))
    have hfinal : Tendsto (fun x : ℝ => (1 - (Real.cos x)^(Real.sin x)) / x^3) (𝓝 0) (𝓝 (1 / 2)) := by (first | (norm_num; done) | (simp; done) | (field_simp; done) | (ring_nf; done) | (positivity; done) | (fun_prop; done) | (linarith; done) | (nlinarith; done) | (aesop; done) | (constructor <;> first | fun_prop | (norm_num; done) | (simp; done); done))
    exact hfinal

#print axioms limit_of_function_at_zero
