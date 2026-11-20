-- CALC-LIM-AI-261024070534-6127: formalize bằng LLM (haiku), kiểm chứng bằng Lean 4 + Mathlib.
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

theorem exam_sin_part (a : ℝ) : (fun x : ℝ => Real.sin (a * x) - (a * x - (a * x) ^ 3 / 6)) =o[𝓝 0] fun x : ℝ => x ^ 3 := by
  have h := MathExam.isLittleO_pow_of_le (MathExam.sin_mul_maclaurin a 2) (show 3 ≤ 2 * 2 by norm_num)
  refine h.congr' (Filter.Eventually.of_forall fun x => ?_) Filter.EventuallyEq.rfl
  norm_num [Finset.sum_range_succ, Nat.factorial]
  ring

theorem exam_cos_part (a : ℝ) : (fun x : ℝ => Real.cos (a * x) - (1 - (a * x) ^ 2 / 2)) =o[𝓝 0] fun x : ℝ => x ^ 3 := by
  have h := MathExam.cos_mul_maclaurin a 1
  refine h.congr' (Filter.Eventually.of_forall fun x => ?_) Filter.EventuallyEq.rfl
  norm_num [Finset.sum_range_succ, Nat.factorial]
  ring

theorem exam_key (a : ℝ) : (fun x : ℝ => Real.sin (a * x) - a * x * Real.cos (a * x) - a ^ 3 / 3 * x ^ 3) =o[𝓝 0] fun x : ℝ => x ^ 3 := by
  have hlin : (fun x : ℝ => a * x) =O[𝓝 0] (1 : ℝ → ℝ) := by
    have ht : Filter.Tendsto (fun x : ℝ => a * x) (𝓝 0) (𝓝 0) := by
      have hc : Continuous (fun x : ℝ => a * x) := by fun_prop
      simpa using hc.tendsto 0
    exact ht.isBigO_one ℝ
  have h2 := (exam_cos_part a).mul_isBigO hlin
  have h2' : (fun x : ℝ => (Real.cos (a * x) - (1 - (a * x) ^ 2 / 2)) * (a * x)) =o[𝓝 0] fun x : ℝ => x ^ 3 :=
    h2.congr' Filter.EventuallyEq.rfl (Filter.Eventually.of_forall fun x => by simp)
  have h3 := (exam_sin_part a).sub h2'
  exact h3.congr' (Filter.Eventually.of_forall fun x => by dsimp only; ring) Filter.EventuallyEq.rfl

theorem exam_answer (m : ℕ) (hm_lo : 2 ≤ m) (hm_hi : m ≤ 9) :
    Filter.Tendsto (fun x : ℝ => (Real.tan ((m : ℝ) * x) - (m : ℝ) * x) / x ^ 3) (𝓝[≠] 0) (𝓝 ((((1 : ℝ) / 3) * ((m : ℝ) ^ (3 : ℕ))))) := by
  have hN := exam_key (m : ℝ)
    have hG : Filter.Tendsto (fun x : ℝ => (Real.sin ((m : ℝ) * x) - (m : ℝ) * x * Real.cos ((m : ℝ) * x)) / x ^ 3) (𝓝[≠] (0 : ℝ)) (𝓝 ((m : ℝ) ^ 3 / 3)) :=
      MathExam.tendsto_div_pow_of_isLittleO (f := fun x : ℝ => Real.sin ((m : ℝ) * x) - (m : ℝ) * x * Real.cos ((m : ℝ) * x)) (c := (m : ℝ) ^ 3 / 3) (n := 3) hN
    have hcos : Filter.Tendsto (fun x : ℝ => Real.cos ((m : ℝ) * x)) (𝓝[≠] (0 : ℝ)) (𝓝 1) := by
      have hc : Continuous (fun x : ℝ => Real.cos ((m : ℝ) * x)) := by fun_prop
      have h0 : Filter.Tendsto (fun x : ℝ => Real.cos ((m : ℝ) * x)) (𝓝 (0 : ℝ)) (𝓝 1) := by
        have := hc.tendsto (0 : ℝ)
        simpa using this
      exact tendsto_nhdsWithin_of_tendsto_nhds h0
    have hinv : Filter.Tendsto (fun x : ℝ => (Real.cos ((m : ℝ) * x))⁻¹) (𝓝[≠] (0 : ℝ)) (𝓝 1) := by
      have := hcos.inv₀ one_ne_zero
      rw [inv_one] at this
      exact this
    have hprod := hG.mul hinv
    rw [mul_one] at hprod
    have heq : (fun x : ℝ => (Real.sin ((m : ℝ) * x) - (m : ℝ) * x * Real.cos ((m : ℝ) * x)) / x ^ 3 * (Real.cos ((m : ℝ) * x))⁻¹) =ᶠ[𝓝[≠] (0 : ℝ)] (fun x : ℝ => (Real.tan ((m : ℝ) * x) - (m : ℝ) * x) / x ^ 3) := by
      filter_upwards [hcos.eventually_ne one_ne_zero] with x hx
      show (Real.sin ((m : ℝ) * x) - (m : ℝ) * x * Real.cos ((m : ℝ) * x)) / x ^ 3 * (Real.cos ((m : ℝ) * x))⁻¹ = (Real.tan ((m : ℝ) * x) - (m : ℝ) * x) / x ^ 3
      have key : (Real.sin ((m : ℝ) * x) - (m : ℝ) * x * Real.cos ((m : ℝ) * x)) * (Real.cos ((m : ℝ) * x))⁻¹ = Real.tan ((m : ℝ) * x) - (m : ℝ) * x := by
        rw [Real.tan_eq_sin_div_cos, sub_mul, mul_inv_cancel_right₀ hx, div_eq_mul_inv]
      rw [← key]
      ring
    have hval : (1 : ℝ) / 3 * ((m : ℝ) ^ (3 : ℕ)) = (m : ℝ) ^ 3 / 3 := by ring
    rw [hval]
    exact Filter.Tendsto.congr' heq hprod

#print axioms exam_answer
