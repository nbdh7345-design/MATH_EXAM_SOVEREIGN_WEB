"""Bộ in chuỗi N1 (mục 6.4 của thiết kế v2.1, không tin cậy).

In cây ra chuỗi theo văn phạm N1, chỉ thêm ngoặc khi thiếu ngoặc sẽ đọc ra cây khác.
Tính chất bắt buộc: chuan_hoa(doc(in(t))) == t với mọi cây t đã chuẩn hóa.
(Dạng đầy đủ ngoặc `(chia (tru …) …)` là của hàm khác: `cay.to_sexpr`.)
"""

from __future__ import annotations

from typing import Any

from sinhde.nen_tang import cay as C


def muc(t: C.Nut) -> int:
    """Mức ưu tiên của chuỗi in ra (bảng mục 6.4).

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
    return 5  # Bien, ThamSo, An, Pi, Ham (kể cả e), LuyThua, TichPhanT


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
        return t.ten
    if isinstance(t, C.ThamSo):
        return t.ten
    if isinstance(t, C.An):
        return "m"
    if isinstance(t, C.Pi):
        return "pi"
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
        if t == C.hang_e():
            return "e"
        return f"{t.ten}({in_chuoi(t.a)})"
    if isinstance(t, C.TichPhanT):
        return f"tp({in_chuoi(t.f)}, {in_chuoi(t.a)}, {in_chuoi(t.b)})"
    raise TypeError(f"Không phải nút biểu thức: {t!r}")


def in_dieu_kien(dk: C.DieuKien) -> str:
    if isinstance(dk, C.SoSanh):
        return f"{in_chuoi(dk.trai)} {dk.op} {in_chuoi(dk.phai)}"
    if isinstance(dk, C.Va):
        return f"{in_dieu_kien(dk.a)} and {in_dieu_kien(dk.b)}"
    return f"{in_dieu_kien(dk.a)} or {in_dieu_kien(dk.b)}"


def _in_dau_mut(d: C.DauMut) -> str:
    if isinstance(d, C.VoCung):
        return "vc" if d.duong else "-vc"
    return in_chuoi(d)


def in_phuong_an(pa: Any) -> str:
    """In một phương án hoặc một tập theo văn phạm N1."""
    if isinstance(pa, C.Nut):
        return in_chuoi(pa)
    if isinstance(pa, C.DacBiet):
        return pa.loai
    if isinstance(pa, C.TapRong):
        return "rong"
    if isinstance(pa, C.TapHuuHan):
        return "{" + ", ".join(in_chuoi(e) for e in pa.phan_tu) + "}"
    if isinstance(pa, C.Khoang):
        return f"{pa.kieu}({_in_dau_mut(pa.trai)}, {_in_dau_mut(pa.phai)})"
    if isinstance(pa, C.HopKhoang):
        return " U ".join(in_phuong_an(k) for k in pa.cac_khoang)
    if isinstance(pa, C.Diem2):
        return f"({in_chuoi(pa.x)}, {in_chuoi(pa.y)})"
    raise TypeError(f"Không in được bằng N1: {pa!r}")
