-- CALC-LIM-AI-261023212534-4E52: 3 ứng viên formalize, biên dịch chung một file.
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
open Real Filter Topology Asymptotics
lemma ex_sin_exp3 (c : ℝ) :
    (fun x : ℝ => Real.sin (c * x) - (c * x - (c * x) ^ 3 / 6)) =o[𝓝 0] fun x : ℝ => x ^ 3 := by
  have h := MathExam.sin_mul_maclaurin c 2
  have h' := MathExam.isLittleO_pow_of_le h (show 3 ≤ 2 * 2 by norm_num)
  exact h'.congr (fun x => by norm_num [Finset.sum_range_succ, Nat.factorial] <;> ring) (fun _ => rfl)

lemma ex_cos_exp2 (c : ℝ) :
    (fun x : ℝ => Real.cos (c * x) - (1 - (c * x) ^ 2 / 2)) =o[𝓝 0] fun x : ℝ => x ^ 2 := by
  have h := MathExam.cos_mul_maclaurin c 1
  have h' := MathExam.isLittleO_pow_of_le h (show 2 ≤ 2 * 1 + 1 by norm_num)
  exact h'.congr (fun x => by norm_num [Finset.sum_range_succ, Nat.factorial] <;> ring) (fun _ => rfl)

lemma ex_sin_exp1 (c : ℝ) :
    (fun x : ℝ => Real.sin (c * x) - c * x) =o[𝓝 0] fun x : ℝ => x := by
  have h := MathExam.sin_mul_maclaurin c 1
  have h' := MathExam.isLittleO_pow_of_le h (show 1 ≤ 2 * 1 by norm_num)
  exact h'.congr (fun x => by norm_num [Finset.sum_range_succ, Nat.factorial] <;> ring) (fun x => by ring)

lemma ex_den_o (c : ℝ) :
    (fun x : ℝ => x ^ 2 * Real.sin (c * x) - c * x ^ 3) =o[𝓝 0] fun x : ℝ => x ^ 3 := by
  have := (Asymptotics.isBigO_refl (fun x : ℝ => x ^ 2) (𝓝 0)).mul_isLittleO (ex_sin_exp1 c)
  exact this.congr (fun x => by ring) (fun x => by ring)

lemma ex_aux_ev (c : ℝ) :
    ∀ᶠ x : ℝ in 𝓝[≠] (0:ℝ), x ≠ 0 ∧ c * x ∈ Set.Ioo (-(Real.pi / 2)) (Real.pi / 2) := by
  have hcont : Continuous (fun x : ℝ => c * x) := by
    first
      | fun_prop
      | exact continuous_const.mul continuous_id
  have hmem : Set.Ioo (-(Real.pi / 2)) (Real.pi / 2) ∈ 𝓝 (c * 0) := by
    rw [mul_zero]
    exact Ioo_mem_nhds (by linarith [Real.pi_pos]) (by linarith [Real.pi_pos])
  have h0 : ∀ᶠ x : ℝ in 𝓝 (0:ℝ), c * x ∈ Set.Ioo (-(Real.pi / 2)) (Real.pi / 2) :=
    (hcont.tendsto 0).eventually_mem hmem
  have h2 : ∀ᶠ x : ℝ in 𝓝[≠] (0:ℝ), c * x ∈ Set.Ioo (-(Real.pi / 2)) (Real.pi / 2) := by
    first
      | exact eventually_nhdsWithin_of_eventually_nhds h0
      | exact h0.filter_mono nhdsWithin_le_nhds
  have h1 : ∀ᶠ x : ℝ in 𝓝[≠] (0:ℝ), x ≠ 0 := by
    filter_upwards [self_mem_nhdsWithin] with x hx
    first
      | exact hx
      | simpa using hx
  filter_upwards [h1, h2] with x hx hx2
  exact ⟨hx, hx2⟩

lemma ex_sin_ne_zero (u : ℝ) (hu : u ∈ Set.Ioo (-(Real.pi / 2)) (Real.pi / 2)) (hu0 : u ≠ 0) :
    Real.sin u ≠ 0 := by
  have hp := Real.pi_pos
  have h1 : -Real.pi < u := by linarith [hu.1]
  have h2 : u < Real.pi := by linarith [hu.2]
  rcases lt_or_gt_of_ne hu0 with h | h
  · exact (Real.sin_neg_of_neg_of_neg_pi_lt h h1).ne
  · exact (Real.sin_pos_of_pos_of_lt_pi h h2).ne'

lemma ex_tan_part (c : ℝ) (hc : c ≠ 0) :
    Filter.Tendsto (fun x : ℝ => c / (x * Real.tan (c * x)) - 1 / x ^ 2) (𝓝[≠] (0:ℝ))
      (𝓝 (-c ^ 2 / 3)) := by
  have h1 := ex_cos_exp2 c
  have h2 := ex_sin_exp3 c
  have h3 : (fun x : ℝ => c * (x * (Real.cos (c * x) - (1 - (c * x) ^ 2 / 2)))) =o[𝓝 0]
      fun x : ℝ => x ^ 3 := by
    have := ((Asymptotics.isBigO_refl (fun x : ℝ => x) (𝓝 0)).mul_isLittleO h1).const_mul_left c
    exact this.congr (fun _ => rfl) (fun x => by ring)
  have hnum : (fun x : ℝ => (c * x * Real.cos (c * x) - Real.sin (c * x)) - (-c ^ 3 / 3) * x ^ 3)
      =o[𝓝 0] fun x : ℝ => x ^ 3 :=
    (h3.sub h2).congr (fun x => by ring) (fun _ => rfl)
  have hden := ex_den_o c
  have hlim := MathExam.tendsto_div_of_isLittleO hc hnum hden
  have hval : -c ^ 3 / 3 / c = -c ^ 2 / 3 := by
    rw [div_eq_iff hc]; ring
  rw [hval] at hlim
  refine Filter.Tendsto.congr' ?_ hlim
  filter_upwards [ex_aux_ev c] with x hx
  obtain ⟨hx0, hxI⟩ := hx
  have hs : Real.sin (c * x) ≠ 0 := ex_sin_ne_zero _ hxI (mul_ne_zero hc hx0)
  have hco : Real.cos (c * x) ≠ 0 := (Real.cos_pos_of_mem_Ioo hxI).ne'
  try dsimp only
  rw [Real.tan_eq_sin_div_cos]
  first
    | (field_simp; ring)
    | field_simp

lemma ex_sin_part (c : ℝ) (hc : c ≠ 0) :
    Filter.Tendsto (fun x : ℝ => c / (x * Real.sin (c * x)) - 1 / x ^ 2) (𝓝[≠] (0:ℝ))
      (𝓝 (c ^ 2 / 6)) := by
  have h2 := ex_sin_exp3 c
  have hnum : (fun x : ℝ => (c * x - Real.sin (c * x)) - (c ^ 3 / 6) * x ^ 3)
      =o[𝓝 0] fun x : ℝ => x ^ 3 :=
    (h2.const_mul_left (-1)).congr (fun x => by ring) (fun _ => rfl)
  have hden := ex_den_o c
  have hlim := MathExam.tendsto_div_of_isLittleO hc hnum hden
  have hval : c ^ 3 / 6 / c = c ^ 2 / 6 := by
    rw [div_eq_iff hc]; ring
  rw [hval] at hlim
  refine Filter.Tendsto.congr' ?_ hlim
  filter_upwards [ex_aux_ev c] with x hx
  obtain ⟨hx0, hxI⟩ := hx
  have hs : Real.sin (c * x) ≠ 0 := ex_sin_ne_zero _ hxI (mul_ne_zero hc hx0)
  try dsimp only
  first
    | (field_simp; ring)
    | field_simp

theorem exam_answer (a : ℕ) (ha_lo : 2 ≤ a) (ha_hi : a ≤ 5) (b : ℕ) (hb_lo : 2 ≤ b) (hb_hi : b ≤ 5) :
    Filter.Tendsto (fun x : ℝ => (a:ℝ) / (x * Real.tan ((a:ℝ) * x)) - (b:ℝ) / (x * Real.sin ((b:ℝ) * x))) (𝓝[≠] (0:ℝ)) (𝓝 (((((-1 : ℝ) / 3) * ((a : ℝ) ^ (2 : ℕ))) + (((-1 : ℝ) / 6) * ((b : ℝ) ^ (2 : ℕ)))))) := by
  have ha : (a:ℝ) ≠ 0 := by
    have h : (2:ℝ) ≤ (a:ℝ) := by exact_mod_cast ha_lo
    exact (by linarith : (0:ℝ) < (a:ℝ)).ne'
  have hb : (b:ℝ) ≠ 0 := by
    have h : (2:ℝ) ≤ (b:ℝ) := by exact_mod_cast hb_lo
    exact (by linarith : (0:ℝ) < (b:ℝ)).ne'
  have hA := ex_tan_part (a:ℝ) ha
  have hB := ex_sin_part (b:ℝ) hb
  have key : Filter.Tendsto (fun x : ℝ => (a:ℝ) / (x * Real.tan ((a:ℝ) * x)) - (b:ℝ) / (x * Real.sin ((b:ℝ) * x))) (𝓝[≠] (0:ℝ)) (𝓝 (-(a:ℝ) ^ 2 / 3 - (b:ℝ) ^ 2 / 6)) := by
    refine Filter.Tendsto.congr (fun x => ?_) (hA.sub hB)
    try dsimp only
    ring
  first
    | (convert key using 2; ring)
    | (convert key using 3; ring)
    | (convert key using 1; congr 1; ring)

end Cand0
#print axioms Cand0.exam_answer

namespace Cand1
open Real Filter Topology
lemma ex_sin_lim (k : ℝ) :
    Filter.Tendsto (fun x : ℝ => (Real.sin (k*x) - k*x)/x^3) (𝓝[≠] 0) (𝓝 (-k^3/6)) := by
  have h := MathExam.sin_mul_maclaurin k 2
  have h2 := MathExam.isLittleO_pow_of_le h (show 3 ≤ 2*2 by norm_num)
  refine MathExam.tendsto_div_pow_of_isLittleO (f := fun x => Real.sin (k*x) - k*x) (c := -k^3/6) (n := 3) ?_
  convert h2 using 1
  try funext x
  simp only [Finset.sum_range_succ, Finset.sum_range_zero]
  first
    | (norm_num [Nat.factorial]; done)
    | (norm_num [Nat.factorial]; ring)
    | (simp [Nat.factorial]; ring)
    | (norm_num [Nat.factorial]; ring_nf)

lemma ex_cos_lim (k : ℝ) :
    Filter.Tendsto (fun x : ℝ => (Real.cos (k*x) - 1)/x^2) (𝓝[≠] 0) (𝓝 (-k^2/2)) := by
  have h := MathExam.cos_mul_maclaurin k 1
  have h2 := MathExam.isLittleO_pow_of_le h (show 2 ≤ 2*1+1 by norm_num)
  refine MathExam.tendsto_div_pow_of_isLittleO (f := fun x => Real.cos (k*x) - 1) (c := -k^2/2) (n := 2) ?_
  convert h2 using 1
  try funext x
  simp only [Finset.sum_range_succ, Finset.sum_range_zero]
  first
    | (norm_num [Nat.factorial]; done)
    | (norm_num [Nat.factorial]; ring)
    | (simp [Nat.factorial]; ring)
    | (norm_num [Nat.factorial]; ring_nf)

lemma ex_alg_aux (a b x A B C : ℝ) (hx : x ≠ 0) (hP : a + x^2*A ≠ 0) (hQ : b + x^2*B ≠ 0) :
    a * (1 + x^2*C) / (x * (x * (a + x^2*A))) - b / (x * (x * (b + x^2*B)))
      = (a*B + a*b*C + a*x^2*C*B - b*A) / ((a + x^2*A) * (b + x^2*B)) := by
  field_simp <;> ring

lemma ex_eq_aux (a b x : ℝ) (hx : x ≠ 0)
    (hP : a + x^2 * ((Real.sin (a*x) - a*x)/x^3) ≠ 0)
    (hQ : b + x^2 * ((Real.sin (b*x) - b*x)/x^3) ≠ 0) :
    (a * ((Real.sin (b*x) - b*x)/x^3) + a*b*((Real.cos (a*x) - 1)/x^2)
      + a*x^2*((Real.cos (a*x) - 1)/x^2)*((Real.sin (b*x) - b*x)/x^3)
      - b*((Real.sin (a*x) - a*x)/x^3))
      / ((a + x^2*((Real.sin (a*x) - a*x)/x^3)) * (b + x^2*((Real.sin (b*x) - b*x)/x^3)))
    = a / (x * Real.tan (a*x)) - b / (x * Real.sin (b*x)) := by
  have hsa : Real.sin (a*x) = x * (a + x^2 * ((Real.sin (a*x) - a*x)/x^3)) := by
    field_simp <;> ring
  have hsb : Real.sin (b*x) = x * (b + x^2 * ((Real.sin (b*x) - b*x)/x^3)) := by
    field_simp <;> ring
  have hca : Real.cos (a*x) = 1 + x^2 * ((Real.cos (a*x) - 1)/x^2) := by
    field_simp <;> ring
  have ht : a / (x * Real.tan (a*x)) = a * Real.cos (a*x) / (x * Real.sin (a*x)) := by
    rw [Real.tan_eq_sin_div_cos, ← mul_div_assoc, div_div_eq_mul_div]
  rw [ht]
  have h := ex_alg_aux a b x ((Real.sin (a*x) - a*x)/x^3) ((Real.sin (b*x) - b*x)/x^3)
    ((Real.cos (a*x) - 1)/x^2) hx hP hQ
  refine h.symm.trans ?_
  rw [← hsa, ← hsb, ← hca]

lemma ex_main (a b : ℝ) (ha : 0 < a) (hb : 0 < b) :
    Filter.Tendsto (fun x : ℝ => a / (x * Real.tan (a*x)) - b / (x * Real.sin (b*x)))
      (𝓝[≠] 0) (𝓝 (-(2*a^2+b^2)/6)) := by
  have ha' : a ≠ 0 := ha.ne'
  have hb' : b ≠ 0 := hb.ne'
  have hne : a * b ≠ 0 := mul_ne_zero ha' hb'
  have hA := ex_sin_lim a
  have hB := ex_sin_lim b
  have hC := ex_cos_lim a
  have hx2 : Filter.Tendsto (fun x : ℝ => x^2) (𝓝[≠] 0) (𝓝 0) :=
    ((continuous_pow 2).tendsto' 0 0 (by norm_num)).mono_left nhdsWithin_le_nhds
  have hP : Filter.Tendsto (fun x : ℝ => a + x^2 * ((Real.sin (a*x) - a*x)/x^3)) (𝓝[≠] 0) (𝓝 a) := by
    have this := (hx2.mul hA).const_add a
    have e : a + 0 * (-a^3/6) = a := by ring
    first | (rw [e] at this; exact this) | simpa using this
  have hQ : Filter.Tendsto (fun x : ℝ => b + x^2 * ((Real.sin (b*x) - b*x)/x^3)) (𝓝[≠] 0) (𝓝 b) := by
    have this := (hx2.mul hB).const_add b
    have e : b + 0 * (-b^3/6) = b := by ring
    first | (rw [e] at this; exact this) | simpa using this
  have hPev : ∀ᶠ x in 𝓝[≠] (0:ℝ), a + x^2 * ((Real.sin (a*x) - a*x)/x^3) ≠ 0 := by
    first
      | exact hP.eventually_ne ha'
      | exact hP.eventually (isOpen_ne.mem_nhds ha')
  have hQev : ∀ᶠ x in 𝓝[≠] (0:ℝ), b + x^2 * ((Real.sin (b*x) - b*x)/x^3) ≠ 0 := by
    first
      | exact hQ.eventually_ne hb'
      | exact hQ.eventually (isOpen_ne.mem_nhds hb')
  have t1 := hB.const_mul a
  have t2 := hC.const_mul (a*b)
  have t3 := ((hx2.const_mul a).mul hC).mul hB
  have t4 := hA.const_mul b
  have hnum := ((t1.add t2).add t3).sub t4
  have hden := hP.mul hQ
  have h4 := hnum.div hden hne
  have hev : (fun x : ℝ =>
      (a * ((Real.sin (b*x) - b*x)/x^3) + a*b*((Real.cos (a*x) - 1)/x^2)
        + a*x^2*((Real.cos (a*x) - 1)/x^2)*((Real.sin (b*x) - b*x)/x^3)
        - b*((Real.sin (a*x) - a*x)/x^3))
        / ((a + x^2*((Real.sin (a*x) - a*x)/x^3)) * (b + x^2*((Real.sin (b*x) - b*x)/x^3))))
      =ᶠ[𝓝[≠] 0] (fun x : ℝ => a / (x * Real.tan (a*x)) - b / (x * Real.sin (b*x))) := by
    filter_upwards [hPev, hQev, self_mem_nhdsWithin] with x hPx hQx hx
    exact ex_eq_aux a b x hx hPx hQx
  have h5 := Filter.Tendsto.congr' hev h4
  convert h5 using 2
  field_simp <;> ring

theorem exam_answer (a : ℕ) (ha_lo : 2 ≤ a) (ha_hi : a ≤ 5) (b : ℕ) (hb_lo : 2 ≤ b) (hb_hi : b ≤ 5) :
    Filter.Tendsto (fun x : ℝ => (a:ℝ) / (x * Real.tan ((a:ℝ) * x)) - (b:ℝ) / (x * Real.sin ((b:ℝ) * x))) (𝓝[≠] 0) (𝓝 (((((-1 : ℝ) / 3) * ((a : ℝ) ^ (2 : ℕ))) + (((-1 : ℝ) / 6) * ((b : ℝ) ^ (2 : ℕ)))))) := by
  have ha' : (0:ℝ) < (a:ℝ) := by exact_mod_cast (by omega : 0 < a)
  have hb' : (0:ℝ) < (b:ℝ) := by exact_mod_cast (by omega : 0 < b)
  have h := ex_main (a:ℝ) (b:ℝ) ha' hb'
  convert h using 2 <;> (first | done | (push_cast; ring))

end Cand1
#print axioms Cand1.exam_answer

namespace Cand2
open Topology Filter Asymptotics
lemma aux_congr {f₁ f₂ g : ℝ → ℝ} (hf : ∀ x, f₁ x = f₂ x)
    (h : Asymptotics.IsLittleO (nhds (0:ℝ)) f₁ g) : Asymptotics.IsLittleO (nhds (0:ℝ)) f₂ g := by
  have e : f₁ = f₂ := funext hf
  subst e
  exact h

lemma aux_mul_o {F : ℝ → ℝ} {k m n : ℕ}
    (h : Asymptotics.IsLittleO (nhds (0:ℝ)) F (fun x : ℝ => x ^ m)) (hkmn : k + m = n) :
    Asymptotics.IsLittleO (nhds (0:ℝ)) (fun x : ℝ => x ^ k * F x) (fun x : ℝ => x ^ n) := by
  have h1 := (Asymptotics.isBigO_refl (fun x : ℝ => x ^ k) (nhds (0:ℝ))).mul_isLittleO h
  subst hkmn
  simpa only [pow_add] using h1

lemma aux_sin3 (c : ℝ) : Asymptotics.IsLittleO (nhds (0:ℝ))
    (fun x : ℝ => Real.sin (c * x) - (c * x - (c * x) ^ 3 / 6)) (fun x : ℝ => x ^ 3) := by
  have h := MathExam.sin_mul_maclaurin c 2
  have h2 := MathExam.isLittleO_pow_of_le (n := 3) h (by norm_num)
  refine aux_congr ?_ h2
  intro x
  simp only [Finset.sum_range_succ, Finset.sum_range_zero]
  norm_num [Nat.factorial]
  try ring

lemma aux_cos2 (c : ℝ) : Asymptotics.IsLittleO (nhds (0:ℝ))
    (fun x : ℝ => Real.cos (c * x) - (1 - (c * x) ^ 2 / 2)) (fun x : ℝ => x ^ 2) := by
  have h := MathExam.cos_mul_maclaurin c 1
  have h2 := MathExam.isLittleO_pow_of_le (n := 2) h (by norm_num)
  refine aux_congr ?_ h2
  intro x
  simp only [Finset.sum_range_succ, Finset.sum_range_zero]
  norm_num [Nat.factorial]
  try ring

lemma aux_sin1 (c : ℝ) : Asymptotics.IsLittleO (nhds (0:ℝ))
    (fun x : ℝ => Real.sin (c * x) - c * x) (fun x : ℝ => x ^ 1) := by
  have h := MathExam.sin_mul_maclaurin c 1
  have h2 := MathExam.isLittleO_pow_of_le (n := 1) h (by norm_num)
  refine aux_congr ?_ h2
  intro x
  simp only [Finset.sum_range_succ, Finset.sum_range_zero]
  norm_num [Nat.factorial]
  try ring

lemma aux_num_tan (c : ℝ) : Asymptotics.IsLittleO (nhds (0:ℝ))
    (fun x : ℝ => (c * x * Real.cos (c * x) - Real.sin (c * x)) - (-c ^ 3 / 3) * x ^ 3)
    (fun x : ℝ => x ^ 3) := by
  have h1 : Asymptotics.IsLittleO (nhds (0:ℝ))
      (fun x : ℝ => x ^ 1 * (Real.cos (c * x) - (1 - (c * x) ^ 2 / 2))) (fun x : ℝ => x ^ 3) :=
    aux_mul_o (aux_cos2 c) (by norm_num)
  have h2 := (h1.const_mul_left c).sub (aux_sin3 c)
  refine aux_congr ?_ h2
  intro x
  try dsimp only
  ring

lemma aux_num_sin (c : ℝ) : Asymptotics.IsLittleO (nhds (0:ℝ))
    (fun x : ℝ => (c * x - Real.sin (c * x)) - (c ^ 3 / 6) * x ^ 3) (fun x : ℝ => x ^ 3) := by
  have h2 := (aux_sin3 c).const_mul_left (-1)
  refine aux_congr ?_ h2
  intro x
  try dsimp only
  ring

lemma aux_den (c : ℝ) : Asymptotics.IsLittleO (nhds (0:ℝ))
    (fun x : ℝ => x ^ 2 * Real.sin (c * x) - c * x ^ 3) (fun x : ℝ => x ^ 3) := by
  have h1 : Asymptotics.IsLittleO (nhds (0:ℝ))
      (fun x : ℝ => x ^ 2 * (Real.sin (c * x) - c * x)) (fun x : ℝ => x ^ 3) :=
    aux_mul_o (aux_sin1 c) (by norm_num)
  refine aux_congr ?_ h1
  intro x
  try dsimp only
  ring

lemma aux_ev (c : ℝ) (hc : c ≠ 0) :
    ∀ᶠ x in nhdsWithin (0:ℝ) {0}ᶜ, x ≠ 0 ∧ Real.sin (c * x) ≠ 0 ∧ Real.cos (c * x) ≠ 0 := by
  have hcont : Continuous (fun x : ℝ => |c * x|) := by
    first
      | fun_prop
      | exact (continuous_const.mul continuous_id).abs
  have hopen : IsOpen {x : ℝ | |c * x| < Real.pi / 2} := isOpen_lt hcont continuous_const
  have h0 : (0:ℝ) ∈ {x : ℝ | |c * x| < Real.pi / 2} := by
    show |c * 0| < Real.pi / 2
    rw [mul_zero, abs_zero]
    have := Real.pi_pos
    linarith
  have h1 : ∀ᶠ x in nhds (0:ℝ), |c * x| < Real.pi / 2 := hopen.mem_nhds h0
  have h2 : ∀ᶠ x in nhdsWithin (0:ℝ) {0}ᶜ, |c * x| < Real.pi / 2 := by
    first
      | exact h1.filter_mono nhdsWithin_le_nhds
      | exact eventually_nhdsWithin_of_eventually_nhds h1
  have h3 : ∀ᶠ x in nhdsWithin (0:ℝ) {0}ᶜ, x ∈ ({0}ᶜ : Set ℝ) := by
    first
      | exact eventually_mem_nhdsWithin
      | exact self_mem_nhdsWithin
  filter_upwards [h2, h3] with x hx1 hx2
  have hx0 : x ≠ 0 := hx2
  have hcx : c * x ≠ 0 := mul_ne_zero hc hx0
  obtain ⟨hl1, hl2⟩ := abs_lt.mp hx1
  have hpi := Real.pi_pos
  refine ⟨hx0, ?_, ?_⟩
  · intro h
    have := (Real.sin_eq_zero_iff_of_lt_of_lt (by linarith) (by linarith)).mp h
    exact hcx this
  · exact (Real.cos_pos_of_mem_Ioo ⟨hl1, hl2⟩).ne'

lemma aux_tan_lim (c : ℝ) (hc : c ≠ 0) :
    Filter.Tendsto (fun x : ℝ => c / (x * Real.tan (c * x)) - 1 / x ^ 2)
      (nhdsWithin (0:ℝ) {0}ᶜ) (nhds (-c ^ 2 / 3)) := by
  have hmain := MathExam.tendsto_div_of_isLittleO
    (f := fun x : ℝ => c * x * Real.cos (c * x) - Real.sin (c * x))
    (g := fun x : ℝ => x ^ 2 * Real.sin (c * x))
    (a := -c ^ 3 / 3) (b := c) (n := 3) hc (aux_num_tan c) (aux_den c)
  have hv : (-c ^ 3 / 3) / c = -c ^ 2 / 3 := by
    rw [div_eq_iff hc]
    ring
  rw [hv] at hmain
  refine hmain.congr' ?_
  filter_upwards [aux_ev c hc] with x hx
  obtain ⟨hx0, hs, hco⟩ := hx
  show (c * x * Real.cos (c * x) - Real.sin (c * x)) / (x ^ 2 * Real.sin (c * x))
      = c / (x * Real.tan (c * x)) - 1 / x ^ 2
  rw [Real.tan_eq_sin_div_cos]
  field_simp
  try ring

lemma aux_sin_lim (c : ℝ) (hc : c ≠ 0) :
    Filter.Tendsto (fun x : ℝ => c / (x * Real.sin (c * x)) - 1 / x ^ 2)
      (nhdsWithin (0:ℝ) {0}ᶜ) (nhds (c ^ 2 / 6)) := by
  have hmain := MathExam.tendsto_div_of_isLittleO
    (f := fun x : ℝ => c * x - Real.sin (c * x))
    (g := fun x : ℝ => x ^ 2 * Real.sin (c * x))
    (a := c ^ 3 / 6) (b := c) (n := 3) hc (aux_num_sin c) (aux_den c)
  have hv : (c ^ 3 / 6) / c = c ^ 2 / 6 := by
    rw [div_eq_iff hc]
    ring
  rw [hv] at hmain
  refine hmain.congr' ?_
  filter_upwards [aux_ev c hc] with x hx
  obtain ⟨hx0, hs, hco⟩ := hx
  show (c * x - Real.sin (c * x)) / (x ^ 2 * Real.sin (c * x))
      = c / (x * Real.sin (c * x)) - 1 / x ^ 2
  field_simp
  try ring

theorem exam_answer (a : ℕ) (ha_lo : 2 ≤ a) (ha_hi : a ≤ 5) (b : ℕ) (hb_lo : 2 ≤ b) (hb_hi : b ≤ 5) :
    Filter.Tendsto (fun x : ℝ => (a:ℝ) / (x * Real.tan ((a:ℝ) * x)) - (b:ℝ) / (x * Real.sin ((b:ℝ) * x))) (𝓝[≠] (0:ℝ)) (𝓝 (((((-1 : ℝ) / 3) * ((a : ℝ) ^ (2 : ℕ))) + (((-1 : ℝ) / 6) * ((b : ℝ) ^ (2 : ℕ)))))) := by
  have ha2 : (2:ℝ) ≤ (a:ℝ) := by exact_mod_cast ha_lo
  have hb2 : (2:ℝ) ≤ (b:ℝ) := by exact_mod_cast hb_lo
  have ha0 : (a:ℝ) ≠ 0 := by
    have : (0:ℝ) < (a:ℝ) := by linarith
    exact this.ne'
  have hb0 : (b:ℝ) ≠ 0 := by
    have : (0:ℝ) < (b:ℝ) := by linarith
    exact this.ne'
  have h1 := aux_tan_lim (a:ℝ) ha0
  have h2 := aux_sin_lim (b:ℝ) hb0
  have h3 := h1.sub h2
  have h4 : Filter.Tendsto (fun x : ℝ => (a:ℝ) / (x * Real.tan ((a:ℝ) * x)) - (b:ℝ) / (x * Real.sin ((b:ℝ) * x))) (𝓝[≠] (0:ℝ)) (nhds (-(a:ℝ) ^ 2 / 3 - (b:ℝ) ^ 2 / 6)) := by
    refine h3.congr (fun x => ?_)
    try dsimp only
    ring
  convert h4 using 2
  all_goals (push_cast; ring)

end Cand2
#print axioms Cand2.exam_answer

