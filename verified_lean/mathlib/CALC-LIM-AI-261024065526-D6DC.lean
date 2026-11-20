-- CALC-LIM-AI-261024065526-D6DC: formalize bằng LLM (haiku), kiểm chứng bằng Lean 4 + Mathlib.
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
open Real Filter Topology



theorem exam_answer (m : ℕ) (hm_lo : 2 ≤ m) (hm_hi : m ≤ 9) :
    Filter.Tendsto (fun x : ℝ => (Real.tan ((m : ℝ) * x) - Real.sin ((m : ℝ) * x)) / x ^ 3) (𝓝[≠] 0) (𝓝 ((((1 : ℝ) / 2) * ((m : ℝ) ^ (3 : ℕ))))) := by
  have hcos : Filter.Tendsto (fun x : ℝ => Real.cos ((m:ℝ) * x)) (𝓝[≠] (0:ℝ)) (𝓝 1) := by
      have h1 : Continuous (fun x : ℝ => Real.cos ((m:ℝ) * x)) := by fun_prop
      have h3 : Filter.Tendsto (fun x : ℝ => Real.cos ((m:ℝ) * x)) (𝓝[≠] (0:ℝ)) (𝓝 (Real.cos ((m:ℝ) * 0))) :=
        (h1.tendsto 0).mono_left nhdsWithin_le_nhds
      have h4 : Real.cos ((m:ℝ) * 0) = 1 := by simp
      rw [h4] at h3
      exact h3
    have hA : (fun x : ℝ => Real.sin ((m:ℝ) * x) - (m:ℝ) * x ^ 1) =o[𝓝 0] fun x : ℝ => x ^ 1 := by
      have e : (fun x : ℝ => Real.sin ((m:ℝ) * x) - (m:ℝ) * x ^ 1) = (fun x : ℝ => Real.sin ((m:ℝ) * x) - ∑ j ∈ Finset.range 1, (-1:ℝ) ^ j * ((m:ℝ) * x) ^ (2 * j + 1) / ((2 * j + 1).factorial : ℝ)) := by
        funext x
        simp [Finset.sum_range_one] <;> ring
      rw [e]
      exact MathExam.isLittleO_pow_of_le (MathExam.sin_mul_maclaurin (m:ℝ) 1) (by norm_num)
    have hg1 : (fun x : ℝ => x - 1 * x ^ 1) =o[𝓝 0] fun x : ℝ => x ^ 1 := by
      have hz : (fun x : ℝ => x - 1 * x ^ 1) = fun _ => (0:ℝ) := by
        funext x
        simp
      rw [hz]
      first
      | exact Asymptotics.isLittleO_zero _ _
      | exact Asymptotics.isLittleO_zero
      | simp
    have hA0 := MathExam.tendsto_div_of_isLittleO (f := fun x : ℝ => Real.sin ((m:ℝ) * x)) (g := fun x : ℝ => x) (a := (m:ℝ)) (b := 1) (n := 1) one_ne_zero hA hg1
    have hA' : Filter.Tendsto (fun x : ℝ => Real.sin ((m:ℝ) * x) / x) (𝓝[≠] (0:ℝ)) (𝓝 (m:ℝ)) := by
      have h := hA0
      rw [div_one] at h
      exact h
    have hB : (fun x : ℝ => Real.cos ((m:ℝ) * x) - 1 - (-((m:ℝ) ^ 2) / 2) * x ^ 2) =o[𝓝 0] fun x : ℝ => x ^ 2 := by
      have e : (fun x : ℝ => Real.cos ((m:ℝ) * x) - 1 - (-((m:ℝ) ^ 2) / 2) * x ^ 2) = (fun x : ℝ => Real.cos ((m:ℝ) * x) - ∑ j ∈ Finset.range (1 + 1), (-1:ℝ) ^ j * ((m:ℝ) * x) ^ (2 * j) / ((2 * j).factorial : ℝ)) := by
        funext x
        simp [Finset.sum_range_succ] <;> ring
      rw [e]
      exact MathExam.isLittleO_pow_of_le (MathExam.cos_mul_maclaurin (m:ℝ) 1) (by norm_num)
    have hg2 : (fun x : ℝ => x ^ 2 - 1 * x ^ 2) =o[𝓝 0] fun x : ℝ => x ^ 2 := by
      have hz : (fun x : ℝ => x ^ 2 - 1 * x ^ 2) = fun _ => (0:ℝ) := by
        funext x
        simp
      rw [hz]
      first
      | exact Asymptotics.isLittleO_zero _ _
      | exact Asymptotics.isLittleO_zero
      | simp
    have hB0 := MathExam.tendsto_div_of_isLittleO (f := fun x : ℝ => Real.cos ((m:ℝ) * x) - 1) (g := fun x : ℝ => x ^ 2) (a := -((m:ℝ) ^ 2) / 2) (b := 1) (n := 2) one_ne_zero hB hg2
    have hB' : Filter.Tendsto (fun x : ℝ => (Real.cos ((m:ℝ) * x) - 1) / x ^ 2) (𝓝[≠] (0:ℝ)) (𝓝 (-((m:ℝ) ^ 2) / 2)) := by
      have h := hB0
      rw [div_one] at h
      exact h
    have hC : Filter.Tendsto (fun x : ℝ => (Real.cos ((m:ℝ) * x))⁻¹) (𝓝[≠] (0:ℝ)) (𝓝 1) := by
      have h := hcos.inv₀ one_ne_zero
      rw [inv_one] at h
      exact h
    have hD : Filter.Tendsto (fun x : ℝ => -(Real.cos ((m:ℝ) * x))⁻¹) (𝓝[≠] (0:ℝ)) (𝓝 (-1)) := hC.neg
    have hfinal := (hA'.mul hB').mul hD
    have hcne : ∀ᶠ x in 𝓝[≠] (0:ℝ), Real.cos ((m:ℝ) * x) ≠ 0 := by
      first
      | exact hcos.eventually_ne one_ne_zero
      | exact hcos.eventually (isOpen_ne.mem_nhds one_ne_zero)
    have hfeq : (fun x : ℝ => Real.sin ((m:ℝ) * x) / x * ((Real.cos ((m:ℝ) * x) - 1) / x ^ 2) * -(Real.cos ((m:ℝ) * x))⁻¹) =ᶠ[𝓝[≠] (0:ℝ)] (fun x : ℝ => (Real.tan ((m:ℝ) * x) - Real.sin ((m:ℝ) * x)) / x ^ 3) := by
      filter_upwards [hcne, self_mem_nhdsWithin] with x hc hx
      have hx' : x ≠ 0 := hx
      rw [Real.tan_eq_sin_div_cos]
      field_simp
      try ring
    have hlim := Filter.Tendsto.congr' hfeq hfinal
    have hval : (m:ℝ) * (-((m:ℝ) ^ 2) / 2) * (-1:ℝ) = ((1 : ℝ) / 2) * ((m : ℝ) ^ (3 : ℕ)) := by
      ring
    rw [← hval]
    exact hlim

#print axioms exam_answer
