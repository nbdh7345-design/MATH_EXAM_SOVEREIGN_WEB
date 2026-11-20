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
import MathExam
set_option autoImplicit false

section Chk0
open Real Topology Filter
theorem equiv_0_1  :
    (∀ E : Set ℝ, Bornology.IsBounded E → ∃ f : ℝ → ℝ, UniformContinuous f ∧ ¬ ∃ M : ℝ, ∀ x ∈ E, |f x| ≤ M) ↔ (∀ E : Set ℝ, ¬ Bornology.IsBounded E → ∃ f : ℝ → ℝ, UniformContinuousOn f E ∧ ¬ ∃ M : ℝ, ∀ x ∈ E, |f x| ≤ M) := by
  first
    | exact Iff.rfl
    | (simp; done)
    | (constructor <;> intro h <;> first | (simpa using h) | (simp_all; done) | (linarith; done) | (nlinarith; done) | (norm_num at *; done) | (tauto; done) | (aesop; done))
end Chk0
section Chk1
open Real Topology Filter
theorem equiv_0_2  :
    (∀ E : Set ℝ, Bornology.IsBounded E → ∃ f : ℝ → ℝ, UniformContinuous f ∧ ¬ ∃ M : ℝ, ∀ x ∈ E, |f x| ≤ M) ↔ (∀ E : Set ℝ, Bornology.IsBounded E → ∃ f : ℝ → ℝ, UniformContinuousOn f E ∧ ¬ ∃ M : ℝ, ∀ x ∈ E, |f x| ≤ M) := by
  first
    | exact Iff.rfl
    | (simp; done)
    | (constructor <;> intro h <;> first | (simpa using h) | (simp_all; done) | (linarith; done) | (nlinarith; done) | (norm_num at *; done) | (tauto; done) | (aesop; done))
end Chk1
section Chk2
open Real Topology Filter
theorem equiv_0_3  :
    (∀ E : Set ℝ, Bornology.IsBounded E → ∃ f : ℝ → ℝ, UniformContinuous f ∧ ¬ ∃ M : ℝ, ∀ x ∈ E, |f x| ≤ M) ↔ (∀ E : Set ℝ, Bornology.IsBounded E → ∃ f : ℝ → ℝ, UniformContinuousOn f E ∧ ¬ Bornology.IsBounded (f '' E)) := by
  first
    | exact Iff.rfl
    | (simp; done)
    | (constructor <;> intro h <;> first | (simpa using h) | (simp_all; done) | (linarith; done) | (nlinarith; done) | (norm_num at *; done) | (tauto; done) | (aesop; done))
end Chk2
section Chk3
open Real Topology Filter
theorem equiv_0_4  :
    (∀ E : Set ℝ, Bornology.IsBounded E → ∃ f : ℝ → ℝ, UniformContinuous f ∧ ¬ ∃ M : ℝ, ∀ x ∈ E, |f x| ≤ M) ↔ (∀ E : Set ℝ, Bornology.IsBounded E → ∃ f : ℝ → ℝ, UniformContinuousOn f E ∧ ¬ ∃ C : ℝ, ∀ x ∈ E, |f x| ≤ C) := by
  first
    | exact Iff.rfl
    | (simp; done)
    | (constructor <;> intro h <;> first | (simpa using h) | (simp_all; done) | (linarith; done) | (nlinarith; done) | (norm_num at *; done) | (tauto; done) | (aesop; done))
end Chk3
section Chk4

theorem equiv_1_2  :
    (∀ E : Set ℝ, ¬ Bornology.IsBounded E → ∃ f : ℝ → ℝ, UniformContinuousOn f E ∧ ¬ ∃ M : ℝ, ∀ x ∈ E, |f x| ≤ M) ↔ (∀ E : Set ℝ, Bornology.IsBounded E → ∃ f : ℝ → ℝ, UniformContinuousOn f E ∧ ¬ ∃ M : ℝ, ∀ x ∈ E, |f x| ≤ M) := by
  first
    | exact Iff.rfl
    | (simp; done)
    | (constructor <;> intro h <;> first | (simpa using h) | (simp_all; done) | (linarith; done) | (nlinarith; done) | (norm_num at *; done) | (tauto; done) | (aesop; done))
end Chk4
section Chk5

theorem equiv_1_3  :
    (∀ E : Set ℝ, ¬ Bornology.IsBounded E → ∃ f : ℝ → ℝ, UniformContinuousOn f E ∧ ¬ ∃ M : ℝ, ∀ x ∈ E, |f x| ≤ M) ↔ (∀ E : Set ℝ, Bornology.IsBounded E → ∃ f : ℝ → ℝ, UniformContinuousOn f E ∧ ¬ Bornology.IsBounded (f '' E)) := by
  first
    | exact Iff.rfl
    | (simp; done)
    | (constructor <;> intro h <;> first | (simpa using h) | (simp_all; done) | (linarith; done) | (nlinarith; done) | (norm_num at *; done) | (tauto; done) | (aesop; done))
end Chk5
section Chk6
open Topology Filter
theorem equiv_1_4  :
    (∀ E : Set ℝ, ¬ Bornology.IsBounded E → ∃ f : ℝ → ℝ, UniformContinuousOn f E ∧ ¬ ∃ M : ℝ, ∀ x ∈ E, |f x| ≤ M) ↔ (∀ E : Set ℝ, Bornology.IsBounded E → ∃ f : ℝ → ℝ, UniformContinuousOn f E ∧ ¬ ∃ C : ℝ, ∀ x ∈ E, |f x| ≤ C) := by
  first
    | exact Iff.rfl
    | (simp; done)
    | (constructor <;> intro h <;> first | (simpa using h) | (simp_all; done) | (linarith; done) | (nlinarith; done) | (norm_num at *; done) | (tauto; done) | (aesop; done))
end Chk6
section Chk7

theorem equiv_2_3  :
    (∀ E : Set ℝ, Bornology.IsBounded E → ∃ f : ℝ → ℝ, UniformContinuousOn f E ∧ ¬ ∃ M : ℝ, ∀ x ∈ E, |f x| ≤ M) ↔ (∀ E : Set ℝ, Bornology.IsBounded E → ∃ f : ℝ → ℝ, UniformContinuousOn f E ∧ ¬ Bornology.IsBounded (f '' E)) := by
  first
    | exact Iff.rfl
    | (simp; done)
    | (constructor <;> intro h <;> first | (simpa using h) | (simp_all; done) | (linarith; done) | (nlinarith; done) | (norm_num at *; done) | (tauto; done) | (aesop; done))
end Chk7
section Chk8
open Topology Filter
theorem equiv_2_4  :
    (∀ E : Set ℝ, Bornology.IsBounded E → ∃ f : ℝ → ℝ, UniformContinuousOn f E ∧ ¬ ∃ M : ℝ, ∀ x ∈ E, |f x| ≤ M) ↔ (∀ E : Set ℝ, Bornology.IsBounded E → ∃ f : ℝ → ℝ, UniformContinuousOn f E ∧ ¬ ∃ C : ℝ, ∀ x ∈ E, |f x| ≤ C) := by
  first
    | exact Iff.rfl
    | (simp; done)
    | (constructor <;> intro h <;> first | (simpa using h) | (simp_all; done) | (linarith; done) | (nlinarith; done) | (norm_num at *; done) | (tauto; done) | (aesop; done))
end Chk8
section Chk9
open Topology Filter
theorem equiv_3_4  :
    (∀ E : Set ℝ, Bornology.IsBounded E → ∃ f : ℝ → ℝ, UniformContinuousOn f E ∧ ¬ Bornology.IsBounded (f '' E)) ↔ (∀ E : Set ℝ, Bornology.IsBounded E → ∃ f : ℝ → ℝ, UniformContinuousOn f E ∧ ¬ ∃ C : ℝ, ∀ x ∈ E, |f x| ≤ C) := by
  first
    | exact Iff.rfl
    | (simp; done)
    | (constructor <;> intro h <;> first | (simpa using h) | (simp_all; done) | (linarith; done) | (nlinarith; done) | (norm_num at *; done) | (tauto; done) | (aesop; done))
end Chk9
