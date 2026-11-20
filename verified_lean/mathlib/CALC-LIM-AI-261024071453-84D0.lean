-- CALC-LIM-AI-261024071453-84D0: formalize bằng LLM (haiku), kiểm chứng bằng Lean 4 + Mathlib.
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

theorem aux_sin5 : (fun y : ℝ => Real.sin y - (y - y ^ 3 / 6 + y ^ 5 / 120)) =o[𝓝 0] (fun y : ℝ => y ^ 5) := by
  have h := MathExam.isLittleO_pow_of_le (MathExam.sin_mul_maclaurin 1 3) (by norm_num : (5:ℕ) ≤ 2 * 3)
  have e : (fun x : ℝ => Real.sin x - (x - x ^ 3 / 6 + x ^ 5 / 120)) = (fun x : ℝ => Real.sin (1 * x) - ∑ j ∈ Finset.range 3, (-1 : ℝ) ^ j * (1 * x) ^ (2 * j + 1) / (Nat.factorial (2 * j + 1) : ℝ)) := by
    funext x
    norm_num [Finset.sum_range_succ, Nat.factorial] <;> ring
  rw [e]
  exact h

theorem aux_cos5 : (fun y : ℝ => Real.cos y - (1 - y ^ 2 / 2 + y ^ 4 / 24)) =o[𝓝 0] (fun y : ℝ => y ^ 5) := by
  have h := MathExam.cos_mul_maclaurin 1 2
  have e : (fun x : ℝ => Real.cos x - (1 - x ^ 2 / 2 + x ^ 4 / 24)) = (fun x : ℝ => Real.cos (1 * x) - ∑ j ∈ Finset.range (2 + 1), (-1 : ℝ) ^ j * (1 * x) ^ (2 * j) / (Nat.factorial (2 * j) : ℝ)) := by
    funext x
    norm_num [Finset.sum_range_succ, Nat.factorial] <;> ring
  rw [e]
  exact h

theorem aux_tan5 : (fun y : ℝ => Real.tan y - (y + y ^ 3 / 3 + 2 * y ^ 5 / 15)) =o[𝓝 0] (fun y : ℝ => y ^ 5) := by
  have hP : Filter.Tendsto (fun y : ℝ => y + y ^ 3 / 3 + 2 * y ^ 5 / 15) (𝓝 0) (𝓝 0) := by
    have hcont : Continuous (fun y : ℝ => y + y ^ 3 / 3 + 2 * y ^ 5 / 15) := by fun_prop
    simpa using hcont.tendsto 0
  have hPO : (fun y : ℝ => y + y ^ 3 / 3 + 2 * y ^ 5 / 15) =O[𝓝 0] (fun _ : ℝ => (1 : ℝ)) :=
    hP.isBigO_one
  have hcos : Filter.Tendsto (fun y : ℝ => Real.cos y) (𝓝 0) (𝓝 1) := by
    have h := Real.continuous_cos.tendsto 0
    simpa using h
  have hne : ∀ᶠ y in 𝓝 (0 : ℝ), Real.cos y ≠ 0 := hcos.eventually_ne one_ne_zero
  have hcinv : Filter.Tendsto (fun y : ℝ => (Real.cos y)⁻¹) (𝓝 0) (𝓝 1) := by
    have h := hcos.inv₀ one_ne_zero
    simpa using h
  have hinvO : (fun y : ℝ => (Real.cos y)⁻¹) =O[𝓝 0] (fun _ : ℝ => (1 : ℝ)) :=
    hcinv.isBigO_one
  have hs := aux_sin5
  have hc := aux_cos5
  have hq : (fun y : ℝ => (19 / 360 * y ^ 2 - y ^ 4 / 180) * y ^ 5) =o[𝓝 0] (fun y : ℝ => y ^ 5) := by
    have hk : Filter.Tendsto (fun y : ℝ => 19 / 360 * y ^ 2 - y ^ 4 / 180) (𝓝 0) (𝓝 0) := by
      have hcont : Continuous (fun y : ℝ => 19 / 360 * y ^ 2 - y ^ 4 / 180) := by fun_prop
      simpa using hcont.tendsto 0
    have hk1 : (fun y : ℝ => 19 / 360 * y ^ 2 - y ^ 4 / 180) =o[𝓝 0] (fun _ : ℝ => (1 : ℝ)) := by
      first
        | exact (Asymptotics.isLittleO_one_iff ℝ).2 hk
        | exact (Asymptotics.isLittleO_one_iff).2 hk
    have h := hk1.mul_isBigO (Asymptotics.isBigO_refl (fun y : ℝ => y ^ 5) (𝓝 0))
    simp only [one_mul] at h
    exact h
  have hmul := hPO.mul_isLittleO hc
  simp only [one_mul] at hmul
  have hfun : (fun y : ℝ => Real.sin y - (y + y ^ 3 / 3 + 2 * y ^ 5 / 15) * Real.cos y)
      = (fun y : ℝ => (Real.sin y - (y - y ^ 3 / 6 + y ^ 5 / 120)) - (y + y ^ 3 / 3 + 2 * y ^ 5 / 15) * (Real.cos y - (1 - y ^ 2 / 2 + y ^ 4 / 24)) + (19 / 360 * y ^ 2 - y ^ 4 / 180) * y ^ 5) := by
    funext y
    ring
  have hA : (fun y : ℝ => Real.sin y - (y + y ^ 3 / 3 + 2 * y ^ 5 / 15) * Real.cos y) =o[𝓝 0] (fun y : ℝ => y ^ 5) := by
    rw [hfun]
    exact (hs.sub hmul).add hq
  have hEq : (fun y : ℝ => Real.tan y - (y + y ^ 3 / 3 + 2 * y ^ 5 / 15)) =ᶠ[𝓝 0] (fun y : ℝ => (Real.sin y - (y + y ^ 3 / 3 + 2 * y ^ 5 / 15) * Real.cos y) * (Real.cos y)⁻¹) := by
    filter_upwards [hne] with y hy
    show Real.tan y - (y + y ^ 3 / 3 + 2 * y ^ 5 / 15) = (Real.sin y - (y + y ^ 3 / 3 + 2 * y ^ 5 / 15) * Real.cos y) * (Real.cos y)⁻¹
    rw [Real.tan_eq_sin_div_cos]
    simp only [div_eq_mul_inv]
    rw [sub_mul, mul_inv_cancel_right₀ hy]
  have hmain : (fun y : ℝ => (Real.sin y - (y + y ^ 3 / 3 + 2 * y ^ 5 / 15) * Real.cos y) * (Real.cos y)⁻¹) =o[𝓝 0] (fun y : ℝ => y ^ 5) := by
    have h := hA.mul_isBigO hinvO
    simp only [mul_one] at h
    exact h
  first
    | exact hmain.congr' hEq (Filter.EventuallyEq.refl _ _)
    | exact hmain.congr' hEq.symm (Filter.EventuallyEq.refl _ _)

theorem exam_answer (m : ℕ) (hm_lo : 2 ≤ m) (hm_hi : m ≤ 9) :
    Filter.Tendsto (fun x : ℝ => (Real.tan ((m : ℝ) * x) - (m : ℝ) * x - (m : ℝ) ^ 3 * x ^ 3 / 3) / x ^ 5) (𝓝[≠] (0 : ℝ)) (𝓝 ((((2 : ℝ) / 15) * ((m : ℝ) ^ (5 : ℕ))))) := by
  have hL : Filter.Tendsto (fun x : ℝ => (m : ℝ) * x) (𝓝 0) (𝓝 0) := by
    have h := (continuous_const.mul continuous_id : Continuous fun x : ℝ => (m : ℝ) * x).tendsto 0
    simpa using h
  have h2 : (fun x : ℝ => Real.tan ((m : ℝ) * x) - ((m : ℝ) * x + ((m : ℝ) * x) ^ 3 / 3 + 2 * ((m : ℝ) * x) ^ 5 / 15)) =o[𝓝 0] (fun x : ℝ => ((m : ℝ) * x) ^ 5) :=
    aux_tan5.comp_tendsto hL
  have hO : (fun x : ℝ => ((m : ℝ) * x) ^ 5) =O[𝓝 0] (fun x : ℝ => x ^ 5) := by
    have e5 : (fun x : ℝ => ((m : ℝ) * x) ^ 5) = (fun x : ℝ => (m : ℝ) ^ 5 * x ^ 5) := by
      funext x
      ring
    rw [e5]
    exact (Asymptotics.isBigO_refl (fun x : ℝ => x ^ 5) (𝓝 0)).const_mul_left ((m : ℝ) ^ 5)
  have h3 := h2.trans_isBigO hO
  have hF : (fun x : ℝ => (Real.tan ((m : ℝ) * x) - (m : ℝ) * x - (m : ℝ) ^ 3 * x ^ 3 / 3) - 2 / 15 * (m : ℝ) ^ 5 * x ^ 5) =o[𝓝 0] (fun x : ℝ => x ^ 5) := by
    have e : (fun x : ℝ => (Real.tan ((m : ℝ) * x) - (m : ℝ) * x - (m : ℝ) ^ 3 * x ^ 3 / 3) - 2 / 15 * (m : ℝ) ^ 5 * x ^ 5) = (fun x : ℝ => Real.tan ((m : ℝ) * x) - ((m : ℝ) * x + ((m : ℝ) * x) ^ 3 / 3 + 2 * ((m : ℝ) * x) ^ 5 / 15)) := by
      funext x
      ring
    rw [e]
    exact h3
  have hg : (fun x : ℝ => x ^ 5 - 1 * x ^ 5) =o[𝓝 0] (fun x : ℝ => x ^ 5) := by
    have e0 : (fun x : ℝ => x ^ 5 - 1 * x ^ 5) = (fun _ : ℝ => (0 : ℝ)) := by
      funext x
      ring
    rw [e0]
    exact Asymptotics.isLittleO_zero _ _
  have key := MathExam.tendsto_div_of_isLittleO (f := fun x : ℝ => Real.tan ((m : ℝ) * x) - (m : ℝ) * x - (m : ℝ) ^ 3 * x ^ 3 / 3) (g := fun x : ℝ => x ^ 5) (a := 2 / 15 * (m : ℝ) ^ 5) (b := 1) (n := 5) one_ne_zero hF hg
  rw [div_one] at key
  exact key

#print axioms exam_answer
