-- Lean 4 Core verification for ALG-DIAG-02
def rem_scalar (m : Nat) : Nat := 2 * m + 2
def trace_M (m : Nat) : Nat := 2 * rem_scalar m

theorem alg_diag_02_trace (m : Nat) : trace_M m = 4 * m + 4 := by
  unfold trace_M rem_scalar
  omega

theorem alg_diag_02_m3 : trace_M 3 = 16 := by decide
#eval trace_M 3
