-- CALC-LIM-AI-261024072604-D4B3: formalize bằng LLM (sonnet), kiểm chứng bằng Lean 4 + Mathlib.
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

lemma aux_lim (n : ℕ) : Filter.Tendsto (fun x : ℝ => (x ^ n - 1 - (n : ℝ) * (x - 1)) / (x - 1) ^ 2) (nhdsWithin 1 {1}ᶜ) (nhds ((n : ℝ) * ((n : ℝ) - 1) / 2)) := by
  induction n with
  | zero => simp
  | succ k ih =>
    have h1 : Filter.Tendsto (fun x : ℝ => x) (nhdsWithin 1 {1}ᶜ) (nhds 1) :=
      tendsto_nhdsWithin_of_tendsto_nhds (continuous_id.tendsto 1)
    have h : Filter.Tendsto (fun x : ℝ => x * ((x ^ k - 1 - (k : ℝ) * (x - 1)) / (x - 1) ^ 2) + k) (nhdsWithin 1 {1}ᶜ) (nhds (1 * ((k : ℝ) * ((k : ℝ) - 1) / 2) + k)) :=
      (h1.mul ih).add_const _
    have e : (((k + 1 : ℕ) : ℝ) * (((k + 1 : ℕ) : ℝ) - 1) / 2) = 1 * ((k : ℝ) * ((k : ℝ) - 1) / 2) + k := by
      push_cast; ring
    rw [e]
    refine h.congr' ?_
    filter_upwards [self_mem_nhdsWithin] with x hx
    have : x - 1 ≠ 0 := sub_ne_zero.mpr (by simpa using hx)
    field_simp
    push_cast
    ring

theorem exam_answer (m : ℕ) (hm_lo : 2 ≤ m) (hm_hi : m ≤ 9) :
    Filter.Tendsto (fun x : ℝ => (x ^ m - 1 - (m : ℝ) * (x - 1)) / (x - 1) ^ 2) (𝓝[≠] 1) (𝓝 ((((1 : ℝ) / 2) * (m : ℝ) * ((-1 : ℝ) + (m : ℝ))))) := by
  have e : (1:ℝ) / 2 * (m : ℝ) * (-1 + (m : ℝ)) = (m : ℝ) * ((m : ℝ) - 1) / 2 := by ring
  rw [e]
  exact aux_lim m

#print axioms exam_answer
