-- CALC-LIM-AI-261024065524-45CD: formalize bằng LLM (haiku), kiểm chứng bằng Lean 4 + Mathlib.
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

theorem tan_div_cube_tendsto_aux : Filter.Tendsto (fun u : ℝ => (Real.tan u - u) / u ^ 3) (𝓝[≠] 0) (𝓝 (1 / 3)) := by
  have hs : (fun x : ℝ => Real.sin x - (x - x ^ 3 / 6)) =o[𝓝 0] fun x : ℝ => x ^ 3 := by
    have h := MathExam.isLittleO_pow_of_le (MathExam.sin_mul_maclaurin 1 2) (show (3 : ℕ) ≤ 2 * 2 by norm_num)
    convert h using 1
    funext x
    norm_num [Finset.sum_range_succ, Nat.factorial] <;> ring
  have hc : (fun x : ℝ => Real.cos x - (1 - x ^ 2 / 2)) =o[𝓝 0] fun x : ℝ => x ^ 3 := by
    have h := MathExam.isLittleO_pow_of_le (MathExam.cos_mul_maclaurin 1 1) (show (3 : ℕ) ≤ 2 * 1 + 1 by norm_num)
    convert h using 1
    funext x
    norm_num [Finset.sum_range_succ, Nat.factorial] <;> ring
  have hid : (fun u : ℝ => u) =O[𝓝 0] (fun _ : ℝ => (1 : ℝ)) :=
    Filter.Tendsto.isBigO_one ℝ (tendsto_id : Filter.Tendsto (fun u : ℝ => u) (𝓝 0) (𝓝 0))
  have hmul : (fun u : ℝ => u * (Real.cos u - (1 - u ^ 2 / 2))) =o[𝓝 0] fun u : ℝ => u ^ 3 := by
    have h := hid.mul_isLittleO hc
    simp only [one_mul] at h
    exact h
  have hN : (fun u : ℝ => (Real.sin u - u * Real.cos u) - 1 / 3 * u ^ 3) =o[𝓝 0] fun u : ℝ => u ^ 3 := by
    have e : (fun u : ℝ => (Real.sin u - u * Real.cos u) - 1 / 3 * u ^ 3)
        = fun u : ℝ => (Real.sin u - (u - u ^ 3 / 6)) - u * (Real.cos u - (1 - u ^ 2 / 2)) := by
      funext u
      ring
    rw [e]
    exact hs.sub hmul
  have hg : (fun x : ℝ => x ^ 3 - 1 * x ^ 3) =o[𝓝 0] fun x : ℝ => x ^ 3 := by
    simp
  have hN2 := MathExam.tendsto_div_of_isLittleO (f := fun u : ℝ => Real.sin u - u * Real.cos u)
    (g := fun x : ℝ => x ^ 3) (a := 1 / 3) (b := 1) (n := 3) one_ne_zero hN hg
  have hcos : Filter.Tendsto Real.cos (𝓝 0) (𝓝 1) := by
    simpa using (Real.continuous_cos.tendsto (0 : ℝ))
  have hcne : ∀ᶠ u in 𝓝 (0 : ℝ), Real.cos u ≠ 0 := hcos.eventually_ne one_ne_zero
  have hlim : Filter.Tendsto (fun u : ℝ => (Real.sin u - u * Real.cos u) / u ^ 3 / Real.cos u)
      (𝓝[≠] 0) (𝓝 (1 / 3 / 1 / 1)) :=
    hN2.div (hcos.mono_left nhdsWithin_le_nhds) one_ne_zero
  have e1 : (1 : ℝ) / 3 / 1 / 1 = 1 / 3 := by norm_num
  rw [e1] at hlim
  refine Filter.Tendsto.congr' ?_ hlim
  filter_upwards [self_mem_nhdsWithin, hcne.filter_mono nhdsWithin_le_nhds] with u hu hc0
  have hu' : u ≠ 0 := hu
  show (Real.sin u - u * Real.cos u) / u ^ 3 / Real.cos u = (Real.tan u - u) / u ^ 3
  rw [Real.tan_eq_sin_div_cos]
  field_simp

theorem exam_answer (m : ℕ) (hm_lo : 2 ≤ m) (hm_hi : m ≤ 9) :
    Filter.Tendsto (fun x : ℝ => (Real.tan ((m : ℝ) * x) - (m : ℝ) * x) / x ^ 3) (𝓝[≠] 0) (𝓝 ((((1 : ℝ) / 3) * ((m : ℝ) ^ (3 : ℕ))))) := by
  have hm2 : (2 : ℝ) ≤ (m : ℝ) := by exact_mod_cast hm_lo
    have hm : (m : ℝ) ≠ 0 := (by linarith : (0 : ℝ) < (m : ℝ)).ne'
    have hm3 : (m : ℝ) ^ 3 ≠ 0 := pow_ne_zero 3 hm
    have hc : Continuous (fun x : ℝ => (m : ℝ) * x) := continuous_const.mul continuous_id
    have h0 : Filter.Tendsto (fun x : ℝ => (m : ℝ) * x) (𝓝 0) (𝓝 0) := by
      have := hc.tendsto 0
      simp only [mul_zero] at this
      exact this
    have h1 : Filter.Tendsto (fun x : ℝ => (m : ℝ) * x) (𝓝[≠] 0) (𝓝[≠] 0) := by
      rw [tendsto_nhdsWithin_iff]
      refine ⟨h0.mono_left nhdsWithin_le_nhds, ?_⟩
      exact eventually_nhdsWithin_of_forall (fun x hx => mul_ne_zero hm hx)
    have h2 := tan_div_cube_tendsto_aux.comp h1
    have h3 : Filter.Tendsto (fun x : ℝ => (m : ℝ) ^ 3 * ((Real.tan ((m : ℝ) * x) - (m : ℝ) * x) / ((m : ℝ) * x) ^ 3)) (𝓝[≠] 0) (𝓝 ((m : ℝ) ^ 3 * (1 / 3))) :=
      h2.const_mul ((m : ℝ) ^ 3)
    have h4 : (m : ℝ) ^ 3 * (1 / 3) = 1 / 3 * (m : ℝ) ^ (3 : ℕ) := by ring
    rw [h4] at h3
    refine h3.congr' ?_
    filter_upwards [self_mem_nhdsWithin] with x hx
    have hx' : x ≠ 0 := hx
    rw [mul_pow]
    first
      | (rw [← mul_div_assoc, mul_div_mul_left _ _ hm3])
      | (field_simp; ring)
      | field_simp

#print axioms exam_answer
