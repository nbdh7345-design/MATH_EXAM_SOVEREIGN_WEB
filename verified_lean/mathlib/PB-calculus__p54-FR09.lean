-- PB-calculus__p54: FR09 (dung), Lean 4 + Mathlib; dòng khai báo định lý do hệ thống viết.
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
The function \(f(x) = x + 2\sin x\) attains its minimum at \( x = \frac{4\pi}{3} \) on the interval \(\left[\frac{\pi}{2}, 200\right]\).
-/

open Real

/-- The function f(x) = x + 2sin(x) -/
noncomputable def f (x : ℝ) : ℝ := x + 2 * sin x

lemma aux_sqrt3_ge : (17/10:ℝ) ≤ Real.sqrt 3 := by
  have h := Real.sq_sqrt (show (0:ℝ) ≤ 3 by norm_num)
  have h0 := Real.sqrt_nonneg 3
  nlinarith

lemma aux_cos_half (s : ℝ) : Real.cos s = 1 - 2 * Real.sin (s/2)^2 := by
  have h1 := Real.cos_two_mul (s/2)
  have h2 := Real.sin_sq_add_cos_sq (s/2)
  rw [show 2*(s/2) = s by ring] at h1
  linarith

lemma aux_L_small (s : ℝ) (h0 : 0 < s) (h1 : s ≤ 1) :
    s - Real.sin s ≤ Real.sqrt 3 * (1 - Real.cos s) := by
  have h3 := aux_sqrt3_ge
  have hsg := Real.sin_gt_sub_cube h0
  have hhalf := Real.sin_gt_sub_cube (x := s/2) (by linarith)
  have hs1 : s^2 ≤ 1 := by nlinarith [mul_nonneg h0.le (sub_nonneg.2 h1)]
  have hs2 : s^3 ≤ s^2 := by nlinarith [mul_nonneg (sq_nonneg s) (sub_nonneg.2 h1)]
  have hs3 : s^3 ≤ s := by nlinarith
  have hlb : 23/48*s ≤ s/2 - (s/2)^3/6 := by nlinarith
  have hu : 0 ≤ Real.sin (s/2) - 23/48*s := by linarith
  have hv : 0 ≤ Real.sin (s/2) + 23/48*s := by linarith
  have hS : (23/48*s)^2 ≤ Real.sin (s/2)^2 := by nlinarith [mul_nonneg hu hv]
  have hA : (17/10:ℝ) * Real.sin (s/2)^2 ≤ Real.sqrt 3 * Real.sin (s/2)^2 :=
    mul_le_mul_of_nonneg_right h3 (sq_nonneg _)
  rw [aux_cos_half s]
  nlinarith [sq_nonneg s]

lemma aux_L_mid (s : ℝ) (h0 : 1 ≤ s) (h1 : s ≤ 4/3) :
    s - Real.sin s ≤ Real.sqrt 3 * (1 - Real.cos s) := by
  have hpi := Real.pi_pos
  have hpi3 := Real.pi_gt_three
  have hpi4 := Real.pi_le_four
  have h3 := aux_sqrt3_ge
  have hpne : π ≠ 0 := hpi.ne'
  have hJ : 2/π * s ≤ Real.sin s := Real.mul_le_sin (by linarith) (by linarith)
  have hJ' : 2*s ≤ π * Real.sin s := by
    have h := mul_le_mul_of_nonneg_left hJ hpi.le
    have e : π * (2/π*s) = 2*s := by field_simp
    linarith
  have hsn : 0 ≤ Real.sin s := by nlinarith
  have hsl : s/2 ≤ Real.sin s := by nlinarith [mul_le_mul_of_nonneg_right hpi4 hsn]
  have hm : Real.sin (1/2) ≤ Real.sin (s/2) :=
    Real.sin_le_sin_of_le_of_le_pi_div_two (by linarith) (by linarith) (by linarith)
  have h2' : (15/32:ℝ) < Real.sin (1/2) := by
    have := Real.sin_gt_sub_cube (x := 1/2) (by norm_num)
    norm_num at this ⊢
    linarith
  have hhalf : 15/32 ≤ Real.sin (s/2) := by linarith
  have hS2 : (15/32)^2 ≤ Real.sin (s/2)^2 := by
    nlinarith [mul_nonneg (sub_nonneg.2 hhalf) (by linarith : (0:ℝ) ≤ Real.sin (s/2) + 15/32)]
  have hA : (17/10:ℝ) * Real.sin (s/2)^2 ≤ Real.sqrt 3 * Real.sin (s/2)^2 :=
    mul_le_mul_of_nonneg_right h3 (sq_nonneg _)
  rw [aux_cos_half s]
  nlinarith

lemma aux_L_all (s : ℝ) (h0 : 0 ≤ s) (h1 : s ≤ 4/3) :
    s - Real.sin s ≤ Real.sqrt 3 * (1 - Real.cos s) := by
  rcases h0.eq_or_lt with h | h
  · rw [← h]; simp
  · rcases le_total s 1 with h2 | h2
    · exact aux_L_small s h h2
    · exact aux_L_mid s h2 h1

theorem minimum_attainment_of_function :
    ∀ x ∈ Set.Icc (π / 2) 200, f (4 * π / 3) ≤ f x := by
  have hpi := Real.pi_pos
  have hpi3 := Real.pi_gt_three
  have hpi4 := Real.pi_le_four
  have h3 := aux_sqrt3_ge
  have hcs : Real.sin (4 * π / 3) = -(Real.sqrt 3 / 2) := by
    have e : 4 * π / 3 = π / 3 + π := by ring
    rw [e, Real.sin_add_pi, Real.sin_pi_div_three]
  have hcc : Real.cos (4 * π / 3) = -(1 / 2) := by
    have e : 4 * π / 3 = π / 3 + π := by ring
    rw [e, Real.cos_add_pi, Real.cos_pi_div_three]
  intro x hx
  obtain ⟨hx1, hx2⟩ := hx
  show 4 * π / 3 + 2 * Real.sin (4 * π / 3) ≤ x + 2 * Real.sin x
  rcases le_total (4 * π / 3) x with hxc | hxc
  · have hsin : Real.sin x = Real.sin (x - 4 * π / 3) * Real.cos (4 * π / 3) + Real.cos (x - 4 * π / 3) * Real.sin (4 * π / 3) := by
      rw [← Real.sin_add]; congr 1; ring
    rw [hsin, hcs, hcc]
    nlinarith [Real.sin_le (show (0:ℝ) ≤ x - 4 * π / 3 by linarith), mul_nonneg (Real.sqrt_nonneg 3) (sub_nonneg.2 (Real.cos_le_one (x - 4 * π / 3)))]
  · rcases le_total x π with hxπ | hxπ
    · have hJ : 2 / π * (π - x) ≤ Real.sin (π - x) := Real.mul_le_sin (by linarith) (by linarith)
      rw [Real.sin_pi_sub] at hJ
      have hpne : π ≠ 0 := hpi.ne'
      have hJ' : 2 * (π - x) ≤ π * Real.sin x := by
        have h := mul_le_mul_of_nonneg_left hJ hpi.le
        have e : π * (2 / π * (π - x)) = 2 * (π - x) := by field_simp
        linarith
      rw [hcs]
      have hsq : π / 3 ≤ Real.sqrt 3 := by linarith
      nlinarith [mul_nonneg (sub_nonneg.2 hxπ) (sub_nonneg.2 hpi4), mul_nonneg hpi.le (sub_nonneg.2 hsq), hJ', hpi]
    · have hs0 : 0 ≤ 4 * π / 3 - x := by linarith
      have hs1 : 4 * π / 3 - x ≤ 4 / 3 := by linarith
      have key := aux_L_all (4 * π / 3 - x) hs0 hs1
      have hsin : Real.sin x = Real.sin (4 * π / 3) * Real.cos (4 * π / 3 - x) - Real.cos (4 * π / 3) * Real.sin (4 * π / 3 - x) := by
        rw [← Real.sin_sub]; congr 1; ring
      rw [hsin, hcs, hcc]
      nlinarith [key, h3]

#print axioms minimum_attainment_of_function
