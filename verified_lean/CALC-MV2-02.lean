-- Lean 4 Core verification for CALC-MV2-02 (implicit differentiation)
-- With E := e^y treated as a positive integer symbol: F_x = E, F_y = x * E + 1
def Fval (m x y E : Int) : Int := x * E + y - m
def Fy (x E : Int) : Int := x * E + 1

theorem calc_mv2_02_point :
    (List.range 8).all (fun k => let m : Int := k + 2;
      (List.range 50).all (fun e => Fval m 0 m (e + 1) == 0)) = true := by decide
theorem calc_mv2_02_nondegenerate :
    (List.range 50).all (fun e => Fy 0 (e + 1) == 1) = true := by decide

#eval Fy 0 20
