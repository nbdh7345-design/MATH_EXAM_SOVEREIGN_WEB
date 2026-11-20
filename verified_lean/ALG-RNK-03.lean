-- Lean 4 Core verification for ALG-RNK-03 (no Mathlib, no sorry)
def rankStratified (lam m : Int) : Nat :=
  let r2_nonzero := (lam - m != 0)
  let r3_nonzero := ((lam - m) * (lam - 2 * m) != 0)
  1 + (if r2_nonzero then 1 else 0) + (if r3_nonzero then 1 else 0)

def characteristicT (m : Int) : Int := m + 2 * (2 * m)

theorem alg_rnk_03_m3 :
    rankStratified 3 3 = 1 ∧ rankStratified 6 3 = 2 ∧ rankStratified 4 3 = 3 ∧ characteristicT 3 = 15 := by
  decide

theorem alg_rnk_03_target (m : Int) : characteristicT m = 5 * m := by
  unfold characteristicT
  omega

#eval (List.range 8).map (fun i => let m := Int.ofNat (i + 2); (m, rankStratified m m, rankStratified (2 * m) m, rankStratified (m + 1) m, characteristicT m))
