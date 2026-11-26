"""Kiểm thử N1 (mục 6.7): văn phạm, bộ đọc, cây, bộ in chuỗi, chuẩn hóa, đa thức theo tham số."""

from __future__ import annotations

import subprocess
import sys
from fractions import Fraction as F
from pathlib import Path

import mpmath as mp
import pytest
from hypothesis import HealthCheck, assume, given, settings
from hypothesis import strategies as st

from sinhde.nen_tang import cay as C
from sinhde.nen_tang.chuan_hoa import chuan_hoa
from sinhde.nen_tang.da_thuc_tham_so import (danh_gia_dieu_kien, dieu_kien_la_da_thuc,
                                             gia_tri_chinh_xac, la_da_thuc_tham_so)
from sinhde.nen_tang.danh_gia import KhongRo, xac_dinh_va_gia_tri
from sinhde.nen_tang.in_chuoi import in_chuoi, in_dieu_kien
from sinhde.nen_tang.van_pham import LoiVanPham, doc_bieu_thuc, doc_diem, doc_dieu_kien

x, a, b, c = C.Bien(), C.ThamSo("a"), C.ThamSo("b"), C.ThamSo("c")


def So(n, d=1):
    return C.So(F(n, d))


# ---------------- Chuỗi hợp lệ và cây mong đợi ----------------
@pytest.mark.parametrize("chuoi, cay", [
    ("-x^2", C.Am(C.Mu(x, 2))),
    ("sin(x)^2", C.Mu(C.Ham("sin", x), 2)),
    ("sin(x^2)", C.Ham("sin", C.Mu(x, 2))),
    ("2*x/3", C.Chia(C.Nhan(So(2), x), So(3))),
    ("x^(-1)", C.Mu(x, -1)),
    ("a - b - c", C.Tru(C.Tru(a, b), c)),
    ("a - (b - c)", C.Tru(a, C.Tru(b, c))),
    ("(-x)^2", C.Mu(C.Am(x), 2)),
    ("-x*y", C.Nhan(C.Am(x), C.ThamSo("y"))),
    ("luythua(x, 1/2)", C.LuyThua(x, C.Chia(So(1), So(2)))),
    ("  x  +  1 ", C.Cong(x, So(1))),
])
def test_chuoi_hop_le(chuoi, cay):
    assert doc_bieu_thuc(chuoi) == cay


def test_dieu_kien_and_uu_tien_hon_or():
    assert doc_dieu_kien("a > 0 and a != 3 or a = 5") == C.Hoac(
        C.Va(C.SoSanh(">", a, So(0)), C.SoSanh("!=", a, So(3))), C.SoSanh("=", a, So(5)))


def test_cac_phep_so_sanh():
    for op in ("<", "<=", ">", ">=", "=", "!="):
        assert doc_dieu_kien(f"a {op} 1") == C.SoSanh(op, a, So(1))


def test_diem():
    assert doc_diem("a^2 - 1/2") == C.Tru(C.Mu(a, 2), C.Chia(So(1), So(2)))


# ---------------- Chuỗi bị cấm ----------------
@pytest.mark.parametrize("chuoi", [
    "sin x", "2x", "log(x)", "x^y", "x^1.5", "tan^-1(x)", "1.5", "e*x",
    "x^2^3", "sin(x", "", "x +", "ab", "i + 1", "o", "a and b",
])
def test_chuoi_bi_cam(chuoi):
    with pytest.raises(LoiVanPham):
        doc_bieu_thuc(chuoi)


def test_loi_co_dong_cot():
    with pytest.raises(LoiVanPham) as e:
        doc_bieu_thuc("x + 2x")
    assert e.value.dong == 1 and e.value.cot is not None


def test_x_khong_duoc_trong_rang_buoc_nhung_van_doc_duoc():
    # Văn phạm đọc được; phép kiểm E_X_SAI_CHO (mục 11.2) nằm ở A2, không ở văn phạm.
    assert C.chua_bien(doc_dieu_kien("x > 0").trai)


# ---------------- Bộ tách từ ----------------
@pytest.mark.parametrize("ten", C.TEN_HAM)
def test_ten_ham_khong_bi_doc_thanh_tham_so(ten):
    assert doc_bieu_thuc(f"{ten}(x)") == C.Ham(ten, x)
    assert doc_bieu_thuc(f"{ten}(a) + a") == C.Cong(C.Ham(ten, a), a)


def test_tu_khoa_khong_bi_doc_thanh_tham_so():
    assert doc_bieu_thuc("luythua(a, x)") == C.LuyThua(a, x)
    assert doc_dieu_kien("a = 1 and b = 2") == C.Va(C.SoSanh("=", a, So(1)), C.SoSanh("=", b, So(2)))
    assert doc_dieu_kien("a = 1 or b = 2") == C.Hoac(C.SoSanh("=", a, So(1)), C.SoSanh("=", b, So(2)))


@pytest.mark.parametrize("chu", C.CHU_THAM_SO)
def test_moi_chu_tham_so(chu):
    assert doc_bieu_thuc(chu) == C.ThamSo(chu)


@pytest.mark.parametrize("chu", "eijlo")
def test_chu_bi_loai_khong_la_tham_so(chu):
    with pytest.raises(LoiVanPham):
        doc_bieu_thuc(chu)


# ---------------- Cây: S-biểu thức, JSON, tiện ích ----------------
def test_to_sexpr():
    assert C.to_sexpr(So(4)) == "(hang 4/1)"
    assert C.to_sexpr(So(-1, 2)) == "(hang -1/2)"
    assert C.to_sexpr(C.Mu(x, -1)) == "(mu x -1)"
    assert C.to_sexpr(C.Chia(C.Tru(C.Mu(x, 2), So(4)), C.Tru(x, So(2)))) == \
        "(chia (tru (mu x 2) (hang 4/1)) (tru x (hang 2/1)))"
    assert C.to_sexpr(C.Ham("sqrt", x)) == "(ham sqrt x)"
    with pytest.raises(ValueError):
        C.to_sexpr(a)


def test_tien_ich():
    t = doc_bieu_thuc("(x^2 - a^2)/(x - a)")
    assert C.chua_bien(t) and C.tham_so_dung(t) == {"a"}
    assert C.so_nut(t) == 9 and C.do_sau(t) == 4
    assert C.thay_tham_so(t, {"a": F(2)}) == doc_bieu_thuc("(x^2 - 2^2)/(x - 2)")


# ---------------- Chuẩn hóa: các trường hợp của bảng 6.5 ----------------
@pytest.mark.parametrize("chuoi, mong_doi", [
    ("-(3)", So(-3)),
    ("1/2 + 1/3", So(5, 6)),
    ("x + -2", C.Tru(x, So(2))),
    ("x - -2", C.Cong(x, So(2))),
    ("1*x", x),
    ("-1*x", C.Am(x)),
    ("-3*x", C.Am(C.Nhan(So(3), x))),
    ("x*2", C.Nhan(x, So(2))),
    ("0*x", C.Nhan(So(0), x)),             # không bỏ thừa số 0
    ("1/0", C.Chia(So(1), So(0))),         # không gộp chia cho 0
    ("0^0", C.Mu(So(0), 0)),               # 0^0 không gộp
    ("0^(-1)", C.Mu(So(0), -1)),
    ("0^2", So(0)),
    ("2^(-1)", So(1, 2)),
    ("x^1", x),
    ("(x^2 - a^2)/(x - a)", doc_bieu_thuc("(x^2 - a^2)/(x - a)")),  # có tham số: không gộp
])
def test_chuan_hoa_bang(chuoi, mong_doi):
    assert chuan_hoa(doc_bieu_thuc(chuoi)) == mong_doi


def test_chuan_hoa_khuon_sau_khi_the():
    t = C.thay_tham_so(doc_bieu_thuc("(x^2 - a^2)/(x - a)"), {"a": F(2)})
    assert chuan_hoa(t) == C.Chia(C.Tru(C.Mu(x, 2), So(4)), C.Tru(x, So(2)))


# ---------------- Đa thức theo tham số (6.6) ----------------
def test_da_thuc_tham_so():
    assert la_da_thuc_tham_so(doc_diem("a^2 - 3*a/2 + 1"))
    assert la_da_thuc_tham_so(doc_diem("(a + 1)/4"))
    assert not la_da_thuc_tham_so(doc_diem("1/a"))
    assert not la_da_thuc_tham_so(doc_diem("a^(-1)"))
    assert not la_da_thuc_tham_so(doc_diem("sqrt(a)"))
    assert not la_da_thuc_tham_so(doc_diem("x + a"))
    assert gia_tri_chinh_xac(doc_diem("a^2 - 3*a/2 + 1"), {"a": F(3)}) == F(11, 2)


def test_rang_buoc():
    dk = doc_dieu_kien("a != 0 and a^2 < 10 or a = 7")
    assert dieu_kien_la_da_thuc(dk)
    hop_le = [v for v in range(-5, 9) if danh_gia_dieu_kien(dk, {"a": F(v)})]
    assert hop_le == [-3, -2, -1, 1, 2, 3, 7]
    assert not dieu_kien_la_da_thuc(doc_dieu_kien("1/a > 0"))


# ---------------- Kiểm thử theo tính chất (Hypothesis) ----------------
_la = st.one_of(
    st.builds(C.So, st.fractions(min_value=-9, max_value=9, max_denominator=4)),
    st.just(x),
    st.sampled_from([a, b]),
)


def _mo_rong(con):
    return st.one_of(
        st.builds(C.Am, con),
        st.builds(C.Cong, con, con), st.builds(C.Tru, con, con),
        st.builds(C.Nhan, con, con), st.builds(C.Chia, con, con),
        st.builds(C.Mu, con, st.integers(-2, 3)),
        st.builds(C.LuyThua, con, con),
        st.builds(C.Ham, st.sampled_from(C.TEN_HAM), con),
    )


cay_ngau_nhien = st.recursive(_la, _mo_rong, max_leaves=12)
_cai_dat = dict(deadline=None, suppress_health_check=[HealthCheck.too_slow])


@settings(max_examples=5000, **_cai_dat)
@given(cay_ngau_nhien)
def test_khu_hoi_chuoi(t):
    """chuan_hoa(doc_bieu_thuc(in_chuoi(t))) == t với mọi cây t đã chuẩn hóa (mục 6.4)."""
    t = chuan_hoa(t)
    assert chuan_hoa(doc_bieu_thuc(in_chuoi(t))) == t


@settings(max_examples=2000, **_cai_dat)
@given(cay_ngau_nhien)
def test_chuan_hoa_luy_dang(t):
    assert chuan_hoa(chuan_hoa(t)) == chuan_hoa(t)


@settings(max_examples=2000, **_cai_dat)
@given(cay_ngau_nhien)
def test_json_hai_chieu(t):
    assert C.from_json(C.to_json(t)) == t


_diem_huu_ti = st.fractions(min_value=-3, max_value=3, max_denominator=7)


@settings(max_examples=2000, **_cai_dat)
@given(cay_ngau_nhien, _diem_huu_ti, _diem_huu_ti, _diem_huu_ti)
def test_chuan_hoa_giu_gia_tri_va_dieu_kien_xac_dinh(t, x0, a0, b0):
    """Chuẩn hóa không đổi giá trị và điều kiện xác định (mục 6.5) tại điểm hữu tỉ."""
    g = {"a": a0, "b": b0}
    try:
        xd1, v1 = xac_dinh_va_gia_tri(t, x0, g)
        xd2, v2 = xac_dinh_va_gia_tri(chuan_hoa(t), x0, g)
    except (KhongRo, OverflowError, ZeroDivisionError):
        assume(False)
        return
    assert xd1 == xd2
    if xd1:
        m1 = mp.mpf(v1.numerator) / v1.denominator if isinstance(v1, F) else v1
        m2 = mp.mpf(v2.numerator) / v2.denominator if isinstance(v2, F) else v2
        assume(mp.isfinite(m1) and mp.isfinite(m2))
        assert abs(m1 - m2) <= mp.mpf(10) ** -25 * max(1, abs(m1)), (t, x0, g, m1, m2)


_so_sanh = st.builds(C.SoSanh, st.sampled_from(["<", "<=", ">", ">=", "=", "!="]),
                     cay_ngau_nhien.map(chuan_hoa), cay_ngau_nhien.map(chuan_hoa))


def _gap_trai(loai, cac):
    kq = cac[0]
    for t in cac[1:]:
        kq = loai(kq, t)
    return kq


# Ràng buộc đúng dạng văn phạm sinh ra: các chuỗi `and` (kết hợp trái) nối bằng `or` (kết hợp trái).
dieu_kien_ngau_nhien = st.lists(st.lists(_so_sanh, min_size=1, max_size=3), min_size=1, max_size=3).map(
    lambda nhom: _gap_trai(C.Hoac, [_gap_trai(C.Va, n) for n in nhom]))


@settings(max_examples=1000, **_cai_dat)
@given(dieu_kien_ngau_nhien)
def test_in_dieu_kien_khu_hoi(dk):
    from sinhde.nen_tang.chuan_hoa import chuan_hoa_dk
    assert chuan_hoa_dk(doc_dieu_kien(in_dieu_kien(dk))) == dk


# ---------------- Công cụ kiểm văn phạm ----------------
def test_tools_kiem_van_pham():
    goc = Path(__file__).resolve().parent.parent
    kq = subprocess.run([sys.executable, str(goc / "tools" / "kiem_van_pham.py")],
                        capture_output=True, text=True)
    assert kq.returncode == 0, kq.stdout + kq.stderr
    assert "đạt" in kq.stdout
