"""Bộ in chuỗi N1 (mục 6.4, không tin cậy): cây → chuỗi văn phạm N1, chỉ thêm ngoặc khi cần.

Tính chất bắt buộc: chuan_hoa(doc_bieu_thuc(in_chuoi(t))) == t với mọi cây t đã chuẩn hóa.
"""

from __future__ import annotations

from sinhde.nen_tang import cay as C


def muc(t: C.Nut) -> int:
    """Mức ưu tiên của chuỗi in ra (bảng mục 6.4, bản 1.2).

    Mức của `So(q)` là mức của chuỗi in ra: `1/2`, `-1/2` là phép chia (mức 2),
    `-2` là dấu trừ một ngôi (mức 3), số nguyên không âm là nguyên tố (mức 5).
    """
    if isinstance(t, C.So):
        if t.q.denominator != 1:
            return 2
        return 5 if t.q >= 0 else 3
    if isinstance(t, (C.Cong, C.Tru)):
        return 1
    if isinstance(t, (C.Nhan, C.Chia)):
        return 2
    if isinstance(t, C.Am):
        return 3
    if isinstance(t, C.Mu):
        return 4
    return 5  # Bien, ThamSo, Ham, LuyThua


def _boc(t: C.Nut, muc_toi_thieu: int) -> str:
    s = in_chuoi(t)
    return f"({s})" if muc(t) < muc_toi_thieu else s


def in_chuoi(t: C.Nut) -> str:
    if isinstance(t, C.So):
        q = t.q
        dau = "-" if q < 0 else ""
        if q.denominator == 1:
            return f"{dau}{abs(q.numerator)}"
        return f"{dau}{abs(q.numerator)}/{q.denominator}"
    if isinstance(t, C.Bien):
        return "x"
    if isinstance(t, C.ThamSo):
        return t.ten
    if isinstance(t, C.Am):
        return "-" + _boc(t.a, 3)
    if isinstance(t, C.Cong):
        return f"{_boc(t.a, 1)} + {_boc(t.b, 2)}"
    if isinstance(t, C.Tru):
        return f"{_boc(t.a, 1)} - {_boc(t.b, 2)}"
    if isinstance(t, C.Nhan):
        return f"{_boc(t.a, 2)}*{_boc(t.b, 3)}"
    if isinstance(t, C.Chia):
        return f"{_boc(t.a, 2)}/{_boc(t.b, 3)}"
    if isinstance(t, C.Mu):
        so_mu = str(t.n) if t.n >= 0 else f"(-{-t.n})"
        return f"{_boc(t.a, 5)}^{so_mu}"
    if isinstance(t, C.LuyThua):
        return f"luythua({in_chuoi(t.a)}, {in_chuoi(t.b)})"
    if isinstance(t, C.Ham):
        return f"{t.ten}({in_chuoi(t.a)})"
    raise TypeError(f"Không phải nút biểu thức: {t!r}")


def in_dieu_kien(dk: C.DieuKien) -> str:
    if isinstance(dk, C.SoSanh):
        return f"{in_chuoi(dk.trai)} {dk.op} {in_chuoi(dk.phai)}"
    if isinstance(dk, C.Va):
        # `and` ưu tiên hơn `or`; vế phải của `and` là một phép so sánh.
        return f"{in_dieu_kien(dk.a)} and {in_dieu_kien(dk.b)}"
    return f"{in_dieu_kien(dk.a)} or {in_dieu_kien(dk.b)}"
