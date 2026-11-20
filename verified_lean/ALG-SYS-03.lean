-- Lean 4 Formal Verification for ALG-SYS-03 (Symmetric Parametric Linear System)
def det_sym (lam : Int) : Int :=
  lam * (lam * lam - 1) - 1 * (lam - 1) + 1 * (1 - lam)

theorem det_sym_factored_at_2 : det_sym 2 = (2 + 2) * (2 - 1) * (2 - 1) := by decide
theorem det_sym_singular_1 : det_sym 1 = 0 := by decide
theorem det_sym_singular_neg2 : det_sym (-2) = 0 := by decide

theorem alg_sys_03_sum (m : Int) : 3 * m = 2 * m + m := by omega

#eval det_sym 2
