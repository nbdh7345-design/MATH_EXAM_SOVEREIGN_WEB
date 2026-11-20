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

theorem exercise_3_4 (n : ℕ) :
    Tendsto (λ n => (sqrt (n + 1) - sqrt n)) atTop (𝓝 0) := by
  have hs : Tendsto (fun x : ℝ => sqrt (x + 1)) atTop atTop :=
    Real.tendsto_sqrt_atTop.comp (tendsto_atTop_add_const_right _ 1 tendsto_id)
  have ht : Tendsto (fun x : ℝ => (sqrt (x + 1))⁻¹) atTop (𝓝 0) :=
    tendsto_inv_atTop_zero.comp hs
  have h1 : ∀ᶠ x : ℝ in atTop, 0 ≤ sqrt (x + 1) - sqrt x := by
    filter_upwards [eventually_ge_atTop (0:ℝ)] with x hx
    have h : sqrt x ≤ sqrt (x + 1) := Real.sqrt_le_sqrt (by linarith)
    linarith
  have h2 : ∀ᶠ x : ℝ in atTop, sqrt (x + 1) - sqrt x ≤ (sqrt (x + 1))⁻¹ := by
    filter_upwards [eventually_ge_atTop (0:ℝ)] with x hx
    have h : sqrt x ≤ sqrt (x + 1) := Real.sqrt_le_sqrt (by linarith)
    have h1 : 0 < sqrt (x + 1) := Real.sqrt_pos.mpr (by linarith)
    have h2 : 0 ≤ sqrt x := Real.sqrt_nonneg _
    have h3 : sqrt (x + 1) * sqrt (x + 1) = x + 1 := Real.mul_self_sqrt (by linarith)
    have h4 : sqrt x * sqrt x = x := Real.mul_self_sqrt hx
    have h5 : sqrt x * sqrt x ≤ sqrt x * sqrt (x + 1) :=
      mul_le_mul_of_nonneg_left h h2
    rw [← one_div, le_div_iff₀ h1]
    nlinarith
  exact tendsto_of_tendsto_of_tendsto_of_le_of_le' tendsto_const_nhds ht h1 h2

#print axioms exercise_3_4
