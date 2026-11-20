-- PB-calculus__p14: FR09 (dung), Lean 4 + Mathlib; dòng khai báo định lý do hệ thống viết.
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
The value of the integral \[\iiint_D e^{x^2+y^2}\,dV\] where \(D\) is the the region
in bounded by the planes \(y=0\), \(z=0\), \(y=x\),
and the paraboloid \(z=4-x^2-y^2\) is \[\frac{\left(e^4-5\right)\pi}8\].
-/

open MeasureTheory

variable {D : Type} [MeasurableSpace D] [MeasureSpace D]

-- Define the set D as a variable
variable (D : Set (Fin 3 → ℝ))

theorem integral_value_over_region (D : Set (Fin 3 → ℝ)) (hD : D = {p : Fin 3 → ℝ | p 2 ≥ 0 ∧ p 3 ≥ 0 ∧ p 2 ≤ p 1 ∧ p 3 ≤ 4 - p 1^2 - p 2^2}) :
    let integrand := fun p : Fin 3 → ℝ => Real.exp (p 1^2 + p 2^2)
  ∫ p in D, integrand p = (Real.exp 4 - 5) * π / 8 := by
  intro integrand
    show ∫ p in D, Real.exp (p 1 ^ 2 + p 2 ^ 2) = (Real.exp 4 - 5) * π / 8
    exact polar_int_aux

#print axioms integral_value_over_region
