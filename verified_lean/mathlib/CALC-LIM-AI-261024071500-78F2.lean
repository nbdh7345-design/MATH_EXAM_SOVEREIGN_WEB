-- CALC-LIM-AI-261024071500-78F2: formalize bằng LLM (haiku), kiểm chứng bằng Lean 4 + Mathlib.
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

theorem aux_sin_o (a : ℝ) : (fun x : ℝ => sin (a * x) - (a * x - (a * x) ^ 3 / 6)) =o[𝓝 0] fun x : ℝ => x ^ 3 := by
  have hf : (fun x : ℝ => sin (a * x) - (a * x - (a * x) ^ 3 / 6)) = (fun x : ℝ => sin (a * x) - ∑ j ∈ Finset.range 2, (-1 : ℝ) ^ j * (a * x) ^ (2 * j + 1) / ((2 * j + 1).factorial : ℝ)) := by
    funext x
    norm_num [Finset.sum_range_succ, Nat.factorial] <;> ring
  rw [hf]
  exact MathExam.isLittleO_pow_of_le (MathExam.sin_mul_maclaurin a 2) (by norm_num)

theorem aux_cos_o (a : ℝ) : (fun x : ℝ => cos (a * x) - (1 - (a * x) ^ 2 / 2)) =o[𝓝 0] fun x : ℝ => x ^ 3 := by
  have hf : (fun x : ℝ => cos (a * x) - (1 - (a * x) ^ 2 / 2)) = (fun x : ℝ => cos (a * x) - ∑ j ∈ Finset.range (1 + 1), (-1 : ℝ) ^ j * (a * x) ^ (2 * j) / ((2 * j).factorial : ℝ)) := by
    funext x
    norm_num [Finset.sum_range_succ, Nat.factorial] <;> ring
  rw [hf]
  exact MathExam.cos_mul_maclaurin a 1

theorem aux_N_o (a : ℝ) : (fun x : ℝ => (sin (a * x) - a * x * cos (a * x)) - a ^ 3 / 3 * x ^ 3) =o[𝓝 0] fun x : ℝ => x ^ 3 := by
  have hO : (fun x : ℝ => a * x) =O[𝓝 0] (fun _ : ℝ => (1 : ℝ)) := by
    refine Asymptotics.IsBigO.of_bound (|a| + 1) ?_
    filter_upwards [Metric.ball_mem_nhds (0:ℝ) one_pos] with x hx
    rw [Metric.mem_ball, Real.dist_eq, sub_zero] at hx
    simp only [Real.norm_eq_abs, abs_mul, abs_one, mul_one]
    nlinarith [abs_nonneg a, abs_nonneg x]
  have hP' : (fun x : ℝ => (cos (a * x) - (1 - (a * x) ^ 2 / 2)) * (a * x)) =o[𝓝 0] fun x : ℝ => x ^ 3 := by
    have hP := (aux_cos_o a).mul_isBigO hO
    simpa using hP
  have hfun : (fun x : ℝ => (sin (a * x) - a * x * cos (a * x)) - a ^ 3 / 3 * x ^ 3) = (fun x : ℝ => (sin (a * x) - (a * x - (a * x) ^ 3 / 6)) - (cos (a * x) - (1 - (a * x) ^ 2 / 2)) * (a * x)) := by
    funext x
    ring
  rw [hfun]
  exact (aux_sin_o a).sub hP'

theorem exam_answer (m : ℕ) (hm_lo : 2 ≤ m) (hm_hi : m ≤ 9) :
    Filter.Tendsto (fun x : ℝ => (Real.tan ((m : ℝ) * x) - (m : ℝ) * x) / x ^ 3) (𝓝[≠] 0) (𝓝 ((((1 : ℝ) / 3) * ((m : ℝ) ^ (3 : ℕ))))) := by
  have hcos : Filter.Tendsto (fun x : ℝ => cos ((m : ℝ) * x)) (𝓝[≠] 0) (𝓝 1) := by
      have hc : Continuous (fun x : ℝ => cos ((m : ℝ) * x)) := by fun_prop
      have h1 : Filter.Tendsto (fun x : ℝ => cos ((m : ℝ) * x)) (𝓝 0) (𝓝 1) := by
        simpa using hc.tendsto 0
      exact h1.mono_left nhdsWithin_le_nhds
    have hne : ∀ᶠ x in 𝓝[≠] (0 : ℝ), cos ((m : ℝ) * x) ≠ 0 := hcos.eventually_ne one_ne_zero
    have hinv : Filter.Tendsto (fun x : ℝ => (cos ((m : ℝ) * x))⁻¹) (𝓝[≠] 0) (𝓝 1) := by
      simpa using hcos.inv₀ one_ne_zero
    have hNl : Filter.Tendsto (fun x : ℝ => (sin ((m : ℝ) * x) - (m : ℝ) * x * cos ((m : ℝ) * x)) / x ^ 3) (𝓝[≠] 0) (𝓝 ((m : ℝ) ^ 3 / 3)) :=
      MathExam.tendsto_div_pow_of_isLittleO (aux_N_o (m : ℝ))
    have hprod := hNl.mul hinv
    have heq : (fun x : ℝ => (sin ((m : ℝ) * x) - (m : ℝ) * x * cos ((m : ℝ) * x)) / x ^ 3 * (cos ((m : ℝ) * x))⁻¹) =ᶠ[𝓝[≠] (0 : ℝ)] (fun x : ℝ => (Real.tan ((m : ℝ) * x) - (m : ℝ) * x) / x ^ 3) := by
      filter_upwards [hne, self_mem_nhdsWithin] with x hx hx0
      have hx0' : x ≠ 0 := hx0
      rw [Real.tan_eq_sin_div_cos]
      field_simp
    have hlim : (m : ℝ) ^ 3 / 3 * 1 = (1 / 3) * ((m : ℝ) ^ (3 : ℕ)) := by ring
    rw [hlim] at hprod
    exact Filter.Tendsto.congr' heq hprod

#print axioms exam_answer
