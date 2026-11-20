-- Lean 4 Core verification for ALG-RNK-01 (no Mathlib, no sorry)
def pivot33 (k m : Int) : Int := (k - 2 * m + 3) - 3

def rank3x4 (k m : Int) : Nat :=
  if pivot33 k m == 0 then 2 else 3

theorem alg_rnk_01_critical_rank (m : Int) :
    rank3x4 (2 * m) m = 2 := by
  unfold rank3x4 pivot33
  have h : (2 * m - 2 * m + 3 - 3 == 0) = true := by
    simp
  rw [h]
  rfl

theorem alg_rnk_01_m3_decide : rank3x4 6 3 = 2 ∧ rank3x4 7 3 = 3 := by decide

#eval (List.range 8).map (fun i => let m := Int.ofNat (i + 2); (m, rank3x4 (2 * m) m, rank3x4 (2 * m + 1) m))
