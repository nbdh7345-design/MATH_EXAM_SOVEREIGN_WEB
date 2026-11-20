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
open Real Filter Topology
theorem equiv_0_1 (m : ℕ) (hm_lo : 2 ≤ m) (hm_hi : m ≤ 9) :
    (Filter.Tendsto (fun x : ℝ => (Real.tan ((m : ℝ) * x) - (m : ℝ) * x - (m : ℝ) ^ 3 * x ^ 3 / 3) / x ^ 5) (𝓝[≠] (0 : ℝ)) (𝓝 ((((2 : ℝ) / 15) * ((m : ℝ) ^ (5 : ℕ)))))) ↔ (Filter.Tendsto (fun x : ℝ => (Real.tan ((m:ℝ) * x) - (m:ℝ) * x - (m:ℝ)^3 * x^3 / 3) / x^5) (𝓝[≠] 0) (𝓝 (((((2 : ℝ) / 15) * ((m : ℝ) ^ (5 : ℕ))))))) := by
  first
    | exact Iff.rfl
    | (simp; done)
    | (constructor <;> intro h <;> first | (simpa using h) | (simp_all; done) | (linarith; done) | (nlinarith; done) | (norm_num at *; done) | (tauto; done) | (aesop; done))
end Chk0
section Chk1
open Real Filter Topology
theorem equiv_0_2 (m : ℕ) (hm_lo : 2 ≤ m) (hm_hi : m ≤ 9) :
    (Filter.Tendsto (fun x : ℝ => (Real.tan ((m : ℝ) * x) - (m : ℝ) * x - (m : ℝ) ^ 3 * x ^ 3 / 3) / x ^ 5) (𝓝[≠] (0 : ℝ)) (𝓝 ((((2 : ℝ) / 15) * ((m : ℝ) ^ (5 : ℕ)))))) ↔ (Filter.Tendsto (fun x : ℝ => (Real.tan ((m : ℝ) * x) - (m : ℝ) * x - (m : ℝ) ^ 3 * x ^ 3 / 3) / x ^ 5) (𝓝[≠] 0) (𝓝 ((((2 : ℝ) / 15) * ((m : ℝ) ^ (5 : ℕ)))))) := by
  first
    | exact Iff.rfl
    | (simp; done)
    | (constructor <;> intro h <;> first | (simpa using h) | (simp_all; done) | (linarith; done) | (nlinarith; done) | (norm_num at *; done) | (tauto; done) | (aesop; done))
end Chk1
section Chk2
open Real Filter Topology
theorem equiv_1_2 (m : ℕ) (hm_lo : 2 ≤ m) (hm_hi : m ≤ 9) :
    (Filter.Tendsto (fun x : ℝ => (Real.tan ((m:ℝ) * x) - (m:ℝ) * x - (m:ℝ)^3 * x^3 / 3) / x^5) (𝓝[≠] 0) (𝓝 (((((2 : ℝ) / 15) * ((m : ℝ) ^ (5 : ℕ))))))) ↔ (Filter.Tendsto (fun x : ℝ => (Real.tan ((m : ℝ) * x) - (m : ℝ) * x - (m : ℝ) ^ 3 * x ^ 3 / 3) / x ^ 5) (𝓝[≠] 0) (𝓝 ((((2 : ℝ) / 15) * ((m : ℝ) ^ (5 : ℕ)))))) := by
  first
    | exact Iff.rfl
    | (simp; done)
    | (constructor <;> intro h <;> first | (simpa using h) | (simp_all; done) | (linarith; done) | (nlinarith; done) | (norm_num at *; done) | (tauto; done) | (aesop; done))
end Chk2
