"""Kiểm thử M0 không cần Lean: cấu hình và CSDL."""

from pathlib import Path

import pydantic
import pytest
import yaml

from sinhde.cau_hinh import THU_MUC_GOC, CauHinh, nap_cau_hinh
from sinhde.luu_tru.kho import Kho


def test_config_hop_le():
    ch = nap_cau_hinh()
    assert ch.che_do in ("phat_trien", "chinh_thuc")
    assert ch.lean.so_tien_trinh >= 1


def test_config_tu_choi_khoa_la(tmp_path: Path):
    du_lieu = yaml.safe_load((THU_MUC_GOC / "config.yaml").read_text(encoding="utf-8"))
    du_lieu["khoa_la"] = 1
    with pytest.raises(pydantic.ValidationError):
        CauHinh.model_validate(du_lieu)


def test_tao_bang_va_ghi_lan_chay(tmp_path: Path):
    kho = Kho(tmp_path / "t.sqlite")
    kho.tao_bang()
    kho.tao_bang()  # chạy lại không lỗi
    ma = kho.ghi_lan_chay_lean("kiem_tep_tam", "Tep.lean", "abc", "dat", "", 12)
    with kho.ket_noi() as kn:
        bang = {r[0] for r in kn.execute("SELECT name FROM sqlite_master WHERE type='table'")}
        dong = kn.execute("SELECT che_do, ket_qua FROM lan_chay_lean WHERE id=?", (ma,)).fetchone()
    assert {"phien_ban_nen_tang", "khuon", "cau", "kiem_mau", "lan_goi_llm",
            "lan_chay_lean", "lan_kiem", "dot_sinh"} <= bang
    assert dong == ("kiem_tep_tam", "dat")


def test_moi_module_import_duoc():
    """Bắt lỗi kiểu 'tệp mã nguồn bị .gitignore loại mất'."""
    import importlib
    import pkgutil

    import sinhde

    for m in pkgutil.walk_packages(sinhde.__path__, "sinhde."):
        importlib.import_module(m.name)
