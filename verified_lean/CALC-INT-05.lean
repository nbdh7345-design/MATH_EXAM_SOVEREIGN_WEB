-- Lean 4 Core verification for CALC-INT-05 (integration by parts)
-- Antiderivative F(x) = (x/m - 1/m^2) e^{mx}; scaled by m^2 with E := e^m symbolic:
--   m^2 F(1) = (m - 1) E,  m^2 F(0) = -1  =>  m^2 (F(1) - F(0)) = (m - 1) E + 1
def m2F1 (m E : Int) : Int := (m * 1 - 1) * E
def m2F0 (_m : Int) : Int := (0 - 1) * 1

theorem calc_int_05_parts :
    (List.range 8).all (fun k => let m : Int := k + 2;
      (List.range 30).all (fun e => let E : Int := e + 1; m2F1 m E - m2F0 m == (m - 1) * E + 1)) = true := by
  decide
