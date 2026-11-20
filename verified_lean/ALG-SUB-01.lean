-- Lean 4 Core verification for ALG-SUB-01: Grassmann dimension formula
def dimU : Nat := 2
def dimW : Nat := 3
def dimInter : Nat := 2
def dimSum : Nat := dimU + dimW - dimInter

def targetExpr (m : Nat) : Nat := m * dimSum + dimInter

theorem grassmann_identity : dimU + dimW = dimSum + dimInter := by decide

theorem alg_sub_01_formula (m : Nat) : targetExpr m = 3 * m + 2 := by
  unfold targetExpr dimSum dimU dimW dimInter
  omega

theorem alg_sub_01_m3 : targetExpr 3 = 11 := by rfl

#eval targetExpr 3
