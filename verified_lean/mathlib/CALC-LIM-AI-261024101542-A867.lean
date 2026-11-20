-- CALC-LIM-AI-261024101542-A867: formalize bằng LLM (sonnet), kiểm chứng bằng Lean 4 + Mathlib.
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
    Filter.Tendsto (fun x : ℝ => (Real.sin ((m : ℝ) * x) - (m : ℝ) * x * Real.cos x) / x ^ 3) (𝓝[≠] 0) (𝓝 (((((1 : ℝ) / 2) * (m : ℝ)) + (((-1 : ℝ) / 6) * ((m : ℝ) ^ (3 : ℕ)))))) := by
  have hA := MathExam.isLittleO_pow_of_le (MathExam.sin_mul_maclaurin (m:ℝ) 2) (by norm_num : 3 ≤ 2*2)
  have hB := MathExam.isLittleO_pow_of_le (MathExam.cos_mul_maclaurin 1 1) (by norm_num : 2 ≤ 2*1+1)
  have hC : (fun x:ℝ => (m:ℝ)*x) =O[𝓝 0] fun x:ℝ => x := by
    simpa using (Asymptotics.isBigO_refl (fun x:ℝ => x) (𝓝 0)).const_mul_left (m:ℝ)
  have hD := hC.mul_isLittleO hB
  have hD' := hD.congr_right (g₂ := fun x:ℝ => x^3) (fun x => by ring)
  have hE := hA.sub hD'
  refine MathExam.tendsto_div_pow_of_isLittleO ?_
  refine hE.congr (fun x => ?_) (fun x => ?_)
  · simp [Finset.sum_range_succ, Nat.factorial]
    ring
  · ring

#print axioms exam_answer
