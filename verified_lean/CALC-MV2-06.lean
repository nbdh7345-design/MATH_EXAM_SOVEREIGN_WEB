-- Lean 4 Core verification for CALC-MV2-06 (implicit function in three variables)
-- With E := e^z = m at the point: F = E + x*y*Z - m, F_z = E + x*y
def Fval (m x y E Z : Int) : Int := E + x * y * Z - m
def Fz (x y E : Int) : Int := E + x * y

theorem calc_mv2_06_point :
    (List.range 8).all (fun k => let m : Int := k + 2;
      (List.range 20).all (fun z => Fval m 0 1 m z == 0) && Fz 0 1 m == m && m != 0) = true := by decide
