-- CALC-LIM-AI-261024070829-B694: formalize bằng LLM (haiku), kiểm chứng bằng Lean 4 + Mathlib.
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

lemma my_sin_exp3 : (fun y : ℝ => sin y - (y - y ^ 3 / 6)) =o[𝓝 0] (fun y : ℝ => y ^ 3) := by
  have h := MathExam.sin_mul_maclaurin 1 2
  have h' := MathExam.isLittleO_pow_of_le h (by norm_num : 3 ≤ 2 * 2)
  refine h'.congr' (Filter.Eventually.of_forall fun y => ?_) (Filter.Eventually.of_forall fun y => ?_)
  · norm_num [Finset.sum_range_succ, Nat.factorial] <;> ring
  · norm_num

lemma my_cos_exp2 : (fun y : ℝ => cos y - (1 - y ^ 2 / 2)) =o[𝓝 0] (fun y : ℝ => y ^ 3) := by
  have h := MathExam.cos_mul_maclaurin 1 1
  refine h.congr' (Filter.Eventually.of_forall fun y => ?_) (Filter.Eventually.of_forall fun y => ?_)
  · norm_num [Finset.sum_range_succ, Nat.factorial] <;> ring
  · norm_num

lemma my_tan_exp3 : (fun y : ℝ => tan y - y - y ^ 3 / 3) =o[𝓝 0] (fun y : ℝ => y ^ 3) := by
  have hcinv : Filter.Tendsto (fun y : ℝ => (cos y)⁻¹) (𝓝 0) (𝓝 1) := by
    have h := (Real.continuous_cos.tendsto (0:ℝ)).inv₀ (by simp : cos (0:ℝ) ≠ 0)
    simpa using h
  have hinv : (fun y : ℝ => (cos y)⁻¹) =O[𝓝 0] (fun _ : ℝ => (1:ℝ)) :=
    hcinv.isBigO_one ℝ
  have hidT : Filter.Tendsto (fun y : ℝ => y) (𝓝 0) (𝓝 0) :=
    (continuous_id.tendsto (0:ℝ))
  have hid : (fun y : ℝ => y) =O[𝓝 0] (fun _ : ℝ => (1:ℝ)) :=
    hidT.isBigO_one ℝ
  have hc2 : Filter.Tendsto (fun y : ℝ => y ^ 2 / 6) (𝓝 0) (𝓝 0) := by
    simpa using ((continuous_pow 2).div_const (6:ℝ)).tendsto (0:ℝ)
  have hy2 : (fun y : ℝ => y ^ 2 / 6) =o[𝓝 0] (fun _ : ℝ => (1:ℝ)) := by
    rw [Asymptotics.isLittleO_one_iff]
    exact hc2
  have hc3 : Filter.Tendsto (fun y : ℝ => y ^ 3 / 3) (𝓝 0) (𝓝 0) := by
    simpa using ((continuous_pow 3).div_const (3:ℝ)).tendsto (0:ℝ)
  have hbig : (fun y : ℝ => y ^ 3 / 3) =O[𝓝 0] (fun _ : ℝ => (1:ℝ)) :=
    hc3.isBigO_one ℝ
  have hv2 : (fun y : ℝ => (cos y - (1 - y ^ 2 / 2)) * y) =o[𝓝 0] (fun y : ℝ => y ^ 3) := by
    have h := my_cos_exp2.mul_isBigO hid
    refine h.congr' (Filter.Eventually.of_forall fun y => ?_) (Filter.Eventually.of_forall fun y => ?_)
    · ring
    · ring
  have hyv3 : (fun y : ℝ => (y ^ 3 / 3) * (cos y - (1 - y ^ 2 / 2))) =o[𝓝 0] (fun y : ℝ => y ^ 3) := by
    have h := hbig.mul_isLittleO my_cos_exp2
    refine h.congr' (Filter.Eventually.of_forall fun y => ?_) (Filter.Eventually.of_forall fun y => ?_)
    · rfl
    · ring
  have hy5 : (fun y : ℝ => (y ^ 2 / 6) * y ^ 3) =o[𝓝 0] (fun y : ℝ => y ^ 3) := by
    have h := hy2.mul_isBigO (Asymptotics.isBigO_refl (fun y : ℝ => y ^ 3) (𝓝 0))
    refine h.congr' (Filter.Eventually.of_forall fun y => ?_) (Filter.Eventually.of_forall fun y => ?_)
    · rfl
    · simp
  have hN : (fun y : ℝ => sin y - y * cos y - y ^ 3 / 3 * cos y) =o[𝓝 0] (fun y : ℝ => y ^ 3) := by
    have hA := ((my_sin_exp3.sub hv2).sub hyv3).add hy5
    refine hA.congr' (Filter.Eventually.of_forall fun y => ?_) (Filter.Eventually.of_forall fun y => rfl)
    ring
  have hev : Set.Ioo (-(π / 2)) (π / 2) ∈ 𝓝 (0:ℝ) :=
    Ioo_mem_nhds (by linarith [Real.pi_pos]) (by linarith [Real.pi_pos])
  have hfin := hN.mul_isBigO hinv
  refine hfin.congr' ?_ (Filter.Eventually.of_forall fun y => by simp)
  filter_upwards [hev] with y hy
  have hc : 0 < cos y := Real.cos_pos_of_mem_Ioo hy
  have hc' : cos y ≠ 0 := hc.ne'
  rw [Real.tan_eq_sin_div_cos]
  field_simp <;> ring

lemma my_tan_scaled (a : ℝ) :
    Filter.Tendsto (fun x : ℝ => (tan (a * x) - a * x) / x ^ 3) (𝓝[≠] 0) (𝓝 (1 / 3 * a ^ 3)) := by
  have hk : Filter.Tendsto (fun x : ℝ => a * x) (𝓝 0) (𝓝 0) := by
    simpa using ((continuous_id.const_mul a).tendsto (0:ℝ))
  have H := my_tan_exp3.comp_tendsto hk
  have hO : (fun x : ℝ => (a * x) ^ 3) =O[𝓝 0] (fun x : ℝ => x ^ 3) := by
    have h := (Asymptotics.isBigO_refl (fun x : ℝ => x ^ 3) (𝓝 0)).const_mul_left (a ^ 3)
    refine h.congr' (Filter.Eventually.of_forall fun x => ?_) (Filter.Eventually.of_forall fun x => rfl)
    ring
  have H3 : (fun x : ℝ => (tan (a * x) - a * x) - 1 / 3 * a ^ 3 * x ^ 3) =o[𝓝 0] (fun x : ℝ => (a * x) ^ 3) := by
    refine H.congr' (Filter.Eventually.of_forall fun x => ?_) (Filter.Eventually.of_forall fun x => rfl)
    simp only [Function.comp_apply]
    ring
  have H2 : (fun x : ℝ => (tan (a * x) - a * x) - 1 / 3 * a ^ 3 * x ^ 3) =o[𝓝 0] (fun x : ℝ => x ^ 3) :=
    H3.trans_isBigO hO
  exact MathExam.tendsto_div_pow_of_isLittleO (f := fun x : ℝ => tan (a * x) - a * x) (c := 1 / 3 * a ^ 3) (n := 3) H2

theorem exam_answer (m : ℕ) (hm_lo : 2 ≤ m) (hm_hi : m ≤ 9) :
    Filter.Tendsto (fun x : ℝ => (tan ((m : ℝ) * x) - (m : ℝ) * x) / x ^ 3) (𝓝[≠] 0) (𝓝 ((((1 : ℝ) / 3) * ((m : ℝ) ^ (3 : ℕ))))) := by
  exact my_tan_scaled (m : ℝ)

#print axioms exam_answer
