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

open Set Filter Topology

-- Rudin 5.2: f⁻¹ trong Mathlib là hàm 1/f (nghịch đảo từng điểm), không phải hàm ngược
theorem neg_5_2 : ¬ ∀ (a b : ℝ) (f g : ℝ → ℝ), (∀ x ∈ Set.Ioo a b, deriv f x > 0) → g = f⁻¹ →
    (StrictMonoOn f (Set.Ioo a b) ∧ DifferentiableOn ℝ g (Set.Ioo a b) ∧
     ∀ x ∈ Set.Ioo a b, deriv g (f x) = 1 / deriv f x) := by
  intro H
  have h := (H (-1) 1 id id⁻¹ (by intro x _; simp) rfl).2.1
  have h0 : DifferentiableAt ℝ (fun x : ℝ => x⁻¹) 0 :=
    (h 0 (by norm_num)).differentiableAt (Ioo_mem_nhds (by norm_num) (by norm_num))
  exact (differentiableAt_inv_iff.mp h0) rfl

-- Rudin 4.8b: hàm liên tục đều trên tập bị chặn của ℝ thì bị chặn trên tập đó
theorem neg_4_8b : ¬ ∀ (E : Set ℝ), Bornology.IsBounded E →
    ∃ f : ℝ → ℝ, UniformContinuousOn f E ∧ ¬ Bornology.IsBounded (Set.image f E) := by
  intro H
  obtain ⟨f, hf, hnb⟩ := H (Set.Icc 0 1) (Metric.isBounded_Icc 0 1)
  have hr : UniformContinuous ((Set.Icc (0:ℝ) 1).restrict f) := uniformContinuousOn_iff_restrict.mp hf
  have : CompactSpace (Set.Icc (0:ℝ) 1) := isCompact_iff_compactSpace.mp isCompact_Icc
  have tb := (isCompact_univ (X := Set.Icc (0:ℝ) 1)).totallyBounded.image hr
  rw [Set.image_univ] at tb
  exact hnb (by rw [Set.image_eq_range]; exact tb.isBounded)

-- Rudin 5.15: sSup của tập không bị chặn trong ℝ bằng 0 (quy ước của Mathlib); f = id trên (0, ∞)
theorem neg_5_15 : ¬ ∀ (f : ℝ → ℝ) (a M0 M1 M2 : ℝ), DifferentiableOn ℝ f (Set.Ioi a) →
    DifferentiableOn ℝ (deriv f) (Set.Ioi a) →
    M0 = sSup {(|f x|) | x ∈ (Set.Ioi a)} → M1 = sSup {(|deriv f x|) | x ∈ (Set.Ioi a)} →
    M2 = sSup {(|deriv (deriv f) x|) | x ∈ (Set.Ioi a)} → (M1 ^ 2) ≤ 4 * M0 * M2 := by
  intro H
  have e0 : {y | ∃ x ∈ Set.Ioi (0:ℝ), |id x| = y} = Set.Ioi 0 := by
    ext y; constructor
    · rintro ⟨x, hx, rfl⟩; simpa [abs_of_pos (show (0:ℝ) < x from hx)] using hx
    · intro hy; exact ⟨y, hy, by simp [abs_of_pos (show (0:ℝ) < y from hy)]⟩
  have e1 : {y | ∃ x ∈ Set.Ioi (0:ℝ), |deriv id x| = y} = {1} := by
    ext y; simp only [deriv_id, abs_one, Set.mem_setOf_eq, Set.mem_singleton_iff]
    exact ⟨fun ⟨_, _, h⟩ => h.symm, fun h => ⟨1, by norm_num, h.symm⟩⟩
  have e2 : {y | ∃ x ∈ Set.Ioi (0:ℝ), |deriv (deriv id) x| = y} = {0} := by
    ext y
    have : deriv (deriv (id : ℝ → ℝ)) = fun _ => 0 := by
      funext x; simp [show deriv (id : ℝ → ℝ) = fun _ => 1 from funext deriv_id]
    simp only [this, abs_zero, Set.mem_setOf_eq, Set.mem_singleton_iff]
    exact ⟨fun ⟨_, _, h⟩ => h.symm, fun h => ⟨1, by norm_num, h.symm⟩⟩
  have h := H id 0 0 1 0 differentiableOn_id
    (by simpa [show deriv (id : ℝ → ℝ) = fun _ => 1 from funext deriv_id] using differentiableOn_const 1)
    (by rw [show {(|id x|) | x ∈ Set.Ioi (0:ℝ)} = {y | ∃ x ∈ Set.Ioi (0:ℝ), |id x| = y} from rfl, e0]
        exact (Real.sSup_of_not_bddAbove (not_bddAbove_Ioi (0:ℝ))).symm)
    (by rw [show {(|deriv id x|) | x ∈ Set.Ioi (0:ℝ)} = {y | ∃ x ∈ Set.Ioi (0:ℝ), |deriv id x| = y} from rfl, e1]
        simp)
    (by rw [show {(|deriv (deriv id) x|) | x ∈ Set.Ioi (0:ℝ)} = {y | ∃ x ∈ Set.Ioi (0:ℝ), |deriv (deriv id) x| = y} from rfl, e2]
        simp)
  norm_num at h

-- Rudin 4.19: giả thiết giá trị trung gian chỉ viết cho trường hợp f a < c < f b với a < b; hàm giảm ngặt có bước
-- nhảy thỏa giả thiết một cách rỗng, mọi tập mức có tối đa một điểm (đóng), nhưng không liên tục tại 0
noncomputable def fj (x : ℝ) : ℝ := if x < 0 then -x else -x - 1

theorem fj_anti : StrictAnti fj := by
  intro a b hab
  unfold fj
  split_ifs <;> linarith

theorem neg_4_19 : ¬ ∀ (f : ℝ → ℝ), (∀ a b c, a < b → f a < c → c < f b → ∃ x, a < x ∧ x < b ∧ f x = c) →
    (∀ r : ℚ, IsClosed {x | f x = r}) → Continuous f := by
  intro H
  have hc := H fj (fun a b c hab h1 h2 => absurd (h1.trans h2) (not_lt.mpr (fj_anti hab).le))
    (fun r => (show Set.Subsingleton {x | fj x = (r : ℝ)} from
      fun x hx y hy => fj_anti.injective (hx.trans hy.symm)).isClosed)
  have ivt := intermediate_value_Icc' (show (-1:ℝ) ≤ 0 by norm_num) hc.continuousOn
  have hm : (-1/2 : ℝ) ∈ Set.Icc (fj 0) (fj (-1)) := by
    unfold fj; constructor <;> norm_num
  obtain ⟨x, ⟨hx1, hx2⟩, hx⟩ := ivt hm
  unfold fj at hx
  by_cases h : x < 0
  · rw [if_pos h] at hx; linarith
  · rw [if_neg h] at hx; push_neg at h; linarith

#print axioms neg_4_19
#print axioms neg_5_2
#print axioms neg_4_8b
#print axioms neg_5_15
