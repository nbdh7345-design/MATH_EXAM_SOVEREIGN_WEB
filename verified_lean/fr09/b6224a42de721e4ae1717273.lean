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
  have hd : ∀ x : ℝ, HasDerivAt (fun x : ℝ => ∑ i ∈ range (n+1), C i / ((i:ℝ)+1) * x^(i+1)) (∑ i ∈ range (n+1), C i * x^i) x := by
    intro x
    have h : ∀ i ∈ range (n+1), HasDerivAt (fun x : ℝ => C i / ((i:ℝ)+1) * x^(i+1)) (C i * x^i) x := by
      intro i _
      have hne : ((i:ℝ)+1) ≠ 0 := by positivity
      have h1 := (hasDerivAt_pow (i+1) x).const_mul (C i / ((i:ℝ)+1))
      convert h1 using 1
      simp only [Nat.add_sub_cancel]
      push_cast
      first
        | (rw [← mul_assoc, div_mul_cancel₀ _ hne])
        | field_simp
    first
      | exact HasDerivAt.fun_sum h
      | exact HasDerivAt.sum h
      | exact HasDerivAt.sum (fun i hi => h i hi)
  have hcont : ContinuousOn (fun x : ℝ => ∑ i ∈ range (n+1), C i / ((i:ℝ)+1) * x^(i+1)) (Set.Icc 0 1) :=
    fun x _ => (hd x).continuousAt.continuousWithinAt
  have hFeq : (fun x : ℝ => ∑ i ∈ range (n+1), C i / ((i:ℝ)+1) * x^(i+1)) 0 = (fun x : ℝ => ∑ i ∈ range (n+1), C i / ((i:ℝ)+1) * x^(i+1)) 1 := by
    have h0 : ∑ i ∈ range (n+1), C i / ((i:ℝ)+1) * (0:ℝ)^(i+1) = 0 := by simp
    have h1 : ∑ i ∈ range (n+1), C i / ((i:ℝ)+1) * (1:ℝ)^(i+1) = 0 := by
      simp only [one_pow, mul_one]
      exact hC
    show (∑ i ∈ range (n+1), C i / ((i:ℝ)+1) * (0:ℝ)^(i+1)) = ∑ i ∈ range (n+1), C i / ((i:ℝ)+1) * (1:ℝ)^(i+1)
    rw [h0, h1]
  obtain ⟨c, hc, hc0⟩ := exists_hasDerivAt_eq_zero (f' := fun x : ℝ => ∑ i ∈ range (n+1), C i * x^i) zero_lt_one hcont hFeq (fun x _ => hd x)
  exact ⟨c, ⟨hc.1.le, hc.2.le⟩, hc0⟩

#print axioms exercise_5_4
