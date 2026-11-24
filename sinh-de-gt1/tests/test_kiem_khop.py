"""Kiểm thử tiện ích đối chiếu kiem_khop (M0, thử nghiệm 3; mục 12.7, 16.1).

Chạy: pytest -m sandbox tests/test_kiem_khop.py
"""

import json

import pytest

from sinhde.cau_hinh import nap_cau_hinh
from sinhde.lean.chay_lean import LeanRunner
from sinhde.luu_tru.kho import Kho

pytestmark = [pytest.mark.sandbox, pytest.mark.lean]

# Kiểu `(2 : Nat) + 2 = 4`, dựng thẳng bằng S-biểu thức của Expr (không qua bộ phân tích Lean).
KIEU = "(a (c Eq 1) (c Nat) (a (c Nat.add) (n 2) (n 2)) (n 4))"


@pytest.fixture(scope="module")
def runner(tmp_path_factory) -> LeanRunner:
    kho = Kho(tmp_path_factory.mktemp("csdl") / "t.sqlite")
    kho.tao_bang()
    r = LeanRunner(nap_cau_hinh(), kho)
    for muc_tieu in ("KiemThu.ThuNghiem", "KiemThu.TanCong", "kiem_khop"):
        kq = r.build_module(muc_tieu, gioi_han_giay=600)
        assert kq.dat, kq.thong_bao
    return r


def kiem(r: LeanRunner, module: str, dinh_ly: str, kieu: str = KIEU):
    kq = r.kiem_khop({"module": module, "dinh_ly": dinh_ly, "kieu": kieu}, gioi_han_giay=120)
    try:
        ket_qua = json.loads(kq.thong_bao)
    except json.JSONDecodeError:
        ket_qua = None
    return kq, ket_qua


def test_dinh_ly_dung_dat(runner):
    kq, j = kiem(runner, "KiemThu.ThuNghiem", "KiemThu.ThuNghiem.dung")
    assert kq.dat, kq.thong_bao
    assert j["axioms"] == []


def test_sai_kieu_bi_loai(runner):
    kq, j = kiem(runner, "KiemThu.ThuNghiem", "KiemThu.ThuNghiem.gia")
    assert not kq.dat
    assert j["khop_kieu"] is False


def test_axiom_tu_khai_bi_loai(runner):
    kq, j = kiem(runner, "KiemThu.ThuNghiem", "KiemThu.ThuNghiem.dungAxiomTuKhai")
    assert not kq.dat
    assert j["khop_kieu"] is True and j["axiom_chuan"] is False
    assert "KiemThu.ThuNghiem.tuKhai" in j["axioms"]


def test_axiom_khong_phai_theorem(runner):
    kq, j = kiem(runner, "KiemThu.ThuNghiem", "KiemThu.ThuNghiem.tuKhai")
    assert not kq.dat
    assert j["la_theorem"] is False


def test_dinh_ly_khong_ton_tai(runner):
    kq, j = kiem(runner, "KiemThu.ThuNghiem", "KiemThu.ThuNghiem.khongCo")
    assert not kq.dat
    assert j["ton_tai"] is False


def test_doi_nghia_ky_hieu_khong_lua_duoc(runner):
    """Module khai báo macro_rules đọc "(2 : Nat) + 2 = 4" thành True (mục 12.7, 16.1)."""
    kq, j = kiem(runner, "KiemThu.TanCong", "KiemThu.TanCong.tanCong")
    assert not kq.dat
    assert j["khop_kieu"] is False


def test_s_bieu_thuc_hong_bi_loai(runner):
    kq, j = kiem(runner, "KiemThu.ThuNghiem", "KiemThu.ThuNghiem.dung", kieu="(a (c Eq")
    assert not kq.dat
    assert j is None


def test_module_khong_ton_tai_bi_loai(runner):
    kq, _ = kiem(runner, "KiemThu.KhongCo", "KiemThu.KhongCo.dung")
    assert not kq.dat
