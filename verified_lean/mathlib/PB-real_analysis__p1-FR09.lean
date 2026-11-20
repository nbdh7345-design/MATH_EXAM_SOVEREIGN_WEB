-- PB-real_analysis__p1: FR09 (dung), Lean 4 + Mathlib; dòng khai báo định lý do hệ thống viết.
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
Let $f$ be a function defined by $f(x)=\frac{\sqrt{-1-x}}{\log _{\frac{1}{2}}(x)}$. Then the domain of $f$ is the empty set, i.e., $\text{Dom}(f) = \emptyset$.
-/

open Real Set

/-- The function f(x) = √(-1-x) / log₁/₂(x) -/
noncomputable def f (x : ℝ) : ℝ :=
sqrt (-1 - x) / logb (1/2) x

/-- The domain of f is empty -/
def Dom : Set ℝ := {x | -1 - x ≥ 0 ∧ x > 0}

theorem f_domain_empty :
    Dom = ∅ := by
  ext x
  constructor
  · intro h
    obtain ⟨h1, h2⟩ := h
    exfalso
    linarith
  · intro h
    exact h.elim

#print axioms f_domain_empty
