-- PB-calculus__p56: FR09 (dung), Lean 4 + Mathlib; dòng khai báo định lý do hệ thống viết.
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
The maximum value of \[\int_0^1 \left(x^2f(x)-xf^2(x)\right)\,dx\] over all continuous functions \(f:[0,1]\to\mathbb R\) is \(\frac{1}{16}\).
-/

open Filter Topology

variable {f : ℝ → ℝ} (hf : Continuous f)

theorem max_integral_value :
    IsMaxOn (fun f => ∫ x in Set.Icc 0 1, (x^2 * f x - x * f x^2)) {f | Continuous f} f →
(∫ x in Set.Icc 0 1, (x^2 * f x - x * f x^2)) = 1/16 := by
  have h3 : ∫ x in Set.Icc (0:ℝ) 1, x^3/4 = 1/16 := by
    rw [MeasureTheory.integral_Icc_eq_integral_Ioc, ← intervalIntegral.integral_of_le (show (0:ℝ) ≤ 1 by norm_num)]
    norm_num [intervalIntegral.integral_div, integral_pow]
  have hcalc : (∫ x in Set.Icc (0:ℝ) 1, (x^2 * (x/2) - x * (x/2)^2)) = 1/16 := by
    have e : ∀ x : ℝ, x^2 * (x/2) - x * (x/2)^2 = x^3/4 := fun x => by ring
    simp only [e]
    exact h3
  intro h
  have hg : (fun x : ℝ => x/2) ∈ {f : ℝ → ℝ | Continuous f} := by
    show Continuous (fun x : ℝ => x/2)
    fun_prop
  have hle : (∫ x in Set.Icc (0:ℝ) 1, (x^2 * (x/2) - x * (x/2)^2)) ≤ ∫ x in Set.Icc (0:ℝ) 1, (x^2 * f x - x * f x^2) :=
    isMaxOn_iff.mp h (fun x : ℝ => x/2) hg
  rw [hcalc] at hle
  by_cases hint : MeasureTheory.IntegrableOn (fun x : ℝ => x^2 * f x - x * f x^2) (Set.Icc (0:ℝ) 1)
  · have hgint : MeasureTheory.IntegrableOn (fun x : ℝ => x^3/4) (Set.Icc (0:ℝ) 1) :=
      (by fun_prop : Continuous (fun x : ℝ => x^3/4)).integrableOn_Icc
    have hmono : (∫ x in Set.Icc (0:ℝ) 1, (x^2 * f x - x * f x^2)) ≤ ∫ x in Set.Icc (0:ℝ) 1, x^3/4 := by
      apply MeasureTheory.setIntegral_mono_on hint hgint measurableSet_Icc
      intro x hx
      obtain ⟨hx0, _⟩ := hx
      nlinarith [mul_nonneg hx0 (sq_nonneg (f x - x/2))]
    rw [h3] at hmono
    linarith
  · exfalso
    rw [MeasureTheory.integral_undef hint] at hle
    linarith

#print axioms max_integral_value
