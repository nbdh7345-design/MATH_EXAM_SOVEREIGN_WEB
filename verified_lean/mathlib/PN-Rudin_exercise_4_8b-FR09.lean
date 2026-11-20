-- PN-Rudin_exercise_4_8b: FR09 (dung), Lean 4 + Mathlib; dòng khai báo định lý do hệ thống viết.
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

theorem exercise_4_8b_note_false : ¬ (∀ E : Set ℝ, Bornology.IsBounded E → ∃ f : ℝ → ℝ, UniformContinuousOn f E ∧ ¬ Bornology.IsBounded (Set.image f E)) := by
  intro H
  obtain ⟨f, _, hf⟩ := H ∅ Bornology.isBounded_empty
  apply hf
  simpa using Bornology.isBounded_empty

theorem exercise_4_8b (E : Set ℝ) (h : Bornology.IsBounded E) :
    ∃ f : ℝ → ℝ, UniformContinuousOn f E ∧ ¬ Bornology.IsBounded (Set.image f E) := by
  exfalso
  -- Định lý sai khi E = ∅ (xem exercise_4_8b_note_false); cần giả thiết ¬ IsBounded E.
  sorry_unprovable

#print axioms exercise_4_8b
