-- Lean 4 Core Verification for CALC-VEC-03 (Gauss Flux + Stokes Circulation)
def divF (m : Nat) : Nat := m + 2 * m + 3 * m
def boxVolume : Nat := 2 * 1 * 1
def gaussFlux (m : Nat) : Nat := divF m * boxVolume

def curlGz (m : Nat) : Nat := 2 * m + m
def topFaceArea : Nat := 2 * 1
def stokesCirculation (m : Nat) : Nat := curlGz m * topFaceArea

def totalInvariant (m : Nat) : Nat := gaussFlux m + stokesCirculation m

theorem calc_vec_03_flux (m : Nat) : gaussFlux m = 12 * m := by
  simp [gaussFlux, divF, boxVolume]
  omega

theorem calc_vec_03_circ (m : Nat) : stokesCirculation m = 6 * m := by
  simp [stokesCirculation, curlGz, topFaceArea]
  omega

theorem calc_vec_03_total (m : Nat) : totalInvariant m = 18 * m := by
  simp [totalInvariant, gaussFlux, stokesCirculation, divF, curlGz, boxVolume, topFaceArea]
  omega

theorem calc_vec_03_m3 : totalInvariant 3 = 54 := by
  decide

#eval (gaussFlux 3, stokesCirculation 3, totalInvariant 3)
