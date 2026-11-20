-- PN-Rudin_exercise_4_8b-STMT: 2 ứng viên formalize, biên dịch chung một file.
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

namespace Cand3



theorem exam_answer  :
    ∀ E : Set ℝ, Bornology.IsBounded E → ∃ f : ℝ → ℝ, UniformContinuousOn f E ∧ ¬ Bornology.IsBounded (f '' E) := by
  sorry

end Cand3
#print axioms Cand3.exam_answer

namespace Cand4
open Topology Filter


theorem exam_answer  :
    ∀ E : Set ℝ, Bornology.IsBounded E → ∃ f : ℝ → ℝ, UniformContinuousOn f E ∧ ¬ ∃ C : ℝ, ∀ x ∈ E, |f x| ≤ C := by
  sorry

end Cand4
#print axioms Cand4.exam_answer

section Vac3

theorem vacuity_3  :
    ∀ E : Set ℝ, Bornology.IsBounded E → ∃ f : ℝ → ℝ, UniformContinuousOn f E ∧ ¬ Bornology.IsBounded (f '' E) := by
  intros
  exfalso
  first
    | (simp_all; done)
    | (linarith; done)
    | (nlinarith; done)
    | (norm_num at *; done)
    | (tauto; done)
    | (aesop; done)
end Vac3

section Vac4
open Topology Filter
theorem vacuity_4  :
    ∀ E : Set ℝ, Bornology.IsBounded E → ∃ f : ℝ → ℝ, UniformContinuousOn f E ∧ ¬ ∃ C : ℝ, ∀ x ∈ E, |f x| ≤ C := by
  intros
  exfalso
  first
    | (simp_all; done)
    | (linarith; done)
    | (nlinarith; done)
    | (norm_num at *; done)
    | (tauto; done)
    | (aesop; done)
end Vac4

section Auto3

theorem auto_3  :
    ∀ E : Set ℝ, Bornology.IsBounded E → ∃ f : ℝ → ℝ, UniformContinuousOn f E ∧ ¬ Bornology.IsBounded (f '' E) := by
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
end Auto3

section Auto4
open Topology Filter
theorem auto_4  :
    ∀ E : Set ℝ, Bornology.IsBounded E → ∃ f : ℝ → ℝ, UniformContinuousOn f E ∧ ¬ ∃ C : ℝ, ∀ x ∈ E, |f x| ≤ C := by
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
end Auto4

