-- CALC-INT-AI-261023212515-5874: 3 ứng viên formalize, biên dịch chung một file.
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
import Mathlib.Analysis.SpecialFunctions.ImproperIntegrals
import Mathlib.Analysis.SpecialFunctions.Trigonometric.Bounds
import Mathlib.Analysis.Calculus.ParametricIntegral
import Mathlib.Analysis.Calculus.MeanValue
set_option autoImplicit false

namespace Cand0
open MeasureTheory Filter Topology
lemma me_one_sub_cos_le (t : ℝ) : 1 - Real.cos t ≤ 2 * |t| := by
  by_cases h : |t| ≤ 1
  · have h1 := (abs_le.mp (Real.cos_bound h)).1
    have ha0 : 0 ≤ |t| := abs_nonneg t
    have h2 : |t| ^ 2 ≤ |t| := by nlinarith
    have h3 : |t| ^ 4 ≤ |t| ^ 2 := by
      have h5 : |t| ^ 2 ≤ 1 := h2.trans h
      nlinarith [mul_nonneg (sq_nonneg |t|) (sub_nonneg.2 h5)]
    have h4 := sq_abs t
    nlinarith
  · push_neg at h
    nlinarith [Real.neg_one_le_cos t]

lemma me_tendsto_exp (m : ℝ) (hm : 0 < m) :
    Filter.Tendsto (fun x : ℝ => Real.exp (-m * x)) Filter.atTop (nhds 0) := by
  have h1 : Filter.Tendsto (fun x : ℝ => m * x) Filter.atTop Filter.atTop := by
    first
    | exact Filter.tendsto_id.const_mul_atTop hm
    | exact Filter.Tendsto.const_mul_atTop hm Filter.tendsto_id
    | exact Filter.tendsto_id.const_mul_atTop' hm
  have h2 := Real.tendsto_exp_neg_atTop_nhds_zero.comp h1
  refine h2.congr (fun x => ?_)
  show Real.exp (-(m * x)) = Real.exp (-m * x)
  rw [neg_mul]

lemma me_int_exp (m : ℝ) (hm : 0 < m) :
    MeasureTheory.IntegrableOn (fun x : ℝ => Real.exp (-m * x)) (Set.Ioi 0) := by
  have hd : ∀ x : ℝ, HasDerivAt (fun x : ℝ => -(Real.exp (-m * x)) / m) (Real.exp (-m * x)) x := by
    intro x
    have h1 := ((hasDerivAt_id' x).const_mul (-m)).exp
    have h2 := h1.neg.div_const m
    refine h2.congr_deriv ?_
    have hm' : m ≠ 0 := hm.ne'
    rw [div_eq_iff hm']
    ring
  have htend : Filter.Tendsto (fun x : ℝ => -(Real.exp (-m * x)) / m) Filter.atTop (nhds 0) := by
    have h := ((me_tendsto_exp m hm).neg).div_const m
    have h0 : (-(0:ℝ)) / m = 0 := by simp
    rw [h0] at h
    exact h
  first
  | exact exp_neg_integrableOn_Ioi 0 hm
  | exact integrableOn_exp_mul_Ioi (neg_neg_of_pos hm) 0
  | exact integrableOn_Ioi_deriv_of_nonneg (hd 0).continuousAt.continuousWithinAt (fun x _ => hd x) (fun x _ => (Real.exp_pos _).le) htend
  | exact MeasureTheory.integrableOn_Ioi_deriv_of_nonneg (hd 0).continuousAt.continuousWithinAt (fun x _ => hd x) (fun x _ => (Real.exp_pos _).le) htend

lemma me_norm_exp_sin (m u x : ℝ) :
    ‖Real.exp (-m * x) * Real.sin (u * x)‖ ≤ Real.exp (-m * x) := by
  rw [Real.norm_eq_abs, abs_mul, abs_of_pos (Real.exp_pos _)]
  exact mul_le_of_le_one_right (Real.exp_pos _).le (Real.abs_sin_le_one _)

lemma me_laplace_sin (m : ℝ) (hm : 0 < m) (s : ℝ) :
    ∫ x in Set.Ioi (0:ℝ), Real.exp (-m * x) * Real.sin (s * x) = s / (m ^ 2 + s ^ 2) := by
  have hpos : 0 < m ^ 2 + s ^ 2 := add_pos_of_pos_of_nonneg (pow_pos hm 2) (sq_nonneg s)
  have hne : m ^ 2 + s ^ 2 ≠ 0 := hpos.ne'
  have hD : ∀ x : ℝ, HasDerivAt
      (fun x : ℝ => -(Real.exp (-m * x) * (m * Real.sin (s * x) + s * Real.cos (s * x))) / (m ^ 2 + s ^ 2))
      (Real.exp (-m * x) * Real.sin (s * x)) x := by
    intro x
    have h1 := ((hasDerivAt_id' x).const_mul (-m)).exp
    have h2 := ((hasDerivAt_id' x).const_mul s).sin
    have h3 := ((hasDerivAt_id' x).const_mul s).cos
    have h4 := (h1.mul ((h2.const_mul m).add (h3.const_mul s))).neg.div_const (m ^ 2 + s ^ 2)
    refine h4.congr_deriv ?_
    rw [div_eq_iff hne]
    ring
  have htend : Filter.Tendsto
      (fun x : ℝ => -(Real.exp (-m * x) * (m * Real.sin (s * x) + s * Real.cos (s * x))) / (m ^ 2 + s ^ 2))
      Filter.atTop (nhds 0) := by
    have h1 : Filter.Tendsto (fun x : ℝ => Real.exp (-m * x) * ((m + |s|) / (m ^ 2 + s ^ 2)))
        Filter.atTop (nhds 0) := by
      have h := (me_tendsto_exp m hm).mul_const ((m + |s|) / (m ^ 2 + s ^ 2))
      rw [zero_mul] at h
      exact h
    have hkey : ∀ x : ℝ,
        ‖-(Real.exp (-m * x) * (m * Real.sin (s * x) + s * Real.cos (s * x))) / (m ^ 2 + s ^ 2)‖
          ≤ Real.exp (-m * x) * ((m + |s|) / (m ^ 2 + s ^ 2)) := by
      intro x
      have hb : |m * Real.sin (s * x) + s * Real.cos (s * x)| ≤ m + |s| := by
        have e1 : |m * Real.sin (s * x)| ≤ m := by
          rw [abs_mul, abs_of_pos hm]
          exact mul_le_of_le_one_right hm.le (Real.abs_sin_le_one _)
        have e2 : |s * Real.cos (s * x)| ≤ |s| := by
          rw [abs_mul]
          exact mul_le_of_le_one_right (abs_nonneg _) (Real.abs_cos_le_one _)
        have e1' := abs_le.mp e1
        have e2' := abs_le.mp e2
        exact abs_le.mpr ⟨by linarith [e1'.1, e2'.1], by linarith [e1'.2, e2'.2]⟩
      have hE := Real.exp_pos (-m * x)
      rw [Real.norm_eq_abs, abs_div, abs_neg, abs_mul, abs_of_pos hE, abs_of_pos hpos, ← mul_div_assoc]
      have hE2 := mul_le_mul_of_nonneg_left hb hE.le
      first
      | exact div_le_div_of_nonneg_right hE2 hpos.le
      | (gcongr)
      | exact (div_le_div_iff_of_pos_right hpos).mpr hE2
    exact squeeze_zero_norm hkey h1
  have hint : MeasureTheory.IntegrableOn
      (fun x : ℝ => Real.exp (-m * x) * Real.sin (s * x)) (Set.Ioi 0) := by
    refine MeasureTheory.Integrable.mono' (me_int_exp m hm) ?_ ?_
    · exact (by fun_prop : Continuous (fun x : ℝ => Real.exp (-m * x) * Real.sin (s * x))).aestronglyMeasurable
    · filter_upwards with x
      exact me_norm_exp_sin m s x
  have key : ∫ x in Set.Ioi (0:ℝ), Real.exp (-m * x) * Real.sin (s * x)
      = 0 - (-(Real.exp (-m * 0) * (m * Real.sin (s * 0) + s * Real.cos (s * 0))) / (m ^ 2 + s ^ 2)) :=
    MeasureTheory.integral_Ioi_of_hasDerivAt_of_tendsto (hD 0).continuousAt.continuousWithinAt
      (fun x _ => hD x) hint htend
  rw [key]
  first
  | (simp; done)
  | (simp; ring)

lemma me_hasDeriv_F (m : ℝ) (hm : 0 < m) (t : ℝ) :
    HasDerivAt (fun u : ℝ => ∫ x in Set.Ioi (0:ℝ), Real.exp (-m * x) * (1 - Real.cos (u * x)) / x)
      (t / (m ^ 2 + t ^ 2)) t := by
  have hmeas : ∀ u : ℝ, Measurable (fun x : ℝ => Real.exp (-m * x) * (1 - Real.cos (u * x)) / x) := by
    intro u
    first
    | fun_prop
    | measurability
    | exact ((Real.measurable_exp.comp (measurable_const.mul measurable_id)).mul
        (measurable_const.sub (Real.measurable_cos.comp (measurable_const.mul measurable_id)))).div measurable_id
  have haeP : Filter.Eventually (fun x : ℝ => x ∈ Set.Ioi (0:ℝ))
      (MeasureTheory.ae (MeasureTheory.volume.restrict (Set.Ioi (0:ℝ)))) :=
    MeasureTheory.ae_restrict_mem measurableSet_Ioi
  have hbound : ∀ u x : ℝ, 0 < x →
      ‖Real.exp (-m * x) * (1 - Real.cos (u * x)) / x‖ ≤ 2 * |u| * Real.exp (-m * x) := by
    intro u x hx
    have hc : 0 ≤ 1 - Real.cos (u * x) := by linarith [Real.cos_le_one (u * x)]
    have hE := Real.exp_pos (-m * x)
    have hnn : 0 ≤ Real.exp (-m * x) * (1 - Real.cos (u * x)) / x :=
      div_nonneg (mul_nonneg hE.le hc) hx.le
    rw [Real.norm_eq_abs, abs_of_nonneg hnn]
    have h2 : 1 - Real.cos (u * x) ≤ 2 * |u| * x := by
      have h5 := me_one_sub_cos_le (u * x)
      rw [abs_mul, abs_of_pos hx] at h5
      linarith
    have h3 := mul_le_mul_of_nonneg_left h2 hE.le
    first
    | (rw [div_le_iff₀ hx]; nlinarith [h3])
    | (rw [div_le_iff hx]; nlinarith [h3])
  have hFint : MeasureTheory.IntegrableOn
      (fun x : ℝ => Real.exp (-m * x) * (1 - Real.cos (t * x)) / x) (Set.Ioi 0) := by
    refine MeasureTheory.Integrable.mono'
      (MeasureTheory.Integrable.const_mul (me_int_exp m hm) (2 * |t|))
      (hmeas t).aestronglyMeasurable ?_
    filter_upwards [haeP] with x hx
    exact hbound t x hx
  have hdiff : ∀ x : ℝ, 0 < x → ∀ u : ℝ,
      HasDerivAt (fun u : ℝ => Real.exp (-m * x) * (1 - Real.cos (u * x)) / x)
        (Real.exp (-m * x) * Real.sin (u * x)) u := by
    intro x hx u
    have h1 := ((hasDerivAt_id' u).mul_const x).cos
    have h2 := ((hasDerivAt_const u (1:ℝ)).sub h1).const_mul (Real.exp (-m * x))
    have h3 := h2.div_const x
    refine h3.congr_deriv ?_
    rw [div_eq_iff hx.ne']
    ring
  have key := hasDerivAt_integral_of_dominated_loc_of_deriv_le
    (F := fun (u x : ℝ) => Real.exp (-m * x) * (1 - Real.cos (u * x)) / x)
    (F' := fun (u x : ℝ) => Real.exp (-m * x) * Real.sin (u * x))
    (x₀ := t) (s := Set.univ) (bound := fun x : ℝ => Real.exp (-m * x))
    Filter.univ_mem
    (by
      filter_upwards with u
      exact (hmeas u).aestronglyMeasurable)
    hFint
    ((by fun_prop : Continuous (fun x : ℝ => Real.exp (-m * x) * Real.sin (t * x))).aestronglyMeasurable)
    (by
      filter_upwards with a
      intro u _
      exact me_norm_exp_sin m u a)
    (me_int_exp m hm)
    (by
      filter_upwards [haeP] with a ha
      intro u _
      exact hdiff a ha u)
  exact key.2.congr_deriv (me_laplace_sin m hm t)

lemma me_main (m : ℝ) (hm : 0 < m) (n : ℝ) :
    ∫ x in Set.Ioi (0:ℝ), Real.exp (-m * x) * (1 - Real.cos (n * x)) / x
      = Real.log (1 + n ^ 2 / m ^ 2) / 2 := by
  have hm0 : m ≠ 0 := hm.ne'
  obtain ⟨Fm, hFm⟩ : ∃ Fm : ℝ → ℝ, Fm = fun u => ∫ x in Set.Ioi (0:ℝ),
      Real.exp (-m * x) * (1 - Real.cos (u * x)) / x := ⟨_, rfl⟩
  have hder : ∀ t : ℝ, HasDerivAt Fm (t / (m ^ 2 + t ^ 2)) t := by
    intro t
    rw [hFm]
    exact me_hasDeriv_F m hm t
  have hF0 : Fm 0 = 0 := by
    rw [hFm]
    simp
  have hn : Fm n = ∫ x in Set.Ioi (0:ℝ), Real.exp (-m * x) * (1 - Real.cos (n * x)) / x := by
    rw [hFm]
  have hcontD : Continuous (fun y : ℝ => y / (m ^ 2 + y ^ 2)) :=
    Continuous.div continuous_id (by fun_prop)
      (fun y => (add_pos_of_pos_of_nonneg (pow_pos hm 2) (sq_nonneg y)).ne')
  have hI : ∫ y in (0:ℝ)..n, y / (m ^ 2 + y ^ 2) = Fm n - Fm 0 :=
    intervalIntegral.integral_eq_sub_of_hasDerivAt (fun s _ => hder s) (hcontD.intervalIntegrable 0 n)
  obtain ⟨G, hGdef⟩ : ∃ G : ℝ → ℝ, G = fun u => Real.log (m ^ 2 + u * u) / 2 := ⟨_, rfl⟩
  have hG : ∀ u : ℝ, HasDerivAt G (u / (m ^ 2 + u ^ 2)) u := by
    intro u
    rw [hGdef]
    have hpos : 0 < m ^ 2 + u * u :=
      add_pos_of_pos_of_nonneg (pow_pos hm 2) (mul_self_nonneg u)
    have h1 : HasDerivAt (fun y : ℝ => m ^ 2 + y * y) (1 * u + u * 1) u :=
      ((hasDerivAt_id' u).mul (hasDerivAt_id' u)).const_add (m ^ 2)
    have h2 := (h1.log hpos.ne').div_const 2
    refine h2.congr_deriv ?_
    have e : m ^ 2 + u * u = m ^ 2 + u ^ 2 := by ring
    have hne : m ^ 2 + u ^ 2 ≠ 0 :=
      (add_pos_of_pos_of_nonneg (pow_pos hm 2) (sq_nonneg u)).ne'
    first
    | ring
    | (rw [e]; field_simp; ring)
    | (rw [e]; field_simp)
  have hI2 : ∫ y in (0:ℝ)..n, y / (m ^ 2 + y ^ 2) = G n - G 0 :=
    intervalIntegral.integral_eq_sub_of_hasDerivAt (fun s _ => hG s) (hcontD.intervalIntegrable 0 n)
  have hGn : G n = Real.log (m ^ 2 + n * n) / 2 := by rw [hGdef]
  have hG0 : G 0 = Real.log (m ^ 2 + 0 * 0) / 2 := by rw [hGdef]
  have h3 : Fm n = G n - G 0 := by
    have h := hI.symm.trans hI2
    rw [hF0, sub_zero] at h
    exact h
  have hp : 0 < m ^ 2 + n * n := add_pos_of_pos_of_nonneg (pow_pos hm 2) (mul_self_nonneg n)
  have hm2 : m ^ 2 ≠ 0 := (pow_pos hm 2).ne'
  have h1 : 1 + n ^ 2 / m ^ 2 = (m ^ 2 + n * n) / m ^ 2 := by
    first
    | (field_simp; ring)
    | field_simp
    | (rw [eq_div_iff hm2, add_mul, div_mul_cancel₀ _ hm2]; ring)
  have hA : Real.log (1 + n ^ 2 / m ^ 2)
      = Real.log (m ^ 2 + n * n) - Real.log (m ^ 2 + 0 * 0) := by
    rw [h1, Real.log_div hp.ne' hm2]
    simp
  rw [← hn]
  linarith [h3, hGn, hG0, hA]

theorem exam_answer (m : ℕ) (hm_lo : 1 ≤ m) (hm_hi : m ≤ 4) (n : ℕ) (hn_lo : 1 ≤ n) (hn_hi : n ≤ 4) :
    ∫ x in Set.Ioi (0:ℝ), Real.exp (-(m:ℝ) * x) * (1 - Real.cos ((n:ℝ) * x)) / x = ((((1 : ℝ) / 2) * (Real.log ((1 : ℝ) + ((((m : ℝ) ^ (2 : ℕ))⁻¹) * ((n : ℝ) ^ (2 : ℕ))))))) := by
  have hm : (0:ℝ) < (m:ℝ) := Nat.cast_pos.mpr (by omega)
  have h := me_main (m:ℝ) hm (n:ℝ)
  first
  | exact h
  | (rw [h]; ring_nf)
  | (rw [h]; push_cast; ring_nf)

end Cand0
#print axioms Cand0.exam_answer

namespace Cand1
open MeasureTheory Filter Topology Set
lemma exam_one_sub_cos_le (u : ℝ) : 1 - Real.cos u ≤ |u| := by
  have h1 := Real.one_sub_sq_div_two_le_cos (x := u)
  have h2 := Real.neg_one_le_cos u
  by_cases h : |u| ≤ 2
  · have h3 : u ^ 2 = |u| ^ 2 := (sq_abs u).symm
    nlinarith [abs_nonneg u, mul_nonneg (abs_nonneg u) (sub_nonneg.mpr h)]
  · have h' : 2 < |u| := not_le.mp h
    linarith

lemma exam_exp_mul_bdd (p x u : ℝ) (hu : |u| ≤ 1) :
    ‖Real.exp (-p * x) * u‖ ≤ Real.exp (-p * x) := by
  rw [Real.norm_eq_abs, abs_mul, abs_of_pos (Real.exp_pos _)]
  exact mul_le_of_le_one_right (Real.exp_pos _).le hu

lemma exam_exp_tendsto (p : ℝ) (hp : 0 < p) :
    Tendsto (fun x : ℝ => Real.exp (-p * x)) atTop (𝓝 0) := by
  have h := Real.tendsto_exp_neg_atTop_nhds_zero.comp (Filter.tendsto_id.const_mul_atTop hp)
  refine h.congr (fun x => ?_)
  simp [neg_mul]

lemma exam_tendsto_zero (p : ℝ) (hp : 0 < p) (u : ℝ → ℝ) (hu : ∀ x, |u x| ≤ 1) :
    Tendsto (fun x : ℝ => Real.exp (-p * x) * u x) atTop (𝓝 0) := by
  refine squeeze_zero_norm (fun x => ?_) (exam_exp_tendsto p hp)
  exact exam_exp_mul_bdd p x (u x) (hu x)

lemma exam_sin_integral (p s : ℝ) (hp : 0 < p) :
    ∫ x in Ioi (0:ℝ), Real.exp (-p * x) * Real.sin (s * x) = s / (p ^ 2 + s ^ 2) := by
  have hpos : 0 < p ^ 2 + s ^ 2 := by positivity
  obtain ⟨G, hG⟩ : ∃ G : ℝ → ℝ, G = fun x => -(Real.exp (-p * x) * (p * Real.sin (s * x) + s * Real.cos (s * x))) / (p ^ 2 + s ^ 2) := ⟨_, rfl⟩
  have hderiv : ∀ x ∈ Ioi (0:ℝ), HasDerivAt G (Real.exp (-p * x) * Real.sin (s * x)) x := by
    intro x _
    rw [hG]
    have h1 : HasDerivAt (fun x : ℝ => -p * x) (-p) x :=
      ((hasDerivAt_id x).const_mul (-p)).congr_deriv (by ring)
    have h2 : HasDerivAt (fun x : ℝ => Real.exp (-p * x)) (Real.exp (-p * x) * (-p)) x := h1.exp
    have h3 : HasDerivAt (fun x : ℝ => s * x) s x :=
      ((hasDerivAt_id x).const_mul s).congr_deriv (by ring)
    have h4 : HasDerivAt (fun x : ℝ => Real.sin (s * x)) (Real.cos (s * x) * s) x := h3.sin
    have h5 : HasDerivAt (fun x : ℝ => Real.cos (s * x)) (-Real.sin (s * x) * s) x := h3.cos
    have h6 := (h2.mul ((h4.const_mul p).add (h5.const_mul s))).neg.div_const (p ^ 2 + s ^ 2)
    refine h6.congr_deriv ?_
    rw [div_eq_iff hpos.ne']
    ring
  have hGc : Continuous G := by
    rw [hG]
    fun_prop
  have hmeas : AEStronglyMeasurable (fun x : ℝ => Real.exp (-p * x) * Real.sin (s * x))
      (volume.restrict (Ioi (0:ℝ))) :=
    (by fun_prop : Continuous fun x : ℝ => Real.exp (-p * x) * Real.sin (s * x)).aestronglyMeasurable
  have hint : IntegrableOn (fun x : ℝ => Real.exp (-p * x) * Real.sin (s * x)) (Ioi (0:ℝ)) :=
    Integrable.mono' (exp_neg_integrableOn_Ioi 0 hp) hmeas
      (ae_of_all _ (fun x => exam_exp_mul_bdd p x (Real.sin (s * x)) (Real.abs_sin_le_one _)))
  have t1 := exam_tendsto_zero p hp (fun x => Real.sin (s * x)) (fun x => Real.abs_sin_le_one _)
  have t2 := exam_tendsto_zero p hp (fun x => Real.cos (s * x)) (fun x => Real.abs_cos_le_one _)
  have t3 : Tendsto (fun x : ℝ => -(p / (p ^ 2 + s ^ 2)) * (Real.exp (-p * x) * Real.sin (s * x))
      + -(s / (p ^ 2 + s ^ 2)) * (Real.exp (-p * x) * Real.cos (s * x))) atTop
      (𝓝 (-(p / (p ^ 2 + s ^ 2)) * 0 + -(s / (p ^ 2 + s ^ 2)) * 0)) :=
    (t1.const_mul _).add (t2.const_mul _)
  have hlim : Tendsto G atTop (𝓝 0) := by
    rw [show -(p / (p ^ 2 + s ^ 2)) * 0 + -(s / (p ^ 2 + s ^ 2)) * 0 = (0:ℝ) by ring] at t3
    refine Filter.Tendsto.congr (fun x => ?_) t3
    simp only [hG]
    ring
  have key := integral_Ioi_of_hasDerivAt_of_tendsto hGc.continuousWithinAt hderiv hint hlim
  rw [key, hG]
  simp only [mul_zero, Real.exp_zero, Real.sin_zero, Real.cos_zero, mul_one, one_mul, add_zero, zero_add]
  ring

lemma exam_hasDerivAt_integrand (p x : ℝ) (hx : 0 < x) (s : ℝ) :
    HasDerivAt (fun s : ℝ => Real.exp (-p * x) * (1 - Real.cos (s * x)) / x)
      (Real.exp (-p * x) * Real.sin (s * x)) s := by
  have h1 : HasDerivAt (fun s : ℝ => s * x) x s :=
    ((hasDerivAt_id s).mul_const x).congr_deriv (by ring)
  have h2 : HasDerivAt (fun s : ℝ => Real.exp (-p * x) * (1 - Real.cos (s * x)) / x)
      (Real.exp (-p * x) * (-(-Real.sin (s * x) * x)) / x) s :=
    (((h1.cos).const_sub 1).const_mul (Real.exp (-p * x))).div_const x
  refine h2.congr_deriv ?_
  rw [div_eq_iff hx.ne']
  ring

lemma exam_hasDerivAt_F (p : ℝ) (hp : 0 < p) (s₀ : ℝ) :
    HasDerivAt (fun s : ℝ => ∫ x in Ioi (0:ℝ), Real.exp (-p * x) * (1 - Real.cos (s * x)) / x)
      (s₀ / (p ^ 2 + s₀ ^ 2)) s₀ := by
  rw [← exam_sin_integral p s₀ hp]
  have hint_exp : Integrable (fun x : ℝ => Real.exp (-p * x)) (volume.restrict (Ioi (0:ℝ))) :=
    exp_neg_integrableOn_Ioi 0 hp
  have hmeasF : ∀ s : ℝ, AEStronglyMeasurable
      (fun x : ℝ => Real.exp (-p * x) * (1 - Real.cos (s * x)) / x)
      (volume.restrict (Ioi (0:ℝ))) := by
    intro s
    have hc : Continuous (fun x : ℝ => Real.exp (-p * x) * (1 - Real.cos (s * x))) := by
      fun_prop
    exact (hc.measurable.div measurable_id').aestronglyMeasurable
  have hF_int : Integrable (fun x : ℝ => Real.exp (-p * x) * (1 - Real.cos (s₀ * x)) / x)
      (volume.restrict (Ioi (0:ℝ))) := by
    refine Integrable.mono' (hint_exp.const_mul |s₀|) (hmeasF s₀) ?_
    refine (ae_restrict_iff' measurableSet_Ioi).mpr (ae_of_all _ (fun x hx => ?_))
    have hx' : 0 < x := hx
    have h1 := exam_one_sub_cos_le (s₀ * x)
    have h2 := Real.cos_le_one (s₀ * x)
    rw [abs_mul, abs_of_pos hx'] at h1
    rw [Real.norm_eq_abs, abs_div, abs_mul, abs_of_pos (Real.exp_pos _),
      abs_of_nonneg (by linarith : 0 ≤ 1 - Real.cos (s₀ * x)), abs_of_pos hx', div_le_iff₀ hx']
    calc Real.exp (-p * x) * (1 - Real.cos (s₀ * x)) ≤ Real.exp (-p * x) * (|s₀| * x) :=
          mul_le_mul_of_nonneg_left h1 (Real.exp_pos _).le
      _ = |s₀| * Real.exp (-p * x) * x := by ring
  have h := hasDerivAt_integral_of_dominated_loc_of_deriv_le
    (μ := volume.restrict (Ioi (0:ℝ)))
    (F := fun s x => Real.exp (-p * x) * (1 - Real.cos (s * x)) / x)
    (F' := fun s x => Real.exp (-p * x) * Real.sin (s * x))
    (x₀ := s₀) (bound := fun x => Real.exp (-p * x)) (s := Set.univ)
    Filter.univ_mem
    (by filter_upwards with s using hmeasF s)
    hF_int
    (Continuous.aestronglyMeasurable
      (by fun_prop : Continuous fun x : ℝ => Real.exp (-p * x) * Real.sin (s₀ * x)))
    (ae_of_all _ (fun x s _ => exam_exp_mul_bdd p x (Real.sin (s * x)) (Real.abs_sin_le_one _)))
    hint_exp
    ((ae_restrict_iff' measurableSet_Ioi).mpr
      (ae_of_all _ (fun x hx s _ => exam_hasDerivAt_integrand p x hx s)))
  exact h.2

lemma exam_deriv_log (p : ℝ) (hp : 0 < p) (s : ℝ) :
    HasDerivAt (fun s : ℝ => Real.log (p ^ 2 + s ^ 2) / 2) (s / (p ^ 2 + s ^ 2)) s := by
  have hq : p ^ 2 + s ^ 2 ≠ 0 := by positivity
  have d1 : HasDerivAt (fun s : ℝ => s ^ 2) (2 * s) s :=
    (hasDerivAt_pow 2 s).congr_deriv (by norm_num)
  have h := ((d1.const_add (p ^ 2)).log hq).div_const 2
  refine h.congr_deriv ?_
  ring

lemma exam_main (p q : ℝ) (hp : 0 < p) :
    ∫ x in Ioi (0:ℝ), Real.exp (-p * x) * (1 - Real.cos (q * x)) / x
      = Real.log (1 + q ^ 2 / p ^ 2) / 2 := by
  have hp0 : p ≠ 0 := hp.ne'
  have hderiv : ∀ s ∈ Set.uIcc (0:ℝ) q, HasDerivAt
      (fun s : ℝ => ∫ x in Ioi (0:ℝ), Real.exp (-p * x) * (1 - Real.cos (s * x)) / x)
      (s / (p ^ 2 + s ^ 2)) s := fun s _ => exam_hasDerivAt_F p hp s
  have hderiv2 : ∀ s ∈ Set.uIcc (0:ℝ) q, HasDerivAt
      (fun s : ℝ => Real.log (p ^ 2 + s ^ 2) / 2) (s / (p ^ 2 + s ^ 2)) s :=
    fun s _ => exam_deriv_log p hp s
  have hcont : Continuous (fun s : ℝ => s / (p ^ 2 + s ^ 2)) :=
    Continuous.div continuous_id' (by fun_prop)
      (fun s => (by positivity : p ^ 2 + s ^ 2 ≠ 0))
  have hint : IntervalIntegrable (fun s : ℝ => s / (p ^ 2 + s ^ 2)) volume 0 q :=
    hcont.intervalIntegrable 0 q
  have h1 := intervalIntegral.integral_eq_sub_of_hasDerivAt hderiv hint
  have h2 := intervalIntegral.integral_eq_sub_of_hasDerivAt hderiv2 hint
  have hF0 : (∫ x in Ioi (0:ℝ), Real.exp (-p * x) * (1 - Real.cos (0 * x)) / x) = 0 := by
    simp
  have hlog : Real.log (p ^ 2 + 0 ^ 2) = Real.log (p ^ 2) := by norm_num
  have e : 1 + q ^ 2 / p ^ 2 = (p ^ 2 + q ^ 2) / p ^ 2 := by
    rw [add_div, div_self (pow_ne_zero 2 hp0)]
  have hA : p ^ 2 + q ^ 2 ≠ 0 := by positivity
  have hB : p ^ 2 ≠ 0 := by positivity
  rw [e, Real.log_div hA hB]
  linarith

theorem exam_answer (m : ℕ) (hm_lo : 1 ≤ m) (hm_hi : m ≤ 4) (n : ℕ) (hn_lo : 1 ≤ n) (hn_hi : n ≤ 4) :
    ∫ x in Set.Ioi (0:ℝ), Real.exp (-(m:ℝ) * x) * (1 - Real.cos ((n:ℝ) * x)) / x = ((((1 : ℝ) / 2) * (Real.log ((1 : ℝ) + ((((m : ℝ) ^ (2 : ℕ))⁻¹) * ((n : ℝ) ^ (2 : ℕ))))))) := by
  have hp : (0:ℝ) < (m:ℝ) := Nat.cast_pos.mpr (by omega)
  exact exam_main (m:ℝ) (n:ℝ) hp

end Cand1
#print axioms Cand1.exam_answer

namespace Cand2
open Real
lemma one_sub_cos_bd (t : ℝ) : 0 ≤ 1 - Real.cos t ∧ 1 - Real.cos t ≤ t ^ 2 / 2 := by
  refine ⟨by linarith [Real.cos_le_one t], ?_⟩
  have h : 1 - t ^ 2 / 2 ≤ Real.cos t := by
    first
      | exact Real.one_sub_sq_div_two_le_cos (x := t)
      | exact Real.one_sub_sq_div_two_le_cos
      | have h1 : Real.cos t = 1 - 2 * Real.sin (t / 2) ^ 2 := by
          have h2 := Real.cos_two_mul (t / 2)
          have h3 := Real.sin_sq_add_cos_sq (t / 2)
          rw [show 2 * (t / 2) = t by ring] at h2
          nlinarith
        have h4 : Real.sin (t / 2) ^ 2 ≤ (t / 2) ^ 2 := by
          have h5 := Real.abs_sin_le_abs (x := t / 2)
          exact sq_le_sq.mpr h5
        nlinarith
  linarith

lemma one_sub_cos_le_abs (t : ℝ) : 1 - Real.cos t ≤ |t| := by
  obtain ⟨h0, h1⟩ := one_sub_cos_bd t
  have h2 := Real.neg_one_le_cos t
  have h3 : t ^ 2 = |t| ^ 2 := (sq_abs t).symm
  have h4 := abs_nonneg t
  by_cases h : |t| ≤ 2
  · nlinarith [mul_nonneg h4 (sub_nonneg.2 h)]
  · push_neg at h
    linarith

lemma meas_aux (c t : ℝ) : MeasureTheory.AEStronglyMeasurable
    (fun x : ℝ => Real.exp (-c * x) * (1 - Real.cos (t * x)) / x)
    (MeasureTheory.volume.restrict (Set.Ioi (0:ℝ))) := by
  have h1 : Continuous fun x : ℝ => Real.exp (-c * x) * (1 - Real.cos (t * x)) := by fun_prop
  first
    | exact (ContinuousOn.div h1.continuousOn continuousOn_id (fun x hx => (Set.mem_Ioi.mp hx).ne')).aestronglyMeasurable measurableSet_Ioi
    | exact Measurable.aestronglyMeasurable (by fun_prop)

lemma norm_bd1 (c t x : ℝ) : ‖Real.exp (-c * x) * Real.sin (t * x)‖ ≤ Real.exp (-c * x) := by
  rw [Real.norm_eq_abs, abs_mul, abs_of_pos (Real.exp_pos _)]
  have h := Real.abs_sin_le_one (t * x)
  nlinarith [mul_nonneg (Real.exp_pos (-c * x)).le (sub_nonneg.2 h)]

lemma exp_int (c : ℝ) (hc : 0 < c) : MeasureTheory.Integrable (fun x : ℝ => Real.exp (-c * x))
    (MeasureTheory.volume.restrict (Set.Ioi (0:ℝ))) := by
  first
    | exact exp_neg_integrableOn_Ioi 0 hc
    | exact integrableOn_exp_mul_Ioi (by linarith) 0

lemma integ_F (c t : ℝ) (hc : 0 < c) : MeasureTheory.Integrable
    (fun x : ℝ => Real.exp (-c * x) * (1 - Real.cos (t * x)) / x)
    (MeasureTheory.volume.restrict (Set.Ioi (0:ℝ))) := by
  refine MeasureTheory.Integrable.mono' ((exp_int c hc).const_mul |t|) (meas_aux c t) ?_
  filter_upwards [MeasureTheory.ae_restrict_mem measurableSet_Ioi] with x hx
  have hx' : 0 < x := hx
  show ‖Real.exp (-c * x) * (1 - Real.cos (t * x)) / x‖ ≤ |t| * Real.exp (-c * x)
  have hc0 : 0 ≤ 1 - Real.cos (t * x) := (one_sub_cos_bd _).1
  have hcl : 1 - Real.cos (t * x) ≤ |t| * x := by
    have h := one_sub_cos_le_abs (t * x)
    rwa [abs_mul, abs_of_pos hx'] at h
  have hpos : 0 ≤ Real.exp (-c * x) * (1 - Real.cos (t * x)) / x :=
    div_nonneg (mul_nonneg (Real.exp_pos _).le hc0) hx'.le
  rw [Real.norm_eq_abs, abs_of_nonneg hpos]
  first
    | rw [div_le_iff₀ hx']
    | rw [div_le_iff hx']
  nlinarith [mul_le_mul_of_nonneg_left hcl (Real.exp_pos (-c * x)).le]

lemma integ_sin (c r : ℝ) (hc : 0 < c) : MeasureTheory.Integrable
    (fun x : ℝ => Real.exp (-c * x) * Real.sin (r * x))
    (MeasureTheory.volume.restrict (Set.Ioi (0:ℝ))) := by
  refine MeasureTheory.Integrable.mono' (exp_int c hc) ?_ ?_
  · exact (by fun_prop : Continuous fun x : ℝ => Real.exp (-c * x) * Real.sin (r * x)).aestronglyMeasurable
  · filter_upwards with x
    exact norm_bd1 c r x

lemma deriv_pt (c x t : ℝ) (hx : 0 < x) :
    HasDerivAt (fun u : ℝ => Real.exp (-c * x) * (1 - Real.cos (u * x)) / x)
      (Real.exp (-c * x) * Real.sin (t * x)) t := by
  have h1 : HasDerivAt (fun u : ℝ => u * x) x t := by
    first
      | exact hasDerivAt_mul_const x
      | simpa using (hasDerivAt_id' t).mul_const x
  have h2 : HasDerivAt (fun u : ℝ => Real.cos (u * x)) (-Real.sin (t * x) * x) t := h1.cos
  have h3 := ((h2.const_sub 1).const_mul (Real.exp (-c * x))).div_const x
  refine h3.congr_deriv ?_
  rw [div_eq_iff hx.ne']
  ring

lemma hasDeriv_F (c s : ℝ) (hc : 0 < c) :
    HasDerivAt (fun t : ℝ => ∫ x in Set.Ioi (0:ℝ), Real.exp (-c * x) * (1 - Real.cos (t * x)) / x)
      (∫ x in Set.Ioi (0:ℝ), Real.exp (-c * x) * Real.sin (s * x)) s := by
  have hmeas : ∀ᶠ t in nhds s, MeasureTheory.AEStronglyMeasurable
      (fun x : ℝ => Real.exp (-c * x) * (1 - Real.cos (t * x)) / x)
      (MeasureTheory.volume.restrict (Set.Ioi (0:ℝ))) := by
    filter_upwards with t
    exact meas_aux c t
  have hint := integ_F c s hc
  have hmeas' : MeasureTheory.AEStronglyMeasurable
      (fun x : ℝ => Real.exp (-c * x) * Real.sin (s * x))
      (MeasureTheory.volume.restrict (Set.Ioi (0:ℝ))) :=
    (by fun_prop : Continuous fun x : ℝ => Real.exp (-c * x) * Real.sin (s * x)).aestronglyMeasurable
  have hbound : ∀ᵐ x ∂(MeasureTheory.volume.restrict (Set.Ioi (0:ℝ))), ∀ t : ℝ,
      ‖Real.exp (-c * x) * Real.sin (t * x)‖ ≤ Real.exp (-c * x) := by
    filter_upwards with x
    intro t
    exact norm_bd1 c t x
  have hdiff : ∀ᵐ x ∂(MeasureTheory.volume.restrict (Set.Ioi (0:ℝ))), ∀ t : ℝ,
      HasDerivAt (fun u : ℝ => Real.exp (-c * x) * (1 - Real.cos (u * x)) / x)
        (Real.exp (-c * x) * Real.sin (t * x)) t := by
    filter_upwards [MeasureTheory.ae_restrict_mem measurableSet_Ioi] with x hx
    intro t
    exact deriv_pt c x t hx
  have key : MeasureTheory.Integrable (fun x : ℝ => Real.exp (-c * x) * Real.sin (s * x))
        (MeasureTheory.volume.restrict (Set.Ioi (0:ℝ))) ∧
      HasDerivAt (fun t : ℝ => ∫ x in Set.Ioi (0:ℝ), Real.exp (-c * x) * (1 - Real.cos (t * x)) / x)
        (∫ x in Set.Ioi (0:ℝ), Real.exp (-c * x) * Real.sin (s * x)) s := by
    first
      | exact hasDerivAt_integral_of_dominated_loc_of_deriv_le
          (F := fun (t x : ℝ) => Real.exp (-c * x) * (1 - Real.cos (t * x)) / x)
          (F' := fun (t x : ℝ) => Real.exp (-c * x) * Real.sin (t * x))
          (bound := fun x : ℝ => Real.exp (-c * x))
          Filter.univ_mem hmeas hint hmeas'
          (by
            filter_upwards [hbound] with x hx
            intro t _
            exact hx t)
          (exp_int c hc)
          (by
            filter_upwards [hdiff] with x hx
            intro t _
            exact hx t)
      | exact hasDerivAt_integral_of_dominated_loc_of_deriv_le
          (F := fun (t x : ℝ) => Real.exp (-c * x) * (1 - Real.cos (t * x)) / x)
          (F' := fun (t x : ℝ) => Real.exp (-c * x) * Real.sin (t * x))
          (bound := fun x : ℝ => Real.exp (-c * x))
          one_pos hmeas hint hmeas'
          (by
            filter_upwards [hbound] with x hx
            intro t _
            exact hx t)
          (exp_int c hc)
          (by
            filter_upwards [hdiff] with x hx
            intro t _
            exact hx t)
  exact key.2

lemma G_deriv (c r x : ℝ) (hc : 0 < c) :
    HasDerivAt (fun y : ℝ => -(Real.exp (-c * y) * (c * Real.sin (r * y) + r * Real.cos (r * y))) / (c ^ 2 + r ^ 2))
      (Real.exp (-c * x) * Real.sin (r * x)) x := by
  have hD : c ^ 2 + r ^ 2 ≠ 0 := by positivity
  have h1 : HasDerivAt (fun y : ℝ => -c * y) (-c) x := by
    have h := (hasDerivAt_id' x).const_mul (-c)
    rwa [mul_one] at h
  have hE : HasDerivAt (fun y : ℝ => Real.exp (-c * y)) (Real.exp (-c * x) * (-c)) x := h1.exp
  have h2 : HasDerivAt (fun y : ℝ => r * y) r x := by
    have h := (hasDerivAt_id' x).const_mul r
    rwa [mul_one] at h
  have hs : HasDerivAt (fun y : ℝ => Real.sin (r * y)) (Real.cos (r * x) * r) x := h2.sin
  have hk : HasDerivAt (fun y : ℝ => Real.cos (r * y)) (-Real.sin (r * x) * r) x := h2.cos
  have hS : HasDerivAt (fun y : ℝ => c * Real.sin (r * y) + r * Real.cos (r * y))
      (c * (Real.cos (r * x) * r) + r * (-Real.sin (r * x) * r)) x :=
    (hs.const_mul c).add (hk.const_mul r)
  have hP := ((hE.mul hS).neg).div_const (c ^ 2 + r ^ 2)
  refine hP.congr_deriv ?_
  rw [div_eq_iff hD]
  try beta_reduce
  ring

lemma tendsto_exp_neg_aux (c : ℝ) (hc : 0 < c) :
    Filter.Tendsto (fun x : ℝ => Real.exp (-c * x)) Filter.atTop (nhds 0) := by
  have h1 : Filter.Tendsto (fun x : ℝ => c * x) Filter.atTop Filter.atTop :=
    Filter.Tendsto.const_mul_atTop hc Filter.tendsto_id
  have h2 := Real.tendsto_exp_neg_atTop_nhds_zero.comp h1
  refine h2.congr (fun x => ?_)
  simp [neg_mul]

lemma int_exp_sin (c r : ℝ) (hc : 0 < c) :
    ∫ x in Set.Ioi (0:ℝ), Real.exp (-c * x) * Real.sin (r * x) = r / (c ^ 2 + r ^ 2) := by
  have hD : 0 < c ^ 2 + r ^ 2 := by positivity
  have hcont : ContinuousWithinAt
      (fun x : ℝ => -(Real.exp (-c * x) * (c * Real.sin (r * x) + r * Real.cos (r * x))) / (c ^ 2 + r ^ 2))
      (Set.Ici 0) 0 :=
    (by fun_prop : Continuous fun x : ℝ => -(Real.exp (-c * x) * (c * Real.sin (r * x) + r * Real.cos (r * x))) / (c ^ 2 + r ^ 2)).continuousWithinAt
  have hK : Filter.Tendsto (fun x : ℝ => (c + |r|) / (c ^ 2 + r ^ 2) * Real.exp (-c * x))
      Filter.atTop (nhds 0) := by
    have h := (tendsto_exp_neg_aux c hc).const_mul ((c + |r|) / (c ^ 2 + r ^ 2))
    rwa [mul_zero] at h
  have hlim : Filter.Tendsto
      (fun x : ℝ => -(Real.exp (-c * x) * (c * Real.sin (r * x) + r * Real.cos (r * x))) / (c ^ 2 + r ^ 2))
      Filter.atTop (nhds 0) := by
    refine squeeze_zero_norm (fun x => ?_) hK
    show ‖-(Real.exp (-c * x) * (c * Real.sin (r * x) + r * Real.cos (r * x))) / (c ^ 2 + r ^ 2)‖
      ≤ (c + |r|) / (c ^ 2 + r ^ 2) * Real.exp (-c * x)
    have hE := Real.exp_pos (-c * x)
    have h1 : |c * Real.sin (r * x) + r * Real.cos (r * x)| ≤ c + |r| := by
      calc |c * Real.sin (r * x) + r * Real.cos (r * x)|
          ≤ |c * Real.sin (r * x)| + |r * Real.cos (r * x)| := abs_add_le _ _
        _ = c * |Real.sin (r * x)| + |r| * |Real.cos (r * x)| := by
            rw [abs_mul, abs_mul, abs_of_pos hc]
        _ ≤ c * 1 + |r| * 1 :=
            add_le_add (mul_le_mul_of_nonneg_left (Real.abs_sin_le_one _) hc.le)
              (mul_le_mul_of_nonneg_left (Real.abs_cos_le_one _) (abs_nonneg r))
        _ = c + |r| := by ring
    rw [Real.norm_eq_abs, abs_div, abs_neg, abs_mul, abs_of_pos hE, abs_of_pos hD]
    calc Real.exp (-c * x) * |c * Real.sin (r * x) + r * Real.cos (r * x)| / (c ^ 2 + r ^ 2)
        ≤ Real.exp (-c * x) * (c + |r|) / (c ^ 2 + r ^ 2) := by
          first
            | gcongr
            | exact div_le_div_of_nonneg_right (mul_le_mul_of_nonneg_left h1 hE.le) hD.le
      _ = (c + |r|) / (c ^ 2 + r ^ 2) * Real.exp (-c * x) := by ring
  have key := MeasureTheory.integral_Ioi_of_hasDerivAt_of_tendsto hcont
    (fun x _ => G_deriv c r x hc) (integ_sin c r hc) hlim
  refine key.trans ?_
  have h0 : -(Real.exp (-c * 0) * (c * Real.sin (r * 0) + r * Real.cos (r * 0))) / (c ^ 2 + r ^ 2)
      = -r / (c ^ 2 + r ^ 2) := by
    first
      | simp
      | norm_num
  show (0:ℝ) - (-(Real.exp (-c * 0) * (c * Real.sin (r * 0) + r * Real.cos (r * 0))) / (c ^ 2 + r ^ 2))
    = r / (c ^ 2 + r ^ 2)
  rw [h0]
  ring

lemma main_formula (c r : ℝ) (hc : 0 < c) :
    ∫ x in Set.Ioi (0:ℝ), Real.exp (-c * x) * (1 - Real.cos (r * x)) / x
      = Real.log (1 + r ^ 2 / c ^ 2) / 2 := by
  have hD : ∀ t : ℝ, c ^ 2 + t ^ 2 ≠ 0 := fun t => by positivity
  have hF : ∀ t : ℝ, HasDerivAt
      (fun t' : ℝ => ∫ x in Set.Ioi (0:ℝ), Real.exp (-c * x) * (1 - Real.cos (t' * x)) / x)
      (t / (c ^ 2 + t ^ 2)) t := by
    intro t
    have h := hasDeriv_F c t hc
    rwa [int_exp_sin c t hc] at h
  have hL : ∀ t : ℝ, HasDerivAt (fun t' : ℝ => Real.log (c ^ 2 + t' ^ 2) / 2)
      (t / (c ^ 2 + t ^ 2)) t := by
    intro t
    have h1 : HasDerivAt (fun t' : ℝ => c ^ 2 + t' ^ 2) (2 * t) t := by
      have h := (hasDerivAt_pow 2 t).const_add (c ^ 2)
      first
        | simpa using h
        | (convert h using 1; norm_num)
    have h2 := (h1.log (hD t)).div_const 2
    refine h2.congr_deriv ?_
    first
      | ring1
      | (field_simp; done)
      | (field_simp; ring1)
  have hH : ∀ t : ℝ, HasDerivAt
      (fun t' : ℝ => (∫ x in Set.Ioi (0:ℝ), Real.exp (-c * x) * (1 - Real.cos (t' * x)) / x)
        - Real.log (c ^ 2 + t' ^ 2) / 2) 0 t :=
    fun t => ((hF t).sub (hL t)).congr_deriv (sub_self _)
  have hconst : (∫ x in Set.Ioi (0:ℝ), Real.exp (-c * x) * (1 - Real.cos (r * x)) / x)
        - Real.log (c ^ 2 + r ^ 2) / 2
      = (∫ x in Set.Ioi (0:ℝ), Real.exp (-c * x) * (1 - Real.cos ((0:ℝ) * x)) / x)
        - Real.log (c ^ 2 + (0:ℝ) ^ 2) / 2 :=
    is_const_of_deriv_eq_zero (fun t => (hH t).differentiableAt) (fun t => (hH t).deriv) r 0
  have hF0 : (∫ x in Set.Ioi (0:ℝ), Real.exp (-c * x) * (1 - Real.cos ((0:ℝ) * x)) / x) = 0 := by
    simp
  have e0 : c ^ 2 + (0:ℝ) ^ 2 = c ^ 2 := by ring
  rw [hF0, e0] at hconst
  have hlog : Real.log (1 + r ^ 2 / c ^ 2) = Real.log (c ^ 2 + r ^ 2) - Real.log (c ^ 2) := by
    rw [← Real.log_div (hD r) (show c ^ 2 ≠ 0 by positivity)]
    congr 1
    first
      | (field_simp; done)
      | (field_simp; ring1)
  linarith

theorem exam_answer (m : ℕ) (hm_lo : 1 ≤ m) (hm_hi : m ≤ 4) (n : ℕ) (hn_lo : 1 ≤ n) (hn_hi : n ≤ 4) :
    MeasureTheory.IntegrableOn (fun x : ℝ => Real.exp (-(m : ℝ) * x) * (1 - Real.cos ((n : ℝ) * x)) / x) (Set.Ioi (0 : ℝ)) ∧
  (∫ x in Set.Ioi (0 : ℝ), Real.exp (-(m : ℝ) * x) * (1 - Real.cos ((n : ℝ) * x)) / x) = ((((1 : ℝ) / 2) * (Real.log ((1 : ℝ) + ((((m : ℝ) ^ (2 : ℕ))⁻¹) * ((n : ℝ) ^ (2 : ℕ))))))) := by
  have hc : (0:ℝ) < (m:ℝ) := by
    have h : 0 < m := by omega
    exact_mod_cast h
  refine ⟨integ_F (m:ℝ) (n:ℝ) hc, ?_⟩
  refine (main_formula (m:ℝ) (n:ℝ) hc).trans ?_
  first
    | rfl
    | (push_cast; ring_nf)
    | norm_num

end Cand2
#print axioms Cand2.exam_answer

