-- PN-Rudin_exercise_5_15-STMT: 1 ứng viên formalize, biên dịch chung một file.
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

namespace Cand2



theorem exam_answer  :
    ∀ a : ℝ, ∀ f : ℝ → ℝ, (ContDiffOn ℝ 1 f (Set.Ioi a) ∧ ∀ x : ℝ, a < x → DifferentiableAt ℝ f x ∧ DifferentiableAt ℝ (deriv f) x) → ∀ M0 M1 M2 : ℝ, IsLUB ((fun x : ℝ => |f x|) '' Set.Ioi a) M0 → IsLUB ((fun x : ℝ => |deriv f x|) '' Set.Ioi a) M1 → IsLUB ((fun x : ℝ => |iteratedDeriv 2 f x|) '' Set.Ioi a) M2 → M1 ^ 2 ≤ 4 * M0 * M2 := by
  sorry

end Cand2
#print axioms Cand2.exam_answer

section Vac2

theorem vacuity_2  :
    ∀ a : ℝ, ∀ f : ℝ → ℝ, (ContDiffOn ℝ 1 f (Set.Ioi a) ∧ ∀ x : ℝ, a < x → DifferentiableAt ℝ f x ∧ DifferentiableAt ℝ (deriv f) x) → ∀ M0 M1 M2 : ℝ, IsLUB ((fun x : ℝ => |f x|) '' Set.Ioi a) M0 → IsLUB ((fun x : ℝ => |deriv f x|) '' Set.Ioi a) M1 → IsLUB ((fun x : ℝ => |iteratedDeriv 2 f x|) '' Set.Ioi a) M2 → M1 ^ 2 ≤ 4 * M0 * M2 := by
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

section Auto2

theorem auto_2  :
    ∀ a : ℝ, ∀ f : ℝ → ℝ, (ContDiffOn ℝ 1 f (Set.Ioi a) ∧ ∀ x : ℝ, a < x → DifferentiableAt ℝ f x ∧ DifferentiableAt ℝ (deriv f) x) → ∀ M0 M1 M2 : ℝ, IsLUB ((fun x : ℝ => |f x|) '' Set.Ioi a) M0 → IsLUB ((fun x : ℝ => |deriv f x|) '' Set.Ioi a) M1 → IsLUB ((fun x : ℝ => |iteratedDeriv 2 f x|) '' Set.Ioi a) M2 → M1 ^ 2 ≤ 4 * M0 * M2 := by
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

