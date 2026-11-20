-- Lean 4 Core verification for CALC-CONT-06 (continuity conditions at x = 1)
def leftLimit (a : Int) : Int := 1 ^ 2 + a * 1
def rightLimit (m : Int) : Int := m * 1 + 3

theorem calc_cont_06_continuity :
    (List.range 8).all (fun k => let m : Int := k + 2; let a := m + 2; let b := m + 3;
      leftLimit a == rightLimit m && rightLimit m == b && a + b == 2 * m + 5) = true := by decide
-- b) (sqrt(n^2 + m n) - n)(sqrt(n^2 + m n) + n) = m n
theorem calc_cont_06_conjugate :
    (List.range 8).all (fun k => let m : Int := k + 2;
      (List.range 20).all (fun j => let n : Int := j + 1; (n ^ 2 + m * n) - n ^ 2 == m * n)) = true := by decide
