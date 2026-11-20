-- Lean 4 Core verification for CALC-DER-06 (Leibniz rule, only k = 2 survives at x = 0)
def choose : Nat → Nat → Nat
  | _, 0 => 1
  | 0, _ + 1 => 0
  | n + 1, k + 1 => choose n k + choose n (k + 1)
def uDerivAt0 : Nat → Nat   -- derivatives of x^2 at 0
  | 2 => 2
  | _ => 0
def f10At0 (m : Nat) : Nat :=
  ((List.range 11).map (fun k => choose 10 k * uDerivAt0 k * m ^ (10 - k))).foldl (· + ·) 0

theorem calc_der_06_binom : choose 10 2 = 45 := by decide
theorem calc_der_06_answer :
    (List.range 8).all (fun k => let m := k + 2; f10At0 m == 90 * m ^ 8) = true := by decide
