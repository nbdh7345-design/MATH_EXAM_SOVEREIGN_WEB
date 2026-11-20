-- CALC-LIM-AI-261024100153-FC12: formalize bằng LLM (sonnet), kiểm chứng bằng Lean 4 + Mathlib.
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
open Topology Filter



theorem exam_answer (m : ℕ) (hm_lo : 2 ≤ m) (hm_hi : m ≤ 9) :
    Filter.Tendsto (fun x : ℝ => (Real.exp (Real.sin ((m:ℝ) * x)) - Real.exp ((m:ℝ) * x)) / x ^ 3) (𝓝[≠] 0) (𝓝 ((((-1 : ℝ) / 6) * ((m : ℝ) ^ (3 : ℕ))))) := by
  obtain ⟨c, hc⟩ : ∃ c : ℝ, c = (m:ℝ) := ⟨_, rfl⟩
  rw [← hc]
  have hA : Tendsto (fun x:ℝ => (Real.sin (c*x) - c*x)/x^3) (𝓝[≠] 0) (𝓝 (-1/6*c^3)) := by
    have h0 : Tendsto (fun x:ℝ => (|c|^5/100) * x^2) (𝓝[≠] 0) (𝓝 0) := by
      have h : Tendsto (fun x:ℝ => (|c|^5/100) * x^2) (𝓝 0) (𝓝 ((|c|^5/100) * (0:ℝ)^2)) :=
        (continuous_const.mul (continuous_pow 2)).tendsto 0
      have e : (|c|^5/100) * (0:ℝ)^2 = 0 := by simp
      rw [e] at h
      exact h.mono_left nhdsWithin_le_nhds
    have hev : ∀ᶠ x:ℝ in 𝓝 0, |c*x| < 1 := by
      have hcont : Continuous fun x:ℝ => |c*x| := by fun_prop
      exact hcont.continuousAt.eventually_lt continuousAt_const (by simp)
    rw [← tendsto_sub_nhds_zero_iff]
    refine squeeze_zero_norm' ?_ h0
    filter_upwards [hev.filter_mono nhdsWithin_le_nhds, self_mem_nhdsWithin] with x hx1 hx
    have hx' : x ≠ 0 := hx
    beta_reduce
    have hb := Real.sin_bound (le_of_lt hx1)
    have key : (Real.sin (c*x) - c*x)/x^3 - (-1/6*c^3)
        = (Real.sin (c*x) - (c*x - (c*x)^3/6))/x^3 := by
      field_simp
      ring
    have hx3 : 0 < |x|^3 := pow_pos (abs_pos.mpr hx') 3
    have e5 : |x|^5 = x^2 * |x|^3 := by
      rw [← sq_abs x]; ring
    rw [key, Real.norm_eq_abs, abs_div, abs_pow, div_le_iff₀ hx3]
    calc |Real.sin (c*x) - (c*x - (c*x)^3/6)| ≤ |c*x|^5/100 := hb
      _ = (|c|^5/100 * x^2) * |x|^3 := by
        rw [abs_mul, mul_pow, e5]; ring
  have hB : Tendsto (fun x:ℝ => (Real.exp (Real.sin (c*x) - c*x) - 1 - (Real.sin (c*x) - c*x))/x^3) (𝓝[≠] 0) (𝓝 0) := by
    have h : Tendsto (fun x:ℝ => |x|^3) (𝓝 0) (𝓝 (|(0:ℝ)|^3)) :=
      (continuous_abs.pow 3).tendsto 0
    have h1 : Tendsto (fun x:ℝ => |x|^3) (𝓝[≠] 0) (𝓝 (|(0:ℝ)|^3)) := h.mono_left nhdsWithin_le_nhds
    have h2 : Tendsto (fun x:ℝ => |x|^3 * ((Real.sin (c*x) - c*x)/x^3)^2) (𝓝[≠] 0)
        (𝓝 (|(0:ℝ)|^3 * (-1/6*c^3)^2)) := h1.mul (hA.pow 2)
    have e : |(0:ℝ)|^3 * (-1/6*c^3)^2 = 0 := by simp
    rw [e] at h2
    have hev : ∀ᶠ x:ℝ in 𝓝 0, |Real.sin (c*x) - c*x| < 1 := by
      have hcont : Continuous fun x:ℝ => |Real.sin (c*x) - c*x| := by fun_prop
      exact hcont.continuousAt.eventually_lt continuousAt_const (by simp)
    refine squeeze_zero_norm' ?_ h2
    filter_upwards [hev.filter_mono nhdsWithin_le_nhds, self_mem_nhdsWithin] with x hx1 hx
    have hx' : x ≠ 0 := hx
    beta_reduce
    have hb := Real.abs_exp_sub_one_sub_id_le (le_of_lt hx1)
    have hx3 : 0 < |x|^3 := pow_pos (abs_pos.mpr hx') 3
    rw [Real.norm_eq_abs, abs_div, abs_pow, div_le_iff₀ hx3]
    calc |Real.exp (Real.sin (c*x) - c*x) - 1 - (Real.sin (c*x) - c*x)|
        ≤ (Real.sin (c*x) - c*x)^2 := hb
      _ = |x|^3 * ((Real.sin (c*x) - c*x)/x^3)^2 * |x|^3 := by
        have h6 : |x|^3 * |x|^3 = x^6 := by
          have : |x|^3 * |x|^3 = (|x|^2)^3 := by ring
          rw [this, sq_abs]; ring
        have : |x|^3 * ((Real.sin (c*x) - c*x)/x^3)^2 * |x|^3
            = (|x|^3 * |x|^3) * ((Real.sin (c*x) - c*x)/x^3)^2 := by ring
        rw [this, h6]
        field_simp
  have hE : Tendsto (fun x:ℝ => Real.exp (c*x)) (𝓝[≠] 0) (𝓝 1) := by
    have h : Tendsto (fun x:ℝ => Real.exp (c*x)) (𝓝 0) (𝓝 (Real.exp (c*0))) :=
      (by fun_prop : Continuous fun x:ℝ => Real.exp (c*x)).tendsto 0
    rw [mul_zero, Real.exp_zero] at h
    exact h.mono_left nhdsWithin_le_nhds
  have hT := hE.mul (hA.add hB)
  rw [add_zero, one_mul] at hT
  refine hT.congr' ?_
  filter_upwards [self_mem_nhdsWithin] with x hx
  have hx' : x ≠ 0 := hx
  have h1 : Real.exp (Real.sin (c*x)) = Real.exp (c*x) * Real.exp (Real.sin (c*x) - c*x) := by
    rw [← Real.exp_add]
    congr 1
    ring
  beta_reduce
  rw [h1]
  ring

#print axioms exam_answer
