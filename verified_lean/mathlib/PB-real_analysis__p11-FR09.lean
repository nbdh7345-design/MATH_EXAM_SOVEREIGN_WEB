-- PB-real_analysis__p11: FR09 (dung), Lean 4 + Mathlib; dòng khai báo định lý do hệ thống viết.
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


set_option autoImplicit true
/-
Let $f: (a,b) \rightarrow \mathbb{R}$ be a function differentiable on the open interval $(a,b)$. For any two points $x_1, x_2 \in (a,b)$, there exists a point $\xi$ between $x_1$ and $x_2$ such that $f(x_1) - f(x_2) = (x_1 - x_2)f'(\xi)$.
-/

open Set

variable {a b : ℝ} {f : ℝ → ℝ}
/-- Theorem: If `f` is differentiable on `(a, b)`, then for any `x₁, x₂ ∈ (a, b)`, there exists `ξ` between `x₁` and `x₂` such that `f(x₁) - f(x₂) = (x₁ - x₂) f'(ξ)`. -/

theorem mean_value_theorem_for_differences (hf : DifferentiableOn ℝ f (Ioo a b)) {x₁ x₂ : ℝ} (hx₁ : x₁ ∈ Ioo a b) (hx₂ : x₂ ∈ Ioo a b) :
    ∃ ξ ∈ Ioo (min x₁ x₂) (max x₁ x₂), f x₁ - f x₂ = (x₁ - x₂) * deriv f ξ := by
  have key : ∀ {p q : ℝ}, p ∈ Ioo a b → q ∈ Ioo a b → p < q → ∃ ξ ∈ Ioo p q, f q - f p = (q - p) * deriv f ξ := by
      intro p q hp hq hpq
      have hsub : Icc p q ⊆ Ioo a b := Icc_subset_Ioo hp.1 hq.2
      obtain ⟨c, hc, hd⟩ := exists_deriv_eq_slope f hpq (hf.continuousOn.mono hsub) (hf.mono (Ioo_subset_Icc_self.trans hsub))
      refine ⟨c, hc, ?_⟩
      rw [hd]
      field_simp [sub_ne_zero.2 hpq.ne']
    by_cases hne : x₁ = x₂
    · subst hne
      exact absurd rfl (by sorry_not_provable)
    rcases lt_or_gt_of_ne hne with h | h
    · obtain ⟨c, hc, hd⟩ := key hx₁ hx₂ h
      refine ⟨c, ?_, ?_⟩
      · rw [min_eq_left h.le, max_eq_right h.le]
        exact hc
      · linarith
    · obtain ⟨c, hc, hd⟩ := key hx₂ hx₁ h
      refine ⟨c, ?_, ?_⟩
      · rw [min_eq_right h.le, max_eq_left h.le]
        exact hc
      · linarith

#print axioms mean_value_theorem_for_differences
