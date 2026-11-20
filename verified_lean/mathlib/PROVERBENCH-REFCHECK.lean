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

namespace PBRef0
set_option autoImplicit true
/-
The integral of \[(x^3 - 3cosx) dx\] is \[\frac{x^4}{4} - 3sinx + C\].
-/

-- Define the function f(x)
noncomputable def f (x : ℝ) : ℝ := x^3 - 3 * Real.cos x

-- Define the integral of f(x)
noncomputable def integralf (x : ℝ) : ℝ := (x^4 / 4) - 3 * Real.sin x

-- Theorem statement
theorem integral_f_eq_integralF_plus_C (x C : ℝ) :
    ∫ x , f x = integralf x + C := by
  sorry
end PBRef0

namespace PBRef1
set_option autoImplicit true
/-
The integral of \(\displaystyle \int_0^1\frac{8x^2 +6x +5}{x^2 +2x+2 }\,dx\) is equal to \(-5\ln\frac52 - \left(\tan^{-1}2-\frac{\pi}4\right)+8\).
-/

open Real
theorem integral_of_rational_function_eq_given_value  :
    let f := fun x => (8 * x^2 + 6 * x + 5) / (x^2 + 2 * x + 2);
  ∫ x in Set.Icc 0 1, f x = -5 * log (5 / 2) - (arctan 2 - π / 4) + 8 := by
  sorry
end PBRef1

namespace PBRef2
set_option autoImplicit true
/-
The local maximum of the function f(x)=x^4/4 - x^3/3 - 2x^2 + 4x + 5 on the interval
[-3,3] is 41 / 4  and is attained at x=3, and
the local minimum is -13/3 and it is attained for x=-2.
-/

noncomputable def f (x : ℝ) : ℝ := x^4 / 4 - x^3 / 3 - 2 * x^2 + 4 * x + 5
theorem extrema_on_interval  :
    ¬ ((∃ x : ℝ, x ∈ Set.Icc (-3) 3 ∧ (∀ y ∈ Set.Icc (-3) 3, f y ≤ f x) ∧ f x = 41/4 ∧ x = 3) ∧
  (∃ z : ℝ, z ∈ Set.Icc (-3) 3 ∧ (∀ y ∈ Set.Icc (-3) 3, f z ≤ f y) ∧ f z = - 13 / 3 ∧ z = -2)) := by
  sorry
end PBRef2

namespace PBRef3
set_option autoImplicit true
/-
The limit of the function \(\displaystyle\lim_{x\to 3}\frac{\cos(2x-6)-1}{x^3-6x^2+9x}\) is -2/3.
-/

open Filter Topology
theorem limit_of_function_at_3  :
    Tendsto (fun x : ℝ => (Real.cos (2 * x - 6) - 1) / (x^3 - 6 * x^2 + 9 * x)) (𝓝 3) (𝓝 (-2 / 3)) := by
  sorry
end PBRef3

namespace PBRef4
set_option autoImplicit true
/-
The integral of \(\int \frac{1}{x^2+1} \, dx\) is \(\arctan x + C\).
-/

open Real

noncomputable def f (x:ℝ ):ℝ := 1 / (x^2 + 1)
theorem integral_of_inv_sq_plus_one (x C: ℝ) :
    ∫ x , f x  = arctan x + C := by
  sorry
end PBRef4

namespace PBRef5
set_option autoImplicit true
/-
The derivative of the function \(f(x)=\cos(x^3)\) is \(f'(x)= -\sin(x^3)\cdot 3x^2\).
-/

open scoped Topology Filter

variable (x : ℝ)
theorem cosX3_derivative  :
    deriv (fun x => Real.cos (x^3)) x = -Real.sin (x^3) * (3 * x^2) := by
  sorry
end PBRef5

namespace PBRef6
set_option autoImplicit true
/-
Let \[F(x)=\cos^2 x-\sin^2 x,\] \[G(x)=2\cos^2x,\] \[H(x)=2\sin^2x,\] \[K(x)=\cos (2x).\] Which of the previously defined functions are anti-derivatives of the function \[\varphi(x)=-4\sin x\cdot\cos x.\] \begin{itemize} \item \textbf{(A)} \(F\) only \item \textbf{(B)} \(F\) and \(K\) only \item \textbf{(C)} \(F\), \(G\), and \(K\) only \item \textbf{(D)} \(H\) and \(K\) only \item \textbf{(E)} \(H\) only \end{itemize}
-/

open Real

-- Define the functions
noncomputable def F (x : ℝ) : ℝ := cos x ^ 2 - sin x ^ 2

noncomputable def G (x : ℝ) : ℝ := 2 * cos x ^ 2

noncomputable def H (x : ℝ) : ℝ := 2 * sin x ^ 2

noncomputable def K (x : ℝ) : ℝ := cos (2 * x)

-- Define the function φ
noncomputable def φ (x : ℝ) : ℝ := -4 * sin x * cos x

-- Theorem statement
theorem formal_statement  :
    ∀ x : ℝ, (deriv F x = φ x) ∧ (deriv K x = φ x) ∧ (deriv G x ≠ φ x) ∧ (deriv H x ≠ φ x) := by
  sorry
end PBRef6

namespace PBRef7
set_option autoImplicit true
/-
The surface integral \[\iint_G (x^2+y^2+2z)\,dS,\] where \(G\) is the part of the paraboloid \(z=7-x^2-y^2\) that lies above the \(xy\)-plane is equal to \[\frac{957\sqrt{29}-47}{20}\pi.\]
-/

variable {G : Set (ℝ × ℝ × ℝ)} (hG : G = {p : ℝ × ℝ × ℝ | p.2.2 = 7 - p.1^2 - p.2.1^2 ∧ p.2.2 ≥ 0})
theorem paraboloid_integral_value  :
    ∫ (x : ℝ) in Set.Icc (-Real.sqrt 7) (Real.sqrt 7), ∫ (y : ℝ) in Set.Icc (-Real.sqrt (7 - x^2)) (Real.sqrt (7 - x^2)),
(x^2 + y^2 + 2*(7 - x^2 - y^2)) = (957 * Real.sqrt 29 - 47) / 20 * π := by
  sorry
end PBRef7

namespace PBRef8
set_option autoImplicit true
/-
The integral of \(\sin^3 x\cos^{6}x\,dx\) is equal to \(-\frac{\cos^7 x}{7} + \frac{\cos^9 x}{9} + C\).
-/
theorem integral_sin_cube_cos_six_power (x : ℝ) :
    ∫ (x : ℝ), Real.sin x ^ 3 * Real.cos x ^ 6 = -(Real.cos x ^ 7 / 7) + Real.cos x ^ 9 / 9 + C := by
  sorry
end PBRef8

namespace PBRef9
set_option autoImplicit true
/-
The integral \(\displaystyle \int \frac{1}{\sqrt{81-x^2}}\,dx\)
is equivalent to \(\arcsin\left(\frac{x}{9}\right)+C\).
-/

open Real
theorem integral_of_one_over_sqrt_eighty_one_minus_x_squared (x C : ℝ) :
    ∫ x, 1 / sqrt (81 - x^2) = arcsin (x / 9) + C := by
  sorry
end PBRef9

namespace PBRef10
set_option autoImplicit true
/-
The derivative of the function \(f(x)=x^3\) at point \(x=4\) equals 48.
-/

open Filter

variable (f : ℝ → ℝ) (x : ℝ)
theorem derivative_of_cube_at_four  :
    deriv (fun x : ℝ => x^3) 4 = 48 := by
  sorry
end PBRef10

namespace PBRef11
set_option autoImplicit true
/-
The integral of \(\displaystyle \frac{1}{x^2-9}\,dx\) is equal to \(\frac{1}{6}\ln\left|\frac{x-3}{x+3}\right|+C\).
-/

open Real
theorem integral_of_rational_function_with_log  :
    ∀ (x : ℝ), x ≠ 3 ∧ x ≠ -3 →
  (∫ (dx : ℝ), 1 / (x^2 - 9)) = (1 / 6) * log (abs ((x - 3) / (x + 3))) + C := by
  sorry
end PBRef11

namespace PBRef12
set_option autoImplicit true
/-
Let $f(x) = \sec^2 x$. The equation of the tangent line to the graph of $f(x)$ at the point $(\pi/3, f(\pi/3))$ is given by $y = 8\sqrt{3}x + 4 - 8\sqrt{3}\pi/3$.
-/

open Real

-- Define `f(x)`: The function `f(x) = sec^2 x`.
noncomputable def f (x : ℝ) : ℝ := (1 / cos x) ^ 2

-- Lemma of `f(π/3)`: The value of `f` at `x = π/3` is `4`.
theorem value_at_pi_over_3  :
    f (π / 3) = 4 := by
  sorry
end PBRef12

namespace PBRef13
set_option autoImplicit true
/-
Let $f(x) = \sec^2 x$. The equation of the tangent line to the graph of $f(x)$ at the point $(\pi/3, f(\pi/3))$ is given by $y = 8\sqrt{3}x + 4 - 8\sqrt{3}\pi/3$.
-/

open Real

-- Define `f(x)`: The function `f(x) = sec^2 x`.
noncomputable def f (x : ℝ) : ℝ := (1 / cos x) ^ 2

-- Lemma of `f(π/3)`: The value of `f` at `x = π/3` is `4`.
axiom value_at_pi_over_3 : f (π / 3) = 4

-- Lemma of `f'(x)`: The derivative of `f(x) = sec^2 x` is `2 sec^2 x tan x`.
theorem derivative_of_f (x : ℝ) :
    HasDerivAt f (2 * (1 / cos x) ^ 2 * tan x) x := by
  sorry
end PBRef13

namespace PBRef14
set_option autoImplicit true
/-
Let $f(x) = \sec^2 x$. The equation of the tangent line to the graph of $f(x)$ at the point $(\pi/3, f(\pi/3))$ is given by $y = 8\sqrt{3}x + 4 - 8\sqrt{3}\pi/3$.
-/

open Real

-- Define `f(x)`: The function `f(x) = sec^2 x`.
noncomputable def f (x : ℝ) : ℝ := (1 / cos x) ^ 2

-- Lemma of `f(π/3)`: The value of `f` at `x = π/3` is `4`.
axiom value_at_pi_over_3 : f (π / 3) = 4

-- Lemma of `f'(x)`: The derivative of `f(x) = sec^2 x` is `2 sec^2 x tan x`.
axiom derivative_of_f (x : ℝ) : HasDerivAt f (2 * (1 / cos x) ^ 2 * tan x) x

-- Lemma of `f'(π/3)`: The value of the derivative at `x = π/3` is `8√3`.
theorem derivative_value_at_pi_over_3  :
    (2 * (1 / cos (π / 3)) ^ 2 * tan (π / 3)) = 8 * Real.sqrt 3 := by
  sorry
end PBRef14

namespace PBRef15
set_option autoImplicit true
/-
Let $f(x) = \sec^2 x$. The equation of the tangent line to the graph of $f(x)$ at the point $(\pi/3, f(\pi/3))$ is given by $y = 8\sqrt{3}x + 4 - 8\sqrt{3}\pi/3$.
-/

open Real

-- Define `f(x)`: The function `f(x) = sec^2 x`.
noncomputable def f (x : ℝ) : ℝ := (1 / cos x) ^ 2

-- Lemma of `f(π/3)`: The value of `f` at `x = π/3` is `4`.
axiom value_at_pi_over_3 : f (π / 3) = 4

-- Lemma of `f'(x)`: The derivative of `f(x) = sec^2 x` is `2 sec^2 x tan x`.
axiom derivative_of_f (x : ℝ) : HasDerivAt f (2 * (1 / cos x) ^ 2 * tan x) x

-- Lemma of `f'(π/3)`: The value of the derivative at `x = π/3` is `8√3`.
axiom derivative_value_at_pi_over_3 : (2 * (1 / cos (π / 3)) ^ 2 * tan (π / 3)) = 8 * Real.sqrt 3

-- Theorem of Tangent Line Equation: The equation of the tangent line to `f(x) = sec^2 x` at `x = π/3` is `y = 8√3 x + 4 - 8√3 π/3`.
theorem tangent_line_equation  :
    ∀ x y : ℝ, y = 8 * Real.sqrt 3 * (x - π / 3) + 4 ↔
y - f (π / 3) = (2 * (1 / cos (π / 3)) ^ 2 * tan (π / 3)) * (x - π / 3) := by
  sorry
end PBRef15

namespace PBRef16
set_option autoImplicit true
/-
Let $f(x) = \sec^2 x$. The equation of the tangent line to the graph of $f(x)$ at the point $(\pi/3, f(\pi/3))$ is given by $y = 8\sqrt{3}x + 4 - 8\sqrt{3}\pi/3$.
-/

open Real

-- Define `f(x)`: The function `f(x) = sec^2 x`.
noncomputable def f (x : ℝ) : ℝ := (1 / cos x) ^ 2

-- Lemma of `f(π/3)`: The value of `f` at `x = π/3` is `4`.
axiom value_at_pi_over_3 : f (π / 3) = 4

-- Lemma of `f'(x)`: The derivative of `f(x) = sec^2 x` is `2 sec^2 x tan x`.
axiom derivative_of_f (x : ℝ) : HasDerivAt f (2 * (1 / cos x) ^ 2 * tan x) x

-- Lemma of `f'(π/3)`: The value of the derivative at `x = π/3` is `8√3`.
axiom derivative_value_at_pi_over_3 : (2 * (1 / cos (π / 3)) ^ 2 * tan (π / 3)) = 8 * Real.sqrt 3

-- Theorem of Tangent Line Equation: The equation of the tangent line to `f(x) = sec^2 x` at `x = π/3` is `y = 8√3 x + 4 - 8√3 π/3`.
axiom tangent_line_equation :
∀ x y : ℝ, y = 8 * Real.sqrt 3 * (x - π / 3) + 4 ↔
y - f (π / 3) = (2 * (1 / cos (π / 3)) ^ 2 * tan (π / 3)) * (x - π / 3)

-- Proof that this is indeed the tangent line
theorem is_tangent_line  :
    HasDerivAt f (8 * Real.sqrt 3) (π / 3) ∧
  f (π / 3) = 8 * Real.sqrt 3 * (π / 3 - π / 3) + 4 := by
  sorry
end PBRef16

namespace PBRef17
set_option autoImplicit true
/-
The value of the integral \[\iiint_D e^{x^2+y^2}\,dV\] where \(D\) is the the region
in bounded by the planes \(y=0\), \(z=0\), \(y=x\),
and the paraboloid \(z=4-x^2-y^2\) is \[\frac{\left(e^4-5\right)\pi}8\].
-/

open MeasureTheory

variable {D : Type} [MeasurableSpace D] [MeasureSpace D]

-- Define the set D as a variable
variable (D : Set (Fin 3 → ℝ))
theorem integral_value_over_region (D : Set (Fin 3 → ℝ)) (hD : D = {p : Fin 3 → ℝ | p 2 ≥ 0 ∧ p 3 ≥ 0 ∧ p 2 ≤ p 1 ∧ p 3 ≤ 4 - p 1^2 - p 2^2}) :
    let integrand := fun p : Fin 3 → ℝ => Real.exp (p 1^2 + p 2^2)
  ∫ p in D, integrand p = (Real.exp 4 - 5) * π / 8 := by
  sorry
end PBRef17

namespace PBRef18
set_option autoImplicit true
/-
Prove that \(\displaystyle \lim_{x\to 0}\frac{1-\cos x}{x^2}=\frac12\).
-/

open Filter Topology
/-- Version 1: Using explicit domain restriction -/
theorem limit_of_cosine_difference_quotient  :
    ¬ (Tendsto (fun x => if x ≠ 0 then (1 - Real.cos x) / x^2 else 1/2) (𝓝 0) (𝓝 (1/2)) ) := by
  sorry
end PBRef18

namespace PBRef19
set_option autoImplicit true
/-
The limit of the function \(f(x)=\frac{\sin(5x^2)}{x^2}\) as \(x\) approaches 0 is 5.
-/

open Filter Topology Real
theorem limit_of_sin_5x2_over_x2_as_x_approaches_0  :
    Tendsto (fun x => (sin (5 * x^2)) / x^2) (𝓝 0) (𝓝 5) := by
  sorry
end PBRef19

namespace PBRef20
set_option autoImplicit true
/-
The integral \(\int \frac{1}{\cos^2 x} \, dx\) equals to \(\tan x + C\).
-/

-- Define the constant C for the integration constant
variable (C : ℝ)

-- Theorem: The indefinite integral of 1/cos^2(x) with respect to x is tan(x) + C.
theorem integral_of_one_over_cos_sq (x : ℝ) :
    ∫ (x : ℝ), 1 / (Real.cos x ^ 2) = Real.tan x + C := by
  sorry
end PBRef20

namespace PBRef21
set_option autoImplicit true
/-
The integral of the function (1/x + x^2) with respect to x from 2 to 8 equals the natural logarithm of 4 plus 168.
-/

open Real
theorem integral_of_function_equals_ln_plus_168  :
    (∫ x in Set.Icc 2 8, (1 / x + x^2) : ℝ) = Real.log 4 + 168 := by
  sorry
end PBRef21

namespace PBRef22
set_option autoImplicit true
/-
The integral \[ \int_{0}^{\frac{\pi}{2}} \ln{(\sin{x})} \,dx \] is equal to -\frac{\pi}{2} \ln{2}.
-/

open Real

variable (x : ℝ)
theorem integral_ln_sin_pi_over_two  :
    ∫ x in Set.Icc 0 (π / 2), log (sin x) = - (π / 2) * log 2 := by
  sorry
end PBRef22

namespace PBRef23
set_option autoImplicit true
/-
The derivative of the composite function \(f(x)=u(v(x))\) at \(x=0\), given that \(u\) and \(v\) are functions satisfying \(u(0)=1\), \(u(1)=2\), \(u(2)=3\), \(v(0)=2\), \(v(1)=3\), \(v(2)=4\), \(u^{\prime}(0)=4\), \(u^{\prime}(1)=5\), \(u^{\prime}(2)=6\), \(v^{\prime}(0)=7\), \(v^{\prime}(1)=8\), \(v^{\prime}(2)=9\), is 42.
-/

variable {u v : ℝ → ℝ} (u_val : u 0 = 1 ∧ u 1 = 2 ∧ u 2 = 3) (v_val : v 0 = 2 ∧ v 1 = 3 ∧ v 2 = 4)

variable (u_deriv : deriv u 0 = 4 ∧ deriv u 1 = 5 ∧ deriv u 2 = 6) (v_deriv : deriv v 0 = 7 ∧ deriv v 1 = 8 ∧ deriv v 2 = 9)
theorem composite_derivative_at_zero  :
    deriv (fun x => u (v x)) 0 = 42 := by
  sorry
end PBRef23

namespace PBRef24
set_option autoImplicit true
/-
The maximal value of the function \(f(x,y,z)=xy+yz+zx\), given that \(x\), \(y\), and \(z\)
are real numbers that satisfy \(x^2+y^2+z^2=1\) is 1, which occurs when \(x=y=z=\frac1{\sqrt 3}\).
-/

variable {x y z : ℝ}

-- Define the function f
def f : ℝ × ℝ × ℝ → ℝ := λ (x, y, z) => x * y + y * z + z * x
theorem max_value_of_function_under_constraint  :
    (x^2 + y^2 + z^2 = 1) → f (x, y, z) ≤ 1 ∧ (f (x, y, z) = 1 ↔ x = 1 / Real.sqrt 3 ∧ y = 1 / Real.sqrt 3 ∧ z = 1 / Real.sqrt 3) := by
  sorry
end PBRef24

namespace PBRef25
set_option autoImplicit true
/-
The value of the integral \[\int_3^9 (x^2-3) dx,\] is 216 according to the Fundamental Theorem of Calculus.
-/

open Real

-- Define the polynomial function
noncomputable def f (x : ℝ) : ℝ := x^2 - 3

-- Theorem statement
theorem integral_of_polynomial  :
    ∫ x in Set.Icc 3 9, f x = 216 := by
  sorry
end PBRef25

namespace PBRef26
set_option autoImplicit true
/-
Let $a_n = \frac{3^n+2^n}{3^{n+1}-2^{n+1}}$ for $n \in \mathbb{N}$. Then,

  $\lim_{n\rightarrow\infty} a_n = \frac{1}{3}$
-/

open Real
open Filter (Tendsto)

variable (n : ℕ)

/-- Define `a_n`: The sequence defined by a_n = (3^n + 2^n) / (3^(n+1) - 2^(n+1)) -/
noncomputable def a_n (n : ℕ) : ℝ := (3^n + 2^n) / (3^(n+1) - 2^(n+1))
/-- Lemma 1: Rewrite a_n as (1 + (2/3)^n) / (3 * (1 - (2/3)^(n+1))) -/
theorem sequence_rewrite (n : ℕ) :
    a_n n = (1 + (2/3)^n) / (3 * (1 - (2/3)^(n+1))) := by
  sorry
end PBRef26

namespace PBRef27
set_option autoImplicit true
/-
Let $a_n = \frac{3^n+2^n}{3^{n+1}-2^{n+1}}$ for $n \in \mathbb{N}$. Then,

  $\lim_{n\rightarrow\infty} a_n = \frac{1}{3}$
-/

open Real
open Filter (Tendsto)

variable (n : ℕ)

/-- Define `a_n`: The sequence defined by a_n = (3^n + 2^n) / (3^(n+1) - 2^(n+1)) -/
noncomputable def a_n (n : ℕ) : ℝ := (3^n + 2^n) / (3^(n+1) - 2^(n+1))

/-- Lemma 1: Rewrite a_n as (1 + (2/3)^n) / (3 * (1 - (2/3)^(n+1))) -/
axiom sequence_rewrite (n : ℕ) : a_n n = (1 + (2/3)^n) / (3 * (1 - (2/3)^(n+1)))
/-- Lemma 2: As n approaches infinity, (2/3)^n approaches 0 -/
theorem geometric_limit  :
    Tendsto (λ n : ℕ => (2/3 : ℝ)^n) Filter.atTop (nhds 0) := by
  sorry
end PBRef27

namespace PBRef28
set_option autoImplicit true
/-
Let $a_n = \frac{3^n+2^n}{3^{n+1}-2^{n+1}}$ for $n \in \mathbb{N}$. Then,

  $\lim_{n\rightarrow\infty} a_n = \frac{1}{3}$
-/

open Real
open Filter (Tendsto)

variable (n : ℕ)

/-- Define `a_n`: The sequence defined by a_n = (3^n + 2^n) / (3^(n+1) - 2^(n+1)) -/
noncomputable def a_n (n : ℕ) : ℝ := (3^n + 2^n) / (3^(n+1) - 2^(n+1))

/-- Lemma 1: Rewrite a_n as (1 + (2/3)^n) / (3 * (1 - (2/3)^(n+1))) -/
axiom sequence_rewrite (n : ℕ) : a_n n = (1 + (2/3)^n) / (3 * (1 - (2/3)^(n+1)))

/-- Lemma 2: As n approaches infinity, (2/3)^n approaches 0 -/
axiom geometric_limit :
  Tendsto (λ n : ℕ => (2/3 : ℝ)^n) Filter.atTop (nhds 0)
theorem sequence_limit  :
    Filter.Tendsto a_n Filter.atTop (nhds (1/3)) := by
  sorry
end PBRef28

namespace PBRef29
set_option autoImplicit true
/-
The limit of the function \(\displaystyle \lim_{x\to +\infty}\frac{\sin\left(2x+x^3\right)}{x+3x^3}\) as x approaches infinity is equal to 0.
-/

open Filter Topology Real
theorem limit_of_sin_fraction_as_x_approaches_infinity  :
    Tendsto (fun x : ℝ => sin (2 * x + x^3) / (x + 3 * x^3)) atTop (𝓝 0) := by
  sorry
end PBRef29

namespace PBRef30
set_option autoImplicit true
/-
The function \(f(x)=\cos(3x+x^2)\) is differentiable for \(x\in\mathbb R\) and its derivative \(f^{\prime}(x)\) is \(-\sin(3x+x^2)\cdot (3+2x)\).
-/

open Real
theorem cosine_derivative_formula (x : ℝ) :
    deriv (fun x => cos (3 * x + x^2)) x = -sin (3 * x + x^2) * (3 + 2 * x) := by
  sorry
end PBRef30

namespace PBRef31
set_option autoImplicit true
/-
The derivative of \(f(x)=e^x\) at \(x=e\) is \(e^e\).
-/

open Real
theorem derivative_of_exp_at_e  :
    deriv (fun x => exp x) e = exp e := by
  sorry
end PBRef31

namespace PBRef32
set_option autoImplicit true
/-
The partial derivative of the function g(s,t)=f(x(s,t),y(s,t),z(s,t))
with respect to ∂t evaluated at (2,π) is 24π², where:
  f(x,y,z) = x² + y³ + z⁴
  x(s,t) = s·cos(t)
  y(s,t) = s·t
  z(s,t) = s²
-/

open Real
open Function

/-- The main function f(x,y,z) = x² + y³ + z⁴ -/
noncomputable def f (x y z : ℝ) : ℝ := x^2 + y^3 + z^4

/-- x(s,t) = s·cos(t) -/
noncomputable def x (s t : ℝ) : ℝ := s * cos t

/-- y(s,t) = s·t -/
noncomputable def y (s t : ℝ) : ℝ := s * t

/-- z(s,t) = s² -/
noncomputable def z (s : ℝ) : ℝ := s^2

/-- The composite function g(s,t) = f(x(s,t), y(s,t), z(s,t)) -/
noncomputable def g (s t : ℝ) : ℝ :=
  f (x s t) (y s t) (z s)

/-- Partial derivative of g with respect to t -/
noncomputable def partial_t (s t : ℝ) : ℝ :=
  deriv (fun τ => g s τ) t
/-- Main theorem: The partial derivative ∂g/∂t at (2,π) equals 24π² -/
theorem partial_derivative_example  :
    partial_t 2 π = 24 * π^2 := by
  sorry
end PBRef32

namespace PBRef33
set_option autoImplicit true
open Polynomial Set

/-- Define the parabola as a polynomial x² + 3 -/
noncomputable def parabola_poly : Polynomial ℝ :=
  X^2 + C 3

/-- Convert polynomial to real function -/
noncomputable def parabola_fun (x : ℝ) : ℝ :=
  aeval x parabola_poly
/-- The area under the parabola between x=1 and x=3 is 44/3 -/
theorem area_under_parabola_from_1_to_3  :
    (∫ x in Icc 1 3, parabola_fun x) = 44/3 := by
  sorry
end PBRef33

namespace PBRef34
set_option autoImplicit true
/-
The integral of \(\frac{1}{x^2 + 1}\) with respect to \(x\) equals to the arctangent function \(\arctan x + C\).
-/

open Real
theorem integral_of_one_over_x_squared_plus_one (x : ℝ) :
    ∫ y in Set.Icc 0 x, (1 : ℝ) / (y^2 + 1) = arctan x - arctan 0 := by
  sorry
end PBRef34

namespace PBRef35
set_option autoImplicit true
/-
The value of \(f_y(7,1)\) for the function \(f(x,y) = xy^2 + x^2y\) is 63.
-/

-- Define the function f(x, y) = x * y^2 + x^2 * y
noncomputable def f (x y : ℤ) : ℤ := x * y^2 + x^2 * y

-- Theorem statement: The value of f(7, 1) is 56
theorem function_evaluation_example  :
    f 7 1 = 56 := by
  sorry
end PBRef35

namespace PBRef36
set_option autoImplicit true
/-
The integral of \(\int_0^a \sqrt{a^2-x^2} \,dx\) is \(\frac{a^2 \pi}{4}\).
-/

open Real

variable {a : ℝ} (ha : 0 < a)
theorem integral_sqrt_a2_minus_x2_eq_a2_pi_div_4  :
    ∫ x in Set.Icc 0 a, sqrt (a^2 - x^2) = a^2 * π / 4 := by
  sorry
end PBRef36

namespace PBRef37
set_option autoImplicit true
/-
The integral of 1 over cos^2x dx is equal to tan x + C.
-/

open intervalIntegral
open Real
theorem integral_of_one_over_cos_squared (x C: ℝ) :
    ∫ x , 1 / cos x ^ 2 = tan x + C := by
  sorry
end PBRef37

namespace PBRef38
set_option autoImplicit true
/-
The composition of the functions \(u(x)=\sin x\) and \(v(x)=x^2\) is \(u(v(x))=\sin(x^2)\).
-/

-- Define the sine function
noncomputable def u (x : ℝ) : ℝ := Real.sin x

-- Define the quadratic function
def v (x : ℝ) : ℝ := x ^ 2

-- Theorem statement for the composition of u and v
theorem composition_of_sine_and_quadratic (x : ℝ) :
    u (v x) = Real.sin (x ^ 2) := by
  sorry
end PBRef38

namespace PBRef39
set_option autoImplicit true
/-
The length of the curve obtained by a moving paint nozzle that rotates around a rotating paraboloid in unit time is given by the integral
(without evaluating) \[\int_0^1\sqrt{1+\left(4+4\pi^2\right)t^2}\,dt.\]
-/

-- Define the integrand function
noncomputable def integrand (t : ℝ) : ℝ := Real.sqrt (1 + (4 + 4 * Real.pi ^ 2) * t ^ 2)

-- Theorem statement
theorem curveLength_integral  :
    ∫ (t : ℝ) in Set.Icc 0 1, integrand t = ∫ (t : ℝ) in Set.Icc 0 1, Real.sqrt (1 + (4 + 4 * Real.pi ^ 2) * t ^ 2) := by
  sorry
end PBRef39

namespace PBRef40
set_option autoImplicit true
/-
Let $f(x) = x^3-9x^2+24x$ be a real-valued function defined on $\mathbb{R}$. Then:
  1. $f(x)$ has a local maximum at $x=2$.
  2. $f(x)$ has a local minimum at $x=4$.
  3. These are the only local extrema of $f(x)$ on $\mathbb{R}$.
-/

open Real

variable (x : ℝ)

/-- The cubic polynomial f(x) = x³ - 9x² + 24x -/
noncomputable def f (x : ℝ) : ℝ := x^3 - 9*x^2 + 24*x

/-- The first derivative f'(x) = 3x² - 18x + 24 -/
noncomputable def f_deriv (x : ℝ) : ℝ := 3*x^2 - 18*x + 24

/-- The second derivative f''(x) = 6x - 18 -/
noncomputable def f_second_deriv (x : ℝ) : ℝ := 6*x - 18
/-- Lemma: Critical points are x = 2 and x = 4 -/
theorem critical_points  :
    f_deriv x = 0 ↔ x = 2 ∨ x = 4 := by
  sorry
end PBRef40

namespace PBRef41
set_option autoImplicit true
/-
Let $f(x) = x^3-9x^2+24x$ be a real-valued function defined on $\mathbb{R}$. Then:
  1. $f(x)$ has a local maximum at $x=2$.
  2. $f(x)$ has a local minimum at $x=4$.
  3. These are the only local extrema of $f(x)$ on $\mathbb{R}$.
-/

open Real

variable (x : ℝ)

/-- The cubic polynomial f(x) = x³ - 9x² + 24x -/
noncomputable def f (x : ℝ) : ℝ := x^3 - 9*x^2 + 24*x

/-- The first derivative f'(x) = 3x² - 18x + 24 -/
noncomputable def f_deriv (x : ℝ) : ℝ := 3*x^2 - 18*x + 24

/-- The second derivative f''(x) = 6x - 18 -/
noncomputable def f_second_deriv (x : ℝ) : ℝ := 6*x - 18

/-- Lemma: Critical points are x = 2 and x = 4 -/
axiom critical_points : f_deriv x = 0 ↔ x = 2 ∨ x = 4
/-- Lemma: Second derivative test -/
theorem second_derivative_test (x : ℝ) (h : f_deriv x = 0) :
    (x = 2 ∧ f_second_deriv x < 0) ∨ (x = 4 ∧ f_second_deriv x > 0) := by
  sorry
end PBRef41

namespace PBRef42
set_option autoImplicit true
/-
Let $f(x) = x^3-9x^2+24x$ be a real-valued function defined on $\mathbb{R}$. Then:
  1. $f(x)$ has a local maximum at $x=2$.
  2. $f(x)$ has a local minimum at $x=4$.
  3. These are the only local extrema of $f(x)$ on $\mathbb{R}$.
-/

open Real

variable (x : ℝ)

/-- The cubic polynomial f(x) = x³ - 9x² + 24x -/
noncomputable def f (x : ℝ) : ℝ := x^3 - 9*x^2 + 24*x

/-- The first derivative f'(x) = 3x² - 18x + 24 -/
noncomputable def f_deriv (x : ℝ) : ℝ := 3*x^2 - 18*x + 24

/-- The second derivative f''(x) = 6x - 18 -/
noncomputable def f_second_deriv (x : ℝ) : ℝ := 6*x - 18

/-- Lemma: Critical points are x = 2 and x = 4 -/
axiom critical_points : f_deriv x = 0 ↔ x = 2 ∨ x = 4

/-- Lemma: Second derivative test -/
axiom second_derivative_test (x : ℝ) (h : f_deriv x = 0) :
  (x = 2 ∧ f_second_deriv x < 0) ∨ (x = 4 ∧ f_second_deriv x > 0)
/-- Theorem: f(x) has a local maximum at x = 2 -/
theorem local_max_at_2  :
    IsLocalMax f 2 := by
  sorry
end PBRef42

namespace PBRef43
set_option autoImplicit true
/-
Let $f(x) = x^3-9x^2+24x$ be a real-valued function defined on $\mathbb{R}$. Then:
  1. $f(x)$ has a local maximum at $x=2$.
  2. $f(x)$ has a local minimum at $x=4$.
  3. These are the only local extrema of $f(x)$ on $\mathbb{R}$.
-/

open Real

variable (x : ℝ)

/-- The cubic polynomial f(x) = x³ - 9x² + 24x -/
noncomputable def f (x : ℝ) : ℝ := x^3 - 9*x^2 + 24*x

/-- The first derivative f'(x) = 3x² - 18x + 24 -/
noncomputable def f_deriv (x : ℝ) : ℝ := 3*x^2 - 18*x + 24

/-- The second derivative f''(x) = 6x - 18 -/
noncomputable def f_second_deriv (x : ℝ) : ℝ := 6*x - 18

/-- Lemma: Critical points are x = 2 and x = 4 -/
axiom critical_points : f_deriv x = 0 ↔ x = 2 ∨ x = 4

/-- Lemma: Second derivative test -/
axiom second_derivative_test (x : ℝ) (h : f_deriv x = 0) :
  (x = 2 ∧ f_second_deriv x < 0) ∨ (x = 4 ∧ f_second_deriv x > 0)

/-- Theorem: f(x) has a local maximum at x = 2 -/
axiom local_max_at_2 : IsLocalMax f 2
/-- Theorem: f(x) has a local minimum at x = 4 -/
theorem local_min_at_4  :
    IsLocalMin f 4 := by
  sorry
end PBRef43

namespace PBRef44
set_option autoImplicit true
/-
Let $f(x) = x^3-9x^2+24x$ be a real-valued function defined on $\mathbb{R}$. Then:
  1. $f(x)$ has a local maximum at $x=2$.
  2. $f(x)$ has a local minimum at $x=4$.
  3. These are the only local extrema of $f(x)$ on $\mathbb{R}$.
-/

open Real

variable (x : ℝ)

/-- The cubic polynomial f(x) = x³ - 9x² + 24x -/
noncomputable def f (x : ℝ) : ℝ := x^3 - 9*x^2 + 24*x

/-- The first derivative f'(x) = 3x² - 18x + 24 -/
noncomputable def f_deriv (x : ℝ) : ℝ := 3*x^2 - 18*x + 24

/-- The second derivative f''(x) = 6x - 18 -/
noncomputable def f_second_deriv (x : ℝ) : ℝ := 6*x - 18

/-- Lemma: Critical points are x = 2 and x = 4 -/
axiom critical_points : f_deriv x = 0 ↔ x = 2 ∨ x = 4

/-- Lemma: Second derivative test -/
axiom second_derivative_test (x : ℝ) (h : f_deriv x = 0) :
  (x = 2 ∧ f_second_deriv x < 0) ∨ (x = 4 ∧ f_second_deriv x > 0)

/-- Theorem: f(x) has a local maximum at x = 2 -/
axiom local_max_at_2 : IsLocalMax f 2

/-- Theorem: f(x) has a local minimum at x = 4 -/
axiom local_min_at_4 : IsLocalMin f 4
/-- Theorem: x = 2 and x = 4 are the only local extrema of f(x) -/
theorem only_local_extrema (x : ℝ) :
    IsLocalMax f x ∨ IsLocalMin f x → x = 2 ∨ x = 4 := by
  sorry
end PBRef44

namespace PBRef45
set_option autoImplicit true
/-
Let $f(x) = x^3-9x^2+24x$ be a real-valued function defined on $\mathbb{R}$. Then:
  1. $f(x)$ has a local maximum at $x=2$.
  2. $f(x)$ has a local minimum at $x=4$.
  3. These are the only local extrema of $f(x)$ on $\mathbb{R}$.
-/

open Real

variable (x : ℝ)

/-- The cubic polynomial f(x) = x³ - 9x² + 24x -/
noncomputable def f (x : ℝ) : ℝ := x^3 - 9*x^2 + 24*x

/-- The first derivative f'(x) = 3x² - 18x + 24 -/
noncomputable def f_deriv (x : ℝ) : ℝ := 3*x^2 - 18*x + 24

/-- The second derivative f''(x) = 6x - 18 -/
noncomputable def f_second_deriv (x : ℝ) : ℝ := 6*x - 18

/-- Lemma: Critical points are x = 2 and x = 4 -/
axiom critical_points : f_deriv x = 0 ↔ x = 2 ∨ x = 4

/-- Lemma: Second derivative test -/
axiom second_derivative_test (x : ℝ) (h : f_deriv x = 0) :
  (x = 2 ∧ f_second_deriv x < 0) ∨ (x = 4 ∧ f_second_deriv x > 0)

/-- Theorem: f(x) has a local maximum at x = 2 -/
axiom local_max_at_2 : IsLocalMax f 2

/-- Theorem: f(x) has a local minimum at x = 4 -/
axiom local_min_at_4 : IsLocalMin f 4

/-- Theorem: x = 2 and x = 4 are the only local extrema of f(x) -/
axiom only_local_extrema (x : ℝ) :
IsLocalMax f x ∨ IsLocalMin f x → x = 2 ∨ x = 4
/-- Theorem: Local extrema of f(x) -/
theorem local_extrema  :
    (∃ x, IsLocalMax f x) ∧ (∃ x, IsLocalMin f x) ∧
(∀ x, IsLocalMax f x ∨ IsLocalMin f x → x = 2 ∨ x = 4) := by
  sorry
end PBRef45

namespace PBRef46
set_option autoImplicit true
/-
The integral of \(x^p\) with respect to \(x\) where \(p\) is a real number different from -1, is given by \(\frac{x^{p+1}}{p+1} + C\).
-/
theorem integral_of_power_function (p : ℝ) (hp : p ≠ -1) :
    ∫ x in Set.Icc 0 1, x^p = (1^(p+1) - 0^(p+1)) / (p+1) := by
  sorry
end PBRef46

namespace PBRef47
set_option autoImplicit true
/-
The indefinite integral \(\int \frac{\sin\sqrt{x}}{\sqrt{x}}\,dx\) is equal to \(-2 \cos (\sqrt{x}) + C\).
-/

open Real
theorem sin_sqrt_x_over_sqrt_x_integral (x C: ℝ) :
    ∫ (x : ℝ), sin (sqrt x) / sqrt x = -2 * cos (sqrt x) + C := by
  sorry
end PBRef47

namespace PBRef48
set_option autoImplicit true
/-
The points (x,y) on the curve \(x^2+y^2=1\) for which the quantity \(f(x,y)=xy\) is maximal are
\((x,y)\in\left\{\left(\frac1{\sqrt 2},\frac1{\sqrt2}\right),
\left(-\frac1{\sqrt 2},-\frac1{\sqrt 2}\right)\right\}\) and the maximum of \(f\) is \(\frac12\).
-/

open Real

variable (x y : ℝ)
theorem max_xy_on_unit_circle  :
    (x^2 + y^2 = 1) → (x * y ≤ 1 / 2) ∧ ((x = 1 / sqrt 2 ∧ y = 1 / sqrt 2) ∨ (x = -1 / sqrt 2 ∧ y = -1 / sqrt 2)) → (x * y = 1 / 2) := by
  sorry
end PBRef48

namespace PBRef49
set_option autoImplicit true
/-
The integral \(\displaystyle \int \sin^{10}x\cos x \,dx\) is equal to
\(\frac{\sin^{11} x}{11} + C\), where C is the constant of integration.
-/

open Real
theorem integral_sin_pow_ten_cos (x C: ℝ) :
    ∫ x , (sin x)^10 * cos x = (sin x)^11 / 11 +C := by
  sorry
end PBRef49

namespace PBRef50
set_option autoImplicit true
/-
The derivative of the function \(f(x)=e^{-\frac{x^2}2}\) is \(f^{\prime}(x)=-xe^{-\frac{x^2}2}\).
-/

open Real
theorem derivative_of_exponential_function  :
    deriv (fun x => exp (-x^2 / 2)) = fun x => -x * exp (-x^2 / 2) := by
  sorry
end PBRef50

namespace PBRef51
set_option autoImplicit true
/-
The limit of the function \(\displaystyle \lim_{x\to0}\frac{ e^{8x}-1}{x}\) is 8.
-/

open Filter Topology

variable (x : ℝ)
theorem limit_of_function  :
    Tendsto (fun x => (Real.exp (8 * x) - 1) / x) (𝓝[Set.Ioi 0] 0) (𝓝 8) := by
  sorry
end PBRef51

namespace PBRef52
set_option autoImplicit true
/-
The integral \(\displaystyle \int \sin^3 x\cos^{6}x\,dx\) is equal to -\frac{\cos^9x}9+\frac{\cos^{11}x}{11}+C.
-/

open Real
theorem integral_sin_cube_cos_sixth (x : ℝ) :
    ∫ (x : ℝ), sin x ^ 3 * cos x ^ 6 = -cos x ^ 9 / 9 + cos x ^ 11 / 11 + C := by
  sorry
end PBRef52

namespace PBRef53
set_option autoImplicit true
/-
Let $y(t) = 40t - 16t^2$ represent the height in feet of a ball $t$ seconds after being thrown vertically upward with an initial velocity of 40 ft/s. Then the average velocity $v_{avg}$ of the ball over the time interval $[2, 2.5]$ seconds is given by:

    $v_{avg} = \frac{y(2.5) - y(2)}{2.5 - 2} = -32 \text{ ft/s}$
-/

open Real

noncomputable def heightFunction (t : ℝ) : ℝ := 40 * t - 16 * t^2
theorem heightAtTwo  :
    heightFunction 2 = 16 := by
  sorry
end PBRef53

namespace PBRef54
set_option autoImplicit true
/-
Let $y(t) = 40t - 16t^2$ represent the height in feet of a ball $t$ seconds after being thrown vertically upward with an initial velocity of 40 ft/s. Then the average velocity $v_{avg}$ of the ball over the time interval $[2, 2.5]$ seconds is given by:

    $v_{avg} = \frac{y(2.5) - y(2)}{2.5 - 2} = -32 \text{ ft/s}$
-/

open Real

noncomputable def heightFunction (t : ℝ) : ℝ := 40 * t - 16 * t^2

axiom heightAtTwo : heightFunction 2 = 16
theorem heightAtTwoPointFive  :
    heightFunction 2.5 = 0 := by
  sorry
end PBRef54

namespace PBRef55
set_option autoImplicit true
/-
Let $y(t) = 40t - 16t^2$ represent the height in feet of a ball $t$ seconds after being thrown vertically upward with an initial velocity of 40 ft/s. Then the average velocity $v_{avg}$ of the ball over the time interval $[2, 2.5]$ seconds is given by:

    $v_{avg} = \frac{y(2.5) - y(2)}{2.5 - 2} = -32 \text{ ft/s}$
-/

open Real

noncomputable def heightFunction (t : ℝ) : ℝ := 40 * t - 16 * t^2

axiom heightAtTwo : heightFunction 2 = 16

axiom heightAtTwoPointFive : heightFunction 2.5 = 0
theorem averageVelocity  :
    (heightFunction 2.5 - heightFunction 2) / (2.5 - 2) = -32 := by
  sorry
end PBRef55

namespace PBRef56
set_option autoImplicit true
/-
Let $y(t) = 40t - 16t^2$ represent the height in feet of a ball $t$ seconds after being thrown vertically upward with an initial velocity of 40 ft/s. Then the average velocity $v_{avg}$ of the ball over the time interval $[2, 2.5]$ seconds is given by:

    $v_{avg} = \frac{y(2.5) - y(2)}{2.5 - 2} = -32 \text{ ft/s}$
-/

open Real

noncomputable def heightFunction (t : ℝ) : ℝ := 40 * t - 16 * t^2

axiom heightAtTwo : heightFunction 2 = 16

axiom heightAtTwoPointFive : heightFunction 2.5 = 0

axiom averageVelocity : (heightFunction 2.5 - heightFunction 2) / (2.5 - 2) = -32
theorem graphSatisfiesAvgVelocity  :
    (2.5 - 2) * -32 = heightFunction 2.5 - heightFunction 2 := by
  sorry
end PBRef56

namespace PBRef57
set_option autoImplicit true
/-
The limit of the function \[\lim_{x\to 0}\frac{1-(\cos x)^{\sin x}}{x^3}\] is 1/2.
-/

open Filter Topology
theorem limit_of_function_at_zero  :
    Tendsto (fun x => (1 - (Real.cos x)^(Real.sin x)) / x^3) (𝓝 0) (𝓝 (1 / 2)) := by
  sorry
end PBRef57

namespace PBRef58
set_option autoImplicit true
/-
The integral \(\displaystyle \int \frac{2\sin^3x+\sin^2x\cos x-4\sin x\cos^2x+3\cos^3x}{\left(\sin^2x-\sin x\cos x-2\cos^2x\right)\cos x}\,dx\) is equal to \(\ln\left|\tan x-2\right|-\ln\left|\tan x+1\right|-2\ln\left|\cos x\right|+C\).
-/

-- Define the integral function
noncomputable def integralFunction (x : ℝ) : ℝ :=
  (2 * Real.sin x ^ 3 + Real.sin x ^ 2 * Real.cos x - 4 * Real.sin x * Real.cos x ^ 2 + 3 * Real.cos x ^ 3) / ((Real.sin x ^ 2 - Real.sin x * Real.cos x - 2 * Real.cos x ^ 2) * Real.cos x)

-- Theorem statement
theorem trigonometric_integral_result  :
    ∀ x : ℝ, ∃ C : ℝ, ∫ x, integralFunction x = Real.log (abs (Real.tan x - 2)) - Real.log (abs (Real.tan x + 1)) - 2 * Real.log (abs (Real.cos x)) + C := by
  sorry
end PBRef58

namespace PBRef59
set_option autoImplicit true
/-
The evaluated integral of \(\displaystyle \int \sqrt{x -5}\,dx\) is \(\frac{2}{3} (x - 5)^{3/2} + C\).
-/

-- Define the theorem statement
theorem integral_sqrt_x_minus_5 (x : ℝ) :
    ∫ (x : ℝ), Real.sqrt (x - 5) = (2 / 3) * (x - 5) ^ (3 / 2) + C := by
  sorry
end PBRef59

namespace PBRef60
set_option autoImplicit true
/-
The indefinite integral \[\int \frac{x}{x^2+1}\,dx\] is equal to \[\frac12\ln(x^2+1)+C.\]
-/

-- Define the function to be integrated
noncomputable def integrand (x : ℝ) : ℝ := x / (x^2 + 1)

-- Theorem statement
theorem integral_of_integrand2  :
    ∃ F : ℝ → ℝ, ∀ x : ℝ, (deriv F x = integrand x) ∧ F x = (1 / 2) * Real.log (x^2 + 1) + C := by
  sorry
end PBRef60

namespace PBRef61
set_option autoImplicit true
/-
For all real numbers x, the cosine function cos(x) can be expressed as the following infinite series:

    $\cos(x) = \sum_{n=0}^{\infty} \frac{(-1)^n}{(2n)!} x^{2n}$

    where this series converges for all x in the interval (-∞, +∞).
-/

open Real

variable (x : ℝ)

/-- The Taylor series expansion of cos(x) -/
noncomputable def cos_taylor_series (x : ℝ) : ℝ := ∑' (n : ℕ), ((-1 : ℝ)^n / (2 * n).factorial) * x^(2 * n)
/-- Proof that the Taylor series of cos(x) converges for all real numbers x -/
theorem cos_taylor_series_converges (x : ℝ) :
    HasSum (λ n : ℕ => ((-1 : ℝ)^n / (2 * n).factorial) * x^(2 * n)) (cos x) := by
  sorry
end PBRef61

namespace PBRef62
set_option autoImplicit true
/-
For all real numbers x, the cosine function cos(x) can be expressed as the following infinite series:

    $\cos(x) = \sum_{n=0}^{\infty} \frac{(-1)^n}{(2n)!} x^{2n}$

    where this series converges for all x in the interval (-∞, +∞).
-/

open Real

variable (x : ℝ)

/-- The Taylor series expansion of cos(x) -/
noncomputable def cos_taylor_series (x : ℝ) : ℝ := ∑' (n : ℕ), ((-1 : ℝ)^n / (2 * n).factorial) * x^(2 * n)

/-- Proof that the Taylor series of cos(x) converges for all real numbers x -/
axiom cos_taylor_series_converges (x : ℝ) : HasSum (λ n : ℕ => ((-1 : ℝ)^n / (2 * n).factorial) * x^(2 * n)) (cos x)
/-- The cosine function can be expressed as the infinite series -/
theorem cos_infinite_series (x : ℝ) :
    cos x = cos_taylor_series x := by
  sorry
end PBRef62

namespace PBRef63
set_option autoImplicit true
/-
The integral \[\int_{-1}^1 \frac{x^2}{1+x^2}\,dx\] is equal to \[2-\frac{\pi}2.\]
-/

open Real
open MeasureTheory
theorem integral_of_rational_function_over_interval  :
    ∫ x in Set.Icc (-1) 1, (x^2 / (1 + x^2)) = 2 - π / 2 := by
  sorry
end PBRef63

namespace PBRef64
set_option autoImplicit true
/-
The integral \[\int_0^{\frac{\pi}2} x\sin x\,dx.\] is equal to 1.
-/

open Real Set Filter

variable {f : ℝ → ℝ}
theorem integral_x_sin_x_pi_over_2  :
    ∫ x in Icc 0 (π / 2), x * sin x = 1 := by
  sorry
end PBRef64

namespace PBRef65
set_option autoImplicit true
/-
The integral of \(\displaystyle \int_0^{\frac{\pi}4}\frac{ 3\sin x +2 \cos x}{ 4\sin x+ 3\cos x} \,dx\) is equal to \(\frac{1}{50} \ln 2 -\frac{1}{25} \ln \frac{7}{3} + \frac{9\pi}{50}\).
-/

open Real

variable (x : ℝ)
theorem integral_of_trig_rational_function  :
    ∫ x in Set.Icc 0 (π / 4), (3 * sin x + 2 * cos x) / (4 * sin x + 3 * cos x) =
    (1 / 50) * log 2 - (1 / 25) * log (7 / 3) + (9 * π) / 50 := by
  sorry
end PBRef65

namespace PBRef66
set_option autoImplicit true
/-
The integral of \(\sec x\,dx=\int\frac1{\cos x}\,dx\) equals to \ln\left|\sec x+\tan x\right|+C.
-/

-- Define the theorem statement
theorem sec_integral (x : ℝ) :
    ∫ t in Set.Icc 0 x, (1 / Real.cos t) = Real.log (abs (1 / Real.cos x + Real.sin x / Real.cos x)) + C := by
  sorry
end PBRef66

namespace PBRef67
set_option autoImplicit true
/-
The integral of 4/(x^2 -7x +12) from 100 to 200 is equal to 4 * log(196/96) - 4 * log(197/97).
-/

open Real Filter

variable {a b : ℝ} (h_a : a = 100) (h_b : b = 200)
theorem integral_of_rational_function  :
    ∫ x in a..b, (4 : ℝ) / (x^2 - 7*x + 12) = 4 * log (196 / 96) - 4 * log (197 / 97) := by
  sorry
end PBRef67

namespace PBRef68
set_option autoImplicit true
/-
The function \(f(x) = x + 2\sin x\) attains its minimum at \( x = \frac{4\pi}{3} \) on the interval \(\left[\frac{\pi}{2}, 200\right]\).
-/

open Real

/-- The function f(x) = x + 2sin(x) -/
noncomputable def f (x : ℝ) : ℝ := x + 2 * sin x
theorem minimum_attainment_of_function  :
    ∀ x ∈ Set.Icc (π / 2) 200, f (4 * π / 3) ≤ f x := by
  sorry
end PBRef68

namespace PBRef69
set_option autoImplicit true
/-
If \(f(x)=2^x\) and \(g(x)=5\cdot x-6\), then the function \(h(x)=f(g(x))=2^{5x-6}\) results in \(h(3)=2^{5\cdot 3-6}=2^{9}=512\), and function \(m(x)=g(f(x))=5\cdot 2^x-6\) results in \(m(3)=5\cdot 2^3-6=5\cdot 8-6=34\).
-/

/-- The exponential function with base a, f(x) = a^x -/
noncomputable def f (a : ℝ) (x : ℝ) : ℝ := a^x

/-- The linear function g(x) = mx + b -/
noncomputable def g (m b : ℝ) (x : ℝ) : ℝ := m * x + b

/-- The composition h(x) = f(g(x)) = a^(mx + b) -/
noncomputable def h (a m b : ℝ) (x : ℝ) : ℝ := f a (g m b x)

/-- The composition m(x) = g(f(x)) = m * a^x + b -/
noncomputable def m_comp (a m b : ℝ) (x : ℝ) : ℝ := g m b (f a x)
/-- Specific example where a = 2, m = 5, b = -6, and x = 3 -/
theorem specific_example  :
    h 2 5 (-6) 3 = 512 ∧ m_comp 2 5 (-6) 3 = 34 := by
  sorry
end PBRef69

namespace PBRef70
set_option autoImplicit true
/-
The maximum value of \[\int_0^1 \left(x^2f(x)-xf^2(x)\right)\,dx\] over all continuous functions \(f:[0,1]\to\mathbb R\) is \(\frac{1}{16}\).
-/

open Filter Topology

variable {f : ℝ → ℝ} (hf : Continuous f)
theorem max_integral_value  :
    IsMaxOn (fun f => ∫ x in Set.Icc 0 1, (x^2 * f x - x * f x^2)) {f | Continuous f} f →
(∫ x in Set.Icc 0 1, (x^2 * f x - x * f x^2)) = 1/16 := by
  sorry
end PBRef70

namespace PBRef71
set_option autoImplicit true
/-
Let $f(x) = \frac{x+1}{\sqrt{5x^2+35}}$ be a function defined on $\mathbb{R}$. Then $f(x)$ is concave up on the intervals $(-\infty, \frac{21-\sqrt{497}}{4})$ and $(\frac{21+\sqrt{497}}{4}, \infty)$.
-/

open Real

variable (x : ℝ)

/-- The function f(x) = (x + 1) / sqrt(5x^2 + 35) -/
noncomputable def f (x : ℝ) : ℝ := (x + 1) / sqrt (5 * x^2 + 35)
/-- The first derivative of f(x) -/
theorem f_deriv (x : ℝ) :
    deriv f x = (35 - 5 * x^2) / ((5 * x^2 + 35) * sqrt (5 * x^2 + 35)) := by
  sorry
end PBRef71

namespace PBRef72
set_option autoImplicit true
/-
Let $f(x) = \frac{x+1}{\sqrt{5x^2+35}}$ be a function defined on $\mathbb{R}$. Then $f(x)$ is concave up on the intervals $(-\infty, \frac{21-\sqrt{497}}{4})$ and $(\frac{21+\sqrt{497}}{4}, \infty)$.
-/

open Real

variable (x : ℝ)

/-- The function f(x) = (x + 1) / sqrt(5x^2 + 35) -/
noncomputable def f (x : ℝ) : ℝ := (x + 1) / sqrt (5 * x^2 + 35)

/-- The first derivative of f(x) -/
axiom f_deriv (x : ℝ) : deriv f x = (35 - 5 * x^2) / ((5 * x^2 + 35) * sqrt (5 * x^2 + 35))
/-- The second derivative of f(x) -/
theorem f_second_deriv (x : ℝ) :
    deriv (deriv f) x = (50 * x^2 - 525 * x - 175) / ((5 * x^2 + 35)^(5/2)) := by
  sorry
end PBRef72

namespace PBRef73
set_option autoImplicit true
/-
Let $f(x) = \frac{x+1}{\sqrt{5x^2+35}}$ be a function defined on $\mathbb{R}$. Then $f(x)$ is concave up on the intervals $(-\infty, \frac{21-\sqrt{497}}{4})$ and $(\frac{21+\sqrt{497}}{4}, \infty)$.
-/

open Real

variable (x : ℝ)

/-- The function f(x) = (x + 1) / sqrt(5x^2 + 35) -/
noncomputable def f (x : ℝ) : ℝ := (x + 1) / sqrt (5 * x^2 + 35)

/-- The first derivative of f(x) -/
axiom f_deriv (x : ℝ) : deriv f x = (35 - 5 * x^2) / ((5 * x^2 + 35) * sqrt (5 * x^2 + 35))

/-- The second derivative of f(x) -/
axiom f_second_deriv (x : ℝ) : deriv (deriv f) x = (50 * x^2 - 525 * x - 175) / ((5 * x^2 + 35)^(5/2))
/-- The critical points of f''(x) -/
theorem critical_points  :
    ∃ a b : ℝ, a < b ∧
  a = (21 - sqrt 497) / 4 ∧
  b = (21 + sqrt 497) / 4 ∧
  ∀ x, deriv (deriv f) x = 0 ↔ x = a ∨ x = b := by
  sorry
end PBRef73

namespace PBRef74
set_option autoImplicit true
/-
Let $f(x) = \frac{x+1}{\sqrt{5x^2+35}}$ be a function defined on $\mathbb{R}$. Then $f(x)$ is concave up on the intervals $(-\infty, \frac{21-\sqrt{497}}{4})$ and $(\frac{21+\sqrt{497}}{4}, \infty)$.
-/

open Real

variable (x : ℝ)

/-- The function f(x) = (x + 1) / sqrt(5x^2 + 35) -/
noncomputable def f (x : ℝ) : ℝ := (x + 1) / sqrt (5 * x^2 + 35)

/-- The first derivative of f(x) -/
axiom f_deriv (x : ℝ) : deriv f x = (35 - 5 * x^2) / ((5 * x^2 + 35) * sqrt (5 * x^2 + 35))

/-- The second derivative of f(x) -/
axiom f_second_deriv (x : ℝ) : deriv (deriv f) x = (50 * x^2 - 525 * x - 175) / ((5 * x^2 + 35)^(5/2))

/-- The critical points of f''(x) -/
axiom critical_points : ∃ a b : ℝ, a < b ∧
  a = (21 - sqrt 497) / 4 ∧
  b = (21 + sqrt 497) / 4 ∧
  ∀ x, deriv (deriv f) x = 0 ↔ x = a ∨ x = b
/-- f(x) is concave up on the intervals (-∞, (21 - √497)/4) and ((21 + √497)/4, ∞) -/
theorem concave_up_intervals  :
    ∃ a b : ℝ, a < b ∧
  (∀ x < a, deriv (deriv f) x > 0) ∧
  (∀ x > b, deriv (deriv f) x > 0) ∧
  a = (21 - sqrt 497) / 4 ∧
  b = (21 + sqrt 497) / 4 := by
  sorry
end PBRef74

namespace PBRef75
set_option autoImplicit true
/-
The critical values of the function \( f(x) = 2x^3 - 3x^2 - 36x + 18 \) are \( x = -2 \) and \( x = 3 \).
-/

open Polynomial

/-- The cubic polynomial f(x) = 2x³ - 3x² - 36x + 18 -/
noncomputable def f_poly : Polynomial ℝ :=
  2 * X^3 - 3 * X^2 - 36 * X + 18

/-- Convert polynomial to function -/
noncomputable def f (x : ℝ) : ℝ := f_poly.eval x

/-- The derivative polynomial -/
noncomputable def f_deriv_poly : Polynomial ℝ :=
  (2 * 3) * X^2 - (3 * 2) * X - 36

/-- The derivative as a function -/
noncomputable def f_deriv (x : ℝ) : ℝ := f_deriv_poly.eval x

/-- The critical values of f(x) are x = -2 and x = 3 -/
def critical_values_of_cubic (x : ℝ) : Prop :=
  f_deriv x = 0 ↔ x = -2 ∨ x = 3
/-- Verification of the critical values -/
theorem verify_critical_values  :
    ∀ x, critical_values_of_cubic x := by
  sorry
end PBRef75

namespace PBRef76
set_option autoImplicit true
/-
The integral \[\iint_{R}f(x,y)\,dxdy,\] where \(f(x,y)=11-2x-3y^2\) and \(R\) is the rectangle \([1,3]\times[-2,5]\) is equal to -168.
-/

open Set Filter MeasureTheory

variable (f : ℝ → ℝ → ℝ) (R : Set (ℝ × ℝ))
theorem integral_over_rectangle_equals_minus_168  :
    let f := fun x y => 11 - 2 * x - 3 * y^2
  let R := Icc (1 : ℝ) (3 : ℝ) ×ˢ Icc (-2 : ℝ) (5 : ℝ)
  ∫ x in Icc (1 : ℝ) (3 : ℝ), ∫ y in Icc (-2 : ℝ) (5 : ℝ), f x y = -168 := by
  sorry
end PBRef76

namespace PBRef77
set_option autoImplicit true
/-
The limit of the function \(\displaystyle \lim_{x\to 0}\frac{\sin\left(3x+x^2\right)}{5x+2x^2}\) equals to \(\frac{3}{5}\).
-/

open Filter Topology
theorem limit_of_function_at_zero  :
    Tendsto (fun x => Real.sin (3 * x + x^2) / (5 * x + 2 * x^2)) (𝓝 0) (𝓝 (3 / 5)) := by
  sorry
end PBRef77

namespace PBRef78
set_option autoImplicit true
/-
The limit of the function \(f(x)=\frac{ 3^{x}-1}{x}\) as \(x\) approaches 0 is \(\ln 3\).
-/

open Filter Topology
theorem limit_of_function_as_x_approaches_zero  :
    Tendsto (fun x => (3^x - 1) / x) (𝓝[≠] 0) (𝓝 (Real.log 3)) := by
  sorry
end PBRef78

namespace PBRef79
set_option autoImplicit true
/-
The integral \(\displaystyle \int \frac{x}{\sqrt{49-x^2}}\,dx\) evaluates to \(-\sqrt{49-x^2}+C.\)
-/

-- Define the function as noncomputable
noncomputable def f (x : ℝ) : ℝ := x / Real.sqrt (49 - x^2)

-- Theorem statement
theorem integral_f_eq (x C : ℝ) :
    ∫  x, f x = -Real.sqrt (49 - x^2) + C := by
  sorry
end PBRef79

namespace PBRef80
set_option autoImplicit true
/-
The indefinite integral of cos(5x) with respect to x is 1/5 sin(5x) + C.
-/
theorem cos_5x_indefinite_integral {f : ℝ → ℝ} (hf : Continuous f) (h_diff : ∀ x, DifferentiableAt ℝ f x) (h_deriv : ∀ x, deriv f x = (1 / 5 : ℝ) * Real.sin (5 * x)) :
    ∃ C, ∀ x, f x = (1 / 5 : ℝ) * Real.sin (5 * x) + C := by
  sorry
end PBRef80

namespace PBRef81
set_option autoImplicit true
/- For the equation cos(2x) - √3 sin(2x) = √2, there exist exactly four solutions
   in the interval [0, 2π), namely x = 0, x = π/3, x = π, and x = 4π/3. -/

/-- The left side of the equation cos(2x) - √3 sin(2x) = √2 -/
noncomputable def equation (x : ℝ) : ℝ :=
  Real.cos (2 * x) - Real.sqrt 3 * Real.sin (2 * x)
/-- The equation can be rewritten as 2cos(2x + π/3) = √2 -/
theorem simplified_equation (x : ℝ) :
    equation x = 2 * Real.cos (2 * x + Real.pi / 3) - Real.sqrt 2 := by
  sorry
end PBRef81

namespace PBRef82
set_option autoImplicit true
/- For the equation cos(2x) - √3 sin(2x) = √2, there exist exactly four solutions
   in the interval [0, 2π), namely x = 0, x = π/3, x = π, and x = 4π/3. -/

/-- The left side of the equation cos(2x) - √3 sin(2x) = √2 -/
noncomputable def equation (x : ℝ) : ℝ :=
  Real.cos (2 * x) - Real.sqrt 3 * Real.sin (2 * x)

/-- The equation can be rewritten as 2cos(2x + π/3) = √2 -/
axiom simplified_equation (x : ℝ) :
  equation x = 2 * Real.cos (2 * x + Real.pi / 3) - Real.sqrt 2

/-- The set of solutions in [0, 2π) -/
noncomputable def solution_set : Finset ℝ :=
  {0, Real.pi / 3, Real.pi, 4 * Real.pi / 3}
/-- Verify each solution lies in [0, 2π) -/
theorem solutions_in_interval  :
    ∀ x ∈ solution_set, x ∈ Set.Ico 0 (2 * Real.pi) := by
  sorry
end PBRef82

namespace PBRef83
set_option autoImplicit true
/- For the equation cos(2x) - √3 sin(2x) = √2, there exist exactly four solutions
   in the interval [0, 2π), namely x = 0, x = π/3, x = π, and x = 4π/3. -/

/-- The left side of the equation cos(2x) - √3 sin(2x) = √2 -/
noncomputable def equation (x : ℝ) : ℝ :=
  Real.cos (2 * x) - Real.sqrt 3 * Real.sin (2 * x)

/-- The equation can be rewritten as 2cos(2x + π/3) = √2 -/
axiom simplified_equation (x : ℝ) :
  equation x = 2 * Real.cos (2 * x + Real.pi / 3) - Real.sqrt 2

/-- The set of solutions in [0, 2π) -/
noncomputable def solution_set : Finset ℝ :=
  {0, Real.pi / 3, Real.pi, 4 * Real.pi / 3}

/-- Verify each solution lies in [0, 2π) -/
axiom solutions_in_interval :
  ∀ x ∈ solution_set, x ∈ Set.Ico 0 (2 * Real.pi)
/-- Verify each solution satisfies the equation -/
theorem solutions_satisfy_equation  :
    ∀ x ∈ solution_set, equation x = 0 := by
  sorry
end PBRef83

namespace PBRef84
set_option autoImplicit true
/- For the equation cos(2x) - √3 sin(2x) = √2, there exist exactly four solutions
   in the interval [0, 2π), namely x = 0, x = π/3, x = π, and x = 4π/3. -/

/-- The left side of the equation cos(2x) - √3 sin(2x) = √2 -/
noncomputable def equation (x : ℝ) : ℝ :=
  Real.cos (2 * x) - Real.sqrt 3 * Real.sin (2 * x)

/-- The equation can be rewritten as 2cos(2x + π/3) = √2 -/
axiom simplified_equation (x : ℝ) :
  equation x = 2 * Real.cos (2 * x + Real.pi / 3) - Real.sqrt 2

/-- The set of solutions in [0, 2π) -/
noncomputable def solution_set : Finset ℝ :=
  {0, Real.pi / 3, Real.pi, 4 * Real.pi / 3}

/-- Verify each solution lies in [0, 2π) -/
axiom solutions_in_interval :
  ∀ x ∈ solution_set, x ∈ Set.Ico 0 (2 * Real.pi)

/-- Verify each solution satisfies the equation -/
axiom solutions_satisfy_equation :
  ∀ x ∈ solution_set, equation x = 0
/-- Any solution in [0, 2π) must be one of our four solutions -/
theorem all_solutions_found (x : ℝ) (h : x ∈ Set.Ico 0 (2 * Real.pi)) :
    equation x = 0 → x ∈ solution_set := by
  sorry
end PBRef84

namespace PBRef85
set_option autoImplicit true
/- For the equation cos(2x) - √3 sin(2x) = √2, there exist exactly four solutions
   in the interval [0, 2π), namely x = 0, x = π/3, x = π, and x = 4π/3. -/

/-- The left side of the equation cos(2x) - √3 sin(2x) = √2 -/
noncomputable def equation (x : ℝ) : ℝ :=
  Real.cos (2 * x) - Real.sqrt 3 * Real.sin (2 * x)

/-- The equation can be rewritten as 2cos(2x + π/3) = √2 -/
axiom simplified_equation (x : ℝ) :
  equation x = 2 * Real.cos (2 * x + Real.pi / 3) - Real.sqrt 2

/-- The set of solutions in [0, 2π) -/
noncomputable def solution_set : Finset ℝ :=
  {0, Real.pi / 3, Real.pi, 4 * Real.pi / 3}

/-- Verify each solution lies in [0, 2π) -/
axiom solutions_in_interval :
  ∀ x ∈ solution_set, x ∈ Set.Ico 0 (2 * Real.pi)

/-- Verify each solution satisfies the equation -/
axiom solutions_satisfy_equation :
  ∀ x ∈ solution_set, equation x = 0

/-- Any solution in [0, 2π) must be one of our four solutions -/
axiom all_solutions_found (x : ℝ) (h : x ∈ Set.Ico 0 (2 * Real.pi)) :
  equation x = 0 → x ∈ solution_set
/-- There are exactly four solutions in [0, 2π) -/
theorem exactly_four_solutions  :
    ∃! (s : Finset ℝ), s.card = 4 ∧
    (∀ x ∈ s, x ∈ Set.Ico 0 (2 * Real.pi) ∧ equation x = 0) ∧
    (∀ x, x ∈ Set.Ico 0 (2 * Real.pi) ∧ equation x = 0 → x ∈ s) := by
  sorry
end PBRef85

namespace PBRef86
set_option autoImplicit true
/-
The derivative of the function g(x) = cos(x) is g'(x) = -sin(x).
-/
theorem cos_derivative  :
    deriv (fun x => Real.cos x) = fun x => -Real.sin x := by
  sorry
end PBRef86

namespace PBRef87
set_option autoImplicit true
/-
The indefinite integral \[\int_1^5 x\ln x\,dx\] is equivalent to \[\frac{25\ln 5-12}2. \]
-/

open Real
open MeasureTheory
theorem integral_x_ln_x_over_interval  :
    ∫ x in Set.Icc 1 5, x * log x = (25 * log 5 - 12) / 2 := by
  sorry
end PBRef87

namespace PBRef88
set_option autoImplicit true
/-
The integral \(\displaystyle \int \sqrt[3]{\cos x}\cdot \sin^3x\,dx\) can be evaluated as \(-\frac34 \cos^{\frac43}x+\frac{3}{10}\cos^{\frac{10}3}x+C\), by substituting \(u=\cos x\) and integring term by term.
-/

open Real
theorem integral_of_cube_root_cos_sin_cube (x : ℝ) :
    ∫ x in Set.Icc 0 x, (cos x)^(1/3 : ℝ) * (sin x)^3 =
  - (3/4) * (cos x)^(4/3 : ℝ) + (3/10) * (cos x)^(10/3 : ℝ) + C := by
  sorry
end PBRef88

namespace PBRef89
set_option autoImplicit true
/-
The integral \[\iiint_S z\,dxdydz,\] where \(S\) is a triangular prism bounded by the planes \(x=0\), \(y=0\), \(z=0\), \(x=5\), and \(y+z=1\), is equal to \(\frac{5}{6}\).
-/

open MeasureTheory
open Real

variable {S : Set (ℝ × ℝ × ℝ)}
theorem integral_over_triangular_prism  :
    (∫⁻ (p : ℝ × ℝ × ℝ) in {p : ℝ × ℝ × ℝ | p.1 ∈ Set.Icc 0 5 ∧ p.2.1 ∈ Set.Icc 0 1 ∧
  p.2.2 ∈ Set.Icc 0 1 ∧ p.2.1 + p.2.2 ≤ 1}, ENNReal.ofReal p.2.2) = 5 / 6 := by
  sorry
end PBRef89

namespace PBRef90
set_option autoImplicit true
/-
Let $f$ be a function defined by $f(x)=\frac{\sqrt{-1-x}}{\log _{\frac{1}{2}}(x)}$. Then the domain of $f$ is the empty set, i.e., $\text{Dom}(f) = \emptyset$.
-/

open Real Set

/-- The function f(x) = √(-1-x) / log₁/₂(x) -/
noncomputable def f (x : ℝ) : ℝ :=
sqrt (-1 - x) / logb (1/2) x

/-- The domain of f is empty -/
def Dom : Set ℝ := {x | -1 - x ≥ 0 ∧ x > 0}
theorem f_domain_empty  :
    Dom = ∅ := by
  sorry
end PBRef90

namespace PBRef91
set_option autoImplicit true
/-
For any real number $x$, the inequality $2.3 < -\log(x) < 5.4$ is satisfied if and only if $x \in \left(10^{-5.4}, 10^{-2.3}\right)$.
-/

open Real

variable (x : ℝ)

/-- The logarithmic inequality: 2.3 < -log 10 x < 5.4 -/
def log_inequality (x : ℝ) : Prop := 2.3 < -logb 10 x ∧ -logb 10 x < 5.4

/-- The interval (10^-5.4, 10^-2.3) -/
def target_interval : Set ℝ := Set.Ioo (10^(-5.4 : ℝ)) (10^(-2.3 : ℝ))
theorem log_inequality_of_in_interval (h : x ∈ target_interval) :
    log_inequality x := by
  sorry
end PBRef91

namespace PBRef92
set_option autoImplicit true
/-
For any real number $x$, the inequality $2.3 < -\log(x) < 5.4$ is satisfied if and only if $x \in \left(10^{-5.4}, 10^{-2.3}\right)$.
-/

open Real

variable (x : ℝ)

/-- The logarithmic inequality: 2.3 < -log 10 x < 5.4 -/
def log_inequality (x : ℝ) : Prop := 2.3 < -logb 10 x ∧ -logb 10 x < 5.4

/-- The interval (10^-5.4, 10^-2.3) -/
def target_interval : Set ℝ := Set.Ioo (10^(-5.4 : ℝ)) (10^(-2.3 : ℝ))

axiom log_inequality_of_in_interval (h : x ∈ target_interval) : log_inequality x
theorem in_interval_of_log_inequality (h : log_inequality x) :
    x ∈ target_interval := by
  sorry
end PBRef92

namespace PBRef93
set_option autoImplicit true
/-
For any real number $x$, the inequality $2.3 < -\log(x) < 5.4$ is satisfied if and only if $x \in \left(10^{-5.4}, 10^{-2.3}\right)$.
-/

open Real

variable (x : ℝ)

/-- The logarithmic inequality: 2.3 < -log 10 x < 5.4 -/
def log_inequality (x : ℝ) : Prop := 2.3 < -logb 10 x ∧ -logb 10 x < 5.4

/-- The interval (10^-5.4, 10^-2.3) -/
def target_interval : Set ℝ := Set.Ioo (10^(-5.4 : ℝ)) (10^(-2.3 : ℝ))

axiom log_inequality_of_in_interval (h : x ∈ target_interval) : log_inequality x

axiom in_interval_of_log_inequality (h : log_inequality x) : x ∈ target_interval
/-- The inequality 2.3 < -log 10 x < 5.4 is satisfied if and only if x ∈ (10^-5.4, 10^-2.3). -/
theorem log_inequality_iff  :
    log_inequality x ↔ x ∈ target_interval := by
  sorry
end PBRef93

namespace PBRef94
set_option autoImplicit true
/-
Let $f: (-1, 1) \to \mathbb{R}$ be a function such that $\lim_{x \to 0} f(x) = 0$. If $f$ is differentiable at $x = 0$ with $f'(0) = m$, then $\lim_{x \to 0} \frac{f(x)}{x} = m$.
-/

open Filter Set Function
open scoped Topology

variable (f : ℝ → ℝ) (m : ℝ)

-- Define the open interval (-1, 1)
def open_unit_interval : Set ℝ := Ioo (-1) 1

-- Theorem
theorem main_theorem (hf : ContinuousOn f open_unit_interval) (h_lim : Tendsto f (𝓝[≠] 0) (𝓝 0)) (h_diff : DifferentiableAt ℝ f 0) (h_deriv : deriv f 0 = m) :
    Tendsto (λ x => f x / x) (𝓝[≠] 0) (𝓝 m) := by
  sorry
end PBRef94

namespace PBRef95
set_option autoImplicit true
/-
Let $f: (-1, 1) \to \mathbb{R}$ be a function such that $\lim_{x \to 0} f(x) = 0$. If $f$ is differentiable at $x = 0$ with $f'(0) = m$, then $\lim_{x \to 0} \frac{f(x)}{x} = m$.
-/

open Filter Set Function
open scoped Topology

variable (f : ℝ → ℝ)
variable (m : ℝ)

-- Define the open interval (-1, 1)
def open_unit_interval : Set ℝ := Ioo (-1) 1

-- Theorem
axiom main_theorem (hf : ContinuousOn f open_unit_interval)
  (h_lim : Tendsto f (𝓝[≠] 0) (𝓝 0))
  (h_diff : DifferentiableAt ℝ f 0)
  (h_deriv : deriv f 0 = m) :
  Tendsto (λ x => f x / x) (𝓝[≠] 0) (𝓝 m)

-- Corollary: If f(0) = 0, then the limit of f(x)/x as x approaches 0 equals f'(0)
theorem limit_quotient_eq_deriv (hf : ContinuousOn f open_unit_interval) (h_zero : f 0 = 0) (h_diff : DifferentiableAt ℝ f 0) :
    Tendsto (λ x => f x / x) (𝓝[≠] 0) (𝓝 (deriv f 0)) := by
  sorry
end PBRef95

namespace PBRef96
set_option autoImplicit true
/-
For all real numbers x, the inequality $\frac{1-\ln (x)}{x^{2}}<0$ is satisfied if and only if x ∈ (e, ∞), where e is Euler's number.
-/

open Real

-- Theorem: The inequality (1 - ln(x)) / x^2 < 0 holds if and only if x ∈ (e, ∞)
theorem inequality_solution (x : ℝ) :
    (1 - log x) / x^2 < 0 ↔ x > exp 1 := by
  sorry
end PBRef96

namespace PBRef97
set_option autoImplicit true
/-
The only real number values for \(a, b, c, d\) that satisfy the condition \(a^2+b^2+c^2+d^2=a(b+c+d)\), are when \(a = b = c = d = 0\).
-/

variable (a b c d : ℝ) (h : a^2 + b^2 + c^2 + d^2 = a * (b + c + d))
theorem sum_of_squares_and_product_implies_zero  :
    a = 0 ∧ b = 0 ∧ c = 0 ∧ d = 0 := by
  sorry
end PBRef97

namespace PBRef98
set_option autoImplicit true
/-
The series $\sum_{n=1}^{\infty} \frac{n}{n^{2}+1}$ is divergent.
-/

open Real NNReal

-- Define a comparison series that is known to diverge
noncomputable def comparison_series (n : ℕ+) : ℝ≥0 := 1 / (2 * n)

-- Define `general_term`: The general term of the series
noncomputable def general_term (n : ℕ+) : ℝ≥0 := (n : ℝ≥0) / ((n : ℝ≥0)^2 + 1)

-- Lemma: For all n ≥ 1, general_term n ≤ comparison_series n
theorem upper_bound (n : ℕ+) :
    general_term n ≤ comparison_series n := by
  sorry
end PBRef98

namespace PBRef99
set_option autoImplicit true
/-
The series $\sum_{n=1}^{\infty} \frac{n}{n^{2}+1}$ is divergent.
-/

open Real NNReal

-- Define a comparison series that is known to diverge
noncomputable def comparison_series (n : ℕ+) : ℝ≥0 := 1 / (2 * n)

-- Define `general_term`: The general term of the series
noncomputable def general_term (n : ℕ+) : ℝ≥0 := (n : ℝ≥0) / ((n : ℝ≥0)^2 + 1)

-- Lemma: For all n ≥ 1, general_term n ≤ comparison_series n
axiom upper_bound (n : ℕ+) : general_term n ≤ comparison_series n

-- Lemma: Comparison test for non-negative real series
theorem comparison_test {a b : ℕ+ → ℝ≥0} (h : ∀ n, a n ≤ b n) (hb : ¬ Summable b) :
    ¬ Summable a := by
  sorry
end PBRef99

namespace PBRef100
set_option autoImplicit true
/-
The series $\sum_{n=1}^{\infty} \frac{n}{n^{2}+1}$ is divergent.
-/

open Real NNReal

-- Define a comparison series that is known to diverge
noncomputable def comparison_series (n : ℕ+) : ℝ≥0 := 1 / (2 * n)

-- Define `general_term`: The general term of the series
noncomputable def general_term (n : ℕ+) : ℝ≥0 := (n : ℝ≥0) / ((n : ℝ≥0)^2 + 1)

-- Lemma: For all n ≥ 1, general_term n ≤ comparison_series n
axiom upper_bound (n : ℕ+) : general_term n ≤ comparison_series n

-- Lemma: Comparison test for non-negative real series
axiom comparison_test {a b : ℕ+ → ℝ≥0} (h : ∀ n, a n ≤ b n) (hb : ¬ Summable b) :
    ¬ Summable a

-- Lemma: The comparison series diverges
theorem comparison_series_diverges  :
    ¬ Summable comparison_series := by
  sorry
end PBRef100

namespace PBRef101
set_option autoImplicit true
/-
The series $\sum_{n=1}^{\infty} \frac{n}{n^{2}+1}$ is divergent.
-/

open Real NNReal

-- Define a comparison series that is known to diverge
noncomputable def comparison_series (n : ℕ+) : ℝ≥0 := 1 / (2 * n)

-- Define `general_term`: The general term of the series
noncomputable def general_term (n : ℕ+) : ℝ≥0 := (n : ℝ≥0) / ((n : ℝ≥0)^2 + 1)

-- Lemma: For all n ≥ 1, general_term n ≤ comparison_series n
axiom upper_bound (n : ℕ+) : general_term n ≤ comparison_series n

-- Lemma: Comparison test for non-negative real series
axiom comparison_test {a b : ℕ+ → ℝ≥0} (h : ∀ n, a n ≤ b n) (hb : ¬ Summable b) :
    ¬ Summable a

-- Lemma: The comparison series diverges
axiom comparison_series_diverges : ¬ Summable comparison_series

-- Theorem: The series ∑ (n : ℕ+), general_term n diverges
theorem series_diverges  :
    ¬ Summable general_term := by
  sorry
end PBRef101

namespace PBRef102
set_option autoImplicit true
/-
Let $f:[0,8] \rightarrow \mathbb{R}$ be defined by $f(x)=\sqrt[3]{8x-x^2}$. Then there exists a point $c \in (0,8)$ such that $f'(c) = 0$. Moreover, this point is specifically $c = 4$.
-/

open Real

variable (x : ℝ)

-- Define `f`: The function f is defined as f(x) = (8x - x^2)^(1/3)
noncomputable def f (x : ℝ) : ℝ := (8 * x - x^2)^(1/3 : ℝ)

-- Prove `derivative_f`: The derivative of f is given by f'(x) = (1/3) * (8x - x^2)^(-2/3) * (8 - 2x)
theorem derivative_f  :
    ∀ x ∈ Set.Ioo 0 8, HasDerivAt f ((1/3 : ℝ) * (8 * x - x^2)^(-2/3 : ℝ) * (8 - 2 * x)) x := by
  sorry
end PBRef102

namespace PBRef103
set_option autoImplicit true
/-
Let $f:[0,8] \rightarrow \mathbb{R}$ be defined by $f(x)=\sqrt[3]{8x-x^2}$. Then there exists a point $c \in (0,8)$ such that $f'(c) = 0$. Moreover, this point is specifically $c = 4$.
-/

open Real

variable (x : ℝ)

-- Define `f`: The function f is defined as f(x) = (8x - x^2)^(1/3)
noncomputable def f (x : ℝ) : ℝ := (8 * x - x^2)^(1/3 : ℝ)

-- Prove `derivative_f`: The derivative of f is given by f'(x) = (1/3) * (8x - x^2)^(-2/3) * (8 - 2x)
axiom derivative_f : ∀ x ∈ Set.Ioo 0 8, HasDerivAt f ((1/3 : ℝ) * (8 * x - x^2)^(-2/3 : ℝ) * (8 - 2 * x)) x

-- Prove that f is continuous on [0,8]
theorem f_continuous  :
    ContinuousOn f (Set.Icc 0 8) := by
  sorry
end PBRef103

namespace PBRef104
set_option autoImplicit true
/-
Let $f:[0,8] \rightarrow \mathbb{R}$ be defined by $f(x)=\sqrt[3]{8x-x^2}$. Then there exists a point $c \in (0,8)$ such that $f'(c) = 0$. Moreover, this point is specifically $c = 4$.
-/

open Real

variable (x : ℝ)

-- Define `f`: The function f is defined as f(x) = (8x - x^2)^(1/3)
noncomputable def f (x : ℝ) : ℝ := (8 * x - x^2)^(1/3 : ℝ)

-- Prove `derivative_f`: The derivative of f is given by f'(x) = (1/3) * (8x - x^2)^(-2/3) * (8 - 2x)
axiom derivative_f : ∀ x ∈ Set.Ioo 0 8, HasDerivAt f ((1/3 : ℝ) * (8 * x - x^2)^(-2/3 : ℝ) * (8 - 2 * x)) x

-- Prove that f is continuous on [0,8]
axiom f_continuous : ContinuousOn f (Set.Icc 0 8)

-- Prove that f is differentiable on (0,8)
theorem f_differentiable  :
    DifferentiableOn ℝ f (Set.Ioo 0 8) := by
  sorry
end PBRef104

namespace PBRef105
set_option autoImplicit true
/-
Let $f:[0,8] \rightarrow \mathbb{R}$ be defined by $f(x)=\sqrt[3]{8x-x^2}$. Then there exists a point $c \in (0,8)$ such that $f'(c) = 0$. Moreover, this point is specifically $c = 4$.
-/

open Real

variable (x : ℝ)

-- Define `f`: The function f is defined as f(x) = (8x - x^2)^(1/3)
noncomputable def f (x : ℝ) : ℝ := (8 * x - x^2)^(1/3 : ℝ)

-- Prove `derivative_f`: The derivative of f is given by f'(x) = (1/3) * (8x - x^2)^(-2/3) * (8 - 2x)
axiom derivative_f : ∀ x ∈ Set.Ioo 0 8, HasDerivAt f ((1/3 : ℝ) * (8 * x - x^2)^(-2/3 : ℝ) * (8 - 2 * x)) x

-- Prove that f is continuous on [0,8]
axiom f_continuous : ContinuousOn f (Set.Icc 0 8)

-- Prove that f is differentiable on (0,8)
axiom f_differentiable : DifferentiableOn ℝ f (Set.Ioo 0 8)

-- Prove `critical_point`: The critical point of f is found by solving 8 - 2x = 0, yielding x = 4
theorem critical_point  :
    ∃! c, c ∈ Set.Ioo 0 8 ∧ HasDerivAt f 0 c := by
  sorry
end PBRef105

namespace PBRef106
set_option autoImplicit true
/-
Let $f:[0,8] \rightarrow \mathbb{R}$ be defined by $f(x)=\sqrt[3]{8x-x^2}$. Then there exists a point $c \in (0,8)$ such that $f'(c) = 0$. Moreover, this point is specifically $c = 4$.
-/

open Real

variable (x : ℝ)

-- Define `f`: The function f is defined as f(x) = (8x - x^2)^(1/3)
noncomputable def f (x : ℝ) : ℝ := (8 * x - x^2)^(1/3 : ℝ)

-- Prove `derivative_f`: The derivative of f is given by f'(x) = (1/3) * (8x - x^2)^(-2/3) * (8 - 2x)
axiom derivative_f : ∀ x ∈ Set.Ioo 0 8, HasDerivAt f ((1/3 : ℝ) * (8 * x - x^2)^(-2/3 : ℝ) * (8 - 2 * x)) x

-- Prove that f is continuous on [0,8]
axiom f_continuous : ContinuousOn f (Set.Icc 0 8)

-- Prove that f is differentiable on (0,8)
axiom f_differentiable : DifferentiableOn ℝ f (Set.Ioo 0 8)

-- Prove `critical_point`: The critical point of f is found by solving 8 - 2x = 0, yielding x = 4
axiom critical_point : ∃! c, c ∈ Set.Ioo 0 8 ∧ HasDerivAt f 0 c
/-- By Rolle's theorem, there exists a unique point c ∈ (0,8) such that f'(c) = 0, specifically c = 4 -/
theorem rolle_theorem_application  :
    ∃! c, c ∈ Set.Ioo 0 8 ∧ HasDerivAt f 0 c ∧ c = 4 := by
  sorry
end PBRef106

namespace PBRef107
set_option autoImplicit true
/-
For the function $f(x)=\ln(x^2+1)$, the domain is the set of all real numbers, i.e., $\text{Dom}(f) = \mathbb{R} = (-\infty, \infty)$.
-/

open Real Set

-- Define the function f(x) = ln(x^2 + 1)
noncomputable def f (x : ℝ) : ℝ := log (x^2 + 1)

-- Lemma: x^2 + 1 is always positive for all real numbers x
theorem positivity_of_square_plus_one (x : ℝ) :
    0 < x^2 + 1 := by
  sorry
end PBRef107

namespace PBRef108
set_option autoImplicit true
/-
For the function $f(x)=\ln(x^2+1)$, the domain is the set of all real numbers, i.e., $\text{Dom}(f) = \mathbb{R} = (-\infty, \infty)$.
-/

open Real Set

-- Define the function f(x) = ln(x^2 + 1)
noncomputable def f (x : ℝ) : ℝ := log (x^2 + 1)

-- Lemma: x^2 + 1 is always positive for all real numbers x
axiom positivity_of_square_plus_one (x : ℝ) : 0 < x^2 + 1

-- Theorem: The domain of f(x) = ln(x^2 + 1) is the set of all real numbers
theorem domain_of_f_is_reals  :
    ∀ x : ℝ, x ∈ univ := by
  sorry
end PBRef108

namespace PBRef109
set_option autoImplicit true
/-
For the function $f(x)=\ln(x^2+1)$, the domain is the set of all real numbers, i.e., $\text{Dom}(f) = \mathbb{R} = (-\infty, \infty)$.
-/

open Real Set

-- Define the function f(x) = ln(x^2 + 1)
noncomputable def f (x : ℝ) : ℝ := log (x^2 + 1)

-- Lemma: x^2 + 1 is always positive for all real numbers x
axiom positivity_of_square_plus_one (x : ℝ) : 0 < x^2 + 1

-- Theorem: The domain of f(x) = ln(x^2 + 1) is the set of all real numbers
axiom domain_of_f_is_reals : ∀ x : ℝ, x ∈ univ

-- Corollary: f(x) is well-defined for all real numbers
theorem f_well_defined  :
    ∀ x : ℝ, ∃! y : ℝ, y = Real.log (x^2 + 1) := by
  sorry
end PBRef109

namespace PBRef110
set_option autoImplicit true
/-
Let $f: D \to \mathbb{R}$ be a function and $X \subseteq D$. If there exists a constant $M > 0$ such that $|f(x)| \leq M$ for all $x \in X$, then $f$ is bounded on $X$.
-/

variable {D : Type*} {f : D → ℝ} {X : Set D}

def BoundedOn (f : D → ℝ) (X : Set D) : Prop :=
  BddAbove (f '' X) ∧ BddBelow (f '' X)
theorem bounded_function_on_subset  :
    (∃ M > 0, ∀ x ∈ X, |f x| ≤ M) → BoundedOn f X := by
  sorry
end PBRef110

namespace PBRef111
set_option autoImplicit true
/-
Let $f$ be a function defined in a punctured neighborhood of $x_0$. If $\lim_{x \rightarrow x_0} f(x) = A$ and $A > 0$, then there exists $\delta > 0$ such that for all $x$ satisfying $0 < |x - x_0| < \delta$, we have $f(x) > 0$.
-/

open Filter Topology

variable {X Y : Type} [MetricSpace X] [MetricSpace Y] [LinearOrderedField Y]
variable {f : X → Y} {x₀ : X} {A : Y}
/-- Theorem: If the limit of f(x) as x approaches x₀ is A and A > 0, then f(x) > 0 in some punctured neighborhood of x₀. -/
theorem limit_positive_implies_function_positive (h : Tendsto f (𝓝 x₀) (𝓝 A)) (hA : A > (0 : Y)) :
    ∃ δ > (0 : ℝ), ∀ x, 0 < dist x x₀ ∧ dist x x₀ < δ → 0 < f x := by
  sorry
end PBRef111

namespace PBRef112
set_option autoImplicit true
/-
Let $f: (a,b) \rightarrow \mathbb{R}$ be a function differentiable on the open interval $(a,b)$. For any two points $x_1, x_2 \in (a,b)$, there exists a point $\xi$ between $x_1$ and $x_2$ such that $f(x_1) - f(x_2) = (x_1 - x_2)f'(\xi)$.
-/

open Set

variable {a b : ℝ} {f : ℝ → ℝ}
/-- Theorem: If `f` is differentiable on `(a, b)`, then for any `x₁, x₂ ∈ (a, b)`, there exists `ξ` between `x₁` and `x₂` such that `f(x₁) - f(x₂) = (x₁ - x₂) f'(ξ)`. -/
theorem mean_value_theorem_for_differences (hf : DifferentiableOn ℝ f (Ioo a b)) {x₁ x₂ : ℝ} (hx₁ : x₁ ∈ Ioo a b) (hx₂ : x₂ ∈ Ioo a b) :
    ∃ ξ ∈ Ioo (min x₁ x₂) (max x₁ x₂), f x₁ - f x₂ = (x₁ - x₂) * deriv f ξ := by
  sorry
end PBRef112

namespace PBRef113
set_option autoImplicit true
/-
Let ${x_n}$ be a convergent sequence of real numbers. If $\lim_{n \to \infty}(x_n + \sin x_n) = 0$, then $\lim_{n \to \infty} x_n = 0$.
-/

open Topology Metric Filter

variable {x : ℕ → ℝ}
theorem abs_sin_le_one (x : ℝ) :
    |Real.sin x| ≤ 1 := by
  sorry
end PBRef113

namespace PBRef114
set_option autoImplicit true
/-
Let ${x_n}$ be a convergent sequence of real numbers. If $\lim_{n \to \infty}(x_n + \sin x_n) = 0$, then $\lim_{n \to \infty} x_n = 0$.
-/

open Topology Metric Filter

variable {x : ℕ → ℝ}

axiom abs_sin_le_one (x : ℝ) : |Real.sin x| ≤ 1
theorem convergent_seq_bounded {x : ℕ → ℝ} (hx : ∃ L, Tendsto x atTop (𝓝 L)) :
    ∃ M, ∀ n, |x n| ≤ M := by
  sorry
end PBRef114

namespace PBRef115
set_option autoImplicit true
/-
Let ${x_n}$ be a convergent sequence of real numbers. If $\lim_{n \to \infty}(x_n + \sin x_n) = 0$, then $\lim_{n \to \infty} x_n = 0$.
-/

open Topology Metric Filter

variable {x : ℕ → ℝ}

axiom abs_sin_le_one (x : ℝ) : |Real.sin x| ≤ 1

axiom convergent_seq_bounded {x : ℕ → ℝ} (hx : ∃ L, Tendsto x atTop (𝓝 L)) :
  ∃ M, ∀ n, |x n| ≤ M
theorem convergent_sum_sin_zero (hx : ∃ L, Tendsto x atTop (𝓝 L)) (h : Tendsto (λ n => x n + Real.sin (x n)) atTop (𝓝 0)) :
    Tendsto x atTop (𝓝 0) := by
  sorry
end PBRef115

namespace PBRef116
set_option autoImplicit true
/-
For real numbers $x > 0$, the inequality $\ln(x^2) \leq (\ln(x))^2$ holds if and only if $x \in (0,1] \cup [e^2, \infty)$.
-/

open Real

-- Assuming these lemmas are not available in the imported libraries, define them
theorem log_le_zero_iff (x : ℝ) (hx : x > 0) :
    log x ≤ 0 ↔ x ≤ 1 := by
  sorry
end PBRef116

namespace PBRef117
set_option autoImplicit true
/-
For real numbers $x > 0$, the inequality $\ln(x^2) \leq (\ln(x))^2$ holds if and only if $x \in (0,1] \cup [e^2, \infty)$.
-/

open Real

-- Assuming these lemmas are not available in the imported libraries, define them
axiom log_le_zero_iff (x : ℝ) (hx : x > 0) : log x ≤ 0 ↔ x ≤ 1
theorem two_le_log_iff (x : ℝ) (hx : x > 0) :
    2 ≤ log x ↔ exp 2 ≤ x := by
  sorry
end PBRef117

namespace PBRef118
set_option autoImplicit true
/-
For real numbers $x > 0$, the inequality $\ln(x^2) \leq (\ln(x))^2$ holds if and only if $x \in (0,1] \cup [e^2, \infty)$.
-/

open Real

-- Assuming these lemmas are not available in the imported libraries, define them
axiom log_le_zero_iff (x : ℝ) (hx : x > 0) : log x ≤ 0 ↔ x ≤ 1

axiom two_le_log_iff (x : ℝ) (hx : x > 0) : 2 ≤ log x ↔ exp 2 ≤ x
/-- The inequality `ln(x^2) ≤ (ln(x))^2` holds if and only if `x ∈ (0,1] ∪ [e^2, ∞)`. -/
theorem log_square_le_square_log (x : ℝ) (hx : x > 0) :
    log (x^2) ≤ (log x)^2 ↔ x ∈ Set.Ioo 0 1 ∪ Set.Ici (exp 2) := by
  sorry
end PBRef118

namespace PBRef119
set_option autoImplicit true
/-
Let $f: [a,b] \rightarrow \mathbb{R}$ be a function that is continuous on $[a,b]$ and differentiable on $(a,b)$. If $f(a) = f(b)$, then there exists at least one point $\xi \in (a,b)$ such that $f'(\xi) = 0$.
-/

variable {a b : ℝ}
/-- Application of Rolle's Theorem: If f is continuous on [a,b], differentiable on (a,b),
    and f(a) = f(b), then there exists c ∈ (a,b) such that f'(c) = 0. -/
theorem rolles_theorem_application (hab : a < b) {f : ℝ → ℝ} (h_cont : ContinuousOn f (Set.Icc a b)) (h_diff : DifferentiableOn ℝ f (Set.Ioo a b)) (h_eq : f a = f b) :
    ∃ c ∈ Set.Ioo a b, deriv f c = 0 := by
  sorry
end PBRef119

