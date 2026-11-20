-- Lean 4 Core verification for ALG-RNK-02 (no Mathlib, no sorry)
def detU (lam m : Int) : Int := (lam - 1) * lam * (lam - m)

def rankU (lam m : Int) : Nat :=
  let d2 := if lam - 1 == 0 then 0 else 1
  let d3 := if lam * (lam - m) == 0 then 0 else 1
  1 + d2 + d3

def sumSqS (m : Int) : Int := 0 * 0 + 1 * 1 + m * m

theorem alg_rnk_02_m3 : rankU 0 3 = 2 ∧ rankU 1 3 = 2 ∧ rankU 3 3 = 2 ∧ sumSqS 3 = 10 := by decide

theorem alg_rnk_02_formula (m : Int) : sumSqS m = m * m + 1 := by
  unfold sumSqS
  omega

#eval (List.range 8).map (fun i => let m := Int.ofNat (i + 2); (m, rankU 0 m, rankU 1 m, rankU m m, sumSqS m))
