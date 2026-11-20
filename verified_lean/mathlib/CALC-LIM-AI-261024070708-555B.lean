-- CALC-LIM-AI-261024070708-555B: formalize bằng LLM (haiku), kiểm chứng bằng Lean 4 + Mathlib.
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
    Filter.Tendsto (fun x : ℝ => ((1 + (m:ℝ) * x) ^ ((1:ℝ)/3) - 1) / x) (𝓝[≠] 0) (𝓝 ((((1 : ℝ) / 3) * (m : ℝ)))) := by
  have hd : HasDerivAt (fun x : ℝ => (1 + (m:ℝ)*x)^((1:ℝ)/3)) ((1:ℝ)/3 * (m:ℝ)) 0 := by
    have h1 : HasDerivAt (fun x : ℝ => 1 + (m:ℝ)*x) ((m:ℝ)*1) 0 :=
      ((hasDerivAt_id (0:ℝ)).const_mul (m:ℝ)).const_add 1
    have h2 := h1.rpow_const (p := (1:ℝ)/3) (Or.inl (by norm_num))
    exact h2.congr_deriv (by norm_num)
  have key := hasDerivAt_iff_tendsto_slope_zero.mp hd
  refine Tendsto.congr' ?_ key
  filter_upwards with t
  simp only [zero_add, mul_zero, add_zero, Real.one_rpow, smul_eq_mul]
  ring

#print axioms exam_answer
