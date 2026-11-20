import sympy as sp

x, y, z, m = sp.symbols('x y z m', real=True)
f = x**2 + 2*y**2 + 2*z**2 + 2*x*y + 2*x*z + 2*y*z - 2*m*x - 6*m*y + 7*m**2
sos = (x + y + z - m)**2 + (y - 2*m)**2 + (z + m)**2 + m**2
assert sp.expand(f - sos) == 0

grad = [sp.diff(f, v) for v in (x, y, z)]
sol = sp.solve(grad, (x, y, z))
assert sol[x] == 0 and sol[y] == 2*m and sol[z] == -m

H = sp.hessian(f, (x, y, z))
D1 = int(H[:1, :1].det())
D2 = int(H[:2, :2].det())
D3 = int(H.det())
assert (D1, D2, D3) == (2, 4, 8)

for m_val in range(2, 10):
    f_min = int(f.subs({x: 0, y: 2*m_val, z: -m_val, m: m_val}))
    assert f_min == m_val**2
    assert f_min + D1 + D2 + D3 == m_val**2 + 14

print('VERIFIED_OK: CALC-MUL-03 3D Sylvester Hessian & global minimum passed.')
