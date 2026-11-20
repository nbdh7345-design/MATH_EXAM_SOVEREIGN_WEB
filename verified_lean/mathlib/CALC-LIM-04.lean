-- CALC-LIM-04: formalize bằng LLM (haiku), kiểm chứng bằng Lean 4 + Mathlib.
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
    Filter.Tendsto (fun x : ℝ => Real.sin ((m : ℝ) * x) / x) (𝓝[≠] 0) (𝓝 ((m : ℝ))) := by
  have hm2 : (2:ℝ) ≤ (m:ℝ) := by exact_mod_cast hm_lo
  have hm0 : (m:ℝ) ≠ 0 := by
    intro h
    linarith
  have hmul : Filter.Tendsto (fun x : ℝ => (m:ℝ) * x) (𝓝[≠] (0:ℝ)) (𝓝[≠] (0:ℝ)) := by
    apply tendsto_nhdsWithin_of_tendsto_nhds_of_eventually_within
    · have hc : Continuous (fun x : ℝ => (m:ℝ) * x) := continuous_const.mul continuous_id
      have h0 : Filter.Tendsto (fun x : ℝ => (m:ℝ) * x) (𝓝 (0:ℝ)) (𝓝 ((m:ℝ) * 0)) := hc.tendsto 0
      rw [mul_zero] at h0
      exact h0.mono_left nhdsWithin_le_nhds
    · filter_upwards [self_mem_nhdsWithin] with x hx
      simp only [Set.mem_compl_iff, Set.mem_singleton_iff] at hx ⊢
      exact mul_ne_zero hm0 hx
  have hsin := Real.tendsto_sin_div_nhdsNE_zero.comp hmul
  have hfin := hsin.const_mul (m:ℝ)
  rw [mul_one] at hfin
  apply hfin.congr'
  filter_upwards [self_mem_nhdsWithin] with x hx
  simp only [Set.mem_compl_iff, Set.mem_singleton_iff] at hx
  show (m:ℝ) * (Real.sin ((m:ℝ) * x) / ((m:ℝ) * x)) = Real.sin ((m:ℝ) * x) / x
  rw [mul_div_assoc', mul_div_mul_left _ _ hm0]

#print axioms exam_answer
