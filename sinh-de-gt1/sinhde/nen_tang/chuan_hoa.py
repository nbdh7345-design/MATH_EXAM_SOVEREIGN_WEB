"""Chuẩn hóa N1 (mục 6.5): một lượt từ lá lên gốc bằng các hàm dựng thông minh.

Thuật toán phải GIỐNG HỆT `chuanHoa` trong Lean (mục 7.3); hai bên được kiểm chéo ở mục 7.9.
Mỗi hàm dựng thử từng dòng của bảng theo thứ tự và dừng ở dòng đầu tiên khớp.
Không làm mất chỗ không xác định: không gộp chia cho 0, không gộp 0^n với n ≤ 0,
không bỏ thừa số 0.
"""

from __future__ import annotations

from sinhde.nen_tang import cay as C


def mk_am(a: C.Nut) -> C.Nut:
    if isinstance(a, C.So):
        return C.So(-a.q)
    return C.Am(a)


def mk_cong(a: C.Nut, b: C.Nut) -> C.Nut:
    if isinstance(a, C.So) and isinstance(b, C.So):
        return C.So(a.q + b.q)
    if isinstance(b, C.So) and b.q < 0:
        return C.Tru(a, C.So(-b.q))
    return C.Cong(a, b)


def mk_tru(a: C.Nut, b: C.Nut) -> C.Nut:
    if isinstance(a, C.So) and isinstance(b, C.So):
        return C.So(a.q - b.q)
    if isinstance(b, C.So) and b.q < 0:
        return C.Cong(a, C.So(-b.q))
    return C.Tru(a, b)


def mk_nhan(a: C.Nut, b: C.Nut) -> C.Nut:
    if isinstance(a, C.So) and isinstance(b, C.So):
        return C.So(a.q * b.q)
    if isinstance(a, C.So):
        p = a.q
        if p == 1:
            return b
        if p == -1:
            return C.Am(b)
        if p < 0:
            return C.Am(C.Nhan(C.So(-p), b))
    return C.Nhan(a, b)


def mk_chia(a: C.Nut, b: C.Nut) -> C.Nut:
    if isinstance(a, C.So) and isinstance(b, C.So) and b.q != 0:
        return C.So(a.q / b.q)
    return C.Chia(a, b)


def mk_mu(a: C.Nut, n: int) -> C.Nut:
    if isinstance(a, C.So):
        if a.q != 0 or n > 0:
            return C.So(a.q ** n)
        return C.Mu(a, n)
    if n == 1:
        return a
    return C.Mu(a, n)


def chuan_hoa(t: C.Nut) -> C.Nut:
    if isinstance(t, (C.So, C.Bien, C.ThamSo)):
        return t
    if isinstance(t, C.Am):
        return mk_am(chuan_hoa(t.a))
    if isinstance(t, C.Cong):
        return mk_cong(chuan_hoa(t.a), chuan_hoa(t.b))
    if isinstance(t, C.Tru):
        return mk_tru(chuan_hoa(t.a), chuan_hoa(t.b))
    if isinstance(t, C.Nhan):
        return mk_nhan(chuan_hoa(t.a), chuan_hoa(t.b))
    if isinstance(t, C.Chia):
        return mk_chia(chuan_hoa(t.a), chuan_hoa(t.b))
    if isinstance(t, C.Mu):
        return mk_mu(chuan_hoa(t.a), t.n)
    if isinstance(t, C.LuyThua):
        return C.LuyThua(chuan_hoa(t.a), chuan_hoa(t.b))
    if isinstance(t, C.Ham):
        return C.Ham(t.ten, chuan_hoa(t.a))
    raise TypeError(f"Không phải nút biểu thức: {t!r}")


def chuan_hoa_dk(dk: C.DieuKien) -> C.DieuKien:
    if isinstance(dk, C.SoSanh):
        return C.SoSanh(dk.op, chuan_hoa(dk.trai), chuan_hoa(dk.phai))
    return type(dk)(chuan_hoa_dk(dk.a), chuan_hoa_dk(dk.b))
