-- PB-calculus__p18: FR09 (dung), Lean 4 + Mathlib; dòng khai báo định lý do hệ thống viết.
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
The integral of the function (1/x + x^2) with respect to x from 2 to 8 equals the natural logarithm of 4 plus 168.
-/

open Real

theorem integral_of_function_equals_ln_plus_168 :
    (∫ x in Set.Icc 2 8, (1 / x + x^2) : ℝ) = Real.log 4 + 168 := by
  have h2 : (∫ x in Set.Icc (2:ℝ) 8, (1 / x + x^2) : ℝ) = ∫ x in (2:ℝ)..8, (1 / x + x^2) := by
    rw [intervalIntegral.integral_of_le (by norm_num : (2:ℝ) ≤ 8), MeasureTheory.integral_Icc_eq_integral_Ioc]
  rw [h2]
  have i1 : IntervalIntegrable (fun x : ℝ => 1 / x) MeasureTheory.volume 2 8 := by
    apply ContinuousOn.intervalIntegrable
    rw [Set.uIcc_of_le (by norm_num : (2:ℝ) ≤ 8)]
    apply ContinuousOn.div continuousOn_const continuousOn_id
    intro x hx
    have hx0 : (0:ℝ) < x := lt_of_lt_of_le (by norm_num) hx.1
    exact hx0.ne'
  have i2 : IntervalIntegrable (fun x : ℝ => x ^ 2) MeasureTheory.volume 2 8 := by
    apply ContinuousOn.intervalIntegrable
    exact (continuous_pow 2).continuousOn
  rw [intervalIntegral.integral_add i1 i2]
  rw [integral_one_div_of_pos (by norm_num) (by norm_num), integral_pow]
  norm_num

#print axioms integral_of_function_equals_ln_plus_168
