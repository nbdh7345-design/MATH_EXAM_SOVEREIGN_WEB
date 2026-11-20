-- PN-Putnam_exercise_1998_a3: FR09 (dung), Lean 4 + Mathlib; dòng khai báo định lý do hệ thống viết.
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
import Mathlib.Analysis.Convex.Function
import Mathlib.Analysis.Convex.Deriv
import Mathlib.Topology.Bornology.Basic
import Mathlib.Topology.UniformSpace.UniformConvergence
import Mathlib.Order.LiminfLimsup
import Mathlib.Data.EReal.Basic
import Mathlib.Data.PNat.Basic
import Mathlib.Analysis.Calculus.Deriv.Inverse
import Mathlib.Topology.Order.IntermediateValue
import Mathlib.Analysis.Calculus.LocalExtr.Basic
import Mathlib.Analysis.SpecialFunctions.Trigonometric.ArctanDeriv
import Mathlib.Analysis.Calculus.MeanValue
import Mathlib.Topology.MetricSpace.Basic
import MathExam
set_option autoImplicit false
set_option maxHeartbeats 400000


open scoped BigOperators

lemma ex98_sign (F : ℝ → ℝ) (hc : Continuous F) (h0 : ∀ x, F x ≠ 0) :
    (∀ x, 0 < F x) ∨ (∀ x, F x < 0) := by
  by_contra h
  push_neg at h
  obtain ⟨⟨a, ha⟩, ⟨b, hb⟩⟩ := h
  have ha' : F a < 0 := lt_of_le_of_ne ha (h0 a)
  have hb' : 0 < F b := lt_of_le_of_ne hb (h0 b).symm
  have hmem : (0:ℝ) ∈ Set.uIcc (F a) (F b) := Set.mem_uIcc.2 (Or.inl ⟨ha'.le, hb'.le⟩)
  obtain ⟨c, _, hc0⟩ := intermediate_value_uIcc hc.continuousOn hmem
  exact h0 c hc0

lemma ex98_mvt (F G : ℝ → ℝ) (dF : ∀ x, HasDerivAt F (G x) x) (a b : ℝ) (hab : a < b) :
    ∃ c, a < c ∧ c < b ∧ F b - F a = G c * (b - a) := by
  obtain ⟨c, hc, h⟩ := exists_hasDerivAt_eq_slope F G hab
    (fun x _ => (dF x).continuousAt.continuousWithinAt) (fun x _ => dF x)
  refine ⟨c, hc.1, hc.2, ?_⟩
  have hne : b - a ≠ 0 := sub_ne_zero.mpr hab.ne'
  rw [h]
  field_simp

lemma ex98_anti (G H : ℝ → ℝ) (dG : ∀ x, HasDerivAt G (H x) x) (hH : ∀ x, H x < 0) :
    ∀ a b, a < b → G b < G a := by
  intro a b hab
  obtain ⟨c, _, _, h⟩ := ex98_mvt G H dG a b hab
  have := mul_neg_of_neg_of_pos (hH c) (sub_pos.2 hab)
  linarith

lemma ex98_A (F G H : ℝ → ℝ) (dF : ∀ x, HasDerivAt F (G x) x) (dG : ∀ x, HasDerivAt G (H x) x)
    (hH : ∀ x, H x < 0) (hF : ∀ x, 0 < F x) : False := by
  have anti := ex98_anti G H dG hH
  by_cases h : G 1 < 0
  · obtain ⟨t, htpos, ht⟩ : ∃ t : ℝ, 0 < t ∧ G 1 * t = -(|F 1| + 1) :=
      ⟨(|F 1| + 1) / (-G 1), div_pos (by linarith [abs_nonneg (F 1)]) (by linarith), by
        have hne : G 1 ≠ 0 := h.ne
        field_simp⟩
    obtain ⟨c, hc1, _, hc⟩ := ex98_mvt F G dF 1 (1 + t) (by linarith)
    have hlt : G c < G 1 := anti 1 c hc1
    have h2 : G c * (1 + t - 1) < G 1 * t := by
      have e : 1 + t - 1 = t := by ring
      rw [e]
      exact mul_lt_mul_of_pos_right hlt htpos
    have h3 := hF (1 + t)
    have h4 := le_abs_self (F 1)
    linarith
  · push_neg at h
    have hg : 0 < G 0 := lt_of_le_of_lt h (anti 0 1 (by norm_num))
    obtain ⟨t, htpos, ht⟩ : ∃ t : ℝ, 0 < t ∧ G 0 * t = (|F 0| + 1) :=
      ⟨(|F 0| + 1) / G 0, div_pos (by linarith [abs_nonneg (F 0)]) hg, by
        have hne : G 0 ≠ 0 := hg.ne'
        field_simp⟩
    obtain ⟨c, _, hc2, hc⟩ := ex98_mvt F G dF (-t) 0 (by linarith)
    have hlt : G 0 < G c := anti c 0 hc2
    have h2 : G 0 * (0 - -t) < G c * (0 - -t) := by
      have e : (0:ℝ) - -t = t := by ring
      rw [e]
      exact mul_lt_mul_of_pos_right hlt htpos
    have h3 := hF (-t)
    have h4 := le_abs_self (F 0)
    have e : (0:ℝ) - -t = t := by ring
    rw [e] at h2 hc
    linarith

lemma ex98_B (F G H : ℝ → ℝ) (dF : ∀ x, HasDerivAt F (G x) x) (dG : ∀ x, HasDerivAt G (H x) x)
    (hFc : Continuous F) (hHc : Continuous H) (hF0 : ∀ x, F x ≠ 0) (hH0 : ∀ x, H x ≠ 0) :
    0 < F 0 * H 0 := by
  rcases ex98_sign F hFc hF0 with hF1 | hF1
  · rcases ex98_sign H hHc hH0 with hH1 | hH1
    · exact mul_pos (hF1 0) (hH1 0)
    · exact (ex98_A F G H dF dG hH1 hF1).elim
  · rcases ex98_sign H hHc hH0 with hH1 | hH1
    · exact (ex98_A (fun x => -F x) (fun x => -G x) (fun x => -H x)
        (fun x => (dF x).neg) (fun x => (dG x).neg)
        (fun x => by show -H x < 0; linarith [hH1 x])
        (fun x => by show 0 < -F x; linarith [hF1 x])).elim
    · exact mul_pos_of_neg_of_neg (hF1 0) (hH1 0)

theorem exercise_1998_a3 (f : ℝ → ℝ) (hf : ContDiff ℝ 3 f) :
    ∃ a : ℝ, (f a) * (deriv f a) * (iteratedDeriv 2 f a) * (iteratedDeriv 3 f a) ≥ 0 := by
  by_contra hcon
  push_neg at hcon
  have hd0 : Differentiable ℝ f := hf.differentiable (by norm_num)
  have hD1 : Differentiable ℝ (deriv f) := by
    have h := hf.differentiable_iteratedDeriv 1 (by norm_num)
    rwa [iteratedDeriv_one] at h
  have hD2 : Differentiable ℝ (iteratedDeriv 2 f) := hf.differentiable_iteratedDeriv 2 (by norm_num)
  have hC2 : Continuous (iteratedDeriv 2 f) := hf.continuous_iteratedDeriv 2 (by norm_num)
  have hC3 : Continuous (iteratedDeriv 3 f) := hf.continuous_iteratedDeriv 3 (by norm_num)
  have e2 : iteratedDeriv 2 f = deriv (deriv f) := by
    have h : iteratedDeriv 2 f = deriv (iteratedDeriv 1 f) := iteratedDeriv_succ
    rw [h, iteratedDeriv_one]
  have e3 : iteratedDeriv 3 f = deriv (iteratedDeriv 2 f) := iteratedDeriv_succ
  have dF : ∀ x, HasDerivAt f (deriv f x) x := fun x => (hd0 x).hasDerivAt
  have dG : ∀ x, HasDerivAt (deriv f) (iteratedDeriv 2 f x) x :=
    fun x => by rw [e2]; exact (hD1 x).hasDerivAt
  have dH : ∀ x, HasDerivAt (iteratedDeriv 2 f) (iteratedDeriv 3 f x) x :=
    fun x => by rw [e3]; exact (hD2 x).hasDerivAt
  have hF0 : ∀ x, f x ≠ 0 := fun x hx => by
    have h := hcon x
    rw [hx] at h
    simp at h
  have hG0 : ∀ x, deriv f x ≠ 0 := fun x hx => by
    have h := hcon x
    rw [hx] at h
    simp at h
  have hH0 : ∀ x, iteratedDeriv 2 f x ≠ 0 := fun x hx => by
    have h := hcon x
    rw [hx] at h
    simp at h
  have hK0 : ∀ x, iteratedDeriv 3 f x ≠ 0 := fun x hx => by
    have h := hcon x
    rw [hx] at h
    simp at h
  have b1 := ex98_B f (deriv f) (iteratedDeriv 2 f) dF dG hd0.continuous hC2 hF0 hH0
  have b2 := ex98_B (deriv f) (iteratedDeriv 2 f) (iteratedDeriv 3 f) dG dH hD1.continuous hC3 hG0 hK0
  have b3 := mul_pos b1 b2
  have b4 := hcon 0
  have e : f 0 * iteratedDeriv 2 f 0 * (deriv f 0 * iteratedDeriv 3 f 0)
      = f 0 * deriv f 0 * iteratedDeriv 2 f 0 * iteratedDeriv 3 f 0 := by ring
  linarith

#print axioms exercise_1998_a3
