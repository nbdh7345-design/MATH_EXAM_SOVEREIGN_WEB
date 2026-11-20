-- PN-Rudin_exercise_3_3: FR09 (dung), Lean 4 + Mathlib; dòng khai báo định lý do hệ thống viết.
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
noncomputable def f : ℕ → ℝ
| 0 => sqrt 2
| (n + 1) => sqrt (2 + sqrt (f n))

lemma sqrt_lip (x y : ℝ) (hx : 1 ≤ x) (hy : 1 ≤ y) :
    |Real.sqrt (2 + Real.sqrt x) - Real.sqrt (2 + Real.sqrt y)| ≤ |x - y| / 4 := by
  have ha := Real.sq_sqrt (show (0:ℝ) ≤ x by linarith)
  have hb := Real.sq_sqrt (show (0:ℝ) ≤ y by linarith)
  have ha0 := Real.sqrt_nonneg x
  have hb0 := Real.sqrt_nonneg y
  have ha1 : 1 ≤ Real.sqrt x := by nlinarith
  have hb1 : 1 ≤ Real.sqrt y := by nlinarith
  have hc := Real.sq_sqrt (show (0:ℝ) ≤ 2 + Real.sqrt x by linarith)
  have hd := Real.sq_sqrt (show (0:ℝ) ≤ 2 + Real.sqrt y by linarith)
  have hc0 := Real.sqrt_nonneg (2 + Real.sqrt x)
  have hd0 := Real.sqrt_nonneg (2 + Real.sqrt y)
  have hc1 : 1 ≤ Real.sqrt (2 + Real.sqrt x) := by nlinarith
  have hd1 : 1 ≤ Real.sqrt (2 + Real.sqrt y) := by nlinarith
  have hab : (Real.sqrt (2 + Real.sqrt x) - Real.sqrt (2 + Real.sqrt y)) * (Real.sqrt (2 + Real.sqrt x) + Real.sqrt (2 + Real.sqrt y)) = Real.sqrt x - Real.sqrt y := by
    linear_combination hc - hd
  have hab2 : (Real.sqrt x - Real.sqrt y) * (Real.sqrt x + Real.sqrt y) = x - y := by
    linear_combination ha - hb
  have h1 : |Real.sqrt (2 + Real.sqrt x) - Real.sqrt (2 + Real.sqrt y)| * (Real.sqrt (2 + Real.sqrt x) + Real.sqrt (2 + Real.sqrt y)) = |Real.sqrt x - Real.sqrt y| := by
    rw [← hab, abs_mul, abs_of_nonneg (by linarith : (0:ℝ) ≤ Real.sqrt (2 + Real.sqrt x) + Real.sqrt (2 + Real.sqrt y))]
  have h2 : |Real.sqrt x - Real.sqrt y| * (Real.sqrt x + Real.sqrt y) = |x - y| := by
    rw [← hab2, abs_mul, abs_of_nonneg (by linarith : (0:ℝ) ≤ Real.sqrt x + Real.sqrt y)]
  have h3 : 2 * |Real.sqrt (2 + Real.sqrt x) - Real.sqrt (2 + Real.sqrt y)| ≤ |Real.sqrt x - Real.sqrt y| := by
    nlinarith [mul_nonneg (abs_nonneg (Real.sqrt (2 + Real.sqrt x) - Real.sqrt (2 + Real.sqrt y))) (show (0:ℝ) ≤ Real.sqrt (2 + Real.sqrt x) + Real.sqrt (2 + Real.sqrt y) - 2 by linarith)]
  have h4 : 2 * |Real.sqrt x - Real.sqrt y| ≤ |x - y| := by
    nlinarith [mul_nonneg (abs_nonneg (Real.sqrt x - Real.sqrt y)) (show (0:ℝ) ≤ Real.sqrt x + Real.sqrt y - 2 by linarith)]
  linarith

lemma f_succ (n : ℕ) : f (n+1) = Real.sqrt (2 + Real.sqrt (f n)) := by
  first
  | rfl
  | simp only [f]

lemma f_bounds (n : ℕ) : 1 ≤ f n ∧ f n < 2 := by
  induction n with
  | zero =>
    have h0 : f 0 = Real.sqrt 2 := by
      first
      | rfl
      | simp [f]
    rw [h0]
    have h1 := Real.sq_sqrt (show (0:ℝ) ≤ 2 by norm_num)
    have h2 := Real.sqrt_nonneg 2
    constructor
    · nlinarith
    · nlinarith
  | succ k ih =>
    obtain ⟨h1, h2⟩ := ih
    rw [f_succ]
    have hs : 0 ≤ f k := by linarith
    have hsq := Real.sq_sqrt hs
    have hsq0 := Real.sqrt_nonneg (f k)
    have hlt : Real.sqrt (f k) < 2 := by nlinarith
    have hc := Real.sq_sqrt (show (0:ℝ) ≤ 2 + Real.sqrt (f k) by linarith)
    have hc0 := Real.sqrt_nonneg (2 + Real.sqrt (f k))
    constructor
    · nlinarith
    · nlinarith

lemma f_step (n : ℕ) : |f (n+1+1) - f (n+1)| ≤ |f (n+1) - f n| / 4 := by
  have e1 : f (n+1+1) = Real.sqrt (2 + Real.sqrt (f (n+1))) := f_succ (n+1)
  have e2 : f (n+1) = Real.sqrt (2 + Real.sqrt (f n)) := f_succ n
  have key := sqrt_lip (f (n+1)) (f n) (f_bounds (n+1)).1 (f_bounds n).1
  rw [← e1, ← e2] at key
  exact key

lemma f_geom (n : ℕ) : |f (n+1) - f n| ≤ (1/4 : ℝ)^n * |f 1 - f 0| := by
  induction n with
  | zero => simp
  | succ k ih =>
    have hs := f_step k
    calc |f (k+1+1) - f (k+1)| ≤ |f (k+1) - f k| / 4 := hs
      _ ≤ ((1/4 : ℝ)^k * |f 1 - f 0|) / 4 := by linarith
      _ = (1/4 : ℝ)^(k+1) * |f 1 - f 0| := by ring

lemma f_cauchy : CauchySeq f := by
  have hbound : ∀ n : ℕ, dist (f n) (f (n+1)) ≤ |f 1 - f 0| * (1/4 : ℝ)^n := by
    intro n
    rw [Real.dist_eq, abs_sub_comm, mul_comm]
    exact f_geom n
  first
  | exact cauchySeq_of_le_geometric (1/4 : ℝ) (|f 1 - f 0|) (by norm_num) hbound
  | exact cauchySeq_of_le_geometric (|f 1 - f 0|) (1/4 : ℝ) (by norm_num) hbound
  | exact cauchySeq_of_le_geometric (by norm_num) hbound

theorem exercise_3_3 :
    ∃ (x : ℝ), Tendsto f atTop (𝓝 x) ∧ ∀ n, f n < 2 := by
  obtain ⟨x, hx⟩ := cauchySeq_tendsto_of_complete f_cauchy
  exact ⟨x, hx, fun n => (f_bounds n).2⟩

#print axioms exercise_3_3
