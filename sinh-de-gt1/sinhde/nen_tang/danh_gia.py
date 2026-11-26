"""Tính giá trị và điều kiện xác định của biểu thức tại một điểm (không tin cậy).

Theo đúng `XacDinh` của Lean (mục 7.2). Phần hữu tỉ tính chính xác bằng `Fraction`; phần có
hàm siêu việt tính bằng mpmath với 50 chữ số. Khi một phép so sánh với 0 không quyết định
được bằng số gần đúng, hàm ném `KhongRo` (phép thử chỉ được loại, không được chấp nhận — I5).
Dùng cho kiểm thử theo tính chất (mục 6.7) và sau này cho phép thử T2 ở A4.
"""

from __future__ import annotations

from fractions import Fraction
from typing import Union

import mpmath as mp

from sinhde.nen_tang import cay as C

mp.mp.dps = 50
_NGUONG = mp.mpf(10) ** -30

GiaTri = Union[Fraction, mp.mpf]


class KhongRo(Exception):
    """Không quyết định được bằng số gần đúng (giá trị quá gần biên)."""


class KhongXacDinh(Exception):
    """Biểu thức không xác định tại điểm đang xét."""


def _mp(v: GiaTri) -> mp.mpf:
    return mp.mpf(v.numerator) / v.denominator if isinstance(v, Fraction) else v


def _dau(v: GiaTri) -> int:
    """Dấu của v: −1, 0, 1. Ném KhongRo nếu v là số gần đúng quá gần 0."""
    if isinstance(v, Fraction):
        return (v > 0) - (v < 0)
    if abs(v) < _NGUONG:
        raise KhongRo()
    return 1 if v > 0 else -1


def _ham(ten: str, u: GiaTri) -> GiaTri:
    if ten == "abs":
        return abs(u)
    m = _mp(u)
    if ten in ("sin", "cos", "arctan", "exp"):
        return {"sin": mp.sin, "cos": mp.cos, "arctan": mp.atan, "exp": mp.exp}[ten](m)
    if ten == "tan":
        if _dau(mp.cos(m)) == 0:
            raise KhongXacDinh()
        return mp.tan(m)
    if ten == "cot":
        if _dau(mp.sin(m)) == 0:
            raise KhongXacDinh()
        return mp.cos(m) / mp.sin(m)
    if ten in ("arcsin", "arccos"):
        if _dau(u - 1 if isinstance(u, Fraction) else m - 1) > 0 or \
                _dau(u + 1 if isinstance(u, Fraction) else m + 1) < 0:
            raise KhongXacDinh()
        return mp.asin(m) if ten == "arcsin" else mp.acos(m)
    if ten == "ln":
        if _dau(u) <= 0:
            raise KhongXacDinh()
        return mp.log(m)
    if ten == "sqrt":
        if _dau(u) < 0:
            raise KhongXacDinh()
        return mp.sqrt(m)
    if ten == "cbrt":
        return mp.sign(m) * mp.cbrt(abs(m))
    raise ValueError(f"Hàm không biết: {ten}")


def _tinh(t: C.Nut, x: Fraction, g: dict[str, Fraction]) -> GiaTri:
    if isinstance(t, C.So):
        return t.q
    if isinstance(t, C.Bien):
        return x
    if isinstance(t, C.ThamSo):
        return Fraction(g[t.ten])
    if isinstance(t, C.Am):
        return -_tinh(t.a, x, g)
    if isinstance(t, C.Ham):
        return _ham(t.ten, _tinh(t.a, x, g))
    if isinstance(t, C.Mu):
        a = _tinh(t.a, x, g)
        if t.n <= 0 and _dau(a) == 0:
            raise KhongXacDinh()  # 0^0 và 0^(−k) không xác định
        return a ** t.n if isinstance(a, Fraction) else mp.power(a, t.n)
    a, b = _tinh(t.a, x, g), _tinh(t.b, x, g)
    if isinstance(t, C.LuyThua):
        if _dau(a) <= 0:
            raise KhongXacDinh()
        return mp.power(_mp(a), _mp(b))
    if isinstance(t, C.Chia) and _dau(b) == 0:
        raise KhongXacDinh()
    if not (isinstance(a, Fraction) and isinstance(b, Fraction)):
        a, b = _mp(a), _mp(b)  # có phần gần đúng thì tính cả phép bằng mpmath
    if isinstance(t, C.Cong):
        return a + b
    if isinstance(t, C.Tru):
        return a - b
    if isinstance(t, C.Nhan):
        return a * b
    return a / b


def xac_dinh_va_gia_tri(t: C.Nut, x: Fraction,
                        gia_tri_tham_so: dict[str, Fraction] | None = None) -> tuple[bool, GiaTri | None]:
    """(có xác định không, giá trị). Ném KhongRo nếu không quyết định được."""
    try:
        return True, _tinh(t, Fraction(x), gia_tri_tham_so or {})
    except KhongXacDinh:
        return False, None
