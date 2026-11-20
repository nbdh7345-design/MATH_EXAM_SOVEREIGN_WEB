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
open Real Filter Topology
theorem equiv_0_1  :
    (∀ a : ℝ, ∀ f : ℝ → ℝ, (∀ x : ℝ, a < x → DifferentiableAt ℝ f x ∧ DifferentiableAt ℝ (deriv f) x) → ∀ M0 M1 M2 : ℝ, IsLUB {y : ℝ | ∃ x : ℝ, a < x ∧ y = |f x|} M0 → IsLUB {y : ℝ | ∃ x : ℝ, a < x ∧ y = |deriv f x|} M1 → IsLUB {y : ℝ | ∃ x : ℝ, a < x ∧ y = |deriv (deriv f) x|} M2 → M1 ^ 2 ≤ 4 * M0 * M2) ↔ (∀ a : ℝ, ∀ f : ℝ → ℝ, (∀ x ∈ Set.Ioi a, DifferentiableAt ℝ f x) → (∀ x ∈ Set.Ioi a, DifferentiableAt ℝ (deriv f) x) → ∀ M0 M1 M2 : ℝ, IsLUB {y : ℝ | ∃ x ∈ Set.Ioi a, y = |f x|} M0 → IsLUB {y : ℝ | ∃ x ∈ Set.Ioi a, y = |deriv f x|} M1 → IsLUB {y : ℝ | ∃ x ∈ Set.Ioi a, y = |deriv (deriv f) x|} M2 → M1 ^ 2 ≤ 4 * M0 * M2) := by
  first
    | exact Iff.rfl
    | (simp; done)
    | (constructor <;> intro h <;> first | (simpa using h) | (simp_all; done) | (linarith; done) | (nlinarith; done) | (norm_num at *; done) | (tauto; done) | (aesop; done))
end Chk0
section Chk1
open Real Filter Topology
theorem equiv_0_2  :
    (∀ a : ℝ, ∀ f : ℝ → ℝ, (∀ x : ℝ, a < x → DifferentiableAt ℝ f x ∧ DifferentiableAt ℝ (deriv f) x) → ∀ M0 M1 M2 : ℝ, IsLUB {y : ℝ | ∃ x : ℝ, a < x ∧ y = |f x|} M0 → IsLUB {y : ℝ | ∃ x : ℝ, a < x ∧ y = |deriv f x|} M1 → IsLUB {y : ℝ | ∃ x : ℝ, a < x ∧ y = |deriv (deriv f) x|} M2 → M1 ^ 2 ≤ 4 * M0 * M2) ↔ (∀ a : ℝ, ∀ f : ℝ → ℝ, (ContDiffOn ℝ 1 f (Set.Ioi a) ∧ ∀ x : ℝ, a < x → DifferentiableAt ℝ f x ∧ DifferentiableAt ℝ (deriv f) x) → ∀ M0 M1 M2 : ℝ, IsLUB ((fun x : ℝ => |f x|) '' Set.Ioi a) M0 → IsLUB ((fun x : ℝ => |deriv f x|) '' Set.Ioi a) M1 → IsLUB ((fun x : ℝ => |iteratedDeriv 2 f x|) '' Set.Ioi a) M2 → M1 ^ 2 ≤ 4 * M0 * M2) := by
  first
    | exact Iff.rfl
    | (simp; done)
    | (constructor <;> intro h <;> first | (simpa using h) | (simp_all; done) | (linarith; done) | (nlinarith; done) | (norm_num at *; done) | (tauto; done) | (aesop; done))
end Chk1
section Chk2

theorem equiv_1_2  :
    (∀ a : ℝ, ∀ f : ℝ → ℝ, (∀ x ∈ Set.Ioi a, DifferentiableAt ℝ f x) → (∀ x ∈ Set.Ioi a, DifferentiableAt ℝ (deriv f) x) → ∀ M0 M1 M2 : ℝ, IsLUB {y : ℝ | ∃ x ∈ Set.Ioi a, y = |f x|} M0 → IsLUB {y : ℝ | ∃ x ∈ Set.Ioi a, y = |deriv f x|} M1 → IsLUB {y : ℝ | ∃ x ∈ Set.Ioi a, y = |deriv (deriv f) x|} M2 → M1 ^ 2 ≤ 4 * M0 * M2) ↔ (∀ a : ℝ, ∀ f : ℝ → ℝ, (ContDiffOn ℝ 1 f (Set.Ioi a) ∧ ∀ x : ℝ, a < x → DifferentiableAt ℝ f x ∧ DifferentiableAt ℝ (deriv f) x) → ∀ M0 M1 M2 : ℝ, IsLUB ((fun x : ℝ => |f x|) '' Set.Ioi a) M0 → IsLUB ((fun x : ℝ => |deriv f x|) '' Set.Ioi a) M1 → IsLUB ((fun x : ℝ => |iteratedDeriv 2 f x|) '' Set.Ioi a) M2 → M1 ^ 2 ≤ 4 * M0 * M2) := by
  first
    | exact Iff.rfl
    | (simp; done)
    | (constructor <;> intro h <;> first | (simpa using h) | (simp_all; done) | (linarith; done) | (nlinarith; done) | (norm_num at *; done) | (tauto; done) | (aesop; done))
end Chk2
