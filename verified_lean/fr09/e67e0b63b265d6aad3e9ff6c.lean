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

theorem exercise_4_24 {f : ℝ → ℝ} (hf : Continuous f) (a : ℝ) (b : ℝ) (hab : a < b) (h : ∀ x y : ℝ, a < x → x < b → a < y → y < b → f ((x + y) / 2) ≤ (f x + f y) / 2) :
    ConvexOn ℝ (Set.Ioo a b) f := by
  refine ⟨convex_Ioo a b, ?_⟩
  have hcomb : ∀ x y σ : ℝ, x ∈ Set.Ioo a b → y ∈ Set.Ioo a b → 0 ≤ σ → σ ≤ 1 → (1 - σ) * x + σ * y ∈ Set.Ioo a b := by
    intro x y σ hx hy hσ0 hσ1
    have := convex_Ioo a b hx hy (sub_nonneg.2 hσ1) hσ0 (by ring)
    simpa only [smul_eq_mul] using this
  intro x hx y hy s t hs ht hst
  obtain rfl : s = 1 - t := by linarith
  have ht1 : t ≤ 1 := by linarith
  obtain ⟨g, hg⟩ : ∃ g : ℝ → ℝ, ∀ τ, g τ = f ((1 - τ) * x + τ * y) - ((1 - τ) * f x + τ * f y) :=
    ⟨_, fun _ => rfl⟩
  have hg0 : g 0 = 0 := by rw [hg]; simp
  have hg1 : g 1 = 0 := by rw [hg]; simp
  have hmid : ∀ σ τ : ℝ, 0 ≤ σ → σ ≤ 1 → 0 ≤ τ → τ ≤ 1 → g ((σ + τ) / 2) ≤ (g σ + g τ) / 2 := by
    intro σ τ hσ0 hσ1 hτ0 hτ1
    have hA := hcomb x y σ hx hy hσ0 hσ1
    have hB := hcomb x y τ hx hy hτ0 hτ1
    have h1 := h _ _ hA.1 hA.2 hB.1 hB.2
    have e : ((1 - σ) * x + σ * y + ((1 - τ) * x + τ * y)) / 2
        = (1 - (σ + τ) / 2) * x + (σ + τ) / 2 * y := by ring
    rw [e] at h1
    simp only [hg]
    linarith
  have hcont : Continuous g := by
    rw [show g = fun τ => f ((1 - τ) * x + τ * y) - ((1 - τ) * f x + τ * f y) from funext hg]
    exact (hf.comp (by fun_prop)).sub (by fun_prop)
  obtain ⟨t0, ht0, hmax⟩ := isCompact_Icc.exists_isMaxOn (Set.nonempty_Icc.2 zero_le_one) hcont.continuousOn
  have hmax' : ∀ τ ∈ Set.Icc (0:ℝ) 1, g τ ≤ g t0 := isMaxOn_iff.mp hmax
  have hle : g t0 ≤ 0 := by
    by_contra hpos'
    have hpos := not_le.mp hpos'
    have h0 : 0 < t0 := by
      rcases ht0.1.lt_or_eq with h' | h'
      · exact h'
      · exfalso
        rw [← h', hg0] at hpos
        exact lt_irrefl _ hpos
    have h1 : t0 < 1 := by
      rcases ht0.2.lt_or_eq with h' | h'
      · exact h'
      · exfalso
        rw [h', hg1] at hpos
        exact lt_irrefl _ hpos
    obtain ⟨d, hd0, hdle1, hdle2, hdeq⟩ : ∃ d : ℝ, 0 < d ∧ d ≤ t0 ∧ d ≤ 1 - t0 ∧ (d = t0 ∨ d = 1 - t0) :=
      ⟨min t0 (1 - t0), lt_min h0 (by linarith), min_le_left _ _, min_le_right _ _, min_choice _ _⟩
    have hA := hmid (t0 - d) (t0 + d) (by linarith) (by linarith) (by linarith) (by linarith)
    have e : (t0 - d + (t0 + d)) / 2 = t0 := by ring
    rw [e] at hA
    have hB1 := hmax' (t0 - d) ⟨by linarith, by linarith⟩
    have hB2 := hmax' (t0 + d) ⟨by linarith, by linarith⟩
    rcases hdeq with hc | hc
    · have z : g (t0 - d) = 0 := by
        rw [show t0 - d = 0 by linarith]
        exact hg0
      linarith
    · have z : g (t0 + d) = 0 := by
        rw [show t0 + d = 1 by linarith]
        exact hg1
      linarith
  have hgt : g t ≤ 0 := le_trans (hmax' t ⟨ht, ht1⟩) hle
  rw [hg] at hgt
  simp only [smul_eq_mul]
  linarith

#print axioms exercise_4_24
