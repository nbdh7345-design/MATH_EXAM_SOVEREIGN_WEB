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

theorem integral_of_rational_function_eq_given_value :
    let f := fun x => (8 * x^2 + 6 * x + 5) / (x^2 + 2 * x + 2);
  ∫ x in Set.Icc 0 1, f x = -5 * log (5 / 2) - (arctan 2 - π / 4) + 8 := by
  intro f
  have hpos : ∀ x : ℝ, 0 < x^2 + 2*x + 2 := fun x => by nlinarith [sq_nonneg (x+1)]
  have hfx : ∀ x : ℝ, f x = 8*1 - 5*((2*x+2)/(x^2+2*x+2)) - 1/(1+(x+1)^2) := by
    intro x
    have e : (1:ℝ)+(x+1)^2 = x^2+2*x+2 := by ring
    have hD : x^2+2*x+2 ≠ 0 := (hpos x).ne'
    show (8*x^2+6*x+5)/(x^2+2*x+2) = _
    rw [e]
    rw [div_eq_iff hD]
    have h1 : (2*x+2)/(x^2+2*x+2)*(x^2+2*x+2) = 2*x+2 := div_mul_cancel₀ _ hD
    have h2 : 1/(x^2+2*x+2)*(x^2+2*x+2) = 1 := div_mul_cancel₀ _ hD
    linear_combination 5*h1 + h2
  have hderiv : ∀ x : ℝ, HasDerivAt (fun x : ℝ => 8*x - 5 * log (x^2+2*x+2) - arctan (x+1)) (f x) x := by
    intro x
    have h1 : HasDerivAt (fun x : ℝ => x^2+2*x+2) (2*x+2) x :=
      ((((hasDerivAt_id' x).pow 2).add ((hasDerivAt_id' x).const_mul 2)).add_const 2).congr_deriv (by norm_num <;> ring)
    have h2 : HasDerivAt (fun x : ℝ => log (x^2+2*x+2)) ((2*x+2)/(x^2+2*x+2)) x :=
      h1.log (hpos x).ne'
    have h3 : HasDerivAt (fun x : ℝ => arctan (x+1)) (1/(1+(x+1)^2)) x :=
      (((hasDerivAt_id' x).add_const 1).arctan).congr_deriv (by ring)
    have hF : HasDerivAt (fun x : ℝ => 8*x - 5 * log (x^2+2*x+2) - arctan (x+1))
        (8*1 - 5*((2*x+2)/(x^2+2*x+2)) - 1/(1+(x+1)^2)) x :=
      (((hasDerivAt_id' x).const_mul 8).sub (h2.const_mul 5)).sub h3
    rw [hfx x]
    exact hF
  have hcont : ContinuousOn f (Set.uIcc 0 1) := by
    have hfeq : f = fun x : ℝ => (8*x^2+6*x+5)/(x^2+2*x+2) := rfl
    rw [hfeq]
    exact ContinuousOn.div (by fun_prop) (by fun_prop) (fun x _ => (hpos x).ne')
  rw [MeasureTheory.integral_Icc_eq_integral_Ioc, ← intervalIntegral.integral_of_le zero_le_one]
  have key := intervalIntegral.integral_eq_sub_of_hasDerivAt (fun x _ => hderiv x) hcont.intervalIntegrable
  rw [key]
  have h5 : log (5/2 : ℝ) = log 5 - log 2 := Real.log_div (by norm_num) (by norm_num)
  have e1 : (1:ℝ)^2+2*1+2 = 5 := by norm_num
  have e0 : (0:ℝ)^2+2*0+2 = 2 := by norm_num
  have e2 : (1:ℝ)+1 = 2 := by norm_num
  have e3 : (0:ℝ)+1 = 1 := by norm_num
  show (8*1 - 5*log (1^2+2*1+2) - arctan (1+1)) - (8*0 - 5*log (0^2+2*0+2) - arctan (0+1)) = _
  rw [e1, e0, e2, e3, Real.arctan_one, h5]
  ring

#print axioms integral_of_rational_function_eq_given_value
