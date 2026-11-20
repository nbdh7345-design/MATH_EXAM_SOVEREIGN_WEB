-- PN-Rudin_exercise_5_2-STMT: 3 ứng viên formalize, biên dịch chung một file.
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

namespace Cand0



theorem exam_answer  :
    ∀ a b : ℝ, a < b → ∀ f : ℝ → ℝ, (∀ x ∈ Set.Ioo a b, DifferentiableAt ℝ f x ∧ 0 < deriv f x) → ∀ g : ℝ → ℝ, (∀ x ∈ Set.Ioo a b, g (f x) = x) → (∀ y ∈ f '' Set.Ioo a b, f (g y) = y) → StrictMonoOn f (Set.Ioo a b) ∧ ∀ x ∈ Set.Ioo a b, DifferentiableAt ℝ g (f x) ∧ deriv g (f x) = 1 / deriv f x := by
  sorry

end Cand0
#print axioms Cand0.exam_answer

namespace Cand1
open Set


theorem exam_answer  :
    ∀ f g : ℝ → ℝ, ∀ a b : ℝ, a < b → (∀ x ∈ Set.Ioo a b, DifferentiableAt ℝ f x ∧ 0 < deriv f x) → (∀ x ∈ Set.Ioo a b, g (f x) = x) → (∀ y ∈ f '' Set.Ioo a b, f (g y) = y) → StrictMonoOn f (Set.Ioo a b) ∧ ∀ x ∈ Set.Ioo a b, DifferentiableAt ℝ g (f x) ∧ deriv g (f x) = 1 / deriv f x := by
  sorry

end Cand1
#print axioms Cand1.exam_answer

namespace Cand2
open Topology


theorem exam_answer  :
    ∀ a b : ℝ, a < b → ∀ f : ℝ → ℝ, (∀ x ∈ Set.Ioo a b, DifferentiableAt ℝ f x ∧ 0 < deriv f x) → (StrictMonoOn f (Set.Ioo a b) ∧ ∀ g : ℝ → ℝ, (∀ x ∈ Set.Ioo a b, g (f x) = x) → ∀ x ∈ Set.Ioo a b, HasDerivWithinAt g (1 / deriv f x) (f '' Set.Ioo a b) (f x) ∧ derivWithin g (f '' Set.Ioo a b) (f x) = 1 / deriv f x) := by
  sorry

end Cand2
#print axioms Cand2.exam_answer

section Vac0

theorem vacuity_0  :
    ∀ a b : ℝ, a < b → ∀ f : ℝ → ℝ, (∀ x ∈ Set.Ioo a b, DifferentiableAt ℝ f x ∧ 0 < deriv f x) → ∀ g : ℝ → ℝ, (∀ x ∈ Set.Ioo a b, g (f x) = x) → (∀ y ∈ f '' Set.Ioo a b, f (g y) = y) → StrictMonoOn f (Set.Ioo a b) ∧ ∀ x ∈ Set.Ioo a b, DifferentiableAt ℝ g (f x) ∧ deriv g (f x) = 1 / deriv f x := by
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
open Set
theorem vacuity_1  :
    ∀ f g : ℝ → ℝ, ∀ a b : ℝ, a < b → (∀ x ∈ Set.Ioo a b, DifferentiableAt ℝ f x ∧ 0 < deriv f x) → (∀ x ∈ Set.Ioo a b, g (f x) = x) → (∀ y ∈ f '' Set.Ioo a b, f (g y) = y) → StrictMonoOn f (Set.Ioo a b) ∧ ∀ x ∈ Set.Ioo a b, DifferentiableAt ℝ g (f x) ∧ deriv g (f x) = 1 / deriv f x := by
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
open Topology
theorem vacuity_2  :
    ∀ a b : ℝ, a < b → ∀ f : ℝ → ℝ, (∀ x ∈ Set.Ioo a b, DifferentiableAt ℝ f x ∧ 0 < deriv f x) → (StrictMonoOn f (Set.Ioo a b) ∧ ∀ g : ℝ → ℝ, (∀ x ∈ Set.Ioo a b, g (f x) = x) → ∀ x ∈ Set.Ioo a b, HasDerivWithinAt g (1 / deriv f x) (f '' Set.Ioo a b) (f x) ∧ derivWithin g (f '' Set.Ioo a b) (f x) = 1 / deriv f x) := by
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

section Auto0

theorem auto_0  :
    ∀ a b : ℝ, a < b → ∀ f : ℝ → ℝ, (∀ x ∈ Set.Ioo a b, DifferentiableAt ℝ f x ∧ 0 < deriv f x) → ∀ g : ℝ → ℝ, (∀ x ∈ Set.Ioo a b, g (f x) = x) → (∀ y ∈ f '' Set.Ioo a b, f (g y) = y) → StrictMonoOn f (Set.Ioo a b) ∧ ∀ x ∈ Set.Ioo a b, DifferentiableAt ℝ g (f x) ∧ deriv g (f x) = 1 / deriv f x := by
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
open Set
theorem auto_1  :
    ∀ f g : ℝ → ℝ, ∀ a b : ℝ, a < b → (∀ x ∈ Set.Ioo a b, DifferentiableAt ℝ f x ∧ 0 < deriv f x) → (∀ x ∈ Set.Ioo a b, g (f x) = x) → (∀ y ∈ f '' Set.Ioo a b, f (g y) = y) → StrictMonoOn f (Set.Ioo a b) ∧ ∀ x ∈ Set.Ioo a b, DifferentiableAt ℝ g (f x) ∧ deriv g (f x) = 1 / deriv f x := by
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

section Auto2
open Topology
theorem auto_2  :
    ∀ a b : ℝ, a < b → ∀ f : ℝ → ℝ, (∀ x ∈ Set.Ioo a b, DifferentiableAt ℝ f x ∧ 0 < deriv f x) → (StrictMonoOn f (Set.Ioo a b) ∧ ∀ g : ℝ → ℝ, (∀ x ∈ Set.Ioo a b, g (f x) = x) → ∀ x ∈ Set.Ioo a b, HasDerivWithinAt g (1 / deriv f x) (f '' Set.Ioo a b) (f x) ∧ derivWithin g (f '' Set.Ioo a b) (f x) = 1 / deriv f x) := by
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
end Auto2

