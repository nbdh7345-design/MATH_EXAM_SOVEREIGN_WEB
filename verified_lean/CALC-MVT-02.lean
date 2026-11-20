-- Lean 4 Core verification for CALC-MVT-02 (slant asymptote by polynomial division)
-- x^2 + m x + 1 = (x - 1)(x + m + 1) + (m + 2)  =>  a = 1, b = m + 1
def numer (m x : Int) : Int := x ^ 2 + m * x + 1
def divided (m x : Int) : Int := (x - 1) * (x + m + 1) + (m + 2)
def optionsAB (m : Int) : List Int := [m + 1, m, m + 3, m + 2]

theorem calc_mvt_02_division :
    (List.range 8).all (fun k => let m : Int := k + 2;
      (List.range 21).all (fun j => let x : Int := j - 10; numer m x == divided m x)) = true := by decide
theorem calc_mvt_02_answer :
    (List.range 8).all (fun k => let m : Int := k + 2;
      1 + (m + 1) == m + 2 && m + 2 != 0 && (optionsAB m).Nodup) = true := by decide

#eval divided 3 5
