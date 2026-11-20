-- CORE-SELFTEST-STMT: 2 ứng viên formalize, biên dịch chung một file.
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
open Filter Topology


theorem exam_answer (m : ℕ) (hm_lo : 2 ≤ m) (hm_hi : m ≤ 9) :
    (m:ℝ) * 2 = 2 * ((m : ℝ)) := by
  sorry

end Cand0
#print axioms Cand0.exam_answer

namespace Cand1
open Filter Topology


theorem exam_answer (m : ℕ) (hm_lo : 2 ≤ m) (hm_hi : m ≤ 9) :
    Tendsto (fun x : ℝ => Real.sin ((m:ℝ) * x) / x) (𝓝[≠] 0) (𝓝 ((m : ℝ))) := by
  sorry

end Cand1
#print axioms Cand1.exam_answer

section Vac0
open Filter Topology
theorem vacuity_0 (m : ℕ) (hm_lo : 2 ≤ m) (hm_hi : m ≤ 9) :
    (m:ℝ) * 2 = 2 * ((m : ℝ)) := by
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
open Filter Topology
theorem vacuity_1 (m : ℕ) (hm_lo : 2 ≤ m) (hm_hi : m ≤ 9) :
    Tendsto (fun x : ℝ => Real.sin ((m:ℝ) * x) / x) (𝓝[≠] 0) (𝓝 ((m : ℝ))) := by
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

section Auto0
open Filter Topology
theorem auto_0 (m : ℕ) (hm_lo : 2 ≤ m) (hm_hi : m ≤ 9) :
    (m:ℝ) * 2 = 2 * ((m : ℝ)) := by
  first
    | (norm_num; done)
    | (simp; done)
    | (field_simp; done)
    | (ring_nf; done)
    | (positivity; done)
    | (fun_prop; done)
    | (linarith; done)
    | (nlinarith; done)
    | (aesop; done)
    | (constructor <;> first | fun_prop | (norm_num; done) | (simp; done); done)
end Auto0

section Auto1
open Filter Topology
theorem auto_1 (m : ℕ) (hm_lo : 2 ≤ m) (hm_hi : m ≤ 9) :
    Tendsto (fun x : ℝ => Real.sin ((m:ℝ) * x) / x) (𝓝[≠] 0) (𝓝 ((m : ℝ))) := by
  first
    | (norm_num; done)
    | (simp; done)
    | (field_simp; done)
    | (ring_nf; done)
    | (positivity; done)
    | (fun_prop; done)
    | (linarith; done)
    | (nlinarith; done)
    | (aesop; done)
    | (constructor <;> first | fun_prop | (norm_num; done) | (simp; done); done)
end Auto1

