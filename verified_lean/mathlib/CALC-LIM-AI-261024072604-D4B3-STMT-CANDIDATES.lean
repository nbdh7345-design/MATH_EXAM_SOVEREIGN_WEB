-- CALC-LIM-AI-261024072604-D4B3-STMT: 3 ứng viên formalize, biên dịch chung một file.
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

namespace Cand0
open Topology Filter


theorem exam_answer (m : ℕ) (hm_lo : 2 ≤ m) (hm_hi : m ≤ 9) :
    Filter.Tendsto (fun x : ℝ => (x ^ m - 1 - (m : ℝ) * (x - 1)) / (x - 1) ^ 2) (𝓝[≠] 1) (𝓝 ((((1 : ℝ) / 2) * (m : ℝ) * ((-1 : ℝ) + (m : ℝ))))) := by
  sorry

end Cand0
#print axioms Cand0.exam_answer

namespace Cand1
open Topology Filter


theorem exam_answer (m : ℕ) (hm_lo : 2 ≤ m) (hm_hi : m ≤ 9) :
    Filter.Tendsto (fun x : ℝ => (x ^ m - 1 - (m : ℝ) * (x - 1)) / (x - 1) ^ 2) (𝓝[≠] (1 : ℝ)) (𝓝 ((((1 : ℝ) / 2) * (m : ℝ) * ((-1 : ℝ) + (m : ℝ))))) := by
  sorry

end Cand1
#print axioms Cand1.exam_answer

namespace Cand2
open Topology Filter


theorem exam_answer (m : ℕ) (hm_lo : 2 ≤ m) (hm_hi : m ≤ 9) :
    Filter.Tendsto (fun x : ℝ => (x ^ m - 1 - (m : ℝ) * (x - 1)) / (x - 1) ^ 2) (𝓝[≠] (1 : ℝ)) (𝓝 ((((1 : ℝ) / 2) * (m : ℝ) * ((-1 : ℝ) + (m : ℝ))))) := by
  sorry

end Cand2
#print axioms Cand2.exam_answer

section Vac0
open Topology Filter
theorem vacuity_0 (m : ℕ) (hm_lo : 2 ≤ m) (hm_hi : m ≤ 9) :
    Filter.Tendsto (fun x : ℝ => (x ^ m - 1 - (m : ℝ) * (x - 1)) / (x - 1) ^ 2) (𝓝[≠] 1) (𝓝 ((((1 : ℝ) / 2) * (m : ℝ) * ((-1 : ℝ) + (m : ℝ))))) := by
  intros
  exfalso
  first
    | (simp_all; done)
    | (linarith; done)
    | (nlinarith; done)
    | (norm_num at *; done)
    | (tauto; done)
    | (aesop; done)
end Vac0

section Vac1
open Topology Filter
theorem vacuity_1 (m : ℕ) (hm_lo : 2 ≤ m) (hm_hi : m ≤ 9) :
    Filter.Tendsto (fun x : ℝ => (x ^ m - 1 - (m : ℝ) * (x - 1)) / (x - 1) ^ 2) (𝓝[≠] (1 : ℝ)) (𝓝 ((((1 : ℝ) / 2) * (m : ℝ) * ((-1 : ℝ) + (m : ℝ))))) := by
  intros
  exfalso
  first
    | (simp_all; done)
    | (linarith; done)
    | (nlinarith; done)
    | (norm_num at *; done)
    | (tauto; done)
    | (aesop; done)
end Vac1

section Vac2
open Topology Filter
theorem vacuity_2 (m : ℕ) (hm_lo : 2 ≤ m) (hm_hi : m ≤ 9) :
    Filter.Tendsto (fun x : ℝ => (x ^ m - 1 - (m : ℝ) * (x - 1)) / (x - 1) ^ 2) (𝓝[≠] (1 : ℝ)) (𝓝 ((((1 : ℝ) / 2) * (m : ℝ) * ((-1 : ℝ) + (m : ℝ))))) := by
  intros
  exfalso
  first
    | (simp_all; done)
    | (linarith; done)
    | (nlinarith; done)
    | (norm_num at *; done)
    | (tauto; done)
    | (aesop; done)
end Vac2

