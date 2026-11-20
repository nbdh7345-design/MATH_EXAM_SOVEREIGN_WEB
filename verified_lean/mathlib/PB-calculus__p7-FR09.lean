-- PB-calculus__p7: FR09 (dung), Lean 4 + Mathlib; dòng khai báo định lý do hệ thống viết.
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
Let \[F(x)=\cos^2 x-\sin^2 x,\] \[G(x)=2\cos^2x,\] \[H(x)=2\sin^2x,\] \[K(x)=\cos (2x).\] Which of the previously defined functions are anti-derivatives of the function \[\varphi(x)=-4\sin x\cdot\cos x.\] \begin{itemize} \item \textbf{(A)} \(F\) only \item \textbf{(B)} \(F\) and \(K\) only \item \textbf{(C)} \(F\), \(G\), and \(K\) only \item \textbf{(D)} \(H\) and \(K\) only \item \textbf{(E)} \(H\) only \end{itemize}
-/

open Real

-- Define the functions
noncomputable def F (x : ℝ) : ℝ := cos x ^ 2 - sin x ^ 2

noncomputable def G (x : ℝ) : ℝ := 2 * cos x ^ 2

noncomputable def H (x : ℝ) : ℝ := 2 * sin x ^ 2

noncomputable def K (x : ℝ) : ℝ := cos (2 * x)

-- Define the function φ
noncomputable def φ (x : ℝ) : ℝ := -4 * sin x * cos x

-- Theorem statement

theorem F_deriv_aux (x : ℝ) : deriv F x = φ x := by
  have h : HasDerivAt F (2 * cos x ^ 1 * (-sin x) - 2 * sin x ^ 1 * cos x) x := by
    unfold F
    exact ((hasDerivAt_cos x).pow 2).sub ((hasDerivAt_sin x).pow 2)
  rw [h.deriv]; unfold φ; ring

theorem K_deriv_aux (x : ℝ) : deriv K x = φ x := by
  have h : HasDerivAt K (-sin (2 * x) * 2) x := by
    unfold K
    have h2 : HasDerivAt (fun y : ℝ => 2 * y) 2 x := by
      simpa using (hasDerivAt_id x).const_mul (2:ℝ)
    exact (hasDerivAt_cos (2 * x)).comp x h2
  rw [h.deriv]; unfold φ; rw [Real.sin_two_mul]; ring

theorem formal_statement :
    ∀ x : ℝ, (deriv F x = φ x) ∧ (deriv K x = φ x) ∧ (deriv G x ≠ φ x) ∧ (deriv H x ≠ φ x) := by
  intro x
  refine ⟨F_deriv_aux x, K_deriv_aux x, ?_, ?_⟩
  · -- FALSE: deriv G x = φ x for all x
    have h : HasDerivAt G (2 * (2 * cos x ^ 1 * (-sin x))) x := by
      unfold G
      exact ((hasDerivAt_cos x).pow 2).const_mul 2
    rw [h.deriv]; unfold φ
    intro h'
    nlinarith [h']
  · -- FALSE at x = 0
    have h : HasDerivAt H (2 * (2 * sin x ^ 1 * cos x)) x := by
      unfold H
      exact ((hasDerivAt_sin x).pow 2).const_mul 2
    rw [h.deriv]; unfold φ
    intro h'
    nlinarith [h']

#print axioms formal_statement
