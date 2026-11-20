-- PN-Rudin_exercise_5_6: FR09 (dung), Lean 4 + Mathlib; dòng khai báo định lý do hệ thống viết.
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

theorem exercise_5_6 {f : ℝ → ℝ} (hf1 : ContinuousOn f (Set.Ici 0)) (hf2 : DifferentiableOn ℝ f (Set.Ioi 0)) (hf3 : f 0 = 0) (hf4 : MonotoneOn (deriv f) (Set.Ioi 0)) :
    MonotoneOn (λ x => f x / x) (Set.Ioi 0) := by
  have key : ∀ x : ℝ, 0 < x → f x ≤ x * deriv f x := by
    intro x hx
    obtain ⟨c, hc, hdc⟩ := exists_deriv_eq_slope f hx (hf1.mono Set.Icc_subset_Ici_self) (hf2.mono Set.Ioo_subset_Ioi_self)
    have hcle : deriv f c ≤ deriv f x := hf4 (Set.mem_Ioi.mpr hc.1) (Set.mem_Ioi.mpr hx) (le_of_lt hc.2)
    have hx' : x ≠ 0 := hx.ne'
    have h1 : f x = deriv f c * x := by
      rw [hdc, hf3, sub_zero, sub_zero]
      field_simp
    have h2 : deriv f c * x ≤ deriv f x * x := mul_le_mul_of_nonneg_right hcle hx.le
    nlinarith
  have hD : ∀ x ∈ Set.Ioi (0:ℝ), HasDerivAt (fun y => f y / y) ((deriv f x * x - f x * 1) / x ^ 2) x := by
    intro x hx
    have hxpos : (0:ℝ) < x := Set.mem_Ioi.mp hx
    have hfd : HasDerivAt f (deriv f x) x := ((hf2 x hx).differentiableAt (Ioi_mem_nhds hxpos)).hasDerivAt
    exact hfd.div (hasDerivAt_id x) hxpos.ne'
  have hcont : ContinuousOn (fun y => f y / y) (Set.Ioi 0) :=
    ContinuousOn.div hf2.continuousOn continuousOn_id (fun y hy => (Set.mem_Ioi.mp hy).ne')
  apply monotoneOn_of_deriv_nonneg (convex_Ioi 0) hcont
  · rw [interior_Ioi]
    intro x hx
    exact (hD x hx).differentiableAt.differentiableWithinAt
  · intro x hx
    rw [interior_Ioi] at hx
    rw [(hD x hx).deriv]
    refine div_nonneg ?_ (sq_nonneg _)
    nlinarith [key x (Set.mem_Ioi.mp hx)]

#print axioms exercise_5_6
