-- PN-Rudin_exercise_4_24: FR09 (dung), Lean 4 + Mathlib; dòng khai báo định lý do hệ thống viết.
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


open Topology Filter Real Complex TopologicalSpace Finset
open scoped BigOperators

lemma exercise_4_24_chord (f : ℝ → ℝ) (hf : Continuous f) (a b : ℝ)
    (h : ∀ x y : ℝ, a < x → x < b → a < y → y < b → f ((x + y) / 2) ≤ (f x + f y) / 2)
    (p q : ℝ) (hp : a < p) (hq : q < b) (hpq : p < q) (s : ℝ) (hs1 : p ≤ s) (hs2 : s ≤ q) :
    f s ≤ f p + (s - p) * ((f q - f p) / (q - p)) := by
  obtain ⟨c, hc⟩ : ∃ c : ℝ, c = (f q - f p) / (q - p) := ⟨_, rfl⟩
  rw [← hc]
  have hne : q - p ≠ 0 := (sub_pos.2 hpq).ne'
  have hqc : (q - p) * c = f q - f p := by
    rw [hc]
    field_simp <;> ring
  have hK : 0 < (q - p) ^ 2 := pow_pos (sub_pos.2 hpq) 2
  have H : ∀ ε : ℝ, 0 < ε → f s - (f p + (s - p) * c) ≤ ε * (q - p) ^ 2 := by
    intro ε hε
    obtain ⟨m, hm⟩ : ∃ m : ℝ → ℝ, ∀ t, m t = f t - (f p + (t - p) * c) + ε * (t - p) ^ 2 :=
      ⟨fun t => f t - (f p + (t - p) * c) + ε * (t - p) ^ 2, fun t => rfl⟩
    have hmc : Continuous m := by
      have e : m = fun t => f t - (f p + (t - p) * c) + ε * (t - p) ^ 2 := funext hm
      rw [e]
      fun_prop
    have key : ∀ u v : ℝ, a < u → u < b → a < v → v < b →
        m ((u + v) / 2) ≤ (m u + m v) / 2 - ε * (u - v) ^ 2 / 4 := by
      intro u v hu1 hu2 hv1 hv2
      have h1 := h u v hu1 hu2 hv1 hv2
      have e1 : ε * ((u + v) / 2 - p) ^ 2
          = (ε * (u - p) ^ 2 + ε * (v - p) ^ 2) / 2 - ε * (u - v) ^ 2 / 4 := by ring
      have e2 : ((u + v) / 2 - p) * c = ((u - p) * c + (v - p) * c) / 2 := by ring
      simp only [hm]
      linarith [h1, e1, e2]
    obtain ⟨c0, hc0, hmax⟩ :=
      isCompact_Icc.exists_isMaxOn (Set.nonempty_Icc.2 hpq.le) hmc.continuousOn
    have hmax' : ∀ t : ℝ, p ≤ t → t ≤ q → m t ≤ m c0 :=
      fun t ht1 ht2 => isMaxOn_iff.1 hmax t ⟨ht1, ht2⟩
    have hmp : m p = 0 := by
      rw [hm]
      ring
    have hmq : m q = ε * (q - p) ^ 2 := by
      rw [hm]
      linear_combination -hqc
    have hmc0 : m c0 ≤ ε * (q - p) ^ 2 := by
      have hcase : c0 = p ∨ c0 = q := by
        by_contra hne'
        push_neg at hne'
        obtain ⟨h1, h2⟩ := hne'
        have hp1 : p < c0 := lt_of_le_of_ne hc0.1 (Ne.symm h1)
        have hq1 : c0 < q := lt_of_le_of_ne hc0.2 h2
        obtain ⟨d, hd_def⟩ : ∃ d : ℝ, d = min (c0 - p) (q - c0) := ⟨_, rfl⟩
        have hd0 : 0 < d := by
          rw [hd_def]
          exact lt_min (by linarith) (by linarith)
        have hd1 : d ≤ c0 - p := by
          rw [hd_def]
          exact min_le_left _ _
        have hd2 : d ≤ q - c0 := by
          rw [hd_def]
          exact min_le_right _ _
        have k := key (c0 + d) (c0 - d) (by linarith) (by linarith) (by linarith) (by linarith)
        have e : (c0 + d + (c0 - d)) / 2 = c0 := by ring
        rw [e] at k
        have m1 := hmax' (c0 + d) (by linarith) (by linarith)
        have m2 := hmax' (c0 - d) (by linarith) (by linarith)
        have e3 : ε * (c0 + d - (c0 - d)) ^ 2 / 4 = ε * d ^ 2 := by ring
        have pos : 0 < ε * d ^ 2 := mul_pos hε (pow_pos hd0 2)
        linarith
      rcases hcase with h' | h'
      · have h0 : m c0 = 0 := by rw [h', hmp]
        have := mul_nonneg hε.le (sq_nonneg (q - p))
        linarith
      · exact le_of_eq (by rw [h', hmq])
    have hnn := mul_nonneg hε.le (sq_nonneg (s - p))
    have hsm : m s ≤ m c0 := hmax' s hs1 hs2
    have hms := hm s
    linarith
  by_contra hX
  push_neg at hX
  have hXpos : 0 < f s - (f p + (s - p) * c) := by linarith
  have hK2 : 0 < 2 * (q - p) ^ 2 := mul_pos two_pos hK
  have hεpos : 0 < (f s - (f p + (s - p) * c)) / (2 * (q - p) ^ 2) := div_pos hXpos hK2
  have h1 := H _ hεpos
  have h2 : (f s - (f p + (s - p) * c)) / (2 * (q - p) ^ 2) * (q - p) ^ 2
      = (f s - (f p + (s - p) * c)) / 2 := by
    rw [div_mul_eq_mul_div, div_eq_div_iff hK2.ne' two_ne_zero]
    ring
  linarith

theorem exercise_4_24 {f : ℝ → ℝ} (hf : Continuous f) (a : ℝ) (b : ℝ) (hab : a < b) (h : ∀ x y : ℝ, a < x → x < b → a < y → y < b → f ((x + y) / 2) ≤ (f x + f y) / 2) :
    ConvexOn ℝ (Set.Ioo a b) f := by
  refine ⟨?_, ?_⟩
  · apply convex_Ioo
  · intro x hx y hy α β hα hβ hαβ
    obtain ⟨hx1, hx2⟩ := hx
    obtain ⟨hy1, hy2⟩ := hy
    simp only [smul_eq_mul]
    have hα' : α = 1 - β := by linarith
    subst hα'
    rcases lt_trichotomy x y with hxy | hxy | hxy
    · have hyx' : y - x ≠ 0 := (sub_pos.2 hxy).ne'
      have hz := exercise_4_24_chord f hf a b h x y hx1 hy2 hxy ((1 - β) * x + β * y)
        (by nlinarith [mul_nonneg hβ (sub_nonneg.2 hxy.le)])
        (by nlinarith [mul_nonneg hα (sub_nonneg.2 hxy.le)])
      have hq' : (f y - f x) / (y - x) * (y - x) = f y - f x := by
        field_simp
      have key3 : ((1 - β) * x + β * y - x) * ((f y - f x) / (y - x)) = β * (f y - f x) := by
        linear_combination β * hq'
      linarith [hz, key3]
    · rw [← hxy]
      have e : (1 - β) * x + β * x = x := by ring
      rw [e]
      linarith [show (1 - β) * f x + β * f x = f x by ring]
    · have hyx' : x - y ≠ 0 := (sub_pos.2 hxy).ne'
      have hz := exercise_4_24_chord f hf a b h y x hy1 hx2 hxy ((1 - β) * x + β * y)
        (by nlinarith [mul_nonneg hα (sub_nonneg.2 hxy.le)])
        (by nlinarith [mul_nonneg hβ (sub_nonneg.2 hxy.le)])
      have hq' : (f x - f y) / (x - y) * (x - y) = f x - f y := by
        field_simp
      have key3 : ((1 - β) * x + β * y - y) * ((f x - f y) / (x - y))
          = (1 - β) * (f x - f y) := by
        linear_combination (1 - β) * hq'
      linarith [hz, key3]

#print axioms exercise_4_24
