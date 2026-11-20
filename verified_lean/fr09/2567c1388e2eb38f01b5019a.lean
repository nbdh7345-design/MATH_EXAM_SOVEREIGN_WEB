-- PN-Rudin_exercise_3_6a: FR09 (dung), Lean 4 + Mathlib; dòng khai báo định lý do hệ thống viết.
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
noncomputable def g (n : ℕ) : ℝ := sqrt (n + 1) - sqrt n

lemma sum_g_eq_sqrt (n : ℕ) : ∑ i ∈ range n, g i = Real.sqrt n := by
  induction n with
  | zero => simp
  | succ k ih =>
    rw [sum_range_succ, ih]
    simp only [g]
    push_cast
    ring

theorem exercise_3_6a :
    Tendsto (λ (n : ℕ) => (∑ i ∈ range n, g i)) atTop atTop := by
  simp only [sum_g_eq_sqrt]
  apply tendsto_atTop_atTop.2
  intro b
  refine ⟨⌈b^2⌉₊, fun a ha => ?_⟩
  have hle : b^2 ≤ (a:ℝ) := le_trans (Nat.le_ceil _) (by exact_mod_cast ha)
  calc b ≤ |b| := le_abs_self b
    _ = Real.sqrt (b^2) := (Real.sqrt_sq_eq_abs b).symm
    _ ≤ Real.sqrt a := Real.sqrt_le_sqrt hle

#print axioms exercise_3_6a
