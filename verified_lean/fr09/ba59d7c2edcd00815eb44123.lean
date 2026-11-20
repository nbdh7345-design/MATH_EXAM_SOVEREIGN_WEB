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

theorem ex_mvt_left_lb (h h' : ℝ → ℝ) (hd : ∀ x, HasDerivAt h (h' x) x) (p c : ℝ)
    (hc : ∀ ξ, ξ ≤ p → c ≤ h' ξ) (x : ℝ) (hx : x ≤ p) : h x ≤ h p + c * (x - p) := by
  rcases hx.eq_or_lt with rfl | hx'
  · simp
  · obtain ⟨ξ, hξ, hξe⟩ := exists_hasDerivAt_eq_slope h h' hx'
      (fun y _ => (hd y).continuousAt.continuousWithinAt) (fun y _ => hd y)
    have h1 : c ≤ (h p - h x) / (p - x) := by
      rw [← hξe]; exact hc ξ hξ.2.le
    have h2 : c * (p - x) ≤ h p - h x := (le_div_iff₀ (by linarith)).mp h1
    have h3 : c * (x - p) = -(c * (p - x)) := by ring
    linarith

theorem ex_mvt_right_lb (h h' : ℝ → ℝ) (hd : ∀ x, HasDerivAt h (h' x) x) (p c : ℝ)
    (hc : ∀ ξ, p ≤ ξ → c ≤ h' ξ) (x : ℝ) (hx : p ≤ x) : h p + c * (x - p) ≤ h x := by
  rcases hx.eq_or_lt with rfl | hx'
  · simp
  · obtain ⟨ξ, hξ, hξe⟩ := exists_hasDerivAt_eq_slope h h' hx'
      (fun y _ => (hd y).continuousAt.continuousWithinAt) (fun y _ => hd y)
    have h1 : c ≤ (h x - h p) / (x - p) := by
      rw [← hξe]; exact hc ξ hξ.1.le
    have h2 : c * (x - p) ≤ h x - h p := (le_div_iff₀ (by linarith)).mp h1
    linarith

theorem ex_mvt_left_ub (h h' : ℝ → ℝ) (hd : ∀ x, HasDerivAt h (h' x) x) (p c : ℝ)
    (hc : ∀ ξ, ξ ≤ p → h' ξ ≤ c) (x : ℝ) (hx : x ≤ p) : h p + c * (x - p) ≤ h x := by
  rcases hx.eq_or_lt with rfl | hx'
  · simp
  · obtain ⟨ξ, hξ, hξe⟩ := exists_hasDerivAt_eq_slope h h' hx'
      (fun y _ => (hd y).continuousAt.continuousWithinAt) (fun y _ => hd y)
    have h1 : (h p - h x) / (p - x) ≤ c := by
      rw [← hξe]; exact hc ξ hξ.2.le
    have h2 : h p - h x ≤ c * (p - x) := (div_le_iff₀ (by linarith)).mp h1
    have h3 : c * (x - p) = -(c * (p - x)) := by ring
    linarith

theorem ex_mvt_right_ub (h h' : ℝ → ℝ) (hd : ∀ x, HasDerivAt h (h' x) x) (p c : ℝ)
    (hc : ∀ ξ, p ≤ ξ → h' ξ ≤ c) (x : ℝ) (hx : p ≤ x) : h x ≤ h p + c * (x - p) := by
  rcases hx.eq_or_lt with rfl | hx'
  · simp
  · obtain ⟨ξ, hξ, hξe⟩ := exists_hasDerivAt_eq_slope h h' hx'
      (fun y _ => (hd y).continuousAt.continuousWithinAt) (fun y _ => hd y)
    have h1 : (h x - h p) / (x - p) ≤ c := by
      rw [← hξe]; exact hc ξ hξ.1.le
    have h2 : h x - h p ≤ c * (x - p) := (div_le_iff₀ (by linarith)).mp h1
    linarith

theorem ex_sgn_const (g : ℝ → ℝ) (hg : Continuous g) (h0 : ∀ x, g x ≠ 0) :
    (∀ x, 0 < g x) ∨ (∀ x, g x < 0) := by
  by_contra hcon
  push_neg at hcon
  obtain ⟨⟨a, ha⟩, ⟨b, hb⟩⟩ := hcon
  have ha' : g a < 0 := lt_of_le_of_ne ha (h0 a)
  have hb' : 0 < g b := lt_of_le_of_ne hb (h0 b).symm
  have hmem : (0:ℝ) ∈ Set.uIcc (g a) (g b) := Set.mem_uIcc.mpr (Or.inl ⟨ha'.le, hb'.le⟩)
  have hcont : ContinuousOn g (Set.uIcc a b) := hg.continuousOn
  have himg : (0:ℝ) ∈ g '' Set.uIcc a b := intermediate_value_uIcc hcont hmem
  obtain ⟨c, _, hc⟩ := himg
  exact h0 c hc

theorem ex_exists_mul_pos (a b : ℝ) (ha : 0 < a) (hb : 0 < b) :
    ∃ t : ℝ, 0 < t ∧ a * t = b := by
  refine ⟨b / a, div_pos hb ha, ?_⟩
  have hne : a ≠ 0 := ha.ne'
  field_simp

theorem ex_no_prod (a b c d : ℝ) (h : a * b * c * d < 0) (h1 : 0 < a * c) (h2 : 0 < b * d) :
    False := by
  have e : a * b * c * d = (a * c) * (b * d) := by ring
  have := mul_pos h1 h2
  linarith

theorem ex_caseM1 (g1 g2 g3 : ℝ → ℝ) (hd1 : ∀ x, HasDerivAt g1 (g2 x) x)
    (hd2 : ∀ x, HasDerivAt g2 (g3 x) x)
    (hp1 : ∀ x, 0 < g1 x) (hg3 : ∀ x, g3 x ≤ 0) (h20 : 0 < g2 0) : False := by
  have hanti : Antitone g2 := antitone_of_deriv_nonpos
    ((fun x => (hd2 x).differentiableAt) : Differentiable ℝ g2)
    (fun x => by rw [(hd2 x).deriv]; exact hg3 x)
  obtain ⟨t, ht, hte⟩ := ex_exists_mul_pos (g2 0) (g1 0 + 1) h20 (by linarith [hp1 0])
  have h1 := ex_mvt_left_lb g1 g2 hd1 0 (g2 0) (fun ξ hξ => hanti hξ) (-t) (by linarith)
  have e : g2 0 * (-t - 0) = -(g2 0 * t) := by ring
  linarith [hp1 (-t)]

theorem ex_caseM2 (g1 g2 g3 : ℝ → ℝ) (hd1 : ∀ x, HasDerivAt g1 (g2 x) x)
    (hd2 : ∀ x, HasDerivAt g2 (g3 x) x)
    (hp1 : ∀ x, 0 < g1 x) (hg3 : ∀ x, g3 x ≤ 0) (h20 : g2 0 < 0) : False := by
  have hanti : Antitone g2 := antitone_of_deriv_nonpos
    ((fun x => (hd2 x).differentiableAt) : Differentiable ℝ g2)
    (fun x => by rw [(hd2 x).deriv]; exact hg3 x)
  obtain ⟨t, ht, hte⟩ := ex_exists_mul_pos (-g2 0) (g1 0 + 1) (by linarith) (by linarith [hp1 0])
  have h1 := ex_mvt_right_ub g1 g2 hd1 0 (g2 0) (fun ξ hξ => hanti hξ) t ht.le
  have e : g2 0 * (t - 0) = -((-g2 0) * t) := by ring
  linarith [hp1 t]

theorem ex_caseM3 (g1 g2 g3 : ℝ → ℝ) (hd1 : ∀ x, HasDerivAt g1 (g2 x) x)
    (hd2 : ∀ x, HasDerivAt g2 (g3 x) x)
    (hn1 : ∀ x, g1 x < 0) (hg3 : ∀ x, 0 ≤ g3 x) (h20 : 0 < g2 0) : False := by
  have hmono : Monotone g2 := monotone_of_deriv_nonneg
    ((fun x => (hd2 x).differentiableAt) : Differentiable ℝ g2)
    (fun x => by rw [(hd2 x).deriv]; exact hg3 x)
  obtain ⟨t, ht, hte⟩ := ex_exists_mul_pos (g2 0) (-g1 0 + 1) h20 (by linarith [hn1 0])
  have h1 := ex_mvt_right_lb g1 g2 hd1 0 (g2 0) (fun ξ hξ => hmono hξ) t ht.le
  have e : g2 0 * (t - 0) = g2 0 * t := by ring
  linarith [hn1 t]

theorem ex_caseM4 (g1 g2 g3 : ℝ → ℝ) (hd1 : ∀ x, HasDerivAt g1 (g2 x) x)
    (hd2 : ∀ x, HasDerivAt g2 (g3 x) x)
    (hn1 : ∀ x, g1 x < 0) (hg3 : ∀ x, 0 ≤ g3 x) (h20 : g2 0 < 0) : False := by
  have hmono : Monotone g2 := monotone_of_deriv_nonneg
    ((fun x => (hd2 x).differentiableAt) : Differentiable ℝ g2)
    (fun x => by rw [(hd2 x).deriv]; exact hg3 x)
  obtain ⟨t, ht, hte⟩ := ex_exists_mul_pos (-g2 0) (-g1 0 + 1) (by linarith) (by linarith [hn1 0])
  have h1 := ex_mvt_left_ub g1 g2 hd1 0 (g2 0) (fun ξ hξ => hmono hξ) (-t) (by linarith)
  have e : g2 0 * (-t - 0) = (-g2 0) * t := by ring
  linarith [hn1 (-t)]

theorem ex_caseC (g g1 g2 : ℝ → ℝ) (hd0 : ∀ x, HasDerivAt g (g1 x) x)
    (hd1 : ∀ x, HasDerivAt g1 (g2 x) x)
    (hpos : ∀ x, 0 < g x) (hle : ∀ x, g2 x ≤ 0) (hne : g1 1 ≠ 0) : False := by
  have hanti : Antitone g1 := antitone_of_deriv_nonpos
    ((fun x => (hd1 x).differentiableAt) : Differentiable ℝ g1)
    (fun x => by rw [(hd1 x).deriv]; exact hle x)
  rcases lt_or_gt_of_ne hne with hneg | hposd
  · obtain ⟨t, ht, hte⟩ := ex_exists_mul_pos (-g1 1) (g 1 + 1) (by linarith) (by linarith [hpos 1])
    have h1 := ex_mvt_right_ub g g1 hd0 1 (g1 1) (fun ξ hξ => hanti hξ) (1 + t) (by linarith)
    have e : g1 1 * (1 + t - 1) = -((-g1 1) * t) := by ring
    linarith [hpos (1 + t)]
  · obtain ⟨t, ht, hte⟩ := ex_exists_mul_pos (g1 1) (g 1 + 1) hposd (by linarith [hpos 1])
    have h1 := ex_mvt_left_lb g g1 hd0 1 (g1 1) (fun ξ hξ => hanti hξ) (1 - t) (by linarith)
    have e : g1 1 * (1 - t - 1) = -(g1 1 * t) := by ring
    linarith [hpos (1 - t)]

theorem exercise_1998_a3 (f : ℝ → ℝ) (hf : ContDiff ℝ 3 f) :
    ∃ a : ℝ, (f a) * (deriv f a) * (iteratedDeriv 2 f a) * (iteratedDeriv 3 f a) ≥ 0 := by
  rw [← iteratedDeriv_one]
  by_contra hcon
  push_neg at hcon
  have D0 : Differentiable ℝ f := hf.differentiable (by norm_num)
  have D1 : Differentiable ℝ (iteratedDeriv 1 f) := hf.differentiable_iteratedDeriv 1 (by norm_num)
  have D2 : Differentiable ℝ (iteratedDeriv 2 f) := hf.differentiable_iteratedDeriv 2 (by norm_num)
  have C3 : Continuous (iteratedDeriv 3 f) := hf.continuous_iteratedDeriv 3 (by norm_num)
  have e2 : iteratedDeriv 2 f = deriv (iteratedDeriv 1 f) := iteratedDeriv_succ
  have e3 : iteratedDeriv 3 f = deriv (iteratedDeriv 2 f) := iteratedDeriv_succ
  have hd0 : ∀ x, HasDerivAt f (iteratedDeriv 1 f x) x := by
    intro x
    rw [iteratedDeriv_one]
    exact (D0 x).hasDerivAt
  have hd1 : ∀ x, HasDerivAt (iteratedDeriv 1 f) (iteratedDeriv 2 f x) x := by
    intro x
    rw [e2]
    exact (D1 x).hasDerivAt
  have hd2 : ∀ x, HasDerivAt (iteratedDeriv 2 f) (iteratedDeriv 3 f x) x := by
    intro x
    rw [e3]
    exact (D2 x).hasDerivAt
  have cont0 : Continuous f := D0.continuous
  have cont1 : Continuous (iteratedDeriv 1 f) := D1.continuous
  have cont2 : Continuous (iteratedDeriv 2 f) := D2.continuous
  have n0 : ∀ a, f a ≠ 0 := by
    intro a h
    have := hcon a
    rw [h] at this
    simp at this
  have n1 : ∀ a, iteratedDeriv 1 f a ≠ 0 := by
    intro a h
    have := hcon a
    rw [h] at this
    simp at this
  have n2 : ∀ a, iteratedDeriv 2 f a ≠ 0 := by
    intro a h
    have := hcon a
    rw [h] at this
    simp at this
  have n3 : ∀ a, iteratedDeriv 3 f a ≠ 0 := by
    intro a h
    have := hcon a
    rw [h] at this
    simp at this
  rcases ex_sgn_const (iteratedDeriv 1 f) cont1 n1 with s1 | s1 <;>
    rcases ex_sgn_const (iteratedDeriv 2 f) cont2 n2 with s2 | s2 <;>
    rcases ex_sgn_const (iteratedDeriv 3 f) C3 n3 with s3 | s3 <;>
    rcases ex_sgn_const f cont0 n0 with s0 | s0
  all_goals first
    | exact ex_caseM1 (iteratedDeriv 1 f) (iteratedDeriv 2 f) (iteratedDeriv 3 f) hd1 hd2 s1 (fun x => (s3 x).le) (s2 0)
    | exact ex_caseM2 (iteratedDeriv 1 f) (iteratedDeriv 2 f) (iteratedDeriv 3 f) hd1 hd2 s1 (fun x => (s3 x).le) (s2 0)
    | exact ex_caseM3 (iteratedDeriv 1 f) (iteratedDeriv 2 f) (iteratedDeriv 3 f) hd1 hd2 s1 (fun x => (s3 x).le) (s2 0)
    | exact ex_caseM4 (iteratedDeriv 1 f) (iteratedDeriv 2 f) (iteratedDeriv 3 f) hd1 hd2 s1 (fun x => (s3 x).le) (s2 0)
    | exact ex_caseC f (iteratedDeriv 1 f) (iteratedDeriv 2 f) hd0 hd1 s0 (fun x => (s2 x).le) (n1 1)
    | exact ex_caseC (fun x => -f x) (fun x => -iteratedDeriv 1 f x) (fun x => -iteratedDeriv 2 f x)
        (fun x => (hd0 x).neg) (fun x => (hd1 x).neg)
        (fun x => by show 0 < -f x; linarith [s0 x])
        (fun x => by show -iteratedDeriv 2 f x ≤ 0; linarith [s2 x])
        (by show -iteratedDeriv 1 f 1 ≠ 0; intro h; exact n1 1 (neg_eq_zero.mp h))
    | exact ex_no_prod _ _ _ _ (hcon 0)
        (by first | exact mul_pos (s0 0) (s2 0) | exact mul_pos_of_neg_of_neg (s0 0) (s2 0))
        (by first | exact mul_pos (s1 0) (s3 0) | exact mul_pos_of_neg_of_neg (s1 0) (s3 0))

#print axioms exercise_1998_a3
