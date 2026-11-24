"""LeanRunner: mọi lần chạy Lean đều đi qua sandbox Docker (mục 13.1, 13.2)."""

from __future__ import annotations

import hashlib
import os
import subprocess
import tempfile
import time
import uuid
from dataclasses import dataclass, field
from pathlib import Path

from sinhde.cau_hinh import CauHinh
from sinhde.luu_tru.kho import Kho

# Thông báo Lean dài được cắt ngắn trước khi lưu hoặc gửi đi (mục 11.5).
_THONG_BAO_TOI_DA = 20000
# Thời gian cộng thêm cho Docker khởi động và dọn container.
_DU_PHONG_GIAY = 30


@dataclass
class KetQuaLean:
    dat: bool
    thong_bao: str
    thoi_gian_ms: int
    axioms: dict[str, list[str]] = field(default_factory=dict)


class LeanRunner:
    def __init__(self, cau_hinh: CauHinh, kho: Kho | None = None) -> None:
        self.ch = cau_hinh
        self.kho = kho
        self.thu_muc_lean = cau_hinh.duong_dan_tuyet_doi(cau_hinh.duong_dan.lean)

    # ----- lệnh docker -----
    def _lenh_docker(self, ten: str, gan_them: list[str], doi_so: list[str],
                     ghi_build: bool = False) -> list[str]:
        uid, gid = os.getuid(), os.getgid()
        bo_nho = f"{self.ch.lean.bo_nho_gb}g"
        lenh = [
            "docker", "run", "--rm", "--name", ten,
            "--network", "none",
            "--memory", bo_nho, "--memory-swap", bo_nho,
            "--pids-limit", "256", "--cpus", "2",
            "--user", f"{uid}:{gid}",
            "--read-only", "--tmpfs", "/tmp:rw,size=512m",
            "-v", f"{self.thu_muc_lean}:/du_an:ro",
        ]
        if ghi_build:
            # Chỉ thư mục build của dự án được ghi (mục 13.2).
            build = self.thu_muc_lean / ".lake" / "build"
            lenh += ["-v", f"{build}:/du_an/.lake/build:rw"]
        lenh += gan_them + [self.ch.lean.anh_docker] + doi_so
        return lenh

    def _chay(self, che_do: str, muc_tieu: str, tep_hash: str, lenh: list[str],
              ten: str, gioi_han_giay: int) -> KetQuaLean:
        bat_dau = time.monotonic()
        try:
            p = subprocess.run(lenh, capture_output=True, text=True,
                               timeout=gioi_han_giay + _DU_PHONG_GIAY)
            dat = p.returncode == 0
            thong_bao = (p.stdout + p.stderr)
            if p.returncode == 124:
                thong_bao += f"\n[quá giới hạn {gioi_han_giay} giây]"
        except subprocess.TimeoutExpired:
            subprocess.run(["docker", "kill", ten], capture_output=True)
            dat, thong_bao = False, f"[quá giới hạn {gioi_han_giay} giây; đã dừng container]"
        ms = int((time.monotonic() - bat_dau) * 1000)
        thong_bao = thong_bao[-_THONG_BAO_TOI_DA:]
        if self.kho is not None:
            self.kho.ghi_lan_chay_lean(che_do, muc_tieu, tep_hash,
                                       "dat" if dat else "khong_dat", thong_bao, ms)
        return KetQuaLean(dat=dat, thong_bao=thong_bao, thoi_gian_ms=ms)

    # ----- ba chế độ (mục 13.1) -----
    def kiem_tep_tam(self, noi_dung: str, gioi_han_giay: int) -> KetQuaLean:
        """Biên dịch một tệp tạm trong sandbox; dự án chỉ đọc."""
        tep_hash = hashlib.sha256(noi_dung.encode("utf-8")).hexdigest()
        ten = f"sinhde-{uuid.uuid4().hex[:12]}"
        with tempfile.TemporaryDirectory(prefix="sinhde_vao_") as tmp:
            Path(tmp, "Tep.lean").write_text(noi_dung, encoding="utf-8")
            os.chmod(tmp, 0o755)
            lenh = self._lenh_docker(ten, ["-v", f"{tmp}:/vao:ro"],
                                     ["kiem_tep_tam", "/vao/Tep.lean", str(gioi_han_giay)])
            return self._chay("kiem_tep_tam", "Tep.lean", tep_hash, lenh, ten, gioi_han_giay)

    def build_module(self, ten_module: str, gioi_han_giay: int) -> KetQuaLean:
        """`lake build <module>`; chỉ `.lake/build` được ghi."""
        ten = f"sinhde-{uuid.uuid4().hex[:12]}"
        lenh = self._lenh_docker(ten, [], ["build_module", ten_module, str(gioi_han_giay)],
                                 ghi_build=True)
        return self._chay("build_module", ten_module, "", lenh, ten, gioi_han_giay)

    def kiem_khop(self, yeu_cau: dict, gioi_han_giay: int) -> KetQuaLean:
        """Gọi tiện ích kiem_khop (mục 12.7). Cài đặt ở M4."""
        raise NotImplementedError("kiem_khop được cài đặt ở mốc M4")
