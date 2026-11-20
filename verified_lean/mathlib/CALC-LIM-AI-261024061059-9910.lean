-- CALC-LIM-AI-261024061059-9910: formalize bằng LLM (haiku), kiểm chứng bằng Lean 4 + Mathlib.
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
    Filter.Tendsto (fun x : ℝ => (Real.log (1 + (m : ℝ) * x) - (m : ℝ) * x) / x ^ 2) (𝓝[≠] 0) (𝓝 ((((-1 : ℝ) / 2) * ((m : ℝ) ^ (2 : ℕ))))) := by
  have hT : Filter.Tendsto (fun x : ℝ => (m : ℝ) * x) (𝓝 0) (𝓝 0) := by
    have hc : Continuous (fun x : ℝ => (m : ℝ) * x) := continuous_const.mul continuous_id
    simpa using hc.tendsto 0
  have h1 := MathExam.log_one_add_maclaurin 2
  have h2 : (fun x : ℝ => Real.log (1 + (m : ℝ) * x) - ∑ k ∈ Finset.range 2, (-1 : ℝ) ^ k * ((m : ℝ) * x) ^ (k + 1) / ((k : ℝ) + 1)) =o[𝓝 0] fun x : ℝ => ((m : ℝ) * x) ^ 2 :=
    h1.comp_tendsto hT
  have h3 : (fun x : ℝ => ((m : ℝ) * x) ^ 2) =O[𝓝 0] fun x : ℝ => x ^ 2 := by
    have e : (fun x : ℝ => ((m : ℝ) * x) ^ 2) = fun x : ℝ => (m : ℝ) ^ 2 * x ^ 2 := by
      funext x
      ring
    rw [e]
    exact (Asymptotics.isBigO_refl (fun x : ℝ => x ^ 2) (𝓝 0)).const_mul_left ((m : ℝ) ^ 2)
  have h4 := h2.trans_isBigO h3
  have h5 : (fun x : ℝ => (Real.log (1 + (m : ℝ) * x) - (m : ℝ) * x) - (-1 / 2 * (m : ℝ) ^ 2) * x ^ 2) = (fun x : ℝ => Real.log (1 + (m : ℝ) * x) - ∑ k ∈ Finset.range 2, (-1 : ℝ) ^ k * ((m : ℝ) * x) ^ (k + 1) / ((k : ℝ) + 1)) := by
    funext x
    simp only [Finset.sum_range_succ, Finset.sum_range_zero]
    push_cast
    ring
  have hf : (fun x : ℝ => (Real.log (1 + (m : ℝ) * x) - (m : ℝ) * x) - (-1 / 2 * (m : ℝ) ^ 2) * x ^ 2) =o[𝓝 0] fun x : ℝ => x ^ 2 := by
    rw [h5]
    exact h4
  have hg : (fun x : ℝ => x ^ 2 - 1 * x ^ 2) =o[𝓝 0] fun x : ℝ => x ^ 2 := by
    have e : (fun x : ℝ => x ^ 2 - 1 * x ^ 2) = fun _ => (0 : ℝ) := by
      funext x
      ring
    rw [e]
    exact Asymptotics.isLittleO_zero _ _
  have h6 := MathExam.tendsto_div_of_isLittleO (f := fun x : ℝ => Real.log (1 + (m : ℝ) * x) - (m : ℝ) * x) (g := fun x : ℝ => x ^ 2) (a := -1 / 2 * (m : ℝ) ^ 2) (b := 1) (n := 2) one_ne_zero hf hg
  have e2 : (-1 / 2 * (m : ℝ) ^ 2) / 1 = (-1 : ℝ) / 2 * (m : ℝ) ^ 2 := by ring
  rw [e2] at h6
  exact h6

#print axioms exam_answer
