-- Lean 4 Core verification for ALG-DIAG-01
def a0 (m : Nat) : Nat := 2 * m
def traceD (m : Nat) : Nat := m + 2
def S_val (m : Nat) : Nat := a0 m + traceD m

theorem alg_diag_01_formula (m : Nat) : S_val m = 3 * m + 2 := by
   unfold S_val a0 traceD
   omega

theorem alg_diag_01_m3 : S_val 3 = 11 := by decide
#eval S_val 3
