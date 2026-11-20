-- CALC-MVT-AI-261023212509-FC24: 3 ứng viên formalize, biên dịch chung một file.
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

namespace Cand0
open Real Filter Topology
lemma top_b_aux (c : ℝ) (hc : 0 ≤ c) :
    Tendsto (fun x : ℝ => Real.sqrt (x^2 + 2*c*x + 3) - x) atTop (𝓝 c) := by
  have h1 : Tendsto (fun x : ℝ => Real.sqrt (x^2 + 2*c*x + 3) + x + c) atTop atTop := by
    have hl : Tendsto (fun x : ℝ => x + c) atTop atTop :=
      tendsto_id.atTop_add tendsto_const_nhds
    refine tendsto_atTop_mono (fun x => ?_) hl
    have := Real.sqrt_nonneg (x^2 + 2*c*x + 3)
    linarith
  have h2 : Tendsto (fun x : ℝ => (3 - c^2) / (Real.sqrt (x^2 + 2*c*x + 3) + x + c)) atTop (𝓝 0) :=
    tendsto_const_nhds.div_atTop h1
  have h3 := h2.add_const c
  rw [zero_add] at h3
  refine h3.congr' ?_
  filter_upwards [eventually_gt_atTop (0:ℝ)] with x hx
  have hnn : 0 ≤ x^2 + 2*c*x + 3 := by nlinarith [mul_nonneg hc hx.le, sq_nonneg x]
  have hs := Real.sq_sqrt hnn
  have hs0 := Real.sqrt_nonneg (x^2 + 2*c*x + 3)
  have hpos : 0 < Real.sqrt (x^2 + 2*c*x + 3) + x + c := by linarith
  have hne := hpos.ne'
  field_simp
  nlinarith [hs]

lemma top_a_aux (c : ℝ) (hc : 0 ≤ c) :
    Tendsto (fun x : ℝ => Real.sqrt (x^2 + 2*c*x + 3) / x) atTop (𝓝 1) := by
  have h := top_b_aux c hc
  have h2 : Tendsto (fun x : ℝ => (Real.sqrt (x^2 + 2*c*x + 3) - x) / x) atTop (𝓝 0) :=
    h.div_atTop tendsto_id
  have h3 := h2.add_const 1
  rw [zero_add] at h3
  refine h3.congr' ?_
  filter_upwards [eventually_gt_atTop (0:ℝ)] with x hx
  rw [sub_div, div_self hx.ne']
  ring

lemma bot_b_aux (c : ℝ) (hc : 0 ≤ c) :
    Tendsto (fun x : ℝ => Real.sqrt (x^2 + 2*c*x + 3) + x) atBot (𝓝 (-c)) := by
  have hl : Tendsto (fun x : ℝ => -x + -c) atBot atTop :=
    tendsto_neg_atBot_atTop.atTop_add tendsto_const_nhds
  have h1 : Tendsto (fun x : ℝ => Real.sqrt (x^2 + 2*c*x + 3) - x - c) atBot atTop := by
    refine tendsto_atTop_mono (fun x => ?_) hl
    have := Real.sqrt_nonneg (x^2 + 2*c*x + 3)
    linarith
  have h2 : Tendsto (fun x : ℝ => (3 - c^2) / (Real.sqrt (x^2 + 2*c*x + 3) - x - c)) atBot (𝓝 0) :=
    tendsto_const_nhds.div_atTop h1
  have h3 := h2.sub_const c
  rw [zero_sub] at h3
  refine h3.congr' ?_
  filter_upwards [eventually_lt_atBot (-2*c-1)] with x hx
  have hm : 0 < x * (x + 2*c) := mul_pos_of_neg_of_neg (by linarith) (by linarith)
  have hnn : 0 ≤ x^2 + 2*c*x + 3 := by nlinarith [hm]
  have hs := Real.sq_sqrt hnn
  have hs0 := Real.sqrt_nonneg (x^2 + 2*c*x + 3)
  have hpos : 0 < Real.sqrt (x^2 + 2*c*x + 3) - x - c := by linarith
  have hne := hpos.ne'
  field_simp
  nlinarith [hs]

lemma bot_a_aux (c : ℝ) (hc : 0 ≤ c) :
    Tendsto (fun x : ℝ => Real.sqrt (x^2 + 2*c*x + 3) / x) atBot (𝓝 (-1)) := by
  have h := bot_b_aux c hc
  have h2 : Tendsto (fun x : ℝ => (Real.sqrt (x^2 + 2*c*x + 3) + x) / x) atBot (𝓝 0) :=
    h.div_atBot tendsto_id
  have h3 := h2.sub_const 1
  rw [zero_sub] at h3
  refine h3.congr' ?_
  filter_upwards [eventually_lt_atBot (0:ℝ)] with x hx
  rw [add_div, div_self hx.ne']
  ring

theorem exam_answer (m : ℕ) (hm_lo : 1 ≤ m) (hm_hi : m ≤ 5) (k : ℕ) (hk_lo : 1 ≤ k) (hk_hi : k ≤ 6) :
    ∀ a₁ b₁ a₂ b₂ x₀ y₀ : ℝ,
  Filter.Tendsto (fun x : ℝ => Real.sqrt (x^2 + 2*(m:ℝ)*x + 3) / x) Filter.atTop (nhds a₁) →
  Filter.Tendsto (fun x : ℝ => Real.sqrt (x^2 + 2*(m:ℝ)*x + 3) - a₁ * x) Filter.atTop (nhds b₁) →
  Filter.Tendsto (fun x : ℝ => Real.sqrt (x^2 + 2*(m:ℝ)*x + 3) / x) Filter.atBot (nhds a₂) →
  Filter.Tendsto (fun x : ℝ => Real.sqrt (x^2 + 2*(m:ℝ)*x + 3) - a₂ * x) Filter.atBot (nhds b₂) →
  y₀ = a₁ * x₀ + b₁ →
  y₀ = a₂ * x₀ + b₂ →
  |((k:ℝ) - x₀) * ((a₂ * (k:ℝ) + b₂) - y₀) - ((a₁ * (k:ℝ) + b₁) - y₀) * ((k:ℝ) - x₀)| / 2 = ((((k : ℝ) + (m : ℝ)) ^ (2 : ℕ))) := by
  intro a₁ b₁ a₂ b₂ x₀ y₀ ha1 hb1 ha2 hb2 hy1 hy2
  have hm0 : (0:ℝ) ≤ (m:ℝ) := Nat.cast_nonneg m
  have e1 : a₁ = 1 := tendsto_nhds_unique ha1 (top_a_aux (m:ℝ) hm0)
  subst e1
  have hb1' : Tendsto (fun x : ℝ => Real.sqrt (x^2 + 2*(m:ℝ)*x + 3) - 1 * x) atTop (𝓝 (m:ℝ)) :=
    (top_b_aux (m:ℝ) hm0).congr (fun x => by ring)
  have e2 : b₁ = (m:ℝ) := tendsto_nhds_unique hb1 hb1'
  subst e2
  have e3 : a₂ = -1 := tendsto_nhds_unique ha2 (bot_a_aux (m:ℝ) hm0)
  subst e3
  have hb2' : Tendsto (fun x : ℝ => Real.sqrt (x^2 + 2*(m:ℝ)*x + 3) - (-1) * x) atBot (𝓝 (-(m:ℝ))) :=
    (bot_b_aux (m:ℝ) hm0).congr (fun x => by ring)
  have e4 : b₂ = -(m:ℝ) := tendsto_nhds_unique hb2 hb2'
  subst e4
  have hx : x₀ = -(m:ℝ) := by linarith
  have hy : y₀ = 0 := by linarith
  rw [hx, hy]
  rw [abs_of_nonpos]
  · push_cast
    ring
  · nlinarith [sq_nonneg ((k:ℝ) + (m:ℝ))]

end Cand0
#print axioms Cand0.exam_answer

namespace Cand1
open Filter Topology
lemma slant_top_aux (M : ℝ) (hM : 0 < M) :
    Filter.Tendsto (fun x : ℝ => Real.sqrt (x^2 + 2*M*x + 3) - (1*x + M)) Filter.atTop (nhds 0) := by
  have hden : Filter.Tendsto (fun x : ℝ => Real.sqrt (x^2 + 2*M*x + 3) + (x + M)) Filter.atTop Filter.atTop := by
    rw [Filter.tendsto_atTop_atTop]
    intro b
    refine ⟨b - M, fun x hx => ?_⟩
    have := Real.sqrt_nonneg (x^2 + 2*M*x + 3)
    try dsimp only
    linarith
  have h : Filter.Tendsto (fun x : ℝ => (3 - M^2) / (Real.sqrt (x^2 + 2*M*x + 3) + (x + M))) Filter.atTop (nhds 0) :=
    Filter.Tendsto.div_atTop tendsto_const_nhds hden
  refine h.congr' ?_
  filter_upwards [Filter.eventually_ge_atTop (0:ℝ)] with x hx
  have hnn : 0 ≤ x^2 + 2*M*x + 3 := by nlinarith [mul_nonneg hx hM.le, sq_nonneg x]
  have hs := Real.sq_sqrt hnn
  have hnn2 := Real.sqrt_nonneg (x^2 + 2*M*x + 3)
  have hpos : 0 < Real.sqrt (x^2 + 2*M*x + 3) + (x + M) := by linarith
  rw [div_eq_iff hpos.ne']
  linear_combination (-1:ℝ) * hs

lemma slant_bot_aux (M : ℝ) (hM : 0 < M) :
    Filter.Tendsto (fun x : ℝ => Real.sqrt (x^2 + 2*M*x + 3) - ((-1:ℝ)*x + -M)) Filter.atBot (nhds 0) := by
  have hden : Filter.Tendsto (fun x : ℝ => Real.sqrt (x^2 + 2*M*x + 3) - (x + M)) Filter.atBot Filter.atTop := by
    rw [Filter.tendsto_atBot_atTop]
    intro b
    refine ⟨-b - M, fun x hx => ?_⟩
    have := Real.sqrt_nonneg (x^2 + 2*M*x + 3)
    try dsimp only
    linarith
  have h : Filter.Tendsto (fun x : ℝ => (3 - M^2) / (Real.sqrt (x^2 + 2*M*x + 3) - (x + M))) Filter.atBot (nhds 0) :=
    Filter.Tendsto.div_atTop tendsto_const_nhds hden
  refine h.congr' ?_
  filter_upwards [Filter.eventually_le_atBot (-2*M)] with x hx
  have hnn : 0 ≤ x^2 + 2*M*x + 3 := by
    nlinarith [mul_nonneg (by linarith : (0:ℝ) ≤ -x) (by linarith : (0:ℝ) ≤ -(x + 2*M))]
  have hs := Real.sq_sqrt hnn
  have hnn2 := Real.sqrt_nonneg (x^2 + 2*M*x + 3)
  have hpos : 0 < Real.sqrt (x^2 + 2*M*x + 3) - (x + M) := by linarith
  rw [div_eq_iff hpos.ne']
  linear_combination (-1:ℝ) * hs

lemma lin_zero_aux {l : Filter ℝ} [l.NeBot] (hl : Filter.Tendsto (fun x : ℝ => x⁻¹) l (nhds 0))
    (hne : ∀ᶠ x : ℝ in l, x ≠ 0) {c d : ℝ}
    (h : Filter.Tendsto (fun x : ℝ => c*x + d) l (nhds 0)) : c = 0 ∧ d = 0 := by
  have h1 : Filter.Tendsto (fun x : ℝ => (c*x + d) * x⁻¹) l (nhds 0) := by
    have := h.mul hl
    rwa [mul_zero] at this
  have h2 : Filter.Tendsto (fun x : ℝ => (c*x + d) * x⁻¹) l (nhds c) := by
    have h3 : Filter.Tendsto (fun x : ℝ => c + d * x⁻¹) l (nhds c) := by
      have := (tendsto_const_nhds : Filter.Tendsto (fun _ : ℝ => c) l (nhds c)).add (hl.const_mul d)
      rwa [mul_zero, add_zero] at this
    refine h3.congr' ?_
    filter_upwards [hne] with x hx
    have hxx : x * x⁻¹ = 1 := mul_inv_cancel₀ hx
    linear_combination (-c) * hxx
  have hc : c = 0 := tendsto_nhds_unique h2 h1
  subst hc
  refine ⟨rfl, ?_⟩
  have h4 : Filter.Tendsto (fun x : ℝ => (0:ℝ)*x + d) l (nhds d) := by
    simpa using (tendsto_const_nhds : Filter.Tendsto (fun _ : ℝ => d) l (nhds d))
  exact tendsto_nhds_unique h4 h

theorem exam_answer (m : ℕ) (hm_lo : 1 ≤ m) (hm_hi : m ≤ 5) (k : ℕ) (hk_lo : 1 ≤ k) (hk_hi : k ≤ 6) :
    (∃ a₁ b₁ a₂ b₂ : ℝ,
    Filter.Tendsto (fun x : ℝ => Real.sqrt (x^2 + 2*(m:ℝ)*x + 3) - (a₁*x + b₁)) Filter.atTop (nhds 0) ∧
    Filter.Tendsto (fun x : ℝ => Real.sqrt (x^2 + 2*(m:ℝ)*x + 3) - (a₂*x + b₂)) Filter.atBot (nhds 0)) ∧
  ∀ a₁ b₁ a₂ b₂ x₀ y₀ : ℝ,
    Filter.Tendsto (fun x : ℝ => Real.sqrt (x^2 + 2*(m:ℝ)*x + 3) - (a₁*x + b₁)) Filter.atTop (nhds 0) →
    Filter.Tendsto (fun x : ℝ => Real.sqrt (x^2 + 2*(m:ℝ)*x + 3) - (a₂*x + b₂)) Filter.atBot (nhds 0) →
    y₀ = a₁*x₀ + b₁ → y₀ = a₂*x₀ + b₂ →
    |((k:ℝ) - x₀) * ((a₂*(k:ℝ) + b₂) - y₀) - ((k:ℝ) - x₀) * ((a₁*(k:ℝ) + b₁) - y₀)| / 2 = ((((k : ℝ) + (m : ℝ)) ^ (2 : ℕ))) := by
  have hM : (0:ℝ) < (m:ℝ) := Nat.cast_pos.mpr (by omega)
  refine ⟨⟨1, (m:ℝ), -1, -(m:ℝ), slant_top_aux _ hM, slant_bot_aux _ hM⟩, ?_⟩
  intro a₁ b₁ a₂ b₂ x₀ y₀ h1 h2 e1 e2
  have t1 := (slant_top_aux (m:ℝ) hM).sub h1
  have t2 := (slant_bot_aux (m:ℝ) hM).sub h2
  have u1 : Filter.Tendsto (fun x : ℝ => (a₁ - 1)*x + (b₁ - (m:ℝ))) Filter.atTop (nhds (0 - 0)) := by
    refine t1.congr (fun x => ?_)
    first | ring | (dsimp only; ring)
  have u2 : Filter.Tendsto (fun x : ℝ => (a₂ + 1)*x + (b₂ + (m:ℝ))) Filter.atBot (nhds (0 - 0)) := by
    refine t2.congr (fun x => ?_)
    first | ring | (dsimp only; ring)
  rw [sub_self] at u1 u2
  obtain ⟨c1, d1⟩ := lin_zero_aux tendsto_inv_atTop_zero
    ((Filter.eventually_gt_atTop (0:ℝ)).mono fun x hx => hx.ne') u1
  obtain ⟨c2, d2⟩ := lin_zero_aux tendsto_inv_atBot_zero
    ((Filter.eventually_lt_atBot (0:ℝ)).mono fun x hx => hx.ne) u2
  have ha1 : a₁ = 1 := by linarith
  have hb1 : b₁ = (m:ℝ) := by linarith
  have ha2 : a₂ = -1 := by linarith
  have hb2 : b₂ = -(m:ℝ) := by linarith
  rw [ha1, hb1] at e1
  rw [ha2, hb2] at e2
  have hx : x₀ = -(m:ℝ) := by linarith
  have hy : y₀ = 0 := by linarith
  have hin : ((k:ℝ) - x₀) * ((a₂*(k:ℝ) + b₂) - y₀) - ((k:ℝ) - x₀) * ((a₁*(k:ℝ) + b₁) - y₀)
      = -(2*((k:ℝ) + (m:ℝ))^2) := by
    rw [ha1, hb1, ha2, hb2, hx, hy]
    ring
  rw [hin, abs_neg, abs_of_nonneg (by positivity)]
  first | ring | (push_cast; ring)

end Cand1
#print axioms Cand1.exam_answer

namespace Cand2
open Filter Topology
theorem lemA_asym (c : ℝ) (hc : 0 ≤ c) :
    Filter.Tendsto (fun x : ℝ => Real.sqrt (x ^ 2 + 2 * c * x + 3) - (x + c)) Filter.atTop (nhds 0) := by
  have hg : Filter.Tendsto (fun x : ℝ => Real.sqrt (x ^ 2 + 2 * c * x + 3) + x + c) Filter.atTop Filter.atTop := by
    rw [Filter.tendsto_atTop]
    intro b
    filter_upwards [Filter.eventually_ge_atTop b] with x hx
    have := Real.sqrt_nonneg (x ^ 2 + 2 * c * x + 3)
    show b ≤ Real.sqrt (x ^ 2 + 2 * c * x + 3) + x + c
    linarith
  have h2 : Filter.Tendsto (fun x : ℝ => (3 - c ^ 2) / (Real.sqrt (x ^ 2 + 2 * c * x + 3) + x + c)) Filter.atTop (nhds 0) :=
    Filter.Tendsto.div_atTop tendsto_const_nhds hg
  refine h2.congr' ?_
  filter_upwards [Filter.eventually_gt_atTop (0:ℝ)] with x hx
  show (3 - c ^ 2) / (Real.sqrt (x ^ 2 + 2 * c * x + 3) + x + c) = Real.sqrt (x ^ 2 + 2 * c * x + 3) - (x + c)
  have hS : 0 ≤ x ^ 2 + 2 * c * x + 3 := by nlinarith [sq_nonneg x, mul_nonneg hc hx.le]
  have hs := Real.sq_sqrt hS
  have hn := Real.sqrt_nonneg (x ^ 2 + 2 * c * x + 3)
  have hpos : 0 < Real.sqrt (x ^ 2 + 2 * c * x + 3) + x + c := by linarith
  rw [div_eq_iff hpos.ne']
  linear_combination (-1 : ℝ) * hs

theorem lemB_asym (c : ℝ) (hc : 0 ≤ c) :
    Filter.Tendsto (fun x : ℝ => Real.sqrt (x ^ 2 + 2 * c * x + 3) + (x + c)) Filter.atBot (nhds 0) := by
  have hg : Filter.Tendsto (fun x : ℝ => Real.sqrt (x ^ 2 + 2 * c * x + 3) - x - c) Filter.atBot Filter.atTop := by
    rw [Filter.tendsto_atTop]
    intro b
    filter_upwards [Filter.eventually_le_atBot (-b - c)] with x hx
    have := Real.sqrt_nonneg (x ^ 2 + 2 * c * x + 3)
    show b ≤ Real.sqrt (x ^ 2 + 2 * c * x + 3) - x - c
    linarith
  have h2 : Filter.Tendsto (fun x : ℝ => (3 - c ^ 2) / (Real.sqrt (x ^ 2 + 2 * c * x + 3) - x - c)) Filter.atBot (nhds 0) :=
    Filter.Tendsto.div_atTop tendsto_const_nhds hg
  refine h2.congr' ?_
  filter_upwards [Filter.eventually_lt_atBot (-2 * c - 1)] with x hx
  show (3 - c ^ 2) / (Real.sqrt (x ^ 2 + 2 * c * x + 3) - x - c) = Real.sqrt (x ^ 2 + 2 * c * x + 3) + (x + c)
  have h1 : x < 0 := by linarith
  have h1' : x + 2 * c < 0 := by linarith
  have hS : 0 ≤ x ^ 2 + 2 * c * x + 3 := by nlinarith [mul_pos_of_neg_of_neg h1 h1']
  have hs := Real.sq_sqrt hS
  have hn := Real.sqrt_nonneg (x ^ 2 + 2 * c * x + 3)
  have hpos : 0 < Real.sqrt (x ^ 2 + 2 * c * x + 3) - x - c := by linarith
  rw [div_eq_iff hpos.ne']
  linear_combination (-1 : ℝ) * hs

theorem lemC_lin (p q : ℝ) (h : Filter.Tendsto (fun x : ℝ => p * x + q) Filter.atTop (nhds 0)) :
    p = 0 ∧ q = 0 := by
  have hs : Filter.Tendsto (fun x : ℝ => x + 1) Filter.atTop Filter.atTop := by
    rw [Filter.tendsto_atTop]
    intro b
    filter_upwards [Filter.eventually_ge_atTop b] with x hx
    show b ≤ x + 1
    linarith
  have h' := h.comp hs
  have h'' : Filter.Tendsto (fun x : ℝ => (p * (x + 1) + q) - (p * x + q)) Filter.atTop (nhds (0 - 0)) :=
    h'.sub h
  have hp : Filter.Tendsto (fun _ : ℝ => p) Filter.atTop (nhds (0 - 0)) :=
    h''.congr (fun x => by ring)
  have hp1 : p = 0 - 0 := tendsto_nhds_unique tendsto_const_nhds hp
  have hp0 : p = 0 := by linarith
  have hq : Filter.Tendsto (fun _ : ℝ => q) Filter.atTop (nhds 0) :=
    h.congr (fun x => by simp [hp0])
  exact ⟨hp0, tendsto_nhds_unique tendsto_const_nhds hq⟩

theorem lemD_lin (p q : ℝ) (h : Filter.Tendsto (fun x : ℝ => p * x + q) Filter.atBot (nhds 0)) :
    p = 0 ∧ q = 0 := by
  have hs : Filter.Tendsto (fun x : ℝ => x - 1) Filter.atBot Filter.atBot := by
    rw [Filter.tendsto_atBot]
    intro b
    filter_upwards [Filter.eventually_le_atBot b] with x hx
    show x - 1 ≤ b
    linarith
  have h' := h.comp hs
  have h'' : Filter.Tendsto (fun x : ℝ => (p * (x - 1) + q) - (p * x + q)) Filter.atBot (nhds (0 - 0)) :=
    h'.sub h
  have hp : Filter.Tendsto (fun _ : ℝ => -p) Filter.atBot (nhds (0 - 0)) :=
    h''.congr (fun x => by ring)
  have hp1 : -p = 0 - 0 := tendsto_nhds_unique tendsto_const_nhds hp
  have hp0 : p = 0 := by linarith
  have hq : Filter.Tendsto (fun _ : ℝ => q) Filter.atBot (nhds 0) :=
    h.congr (fun x => by simp [hp0])
  exact ⟨hp0, tendsto_nhds_unique tendsto_const_nhds hq⟩

theorem exam_answer (m : ℕ) (hm_lo : 1 ≤ m) (hm_hi : m ≤ 5) (k : ℕ) (hk_lo : 1 ≤ k) (hk_hi : k ≤ 6) :
    ∀ a₁ b₁ a₂ b₂ : ℝ,
    Filter.Tendsto (fun x : ℝ => Real.sqrt (x ^ 2 + 2 * (m : ℝ) * x + 3) - (a₁ * x + b₁)) Filter.atTop (nhds 0) →
    Filter.Tendsto (fun x : ℝ => Real.sqrt (x ^ 2 + 2 * (m : ℝ) * x + 3) - (a₂ * x + b₂)) Filter.atBot (nhds 0) →
    |((a₁ * (k : ℝ) + b₁) - (a₂ * (k : ℝ) + b₂)) * ((k : ℝ) - (b₂ - b₁) / (a₁ - a₂))| / 2 = ((((k : ℝ) + (m : ℝ)) ^ (2 : ℕ))) := by
  intro a₁ b₁ a₂ b₂ h1 h2
  have hm0 : (0:ℝ) ≤ (m:ℝ) := Nat.cast_nonneg m
  have hA := lemA_asym (m:ℝ) hm0
  have hB := lemB_asym (m:ℝ) hm0
  have h3 : Filter.Tendsto (fun x : ℝ => (1 - a₁) * x + ((m:ℝ) - b₁)) Filter.atTop (nhds (0 - 0)) :=
    (h1.sub hA).congr (fun x => by ring)
  rw [sub_zero] at h3
  obtain ⟨e1, e2⟩ := lemC_lin _ _ h3
  have h4 : Filter.Tendsto (fun x : ℝ => (-a₂ - 1) * x + (-b₂ - (m:ℝ))) Filter.atBot (nhds (0 - 0)) :=
    (h2.sub hB).congr (fun x => by ring)
  rw [sub_zero] at h4
  obtain ⟨e3, e4⟩ := lemD_lin _ _ h4
  have ha1 : a₁ = 1 := by linarith
  have hb1 : b₁ = (m:ℝ) := by linarith
  have ha2 : a₂ = -1 := by linarith
  have hb2 : b₂ = -(m:ℝ) := by linarith
  have e : ((a₁ * (k : ℝ) + b₁) - (a₂ * (k : ℝ) + b₂)) * ((k : ℝ) - (b₂ - b₁) / (a₁ - a₂)) = 2 * ((k:ℝ) + (m:ℝ)) ^ 2 := by
    rw [ha1, hb1, ha2, hb2]
    ring
  have hnn : (0:ℝ) ≤ 2 * ((k:ℝ) + (m:ℝ)) ^ 2 := by positivity
  rw [e, abs_of_nonneg hnn]
  push_cast
  ring

end Cand2
#print axioms Cand2.exam_answer

