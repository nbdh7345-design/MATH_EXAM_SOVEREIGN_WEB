"""Kiểm thử N1 (mục 6.7 của thiết kế v2.1)."""

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
from sinhde.nen_tang.bieu_thuc_tham_so import (danh_gia_rang_buoc, la_hang_theo_tham_so,
                                               la_rang_buoc_hop_le, mien_hop_le, them_dieu_kien_mau)
from sinhde.nen_tang.chuan_hoa import chuan_hoa, chuan_hoa_dk, chuan_hoa_pa
from sinhde.nen_tang.danh_gia import KhongRo, xac_dinh_va_gia_tri
from sinhde.nen_tang.in_chuoi import in_chuoi, in_dieu_kien, in_phuong_an
from sinhde.nen_tang.van_pham import (LoiVanPham, doc_bieu_thuc, doc_dac_biet, doc_diem2,
                                      doc_dieu_kien, doc_phuong_an, doc_tap)

x, y, t, n = (C.Bien(v) for v in C.TEN_BIEN)
a, b, c = C.ThamSo("a"), C.ThamSo("b"), C.ThamSo("c")
m, pi, e = C.An(), C.Pi(), C.hang_e()


def So(p, q=1):
    return C.So(F(p, q))


# ================= Bộ đọc: chuỗi hợp lệ =================
@pytest.mark.parametrize("chuoi, cay", [
    # các ca của bản 1.2 vẫn đúng
    ("-x^2", C.Am(C.Mu(x, 2))),
    ("sin(x)^2", C.Mu(C.Ham("sin", x), 2)),
    ("sin(x^2)", C.Ham("sin", C.Mu(x, 2))),
    ("2*x/3", C.Chia(C.Nhan(So(2), x), So(3))),
    ("x^(-1)", C.Mu(x, -1)),
    ("a - b - c", C.Tru(C.Tru(a, b), c)),
    ("a - (b - c)", C.Tru(a, C.Tru(b, c))),
    ("(-x)^2", C.Mu(C.Am(x), 2)),
    ("  x  +  1 ", C.Cong(x, So(1))),
    # bổ sung của bản 2.1
    ("pi/4", C.Chia(pi, So(4))),
    ("e", e),
    ("e*x", C.Nhan(e, x)),
    ("luythua(x, 1/3)", C.LuyThua(x, C.Chia(So(1), So(3)))),
    ("luythua(2, x)", C.LuyThua(So(2), x)),
    ("tp(sin(t), 0, x^2)", C.TichPhanT(C.Ham("sin", t), So(0), C.Mu(x, 2))),
    ("x*y + n", C.Cong(C.Nhan(x, y), n)),
    ("m^2 - 1", C.Tru(C.Mu(m, 2), So(1))),
    ("tp(t*x, a, pi)", C.TichPhanT(C.Nhan(t, x), a, pi)),
])
def test_bieu_thuc_hop_le(chuoi, cay):
    assert doc_bieu_thuc(chuoi) == cay


def test_tap_khoang_va_phuong_an():
    assert doc_tap("kmo(-vc, 2) U kphai(3, vc)") == C.HopKhoang((
        C.Khoang("kmo", C.VoCung(False), So(2)), C.Khoang("kphai", So(3), C.VoCung(True))))
    assert doc_tap("{a, -a}") == C.TapHuuHan((a, C.Am(a)))
    assert doc_tap("rong") == C.TapRong()
    assert doc_tap("kdong(0, 1)") == C.HopKhoang((C.Khoang("kdong", So(0), So(1)),))
    assert doc_dac_biet("khong_ton_tai") == C.DacBiet("khong_ton_tai")
    assert doc_diem2("(1, a)") == C.Diem2(So(1), a)
    assert doc_phuong_an("duong_vc", "T1") == C.DacBiet("duong_vc")
    assert doc_phuong_an("2*a", "T1") == C.Nhan(So(2), a)
    assert doc_phuong_an("ktrai(0, pi)", "T2") == C.HopKhoang((C.Khoang("ktrai", So(0), pi),))


def test_dieu_kien_and_uu_tien_hon_or():
    assert doc_dieu_kien("a > 0 and a != 3 or a = 5") == C.Hoac(
        C.Va(C.SoSanh(">", a, So(0)), C.SoSanh("!=", a, So(3))), C.SoSanh("=", a, So(5)))


# ================= Bộ đọc: chuỗi bị từ chối =================
@pytest.mark.parametrize("chuoi", [
    "sin x", "2x", "log(x)", "x^y", "x^1.5", "tan^-1(x)", "1.5",
    "x^2^3", "sin(x", "", "x +", "ab", "i + 1", "o", "a and b", "luythua(x)",
])
def test_bieu_thuc_bi_tu_choi(chuoi):
    with pytest.raises(LoiVanPham):
        doc_bieu_thuc(chuoi)


@pytest.mark.parametrize("chuoi", ["luythua(x, 2)", "luythua(x, -1)", "luythua(x, 4/2)", "luythua(e, 3)"])
def test_luythua_so_mu_nguyen(chuoi):
    with pytest.raises(LoiVanPham) as loi:
        doc_bieu_thuc(chuoi)
    assert loi.value.ma == "E_LUYTHUA_NGUYEN"


@pytest.mark.parametrize("chuoi", ["t", "t + x", "tp(t, t, 1)", "tp(t, 0, t^2)", "sin(t)"])
def test_bien_t_sai_cho(chuoi):
    with pytest.raises(LoiVanPham) as loi:
        doc_bieu_thuc(chuoi)
    assert loi.value.ma == "E_BIEN_T"


@pytest.mark.parametrize("chuoi", ["{}", "kmo(1)", "kmo(1, 2) U", "{a,}", "vc", "kmo(1, 2) U {a}"])
def test_tap_bi_tu_choi(chuoi):
    with pytest.raises(LoiVanPham):
        doc_tap(chuoi)


def test_loi_co_dong_cot():
    with pytest.raises(LoiVanPham) as e_:
        doc_bieu_thuc("x + 2x")
    assert e_.value.dong == 1 and e_.value.cot is not None and e_.value.ma == "E_VAN_PHAM"


# ================= Bộ tách từ =================
@pytest.mark.parametrize("ten", C.TEN_HAM)
def test_ten_ham_khong_bi_doc_thanh_tham_so(ten):
    assert doc_bieu_thuc(f"{ten}(x)") == C.Ham(ten, x)
    assert doc_bieu_thuc(f"{ten}(a) + a") == C.Cong(C.Ham(ten, a), a)


def test_tu_khoa_khong_bi_doc_thanh_tham_so():
    assert doc_bieu_thuc("pi + p") == C.Cong(pi, C.ThamSo("p"))
    assert doc_bieu_thuc("tp(t, 0, 1) + n") == C.Cong(C.TichPhanT(t, So(0), So(1)), n)
    assert doc_bieu_thuc("exp(x) + e") == C.Cong(C.Ham("exp", x), e)
    assert doc_dieu_kien("a = 1 and b = 2") == C.Va(C.SoSanh("=", a, So(1)), C.SoSanh("=", b, So(2)))
    assert doc_tap("kmo(k, vc)") == C.HopKhoang((C.Khoang("kmo", C.ThamSo("k"), C.VoCung(True)),))
    assert doc_tap("{r, v}") == C.TapHuuHan((C.ThamSo("r"), C.ThamSo("v")))


@pytest.mark.parametrize("chu", C.CHU_THAM_SO)
def test_moi_chu_tham_so(chu):
    assert doc_bieu_thuc(chu) == C.ThamSo(chu)


@pytest.mark.parametrize("chu", "ijlo")
def test_chu_khong_dung(chu):
    with pytest.raises(LoiVanPham):
        doc_bieu_thuc(chu)


# ================= Cây =================
def test_to_sexpr():
    assert C.to_sexpr(So(4)) == "(hang 4/1)"
    assert C.to_sexpr(So(-1, 2)) == "(hang -1/2)"
    assert C.to_sexpr(C.Mu(x, -1)) == "(mu (bien x) -1)"
    assert C.to_sexpr(C.Chia(C.Tru(C.Mu(x, 2), So(4)), C.Tru(x, So(2)))) == \
        "(chia (tru (mu (bien x) 2) (hang 4/1)) (tru (bien x) (hang 2/1)))"
    assert C.to_sexpr(C.TichPhanT(C.Ham("sin", t), So(0), x)) == "(tpt (ham sin (bien t)) (hang 0/1) (bien x))"
    assert C.to_sexpr(C.Chia(pi, So(4))) == "(chia pi (hang 4/1))"
    assert C.to_sexpr(m) == "an"
    assert C.to_sexpr(doc_tap("kmo(-vc, 2)")) == "(tap hop (khoang kmo amvc (so (hang 2/1))))"
    assert C.to_sexpr(doc_tap("{1, 2}")) == "(tap huuhan (hang 1/1) (hang 2/1))"
    assert C.to_sexpr(C.TapRong()) == "(tap rong)"
    assert C.to_sexpr(C.DacBiet("am_vc")) == "(dacbiet am_vc)"
    assert C.to_sexpr(C.Diem2(So(1), So(0))) == "(diem2 (hang 1/1) (hang 0/1))"
    with pytest.raises(ValueError):
        C.to_sexpr(a)


def test_tien_ich():
    tc = doc_bieu_thuc("(x^2 - a^2)/(x - a)")
    assert C.chua_bien(tc) and C.tham_so_dung(tc) == {"a"}
    assert C.so_nut(tc) == 9 and C.do_sau(tc) == 4
    assert C.thay_tham_so(tc, {"a": F(2)}) == doc_bieu_thuc("(x^2 - 2^2)/(x - 2)")
    tp_ = doc_bieu_thuc("tp(t*y, 0, x)")
    assert C.bien_dung(tp_) == {"t", "x", "y"} and C.bien_tu_do(tp_) == {"x", "y"}
    assert C.chi_chua_tham_so(doc_bieu_thuc("pi/a + ln(2)")) and not C.chi_chua_tham_so(doc_bieu_thuc("m + 1"))
    assert C.chi_chua_tham_so(doc_bieu_thuc("tp(t, 0, 1)"))


# ================= Chuẩn hóa =================
@pytest.mark.parametrize("chuoi, mong_doi", [
    ("-(3)", So(-3)),
    ("1/2 + 1/3", So(5, 6)),
    ("x + -2", C.Tru(x, So(2))),
    ("x - -2", C.Cong(x, So(2))),
    ("1*x", x),
    ("-1*x", C.Am(x)),
    ("-3*x", C.Am(C.Nhan(So(3), x))),
    ("0*x", C.Nhan(So(0), x)),             # không bỏ thừa số 0
    ("1/0", C.Chia(So(1), So(0))),         # không gộp chia cho 0
    ("0^0", C.Mu(So(0), 0)),               # 0^0 không gộp
    ("2^(-1)", So(1, 2)),
    ("x^1", x),
    ("pi*1", C.Nhan(pi, So(1))),           # không có quy tắc cho thừa số 1 bên phải
    ("e^2", C.Ham("exp", So(2))),          # bản 2.1: e^n = exp(n)
    ("e^(-1)", C.Ham("exp", So(-1))),
    ("luythua(e, x)", C.Ham("exp", x)),    # bản 2.1: e^b = exp(b)
    ("e^1", e),
    ("tp(1 + 1, 0*1, 2/2)", C.TichPhanT(So(2), So(0), So(1))),
])
def test_chuan_hoa_bang(chuoi, mong_doi):
    assert chuan_hoa(doc_bieu_thuc(chuoi)) == mong_doi


def test_chuan_hoa_phuong_an_khong_sap_khong_bo_trung():
    assert chuan_hoa_pa(doc_tap("{2/2, 1, -(-1)}")) == C.TapHuuHan((So(1), So(1), So(1)))
    assert chuan_hoa_pa(doc_tap("kmo(1 + 1, vc)")) == C.HopKhoang((C.Khoang("kmo", So(2), C.VoCung(True)),))


# ================= Biểu thức theo tham số (6.6) =================
def test_rang_buoc_phan_thuc_va_dieu_kien_mau():
    dk = doc_dieu_kien("a/(a - 2) > 1 or a = 7")
    assert la_rang_buoc_hop_le(dk)
    assert them_dieu_kien_mau(dk) == C.Va(
        C.SoSanh("!=", C.Tru(a, So(2)), So(0)), chuan_hoa_dk(dk))
    # a/(a-2) > 1 ⇔ a > 2 (khi a ≠ 2); hoặc a = 7; a = 2 bị loại bởi điều kiện mẫu
    assert [int(v) for v in mien_hop_le(dk, "a", -3, 8)] == [3, 4, 5, 6, 7, 8]
    assert not danh_gia_rang_buoc(doc_dieu_kien("a = 2 or 1/(a - 2) > 0"), {"a": F(2)})
    assert not danh_gia_rang_buoc(doc_dieu_kien("1/(1/a) > 0"), {"a": F(0)})  # mẫu lồng


@pytest.mark.parametrize("chuoi, hop_le", [
    ("a^2 - 3*a/2 + 1 > 0", True), ("(a + 1)/4 < 2", True), ("1/a != 0", True),
    ("a^(-1) > 0", False), ("sqrt(a) > 1", False), ("x + a > 0", False), ("pi > a", False), ("m > 0", False),
])
def test_rang_buoc_hop_le(chuoi, hop_le):
    assert la_rang_buoc_hop_le(doc_dieu_kien(chuoi)) is hop_le


def test_la_hang_theo_tham_so():
    for s in ("pi/4", "sqrt(a)", "1/a", "ln(2) + e", "tp(t^2, 0, a)"):
        assert la_hang_theo_tham_so(doc_bieu_thuc(s)), s
    for s in ("x", "a*y", "m", "n + 1"):
        assert not la_hang_theo_tham_so(doc_bieu_thuc(s)), s


# ================= Kiểm thử theo tính chất (Hypothesis) =================
def _la(cho_phep_t: bool):
    bien = [x, y, n] + ([t] if cho_phep_t else [])
    return st.one_of(
        st.builds(C.So, st.fractions(min_value=-9, max_value=9, max_denominator=4)),
        st.sampled_from(bien + [a, b, m, pi, e]),
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


_cay_khong_t = st.recursive(_la(False), _mo_rong, max_leaves=10)
_than_tp = st.recursive(_la(True), _mo_rong, max_leaves=5)


def _them_tp(con):
    return st.one_of(con, st.builds(C.TichPhanT, _than_tp, _cay_khong_t, _cay_khong_t))


cay_ngau_nhien = st.recursive(_la(False), lambda con: _mo_rong(con) | _them_tp(con), max_leaves=12)
_cai_dat = dict(deadline=None, suppress_health_check=[HealthCheck.too_slow, HealthCheck.filter_too_much])


def _hop_le_voi_bo_doc(tc: C.Nut) -> bool:
    """Loại các cây mà bộ đọc cố ý từ chối: luythua số mũ nguyên (E_LUYTHUA_NGUYEN)."""
    for nut in [tc, *_moi_nut(tc)]:
        if isinstance(nut, C.LuyThua):
            sm = chuan_hoa(nut.b)
            if isinstance(sm, C.So) and sm.q.denominator == 1:
                return False
    return True


def _moi_nut(tc):
    for c_ in C.con(tc):
        yield c_
        yield from _moi_nut(c_)


@settings(max_examples=5000, **_cai_dat)
@given(cay_ngau_nhien)
def test_khu_hoi_chuoi(tc):
    """chuan_hoa(doc_bieu_thuc(in_chuoi(t))) == t với mọi cây t đã chuẩn hóa (mục 6.4)."""
    tc = chuan_hoa(tc)
    assume(_hop_le_voi_bo_doc(tc))
    assert chuan_hoa(doc_bieu_thuc(in_chuoi(tc))) == tc


@settings(max_examples=2000, **_cai_dat)
@given(cay_ngau_nhien)
def test_chuan_hoa_luy_dang(tc):
    assert chuan_hoa(chuan_hoa(tc)) == chuan_hoa(tc)


@settings(max_examples=2000, **_cai_dat)
@given(cay_ngau_nhien)
def test_json_hai_chieu(tc):
    assert C.from_json(C.to_json(tc)) == tc


_huu_ti = st.fractions(min_value=-3, max_value=3, max_denominator=7)


def _khong_co_tp(tc):
    return not isinstance(tc, C.TichPhanT) and all(_khong_co_tp(c_) for c_ in C.con(tc))


@settings(max_examples=2000, **_cai_dat)
@given(cay_ngau_nhien, _huu_ti, _huu_ti, _huu_ti, _huu_ti, _huu_ti, _huu_ti)
def test_chuan_hoa_giu_gia_tri_va_dieu_kien_xac_dinh(tc, x0, y0, n0, m0, a0, b0):
    """Chuẩn hóa không đổi giá trị và điều kiện xác định (mục 6.5) tại các điểm hữu tỉ."""
    assume(_khong_co_tp(tc))
    gan, g = {"x": x0, "y": y0, "n": n0, "m": m0}, {"a": a0, "b": b0}
    try:
        xd1, v1 = xac_dinh_va_gia_tri(tc, gan, g)
        xd2, v2 = xac_dinh_va_gia_tri(chuan_hoa(tc), gan, g)
    except (KhongRo, OverflowError, ZeroDivisionError):
        assume(False)
        return
    assert xd1 == xd2
    if xd1:
        m1 = mp.mpf(v1.numerator) / v1.denominator if isinstance(v1, F) else v1
        m2 = mp.mpf(v2.numerator) / v2.denominator if isinstance(v2, F) else v2
        assume(mp.isfinite(m1) and mp.isfinite(m2))
        assert abs(m1 - m2) <= mp.mpf(10) ** -25 * max(1, abs(m1)), (tc, gan, g, m1, m2)


# ---- phương án và ràng buộc ----
_bt_hang = st.recursive(st.one_of(st.builds(C.So, st.fractions(min_value=-9, max_value=9, max_denominator=4)),
                                  st.sampled_from([a, b, pi, e])), _mo_rong, max_leaves=5).map(chuan_hoa)
_dau_mut = st.one_of(_bt_hang, st.builds(C.VoCung, st.booleans()))
_khoang = st.builds(C.Khoang, st.sampled_from(C.KIEU_KHOANG), _dau_mut, _dau_mut)
tap_ngau_nhien = st.one_of(
    st.just(C.TapRong()),
    st.lists(_bt_hang, min_size=1, max_size=4).map(lambda ds: C.TapHuuHan(tuple(ds))),
    st.lists(_khoang, min_size=1, max_size=3).map(lambda ks: C.HopKhoang(tuple(ks))),
)


@settings(max_examples=3000, **_cai_dat)
@given(tap_ngau_nhien)
def test_khu_hoi_tap(tp_):
    assume(all(_hop_le_voi_bo_doc(bt) for bt in _bt_trong_tap(tp_)))
    assert chuan_hoa_pa(doc_tap(in_phuong_an(tp_))) == tp_


def _bt_trong_tap(tp_):
    if isinstance(tp_, C.TapHuuHan):
        return list(tp_.phan_tu)
    if isinstance(tp_, C.HopKhoang):
        return [d for k in tp_.cac_khoang for d in (k.trai, k.phai) if isinstance(d, C.Nut)]
    return []


@settings(max_examples=500, **_cai_dat)
@given(st.sampled_from(C.LOAI_DAC_BIET))
def test_khu_hoi_dac_biet(loai):
    assert doc_phuong_an(in_phuong_an(C.DacBiet(loai)), "T1") == C.DacBiet(loai)


_so_sanh = st.builds(C.SoSanh, st.sampled_from(["<", "<=", ">", ">=", "=", "!="]),
                     cay_ngau_nhien.map(chuan_hoa), cay_ngau_nhien.map(chuan_hoa))


def _gap_trai(loai, cac):
    kq = cac[0]
    for u in cac[1:]:
        kq = loai(kq, u)
    return kq


dieu_kien_ngau_nhien = st.lists(st.lists(_so_sanh, min_size=1, max_size=3), min_size=1, max_size=3).map(
    lambda nhom: _gap_trai(C.Hoac, [_gap_trai(C.Va, nh) for nh in nhom]))


def _dk_hop_le(dk):
    if isinstance(dk, C.SoSanh):
        return _hop_le_voi_bo_doc(dk.trai) and _hop_le_voi_bo_doc(dk.phai)
    return _dk_hop_le(dk.a) and _dk_hop_le(dk.b)


@settings(max_examples=1000, **_cai_dat)
@given(dieu_kien_ngau_nhien)
def test_khu_hoi_dieu_kien(dk):
    assume(_dk_hop_le(dk))
    assert chuan_hoa_dk(doc_dieu_kien(in_dieu_kien(dk))) == dk


# ================= Công cụ kiểm văn phạm =================
def test_tools_kiem_van_pham():
    goc = Path(__file__).resolve().parent.parent
    kq = subprocess.run([sys.executable, str(goc / "tools" / "kiem_van_pham.py")],
                        capture_output=True, text=True)
    assert kq.returncode == 0, kq.stdout + kq.stderr
    assert "đạt" in kq.stdout
