-- PB-real_analysis__p9: FR09 (dung), Lean 4 + Mathlib; dòng khai báo định lý do hệ thống viết.
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
Let $f: D \to \mathbb{R}$ be a function and $X \subseteq D$. If there exists a constant $M > 0$ such that $|f(x)| \leq M$ for all $x \in X$, then $f$ is bounded on $X$.
-/

variable {D : Type*} {f : D → ℝ} {X : Set D}

def BoundedOn (f : D → ℝ) (X : Set D) : Prop :=
  BddAbove (f '' X) ∧ BddBelow (f '' X)

theorem bounded_function_on_subset :
    (∃ M > 0, ∀ x ∈ X, |f x| ≤ M) → BoundedOn f X := by
  rintro ⟨M, hM, h⟩
  constructor
  · refine ⟨M, fun y hy => ?_⟩
    obtain ⟨x, hx, rfl⟩ := hy
    exact (abs_le.mp (h x hx)).2
  · refine ⟨-M, fun y hy => ?_⟩
    obtain ⟨x, hx, rfl⟩ := hy
    exact (abs_le.mp (h x hx)).1

#print axioms bounded_function_on_subset
