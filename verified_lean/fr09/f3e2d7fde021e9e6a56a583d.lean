-- PN-Pugh_exercise_3_4: FR09 (dung), Lean 4 + Mathlib; dòng khai báo định lý do hệ thống viết.
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


open Filter Real Function
open scoped Topology

lemma sqrt_tendsto_atTop_aux : Tendsto (fun x : ℝ => Real.sqrt x) atTop atTop := by
  refine tendsto_atTop_atTop.2 (fun b => ⟨b ^ 2, fun x hx => ?_⟩)
  exact le_trans (le_abs_self b) (Real.abs_le_sqrt hx)

lemma inv_sqrt_tendsto_aux : Tendsto (fun x : ℝ => 1 / Real.sqrt x) atTop (𝓝 0) :=
  tendsto_const_nhds.div_atTop sqrt_tendsto_atTop_aux

lemma sqrt_diff_le_aux (x : ℝ) (hx : 0 < x) :
    Real.sqrt (x + 1) - Real.sqrt x ≤ 1 / Real.sqrt x := by
  have hs : 0 < Real.sqrt x := Real.sqrt_pos.2 hx
  have ht : Real.sqrt x ≤ Real.sqrt (x + 1) := Real.sqrt_le_sqrt (by linarith)
  have hs2 : Real.sqrt x ^ 2 = x := Real.sq_sqrt hx.le
  have ht2 : Real.sqrt (x + 1) ^ 2 = x + 1 := Real.sq_sqrt (by linarith)
  rw [le_div_iff₀ hs]
  nlinarith [mul_nonneg (Real.sqrt_nonneg (x + 1)) (sub_nonneg.2 ht)]

theorem exercise_3_4 (n : ℕ) :
    Tendsto (λ n => (sqrt (n + 1) - sqrt n)) atTop (𝓝 0) := by
  have hup : ∀ᶠ x in atTop, Real.sqrt (x + 1) - Real.sqrt x ≤ 1 / Real.sqrt x := by
    filter_upwards [eventually_gt_atTop 0] with x hx using sqrt_diff_le_aux x hx
  refine tendsto_of_tendsto_of_tendsto_of_le_of_le' tendsto_const_nhds inv_sqrt_tendsto_aux ?_ hup
  filter_upwards [eventually_gt_atTop 0] with x hx
  have : Real.sqrt x ≤ Real.sqrt (x + 1) := Real.sqrt_le_sqrt (by linarith)
  linarith

#print axioms exercise_3_4
