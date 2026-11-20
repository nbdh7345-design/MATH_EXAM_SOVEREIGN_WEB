-- Lean 4 Core verification for ALG-QUAD-03 (No Mathlib, No sorry)
def q3_d1 (_m : Int) : Int := 1
def q3_d2 (m : Int) : Int := (m + 1) - 1
def q3_d3 (m : Int) : Int := m * (2 * m - 1)

def q3_form (m x1 x2 x3 : Int) : Int :=
  x1*x1 + (m + 1)*x2*x2 + (m*m + 3*m - 1)*x3*x3 - 2*x1*x2 + 2*m*x1*x3

def q3_lagrange (m x1 x2 x3 : Int) : Int :=
  let y1 := x1 - x2 + m * x3
  let y2 := x2 + x3
  let y3 := x3
  y1*y1 + m*y2*y2 + (2*m - 1)*y3*y3

theorem q3_d2_id (m : Int) : q3_d2 m = m := by
  unfold q3_d2
  omega

theorem q3_lagrange_at_default :
    q3_form 4 3 (-2) 5 = q3_lagrange 4 3 (-2) 5 := by rfl

theorem q3_sylvester_at_default :
    q3_d1 4 > 0 ∧ q3_d2 4 > 0 ∧ q3_d3 4 > 0 := by decide

#eval (q3_d1 4, q3_d2 4, q3_d3 4, q3_form 4 3 (-2) 5)
