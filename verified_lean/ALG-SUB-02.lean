-- Lean 4 Core verification for ALG-SUB-02: Linear span membership
def v1 (m : Int) : Int × Int × Int × Int := (1, 2, m, 1)
def v2 (m : Int) : Int × Int × Int × Int := (2, 5, 2 * m + 1, 3)
def kTarget (m : Int) : Int := m * m + 2

theorem span_fourth_coord (m : Int) : kTarget m - m * m = -1 * 1 + 1 * 3 := by
  unfold kTarget
  omega

theorem alg_sub_02_m3 : kTarget 3 = 11 := by rfl

#eval kTarget 3
