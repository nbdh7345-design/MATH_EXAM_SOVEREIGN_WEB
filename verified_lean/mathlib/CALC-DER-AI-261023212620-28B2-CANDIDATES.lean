-- CALC-DER-AI-261023212620-28B2: 3 ứng viên formalize, biên dịch chung một file.
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



theorem exam_answer (m : ℕ) (hm_lo : 2 ≤ m) (hm_hi : m ≤ 9) :
    (∃ A B : ℝ × ℝ, A.2 = 0 ∧ B.1 = 0 ∧
    A.2 = deriv (fun x : ℝ => x + (m:ℝ)/x) 1 * (A.1 - 1) + (fun x : ℝ => x + (m:ℝ)/x) 1 ∧
    B.2 = deriv (fun x : ℝ => x + (m:ℝ)/x) 1 * (B.1 - 1) + (fun x : ℝ => x + (m:ℝ)/x) 1) ∧
  ∀ A B : ℝ × ℝ, A.2 = 0 → B.1 = 0 →
    A.2 = deriv (fun x : ℝ => x + (m:ℝ)/x) 1 * (A.1 - 1) + (fun x : ℝ => x + (m:ℝ)/x) 1 →
    B.2 = deriv (fun x : ℝ => x + (m:ℝ)/x) 1 * (B.1 - 1) + (fun x : ℝ => x + (m:ℝ)/x) 1 →
    |A.1 * B.2 - A.2 * B.1| / 2 = (((2 : ℝ) * ((m : ℝ) ^ (2 : ℕ)) * ((((-1 : ℝ) + (m : ℝ)) ^ (1 : ℕ))⁻¹))) := by
  have hm2 : (m:ℝ) ≥ 2 := by exact_mod_cast hm_lo
  have hpos : (m:ℝ) - 1 > 0 := by linarith
  have hne : (m:ℝ) - 1 ≠ 0 := hpos.ne'
  have h := (hasDerivAt_id (1:ℝ)).add ((hasDerivAt_const (1:ℝ) (m:ℝ)).div (hasDerivAt_id (1:ℝ)) one_ne_zero)
  have e : deriv (fun x : ℝ => x + (m:ℝ)/x) 1 = 1 + (0 * 1 - (m:ℝ) * 1) / 1 ^ 2 := h.deriv
  have hd : deriv (fun x : ℝ => x + (m:ℝ)/x) 1 = 1 - (m:ℝ) := by
    rw [e]; ring
  have hq : 2 * (m:ℝ) / ((m:ℝ) - 1) * ((m:ℝ) - 1) = 2 * (m:ℝ) := div_mul_cancel₀ _ hne
  refine ⟨⟨(2 * (m:ℝ) / ((m:ℝ) - 1), 0), (0, 2 * (m:ℝ)), rfl, rfl, ?_, ?_⟩, ?_⟩
  · rw [hd]
    beta_reduce
    show (0:ℝ) = (1 - (m:ℝ)) * (2 * (m:ℝ) / ((m:ℝ) - 1) - 1) + (1 + (m:ℝ) / 1)
    linear_combination hq
  · rw [hd]
    beta_reduce
    show (2 * (m:ℝ)) = (1 - (m:ℝ)) * (0 - 1) + (1 + (m:ℝ) / 1)
    ring
  · intro A B hA2 hB1 hA hB
    rw [hd] at hA hB
    beta_reduce at hA hB
    have ha : A.1 = 2 * (m:ℝ) / ((m:ℝ) - 1) := by
      rw [eq_div_iff hne]
      linear_combination hA - hA2
    have hb : B.2 = 2 * (m:ℝ) := by
      rw [hB, hB1]; ring
    rw [hA2, hB1, hb, ha]
    have h0 : 0 ≤ (2 * (m:ℝ) / ((m:ℝ) - 1)) * (2 * (m:ℝ)) - 0 * 0 := by
      simp only [mul_zero, sub_zero]
      exact mul_nonneg (div_nonneg (by linarith) hpos.le) (by linarith)
    rw [abs_of_nonneg h0, eq_div_iff hne]
    linear_combination (m:ℝ) * hq

end Cand0
#print axioms Cand0.exam_answer

namespace Cand1



theorem exam_answer (m : ℕ) (hm_lo : 2 ≤ m) (hm_hi : m ≤ 9) :
    ∀ a b : ℝ,
    (0 : ℝ) = (fun x : ℝ => x + (m:ℝ)/x) 1 + deriv (fun x : ℝ => x + (m:ℝ)/x) 1 * (a - 1) →
    b = (fun x : ℝ => x + (m:ℝ)/x) 1 + deriv (fun x : ℝ => x + (m:ℝ)/x) 1 * (0 - 1) →
    (1/2 : ℝ) * |a| * |b| = (((2 : ℝ) * ((m : ℝ) ^ (2 : ℕ)) * ((((-1 : ℝ) + (m : ℝ)) ^ (1 : ℕ))⁻¹))) := by
  have hd : HasDerivAt (fun x : ℝ => x + (m:ℝ)/x) (1 - (m:ℝ)) 1 := by
    have h := ((hasDerivAt_id (1:ℝ)).add ((hasDerivAt_const (1:ℝ) (m:ℝ)).div (hasDerivAt_id (1:ℝ)) one_ne_zero))
    convert h using 1 <;> simp <;> ring
  intro a b ha hb
  simp only [hd.deriv] at ha hb
  have hm : (2:ℝ) ≤ (m:ℝ) := by exact_mod_cast hm_lo
  have hpos : 0 < (m:ℝ) - 1 := by linarith
  have hm1 : (m:ℝ) - 1 ≠ 0 := hpos.ne'
  have ha2 : a = 2 * (m:ℝ) / ((m:ℝ) - 1) := by
    rw [eq_div_iff hm1]
    simp only [div_one] at ha
    nlinarith
  have hb2 : b = 2 * (m:ℝ) := by
    simp only [div_one] at hb
    nlinarith
  subst ha2
  subst hb2
  have h1 : 0 < 2 * (m:ℝ) / ((m:ℝ) - 1) := div_pos (by linarith) hpos
  rw [abs_of_pos h1, abs_of_pos (by linarith : (0:ℝ) < 2 * (m:ℝ))]
  field_simp <;> ring

end Cand1
#print axioms Cand1.exam_answer

namespace Cand2



theorem exam_answer (m : ℕ) (hm_lo : 2 ≤ m) (hm_hi : m ≤ 9) :
    ∀ A B : ℝ × ℝ, A.2 = 0 → B.1 = 0 →
  A.2 = (fun x : ℝ => x + (m:ℝ)/x) 1 + deriv (fun x : ℝ => x + (m:ℝ)/x) 1 * (A.1 - 1) →
  B.2 = (fun x : ℝ => x + (m:ℝ)/x) 1 + deriv (fun x : ℝ => x + (m:ℝ)/x) 1 * (B.1 - 1) →
  |A.1 * B.2| / 2 = (((2 : ℝ) * ((m : ℝ) ^ (2 : ℕ)) * ((((-1 : ℝ) + (m : ℝ)) ^ (1 : ℕ))⁻¹))) := by
  have hm : (2:ℝ) ≤ (m:ℝ) := by exact_mod_cast hm_lo
  have hm1 : 0 < (m:ℝ) - 1 := by linarith
  have h1 : HasDerivAt (fun x : ℝ => (m:ℝ)/x) (((0:ℝ) * 1 - (m:ℝ) * 1)/1^2) 1 :=
    (hasDerivAt_const (1:ℝ) (m:ℝ)).div (hasDerivAt_id' 1) one_ne_zero
  have hd : HasDerivAt (fun x : ℝ => x + (m:ℝ)/x) (1 + ((0:ℝ) * 1 - (m:ℝ) * 1)/1^2) 1 :=
    (hasDerivAt_id' 1).add h1
  intro A B hA hB hAe hBe
  rw [hd.deriv] at hAe hBe
  have hB2 : B.2 = 2 * (m:ℝ) := by
    rw [hB] at hBe
    simp only at hBe
    linarith
  have hA1 : A.1 = 2 * (m:ℝ) / ((m:ℝ) - 1) := by
    rw [eq_div_iff (ne_of_gt hm1)]
    rw [hA] at hAe
    simp only at hAe
    nlinarith
  rw [hA1, hB2]
  rw [abs_of_pos (mul_pos (div_pos (by linarith) hm1) (by linarith))]
  first | (field_simp; ring) | field_simp

end Cand2
#print axioms Cand2.exam_answer

