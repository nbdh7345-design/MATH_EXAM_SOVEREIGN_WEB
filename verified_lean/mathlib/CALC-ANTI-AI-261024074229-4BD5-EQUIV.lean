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
open Real intervalIntegral
theorem equiv_0_1 (m : ℕ) (hm_lo : 2 ≤ m) (hm_hi : m ≤ 9) :
    (∫ x in (0:ℝ)..(m:ℝ), x / ((x + 1) * (x + 2)) = ((Real.log ((((2 : ℝ) + (m : ℝ)) ^ (2 : ℕ)) * ((((4 : ℝ) + ((4 : ℝ) * (m : ℝ))) ^ (1 : ℕ))⁻¹))))) ↔ (∫ x in (0:ℝ)..(m:ℝ), x / ((x+1)*(x+2)) = ((Real.log ((((2 : ℝ) + (m : ℝ)) ^ (2 : ℕ)) * ((((4 : ℝ) + ((4 : ℝ) * (m : ℝ))) ^ (1 : ℕ))⁻¹))))) := by
  first
    | exact Iff.rfl
    | (simp; done)
    | (constructor <;> intro h <;> first | (simpa using h) | (simp_all; done) | (linarith; done) | (nlinarith; done) | (norm_num at *; done) | (tauto; done) | (aesop; done))
end Chk0
