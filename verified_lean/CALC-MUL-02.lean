-- Lean 4 Core verification for CALC-MUL-02 (No Mathlib, No sorry)
def u_val (m x y z : Int) : Int :=
  m * x^2 * y + y^2 * z + m * z^2 * x

def ux (m x y z : Int) : Int := 2 * m * x * y + m * z^2
def uy (m x y z : Int) : Int := m * x^2 + 2 * y * z
def uz (m x y z : Int) : Int := y^2 + 2 * m * z * x

def uxx (m _ y _ : Int) : Int := 2 * m * y
def uyy (_ _ _ z : Int) : Int := 2 * z
def uzz (m x _ _ : Int) : Int := 2 * m * x

def S_at_111 (m : Int) : Int :=
  let euler_part := 1 * ux m 1 1 1 + 1 * uy m 1 1 1 + 1 * uz m 1 1 1
  let half_trace := (uxx m 1 1 1 + uyy m 1 1 1 + uzz m 1 1 1) / 2
  euler_part + half_trace

theorem calc_mul_02_euler_identity :
    (List.range 10).all (fun k => let m := Int.ofNat (k + 1); ux m 1 1 1 + uy m 1 1 1 + uz m 1 1 1 == 3 * u_val m 1 1 1) = true := by
  decide

theorem calc_mul_02_grid_check :
    (List.range 8).all (fun k =>
      let m : Int := Int.ofNat (k + 2)
      S_at_111 m == 8 * m + 4) = true := by
  decide

#eval (List.range 8).map (fun k => let m := Int.ofNat (k + 2); (m, S_at_111 m))
