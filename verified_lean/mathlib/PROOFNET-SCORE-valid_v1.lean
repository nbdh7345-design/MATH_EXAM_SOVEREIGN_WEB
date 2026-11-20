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

namespace PNEQ0
open Filter Real Function
open scoped Topology
open Filter Topology


theorem gen_to_ref (h_gen : Filter.Tendsto (fun n : ℕ => Real.sqrt ((n : ℝ) + 1) - Real.sqrt (n : ℝ)) Filter.atTop (𝓝 (0 : ℝ))) (n : ℕ) :
    Tendsto (λ n => (sqrt (n + 1) - sqrt n)) atTop (𝓝 0) := by
  first
    | exact h_gen
    | (intros; apply h_gen <;> first | assumption | exact default | (simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done) | fun_prop | aesop)
    | (simpa [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective] using h_gen)
    | (simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done)
    | (intros; simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done)
    | tauto
    | aesop
    | (convert h_gen using 1 <;> first | rfl | (simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done) | aesop)
    | (convert h_gen using 2 <;> first | rfl | (simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done) | aesop)
    | (convert h_gen using 3 <;> first | rfl | (simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done) | aesop)

theorem ref_to_gen (h_ref : ∀ (n : ℕ), Tendsto (λ n => (sqrt (n + 1) - sqrt n)) atTop (𝓝 0)) :
    Filter.Tendsto (fun n : ℕ => Real.sqrt ((n : ℝ) + 1) - Real.sqrt (n : ℝ)) Filter.atTop (𝓝 (0 : ℝ)) := by
  first
    | exact h_ref
    | (intros; apply h_ref <;> first | assumption | exact default | (simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done) | fun_prop | aesop)
    | (simpa [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective] using h_ref)
    | (simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done)
    | (intros; simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done)
    | tauto
    | aesop
    | (convert h_ref using 1 <;> first | rfl | (simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done) | aesop)
    | (convert h_ref using 2 <;> first | rfl | (simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done) | aesop)
    | (convert h_ref using 3 <;> first | rfl | (simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done) | aesop)

#print axioms gen_to_ref
#print axioms ref_to_gen
end PNEQ0

namespace PNEQ1
open Filter Real Function
open scoped Topology
open Filter Topology


theorem gen_to_ref (h_gen : Filter.Tendsto (fun n : ℕ => Real.sqrt ((n : ℝ) + 1) - Real.sqrt (n : ℝ)) Filter.atTop (𝓝 (0 : ℝ))) (n : ℕ) :
    Tendsto (λ n => (sqrt (n + 1) - sqrt n)) atTop (𝓝 0) := by
  first
    | exact h_gen
    | (intros; apply h_gen <;> first | assumption | exact default | (simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done) | fun_prop | aesop)
    | (simpa [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective] using h_gen)
    | (simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done)
    | (intros; simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done)
    | tauto
    | aesop
    | (convert h_gen using 1 <;> first | rfl | (simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done) | aesop)
    | (convert h_gen using 2 <;> first | rfl | (simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done) | aesop)
    | (convert h_gen using 3 <;> first | rfl | (simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done) | aesop)

theorem ref_to_gen (h_ref : ∀ (n : ℕ), Tendsto (λ n => (sqrt (n + 1) - sqrt n)) atTop (𝓝 0)) :
    Filter.Tendsto (fun n : ℕ => Real.sqrt ((n : ℝ) + 1) - Real.sqrt (n : ℝ)) Filter.atTop (𝓝 (0 : ℝ)) := by
  first
    | exact h_ref
    | (intros; apply h_ref <;> first | assumption | exact default | (simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done) | fun_prop | aesop)
    | (simpa [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective] using h_ref)
    | (simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done)
    | (intros; simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done)
    | tauto
    | aesop
    | (convert h_ref using 1 <;> first | rfl | (simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done) | aesop)
    | (convert h_ref using 2 <;> first | rfl | (simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done) | aesop)
    | (convert h_ref using 3 <;> first | rfl | (simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done) | aesop)

#print axioms gen_to_ref
#print axioms ref_to_gen
end PNEQ1

namespace PNEQ2
open scoped BigOperators



theorem gen_to_ref (h_gen : ∀ f : ℝ → ℝ, ContDiff ℝ 3 f → ∃ a : ℝ, 0 ≤ f a * deriv f a * iteratedDeriv 2 f a * iteratedDeriv 3 f a) (f : ℝ → ℝ) (hf : ContDiff ℝ 3 f) :
    ∃ a : ℝ, (f a) * (deriv f a) * (iteratedDeriv 2 f a) * (iteratedDeriv 3 f a) ≥ 0 := by
  first
    | exact h_gen
    | (intros; apply h_gen <;> first | assumption | exact default | (simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done) | fun_prop | aesop)
    | (simpa [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective] using h_gen)
    | (simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done)
    | (intros; simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done)
    | tauto
    | aesop
    | (convert h_gen using 1 <;> first | rfl | (simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done) | aesop)
    | (convert h_gen using 2 <;> first | rfl | (simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done) | aesop)
    | (convert h_gen using 3 <;> first | rfl | (simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done) | aesop)

theorem ref_to_gen (h_ref : ∀ (f : ℝ → ℝ) (hf : ContDiff ℝ 3 f), ∃ a : ℝ, (f a) * (deriv f a) * (iteratedDeriv 2 f a) * (iteratedDeriv 3 f a) ≥ 0) :
    ∀ f : ℝ → ℝ, ContDiff ℝ 3 f → ∃ a : ℝ, 0 ≤ f a * deriv f a * iteratedDeriv 2 f a * iteratedDeriv 3 f a := by
  first
    | exact h_ref
    | (intros; apply h_ref <;> first | assumption | exact default | (simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done) | fun_prop | aesop)
    | (simpa [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective] using h_ref)
    | (simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done)
    | (intros; simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done)
    | tauto
    | aesop
    | (convert h_ref using 1 <;> first | rfl | (simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done) | aesop)
    | (convert h_ref using 2 <;> first | rfl | (simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done) | aesop)
    | (convert h_ref using 3 <;> first | rfl | (simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done) | aesop)

#print axioms gen_to_ref
#print axioms ref_to_gen
end PNEQ2

namespace PNEQ3
open scoped BigOperators



theorem gen_to_ref (h_gen : ∀ f : ℝ → ℝ, ContDiff ℝ 3 f → ∃ a : ℝ, 0 ≤ f a * deriv f a * iteratedDeriv 2 f a * iteratedDeriv 3 f a) (f : ℝ → ℝ) (hf : ContDiff ℝ 3 f) :
    ∃ a : ℝ, (f a) * (deriv f a) * (iteratedDeriv 2 f a) * (iteratedDeriv 3 f a) ≥ 0 := by
  first
    | exact h_gen
    | (intros; apply h_gen <;> first | assumption | exact default | (simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done) | fun_prop | aesop)
    | (simpa [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective] using h_gen)
    | (simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done)
    | (intros; simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done)
    | tauto
    | aesop
    | (convert h_gen using 1 <;> first | rfl | (simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done) | aesop)
    | (convert h_gen using 2 <;> first | rfl | (simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done) | aesop)
    | (convert h_gen using 3 <;> first | rfl | (simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done) | aesop)

theorem ref_to_gen (h_ref : ∀ (f : ℝ → ℝ) (hf : ContDiff ℝ 3 f), ∃ a : ℝ, (f a) * (deriv f a) * (iteratedDeriv 2 f a) * (iteratedDeriv 3 f a) ≥ 0) :
    ∀ f : ℝ → ℝ, ContDiff ℝ 3 f → ∃ a : ℝ, 0 ≤ f a * deriv f a * iteratedDeriv 2 f a * iteratedDeriv 3 f a := by
  first
    | exact h_ref
    | (intros; apply h_ref <;> first | assumption | exact default | (simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done) | fun_prop | aesop)
    | (simpa [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective] using h_ref)
    | (simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done)
    | (intros; simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done)
    | tauto
    | aesop
    | (convert h_ref using 1 <;> first | rfl | (simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done) | aesop)
    | (convert h_ref using 2 <;> first | rfl | (simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done) | aesop)
    | (convert h_ref using 3 <;> first | rfl | (simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done) | aesop)

#print axioms gen_to_ref
#print axioms ref_to_gen
end PNEQ3

namespace PNEQ4
open Topology Filter Real Complex TopologicalSpace Finset
open scoped BigOperators
open Filter Topology


theorem gen_to_ref (h_gen : ∀ s : ℕ → ℝ, (∃ L : ℝ, Filter.Tendsto (fun n : ℕ => s n) Filter.atTop (𝓝 L)) → ∃ M : ℝ, Filter.Tendsto (fun n : ℕ => |s n|) Filter.atTop (𝓝 M)) (f : ℕ → ℝ)
  (h : ∃ (a : ℝ), Tendsto (λ (n : ℕ) => f n) atTop (𝓝 a)) :
    ∃ (a : ℝ), Tendsto (λ (n : ℕ) => |f n|) atTop (𝓝 a) := by
  first
    | exact h_gen
    | (intros; apply h_gen <;> first | assumption | exact default | (simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done) | fun_prop | aesop)
    | (simpa [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective] using h_gen)
    | (simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done)
    | (intros; simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done)
    | tauto
    | aesop
    | (convert h_gen using 1 <;> first | rfl | (simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done) | aesop)
    | (convert h_gen using 2 <;> first | rfl | (simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done) | aesop)
    | (convert h_gen using 3 <;> first | rfl | (simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done) | aesop)

theorem ref_to_gen (h_ref : ∀ (f : ℕ → ℝ)
  (h : ∃ (a : ℝ), Tendsto (λ (n : ℕ) => f n) atTop (𝓝 a)), ∃ (a : ℝ), Tendsto (λ (n : ℕ) => |f n|) atTop (𝓝 a)) :
    ∀ s : ℕ → ℝ, (∃ L : ℝ, Filter.Tendsto (fun n : ℕ => s n) Filter.atTop (𝓝 L)) → ∃ M : ℝ, Filter.Tendsto (fun n : ℕ => |s n|) Filter.atTop (𝓝 M) := by
  first
    | exact h_ref
    | (intros; apply h_ref <;> first | assumption | exact default | (simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done) | fun_prop | aesop)
    | (simpa [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective] using h_ref)
    | (simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done)
    | (intros; simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done)
    | tauto
    | aesop
    | (convert h_ref using 1 <;> first | rfl | (simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done) | aesop)
    | (convert h_ref using 2 <;> first | rfl | (simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done) | aesop)
    | (convert h_ref using 3 <;> first | rfl | (simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done) | aesop)

#print axioms gen_to_ref
#print axioms ref_to_gen
end PNEQ4

namespace PNEQ5
open Topology Filter Real Complex TopologicalSpace Finset
open scoped BigOperators
open Filter Topology


theorem gen_to_ref (h_gen : ∀ s : ℕ → ℝ, (∃ L : ℝ, Filter.Tendsto (fun n : ℕ => s n) Filter.atTop (𝓝 L)) → ∃ M : ℝ, Filter.Tendsto (fun n : ℕ => |s n|) Filter.atTop (𝓝 M)) (f : ℕ → ℝ)
  (h : ∃ (a : ℝ), Tendsto (λ (n : ℕ) => f n) atTop (𝓝 a)) :
    ∃ (a : ℝ), Tendsto (λ (n : ℕ) => |f n|) atTop (𝓝 a) := by
  first
    | exact h_gen
    | (intros; apply h_gen <;> first | assumption | exact default | (simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done) | fun_prop | aesop)
    | (simpa [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective] using h_gen)
    | (simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done)
    | (intros; simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done)
    | tauto
    | aesop
    | (convert h_gen using 1 <;> first | rfl | (simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done) | aesop)
    | (convert h_gen using 2 <;> first | rfl | (simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done) | aesop)
    | (convert h_gen using 3 <;> first | rfl | (simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done) | aesop)

theorem ref_to_gen (h_ref : ∀ (f : ℕ → ℝ)
  (h : ∃ (a : ℝ), Tendsto (λ (n : ℕ) => f n) atTop (𝓝 a)), ∃ (a : ℝ), Tendsto (λ (n : ℕ) => |f n|) atTop (𝓝 a)) :
    ∀ s : ℕ → ℝ, (∃ L : ℝ, Filter.Tendsto (fun n : ℕ => s n) Filter.atTop (𝓝 L)) → ∃ M : ℝ, Filter.Tendsto (fun n : ℕ => |s n|) Filter.atTop (𝓝 M) := by
  first
    | exact h_ref
    | (intros; apply h_ref <;> first | assumption | exact default | (simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done) | fun_prop | aesop)
    | (simpa [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective] using h_ref)
    | (simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done)
    | (intros; simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done)
    | tauto
    | aesop
    | (convert h_ref using 1 <;> first | rfl | (simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done) | aesop)
    | (convert h_ref using 2 <;> first | rfl | (simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done) | aesop)
    | (convert h_ref using 3 <;> first | rfl | (simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done) | aesop)

#print axioms gen_to_ref
#print axioms ref_to_gen
end PNEQ5

namespace PNEQ6
open Topology Filter Real Complex TopologicalSpace Finset
open scoped BigOperators
open Filter Topology
noncomputable def f : ℕ → ℝ
| 0 => sqrt 2
| (n + 1) => sqrt (2 + sqrt (f n))

theorem gen_to_ref (h_gen : ∀ s : ℕ → ℝ, s 1 = Real.sqrt 2 → (∀ n : ℕ, 1 ≤ n → s (n + 1) = Real.sqrt (2 + Real.sqrt (s n))) → (∃ L : ℝ, Filter.Tendsto (fun n : ℕ => s n) Filter.atTop (𝓝 L)) ∧ ∀ n : ℕ, 1 ≤ n → s n < 2)  :
    ∃ (x : ℝ), Tendsto f atTop (𝓝 x) ∧ ∀ n, f n < 2 := by
  first
    | exact h_gen
    | (intros; apply h_gen <;> first | assumption | exact default | (simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done) | fun_prop | aesop)
    | (simpa [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective] using h_gen)
    | (simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done)
    | (intros; simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done)
    | tauto
    | aesop
    | (convert h_gen using 1 <;> first | rfl | (simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done) | aesop)
    | (convert h_gen using 2 <;> first | rfl | (simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done) | aesop)
    | (convert h_gen using 3 <;> first | rfl | (simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done) | aesop)

theorem ref_to_gen (h_ref : ∃ (x : ℝ), Tendsto f atTop (𝓝 x) ∧ ∀ n, f n < 2) :
    ∀ s : ℕ → ℝ, s 1 = Real.sqrt 2 → (∀ n : ℕ, 1 ≤ n → s (n + 1) = Real.sqrt (2 + Real.sqrt (s n))) → (∃ L : ℝ, Filter.Tendsto (fun n : ℕ => s n) Filter.atTop (𝓝 L)) ∧ ∀ n : ℕ, 1 ≤ n → s n < 2 := by
  first
    | exact h_ref
    | (intros; apply h_ref <;> first | assumption | exact default | (simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done) | fun_prop | aesop)
    | (simpa [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective] using h_ref)
    | (simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done)
    | (intros; simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done)
    | tauto
    | aesop
    | (convert h_ref using 1 <;> first | rfl | (simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done) | aesop)
    | (convert h_ref using 2 <;> first | rfl | (simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done) | aesop)
    | (convert h_ref using 3 <;> first | rfl | (simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done) | aesop)

#print axioms gen_to_ref
#print axioms ref_to_gen
end PNEQ6

namespace PNEQ7
open Topology Filter Real Complex TopologicalSpace Finset
open scoped BigOperators
open Filter Topology
noncomputable def f : ℕ → ℝ
| 0 => sqrt 2
| (n + 1) => sqrt (2 + sqrt (f n))

theorem gen_to_ref (h_gen : ∀ s : ℕ → ℝ, s 1 = Real.sqrt 2 → (∀ n : ℕ, 1 ≤ n → s (n + 1) = Real.sqrt (2 + Real.sqrt (s n))) → (∃ L : ℝ, Filter.Tendsto (fun n : ℕ => s n) Filter.atTop (𝓝 L)) ∧ ∀ n : ℕ, 1 ≤ n → s n < 2)  :
    ∃ (x : ℝ), Tendsto f atTop (𝓝 x) ∧ ∀ n, f n < 2 := by
  first
    | exact h_gen
    | (intros; apply h_gen <;> first | assumption | exact default | (simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done) | fun_prop | aesop)
    | (simpa [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective] using h_gen)
    | (simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done)
    | (intros; simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done)
    | tauto
    | aesop
    | (convert h_gen using 1 <;> first | rfl | (simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done) | aesop)
    | (convert h_gen using 2 <;> first | rfl | (simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done) | aesop)
    | (convert h_gen using 3 <;> first | rfl | (simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done) | aesop)

theorem ref_to_gen (h_ref : ∃ (x : ℝ), Tendsto f atTop (𝓝 x) ∧ ∀ n, f n < 2) :
    ∀ s : ℕ → ℝ, s 1 = Real.sqrt 2 → (∀ n : ℕ, 1 ≤ n → s (n + 1) = Real.sqrt (2 + Real.sqrt (s n))) → (∃ L : ℝ, Filter.Tendsto (fun n : ℕ => s n) Filter.atTop (𝓝 L)) ∧ ∀ n : ℕ, 1 ≤ n → s n < 2 := by
  first
    | exact h_ref
    | (intros; apply h_ref <;> first | assumption | exact default | (simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done) | fun_prop | aesop)
    | (simpa [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective] using h_ref)
    | (simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done)
    | (intros; simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done)
    | tauto
    | aesop
    | (convert h_ref using 1 <;> first | rfl | (simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done) | aesop)
    | (convert h_ref using 2 <;> first | rfl | (simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done) | aesop)
    | (convert h_ref using 3 <;> first | rfl | (simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done) | aesop)

#print axioms gen_to_ref
#print axioms ref_to_gen
end PNEQ7

namespace PNEQ8
open Topology Filter Real Complex TopologicalSpace Finset
open scoped BigOperators



theorem gen_to_ref (h_gen : ∀ f : ℝ → ℝ, (∀ a b c : ℝ, f a < c → c < f b → ∃ x ∈ Set.Ioo (min a b) (max a b), f x = c) → (∀ r : ℚ, IsClosed {x : ℝ | f x = (r : ℝ)}) → Continuous f) {f : ℝ → ℝ} (hf : ∀ a b c, a < b → f a < c → c < f b → ∃ x, a < x ∧ x < b ∧ f x = c)
  (hg : ∀ r : ℚ, IsClosed {x | f x = r}) :
    Continuous f := by
  first
    | exact h_gen
    | (intros; apply h_gen <;> first | assumption | exact default | (simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done) | fun_prop | aesop)
    | (simpa [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective] using h_gen)
    | (simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done)
    | (intros; simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done)
    | tauto
    | aesop
    | (convert h_gen using 1 <;> first | rfl | (simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done) | aesop)
    | (convert h_gen using 2 <;> first | rfl | (simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done) | aesop)
    | (convert h_gen using 3 <;> first | rfl | (simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done) | aesop)

theorem ref_to_gen (h_ref : ∀ {f : ℝ → ℝ} (hf : ∀ a b c, a < b → f a < c → c < f b → ∃ x, a < x ∧ x < b ∧ f x = c)
  (hg : ∀ r : ℚ, IsClosed {x | f x = r}), Continuous f) :
    ∀ f : ℝ → ℝ, (∀ a b c : ℝ, f a < c → c < f b → ∃ x ∈ Set.Ioo (min a b) (max a b), f x = c) → (∀ r : ℚ, IsClosed {x : ℝ | f x = (r : ℝ)}) → Continuous f := by
  first
    | exact h_ref
    | (intros; apply h_ref <;> first | assumption | exact default | (simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done) | fun_prop | aesop)
    | (simpa [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective] using h_ref)
    | (simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done)
    | (intros; simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done)
    | tauto
    | aesop
    | (convert h_ref using 1 <;> first | rfl | (simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done) | aesop)
    | (convert h_ref using 2 <;> first | rfl | (simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done) | aesop)
    | (convert h_ref using 3 <;> first | rfl | (simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done) | aesop)

#print axioms gen_to_ref
#print axioms ref_to_gen
end PNEQ8

namespace PNEQ9
open Topology Filter Real Complex TopologicalSpace Finset
open scoped BigOperators



theorem gen_to_ref (h_gen : ∀ f : ℝ → ℝ, (∀ a b c : ℝ, f a < c → c < f b → ∃ x ∈ Set.Ioo (min a b) (max a b), f x = c) → (∀ r : ℚ, IsClosed {x : ℝ | f x = (r : ℝ)}) → Continuous f) {f : ℝ → ℝ} (hf : ∀ a b c, a < b → f a < c → c < f b → ∃ x, a < x ∧ x < b ∧ f x = c)
  (hg : ∀ r : ℚ, IsClosed {x | f x = r}) :
    Continuous f := by
  first
    | exact h_gen
    | (intros; apply h_gen <;> first | assumption | exact default | (simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done) | fun_prop | aesop)
    | (simpa [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective] using h_gen)
    | (simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done)
    | (intros; simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done)
    | tauto
    | aesop
    | (convert h_gen using 1 <;> first | rfl | (simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done) | aesop)
    | (convert h_gen using 2 <;> first | rfl | (simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done) | aesop)
    | (convert h_gen using 3 <;> first | rfl | (simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done) | aesop)

theorem ref_to_gen (h_ref : ∀ {f : ℝ → ℝ} (hf : ∀ a b c, a < b → f a < c → c < f b → ∃ x, a < x ∧ x < b ∧ f x = c)
  (hg : ∀ r : ℚ, IsClosed {x | f x = r}), Continuous f) :
    ∀ f : ℝ → ℝ, (∀ a b c : ℝ, f a < c → c < f b → ∃ x ∈ Set.Ioo (min a b) (max a b), f x = c) → (∀ r : ℚ, IsClosed {x : ℝ | f x = (r : ℝ)}) → Continuous f := by
  first
    | exact h_ref
    | (intros; apply h_ref <;> first | assumption | exact default | (simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done) | fun_prop | aesop)
    | (simpa [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective] using h_ref)
    | (simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done)
    | (intros; simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done)
    | tauto
    | aesop
    | (convert h_ref using 1 <;> first | rfl | (simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done) | aesop)
    | (convert h_ref using 2 <;> first | rfl | (simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done) | aesop)
    | (convert h_ref using 3 <;> first | rfl | (simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done) | aesop)

#print axioms gen_to_ref
#print axioms ref_to_gen
end PNEQ9

namespace PNEQ10
open Topology Filter Real Complex TopologicalSpace Finset
open scoped BigOperators



theorem gen_to_ref (h_gen : ∀ a b : ℝ, a < b → ∀ f : ℝ → ℝ, ContinuousOn f (Set.Ioo a b) → (∀ x ∈ Set.Ioo a b, ∀ y ∈ Set.Ioo a b, f ((x + y) / 2) ≤ (f x + f y) / 2) → ConvexOn ℝ (Set.Ioo a b) f) {f : ℝ → ℝ}
  (hf : Continuous f) (a b : ℝ) (hab : a < b)
  (h : ∀ x y : ℝ, a < x → x < b → a < y → y < b → f ((x + y) / 2) ≤ (f x + f y) / 2) :
    ConvexOn ℝ (Set.Ioo a b) f := by
  first
    | exact h_gen
    | (intros; apply h_gen <;> first | assumption | exact default | (simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done) | fun_prop | aesop)
    | (simpa [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective] using h_gen)
    | (simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done)
    | (intros; simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done)
    | tauto
    | aesop
    | (convert h_gen using 1 <;> first | rfl | (simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done) | aesop)
    | (convert h_gen using 2 <;> first | rfl | (simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done) | aesop)
    | (convert h_gen using 3 <;> first | rfl | (simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done) | aesop)

theorem ref_to_gen (h_ref : ∀ {f : ℝ → ℝ}
  (hf : Continuous f) (a b : ℝ) (hab : a < b)
  (h : ∀ x y : ℝ, a < x → x < b → a < y → y < b → f ((x + y) / 2) ≤ (f x + f y) / 2), ConvexOn ℝ (Set.Ioo a b) f) :
    ∀ a b : ℝ, a < b → ∀ f : ℝ → ℝ, ContinuousOn f (Set.Ioo a b) → (∀ x ∈ Set.Ioo a b, ∀ y ∈ Set.Ioo a b, f ((x + y) / 2) ≤ (f x + f y) / 2) → ConvexOn ℝ (Set.Ioo a b) f := by
  first
    | exact h_ref
    | (intros; apply h_ref <;> first | assumption | exact default | (simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done) | fun_prop | aesop)
    | (simpa [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective] using h_ref)
    | (simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done)
    | (intros; simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done)
    | tauto
    | aesop
    | (convert h_ref using 1 <;> first | rfl | (simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done) | aesop)
    | (convert h_ref using 2 <;> first | rfl | (simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done) | aesop)
    | (convert h_ref using 3 <;> first | rfl | (simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done) | aesop)

#print axioms gen_to_ref
#print axioms ref_to_gen
end PNEQ10

namespace PNEQ11
open Topology Filter Real Complex TopologicalSpace Finset
open scoped BigOperators



theorem gen_to_ref (h_gen : ∀ a b : ℝ, a < b → ∀ f : ℝ → ℝ, ContinuousOn f (Set.Ioo a b) → (∀ x ∈ Set.Ioo a b, ∀ y ∈ Set.Ioo a b, f ((x + y) / 2) ≤ (f x + f y) / 2) → ConvexOn ℝ (Set.Ioo a b) f) {f : ℝ → ℝ}
  (hf : Continuous f) (a b : ℝ) (hab : a < b)
  (h : ∀ x y : ℝ, a < x → x < b → a < y → y < b → f ((x + y) / 2) ≤ (f x + f y) / 2) :
    ConvexOn ℝ (Set.Ioo a b) f := by
  first
    | exact h_gen
    | (intros; apply h_gen <;> first | assumption | exact default | (simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done) | fun_prop | aesop)
    | (simpa [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective] using h_gen)
    | (simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done)
    | (intros; simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done)
    | tauto
    | aesop
    | (convert h_gen using 1 <;> first | rfl | (simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done) | aesop)
    | (convert h_gen using 2 <;> first | rfl | (simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done) | aesop)
    | (convert h_gen using 3 <;> first | rfl | (simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done) | aesop)

theorem ref_to_gen (h_ref : ∀ {f : ℝ → ℝ}
  (hf : Continuous f) (a b : ℝ) (hab : a < b)
  (h : ∀ x y : ℝ, a < x → x < b → a < y → y < b → f ((x + y) / 2) ≤ (f x + f y) / 2), ConvexOn ℝ (Set.Ioo a b) f) :
    ∀ a b : ℝ, a < b → ∀ f : ℝ → ℝ, ContinuousOn f (Set.Ioo a b) → (∀ x ∈ Set.Ioo a b, ∀ y ∈ Set.Ioo a b, f ((x + y) / 2) ≤ (f x + f y) / 2) → ConvexOn ℝ (Set.Ioo a b) f := by
  first
    | exact h_ref
    | (intros; apply h_ref <;> first | assumption | exact default | (simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done) | fun_prop | aesop)
    | (simpa [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective] using h_ref)
    | (simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done)
    | (intros; simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done)
    | tauto
    | aesop
    | (convert h_ref using 1 <;> first | rfl | (simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done) | aesop)
    | (convert h_ref using 2 <;> first | rfl | (simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done) | aesop)
    | (convert h_ref using 3 <;> first | rfl | (simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done) | aesop)

#print axioms gen_to_ref
#print axioms ref_to_gen
end PNEQ11

namespace PNEQ12
open Topology Filter Real Complex TopologicalSpace Finset
open scoped BigOperators
open Set


theorem gen_to_ref (h_gen : ∀ f : ℝ → ℝ, ∀ a b : ℝ, a < b → (∀ x ∈ Set.Ioo a b, DifferentiableAt ℝ f x) → (∀ x ∈ Set.Ioo a b, 0 < deriv f x) → StrictMonoOn f (Set.Ioo a b) ∧ ∀ g : ℝ → ℝ, (∀ x ∈ Set.Ioo a b, g (f x) = x) → ((∀ y ∈ f '' Set.Ioo a b, DifferentiableAt ℝ g y) ∧ ∀ x ∈ Set.Ioo a b, deriv g (f x) = 1 / deriv f x)) {a b : ℝ}
  {f g : ℝ → ℝ} (hf : ∀ x ∈ Set.Ioo a b, deriv f x > 0)
  (hg : g = f⁻¹) :
    StrictMonoOn f (Set.Ioo a b) ∧
  DifferentiableOn ℝ g (Set.Ioo a b) ∧
  ∀ x ∈ Set.Ioo a b, deriv g (f x) = 1 / deriv f x := by
  first
    | exact h_gen
    | (intros; apply h_gen <;> first | assumption | exact default | (simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done) | fun_prop | aesop)
    | (simpa [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective] using h_gen)
    | (simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done)
    | (intros; simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done)
    | tauto
    | aesop
    | (convert h_gen using 1 <;> first | rfl | (simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done) | aesop)
    | (convert h_gen using 2 <;> first | rfl | (simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done) | aesop)
    | (convert h_gen using 3 <;> first | rfl | (simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done) | aesop)

theorem ref_to_gen (h_ref : ∀ {a b : ℝ}
  {f g : ℝ → ℝ} (hf : ∀ x ∈ Set.Ioo a b, deriv f x > 0)
  (hg : g = f⁻¹), StrictMonoOn f (Set.Ioo a b) ∧
  DifferentiableOn ℝ g (Set.Ioo a b) ∧
  ∀ x ∈ Set.Ioo a b, deriv g (f x) = 1 / deriv f x) :
    ∀ f : ℝ → ℝ, ∀ a b : ℝ, a < b → (∀ x ∈ Set.Ioo a b, DifferentiableAt ℝ f x) → (∀ x ∈ Set.Ioo a b, 0 < deriv f x) → StrictMonoOn f (Set.Ioo a b) ∧ ∀ g : ℝ → ℝ, (∀ x ∈ Set.Ioo a b, g (f x) = x) → ((∀ y ∈ f '' Set.Ioo a b, DifferentiableAt ℝ g y) ∧ ∀ x ∈ Set.Ioo a b, deriv g (f x) = 1 / deriv f x) := by
  first
    | exact h_ref
    | (intros; apply h_ref <;> first | assumption | exact default | (simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done) | fun_prop | aesop)
    | (simpa [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective] using h_ref)
    | (simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done)
    | (intros; simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done)
    | tauto
    | aesop
    | (convert h_ref using 1 <;> first | rfl | (simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done) | aesop)
    | (convert h_ref using 2 <;> first | rfl | (simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done) | aesop)
    | (convert h_ref using 3 <;> first | rfl | (simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done) | aesop)

#print axioms gen_to_ref
#print axioms ref_to_gen
end PNEQ12

namespace PNEQ13
open Topology Filter Real Complex TopologicalSpace Finset
open scoped BigOperators
open Set


theorem gen_to_ref (h_gen : ∀ f : ℝ → ℝ, ∀ a b : ℝ, a < b → (∀ x ∈ Set.Ioo a b, DifferentiableAt ℝ f x) → (∀ x ∈ Set.Ioo a b, 0 < deriv f x) → StrictMonoOn f (Set.Ioo a b) ∧ ∀ g : ℝ → ℝ, (∀ x ∈ Set.Ioo a b, g (f x) = x) → ((∀ y ∈ f '' Set.Ioo a b, DifferentiableAt ℝ g y) ∧ ∀ x ∈ Set.Ioo a b, deriv g (f x) = 1 / deriv f x)) {a b : ℝ}
  {f g : ℝ → ℝ} (hf : ∀ x ∈ Set.Ioo a b, deriv f x > 0)
  (hg : g = f⁻¹) :
    StrictMonoOn f (Set.Ioo a b) ∧
  DifferentiableOn ℝ g (Set.Ioo a b) ∧
  ∀ x ∈ Set.Ioo a b, deriv g (f x) = 1 / deriv f x := by
  first
    | exact h_gen
    | (intros; apply h_gen <;> first | assumption | exact default | (simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done) | fun_prop | aesop)
    | (simpa [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective] using h_gen)
    | (simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done)
    | (intros; simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done)
    | tauto
    | aesop
    | (convert h_gen using 1 <;> first | rfl | (simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done) | aesop)
    | (convert h_gen using 2 <;> first | rfl | (simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done) | aesop)
    | (convert h_gen using 3 <;> first | rfl | (simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done) | aesop)

theorem ref_to_gen (h_ref : ∀ {a b : ℝ}
  {f g : ℝ → ℝ} (hf : ∀ x ∈ Set.Ioo a b, deriv f x > 0)
  (hg : g = f⁻¹), StrictMonoOn f (Set.Ioo a b) ∧
  DifferentiableOn ℝ g (Set.Ioo a b) ∧
  ∀ x ∈ Set.Ioo a b, deriv g (f x) = 1 / deriv f x) :
    ∀ f : ℝ → ℝ, ∀ a b : ℝ, a < b → (∀ x ∈ Set.Ioo a b, DifferentiableAt ℝ f x) → (∀ x ∈ Set.Ioo a b, 0 < deriv f x) → StrictMonoOn f (Set.Ioo a b) ∧ ∀ g : ℝ → ℝ, (∀ x ∈ Set.Ioo a b, g (f x) = x) → ((∀ y ∈ f '' Set.Ioo a b, DifferentiableAt ℝ g y) ∧ ∀ x ∈ Set.Ioo a b, deriv g (f x) = 1 / deriv f x) := by
  first
    | exact h_ref
    | (intros; apply h_ref <;> first | assumption | exact default | (simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done) | fun_prop | aesop)
    | (simpa [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective] using h_ref)
    | (simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done)
    | (intros; simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done)
    | tauto
    | aesop
    | (convert h_ref using 1 <;> first | rfl | (simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done) | aesop)
    | (convert h_ref using 2 <;> first | rfl | (simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done) | aesop)
    | (convert h_ref using 3 <;> first | rfl | (simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done) | aesop)

#print axioms gen_to_ref
#print axioms ref_to_gen
end PNEQ13

namespace PNEQ14
open Topology Filter Real Complex TopologicalSpace Finset
open scoped BigOperators
open Finset


theorem gen_to_ref (h_gen : ∀ (n : ℕ) (C : ℕ → ℝ), 1 ≤ n → ∑ k ∈ Finset.range (n + 1), C k / ((k : ℝ) + 1) = 0 → ∃ x : ℝ, 0 < x ∧ x < 1 ∧ ∑ k ∈ Finset.range (n + 1), C k * x ^ k = 0) {n : ℕ}
  (C : ℕ → ℝ)
  (hC : ∑ i ∈ (range (n + 1)), (C i) / (i + 1) = 0) :
    ∃ x, x ∈ (Set.Icc (0 : ℝ) 1) ∧ ∑ i ∈ range (n + 1), (C i) * (x^i) = 0 := by
  first
    | exact h_gen
    | (intros; apply h_gen <;> first | assumption | exact default | (simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done) | fun_prop | aesop)
    | (simpa [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective] using h_gen)
    | (simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done)
    | (intros; simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done)
    | tauto
    | aesop
    | (convert h_gen using 1 <;> first | rfl | (simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done) | aesop)
    | (convert h_gen using 2 <;> first | rfl | (simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done) | aesop)
    | (convert h_gen using 3 <;> first | rfl | (simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done) | aesop)

theorem ref_to_gen (h_ref : ∀ {n : ℕ}
  (C : ℕ → ℝ)
  (hC : ∑ i ∈ (range (n + 1)), (C i) / (i + 1) = 0), ∃ x, x ∈ (Set.Icc (0 : ℝ) 1) ∧ ∑ i ∈ range (n + 1), (C i) * (x^i) = 0) :
    ∀ (n : ℕ) (C : ℕ → ℝ), 1 ≤ n → ∑ k ∈ Finset.range (n + 1), C k / ((k : ℝ) + 1) = 0 → ∃ x : ℝ, 0 < x ∧ x < 1 ∧ ∑ k ∈ Finset.range (n + 1), C k * x ^ k = 0 := by
  first
    | exact h_ref
    | (intros; apply h_ref <;> first | assumption | exact default | (simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done) | fun_prop | aesop)
    | (simpa [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective] using h_ref)
    | (simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done)
    | (intros; simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done)
    | tauto
    | aesop
    | (convert h_ref using 1 <;> first | rfl | (simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done) | aesop)
    | (convert h_ref using 2 <;> first | rfl | (simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done) | aesop)
    | (convert h_ref using 3 <;> first | rfl | (simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done) | aesop)

#print axioms gen_to_ref
#print axioms ref_to_gen
end PNEQ14

namespace PNEQ15
open Topology Filter Real Complex TopologicalSpace Finset
open scoped BigOperators
open Finset


theorem gen_to_ref (h_gen : ∀ (n : ℕ) (C : ℕ → ℝ), 1 ≤ n → ∑ k ∈ Finset.range (n + 1), C k / ((k : ℝ) + 1) = 0 → ∃ x : ℝ, 0 < x ∧ x < 1 ∧ ∑ k ∈ Finset.range (n + 1), C k * x ^ k = 0) {n : ℕ}
  (C : ℕ → ℝ)
  (hC : ∑ i ∈ (range (n + 1)), (C i) / (i + 1) = 0) :
    ∃ x, x ∈ (Set.Icc (0 : ℝ) 1) ∧ ∑ i ∈ range (n + 1), (C i) * (x^i) = 0 := by
  first
    | exact h_gen
    | (intros; apply h_gen <;> first | assumption | exact default | (simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done) | fun_prop | aesop)
    | (simpa [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective] using h_gen)
    | (simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done)
    | (intros; simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done)
    | tauto
    | aesop
    | (convert h_gen using 1 <;> first | rfl | (simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done) | aesop)
    | (convert h_gen using 2 <;> first | rfl | (simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done) | aesop)
    | (convert h_gen using 3 <;> first | rfl | (simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done) | aesop)

theorem ref_to_gen (h_ref : ∀ {n : ℕ}
  (C : ℕ → ℝ)
  (hC : ∑ i ∈ (range (n + 1)), (C i) / (i + 1) = 0), ∃ x, x ∈ (Set.Icc (0 : ℝ) 1) ∧ ∑ i ∈ range (n + 1), (C i) * (x^i) = 0) :
    ∀ (n : ℕ) (C : ℕ → ℝ), 1 ≤ n → ∑ k ∈ Finset.range (n + 1), C k / ((k : ℝ) + 1) = 0 → ∃ x : ℝ, 0 < x ∧ x < 1 ∧ ∑ k ∈ Finset.range (n + 1), C k * x ^ k = 0 := by
  first
    | exact h_ref
    | (intros; apply h_ref <;> first | assumption | exact default | (simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done) | fun_prop | aesop)
    | (simpa [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective] using h_ref)
    | (simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done)
    | (intros; simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done)
    | tauto
    | aesop
    | (convert h_ref using 1 <;> first | rfl | (simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done) | aesop)
    | (convert h_ref using 2 <;> first | rfl | (simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done) | aesop)
    | (convert h_ref using 3 <;> first | rfl | (simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done) | aesop)

#print axioms gen_to_ref
#print axioms ref_to_gen
end PNEQ15

namespace PNEQ16
open Topology Filter Real Complex TopologicalSpace Finset
open scoped BigOperators
open Set


theorem gen_to_ref (h_gen : ∀ f : ℝ → ℝ, ContinuousOn f (Set.Ici 0) → (∀ x ∈ Set.Ioi (0:ℝ), DifferentiableAt ℝ f x) → f 0 = 0 → MonotoneOn (deriv f) (Set.Ioi 0) → MonotoneOn (fun x : ℝ => f x / x) (Set.Ioi 0)) {f : ℝ → ℝ}
  (hf1 : ContinuousOn f (Set.Ici 0))
  (hf2 : DifferentiableOn ℝ f (Set.Ioi 0))
  (hf3 : f 0 = 0)
  (hf4 : MonotoneOn (deriv f) (Set.Ioi 0)) :
    MonotoneOn (λ x => f x / x) (Set.Ioi 0) := by
  first
    | exact h_gen
    | (intros; apply h_gen <;> first | assumption | exact default | (simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done) | fun_prop | aesop)
    | (simpa [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective] using h_gen)
    | (simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done)
    | (intros; simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done)
    | tauto
    | aesop
    | (convert h_gen using 1 <;> first | rfl | (simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done) | aesop)
    | (convert h_gen using 2 <;> first | rfl | (simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done) | aesop)
    | (convert h_gen using 3 <;> first | rfl | (simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done) | aesop)

theorem ref_to_gen (h_ref : ∀ {f : ℝ → ℝ}
  (hf1 : ContinuousOn f (Set.Ici 0))
  (hf2 : DifferentiableOn ℝ f (Set.Ioi 0))
  (hf3 : f 0 = 0)
  (hf4 : MonotoneOn (deriv f) (Set.Ioi 0)), MonotoneOn (λ x => f x / x) (Set.Ioi 0)) :
    ∀ f : ℝ → ℝ, ContinuousOn f (Set.Ici 0) → (∀ x ∈ Set.Ioi (0:ℝ), DifferentiableAt ℝ f x) → f 0 = 0 → MonotoneOn (deriv f) (Set.Ioi 0) → MonotoneOn (fun x : ℝ => f x / x) (Set.Ioi 0) := by
  first
    | exact h_ref
    | (intros; apply h_ref <;> first | assumption | exact default | (simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done) | fun_prop | aesop)
    | (simpa [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective] using h_ref)
    | (simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done)
    | (intros; simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done)
    | tauto
    | aesop
    | (convert h_ref using 1 <;> first | rfl | (simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done) | aesop)
    | (convert h_ref using 2 <;> first | rfl | (simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done) | aesop)
    | (convert h_ref using 3 <;> first | rfl | (simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done) | aesop)

#print axioms gen_to_ref
#print axioms ref_to_gen
end PNEQ16

namespace PNEQ17
open Topology Filter Real Complex TopologicalSpace Finset
open scoped BigOperators
open Set


theorem gen_to_ref (h_gen : ∀ f : ℝ → ℝ, ContinuousOn f (Set.Ici 0) → (∀ x ∈ Set.Ioi (0:ℝ), DifferentiableAt ℝ f x) → f 0 = 0 → MonotoneOn (deriv f) (Set.Ioi 0) → MonotoneOn (fun x : ℝ => f x / x) (Set.Ioi 0)) {f : ℝ → ℝ}
  (hf1 : ContinuousOn f (Set.Ici 0))
  (hf2 : DifferentiableOn ℝ f (Set.Ioi 0))
  (hf3 : f 0 = 0)
  (hf4 : MonotoneOn (deriv f) (Set.Ioi 0)) :
    MonotoneOn (λ x => f x / x) (Set.Ioi 0) := by
  first
    | exact h_gen
    | (intros; apply h_gen <;> first | assumption | exact default | (simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done) | fun_prop | aesop)
    | (simpa [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective] using h_gen)
    | (simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done)
    | (intros; simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done)
    | tauto
    | aesop
    | (convert h_gen using 1 <;> first | rfl | (simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done) | aesop)
    | (convert h_gen using 2 <;> first | rfl | (simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done) | aesop)
    | (convert h_gen using 3 <;> first | rfl | (simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done) | aesop)

theorem ref_to_gen (h_ref : ∀ {f : ℝ → ℝ}
  (hf1 : ContinuousOn f (Set.Ici 0))
  (hf2 : DifferentiableOn ℝ f (Set.Ioi 0))
  (hf3 : f 0 = 0)
  (hf4 : MonotoneOn (deriv f) (Set.Ioi 0)), MonotoneOn (λ x => f x / x) (Set.Ioi 0)) :
    ∀ f : ℝ → ℝ, ContinuousOn f (Set.Ici 0) → (∀ x ∈ Set.Ioi (0:ℝ), DifferentiableAt ℝ f x) → f 0 = 0 → MonotoneOn (deriv f) (Set.Ioi 0) → MonotoneOn (fun x : ℝ => f x / x) (Set.Ioi 0) := by
  first
    | exact h_ref
    | (intros; apply h_ref <;> first | assumption | exact default | (simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done) | fun_prop | aesop)
    | (simpa [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective] using h_ref)
    | (simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done)
    | (intros; simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done)
    | tauto
    | aesop
    | (convert h_ref using 1 <;> first | rfl | (simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done) | aesop)
    | (convert h_ref using 2 <;> first | rfl | (simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done) | aesop)
    | (convert h_ref using 3 <;> first | rfl | (simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done) | aesop)

#print axioms gen_to_ref
#print axioms ref_to_gen
end PNEQ17

namespace PNEQ18
open Topology Filter Real Complex TopologicalSpace Finset
open scoped BigOperators



theorem gen_to_ref (h_gen : ∀ (a : ℝ) (f : ℝ → ℝ) (M0 M1 M2 : ℝ), (∀ x : ℝ, a < x → DifferentiableAt ℝ f x ∧ DifferentiableAt ℝ (deriv f) x) → IsLUB ((fun x : ℝ => |f x|) '' Set.Ioi a) M0 → IsLUB ((fun x : ℝ => |deriv f x|) '' Set.Ioi a) M1 → IsLUB ((fun x : ℝ => |deriv (deriv f) x|) '' Set.Ioi a) M2 → M1 ^ 2 ≤ 4 * M0 * M2) {f : ℝ → ℝ} (a M0 M1 M2 : ℝ)
  (hf' : DifferentiableOn ℝ f (Set.Ioi a))
  (hf'' : DifferentiableOn ℝ (deriv f) (Set.Ioi a))
  (hM0 : M0 = sSup {(|f x|) | x ∈ (Set.Ioi a)})
  (hM1 : M1 = sSup {(|deriv f x|) | x ∈ (Set.Ioi a)})
  (hM2 : M2 = sSup {(|deriv (deriv f) x|) | x ∈ (Set.Ioi a)}) :
    (M1 ^ 2) ≤ 4 * M0 * M2 := by
  first
    | exact h_gen
    | (intros; apply h_gen <;> first | assumption | exact default | (simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done) | fun_prop | aesop)
    | (simpa [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective] using h_gen)
    | (simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done)
    | (intros; simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done)
    | tauto
    | aesop
    | (convert h_gen using 1 <;> first | rfl | (simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done) | aesop)
    | (convert h_gen using 2 <;> first | rfl | (simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done) | aesop)
    | (convert h_gen using 3 <;> first | rfl | (simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done) | aesop)

theorem ref_to_gen (h_ref : ∀ {f : ℝ → ℝ} (a M0 M1 M2 : ℝ)
  (hf' : DifferentiableOn ℝ f (Set.Ioi a))
  (hf'' : DifferentiableOn ℝ (deriv f) (Set.Ioi a))
  (hM0 : M0 = sSup {(|f x|) | x ∈ (Set.Ioi a)})
  (hM1 : M1 = sSup {(|deriv f x|) | x ∈ (Set.Ioi a)})
  (hM2 : M2 = sSup {(|deriv (deriv f) x|) | x ∈ (Set.Ioi a)}), (M1 ^ 2) ≤ 4 * M0 * M2) :
    ∀ (a : ℝ) (f : ℝ → ℝ) (M0 M1 M2 : ℝ), (∀ x : ℝ, a < x → DifferentiableAt ℝ f x ∧ DifferentiableAt ℝ (deriv f) x) → IsLUB ((fun x : ℝ => |f x|) '' Set.Ioi a) M0 → IsLUB ((fun x : ℝ => |deriv f x|) '' Set.Ioi a) M1 → IsLUB ((fun x : ℝ => |deriv (deriv f) x|) '' Set.Ioi a) M2 → M1 ^ 2 ≤ 4 * M0 * M2 := by
  first
    | exact h_ref
    | (intros; apply h_ref <;> first | assumption | exact default | (simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done) | fun_prop | aesop)
    | (simpa [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective] using h_ref)
    | (simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done)
    | (intros; simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done)
    | tauto
    | aesop
    | (convert h_ref using 1 <;> first | rfl | (simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done) | aesop)
    | (convert h_ref using 2 <;> first | rfl | (simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done) | aesop)
    | (convert h_ref using 3 <;> first | rfl | (simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done) | aesop)

#print axioms gen_to_ref
#print axioms ref_to_gen
end PNEQ18

namespace PNEQ19
open Topology Filter Real Complex TopologicalSpace Finset
open scoped BigOperators



theorem gen_to_ref (h_gen : ∀ (a : ℝ) (f : ℝ → ℝ) (M0 M1 M2 : ℝ), (∀ x : ℝ, a < x → DifferentiableAt ℝ f x ∧ DifferentiableAt ℝ (deriv f) x) → IsLUB ((fun x : ℝ => |f x|) '' Set.Ioi a) M0 → IsLUB ((fun x : ℝ => |deriv f x|) '' Set.Ioi a) M1 → IsLUB ((fun x : ℝ => |deriv (deriv f) x|) '' Set.Ioi a) M2 → M1 ^ 2 ≤ 4 * M0 * M2) {f : ℝ → ℝ} (a M0 M1 M2 : ℝ)
  (hf' : DifferentiableOn ℝ f (Set.Ioi a))
  (hf'' : DifferentiableOn ℝ (deriv f) (Set.Ioi a))
  (hM0 : M0 = sSup {(|f x|) | x ∈ (Set.Ioi a)})
  (hM1 : M1 = sSup {(|deriv f x|) | x ∈ (Set.Ioi a)})
  (hM2 : M2 = sSup {(|deriv (deriv f) x|) | x ∈ (Set.Ioi a)}) :
    (M1 ^ 2) ≤ 4 * M0 * M2 := by
  first
    | exact h_gen
    | (intros; apply h_gen <;> first | assumption | exact default | (simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done) | fun_prop | aesop)
    | (simpa [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective] using h_gen)
    | (simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done)
    | (intros; simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done)
    | tauto
    | aesop
    | (convert h_gen using 1 <;> first | rfl | (simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done) | aesop)
    | (convert h_gen using 2 <;> first | rfl | (simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done) | aesop)
    | (convert h_gen using 3 <;> first | rfl | (simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done) | aesop)

theorem ref_to_gen (h_ref : ∀ {f : ℝ → ℝ} (a M0 M1 M2 : ℝ)
  (hf' : DifferentiableOn ℝ f (Set.Ioi a))
  (hf'' : DifferentiableOn ℝ (deriv f) (Set.Ioi a))
  (hM0 : M0 = sSup {(|f x|) | x ∈ (Set.Ioi a)})
  (hM1 : M1 = sSup {(|deriv f x|) | x ∈ (Set.Ioi a)})
  (hM2 : M2 = sSup {(|deriv (deriv f) x|) | x ∈ (Set.Ioi a)}), (M1 ^ 2) ≤ 4 * M0 * M2) :
    ∀ (a : ℝ) (f : ℝ → ℝ) (M0 M1 M2 : ℝ), (∀ x : ℝ, a < x → DifferentiableAt ℝ f x ∧ DifferentiableAt ℝ (deriv f) x) → IsLUB ((fun x : ℝ => |f x|) '' Set.Ioi a) M0 → IsLUB ((fun x : ℝ => |deriv f x|) '' Set.Ioi a) M1 → IsLUB ((fun x : ℝ => |deriv (deriv f) x|) '' Set.Ioi a) M2 → M1 ^ 2 ≤ 4 * M0 * M2 := by
  first
    | exact h_ref
    | (intros; apply h_ref <;> first | assumption | exact default | (simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done) | fun_prop | aesop)
    | (simpa [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective] using h_ref)
    | (simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done)
    | (intros; simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done)
    | tauto
    | aesop
    | (convert h_ref using 1 <;> first | rfl | (simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done) | aesop)
    | (convert h_ref using 2 <;> first | rfl | (simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done) | aesop)
    | (convert h_ref using 3 <;> first | rfl | (simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done) | aesop)

#print axioms gen_to_ref
#print axioms ref_to_gen
end PNEQ19

namespace PNEQ20
open Filter Real Function
open scoped Topology
open Topology


theorem gen_to_ref (h_gen : ∀ (p : ℕ → ℝ) (f : ℕ → ℕ), Function.Injective f →
  (∀ L : ℝ, Filter.Tendsto p Filter.atTop (𝓝 L) → Filter.Tendsto (fun k : ℕ => p (f k)) Filter.atTop (𝓝 L)) ∧
  (Filter.Tendsto p Filter.atTop Filter.atTop → Filter.Tendsto (fun k : ℕ => p (f k)) Filter.atTop Filter.atTop) ∧
  (Filter.Tendsto p Filter.atTop Filter.atBot → Filter.Tendsto (fun k : ℕ => p (f k)) Filter.atTop Filter.atBot)) {α : Type*} [TopologicalSpace α]
  (f : ℕ → ℕ) (p : ℕ → α) (a : α)
  (hf : Injective f) (hp : Tendsto p atTop (𝓝 a)) :
    Tendsto (λ n => p (f n)) atTop (𝓝 a) := by
  first
    | exact h_gen
    | (intros; apply h_gen <;> first | assumption | exact default | (simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done) | fun_prop | aesop)
    | (simpa [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective] using h_gen)
    | (simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done)
    | (intros; simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done)
    | tauto
    | aesop
    | (convert h_gen using 1 <;> first | rfl | (simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done) | aesop)
    | (convert h_gen using 2 <;> first | rfl | (simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done) | aesop)
    | (convert h_gen using 3 <;> first | rfl | (simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done) | aesop)

theorem ref_to_gen (h_ref : ∀ {α : Type*} [TopologicalSpace α]
  (f : ℕ → ℕ) (p : ℕ → α) (a : α)
  (hf : Injective f) (hp : Tendsto p atTop (𝓝 a)), Tendsto (λ n => p (f n)) atTop (𝓝 a)) :
    ∀ (p : ℕ → ℝ) (f : ℕ → ℕ), Function.Injective f →
  (∀ L : ℝ, Filter.Tendsto p Filter.atTop (𝓝 L) → Filter.Tendsto (fun k : ℕ => p (f k)) Filter.atTop (𝓝 L)) ∧
  (Filter.Tendsto p Filter.atTop Filter.atTop → Filter.Tendsto (fun k : ℕ => p (f k)) Filter.atTop Filter.atTop) ∧
  (Filter.Tendsto p Filter.atTop Filter.atBot → Filter.Tendsto (fun k : ℕ => p (f k)) Filter.atTop Filter.atBot) := by
  first
    | exact h_ref
    | (intros; apply h_ref <;> first | assumption | exact default | (simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done) | fun_prop | aesop)
    | (simpa [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective] using h_ref)
    | (simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done)
    | (intros; simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done)
    | tauto
    | aesop
    | (convert h_ref using 1 <;> first | rfl | (simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done) | aesop)
    | (convert h_ref using 2 <;> first | rfl | (simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done) | aesop)
    | (convert h_ref using 3 <;> first | rfl | (simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done) | aesop)

#print axioms gen_to_ref
#print axioms ref_to_gen
end PNEQ20

namespace PNEQ21
open Filter Real Function
open scoped Topology
open Topology


theorem gen_to_ref (h_gen : ∀ (p : ℕ → ℝ) (f : ℕ → ℕ), Function.Injective f →
  (∀ L : ℝ, Filter.Tendsto p Filter.atTop (𝓝 L) → Filter.Tendsto (fun k : ℕ => p (f k)) Filter.atTop (𝓝 L)) ∧
  (Filter.Tendsto p Filter.atTop Filter.atTop → Filter.Tendsto (fun k : ℕ => p (f k)) Filter.atTop Filter.atTop) ∧
  (Filter.Tendsto p Filter.atTop Filter.atBot → Filter.Tendsto (fun k : ℕ => p (f k)) Filter.atTop Filter.atBot)) {α : Type*} [TopologicalSpace α]
  (f : ℕ → ℕ) (p : ℕ → α) (a : α)
  (hf : Injective f) (hp : Tendsto p atTop (𝓝 a)) :
    Tendsto (λ n => p (f n)) atTop (𝓝 a) := by
  first
    | exact h_gen
    | (intros; apply h_gen <;> first | assumption | exact default | (simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done) | fun_prop | aesop)
    | (simpa [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective] using h_gen)
    | (simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done)
    | (intros; simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done)
    | tauto
    | aesop
    | (convert h_gen using 1 <;> first | rfl | (simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done) | aesop)
    | (convert h_gen using 2 <;> first | rfl | (simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done) | aesop)
    | (convert h_gen using 3 <;> first | rfl | (simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done) | aesop)

theorem ref_to_gen (h_ref : ∀ {α : Type*} [TopologicalSpace α]
  (f : ℕ → ℕ) (p : ℕ → α) (a : α)
  (hf : Injective f) (hp : Tendsto p atTop (𝓝 a)), Tendsto (λ n => p (f n)) atTop (𝓝 a)) :
    ∀ (p : ℕ → ℝ) (f : ℕ → ℕ), Function.Injective f →
  (∀ L : ℝ, Filter.Tendsto p Filter.atTop (𝓝 L) → Filter.Tendsto (fun k : ℕ => p (f k)) Filter.atTop (𝓝 L)) ∧
  (Filter.Tendsto p Filter.atTop Filter.atTop → Filter.Tendsto (fun k : ℕ => p (f k)) Filter.atTop Filter.atTop) ∧
  (Filter.Tendsto p Filter.atTop Filter.atBot → Filter.Tendsto (fun k : ℕ => p (f k)) Filter.atTop Filter.atBot) := by
  first
    | exact h_ref
    | (intros; apply h_ref <;> first | assumption | exact default | (simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done) | fun_prop | aesop)
    | (simpa [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective] using h_ref)
    | (simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done)
    | (intros; simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done)
    | tauto
    | aesop
    | (convert h_ref using 1 <;> first | rfl | (simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done) | aesop)
    | (convert h_ref using 2 <;> first | rfl | (simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done) | aesop)
    | (convert h_ref using 3 <;> first | rfl | (simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done) | aesop)

#print axioms gen_to_ref
#print axioms ref_to_gen
end PNEQ21

namespace PNEQ22
open Topology Filter Real Complex TopologicalSpace Finset
open scoped BigOperators



theorem gen_to_ref (h_gen : ∀ A : Set ℝ, A.Nonempty → BddBelow A → ∃ a b : ℝ, IsGLB A a ∧ IsLUB ((fun x : ℝ => -x) '' A) b ∧ a = -b) (A minus_A : Set ℝ) (hA : A.Nonempty)
  (hA_bdd_below : BddBelow A) (hminus_A : minus_A = {x | -x ∈ A}) :
    sInf A = - sSup minus_A := by
  first
    | exact h_gen
    | (intros; apply h_gen <;> first | assumption | exact default | (simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done) | fun_prop | aesop)
    | (simpa [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective] using h_gen)
    | (simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done)
    | (intros; simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done)
    | tauto
    | aesop
    | (convert h_gen using 1 <;> first | rfl | (simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done) | aesop)
    | (convert h_gen using 2 <;> first | rfl | (simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done) | aesop)
    | (convert h_gen using 3 <;> first | rfl | (simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done) | aesop)

theorem ref_to_gen (h_ref : ∀ (A minus_A : Set ℝ) (hA : A.Nonempty)
  (hA_bdd_below : BddBelow A) (hminus_A : minus_A = {x | -x ∈ A}), sInf A = - sSup minus_A) :
    ∀ A : Set ℝ, A.Nonempty → BddBelow A → ∃ a b : ℝ, IsGLB A a ∧ IsLUB ((fun x : ℝ => -x) '' A) b ∧ a = -b := by
  first
    | exact h_ref
    | (intros; apply h_ref <;> first | assumption | exact default | (simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done) | fun_prop | aesop)
    | (simpa [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective] using h_ref)
    | (simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done)
    | (intros; simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done)
    | tauto
    | aesop
    | (convert h_ref using 1 <;> first | rfl | (simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done) | aesop)
    | (convert h_ref using 2 <;> first | rfl | (simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done) | aesop)
    | (convert h_ref using 3 <;> first | rfl | (simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done) | aesop)

#print axioms gen_to_ref
#print axioms ref_to_gen
end PNEQ22

namespace PNEQ23
open Topology Filter Real Complex TopologicalSpace Finset
open scoped BigOperators



theorem gen_to_ref (h_gen : ∀ A : Set ℝ, A.Nonempty → BddBelow A → ∃ a b : ℝ, IsGLB A a ∧ IsLUB ((fun x : ℝ => -x) '' A) b ∧ a = -b) (A minus_A : Set ℝ) (hA : A.Nonempty)
  (hA_bdd_below : BddBelow A) (hminus_A : minus_A = {x | -x ∈ A}) :
    sInf A = - sSup minus_A := by
  first
    | exact h_gen
    | (intros; apply h_gen <;> first | assumption | exact default | (simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done) | fun_prop | aesop)
    | (simpa [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective] using h_gen)
    | (simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done)
    | (intros; simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done)
    | tauto
    | aesop
    | (convert h_gen using 1 <;> first | rfl | (simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done) | aesop)
    | (convert h_gen using 2 <;> first | rfl | (simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done) | aesop)
    | (convert h_gen using 3 <;> first | rfl | (simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done) | aesop)

theorem ref_to_gen (h_ref : ∀ (A minus_A : Set ℝ) (hA : A.Nonempty)
  (hA_bdd_below : BddBelow A) (hminus_A : minus_A = {x | -x ∈ A}), sInf A = - sSup minus_A) :
    ∀ A : Set ℝ, A.Nonempty → BddBelow A → ∃ a b : ℝ, IsGLB A a ∧ IsLUB ((fun x : ℝ => -x) '' A) b ∧ a = -b := by
  first
    | exact h_ref
    | (intros; apply h_ref <;> first | assumption | exact default | (simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done) | fun_prop | aesop)
    | (simpa [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective] using h_ref)
    | (simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done)
    | (intros; simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done)
    | tauto
    | aesop
    | (convert h_ref using 1 <;> first | rfl | (simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done) | aesop)
    | (convert h_ref using 2 <;> first | rfl | (simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done) | aesop)
    | (convert h_ref using 3 <;> first | rfl | (simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done) | aesop)

#print axioms gen_to_ref
#print axioms ref_to_gen
end PNEQ23

namespace PNEQ24
open Topology Filter Real Complex TopologicalSpace Finset
open scoped BigOperators
open Filter
noncomputable def g (n : ℕ) : ℝ := sqrt (n + 1) - sqrt n

theorem gen_to_ref (h_gen : Filter.Tendsto (fun n : ℕ => ∑ i ∈ Finset.range n, (Real.sqrt ((i : ℝ) + 1) - Real.sqrt (i : ℝ))) Filter.atTop Filter.atTop)  :
    Tendsto (λ (n : ℕ) => (∑ i ∈ range n, g i)) atTop atTop := by
  first
    | exact h_gen
    | (intros; apply h_gen <;> first | assumption | exact default | (simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done) | fun_prop | aesop)
    | (simpa [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective] using h_gen)
    | (simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done)
    | (intros; simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done)
    | tauto
    | aesop
    | (convert h_gen using 1 <;> first | rfl | (simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done) | aesop)
    | (convert h_gen using 2 <;> first | rfl | (simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done) | aesop)
    | (convert h_gen using 3 <;> first | rfl | (simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done) | aesop)

theorem ref_to_gen (h_ref : Tendsto (λ (n : ℕ) => (∑ i ∈ range n, g i)) atTop atTop) :
    Filter.Tendsto (fun n : ℕ => ∑ i ∈ Finset.range n, (Real.sqrt ((i : ℝ) + 1) - Real.sqrt (i : ℝ))) Filter.atTop Filter.atTop := by
  first
    | exact h_ref
    | (intros; apply h_ref <;> first | assumption | exact default | (simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done) | fun_prop | aesop)
    | (simpa [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective] using h_ref)
    | (simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done)
    | (intros; simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done)
    | tauto
    | aesop
    | (convert h_ref using 1 <;> first | rfl | (simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done) | aesop)
    | (convert h_ref using 2 <;> first | rfl | (simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done) | aesop)
    | (convert h_ref using 3 <;> first | rfl | (simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done) | aesop)

#print axioms gen_to_ref
#print axioms ref_to_gen
end PNEQ24

namespace PNEQ25
open Topology Filter Real Complex TopologicalSpace Finset
open scoped BigOperators
open Filter
noncomputable def g (n : ℕ) : ℝ := sqrt (n + 1) - sqrt n

theorem gen_to_ref (h_gen : Filter.Tendsto (fun n : ℕ => ∑ i ∈ Finset.range n, (Real.sqrt ((i : ℝ) + 1) - Real.sqrt (i : ℝ))) Filter.atTop Filter.atTop)  :
    Tendsto (λ (n : ℕ) => (∑ i ∈ range n, g i)) atTop atTop := by
  first
    | exact h_gen
    | (intros; apply h_gen <;> first | assumption | exact default | (simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done) | fun_prop | aesop)
    | (simpa [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective] using h_gen)
    | (simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done)
    | (intros; simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done)
    | tauto
    | aesop
    | (convert h_gen using 1 <;> first | rfl | (simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done) | aesop)
    | (convert h_gen using 2 <;> first | rfl | (simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done) | aesop)
    | (convert h_gen using 3 <;> first | rfl | (simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done) | aesop)

theorem ref_to_gen (h_ref : Tendsto (λ (n : ℕ) => (∑ i ∈ range n, g i)) atTop atTop) :
    Filter.Tendsto (fun n : ℕ => ∑ i ∈ Finset.range n, (Real.sqrt ((i : ℝ) + 1) - Real.sqrt (i : ℝ))) Filter.atTop Filter.atTop := by
  first
    | exact h_ref
    | (intros; apply h_ref <;> first | assumption | exact default | (simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done) | fun_prop | aesop)
    | (simpa [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective] using h_ref)
    | (simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done)
    | (intros; simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done)
    | tauto
    | aesop
    | (convert h_ref using 1 <;> first | rfl | (simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done) | aesop)
    | (convert h_ref using 2 <;> first | rfl | (simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done) | aesop)
    | (convert h_ref using 3 <;> first | rfl | (simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done) | aesop)

#print axioms gen_to_ref
#print axioms ref_to_gen
end PNEQ25

namespace PNEQ26
open Topology Filter Real Complex TopologicalSpace Finset
open scoped BigOperators



theorem gen_to_ref (h_gen : ∀ E : Set ℝ, Bornology.IsBounded E → E.Nonempty → ∃ f : ℝ → ℝ, UniformContinuous f ∧ ∀ M : ℝ, ∃ x ∈ E, M < |f x|) (E : Set ℝ) (h : Bornology.IsBounded E) :
    ∃ f : ℝ → ℝ, UniformContinuousOn f E ∧ ¬ Bornology.IsBounded (Set.image f E) := by
  first
    | exact h_gen
    | (intros; apply h_gen <;> first | assumption | exact default | (simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done) | fun_prop | aesop)
    | (simpa [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective] using h_gen)
    | (simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done)
    | (intros; simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done)
    | tauto
    | aesop
    | (convert h_gen using 1 <;> first | rfl | (simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done) | aesop)
    | (convert h_gen using 2 <;> first | rfl | (simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done) | aesop)
    | (convert h_gen using 3 <;> first | rfl | (simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done) | aesop)

theorem ref_to_gen (h_ref : ∀ (E : Set ℝ) (h : Bornology.IsBounded E), ∃ f : ℝ → ℝ, UniformContinuousOn f E ∧ ¬ Bornology.IsBounded (Set.image f E)) :
    ∀ E : Set ℝ, Bornology.IsBounded E → E.Nonempty → ∃ f : ℝ → ℝ, UniformContinuous f ∧ ∀ M : ℝ, ∃ x ∈ E, M < |f x| := by
  first
    | exact h_ref
    | (intros; apply h_ref <;> first | assumption | exact default | (simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done) | fun_prop | aesop)
    | (simpa [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective] using h_ref)
    | (simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done)
    | (intros; simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done)
    | tauto
    | aesop
    | (convert h_ref using 1 <;> first | rfl | (simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done) | aesop)
    | (convert h_ref using 2 <;> first | rfl | (simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done) | aesop)
    | (convert h_ref using 3 <;> first | rfl | (simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done) | aesop)

#print axioms gen_to_ref
#print axioms ref_to_gen
end PNEQ26

namespace PNEQ27
open Topology Filter Real Complex TopologicalSpace Finset
open scoped BigOperators



theorem gen_to_ref (h_gen : ∀ E : Set ℝ, Bornology.IsBounded E → E.Nonempty → ∃ f : ℝ → ℝ, UniformContinuous f ∧ ∀ M : ℝ, ∃ x ∈ E, M < |f x|) (E : Set ℝ) (h : Bornology.IsBounded E) :
    ∃ f : ℝ → ℝ, UniformContinuousOn f E ∧ ¬ Bornology.IsBounded (Set.image f E) := by
  first
    | exact h_gen
    | (intros; apply h_gen <;> first | assumption | exact default | (simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done) | fun_prop | aesop)
    | (simpa [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective] using h_gen)
    | (simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done)
    | (intros; simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done)
    | tauto
    | aesop
    | (convert h_gen using 1 <;> first | rfl | (simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done) | aesop)
    | (convert h_gen using 2 <;> first | rfl | (simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done) | aesop)
    | (convert h_gen using 3 <;> first | rfl | (simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done) | aesop)

theorem ref_to_gen (h_ref : ∀ (E : Set ℝ) (h : Bornology.IsBounded E), ∃ f : ℝ → ℝ, UniformContinuousOn f E ∧ ¬ Bornology.IsBounded (Set.image f E)) :
    ∀ E : Set ℝ, Bornology.IsBounded E → E.Nonempty → ∃ f : ℝ → ℝ, UniformContinuous f ∧ ∀ M : ℝ, ∃ x ∈ E, M < |f x| := by
  first
    | exact h_ref
    | (intros; apply h_ref <;> first | assumption | exact default | (simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done) | fun_prop | aesop)
    | (simpa [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective] using h_ref)
    | (simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done)
    | (intros; simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done)
    | tauto
    | aesop
    | (convert h_ref using 1 <;> first | rfl | (simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done) | aesop)
    | (convert h_ref using 2 <;> first | rfl | (simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done) | aesop)
    | (convert h_ref using 3 <;> first | rfl | (simp_all [Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective]; done) | aesop)

#print axioms gen_to_ref
#print axioms ref_to_gen
end PNEQ27

