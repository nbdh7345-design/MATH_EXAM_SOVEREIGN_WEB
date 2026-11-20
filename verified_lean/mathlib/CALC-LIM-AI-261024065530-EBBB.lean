-- CALC-LIM-AI-261024065530-EBBB: formalize bằng LLM (haiku), kiểm chứng bằng Lean 4 + Mathlib.
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
    Filter.Tendsto (fun x : ℝ => (Real.tan ((m : ℝ) * x) - (m : ℝ) * x) / x ^ 3) (𝓝[≠] 0) (𝓝 ((((1 : ℝ) / 3) * ((m : ℝ) ^ (3 : ℕ))))) := by
  have h1 : Asymptotics.IsLittleO (𝓝 (0:ℝ)) (fun x : ℝ => Real.sin ((m:ℝ)*x) - ((m:ℝ)*x - ((m:ℝ)*x)^3/6)) (fun x : ℝ => x ^ 3) := by
      have h := MathExam.sin_mul_maclaurin (m:ℝ) 2
      have e : (fun x : ℝ => Real.sin ((m:ℝ)*x) - ((m:ℝ)*x - ((m:ℝ)*x)^3/6)) = (fun x : ℝ => Real.sin ((m:ℝ)*x) - ∑ j ∈ Finset.range 2, (-1:ℝ)^j * ((m:ℝ)*x)^(2*j+1)/((2*j+1).factorial : ℝ)) := by
        funext x
        norm_num [Finset.sum_range_succ, Nat.factorial] <;> ring
      rw [e]
      exact MathExam.isLittleO_pow_of_le h (by norm_num)
    have h2 : Asymptotics.IsLittleO (𝓝 (0:ℝ)) (fun x : ℝ => Real.cos ((m:ℝ)*x) - (1 - ((m:ℝ)*x)^2/2)) (fun x : ℝ => x ^ 3) := by
      have h := MathExam.cos_mul_maclaurin (m:ℝ) 1
      have e : (fun x : ℝ => Real.cos ((m:ℝ)*x) - (1 - ((m:ℝ)*x)^2/2)) = (fun x : ℝ => Real.cos ((m:ℝ)*x) - ∑ j ∈ Finset.range (1+1), (-1:ℝ)^j * ((m:ℝ)*x)^(2*j)/((2*j).factorial : ℝ)) := by
        funext x
        norm_num [Finset.sum_range_succ, Nat.factorial] <;> ring
      rw [e]
      exact h
    have hb : Asymptotics.IsBigO (𝓝 (0:ℝ)) (fun x : ℝ => (m:ℝ)*x) (fun _ : ℝ => (1:ℝ)) := by
      apply Asymptotics.IsBigO.of_bound 1
      have hn : Filter.Tendsto (fun x : ℝ => ‖(m:ℝ)*x‖) (𝓝 (0:ℝ)) (𝓝 0) := by
        have hc : Continuous (fun x : ℝ => ‖(m:ℝ)*x‖) := continuous_norm.comp (continuous_const.mul continuous_id)
        have := hc.tendsto (0:ℝ)
        simpa using this
      have hI : ∀ᶠ y in 𝓝 (0:ℝ), y < 1 := Iio_mem_nhds (by norm_num)
      filter_upwards [hn.eventually hI] with x hx
      simp only [norm_one, mul_one]
      exact hx.le
    have h3 : Asymptotics.IsLittleO (𝓝 (0:ℝ)) (fun x : ℝ => (m:ℝ)*x * (Real.cos ((m:ℝ)*x) - (1 - ((m:ℝ)*x)^2/2))) (fun x : ℝ => x ^ 3) := by
      have h := hb.mul_isLittleO h2
      simp only [one_mul] at h
      exact h
    have hE : (fun x : ℝ => Real.sin ((m:ℝ)*x) - (m:ℝ)*x*Real.cos ((m:ℝ)*x) - (m:ℝ)^3/3 * x^3) = (fun x : ℝ => (Real.sin ((m:ℝ)*x) - ((m:ℝ)*x - ((m:ℝ)*x)^3/6)) - (m:ℝ)*x * (Real.cos ((m:ℝ)*x) - (1 - ((m:ℝ)*x)^2/2))) := by
      funext x
      ring
    have hfin : Asymptotics.IsLittleO (𝓝 (0:ℝ)) (fun x : ℝ => Real.sin ((m:ℝ)*x) - (m:ℝ)*x*Real.cos ((m:ℝ)*x) - (m:ℝ)^3/3 * x^3) (fun x : ℝ => x ^ 3) := by
      rw [hE]
      exact h1.sub h3
    have hN : Filter.Tendsto (fun x : ℝ => (Real.sin ((m:ℝ)*x) - (m:ℝ)*x*Real.cos ((m:ℝ)*x)) / x^3) (𝓝[≠] (0:ℝ)) (𝓝 ((m:ℝ)^3/3)) :=
      MathExam.tendsto_div_pow_of_isLittleO (f := fun x : ℝ => Real.sin ((m:ℝ)*x) - (m:ℝ)*x*Real.cos ((m:ℝ)*x)) (c := (m:ℝ)^3/3) (n := 3) hfin
    have hC : Filter.Tendsto (fun x : ℝ => Real.cos ((m:ℝ)*x)) (𝓝[≠] (0:ℝ)) (𝓝 1) := by
      have hc : Continuous (fun x : ℝ => Real.cos ((m:ℝ)*x)) := Real.continuous_cos.comp (continuous_id.const_mul (m:ℝ))
      have h := (hc.tendsto (0:ℝ)).mono_left (nhdsWithin_le_nhds (s := ({0}ᶜ : Set ℝ)))
      simpa using h
    have hev : ∀ᶠ x in 𝓝[≠] (0:ℝ), Real.cos ((m:ℝ)*x) ≠ 0 := hC.eventually (eventually_ne_nhds one_ne_zero)
    have hcomp := hN.div hC one_ne_zero
    have heq : Filter.EventuallyEq (𝓝[≠] (0:ℝ)) (fun x : ℝ => (Real.sin ((m:ℝ)*x) - (m:ℝ)*x*Real.cos ((m:ℝ)*x)) / x^3 / Real.cos ((m:ℝ)*x)) (fun x : ℝ => (Real.tan ((m:ℝ)*x) - (m:ℝ)*x) / x^3) := by
      filter_upwards [hev, self_mem_nhdsWithin] with x hcos hx
      have hx' : x ≠ 0 := by simpa using hx
      simp only [Real.tan_eq_sin_div_cos]
      field_simp
      <;> ring
    have hfinal := Filter.Tendsto.congr' heq hcomp
    rw [show (m:ℝ)^3/3/1 = 1/3*(m:ℝ)^3 by ring] at hfinal
    exact hfinal

#print axioms exam_answer
