-- PN-Rudin_exercise_4_19-STMT: 3 ứng viên formalize, biên dịch chung một file.
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
open Topology Set


theorem exam_answer  :
    ∀ f : ℝ → ℝ, (∀ a b c : ℝ, f a < c → c < f b → ∃ x ∈ Set.uIcc a b, f x = c) → (∀ r : ℚ, IsClosed {x : ℝ | f x = (r : ℝ)}) → Continuous f := by
  sorry

end Cand0
#print axioms Cand0.exam_answer

namespace Cand1
open Topology


theorem exam_answer  :
    ∀ f : ℝ → ℝ, (∀ a b c : ℝ, f a < c → c < f b → ∃ x ∈ Set.uIcc a b, f x = c) → (∀ r : ℚ, IsClosed {x : ℝ | f x = (r : ℝ)}) → Continuous f := by
  sorry

end Cand1
#print axioms Cand1.exam_answer

namespace Cand2



theorem exam_answer  :
    ∀ f : ℝ → ℝ, (∀ a b c : ℝ, f a < c → c < f b → ∃ x ∈ Set.uIcc a b, f x = c) → (∀ r : ℚ, IsClosed {x : ℝ | f x = (r : ℝ)}) → Continuous f := by
  sorry

end Cand2
#print axioms Cand2.exam_answer

section Vac0
open Topology Set
theorem vacuity_0  :
    ∀ f : ℝ → ℝ, (∀ a b c : ℝ, f a < c → c < f b → ∃ x ∈ Set.uIcc a b, f x = c) → (∀ r : ℚ, IsClosed {x : ℝ | f x = (r : ℝ)}) → Continuous f := by
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
open Topology
theorem vacuity_1  :
    ∀ f : ℝ → ℝ, (∀ a b c : ℝ, f a < c → c < f b → ∃ x ∈ Set.uIcc a b, f x = c) → (∀ r : ℚ, IsClosed {x : ℝ | f x = (r : ℝ)}) → Continuous f := by
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

theorem vacuity_2  :
    ∀ f : ℝ → ℝ, (∀ a b c : ℝ, f a < c → c < f b → ∃ x ∈ Set.uIcc a b, f x = c) → (∀ r : ℚ, IsClosed {x : ℝ | f x = (r : ℝ)}) → Continuous f := by
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
open Topology Set
theorem auto_0  :
    ∀ f : ℝ → ℝ, (∀ a b c : ℝ, f a < c → c < f b → ∃ x ∈ Set.uIcc a b, f x = c) → (∀ r : ℚ, IsClosed {x : ℝ | f x = (r : ℝ)}) → Continuous f := by
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
open Topology
theorem auto_1  :
    ∀ f : ℝ → ℝ, (∀ a b c : ℝ, f a < c → c < f b → ∃ x ∈ Set.uIcc a b, f x = c) → (∀ r : ℚ, IsClosed {x : ℝ | f x = (r : ℝ)}) → Continuous f := by
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

theorem auto_2  :
    ∀ f : ℝ → ℝ, (∀ a b c : ℝ, f a < c → c < f b → ∃ x ∈ Set.uIcc a b, f x = c) → (∀ r : ℚ, IsClosed {x : ℝ | f x = (r : ℝ)}) → Continuous f := by
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

