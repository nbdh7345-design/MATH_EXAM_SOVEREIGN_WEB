-- Lean 4 Core verification for CALC-ANTI-04 (with E := e^m symbolic, E ≥ e^2 > 7; all options scaled by m)
def optionsScaled (m E : Int) : List Int := [m * (E - 1), E - 1, m * m * (E - 1), E + 1]

theorem calc_anti_04_distinct :
    (List.range 8).all (fun k => let m : Int := k + 2;
      (List.range 20).all (fun e => let E : Int := e + 7; (optionsScaled m E).Nodup)) = true := by decide
