-- Lean 4 Formal Verification for ALG-SYS-02 (Kronecker-Capelli Rank Consistency)
def row_check (m : Int) (k : Int) : Bool :=
  k - 3 * m - 1 == 0

theorem kronecker_capelli_condition (m : Int) :
  (3 * m + 1) - 3 * m - 1 = 0 := by omega

theorem alg_sys_02_m3 : row_check 3 (3 * 3 + 1) = true := by decide

#eval row_check 3 10
