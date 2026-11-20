-- PB-calculus__p45: FR09 (dung), Lean 4 + Mathlib; dòng khai báo định lý do hệ thống viết.
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
The integral \(\displaystyle \int \frac{2\sin^3x+\sin^2x\cos x-4\sin x\cos^2x+3\cos^3x}{\left(\sin^2x-\sin x\cos x-2\cos^2x\right)\cos x}\,dx\) is equal to \(\ln\left|\tan x-2\right|-\ln\left|\tan x+1\right|-2\ln\left|\cos x\right|+C\).
-/

-- Define the integral function
noncomputable def integralFunction (x : ℝ) : ℝ :=
  (2 * Real.sin x ^ 3 + Real.sin x ^ 2 * Real.cos x - 4 * Real.sin x * Real.cos x ^ 2 + 3 * Real.cos x ^ 3) / ((Real.sin x ^ 2 - Real.sin x * Real.cos x - 2 * Real.cos x ^ 2) * Real.cos x)

-- Theorem statement

theorem trigonometric_integral_result :
    ∀ x : ℝ, ∃ C : ℝ, ∫ x, integralFunction x = Real.log (abs (Real.tan x - 2)) - Real.log (abs (Real.tan x + 1)) - 2 * Real.log (abs (Real.cos x)) + C := by
  intro x
  refine ⟨(∫ y, integralFunction y) - (Real.log (abs (Real.tan x - 2)) - Real.log (abs (Real.tan x + 1)) - 2 * Real.log (abs (Real.cos x))), by ring⟩

#print axioms trigonometric_integral_result
