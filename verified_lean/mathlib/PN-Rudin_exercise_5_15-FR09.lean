-- PN-Rudin_exercise_5_15: FR09 (dung), Lean 4 + Mathlib; dòng khai báo định lý do hệ thống viết.
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


open Topology Filter Real Complex TopologicalSpace Finset
open scoped BigOperators

-- Không có. Định lý như phát biểu là sai (phản ví dụ f = id, a = 0: M0 = 0 do sSup của tập không bị chặn trong ℝ bằng 0, M1 = 1, M2 = 0, nên 1 ≤ 0 sai).

theorem exercise_5_15 {f : ℝ → ℝ} (a : ℝ) (M0 : ℝ) (M1 : ℝ) (M2 : ℝ) (hf' : DifferentiableOn ℝ f (Set.Ioi a)) (hf'' : DifferentiableOn ℝ (deriv f) (Set.Ioi a)) (hM0 : M0 = sSup {(|f x|) | x ∈ (Set.Ioi a)}) (hM1 : M1 = sSup {(|deriv f x|) | x ∈ (Set.Ioi a)}) (hM2 : M2 = sSup {(|deriv (deriv f) x|) | x ∈ (Set.Ioi a)}) :
    (M1 ^ 2) ≤ 4 * M0 * M2 := by
  -- Không thể chứng minh: phát biểu sai (thiếu giả thiết BddAbove cho M0, M2).
  -- Phản ví dụ: f = id, a = 0 cho M0 = 0 (junk sSup), M1 = 1, M2 = 0.
  skip

#print axioms exercise_5_15
