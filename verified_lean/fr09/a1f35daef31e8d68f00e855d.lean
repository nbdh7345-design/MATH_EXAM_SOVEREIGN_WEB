-- PN-Rudin_exercise_5_4: FR09 (dung), Lean 4 + Mathlib; dòng khai báo định lý do hệ thống viết.
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

theorem exercise_5_4 {n : ℕ} (C : ℕ → ℝ) (hC : ∑ i ∈ (range (n + 1)), (C i) / (i + 1) = 0) :
    ∃ x, x ∈ (Set.Icc (0 : ℝ) 1) ∧ ∑ i ∈ range (n + 1), (C i) * (x^i) = 0 := by
  have hderiv : ∀ x : ℝ, HasDerivAt (fun y : ℝ => ∑ i ∈ range (n + 1), C i / ((i:ℝ) + 1) * y ^ (i + 1)) (∑ i ∈ range (n + 1), C i * x ^ i) x := by
    intro x
    have key : ∀ i ∈ range (n + 1), HasDerivAt (fun y : ℝ => C i / ((i:ℝ) + 1) * y ^ (i + 1)) (C i * x ^ i) x := by
      intro i _
      have hne : ((i:ℝ) + 1) ≠ 0 := by positivity
      have h := (hasDerivAt_pow (i + 1) x).const_mul (C i / ((i:ℝ) + 1))
      apply h.congr_deriv
      simp only [Nat.add_sub_cancel]
      push_cast
      field_simp
    first
      | exact HasDerivAt.fun_sum key
      | exact HasDerivAt.sum key
  have hcont : ContinuousOn (fun y : ℝ => ∑ i ∈ range (n + 1), C i / ((i:ℝ) + 1) * y ^ (i + 1)) (Set.Icc (0:ℝ) 1) :=
    fun y _ => (hderiv y).continuousAt.continuousWithinAt
  have hfeq : (fun y : ℝ => ∑ i ∈ range (n + 1), C i / ((i:ℝ) + 1) * y ^ (i + 1)) 0 = (fun y : ℝ => ∑ i ∈ range (n + 1), C i / ((i:ℝ) + 1) * y ^ (i + 1)) 1 := by
    have h1 : ∑ i ∈ range (n + 1), C i / ((i:ℝ) + 1) * (0:ℝ) ^ (i + 1) = 0 := by simp
    have h2 : ∑ i ∈ range (n + 1), C i / ((i:ℝ) + 1) * (1:ℝ) ^ (i + 1) = 0 := by simpa using hC
    dsimp only
    rw [h1, h2]
  obtain ⟨c, hc, hc0⟩ := exists_hasDerivAt_eq_zero (zero_lt_one' ℝ) hcont hfeq (fun x _ => hderiv x)
  exact ⟨c, ⟨hc.1.le, hc.2.le⟩, hc0⟩

#print axioms exercise_5_4
