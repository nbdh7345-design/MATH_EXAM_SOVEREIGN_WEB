-- PB-calculus__p61: FR09 (dung), Lean 4 + Mathlib; dòng khai báo định lý do hệ thống viết.
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
The limit of the function \(f(x)=\frac{ 3^{x}-1}{x}\) as \(x\) approaches 0 is \(\ln 3\).
-/

open Filter Topology

theorem limit_of_function_as_x_approaches_zero :
    Tendsto (fun x => (3^x - 1) / x) (𝓝[≠] 0) (𝓝 (Real.log 3)) := by
  have h1 : HasDerivAt (fun x : ℝ => (3:ℝ)^x) ((3:ℝ)^(0:ℝ) * Real.log 3) 0 := (Real.hasStrictDerivAt_const_rpow (by norm_num) 0).hasDerivAt
  have h2 := hasDerivAt_iff_tendsto_slope.mp h1
  rw [Real.rpow_zero, one_mul] at h2
  exact Tendsto.congr' (Eventually.of_forall fun x => by simp [slope_def_field]) h2

#print axioms limit_of_function_as_x_approaches_zero
