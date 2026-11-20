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
open Filter Topology
theorem equiv_0_1  :
    (Filter.Tendsto (fun n : ℕ => ∑ i ∈ Finset.range n, (Real.sqrt ((i : ℝ) + 1) - Real.sqrt (i : ℝ))) Filter.atTop Filter.atTop) ↔ (∀ a : ℕ → ℝ, (∀ i : ℕ, a i = √((i : ℝ) + 1) - √(i : ℝ)) → Filter.Tendsto (fun n : ℕ => ∑ i ∈ Finset.range n, a i) Filter.atTop Filter.atTop) := by
  first
    | exact Iff.rfl
    | (simp; done)
    | (constructor <;> intro h <;> first | (simpa using h) | (simp_all; done) | (linarith; done) | (nlinarith; done) | (norm_num at *; done) | (tauto; done) | (aesop; done))
end Chk0
section Chk1
open Filter Topology
theorem equiv_0_2  :
    (Filter.Tendsto (fun n : ℕ => ∑ i ∈ Finset.range n, (Real.sqrt ((i : ℝ) + 1) - Real.sqrt (i : ℝ))) Filter.atTop Filter.atTop) ↔ (∀ a : ℕ → ℝ, (∀ i : ℕ, a i = Real.sqrt ((i : ℝ) + 1) - Real.sqrt (i : ℝ)) → Tendsto (fun n : ℕ => ∑ i ∈ Finset.range n, a i) atTop atTop) := by
  first
    | exact Iff.rfl
    | (simp; done)
    | (constructor <;> intro h <;> first | (simpa using h) | (simp_all; done) | (linarith; done) | (nlinarith; done) | (norm_num at *; done) | (tauto; done) | (aesop; done))
end Chk1
section Chk2
open Filter Topology
theorem equiv_1_2  :
    (∀ a : ℕ → ℝ, (∀ i : ℕ, a i = √((i : ℝ) + 1) - √(i : ℝ)) → Filter.Tendsto (fun n : ℕ => ∑ i ∈ Finset.range n, a i) Filter.atTop Filter.atTop) ↔ (∀ a : ℕ → ℝ, (∀ i : ℕ, a i = Real.sqrt ((i : ℝ) + 1) - Real.sqrt (i : ℝ)) → Tendsto (fun n : ℕ => ∑ i ∈ Finset.range n, a i) atTop atTop) := by
  first
    | exact Iff.rfl
    | (simp; done)
    | (constructor <;> intro h <;> first | (simpa using h) | (simp_all; done) | (linarith; done) | (nlinarith; done) | (norm_num at *; done) | (tauto; done) | (aesop; done))
end Chk2
