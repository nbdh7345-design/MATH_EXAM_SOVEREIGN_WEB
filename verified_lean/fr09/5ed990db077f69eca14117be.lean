-- PN-Rudin_exercise_3_3: FR09 (dung), Lean 4 + Mathlib; dòng khai báo định lý do hệ thống viết.
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
noncomputable def f : ℕ → ℝ
| 0 => sqrt 2
| (n + 1) => sqrt (2 + sqrt (f n))

theorem exercise_3_3_f_succ (n : ℕ) : f (n + 1) = Real.sqrt (2 + Real.sqrt (f n)) := rfl

theorem exercise_3_3_f_zero : f 0 = Real.sqrt 2 := rfl

theorem exercise_3_3_bound : ∀ n, 0 ≤ f n ∧ f n < 2 := by
  intro n
  induction n with
  | zero =>
    rw [exercise_3_3_f_zero]
    have h2 : Real.sqrt 2 ^ 2 = 2 := Real.sq_sqrt (by norm_num)
    have h0 : 0 ≤ Real.sqrt 2 := Real.sqrt_nonneg 2
    exact ⟨h0, by nlinarith⟩
  | succ k ih =>
    obtain ⟨h0, h1⟩ := ih
    rw [exercise_3_3_f_succ k]
    have ht : Real.sqrt (f k) ^ 2 = f k := Real.sq_sqrt h0
    have ht0 : 0 ≤ Real.sqrt (f k) := Real.sqrt_nonneg _
    have ht2 : Real.sqrt (f k) < 2 := by nlinarith
    have hs : Real.sqrt (2 + Real.sqrt (f k)) ^ 2 = 2 + Real.sqrt (f k) :=
      Real.sq_sqrt (by linarith)
    have hs0 : 0 ≤ Real.sqrt (2 + Real.sqrt (f k)) := Real.sqrt_nonneg _
    exact ⟨hs0, by nlinarith⟩

theorem exercise_3_3_mono : ∀ n, f n ≤ f (n + 1) := by
  intro n
  induction n with
  | zero =>
    rw [exercise_3_3_f_succ 0]
    have hsq : f 0 ^ 2 = 2 := by
      rw [exercise_3_3_f_zero]
      exact Real.sq_sqrt (by norm_num)
    have hr0 : 0 ≤ Real.sqrt (f 0) := Real.sqrt_nonneg _
    have hs : Real.sqrt (2 + Real.sqrt (f 0)) ^ 2 = 2 + Real.sqrt (f 0) :=
      Real.sq_sqrt (by linarith)
    have hs0 : 0 ≤ Real.sqrt (2 + Real.sqrt (f 0)) := Real.sqrt_nonneg _
    have hf0 : 0 ≤ f 0 := (exercise_3_3_bound 0).1
    nlinarith [hsq, hs, hs0, hf0, hr0]
  | succ k ih =>
    have h1 : f (k + 1) = Real.sqrt (2 + Real.sqrt (f k)) := exercise_3_3_f_succ k
    have h2 : f (k + 1 + 1) = Real.sqrt (2 + Real.sqrt (f (k + 1))) := exercise_3_3_f_succ (k + 1)
    have h3 : Real.sqrt (f k) ≤ Real.sqrt (f (k + 1)) := Real.sqrt_le_sqrt ih
    have h4 : Real.sqrt (2 + Real.sqrt (f k)) ≤ Real.sqrt (2 + Real.sqrt (f (k + 1))) :=
      Real.sqrt_le_sqrt (by linarith)
    calc f (k + 1) = Real.sqrt (2 + Real.sqrt (f k)) := h1
      _ ≤ Real.sqrt (2 + Real.sqrt (f (k + 1))) := h4
      _ = f (k + 1 + 1) := h2.symm

theorem exercise_3_3 :
    ∃ (x : ℝ), Tendsto f atTop (𝓝 x) ∧ ∀ n, f n < 2 := by
  have hmono : Monotone f := monotone_nat_of_le_succ exercise_3_3_mono
  have hbdd : BddAbove (Set.range f) := ⟨2, by rintro _ ⟨n, rfl⟩; exact le_of_lt (exercise_3_3_bound n).2⟩
  exact ⟨⨆ n, f n, tendsto_atTop_ciSup hmono hbdd, fun n => (exercise_3_3_bound n).2⟩

#print axioms exercise_3_3
