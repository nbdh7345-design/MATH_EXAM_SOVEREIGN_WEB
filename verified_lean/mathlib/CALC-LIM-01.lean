-- CALC-LIM-01: formalize bằng LLM (haiku), kiểm chứng bằng Lean 4 + Mathlib.
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
    Filter.Tendsto (fun x : ℝ => 6 * (Real.exp ((m:ℝ) * x) - 1 - Real.sin ((m:ℝ) * x) - (m:ℝ)^2 * x^2 / 2) / x^3) (𝓝[≠] 0) (𝓝 (((2 : ℝ) * ((m : ℝ) ^ (3 : ℕ))))) := by
  have hE : (fun x : ℝ => Real.exp ((m:ℝ)*x) - (1 + (m:ℝ)*x + (m:ℝ)^2*x^2/2 + (m:ℝ)^3*x^3/6)) =o[𝓝 0] fun x : ℝ => x^3 := by
    convert MathExam.exp_maclaurin (m:ℝ) 3 using 1
    funext x
    norm_num [Finset.sum_range_succ, Nat.factorial] <;> ring
  have hS : (fun x : ℝ => Real.sin ((m:ℝ)*x) - ((m:ℝ)*x - (m:ℝ)^3*x^3/6)) =o[𝓝 0] fun x : ℝ => x^3 := by
    convert MathExam.isLittleO_pow_of_le (MathExam.sin_mul_maclaurin (m:ℝ) 2) (show 3 ≤ 2*2 by norm_num) using 1
    funext x
    norm_num [Finset.sum_range_succ, Nat.factorial] <;> ring
  have hf : (fun x : ℝ => 6 * (Real.exp ((m:ℝ)*x) - 1 - Real.sin ((m:ℝ)*x) - (m:ℝ)^2*x^2/2) - 2*(m:ℝ)^3 * x^3) =o[𝓝 0] fun x : ℝ => x^3 := by
    refine ((hE.const_mul_left 6).sub (hS.const_mul_left 6)).congr' ?_ EventuallyEq.rfl
    refine Filter.Eventually.of_forall (fun x => ?_)
    dsimp only
    ring
  have hg : (fun x : ℝ => x^3 - 1 * x^3) =o[𝓝 0] fun x : ℝ => x^3 := by
    simp
  have key := MathExam.tendsto_div_of_isLittleO (f := fun x : ℝ => 6 * (Real.exp ((m:ℝ)*x) - 1 - Real.sin ((m:ℝ)*x) - (m:ℝ)^2*x^2/2)) (g := fun x : ℝ => x^3) (a := 2*(m:ℝ)^3) (b := 1) (n := 3) one_ne_zero hf hg
  rw [div_one] at key
  exact key

#print axioms exam_answer
