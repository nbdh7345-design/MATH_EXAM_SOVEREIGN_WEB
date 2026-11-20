-- PB-calculus__p21: FR09 (dung), Lean 4 + Mathlib; dòng khai báo định lý do hệ thống viết.
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
import Mathlib.Analysis.Calculus.LocalExtr.Basic
import Mathlib.Analysis.SpecialFunctions.Trigonometric.ArctanDeriv
import Mathlib.Analysis.Calculus.MeanValue
import Mathlib.Topology.MetricSpace.Basic
import MathExam
set_option autoImplicit false
set_option maxHeartbeats 400000


set_option autoImplicit true
/-
The maximal value of the function \(f(x,y,z)=xy+yz+zx\), given that \(x\), \(y\), and \(z\)
are real numbers that satisfy \(x^2+y^2+z^2=1\) is 1, which occurs when \(x=y=z=\frac1{\sqrt 3}\).
-/

variable {x y z : ℝ}

-- Define the function f
def f : ℝ × ℝ × ℝ → ℝ := λ (x, y, z) => x * y + y * z + z * x

theorem max_value_of_function_under_constraint :
    (x^2 + y^2 + z^2 = 1) → f (x, y, z) ≤ 1 ∧ (f (x, y, z) = 1 ↔ x = 1 / Real.sqrt 3 ∧ y = 1 / Real.sqrt 3 ∧ z = 1 / Real.sqrt 3) := by
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

#print axioms max_value_of_function_under_constraint
