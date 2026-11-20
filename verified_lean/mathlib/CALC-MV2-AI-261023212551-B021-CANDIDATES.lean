-- CALC-MV2-AI-261023212551-B021: 3 ứng viên formalize, biên dịch chung một file.
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
import MathExam
set_option autoImplicit false

namespace Cand0
open Topology Filter


theorem exam_answer (m : ℕ) (hm_lo : 1 ≤ m) (hm_hi : m ≤ 6) :
    ∀ y : ℝ → ℝ, (∀ᶠ x in 𝓝 (m:ℝ), DifferentiableAt ℝ y x) → DifferentiableAt ℝ (deriv y) (m:ℝ) → (∀ᶠ x in 𝓝 (m:ℝ), x^2 + x * y x + (y x)^2 = 3 * (m:ℝ)^2) → y (m:ℝ) = (m:ℝ) → deriv (deriv y) (m:ℝ) = ((((-2 : ℝ) / 3) * (((m : ℝ) ^ (1 : ℕ))⁻¹))) := by
  intro y hd hd2 heq hy
  have hm : (0:ℝ) < (m:ℝ) := Nat.cast_pos.mpr hm_lo
  have key : ∀ᶠ x in 𝓝 (m:ℝ), (2*x + y x) + (x + 2 * y x) * deriv y x = 0 := by
    filter_upwards [hd.eventually_nhds, heq.eventually_nhds] with x hx hex
    have hyx : DifferentiableAt ℝ y x := hx.self_of_nhds
    have hy' := hyx.hasDerivAt
    have hder : HasDerivAt (fun x : ℝ => x * x + x * y x + y x * y x)
        ((1 * x + x * 1) + (1 * y x + x * deriv y x) + (deriv y x * y x + y x * deriv y x)) x :=
      (((hasDerivAt_id' x).mul (hasDerivAt_id' x)).add ((hasDerivAt_id' x).mul hy')).add (hy'.mul hy')
    have hg : HasDerivAt (fun _ : ℝ => 3 * (m:ℝ)^2)
        ((1 * x + x * 1) + (1 * y x + x * deriv y x) + (deriv y x * y x + y x * deriv y x)) x :=
      hder.congr_of_eventuallyEq (hex.mono fun z hz => by
        show 3 * (m:ℝ)^2 = z * z + z * y z + y z * y z
        linear_combination (-1 : ℝ) * hz)
    have := hg.unique (hasDerivAt_const x _)
    linear_combination this
  have h0 := key.self_of_nhds
  rw [hy] at h0
  have h3 : ((m:ℝ) * 3) * (1 + deriv y (m:ℝ)) = 0 := by linear_combination h0
  have h1 : deriv y (m:ℝ) = -1 := by
    rcases mul_eq_zero.mp h3 with h | h
    · exfalso; linarith
    · linarith
  have hy_m : HasDerivAt y (deriv y (m:ℝ)) (m:ℝ) := (hd.self_of_nhds).hasDerivAt
  have hdy := hd2.hasDerivAt
  have p1 : HasDerivAt (fun x => 2*x + y x) (2*1 + deriv y (m:ℝ)) (m:ℝ) :=
    ((hasDerivAt_id' (m:ℝ)).const_mul 2).add hy_m
  have p2 : HasDerivAt (fun x => x + 2 * y x) (1 + 2 * deriv y (m:ℝ)) (m:ℝ) :=
    (hasDerivAt_id' (m:ℝ)).add (hy_m.const_mul 2)
  have H : HasDerivAt (fun x => (2*x + y x) + (x + 2 * y x) * deriv y x)
      ((2*1 + deriv y (m:ℝ)) + ((1 + 2 * deriv y (m:ℝ)) * deriv y (m:ℝ) + ((m:ℝ) + 2 * y (m:ℝ)) * deriv (deriv y) (m:ℝ))) (m:ℝ) :=
    p1.add (p2.mul hdy)
  have H0 := H.congr_of_eventuallyEq (f₁ := fun _ => (0:ℝ)) (key.mono fun z hz => hz.symm)
  have this := (hasDerivAt_const (m:ℝ) (0:ℝ)).unique H0
  rw [hy, h1] at this
  have h4 : 2 + 3 * (m:ℝ) * deriv (deriv y) (m:ℝ) = 0 := by linear_combination (-1 : ℝ) * this
  rw [eq_div_iff (by positivity)]
  linear_combination h4

end Cand0
#print axioms Cand0.exam_answer

namespace Cand1
open Topology Filter


theorem exam_answer (m : ℕ) (hm_lo : 1 ≤ m) (hm_hi : m ≤ 6) :
    ∀ y : ℝ → ℝ, (∀ᶠ x in 𝓝 (m:ℝ), x^2 + x * y x + (y x)^2 = 3 * (m:ℝ)^2) → y (m:ℝ) = (m:ℝ) → (∀ᶠ x in 𝓝 (m:ℝ), DifferentiableAt ℝ y x) → DifferentiableAt ℝ (deriv y) (m:ℝ) → deriv (deriv y) (m:ℝ) = ((((-2 : ℝ) / 3) * (((m : ℝ) ^ (1 : ℕ))⁻¹))) := by
  intro y heq hd hd2 
  have hmr : (0:ℝ) < (m:ℝ) := Nat.cast_pos.mpr hm_lo
  have hm0 : (m:ℝ) ≠ 0 := hmr.ne'
  sorry_placeholder

end Cand1
#print axioms Cand1.exam_answer

namespace Cand2
open Topology Filter


theorem exam_answer (m : ℕ) (hm_lo : 1 ≤ m) (hm_hi : m ≤ 6) :
    ∀ y : ℝ → ℝ, y (m:ℝ) = (m:ℝ) →
    (∀ᶠ x in 𝓝 (m:ℝ), x^2 + x * y x + (y x)^2 = 3 * (m:ℝ)^2) →
    (∀ᶠ x in 𝓝 (m:ℝ), DifferentiableAt ℝ y x) →
    DifferentiableAt ℝ (deriv y) (m:ℝ) →
    deriv (deriv y) (m:ℝ) = ((((-2 : ℝ) / 3) * (((m : ℝ) ^ (1 : ℕ))⁻¹))) := by
  intro y hy0 heq hdiff hdd
  have hm1' : (1:ℝ) ≤ (m:ℝ) := by exact_mod_cast hm_lo
  have hne : (3 * (m:ℝ)) ≠ 0 := by
    apply ne_of_gt
    linarith
  have key : ∀ᶠ x in 𝓝 (m:ℝ), (2*x + y x) + (x + 2 * y x) * deriv y x = 0 := by
    filter_upwards [hdiff, heq.eventually_nhds] with x hx hx2
    have h1 : HasDerivAt y (deriv y x) x := hx.hasDerivAt
    have h2 : HasDerivAt (fun t : ℝ => t^2 + t * y t + (y t)^2)
        (2*x + (y x + x * deriv y x) + 2 * y x * deriv y x) x := by
      have h := (((hasDerivAt_id' x).mul (hasDerivAt_id' x)).add ((hasDerivAt_id' x).mul h1)).add (h1.mul h1)
      have e : (fun t : ℝ => t^2 + t * y t + (y t)^2) = fun t => t*t + t * y t + y t * y t := by
        funext t; ring
      rw [e]
      exact h.congr_deriv (by ring)
    have h3 : HasDerivAt (fun t : ℝ => t^2 + t * y t + (y t)^2) 0 x :=
      (hasDerivAt_const x (3 * (m:ℝ)^2)).congr_of_eventuallyEq hx2
    have h4 := h2.unique h3
    linarith
  have k0 := key.self_of_nhds
  rw [hy0] at k0
  have hm1 : deriv y (m:ℝ) = -1 := by
    have h : (3 * (m:ℝ)) * (1 + deriv y (m:ℝ)) = 0 := by linear_combination k0
    rcases mul_eq_zero.mp h with h | h
    · exact absurd h hne
    · linarith
  have hy' : HasDerivAt y (deriv y (m:ℝ)) (m:ℝ) := hdiff.self_of_nhds.hasDerivAt
  have hd : HasDerivAt (deriv y) (deriv (deriv y) (m:ℝ)) (m:ℝ) := hdd.hasDerivAt
  have p1 : HasDerivAt (fun t : ℝ => 2*t + y t) _ (m:ℝ) :=
    ((hasDerivAt_id' (m:ℝ)).const_mul 2).add hy'
  have p2 : HasDerivAt (fun t : ℝ => t + 2 * y t) _ (m:ℝ) :=
    (hasDerivAt_id' (m:ℝ)).add (hy'.const_mul 2)
  have p3 := p1.add (p2.mul hd)
  have hz : HasDerivAt (fun t : ℝ => (2*t + y t) + (t + 2 * y t) * deriv y t) 0 (m:ℝ) :=
    (hasDerivAt_const (m:ℝ) (0:ℝ)).congr_of_eventuallyEq key
  have h5 := p3.unique hz
  simp only [mul_one] at h5
  rw [hm1, hy0] at h5
  have h3 : 3 * (m:ℝ) * deriv (deriv y) (m:ℝ) = -2 := by
    linear_combination h5
  rw [eq_div_iff hne]
  linarith [h3]

end Cand2
#print axioms Cand2.exam_answer

