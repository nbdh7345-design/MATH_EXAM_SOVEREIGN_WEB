-- CALC-LIM-AI-261024101541-FC0C: formalize bằng LLM (sonnet), kiểm chứng bằng Lean 4 + Mathlib.
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
    Filter.Tendsto (fun x : ℝ => (Real.arctan ((m:ℝ) * x) - Real.sin ((m:ℝ) * x)) / x ^ 3) (𝓝[≠] 0) (𝓝 ((((-1 : ℝ) / 6) * ((m : ℝ) ^ (3 : ℕ))))) := by
  have h1 : (fun x : ℝ => Real.arctan ((m:ℝ) * x) - ((m:ℝ) * x - ((m:ℝ) * x) ^ 3 / 3)) =o[𝓝 0] fun x : ℝ => x ^ 3 := by
    have := MathExam.isLittleO_comp_mul_pow (MathExam.isLittleO_pow_of_le (MathExam.arctan_maclaurin 2) (show 3 ≤ 2 * 2 by norm_num)) (m:ℝ) 1 one_pos
    refine this.congr (fun x => ?_) (fun x => ?_)
    · norm_num [Finset.sum_range_succ]
      try ring
    · simp
  have h2 : (fun x : ℝ => Real.sin ((m:ℝ) * x) - ((m:ℝ) * x - ((m:ℝ) * x) ^ 3 / 6)) =o[𝓝 0] fun x : ℝ => x ^ 3 := by
    have := MathExam.isLittleO_pow_of_le (MathExam.sin_mul_maclaurin (m:ℝ) 2) (show 3 ≤ 2 * 2 by norm_num)
    refine this.congr (fun x => ?_) (fun x => ?_)
    · norm_num [Finset.sum_range_succ, Nat.factorial]
      try ring
    · rfl
  apply MathExam.tendsto_div_pow_of_isLittleO
  exact (h1.sub h2).congr_left (fun x => by ring)

#print axioms exam_answer
