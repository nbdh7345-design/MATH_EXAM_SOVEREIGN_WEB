"""Biểu thức theo tham số (mục 6.6 của thiết kế v2.1). Thay `da_thuc_tham_so.py` của bản 1.2.

Ba loại:
- **Ràng buộc** của tham số: phân thức hữu tỉ theo tham số (`+ − ×`, mũ nguyên dương, chia).
  Khi có phép chia cho biểu thức không phải hằng khác 0, hệ thống tự thêm điều kiện
  "mẫu ≠ 0" vào ràng buộc, ở cả Python lẫn Lean, nên hai bên luôn cùng kết quả.
- **Điểm, cận**: mọi biểu thức hằng theo tham số, kể cả π, √, ln (Lean so cây, không tính số).
- **Phương án**: kiểm theo kiểu đáp án ở A2.
"""

from __future__ import annotations

from fractions import Fraction

from sinhde.nen_tang import cay as C
from sinhde.nen_tang.chuan_hoa import chuan_hoa, chuan_hoa_dk

_SO_SANH = {
    "<": lambda a, b: a < b, "<=": lambda a, b: a <= b, ">": lambda a, b: a > b,
    ">=": lambda a, b: a >= b, "=": lambda a, b: a == b, "!=": lambda a, b: a != b,
}


# ----- Ràng buộc -----
def _la_phan_thuc(t: C.Nut) -> bool:
    if isinstance(t, (C.So, C.ThamSo)):
        return True
    if isinstance(t, C.Am):
        return _la_phan_thuc(t.a)
    if isinstance(t, (C.Cong, C.Tru, C.Nhan, C.Chia)):
        return _la_phan_thuc(t.a) and _la_phan_thuc(t.b)
    if isinstance(t, C.Mu):
        return t.n >= 1 and _la_phan_thuc(t.a)
    return False  # biến, ẩn m, π, hàm, luythua, tích phân


def la_rang_buoc_hop_le(dk: C.DieuKien) -> bool:
    """Mọi vế của ràng buộc là phân thức hữu tỉ theo tham số."""
    if isinstance(dk, C.SoSanh):
        return _la_phan_thuc(dk.trai) and _la_phan_thuc(dk.phai)
    return la_rang_buoc_hop_le(dk.a) and la_rang_buoc_hop_le(dk.b)


def _cac_mau(t: C.Nut) -> list[C.Nut]:
    """Mẫu của mọi phép chia trong biểu thức (đã chuẩn hóa), trừ mẫu là hằng khác 0."""
    ket_qua: list[C.Nut] = []
    if isinstance(t, C.Chia) and not (isinstance(t.b, C.So) and t.b.q != 0):
        ket_qua.append(t.b)
    for c in C.con(t):
        ket_qua += _cac_mau(c)
    return ket_qua


def _cac_mau_dk(dk: C.DieuKien) -> list[C.Nut]:
    if isinstance(dk, C.SoSanh):
        return _cac_mau(dk.trai) + _cac_mau(dk.phai)
    return _cac_mau_dk(dk.a) + _cac_mau_dk(dk.b)


def them_dieu_kien_mau(dk: C.DieuKien) -> C.DieuKien:
    """Thêm "mẫu ≠ 0" cho mọi mẫu không phải hằng khác 0: R := (m₁ ≠ 0 ∧ … ∧ mₖ ≠ 0) ∧ dk.

    Điều kiện mẫu đứng trước, nên khi một mẫu bằng 0 thì cả ràng buộc sai, bất kể `or`.
    """
    dk = chuan_hoa_dk(dk)
    mau_khong_trung: list[C.Nut] = []
    for m in _cac_mau_dk(dk):
        if m not in mau_khong_trung:
            mau_khong_trung.append(m)
    if not mau_khong_trung:
        return dk
    dieu_kien_mau: C.DieuKien = C.SoSanh("!=", mau_khong_trung[0], C.So(Fraction(0)))
    for m in mau_khong_trung[1:]:
        dieu_kien_mau = C.Va(dieu_kien_mau, C.SoSanh("!=", m, C.So(Fraction(0))))
    return C.Va(dieu_kien_mau, dk)


def gia_tri_huu_ti(t: C.Nut, gia_tri: dict[str, Fraction]) -> Fraction:
    """Giá trị chính xác của một phân thức hữu tỉ theo tham số. Ném ZeroDivisionError nếu chia cho 0."""
    if isinstance(t, C.So):
        return t.q
    if isinstance(t, C.ThamSo):
        return Fraction(gia_tri[t.ten])
    if isinstance(t, C.Am):
        return -gia_tri_huu_ti(t.a, gia_tri)
    if isinstance(t, C.Mu):
        return gia_tri_huu_ti(t.a, gia_tri) ** t.n
    a, b = gia_tri_huu_ti(t.a, gia_tri), gia_tri_huu_ti(t.b, gia_tri)
    if isinstance(t, C.Cong):
        return a + b
    if isinstance(t, C.Tru):
        return a - b
    if isinstance(t, C.Nhan):
        return a * b
    if isinstance(t, C.Chia):
        return a / b
    raise ValueError(f"Không phải phân thức hữu tỉ theo tham số: {t!r}")


def _danh_gia(dk: C.DieuKien, g: dict[str, Fraction]) -> bool:
    if isinstance(dk, C.SoSanh):
        return _SO_SANH[dk.op](gia_tri_huu_ti(dk.trai, g), gia_tri_huu_ti(dk.phai, g))
    if isinstance(dk, C.Va):
        return _danh_gia(dk.a, g) and _danh_gia(dk.b, g)
    return _danh_gia(dk.a, g) or _danh_gia(dk.b, g)


def danh_gia_rang_buoc(dk: C.DieuKien, gia_tri: dict[str, Fraction]) -> bool:
    """Tính chính xác ràng buộc (đã thêm điều kiện mẫu) tại một bộ giá trị tham số.

    Dùng để liệt kê miền hợp lệ ở A2. Điều kiện mẫu được tính trước, nên không bao giờ
    chia cho 0: khi một mẫu bằng 0, kết quả là sai, đúng như bản Lean (ở Lean 1/0 = 0 nhưng
    vế "mẫu ≠ 0" đã sai).
    """
    dk = them_dieu_kien_mau(dk)
    try:
        if any(gia_tri_huu_ti(m, gia_tri) == 0 for m in _cac_mau_dk(dk)):
            return False
        return _danh_gia(dk, gia_tri)
    except ZeroDivisionError:
        # Một mẫu lồng bên trong mẫu khác bằng 0: điều kiện "mẫu ≠ 0" của nó sai.
        return False


def mien_hop_le(dk: C.DieuKien, ten: str, tu: int, den: int) -> list[Fraction]:
    """Liệt kê các giá trị nguyên của một tham số trong [tu, den] thỏa ràng buộc."""
    return [Fraction(v) for v in range(tu, den + 1) if danh_gia_rang_buoc(dk, {ten: Fraction(v)})]


# ----- Điểm, cận, phương án T1 -----
def la_hang_theo_tham_so(t: C.Nut) -> bool:
    """Không chứa biến tự do và không chứa ẩn m (có thể chứa π, √, ln, tham số)."""
    return C.chi_chua_tham_so(chuan_hoa(t))
