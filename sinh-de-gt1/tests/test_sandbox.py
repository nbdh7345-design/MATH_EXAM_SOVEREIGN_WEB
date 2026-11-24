"""Kiểm thử sandbox (nghiệm thu M0, mục 13.2, 17). Chạy: pytest -m sandbox"""

from pathlib import Path

import pytest

from sinhde.cau_hinh import nap_cau_hinh
from sinhde.lean.chay_lean import LeanRunner
from sinhde.luu_tru.kho import Kho

pytestmark = [pytest.mark.sandbox, pytest.mark.lean]


@pytest.fixture(scope="module")
def runner(tmp_path_factory) -> LeanRunner:
    kho = Kho(tmp_path_factory.mktemp("csdl") / "t.sqlite")
    kho.tao_bang()
    return LeanRunner(nap_cau_hinh(), kho)


def test_tep_dung_dat(runner: LeanRunner):
    kq = runner.kiem_tep_tam("example : 1 + 1 = 2 := rfl\n", gioi_han_giay=60)
    assert kq.dat, kq.thong_bao


def test_tep_sai_khong_dat(runner: LeanRunner):
    kq = runner.kiem_tep_tam("example : 1 + 1 = 3 := rfl\n", gioi_han_giay=60)
    assert not kq.dat


def test_nap_thu_vien_gt(runner: LeanRunner):
    """Nạp ThuVienGT (kéo theo Mathlib) trong sandbox; lần đầu có thể chậm."""
    noi_dung = "import ThuVienGT\nexample : (2:ℝ) + 2 = 4 := by norm_num\n"
    kq = runner.kiem_tep_tam(noi_dung, gioi_han_giay=300)
    assert kq.dat, kq.thong_bao


def test_truy_cap_mang_bi_chan(runner: LeanRunner):
    noi_dung = (
        "def thu : IO Unit := do\n"
        "  let r ← IO.Process.output { cmd := \"curl\","
        " args := #[\"-sS\", \"--max-time\", \"5\", \"https://example.com\"] }\n"
        "  IO.println s!\"MA_THOAT={r.exitCode}\"\n"
        "#eval thu\n"
    )
    kq = runner.kiem_tep_tam(noi_dung, gioi_han_giay=60)
    assert "MA_THOAT=" in kq.thong_bao, kq.thong_bao
    assert "MA_THOAT=0" not in kq.thong_bao, "Lean truy cập được mạng!"


def test_ghi_vao_du_an_bi_chan(runner: LeanRunner):
    noi_dung = "#eval IO.FS.writeFile \"/du_an/thu_ghi.txt\" \"x\"\n"
    kq = runner.kiem_tep_tam(noi_dung, gioi_han_giay=60)
    assert not kq.dat
    assert not (runner.thu_muc_lean / "thu_ghi.txt").exists()


def test_qua_gio_bi_dung(runner: LeanRunner):
    kq = runner.kiem_tep_tam("#eval IO.sleep 60000\n", gioi_han_giay=5)
    assert not kq.dat
    assert "quá giới hạn" in kq.thong_bao


def test_build_module_trong_sandbox(runner: LeanRunner):
    """Nghiệm thu M0: `lake build` chạy được trong sandbox, chỉ `.lake/build` được ghi."""
    kq = runner.build_module("ThuVienGT", gioi_han_giay=300)
    assert kq.dat, kq.thong_bao


def test_moi_lan_chay_duoc_ghi(runner: LeanRunner):
    with runner.kho.ket_noi() as kn:
        so = kn.execute("SELECT COUNT(*) FROM lan_chay_lean").fetchone()[0]
    assert so >= 1
