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
import MathExam

namespace PNREF0
open Filter Real Function
open scoped Topology

theorem exercise_3_4 (n : ℕ) :
    Tendsto (λ n => (sqrt (n + 1) - sqrt n)) atTop (𝓝 0) := by
  sorry
end PNREF0

namespace PNREF1
open scoped BigOperators

theorem exercise_1998_a3 (f : ℝ → ℝ) (hf : ContDiff ℝ 3 f) :
    ∃ a : ℝ, (f a) * (deriv f a) * (iteratedDeriv 2 f a) * (iteratedDeriv 3 f a) ≥ 0 := by
  sorry
end PNREF1

namespace PNREF2
open Topology Filter Real Complex TopologicalSpace Finset
open scoped BigOperators

theorem exercise_3_1a (f : ℕ → ℝ)
  (h : ∃ (a : ℝ), Tendsto (λ (n : ℕ) => f n) atTop (𝓝 a)) :
    ∃ (a : ℝ), Tendsto (λ (n : ℕ) => |f n|) atTop (𝓝 a) := by
  sorry
end PNREF2

namespace PNREF3
open Topology Filter Real Complex TopologicalSpace Finset
open scoped BigOperators
noncomputable def f : ℕ → ℝ
| 0 => sqrt 2
| (n + 1) => sqrt (2 + sqrt (f n))
theorem exercise_3_3  :
    ∃ (x : ℝ), Tendsto f atTop (𝓝 x) ∧ ∀ n, f n < 2 := by
  sorry
end PNREF3

namespace PNREF4
open Topology Filter Real Complex TopologicalSpace Finset
open scoped BigOperators

theorem exercise_4_19 {f : ℝ → ℝ} (hf : ∀ a b c, a < b → f a < c → c < f b → ∃ x, a < x ∧ x < b ∧ f x = c)
  (hg : ∀ r : ℚ, IsClosed {x | f x = r}) :
    Continuous f := by
  sorry
end PNREF4

namespace PNREF5
open Topology Filter Real Complex TopologicalSpace Finset
open scoped BigOperators

theorem exercise_4_24 {f : ℝ → ℝ}
  (hf : Continuous f) (a b : ℝ) (hab : a < b)
  (h : ∀ x y : ℝ, a < x → x < b → a < y → y < b → f ((x + y) / 2) ≤ (f x + f y) / 2) :
    ConvexOn ℝ (Set.Ioo a b) f := by
  sorry
end PNREF5

namespace PNREF6
open Topology Filter Real Complex TopologicalSpace Finset
open scoped BigOperators

theorem exercise_5_2 {a b : ℝ}
  {f g : ℝ → ℝ} (hf : ∀ x ∈ Set.Ioo a b, deriv f x > 0)
  (hg : g = f⁻¹) :
    StrictMonoOn f (Set.Ioo a b) ∧
  DifferentiableOn ℝ g (Set.Ioo a b) ∧
  ∀ x ∈ Set.Ioo a b, deriv g (f x) = 1 / deriv f x := by
  sorry
end PNREF6

namespace PNREF7
open Topology Filter Real Complex TopologicalSpace Finset
open scoped BigOperators

theorem exercise_5_4 {n : ℕ}
  (C : ℕ → ℝ)
  (hC : ∑ i ∈ (range (n + 1)), (C i) / (i + 1) = 0) :
    ∃ x, x ∈ (Set.Icc (0 : ℝ) 1) ∧ ∑ i ∈ range (n + 1), (C i) * (x^i) = 0 := by
  sorry
end PNREF7

namespace PNREF8
open Topology Filter Real Complex TopologicalSpace Finset
open scoped BigOperators

theorem exercise_5_6 {f : ℝ → ℝ}
  (hf1 : ContinuousOn f (Set.Ici 0))
  (hf2 : DifferentiableOn ℝ f (Set.Ioi 0))
  (hf3 : f 0 = 0)
  (hf4 : MonotoneOn (deriv f) (Set.Ioi 0)) :
    MonotoneOn (λ x => f x / x) (Set.Ioi 0) := by
  sorry
end PNREF8

namespace PNREF9
open Topology Filter Real Complex TopologicalSpace Finset
open scoped BigOperators

theorem exercise_5_15 {f : ℝ → ℝ} (a M0 M1 M2 : ℝ)
  (hf' : DifferentiableOn ℝ f (Set.Ioi a))
  (hf'' : DifferentiableOn ℝ (deriv f) (Set.Ioi a))
  (hM0 : M0 = sSup {(|f x|) | x ∈ (Set.Ioi a)})
  (hM1 : M1 = sSup {(|deriv f x|) | x ∈ (Set.Ioi a)})
  (hM2 : M2 = sSup {(|deriv (deriv f) x|) | x ∈ (Set.Ioi a)}) :
    (M1 ^ 2) ≤ 4 * M0 * M2 := by
  sorry
end PNREF9

namespace PNREF10
open Filter Real Function
open scoped Topology

theorem exercise_3_1 {f : ℝ → ℝ}
  (hf : ∀ x y, |f x - f y| ≤ |x - y| ^ 2) :
    ∃ c, f = λ x => c := by
  sorry
end PNREF10

namespace PNREF11
open scoped BigOperators

theorem exercise_1999_b4 (f : ℝ → ℝ) (hf: ContDiff ℝ 3 f)
  (hf1 : ∀ n ≤ 3, ∀ x : ℝ, iteratedDeriv n f x > 0)
  (hf2 : ∀ x : ℝ, iteratedDeriv 3 f x ≤ f x) :
    ∀ x : ℝ, deriv f x < 2 * f x := by
  sorry
end PNREF11

namespace PNREF12
open scoped BigOperators

theorem exercise_2018_a5 (f : ℝ → ℝ) (hf : ContDiff ℝ ⊤ f)
  (hf0 : f 0 = 0) (hf1 : f 1 = 1) (hf2 : ∀ x, f x ≥ 0) :
    ∃ (n : ℕ+) (x : ℝ), iteratedDeriv n f x < 0 := by
  sorry
end PNREF12

namespace PNREF13
open Topology Filter Real Complex TopologicalSpace Finset
open scoped BigOperators

theorem exercise_3_2a  :
    Tendsto (λ (n : ℝ) => (sqrt (n^2 + n) - n)) atTop (𝓝 (1/2)) := by
  sorry
end PNREF13

namespace PNREF14
open Topology Filter Real Complex TopologicalSpace Finset
open scoped BigOperators

theorem exercise_4_1a  :
    ∃ (f : ℝ → ℝ), (∀ (x : ℝ), Tendsto (λ y => f (x + y) - f (x - y)) (𝓝 0) (𝓝 0)) ∧ ¬ Continuous f := by
  sorry
end PNREF14

namespace PNREF15
open Topology Filter Real Complex TopologicalSpace Finset
open scoped BigOperators

theorem exercise_5_1 {f : ℝ → ℝ} (hf : ∀ x y : ℝ, |(f x - f y)| ≤ (x - y) ^ 2) :
    ∃ c, f = λ x => c := by
  sorry
end PNREF15

namespace PNREF16
open Topology Filter Real Complex TopologicalSpace Finset
open scoped BigOperators

theorem exercise_5_3 {g : ℝ → ℝ} (hg : Continuous g)
  (hg' : ∃ M : ℝ, ∀ x : ℝ, |deriv g x| ≤ M) :
    ∃ N, ∀ ε > 0, ε < N → Function.Injective (λ x : ℝ => x + ε * g x) := by
  sorry
end PNREF16

namespace PNREF17
open Topology Filter Real Complex TopologicalSpace Finset Set
open scoped BigOperators

theorem exercise_5_5 {f : ℝ → ℝ}
  (hfd : DifferentiableOn ℝ f (Ioi 0))
  (hf : Tendsto (deriv f) atTop (𝓝 0)) :
    Tendsto (λ x => f (x + 1) - f x) atTop (𝓝 0) := by
  sorry
end PNREF17

namespace PNREF18
open Topology Filter Real Complex TopologicalSpace Finset
open scoped BigOperators

theorem exercise_5_7 {f g : ℝ → ℝ} {x : ℝ}
  (hf' : DifferentiableAt ℝ f x)
  (hg' : DifferentiableAt ℝ g x)
  (hg'_ne_0 : deriv g x ≠ 0)
  (f0 : f x = 0) (g0 : g x = 0) :
    Tendsto (λ t => f t / g t) (𝓝 x) (𝓝 (deriv f x / deriv g x)) := by
  sorry
end PNREF18

namespace PNREF19
open Topology Filter Real Complex TopologicalSpace Finset
open scoped BigOperators

theorem exercise_5_17 {f : ℝ → ℝ}
  (hf' : DifferentiableOn ℝ f (Set.Icc (-1) 1))
  (hf'' : DifferentiableOn ℝ (deriv f) (Set.Icc (-1) 1))
  (hf''' : DifferentiableOn ℝ (deriv (deriv f)) (Set.Icc (-1) 1))
  (hf0 : f (-1) = 0)
  (hf1 : f 0 = 0)
  (hf2 : f 1 = 1)
  (hf3 : deriv f 0 = 0) :
    ∃ x, x ∈ Set.Ioo (-1 : ℝ) 1 ∧ deriv (deriv (deriv f)) x ≥ 3 := by
  sorry
end PNREF19

namespace PNREF20
open Filter Real Function
open scoped Topology

theorem exercise_2_12a {α : Type*} [TopologicalSpace α]
  (f : ℕ → ℕ) (p : ℕ → α) (a : α)
  (hf : Injective f) (hp : Tendsto p atTop (𝓝 a)) :
    Tendsto (λ n => p (f n)) atTop (𝓝 a) := by
  sorry
end PNREF20

namespace PNREF21
open Topology Filter Real Complex TopologicalSpace Finset
open scoped BigOperators

theorem exercise_1_5 (A minus_A : Set ℝ) (hA : A.Nonempty)
  (hA_bdd_below : BddBelow A) (hminus_A : minus_A = {x | -x ∈ A}) :
    sInf A = - sSup minus_A := by
  sorry
end PNREF21

namespace PNREF22
open Topology Filter Real Complex TopologicalSpace Finset
open scoped BigOperators
noncomputable def g (n : ℕ) : ℝ := sqrt (n + 1) - sqrt n
theorem exercise_3_6a  :
    Tendsto (λ (n : ℕ) => (∑ i ∈ range n, g i)) atTop atTop := by
  sorry
end PNREF22

namespace PNREF23
open Topology Filter Real Complex TopologicalSpace Finset
open scoped BigOperators

theorem exercise_4_8b (E : Set ℝ) (h : Bornology.IsBounded E) :
    ∃ f : ℝ → ℝ, UniformContinuousOn f E ∧ ¬ Bornology.IsBounded (Set.image f E) := by
  sorry
end PNREF23

namespace PNREF24
open Filter Real Function Set
open scoped Topology

theorem exercise_4_15a (a b : ℝ) (hab : a ≤ b) (f : Icc a b → ℝ) :
    UniformContinuous f ↔ ∃ (μ : ℝ → ℝ), ∀ (x : ℝ), (x > 0 → μ x > 0) ∧
  StrictMonoOn μ (Ioi 0) ∧ Tendsto μ (𝓝 0) (𝓝 0) ∧
  (∀ s t : Icc a b, |f s - f t| ≤ μ (|s - t|)) := by
  sorry
end PNREF24

namespace PNREF25
open Topology Filter Real Complex TopologicalSpace Finset
open scoped BigOperators

theorem exercise_3_5 (a b : ℕ → EReal)
    (hareal : ∀ n, a n ≠ ⊤ ∧ a n ≠ ⊥)
    (hbreal : ∀ n, b n ≠ ⊤ ∧ b n ≠ ⊥)
    (ha : limsup a ≠ ⊤)
    (hb : limsup b ≠ ⊥) :
    limsup (λ n => a n + b n) ≤ limsup a + limsup b := by
  sorry
end PNREF25

namespace PNREF26
open Topology Filter Real Complex TopologicalSpace Finset
open scoped BigOperators

theorem exercise_4_8a (E : Set ℝ) (f : ℝ → ℝ) (hf : UniformContinuousOn f E)
  (hE : Bornology.IsBounded E) :
    Bornology.IsBounded (Set.image f E) := by
  sorry
end PNREF26

