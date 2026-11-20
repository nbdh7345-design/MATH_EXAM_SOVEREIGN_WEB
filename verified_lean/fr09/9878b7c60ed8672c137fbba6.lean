-- PB-calculus__p2: FR09 (dung), Lean 4 + Mathlib; dòng khai báo định lý do hệ thống viết.
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
The integral of \(\displaystyle \int_0^1\frac{8x^2 +6x +5}{x^2 +2x+2 }\,dx\) is equal to \(-5\ln\frac52 - \left(\tan^{-1}2-\frac{\pi}4\right)+8\).
-/

open Real

theorem hpos_aux (x : ℝ) : 0 < x^2 + 2*x + 2 := by
  nlinarith [sq_nonneg (x+1)]

theorem hg_aux (x : ℝ) : HasDerivAt (fun y : ℝ => y^2 + 2*y + 2) (2*x+2) x := by
  have h := ((hasDerivAt_pow 2 x).add ((hasDerivAt_id' x).const_mul (2:ℝ))).add_const (2:ℝ)
  convert h using 1
  norm_num

theorem hd_aux (x : ℝ) : HasDerivAt (fun y : ℝ => 8*y - 5*Real.log (y^2+2*y+2) - Real.arctan (y+1)) ((8*x^2+6*x+5)/(x^2+2*x+2)) x := by
  have A := (hasDerivAt_id' x).const_mul (8:ℝ)
  have B := ((hg_aux x).log (hpos_aux x).ne').const_mul (5:ℝ)
  have C := ((hasDerivAt_id' x).add_const (1:ℝ)).arctan
  have D := (A.sub B).sub C
  convert D using 1
  show (8*x^2+6*x+5)/(x^2+2*x+2) = 8*1 - 5*((2*x+2)/(x^2+2*x+2)) - 1/(1+(x+1)^2)*1
  have h3 : (1:ℝ) + (x+1)^2 = x^2+2*x+2 := by ring
  rw [h3]
  have hQ : x^2+2*x+2 ≠ 0 := (hpos_aux x).ne'
  rw [div_eq_iff hQ]
  have e1 : (2*x+2)/(x^2+2*x+2)*(x^2+2*x+2) = 2*x+2 := div_mul_cancel₀ _ hQ
  have e2 : 1/(x^2+2*x+2)*(x^2+2*x+2) = 1 := div_mul_cancel₀ _ hQ
  linear_combination 5*e1 + e2

theorem hint_aux : IntervalIntegrable (fun x : ℝ => (8*x^2+6*x+5)/(x^2+2*x+2)) MeasureTheory.volume 0 1 := by
  apply ContinuousOn.intervalIntegrable
  exact ContinuousOn.div (by fun_prop) (by fun_prop) (fun x _ => (hpos_aux x).ne')

theorem key_aux : ∫ x in (0:ℝ)..1, (8*x^2+6*x+5)/(x^2+2*x+2) = (8*1 - 5*Real.log (1^2+2*1+2) - Real.arctan (1+1)) - (8*0 - 5*Real.log (0^2+2*0+2) - Real.arctan (0+1)) :=
  intervalIntegral.integral_eq_sub_of_hasDerivAt (fun x _ => hd_aux x) hint_aux

theorem hl_aux : Real.log (5/2) = Real.log 5 - Real.log 2 :=
  Real.log_div (by norm_num) (by norm_num)

theorem integral_of_rational_function_eq_given_value :
    let f := fun x => (8 * x^2 + 6 * x + 5) / (x^2 + 2 * x + 2);
  ∫ x in Set.Icc 0 1, f x = -5 * log (5 / 2) - (arctan 2 - π / 4) + 8 := by
  dsimp only
  rw [MeasureTheory.integral_Icc_eq_integral_Ioc, ← intervalIntegral.integral_of_le (by norm_num : (0:ℝ) ≤ 1), key_aux, hl_aux]
  norm_num [Real.arctan_one] <;> ring

#print axioms integral_of_rational_function_eq_given_value
