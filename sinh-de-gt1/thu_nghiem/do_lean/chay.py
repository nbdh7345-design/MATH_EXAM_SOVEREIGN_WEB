"""Thử nghiệm rủi ro 1 (bản sửa): thời gian và bộ nhớ của Lean trong container.

Bộ import mẫu là phần Mathlib mà ThuVienGT cần (lean/ThuVienGT.lean), không phải `import Mathlib`.

  .venv/bin/python thu_nghiem/do_lean/chay.py kich_thuoc  # kích thước bao đóng import
  .venv/bin/python thu_nghiem/do_lean/chay.py do          # chạy ngay sau khi khởi động lại Ubuntu

Ở chế độ `do`, lần 1 là lần chạy lạnh, cũng chính là bước làm nóng (`LeanRunner.lam_nong`);
các lần sau cho thời gian của một lần chạy bình thường trong đợt sinh.
"""

import subprocess
import sys
import tempfile
import time
from pathlib import Path

from sinhde.cau_hinh import nap_cau_hinh
from sinhde.lean.bao_dong_import import doc_import, kich_thuoc_olean
from sinhde.lean.chay_lean import LeanRunner


def chay_mot_lan(r: LeanRunner, vao: Path) -> tuple[float, int, int]:
    bo_nho = f"{r.ch.lean.bo_nho_gb}g"
    lenh = [
        "docker", "run", "--rm", "--network", "none",
        "--memory", bo_nho, "--memory-swap", bo_nho, "--pids-limit", "256", "--cpus", "2",
        "--user", "1000:1000", "--read-only", "--tmpfs", "/tmp:rw,size=512m",
        "-v", f"{r.thu_muc_lean}:/du_an:ro", "-v", f"{vao}:/vao:ro",
        "--entrypoint", "sh", r.ch.lean.anh_docker, "-c",
        "/usr/local/bin/chay_lean.sh kiem_tep_tam /vao/Tep.lean 900 >/dev/null 2>&1;"
        " echo $? $(cat /sys/fs/cgroup/memory.peak)",
    ]
    bd = time.monotonic()
    out = subprocess.run(lenh, capture_output=True, text=True).stdout.split()
    return time.monotonic() - bd, int(out[0]), int(out[1]) // 2**20


def main() -> None:
    che_do = sys.argv[1]
    r = LeanRunner(nap_cau_hinh())
    import_gt = doc_import((r.thu_muc_lean / "ThuVienGT.lean").read_text(encoding="utf-8"))
    if che_do == "kich_thuoc":
        for ten, goc in [("import Mathlib", ["Mathlib"]),
                         ("import của ThuVienGT", import_gt),
                         ("Mathlib.Algebra.Order.Field.Rat", ["Mathlib.Algebra.Order.Field.Rat"])]:
            so, so_byte = kich_thuoc_olean(goc, r.thu_muc_lean)
            print(f"{ten:34s}: {so:5d} module, {so_byte / 2**30:5.2f} GB tệp .olean*")
        return
    tep = "".join(f"import {m}\n" for m in import_gt) + "example : (2:ℝ) + 2 = 4 := by norm_num\n"
    with tempfile.TemporaryDirectory() as tmp:
        Path(tmp, "Tep.lean").write_text(tep, encoding="utf-8")
        for i in range(1, 4):
            giay, ma, peak = chay_mot_lan(r, Path(tmp))
            print(f"lần {i}: {giay:.1f} s, mã thoát {ma}, memory.peak {peak} MB", flush=True)


if __name__ == "__main__":
    main()
