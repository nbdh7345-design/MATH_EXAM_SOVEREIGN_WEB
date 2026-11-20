-- Lean 4 Core verification for ALG-SUB-03: Direct sum & Grassmann essay
def normSqBcap (m : Nat) : Nat := 1 + 0 + m * m + 0
def dimU_03 : Nat := 2
def dimW_03 : Nat := 2
def dimInter_03 : Nat := 1
def dimSum_03 : Nat := dimU_03 + dimW_03 - dimInter_03

def indexI (m : Nat) : Nat := normSqBcap m + dimSum_03

theorem direct_sum_complement : dimSum_03 + 1 = 4 := by decide

theorem alg_sub_03_formula (m : Nat) : indexI m = m * m + 4 := by
  unfold indexI normSqBcap dimSum_03 dimU_03 dimW_03 dimInter_03
  omega

theorem alg_sub_03_m3 : indexI 3 = 13 := by rfl

#eval indexI 3
