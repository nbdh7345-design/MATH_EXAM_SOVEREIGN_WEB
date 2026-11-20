-- PB-calculus__p55: FR09 (dung), Lean 4 + Mathlib; dòng khai báo định lý do hệ thống viết.
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
If \(f(x)=2^x\) and \(g(x)=5\cdot x-6\), then the function \(h(x)=f(g(x))=2^{5x-6}\) results in \(h(3)=2^{5\cdot 3-6}=2^{9}=512\), and function \(m(x)=g(f(x))=5\cdot 2^x-6\) results in \(m(3)=5\cdot 2^3-6=5\cdot 8-6=34\).
-/

/-- The exponential function with base a, f(x) = a^x -/
noncomputable def f (a : ℝ) (x : ℝ) : ℝ := a^x

/-- The linear function g(x) = mx + b -/
noncomputable def g (m b : ℝ) (x : ℝ) : ℝ := m * x + b

/-- The composition h(x) = f(g(x)) = a^(mx + b) -/
noncomputable def h (a m b : ℝ) (x : ℝ) : ℝ := f a (g m b x)

/-- The composition m(x) = g(f(x)) = m * a^x + b -/
noncomputable def m_comp (a m b : ℝ) (x : ℝ) : ℝ := g m b (f a x)
/-- Specific example where a = 2, m = 5, b = -6, and x = 3 -/

theorem specific_example :
    h 2 5 (-6) 3 = 512 ∧ m_comp 2 5 (-6) 3 = 34 := by
  constructor
  · simp only [h, f, g]
    rw [show (5:ℝ) * 3 + -6 = ((9:ℕ):ℝ) by norm_num, Real.rpow_natCast]
    norm_num
  · simp only [m_comp, g, f]
    rw [show (3:ℝ) = ((3:ℕ):ℝ) by norm_num, Real.rpow_natCast]
    norm_num

#print axioms specific_example
