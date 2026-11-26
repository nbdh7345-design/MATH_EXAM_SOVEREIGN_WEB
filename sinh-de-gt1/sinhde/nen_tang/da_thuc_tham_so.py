"""Biểu thức đa thức theo tham số (mục 6.6).

Điểm giới hạn và các biểu thức trong ràng buộc chỉ được là đa thức theo tham số với hệ số
hữu tỉ. Sau chuẩn hóa chúng chỉ gồm So, ThamSo, Am, Cong, Tru, Nhan, Mu với n ≥ 1 và
Chia(u, So(q)) với q ≠ 0. Nhờ vậy Python (Fraction) và Lean (ℚ) luôn tính ra cùng kết quả,
và không có phép chia cho 0 nào bị quy ước thành 0.
"""

from __future__ import annotations

from fractions import Fraction

from sinhde.nen_tang import cay as C
from sinhde.nen_tang.chuan_hoa import chuan_hoa, chuan_hoa_dk

_SO_SANH = {
    "<": lambda a, b: a < b, "<=": lambda a, b: a <= b, ">": lambda a, b: a > b,
    ">=": lambda a, b: a >= b, "=": lambda a, b: a == b, "!=": lambda a, b: a != b,
}


def _la_da_thuc(t: C.Nut) -> bool:
    if isinstance(t, (C.So, C.ThamSo)):
        return True
    if isinstance(t, C.Am):
        return _la_da_thuc(t.a)
    if isinstance(t, (C.Cong, C.Tru, C.Nhan)):
        return _la_da_thuc(t.a) and _la_da_thuc(t.b)
    if isinstance(t, C.Mu):
        return t.n >= 1 and _la_da_thuc(t.a)
    if isinstance(t, C.Chia):
        return isinstance(t.b, C.So) and t.b.q != 0 and _la_da_thuc(t.a)
    return False  # Bien, Ham, LuyThua, Chia cho biểu thức không phải hằng


def la_da_thuc_tham_so(t: C.Nut) -> bool:
    """Biểu thức (sau chuẩn hóa) là đa thức theo tham số với hệ số hữu tỉ, không chứa x."""
    return _la_da_thuc(chuan_hoa(t))


def dieu_kien_la_da_thuc(dk: C.DieuKien) -> bool:
    dk = chuan_hoa_dk(dk)
    if isinstance(dk, C.SoSanh):
        return _la_da_thuc(dk.trai) and _la_da_thuc(dk.phai)
    return dieu_kien_la_da_thuc(dk.a) and dieu_kien_la_da_thuc(dk.b)


def gia_tri_chinh_xac(t: C.Nut, gia_tri: dict[str, Fraction]) -> Fraction:
    """Giá trị chính xác của một đa thức theo tham số tại `gia_tri`."""
    t = chuan_hoa(t)
    if not _la_da_thuc(t):
        raise ValueError("Không phải đa thức theo tham số (mục 6.6)")
    return _tinh(t, gia_tri)


def _tinh(t: C.Nut, g: dict[str, Fraction]) -> Fraction:
    if isinstance(t, C.So):
        return t.q
    if isinstance(t, C.ThamSo):
        return Fraction(g[t.ten])
    if isinstance(t, C.Am):
        return -_tinh(t.a, g)
    if isinstance(t, C.Cong):
        return _tinh(t.a, g) + _tinh(t.b, g)
    if isinstance(t, C.Tru):
        return _tinh(t.a, g) - _tinh(t.b, g)
    if isinstance(t, C.Nhan):
        return _tinh(t.a, g) * _tinh(t.b, g)
    if isinstance(t, C.Mu):
        return _tinh(t.a, g) ** t.n
    assert isinstance(t, C.Chia)  # mẫu là hằng khác 0, đã kiểm ở _la_da_thuc
    return _tinh(t.a, g) / t.b.q


def danh_gia_dieu_kien(dk: C.DieuKien, gia_tri: dict[str, Fraction]) -> bool:
    """Đánh giá chính xác một ràng buộc (đa thức theo tham số) tại `gia_tri`."""
    if isinstance(dk, C.SoSanh):
        return _SO_SANH[dk.op](gia_tri_chinh_xac(dk.trai, gia_tri),
                               gia_tri_chinh_xac(dk.phai, gia_tri))
    if isinstance(dk, C.Va):
        return danh_gia_dieu_kien(dk.a, gia_tri) and danh_gia_dieu_kien(dk.b, gia_tri)
    return danh_gia_dieu_kien(dk.a, gia_tri) or danh_gia_dieu_kien(dk.b, gia_tri)
