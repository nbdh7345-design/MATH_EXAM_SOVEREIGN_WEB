-- CALC-MUL-AI-261023212601-9F62: 3 ứng viên formalize, biên dịch chung một file.
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

lemma ex_dx (c y x : ℝ) (hx : 0 < x) :
    HasDerivAt (fun t : ℝ => t * y + 4 * c ^ 3 / t + 2 * c ^ 3 / y) (y - 4 * c ^ 3 / (x * x)) x := by
  have hid : HasDerivAt (fun t : ℝ => t) 1 x := hasDerivAt_id x
  have hx' : x ≠ 0 := hx.ne'
  have h := ((hid.mul_const y).add ((hasDerivAt_const x (4 * c ^ 3)).div hid hx')).add
    (hasDerivAt_const x (2 * c ^ 3 / y))
  refine h.congr_deriv ?_
  first | (field_simp; ring) | field_simp | ring

lemma ex_gx (c y x : ℝ) (hx : 0 < x) :
    HasDerivAt (fun t : ℝ => y - 4 * c ^ 3 / (t * t)) (8 * c ^ 3 / x ^ 3) x := by
  have hid : HasDerivAt (fun t : ℝ => t) 1 x := hasDerivAt_id x
  have hx' : x ≠ 0 := hx.ne'
  have h := (hasDerivAt_const x y).sub
    ((hasDerivAt_const x (4 * c ^ 3)).div (hid.mul hid) (mul_ne_zero hx' hx'))
  refine h.congr_deriv ?_
  first | (field_simp; ring) | field_simp | ring

lemma ex_dy (c x y : ℝ) (hy : 0 < y) :
    HasDerivAt (fun t : ℝ => x * t + 4 * c ^ 3 / x + 2 * c ^ 3 / t) (x - 2 * c ^ 3 / (y * y)) y := by
  have hid : HasDerivAt (fun t : ℝ => t) 1 y := hasDerivAt_id y
  have hy' : y ≠ 0 := hy.ne'
  have h := (((hasDerivAt_const y x).mul hid).add (hasDerivAt_const y (4 * c ^ 3 / x))).add
    ((hasDerivAt_const y (2 * c ^ 3)).div hid hy')
  refine h.congr_deriv ?_
  first | (field_simp; ring) | field_simp | ring

lemma ex_gy (c x y : ℝ) (hy : 0 < y) :
    HasDerivAt (fun t : ℝ => x - 2 * c ^ 3 / (t * t)) (4 * c ^ 3 / y ^ 3) y := by
  have hid : HasDerivAt (fun t : ℝ => t) 1 y := hasDerivAt_id y
  have hy' : y ≠ 0 := hy.ne'
  have h := (hasDerivAt_const y x).sub
    ((hasDerivAt_const y (2 * c ^ 3)).div (hid.mul hid) (mul_ne_zero hy' hy'))
  refine h.congr_deriv ?_
  first | (field_simp; ring) | field_simp | ring

theorem exam_answer (m : ℕ) (hm_lo : 1 ≤ m) (hm_hi : m ≤ 6) :
    ∀ f : ℝ → ℝ → ℝ,
    (∀ x y : ℝ, 0 < x → 0 < y → f x y = x * y + 4 * (m:ℝ) ^ 3 / x + 2 * (m:ℝ) ^ 3 / y) →
    ∀ x₀ y₀ : ℝ, 0 < x₀ → 0 < y₀ →
      deriv (fun x => f x y₀) x₀ = 0 →
      deriv (fun y => f x₀ y) y₀ = 0 →
      f x₀ y₀
        + Matrix.trace (!![deriv (fun u => deriv (fun x => f x y₀) u) x₀,
                           deriv (fun v => deriv (fun x => f x v) x₀) y₀;
                           deriv (fun u => deriv (fun y => f u y) y₀) x₀,
                           deriv (fun v => deriv (fun y => f x₀ y) v) y₀] : Matrix (Fin 2) (Fin 2) ℝ)
        + Matrix.det (!![deriv (fun u => deriv (fun x => f x y₀) u) x₀,
                         deriv (fun v => deriv (fun x => f x v) x₀) y₀;
                         deriv (fun u => deriv (fun y => f u y) y₀) x₀,
                         deriv (fun v => deriv (fun y => f x₀ y) v) y₀] : Matrix (Fin 2) (Fin 2) ℝ)
      = (((8 : ℝ) + ((6 : ℝ) * ((m : ℝ) ^ (2 : ℕ))))) := by
  obtain ⟨c, hc⟩ : ∃ c : ℝ, (m:ℝ) = c := ⟨_, rfl⟩
  have h1m : (1:ℝ) ≤ (m:ℝ) := by exact_mod_cast hm_lo
  have hc0 : 0 < c := by rw [← hc]; linarith
  have hcne : c ≠ 0 := hc0.ne'
  intro f hf x₀ y₀ hx0 hy0 h1 h2
  rw [hc] at hf
  have hdx : ∀ y x : ℝ, 0 < x → 0 < y → deriv (fun t => f t y) x = y - 4 * c ^ 3 / (x * x) := by
    intro y x hx hy
    have e : Filter.EventuallyEq (nhds x) (fun t => f t y)
        (fun t : ℝ => t * y + 4 * c ^ 3 / t + 2 * c ^ 3 / y) := by
      filter_upwards [Ioi_mem_nhds hx] with t ht using hf t y ht hy
    exact ((ex_dx c y x hx).congr_of_eventuallyEq e).deriv
  have hdy : ∀ x y : ℝ, 0 < x → 0 < y → deriv (fun t => f x t) y = x - 2 * c ^ 3 / (y * y) := by
    intro x y hx hy
    have e : Filter.EventuallyEq (nhds y) (fun t => f x t)
        (fun t : ℝ => x * t + 4 * c ^ 3 / x + 2 * c ^ 3 / t) := by
      filter_upwards [Ioi_mem_nhds hy] with t ht using hf x t hx ht
    exact ((ex_dy c x y hy).congr_of_eventuallyEq e).deriv
  have a1 := (hdx y₀ x₀ hx0 hy0).symm.trans h1
  have a2 := (hdy x₀ y₀ hx0 hy0).symm.trans h2
  have hxx0 : x₀ * x₀ ≠ 0 := (mul_pos hx0 hx0).ne'
  have hyy0 : y₀ * y₀ ≠ 0 := (mul_pos hy0 hy0).ne'
  have t1 : 4 * c ^ 3 / (x₀ * x₀) = y₀ := by linarith
  have t2 : 2 * c ^ 3 / (y₀ * y₀) = x₀ := by linarith
  rw [div_eq_iff hxx0] at t1
  rw [div_eq_iff hyy0] at t2
  have hp : x₀ * y₀ * (x₀ - 2 * y₀) = 0 := by linear_combination (-1) * t1 + 2 * t2
  have hxy2 : x₀ = 2 * y₀ := by
    rcases mul_eq_zero.1 hp with h | h
    · exact absurd h (mul_pos hx0 hy0).ne'
    · linarith
  have hy3 : y₀ ^ 3 = c ^ 3 := by
    linear_combination (-1/2) * t2 + (-(y₀ ^ 2) / 2) * hxy2
  have hy2 : y₀ = c := by
    have hq : (y₀ - c) * (y₀ ^ 2 + y₀ * c + c ^ 2) = 0 := by linear_combination hy3
    rcases mul_eq_zero.1 hq with h | h
    · linarith
    · have : 0 < y₀ ^ 2 + y₀ * c + c ^ 2 := by positivity
      linarith
  have hx2 : x₀ = 2 * c := by linarith
  have hxx : deriv (fun u => deriv (fun x => f x y₀) u) x₀ = 8 * c ^ 3 / x₀ ^ 3 := by
    have e : Filter.EventuallyEq (nhds x₀) (fun u => deriv (fun x => f x y₀) u)
        (fun u : ℝ => y₀ - 4 * c ^ 3 / (u * u)) := by
      filter_upwards [Ioi_mem_nhds hx0] with u hu using hdx y₀ u hu hy0
    exact ((ex_gx c y₀ x₀ hx0).congr_of_eventuallyEq e).deriv
  have hyy : deriv (fun v => deriv (fun y => f x₀ y) v) y₀ = 4 * c ^ 3 / y₀ ^ 3 := by
    have e : Filter.EventuallyEq (nhds y₀) (fun v => deriv (fun y => f x₀ y) v)
        (fun v : ℝ => x₀ - 2 * c ^ 3 / (v * v)) := by
      filter_upwards [Ioi_mem_nhds hy0] with v hv using hdy x₀ v hx0 hv
    exact ((ex_gy c x₀ y₀ hy0).congr_of_eventuallyEq e).deriv
  have hxy : deriv (fun v => deriv (fun x => f x v) x₀) y₀ = 1 := by
    have e : Filter.EventuallyEq (nhds y₀) (fun v => deriv (fun x => f x v) x₀)
        (fun v : ℝ => v - 4 * c ^ 3 / (x₀ * x₀)) := by
      filter_upwards [Ioi_mem_nhds hy0] with v hv using hdx v x₀ hx0 hv
    have hid : HasDerivAt (fun t : ℝ => t) 1 y₀ := hasDerivAt_id y₀
    exact ((hid.sub_const (4 * c ^ 3 / (x₀ * x₀))).congr_of_eventuallyEq e).deriv
  have hyx : deriv (fun u => deriv (fun y => f u y) y₀) x₀ = 1 := by
    have e : Filter.EventuallyEq (nhds x₀) (fun u => deriv (fun y => f u y) y₀)
        (fun u : ℝ => u - 2 * c ^ 3 / (y₀ * y₀)) := by
      filter_upwards [Ioi_mem_nhds hx0] with u hu using hdy u y₀ hu hy0
    have hid : HasDerivAt (fun t : ℝ => t) 1 x₀ := hasDerivAt_id x₀
    exact ((hid.sub_const (2 * c ^ 3 / (y₀ * y₀))).congr_of_eventuallyEq e).deriv
  have hxx' : deriv (fun u => deriv (fun x => f x y₀) u) x₀ = 1 := by
    rw [hxx, hx2]
    first | (field_simp; ring) | field_simp
  have hyy' : deriv (fun v => deriv (fun y => f x₀ y) v) y₀ = 4 := by
    rw [hyy, hy2]
    first | (field_simp; ring) | field_simp
  have v1 : f x₀ y₀ = 6 * c ^ 2 := by
    rw [hf x₀ y₀ hx0 hy0, hx2, hy2]
    first | (field_simp; ring) | field_simp
  first
    | rw [Matrix.trace_fin_two_of, Matrix.det_fin_two_of]
    | simp only [Matrix.trace_fin_two_of, Matrix.det_fin_two_of]
  rw [hxx', hyy', hxy, hyx, v1]
  rw [← hc]
  first | ring | (push_cast; ring)

end Cand0
#print axioms Cand0.exam_answer

namespace Cand1

theorem exam_dx (a b x y : ℝ) (hx : x ≠ 0) :
    HasDerivAt (fun t : ℝ => t * y + a / t + b / y) (y - a / (x * x)) x := by
  have h1 : HasDerivAt (fun t : ℝ => t * y) y x := by
    simpa using (hasDerivAt_id' x).mul_const y
  have h2 : HasDerivAt (fun t : ℝ => a / t) (-(a / (x * x))) x := by
    refine ((hasDerivAt_const x a).div (hasDerivAt_id' x) hx).congr_deriv ?_
    first | ring1 | (field_simp; ring1) | field_simp
  have h3 := (h1.add h2).add_const (b / y)
  exact h3.congr_deriv (by ring1)

theorem exam_dy (a b x y : ℝ) (hy : y ≠ 0) :
    HasDerivAt (fun t : ℝ => x * t + a / x + b / t) (x - b / (y * y)) y := by
  have h1 : HasDerivAt (fun t : ℝ => x * t) x y := by
    simpa using (hasDerivAt_id' y).const_mul x
  have h2 : HasDerivAt (fun t : ℝ => b / t) (-(b / (y * y))) y := by
    refine ((hasDerivAt_const y b).div (hasDerivAt_id' y) hy).congr_deriv ?_
    first | ring1 | (field_simp; ring1) | field_simp
  have h3 := (h1.add_const (a / x)).add h2
  exact h3.congr_deriv (by ring1)

theorem exam_dxx (a y x : ℝ) (hx : x ≠ 0) :
    HasDerivAt (fun t : ℝ => y - a / (t * t)) (2 * a / (x * x * x)) x := by
  have h := (hasDerivAt_const x a).div ((hasDerivAt_id' x).mul (hasDerivAt_id' x)) (mul_ne_zero hx hx)
  have h' := (hasDerivAt_const x y).sub h
  refine h'.congr_deriv ?_
  first | (field_simp; ring1) | field_simp | ring1

theorem exam_answer (m : ℕ) (hm_lo : 1 ≤ m) (hm_hi : m ≤ 6) :
    ∀ f : ℝ → ℝ → ℝ, (∀ x y : ℝ, f x y = x * y + 4 * (m:ℝ)^3 / x + 2 * (m:ℝ)^3 / y) →
  ((∃ x₀ y₀ : ℝ, 0 < x₀ ∧ 0 < y₀ ∧ deriv (fun x => f x y₀) x₀ = 0 ∧ deriv (fun y => f x₀ y) y₀ = 0) ∧
   ∀ x₀ y₀ : ℝ, 0 < x₀ → 0 < y₀ → deriv (fun x => f x y₀) x₀ = 0 → deriv (fun y => f x₀ y) y₀ = 0 →
    f x₀ y₀
      + Matrix.trace (!![deriv (fun x => deriv (fun x' => f x' y₀) x) x₀,
                         deriv (fun y => deriv (fun x => f x y) x₀) y₀;
                         deriv (fun x => deriv (fun y => f x y) y₀) x₀,
                         deriv (fun y => deriv (fun y' => f x₀ y') y) y₀] : Matrix (Fin 2) (Fin 2) ℝ)
      + Matrix.det (!![deriv (fun x => deriv (fun x' => f x' y₀) x) x₀,
                       deriv (fun y => deriv (fun x => f x y) x₀) y₀;
                       deriv (fun x => deriv (fun y => f x y) y₀) x₀,
                       deriv (fun y => deriv (fun y' => f x₀ y') y) y₀] : Matrix (Fin 2) (Fin 2) ℝ)
      = (((8 : ℝ) + ((6 : ℝ) * ((m : ℝ) ^ (2 : ℕ)))))) := by
  intro f hf
  have hmpos : (0:ℝ) < (m:ℝ) := Nat.cast_pos.mpr (by omega)
  have hmne : (m:ℝ) ≠ 0 := hmpos.ne'
  have d1 : ∀ x y : ℝ, x ≠ 0 → deriv (fun t => f t y) x = y - 4 * (m:ℝ)^3 / (x * x) := by
    intro x y hx
    have h : (fun t => f t y) = fun t => t * y + 4 * (m:ℝ)^3 / t + 2 * (m:ℝ)^3 / y :=
      funext fun t => hf t y
    rw [h]
    exact (exam_dx (4 * (m:ℝ)^3) (2 * (m:ℝ)^3) x y hx).deriv
  have d2 : ∀ x y : ℝ, y ≠ 0 → deriv (fun t => f x t) y = x - 2 * (m:ℝ)^3 / (y * y) := by
    intro x y hy
    have h : (fun t => f x t) = fun t => x * t + 4 * (m:ℝ)^3 / x + 2 * (m:ℝ)^3 / t :=
      funext fun t => hf x t
    rw [h]
    exact (exam_dy (4 * (m:ℝ)^3) (2 * (m:ℝ)^3) x y hy).deriv
  have hH : ∀ x₀ y₀ : ℝ, 0 < x₀ → 0 < y₀ →
      deriv (fun x => deriv (fun x' => f x' y₀) x) x₀ = 2 * (4 * (m:ℝ)^3) / (x₀ * x₀ * x₀) ∧
      deriv (fun y => deriv (fun x => f x y) x₀) y₀ = 1 ∧
      deriv (fun x => deriv (fun y => f x y) y₀) x₀ = 1 ∧
      deriv (fun y => deriv (fun y' => f x₀ y') y) y₀ = 2 * (2 * (m:ℝ)^3) / (y₀ * y₀ * y₀) := by
    intro x₀ y₀ hx hy
    have hx' : x₀ ≠ 0 := hx.ne'
    have hy' : y₀ ≠ 0 := hy.ne'
    refine ⟨?_, ?_, ?_, ?_⟩
    · have hev : Filter.EventuallyEq (nhds x₀) (fun x => deriv (fun x' => f x' y₀) x)
          (fun x => y₀ - 4 * (m:ℝ)^3 / (x * x)) := by
        filter_upwards [Ioi_mem_nhds hx] with t ht
        exact d1 t y₀ (show (0:ℝ) < t from ht).ne'
      rw [hev.deriv_eq]
      exact (exam_dxx (4 * (m:ℝ)^3) y₀ x₀ hx').deriv
    · have h : (fun y => deriv (fun x => f x y) x₀) = fun y => y - 4 * (m:ℝ)^3 / (x₀ * x₀) :=
        funext fun y => d1 x₀ y hx'
      rw [h]
      exact ((hasDerivAt_id' y₀).sub_const (4 * (m:ℝ)^3 / (x₀ * x₀))).deriv
    · have h : (fun x => deriv (fun y => f x y) y₀) = fun x => x - 2 * (m:ℝ)^3 / (y₀ * y₀) :=
        funext fun x => d2 x y₀ hy'
      rw [h]
      exact ((hasDerivAt_id' x₀).sub_const (2 * (m:ℝ)^3 / (y₀ * y₀))).deriv
    · have hev : Filter.EventuallyEq (nhds y₀) (fun y => deriv (fun y' => f x₀ y') y)
          (fun y => x₀ - 2 * (m:ℝ)^3 / (y * y)) := by
        filter_upwards [Ioi_mem_nhds hy] with t ht
        exact d2 x₀ t (show (0:ℝ) < t from ht).ne'
      rw [hev.deriv_eq]
      exact (exam_dxx (2 * (m:ℝ)^3) x₀ y₀ hy').deriv
  constructor
  · have h2m : (0:ℝ) < 2 * (m:ℝ) := by linarith
    refine ⟨2 * (m:ℝ), (m:ℝ), h2m, hmpos, ?_, ?_⟩
    · rw [d1 (2 * (m:ℝ)) (m:ℝ) h2m.ne']
      first | (field_simp; ring1) | field_simp
    · rw [d2 (2 * (m:ℝ)) (m:ℝ) hmne]
      first | (field_simp; ring1) | field_simp
  · intro x₀ y₀ hx hy hs1 hs2
    rw [d1 x₀ y₀ hx.ne'] at hs1
    rw [d2 x₀ y₀ hy.ne'] at hs2
    obtain ⟨h00, h01, h10, h11⟩ := hH x₀ y₀ hx hy
    have hxx : x₀ * x₀ ≠ 0 := mul_ne_zero hx.ne' hx.ne'
    have hyy : y₀ * y₀ ≠ 0 := mul_ne_zero hy.ne' hy.ne'
    have e1 : y₀ * (x₀ * x₀) = 4 * (m:ℝ)^3 := by
      have h : y₀ = 4 * (m:ℝ)^3 / (x₀ * x₀) := by linarith
      exact (eq_div_iff hxx).mp h
    have e2 : x₀ * (y₀ * y₀) = 2 * (m:ℝ)^3 := by
      have h : x₀ = 2 * (m:ℝ)^3 / (y₀ * y₀) := by linarith
      exact (eq_div_iff hyy).mp h
    have hx2 : x₀ = 2 * y₀ := by
      have h : x₀ * y₀ * (x₀ - 2 * y₀) = 0 := by linear_combination e1 - 2 * e2
      rcases mul_eq_zero.mp h with h | h
      · exact absurd h (mul_pos hx hy).ne'
      · linarith
    have hy3 : (y₀ - (m:ℝ)) * (y₀^2 + y₀ * (m:ℝ) + (m:ℝ)^2) = 0 := by
      rw [hx2] at e1
      linear_combination (1/4) * e1
    have hym : y₀ = (m:ℝ) := by
      rcases mul_eq_zero.mp hy3 with h | h
      · linarith
      · have hp := mul_pos hy hmpos
        nlinarith [sq_nonneg y₀, sq_nonneg (m:ℝ)]
    have hxm : x₀ = 2 * (m:ℝ) := by linarith
    rw [h00, h01, h10, h11, hf x₀ y₀, Matrix.trace_fin_two_of, Matrix.det_fin_two_of, hxm, hym]
    first | (field_simp; ring1) | field_simp

end Cand1
#print axioms Cand1.exam_answer

namespace Cand2

lemma ex_hasA (c y x : ℝ) (hx : x ≠ 0) :
    HasDerivAt (fun t : ℝ => t * y + 4 * c ^ 3 / t + 2 * c ^ 3 / y)
      (y - 4 * c ^ 3 * (x⁻¹ * x⁻¹)) x := by
  have h1 : HasDerivAt (fun t : ℝ => t * y) y x := by
    have := (hasDerivAt_id' x).mul_const y
    rwa [one_mul] at this
  have h2 := (hasDerivAt_inv hx).const_mul (4 * c ^ 3)
  have h3 := (h1.add h2).add_const (2 * c ^ 3 / y)
  convert h3 using 1 <;>
    first
    | (funext t; simp only [div_eq_mul_inv]; done)
    | (funext t; ring1)
    | ring1

lemma ex_hasB (c x y : ℝ) (hy : y ≠ 0) :
    HasDerivAt (fun t : ℝ => x * t + 4 * c ^ 3 / x + 2 * c ^ 3 / t)
      (x - 2 * c ^ 3 * (y⁻¹ * y⁻¹)) y := by
  have h1 : HasDerivAt (fun t : ℝ => x * t) x y := by
    have := (hasDerivAt_id' y).const_mul x
    rwa [mul_one] at this
  have h2 := (hasDerivAt_inv hy).const_mul (2 * c ^ 3)
  have h3 := (h1.add_const (4 * c ^ 3 / x)).add h2
  convert h3 using 1 <;>
    first
    | (funext t; simp only [div_eq_mul_inv]; done)
    | (funext t; ring1)
    | ring1

lemma ex_dfx (c : ℝ) (f : ℝ → ℝ → ℝ)
    (hf : ∀ x y : ℝ, f x y = x * y + 4 * c ^ 3 / x + 2 * c ^ 3 / y)
    (x y : ℝ) (hx : 0 < x) :
    deriv (fun t : ℝ => f t y) x = y - 4 * c ^ 3 * (x⁻¹ * x⁻¹) := by
  have h : (fun t : ℝ => f t y) = fun t : ℝ => t * y + 4 * c ^ 3 / t + 2 * c ^ 3 / y := by
    funext t
    exact hf t y
  rw [h]
  exact (ex_hasA c y x hx.ne').deriv

lemma ex_dfy (c : ℝ) (f : ℝ → ℝ → ℝ)
    (hf : ∀ x y : ℝ, f x y = x * y + 4 * c ^ 3 / x + 2 * c ^ 3 / y)
    (x y : ℝ) (hy : 0 < y) :
    deriv (fun t : ℝ => f x t) y = x - 2 * c ^ 3 * (y⁻¹ * y⁻¹) := by
  have h : (fun t : ℝ => f x t) = fun t : ℝ => x * t + 4 * c ^ 3 / x + 2 * c ^ 3 / t := by
    funext t
    exact hf x t
  rw [h]
  exact (ex_hasB c x y hy.ne').deriv

lemma ex_dfxx (c : ℝ) (f : ℝ → ℝ → ℝ)
    (hf : ∀ x y : ℝ, f x y = x * y + 4 * c ^ 3 / x + 2 * c ^ 3 / y)
    (x y : ℝ) (hx : 0 < x) :
    deriv (fun u : ℝ => deriv (fun t : ℝ => f t y) u) x
      = 8 * c ^ 3 * (x⁻¹ * x⁻¹ * x⁻¹) := by
  have hinv : HasDerivAt (fun u : ℝ => u⁻¹) (-(x ^ 2)⁻¹) x := hasDerivAt_inv hx.ne'
  have h1 := hinv.mul hinv
  have h2 := (h1.const_mul (4 * c ^ 3)).const_sub y
  have hev : (fun u : ℝ => deriv (fun t : ℝ => f t y) u)
      =ᶠ[nhds x] (fun u : ℝ => y - 4 * c ^ 3 * (u⁻¹ * u⁻¹)) := by
    filter_upwards [Ioi_mem_nhds hx] with u hu
    exact ex_dfx c f hf u y hu
  refine ((h2.congr_of_eventuallyEq hev).deriv).trans ?_
  first
  | ring1
  | (beta_reduce; ring1)

lemma ex_dfyy (c : ℝ) (f : ℝ → ℝ → ℝ)
    (hf : ∀ x y : ℝ, f x y = x * y + 4 * c ^ 3 / x + 2 * c ^ 3 / y)
    (x y : ℝ) (hy : 0 < y) :
    deriv (fun u : ℝ => deriv (fun t : ℝ => f x t) u) y
      = 4 * c ^ 3 * (y⁻¹ * y⁻¹ * y⁻¹) := by
  have hinv : HasDerivAt (fun u : ℝ => u⁻¹) (-(y ^ 2)⁻¹) y := hasDerivAt_inv hy.ne'
  have h1 := hinv.mul hinv
  have h2 := (h1.const_mul (2 * c ^ 3)).const_sub x
  have hev : (fun u : ℝ => deriv (fun t : ℝ => f x t) u)
      =ᶠ[nhds y] (fun u : ℝ => x - 2 * c ^ 3 * (u⁻¹ * u⁻¹)) := by
    filter_upwards [Ioi_mem_nhds hy] with u hu
    exact ex_dfy c f hf x u hu
  refine ((h2.congr_of_eventuallyEq hev).deriv).trans ?_
  first
  | ring1
  | (beta_reduce; ring1)

lemma ex_dfxy (c : ℝ) (f : ℝ → ℝ → ℝ)
    (hf : ∀ x y : ℝ, f x y = x * y + 4 * c ^ 3 / x + 2 * c ^ 3 / y)
    (x y : ℝ) (hx : 0 < x) :
    deriv (fun u : ℝ => deriv (fun t : ℝ => f t u) x) y = 1 := by
  have h : (fun u : ℝ => deriv (fun t : ℝ => f t u) x)
      = fun u : ℝ => u - 4 * c ^ 3 * (x⁻¹ * x⁻¹) := by
    funext u
    exact ex_dfx c f hf x u hx
  rw [h]
  exact ((hasDerivAt_id' y).sub_const (4 * c ^ 3 * (x⁻¹ * x⁻¹))).deriv

lemma ex_dfyx (c : ℝ) (f : ℝ → ℝ → ℝ)
    (hf : ∀ x y : ℝ, f x y = x * y + 4 * c ^ 3 / x + 2 * c ^ 3 / y)
    (x y : ℝ) (hy : 0 < y) :
    deriv (fun u : ℝ => deriv (fun t : ℝ => f u t) y) x = 1 := by
  have h : (fun u : ℝ => deriv (fun t : ℝ => f u t) y)
      = fun u : ℝ => u - 2 * c ^ 3 * (y⁻¹ * y⁻¹) := by
    funext u
    exact ex_dfy c f hf u y hy
  rw [h]
  exact ((hasDerivAt_id' x).sub_const (2 * c ^ 3 * (y⁻¹ * y⁻¹))).deriv

lemma ex_stat1 (c x y : ℝ) (hx : x ≠ 0) (h : y - 4 * c ^ 3 * (x⁻¹ * x⁻¹) = 0) :
    y * x ^ 2 = 4 * c ^ 3 := by
  have hi : x⁻¹ * x = 1 := inv_mul_cancel₀ hx
  linear_combination x ^ 2 * h + 4 * c ^ 3 * (x⁻¹ * x + 1) * hi

lemma ex_stat2 (c x y : ℝ) (hy : y ≠ 0) (h : x - 2 * c ^ 3 * (y⁻¹ * y⁻¹) = 0) :
    x * y ^ 2 = 2 * c ^ 3 := by
  have hi : y⁻¹ * y = 1 := inv_mul_cancel₀ hy
  linear_combination y ^ 2 * h + 2 * c ^ 3 * (y⁻¹ * y + 1) * hi

lemma ex_solve (c x y : ℝ) (hc : 0 < c) (hx : 0 < x) (hy : 0 < y)
    (e1 : y * x ^ 2 = 4 * c ^ 3) (e2 : x * y ^ 2 = 2 * c ^ 3) :
    x = 2 * c ∧ y = c := by
  have h1 : x * y * (x - 2 * y) = 0 := by linear_combination e1 - 2 * e2
  have hxy : x * y ≠ 0 := (mul_pos hx hy).ne'
  have h2 : x - 2 * y = 0 := by
    rcases mul_eq_zero.mp h1 with h | h
    · exact absurd h hxy
    · exact h
  have hx2 : x = 2 * y := by linarith
  subst hx2
  have h3 : (y - c) * (y ^ 2 + y * c + c ^ 2) = 0 := by
    linear_combination (1 / 4 : ℝ) * e1
  have h4 : y ^ 2 + y * c + c ^ 2 ≠ 0 := by positivity
  have h5 : y - c = 0 := by
    rcases mul_eq_zero.mp h3 with h | h
    · exact h
    · exact absurd h h4
  have h6 : y = c := by linarith
  exact ⟨by linarith, h6⟩

theorem exam_answer (m : ℕ) (hm_lo : 1 ≤ m) (hm_hi : m ≤ 6) :
    ∀ f : ℝ → ℝ → ℝ,
    (∀ x y : ℝ, f x y = x * y + 4 * (m : ℝ) ^ 3 / x + 2 * (m : ℝ) ^ 3 / y) →
    (∃! p : ℝ × ℝ, 0 < p.1 ∧ 0 < p.2 ∧
        deriv (fun t : ℝ => f t p.2) p.1 = 0 ∧
        deriv (fun t : ℝ => f p.1 t) p.2 = 0) ∧
    (∀ x₀ y₀ : ℝ, 0 < x₀ → 0 < y₀ →
        deriv (fun t : ℝ => f t y₀) x₀ = 0 →
        deriv (fun t : ℝ => f x₀ t) y₀ = 0 →
        f x₀ y₀
          + Matrix.trace (!![deriv (fun u : ℝ => deriv (fun t : ℝ => f t y₀) u) x₀,
                             deriv (fun u : ℝ => deriv (fun t : ℝ => f t u) x₀) y₀;
                             deriv (fun u : ℝ => deriv (fun t : ℝ => f u t) y₀) x₀,
                             deriv (fun u : ℝ => deriv (fun t : ℝ => f x₀ t) u) y₀]
                            : Matrix (Fin 2) (Fin 2) ℝ)
          + Matrix.det (!![deriv (fun u : ℝ => deriv (fun t : ℝ => f t y₀) u) x₀,
                           deriv (fun u : ℝ => deriv (fun t : ℝ => f t u) x₀) y₀;
                           deriv (fun u : ℝ => deriv (fun t : ℝ => f u t) y₀) x₀,
                           deriv (fun u : ℝ => deriv (fun t : ℝ => f x₀ t) u) y₀]
                          : Matrix (Fin 2) (Fin 2) ℝ)
          = (((8 : ℝ) + ((6 : ℝ) * ((m : ℝ) ^ (2 : ℕ)))))) := by
  intro f hf
  have hc : (0:ℝ) < (m:ℝ) := by
    have : (1:ℝ) ≤ (m:ℝ) := by exact_mod_cast hm_lo
    linarith
  have hc0 : (m:ℝ) ≠ 0 := hc.ne'
  refine ⟨?_, ?_⟩
  · have hex : 0 < 2 * (m:ℝ) ∧ 0 < (m:ℝ) ∧
        deriv (fun t : ℝ => f t (m:ℝ)) (2 * (m:ℝ)) = 0 ∧
        deriv (fun t : ℝ => f (2 * (m:ℝ)) t) (m:ℝ) = 0 := by
      have h2c : 0 < 2 * (m:ℝ) := by positivity
      refine ⟨h2c, hc, ?_, ?_⟩
      · rw [ex_dfx (m:ℝ) f hf (2 * (m:ℝ)) (m:ℝ) h2c]
        first
        | (field_simp; ring1)
        | field_simp
        | (field_simp; ring_nf)
      · rw [ex_dfy (m:ℝ) f hf (2 * (m:ℝ)) (m:ℝ) hc]
        first
        | (field_simp; ring1)
        | field_simp
        | (field_simp; ring_nf)
    refine ⟨(2 * (m:ℝ), (m:ℝ)), hex, ?_⟩
    intro q hq
    obtain ⟨hx, hy, h1, h2⟩ := hq
    have h1' : q.2 - 4 * (m:ℝ) ^ 3 * (q.1⁻¹ * q.1⁻¹) = 0 :=
      (ex_dfx (m:ℝ) f hf q.1 q.2 hx).symm.trans h1
    have h2' : q.1 - 2 * (m:ℝ) ^ 3 * (q.2⁻¹ * q.2⁻¹) = 0 :=
      (ex_dfy (m:ℝ) f hf q.1 q.2 hy).symm.trans h2
    obtain ⟨hq1, hq2⟩ := ex_solve (m:ℝ) q.1 q.2 hc hx hy
      (ex_stat1 (m:ℝ) q.1 q.2 hx.ne' h1') (ex_stat2 (m:ℝ) q.1 q.2 hy.ne' h2')
    exact Prod.ext hq1 hq2
  · intro x₀ y₀ hx hy h1 h2
    have h1' : y₀ - 4 * (m:ℝ) ^ 3 * (x₀⁻¹ * x₀⁻¹) = 0 :=
      (ex_dfx (m:ℝ) f hf x₀ y₀ hx).symm.trans h1
    have h2' : x₀ - 2 * (m:ℝ) ^ 3 * (y₀⁻¹ * y₀⁻¹) = 0 :=
      (ex_dfy (m:ℝ) f hf x₀ y₀ hy).symm.trans h2
    obtain ⟨hx0, hy0⟩ := ex_solve (m:ℝ) x₀ y₀ hc hx hy
      (ex_stat1 (m:ℝ) x₀ y₀ hx.ne' h1') (ex_stat2 (m:ℝ) x₀ y₀ hy.ne' h2')
    rw [Matrix.trace_fin_two_of, Matrix.det_fin_two_of,
      ex_dfxx (m:ℝ) f hf x₀ y₀ hx, ex_dfxy (m:ℝ) f hf x₀ y₀ hx,
      ex_dfyx (m:ℝ) f hf x₀ y₀ hy, ex_dfyy (m:ℝ) f hf x₀ y₀ hy, hf]
    subst hx0
    subst hy0
    first
    | (field_simp; ring1)
    | field_simp
    | (field_simp; ring_nf)

end Cand2
#print axioms Cand2.exam_answer

