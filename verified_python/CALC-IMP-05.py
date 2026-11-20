import sympy as sp

x = sp.symbols('x', positive=True)
# Kiểm tra trực tiếp bằng SymPy tại biên của điều kiện hội tụ (a = m - 2 hội tụ, a = m - 1 phân kỳ)
conv = sp.integrate(1 / (1 + x**2), (x, 1, sp.oo))
assert conv == sp.pi / 4, f'Expected convergence at m=2, a=0: {conv}'
div = sp.integrate(x / (1 + x**2), (x, 1, sp.oo))
assert div == sp.oo, f'Expected divergence at m=2, a=1: {div}'
for mv in range(3, 10):
    # Tích phân trên [1, B] của trường hợp phân kỳ a = m - 1 tăng như ln(B)/1, trường hợp a = m - 2 bị chặn
    F_conv = lambda B: float(sp.Integral(x**(mv - 2) / (1 + x**mv), (x, 1, B)).evalf(15))
    F_div = lambda B: float(sp.Integral(x**(mv - 1) / (1 + x**mv), (x, 1, B)).evalf(15))
    assert F_conv(1e4) - F_conv(1e2) < 1e-1
    assert F_div(1e4) - F_div(1e2) > 4.0
for mv in range(2, 10):
    # Tiêu chuẩn so sánh: x^a/(1+x^m) ~ x^(a-m) khi x -> +∞, hội tụ <=> m - a > 1
    for a in range(0, mv + 5):
        X = 1e6
        assert abs((X**a / (1 + X**mv)) / X**(a - mv) - 1) < 1e-9
    count = sum(1 for a in range(0, mv + 5) if mv - a > 1)
    assert count == mv - 1
    opts = [mv, mv - 2, mv + 1, mv - 1]
    assert len(set(opts)) == 4, f'Duplicate options at m={mv}'
print('VERIFIED_OK: CALC-IMP-05')
