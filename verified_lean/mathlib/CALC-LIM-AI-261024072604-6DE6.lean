-- CALC-LIM-AI-261024072604-6DE6: formalize bằng LLM (sonnet), kiểm chứng bằng Lean 4 + Mathlib.
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

theorem aux_sqrt_eq (m x : ℝ) (hx : 0 < 1 + m * x) (hx0 : x ≠ 0) :
    -(1/2) * m ^ 2 / (Real.sqrt (1 + m * x) + 1) ^ 2
      = (Real.sqrt (1 + m * x) - 1 - m * x / 2) / x ^ 2 := by
  obtain ⟨s, hsdef⟩ : ∃ s, s = Real.sqrt (1 + m * x) := ⟨_, rfl⟩
  rw [← hsdef]
  have hs : s ^ 2 = 1 + m * x := by
    rw [hsdef]; exact Real.sq_sqrt hx.le
  have hs0 : 0 ≤ s := by rw [hsdef]; exact Real.sqrt_nonneg _
  have hp1 : 0 < s + 1 := by linarith
  have hp : (s + 1) ^ 2 ≠ 0 := ne_of_gt (pow_pos hp1 2)
  have hx2 : x ^ 2 ≠ 0 := pow_ne_zero 2 hx0
  rw [div_eq_div_iff hp hx2]
  have key : s - 1 - m * x / 2 = -(s - 1) ^ 2 / 2 := by
    linear_combination (1/2) * hs
  have hm : m * x = (s - 1) * (s + 1) := by
    linear_combination (-1) * hs
  have h2 : (m * x) ^ 2 = ((s - 1) * (s + 1)) ^ 2 := by rw [hm]
  linear_combination (-1/2) * h2 - (s + 1) ^ 2 * key

theorem exam_answer (m : ℕ) (hm_lo : 2 ≤ m) (hm_hi : m ≤ 9) :
    Filter.Tendsto (fun x : ℝ => (Real.sqrt (1 + (m:ℝ) * x) - 1 - (m:ℝ) * x / 2) / x ^ 2) (𝓝[≠] 0) (𝓝 ((((-1 : ℝ) / 8) * ((m : ℝ) ^ (2 : ℕ))))) := by
  have h1 : Tendsto (fun x : ℝ => Real.sqrt (1 + (m:ℝ) * x)) (𝓝 0) (𝓝 1) := by
    have : Continuous (fun x : ℝ => Real.sqrt (1 + (m:ℝ) * x)) := by fun_prop
    simpa using this.tendsto 0
  have h2 : Tendsto (fun x : ℝ => -(1/2) * (m:ℝ) ^ 2 / (Real.sqrt (1 + (m:ℝ) * x) + 1) ^ 2) (𝓝 0) (𝓝 (-(1/2) * (m:ℝ) ^ 2 / (1 + 1) ^ 2)) :=
    tendsto_const_nhds.div ((h1.add_const 1).pow 2) (by norm_num)
  have h3 := h2.mono_left (nhdsWithin_le_nhds (s := ({0}ᶜ : Set ℝ)))
  have hv : -(1/2) * (m:ℝ) ^ 2 / (1 + 1) ^ 2 = (-1 : ℝ) / 8 * (m:ℝ) ^ 2 := by ring
  rw [hv] at h3
  have hpos : ∀ᶠ x in 𝓝 (0:ℝ), 0 < 1 + (m:ℝ) * x := by
    have hc : Continuous (fun x : ℝ => 1 + (m:ℝ) * x) := by fun_prop
    exact (hc.tendsto 0).eventually (lt_mem_nhds (by norm_num))
  refine h3.congr' ?_
  filter_upwards [nhdsWithin_le_nhds hpos, self_mem_nhdsWithin] with x hx hx0
  exact aux_sqrt_eq (m:ℝ) x hx hx0

#print axioms exam_answer
