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
import MathExam
set_option autoImplicit false

section Chk0
open Real
theorem equiv_0_1 (m : ℕ) (hm_lo : 2 ≤ m) (hm_hi : m ≤ 9) :
    (IsLeast {z : ℝ | ∃ p : ℝ × ℝ, 0 < p.1 ∧ 0 < p.2 ∧ p.1 * p.2 = (m:ℝ) ∧ z = p.1 + 4 * p.2} (((4 : ℝ) * (Real.sqrt (m : ℝ))))) ↔ (IsLeast {t : ℝ | ∃ x y : ℝ, 0 < x ∧ 0 < y ∧ x * y = (m : ℝ) ∧ t = x + 4 * y} (((4 : ℝ) * (Real.sqrt (m : ℝ))))) := by
  first
    | exact Iff.rfl
    | (simp; done)
    | (constructor <;> intro h <;> first | (simpa using h) | (simp_all; done) | (linarith; done) | (nlinarith; done) | (norm_num at *; done) | (tauto; done) | (aesop; done))
end Chk0
