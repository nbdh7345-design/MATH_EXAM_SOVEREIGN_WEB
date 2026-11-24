"""Kiểm thử phần tính bao đóng import (thử nghiệm 1, M0). Không cần Lean."""

from pathlib import Path

from sinhde.lean.bao_dong_import import bao_dong_import, doc_import, kich_thuoc_olean


def test_doc_import_cac_dang():
    van_ban = (
        "/-! Tài liệu. -/\n"
        "module\n"
        "public import Mathlib.A\n"
        "import Mathlib.B  -- ghi chú\n"
        "public meta import Mathlib.C\n"
        "import all Mathlib.D\n"
        "\n"
        "namespace X\n"
        "import Mathlib.KhongPhaiImport\n"
    )
    assert doc_import(van_ban) == ["Mathlib.A", "Mathlib.B", "Mathlib.C", "Mathlib.D"]


def _tep(p: Path, noi_dung: str = "") -> None:
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(noi_dung, encoding="utf-8")


def test_bao_dong_va_kich_thuoc(tmp_path: Path):
    goi = tmp_path / ".lake" / "packages" / "mathlib"
    _tep(tmp_path / "Goc.lean", "import Mathlib.A\nimport Init.Core\n")
    _tep(goi / "Mathlib" / "A.lean", "module\npublic import Mathlib.B\n")
    _tep(goi / "Mathlib" / "B.lean", "module\npublic import Mathlib.A\n")  # vòng lặp
    _tep(goi / "Mathlib" / "C.lean", "module\n")                            # không được import
    build = goi / ".lake" / "build" / "lib" / "lean" / "Mathlib"
    for ten in ("A", "B", "C"):
        for duoi in (".olean", ".olean.private", ".olean.server", ".olean.hash"):
            _tep(build / f"{ten}{duoi}", "x" * 10)

    assert sorted(t for t, _ in bao_dong_import(["Goc"], tmp_path)) == ["Goc", "Mathlib.A", "Mathlib.B"]
    # Goc chưa có tệp build; .hash không tính; C không được import.
    assert kich_thuoc_olean(["Goc"], tmp_path) == (3, 60)
