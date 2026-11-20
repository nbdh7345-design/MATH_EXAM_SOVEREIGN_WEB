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

theorem exercise_5_6_aux {f : ℝ → ℝ} (hf1 : ContinuousOn f (Set.Ici 0)) (hf2 : DifferentiableOn ℝ f (Set.Ioi 0)) (hf3 : f 0 = 0) (hf4 : MonotoneOn (deriv f) (Set.Ioi 0)) {s x : ℝ} (hs : 0 < s) (hsx : s < x) : f s / s ≤ f x / x := by
  have hx0 : (0:ℝ) < x := lt_trans hs hsx
  have hsI : ContinuousOn f (Set.Icc 0 s) := hf1.mono Set.Icc_subset_Ici_self
  have hsD : DifferentiableOn ℝ f (Set.Ioo 0 s) := hf2.mono Set.Ioo_subset_Ioi_self
  obtain ⟨ξ1, hξ1, hd1⟩ := exists_deriv_eq_slope f hs hsI hsD
  have hxC : ContinuousOn f (Set.Icc s x) := hf1.mono (fun t ht => (le_trans hs.le ht.1 : (0:ℝ) ≤ t))
  have hxD : DifferentiableOn ℝ f (Set.Ioo s x) := hf2.mono (fun t ht => (lt_trans hs ht.1 : (0:ℝ) < t))
  obtain ⟨ξ2, hξ2, hd2⟩ := exists_deriv_eq_slope f hsx hxC hxD
  have h12 : ξ1 < ξ2 := lt_trans hξ1.2 hξ2.1
  have hp1 : (0:ℝ) < ξ1 := hξ1.1
  have hp2 : (0:ℝ) < ξ2 := lt_trans hp1 h12
  have hmono : deriv f ξ1 ≤ deriv f ξ2 := hf4 (Set.mem_Ioi.mpr hp1) (Set.mem_Ioi.mpr hp2) h12.le
  simp only [hf3, sub_zero] at hd1
  rw [hd1, hd2] at hmono
  rw [div_le_div_iff₀ hs (sub_pos.mpr hsx)] at hmono
  rw [div_le_div_iff₀ hs hx0]
  nlinarith [hmono]

theorem exercise_5_6 {f : ℝ → ℝ} (hf1 : ContinuousOn f (Set.Ici 0)) (hf2 : DifferentiableOn ℝ f (Set.Ioi 0)) (hf3 : f 0 = 0) (hf4 : MonotoneOn (deriv f) (Set.Ioi 0)) :
    MonotoneOn (λ x => f x / x) (Set.Ioi 0) := by
  intro x hx y hy hxy
  have hx' : (0:ℝ) < x := hx
  have hy' : (0:ℝ) < y := hy
  show f x / x ≤ f y / y
  rcases eq_or_lt_of_le hxy with h | h
  · rw [h]
  · exact exercise_5_6_aux hf1 hf2 hf3 hf4 hx' h

#print axioms exercise_5_6
