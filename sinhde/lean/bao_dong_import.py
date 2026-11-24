"""Bao đóng import của một module Lean và dung lượng tệp `.olean*` của nó (thử nghiệm 1, M0).

Dùng để đo một tệp Lean phải nạp bao nhiêu từ Mathlib. Không thuộc nền tin cậy.
"""

from __future__ import annotations

import re
from pathlib import Path

# Lean 4.36 (hệ thống module) tách mỗi module thành ba tệp; tệp không khai báo `module`
# nạp cả phần `.olean.private`, lớn gấp đôi phần `.olean`.
DUOI_OLEAN = (".olean", ".olean.private", ".olean.server")

# Gốc tên module → thư mục gói trong lean/.lake/packages
_GOI = {
    "Mathlib": "mathlib", "Batteries": "batteries", "Aesop": "aesop", "Qq": "Qq",
    "ProofWidgets": "proofwidgets", "Plausible": "plausible",
    "LeanSearchClient": "LeanSearchClient", "ImportGraph": "importGraph", "Cli": "Cli",
}
# Các module này nằm trong toolchain, trong ảnh Docker.
_TOOLCHAIN = {"Init", "Lean", "Std", "Lake"}

_DONG_IMPORT = re.compile(r"^\s*(?:public\s+)?(?:meta\s+)?import\s+(.+)$")
_TU_KHOA = {"public", "meta", "all", "private"}
# Phần đầu tệp kết thúc ở lệnh đầu tiên không phải import.
_HET_DAU_TEP = re.compile(
    r"^\s*(namespace|section|open|noncomputable|theorem|lemma|def|universe|variable|"
    r"set_option|attribute|instance|class|structure|abbrev|example|@\[|#)")


def doc_import(van_ban: str) -> list[str]:
    """Danh sách module được import ở phần đầu một tệp Lean."""
    ket_qua: list[str] = []
    for dong in van_ban.splitlines():
        dong = dong.split("--", 1)[0]
        if _HET_DAU_TEP.match(dong):
            break
        m = _DONG_IMPORT.match(dong)
        if m:
            ket_qua += [t for t in m.group(1).split() if t not in _TU_KHOA]
    return ket_qua


def _vi_tri(ten: str, thu_muc_lean: Path) -> tuple[Path, Path] | None:
    """(tệp nguồn, tiền tố đường dẫn tệp build) của module; None nếu thuộc toolchain."""
    goc = ten.split(".")[0]
    if goc in _TOOLCHAIN:
        return None
    goi = thu_muc_lean / ".lake" / "packages" / _GOI[goc] if goc in _GOI else thu_muc_lean
    tuong_doi = Path(*ten.split("."))
    nguon = goi / tuong_doi.parent / (tuong_doi.name + ".lean")
    build = goi / ".lake" / "build" / "lib" / "lean" / tuong_doi
    return nguon, build


def bao_dong_import(goc: list[str], thu_muc_lean: Path) -> list[tuple[str, Path]]:
    """Mọi module (ngoài toolchain) mà các module gốc import trực tiếp hoặc gián tiếp."""
    da_tham: set[str] = set()
    hang_doi = list(goc)
    ket_qua: list[tuple[str, Path]] = []
    while hang_doi:
        ten = hang_doi.pop()
        if ten in da_tham:
            continue
        da_tham.add(ten)
        vt = _vi_tri(ten, thu_muc_lean)
        if vt is None or not vt[0].exists():
            continue
        ket_qua.append((ten, vt[1]))
        hang_doi += doc_import(vt[0].read_text(encoding="utf-8", errors="replace"))
    return ket_qua


def kich_thuoc_olean(goc: list[str], thu_muc_lean: Path) -> tuple[int, int]:
    """(số module, tổng số byte các tệp .olean*) của bao đóng import."""
    cac = bao_dong_import(goc, thu_muc_lean)
    so_byte = 0
    for _, build in cac:
        for duoi in DUOI_OLEAN:
            tep = build.with_name(build.name + duoi)
            if tep.exists():
                so_byte += tep.stat().st_size
    return len(cac), so_byte
