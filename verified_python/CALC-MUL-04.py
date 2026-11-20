import sympy as sp

x, y = sp.symbols('x y', real=True)
for mv in range(2, 10):
    f = x**mv + mv * y**2
    val = sp.diff(f, x).subs({x: 1, y: 1}) + sp.diff(f, y).subs({x: 1, y: 1})
    assert val == 3 * mv, f'Value mismatch at m={mv}: {val}'
    opts = [2 * mv, 3 * mv, mv, 4 * mv]
    assert len(set(opts)) == 4, f'Duplicate options at m={mv}'
print('VERIFIED_OK: CALC-MUL-04')
