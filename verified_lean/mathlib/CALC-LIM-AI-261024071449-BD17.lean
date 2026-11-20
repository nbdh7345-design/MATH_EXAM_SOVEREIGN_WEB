-- CALC-LIM-AI-261024071449-BD17: formalize bằng LLM (haiku), kiểm chứng bằng Lean 4 + Mathlib.
-- Header định lý và đáp án (ANSWER) do hệ thống sinh từ CSDL; LLM chỉ viết mệnh đề bài toán và chứng minh.
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
import MathExam
set_option autoImplicit false
open Filter Topology

theorem tan_taylor_aux : (fun u : ℝ => Real.tan u - (u + u^3/3)) =o[𝓝 0] (fun u : ℝ => u^3) := by
  have hsin : (fun u : ℝ => Real.sin u - (u - u^3/6)) =o[𝓝 0] (fun u : ℝ => u^3) := by
    have h := MathExam.isLittleO_pow_of_le (MathExam.sin_mul_maclaurin 1 2) (by norm_num : 3 ≤ 2 * 2)
    convert h using 1
    funext u
    norm_num [Finset.sum_range_succ, Nat.factorial] <;> ring
  have hcos : (fun u : ℝ => Real.cos u - (1 - u^2/2)) =o[𝓝 0] (fun u : ℝ => u^3) := by
    have h := MathExam.cos_mul_maclaurin 1 1
    convert h using 1
    all_goals (funext u; norm_num [Finset.sum_range_succ, Nat.factorial] <;> ring)
  have hc1 : Filter.Tendsto (fun u : ℝ => Real.cos u) (𝓝 0) (𝓝 1) := by
    simpa using Real.continuous_cos.tendsto (0:ℝ)
  have hB : Filter.Tendsto (fun u : ℝ => u + u^3/3) (𝓝 0) (𝓝 0) := by
    have hc : Continuous (fun u : ℝ => u + u^3/3) := by fun_prop
    simpa using hc.tendsto 0
  have hB1 : (fun u : ℝ => u + u^3/3) =O[𝓝 0] (fun _ => (1:ℝ)) := hB.isBigO_one ℝ
  have hinv0 : Filter.Tendsto (fun u : ℝ => (Real.cos u)⁻¹) (𝓝 0) (𝓝 1) := by
    simpa using hc1.inv₀ one_ne_zero
  have hinv : (fun u : ℝ => (Real.cos u)⁻¹) =O[𝓝 0] (fun _ => (1:ℝ)) := hinv0.isBigO_one ℝ
  have hBC : (fun u : ℝ => (u + u^3/3) * (Real.cos u - (1 - u^2/2))) =o[𝓝 0] (fun u : ℝ => u^3) := by
    have := hB1.mul_isLittleO hcos
    simpa using this
  have hu2 : Filter.Tendsto (fun u : ℝ => u^2) (𝓝 0) (𝓝 0) := by
    have hc : Continuous (fun u : ℝ => u^2) := by fun_prop
    simpa using hc.tendsto 0
  have hu5 : (fun u : ℝ => u^5) =o[𝓝 0] (fun u : ℝ => u^3) := by
    have h2 : (fun u : ℝ => u^2) =o[𝓝 0] (fun _ : ℝ => (1:ℝ)) :=
      (Asymptotics.isLittleO_one_iff ℝ).mpr hu2
    have h3 := h2.mul_isBigO (Asymptotics.isBigO_refl _ _)
    convert h3 using 1 <;> (funext u; simp only [Pi.mul_apply]; ring)
  have hT' := (hsin.sub hBC).add (hu5.const_mul_left (1/6 : ℝ))
  have hN : (fun u : ℝ => Real.sin u - (u + u^3/3) * Real.cos u) =o[𝓝 0] (fun u : ℝ => u^3) := by
    have heq : (fun u : ℝ => Real.sin u - (u + u^3/3) * Real.cos u)
        = (fun u : ℝ => (Real.sin u - (u - u^3/6)) - (u + u^3/3) * (Real.cos u - (1 - u^2/2)) + (1/6 : ℝ) * u^5) := by
      funext u; ring
    rw [heq]; exact hT'
  have hne : ∀ᶠ u in 𝓝 (0:ℝ), Real.cos u ≠ 0 := hc1.eventually (eventually_ne_nhds one_ne_zero)
  have heq2 : (fun u : ℝ => Real.tan u - (u + u^3/3))
      =ᶠ[𝓝 0] (fun u : ℝ => (Real.sin u - (u + u^3/3) * Real.cos u) * (Real.cos u)⁻¹) := by
    filter_upwards [hne] with u hu
    rw [Real.tan_eq_sin_div_cos, sub_mul, mul_assoc, mul_inv_cancel₀ hu, mul_one]
    ring
  have hfin : (fun u : ℝ => Real.tan u - (u + u^3/3)) =o[𝓝 0] (fun u : ℝ => u^3) := by
    have h := hN.mul_isBigO hinv
    simp only [mul_one] at h
    exact h.congr' heq2.symm (Filter.EventuallyEq.refl _ _)
  exact hfin

theorem exam_answer (a : ℕ) (ha_lo : 2 ≤ a) (ha_hi : a ≤ 9) :
    Filter.Tendsto (fun x : ℝ => (Real.tan ((a : ℝ) * x) - (a : ℝ) * x) / x ^ 3) (𝓝[≠] 0) (𝓝 ((((1 : ℝ) / 3) * ((a : ℝ) ^ (3 : ℕ))))) := by
  have hT := tan_taylor_aux
    have hk : Filter.Tendsto (fun x : ℝ => (a:ℝ) * x) (𝓝 0) (𝓝 0) := by
      have hc : Continuous (fun x : ℝ => (a:ℝ) * x) := by fun_prop
      simpa using hc.tendsto 0
    have h2 := hT.comp_tendsto hk
    have hbig : (fun x : ℝ => ((a:ℝ) * x)^3) =O[𝓝 0] (fun x : ℝ => x^3) := by
      have hr : (fun x : ℝ => ((a:ℝ) * x)^3) = (fun x : ℝ => (a:ℝ)^3 * x^3) := by
        funext x; ring
      rw [hr]
      exact Asymptotics.isBigO_const_mul_self _ _ _
    have hfun : (fun x : ℝ => Real.tan ((a:ℝ) * x) - (a:ℝ) * x - (a:ℝ)^3/3 * x^3)
        = (fun u : ℝ => Real.tan u - (u + u^3/3)) ∘ (fun x : ℝ => (a:ℝ) * x) := by
      funext x
      simp only [Function.comp]
      ring
    have hf : (fun x : ℝ => Real.tan ((a:ℝ) * x) - (a:ℝ) * x - (a:ℝ)^3/3 * x^3) =o[𝓝 0] (fun x : ℝ => x^3) := by
      rw [hfun]
      exact h2.trans_isBigO hbig
    have hg : (fun x : ℝ => x^3 - (1:ℝ) * x^3) =o[𝓝 0] (fun x : ℝ => x^3) := by
      simp only [one_mul, sub_self]
      apply Asymptotics.isLittleO_zero
    have key := MathExam.tendsto_div_of_isLittleO (f := fun x : ℝ => Real.tan ((a:ℝ) * x) - (a:ℝ) * x)
      (g := fun x : ℝ => x^3) (a := (a:ℝ)^3/3) (b := 1) (n := 3) one_ne_zero hf hg
    rw [show ((1:ℝ)/3) * ((a:ℝ)^(3:ℕ)) = (a:ℝ)^3/3/1 by ring]
    exact key

#print axioms exam_answer
