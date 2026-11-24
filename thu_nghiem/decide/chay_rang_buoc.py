"""Thử nghiệm rủi ro 2 (phần thêm): `thoa_R` và `khop_diem` của mục 12.6, với decide thường và decide +kernel.

Chạy: .venv/bin/python thu_nghiem/decide/chay_rang_buoc.py
"""

import re

from sinhde.cau_hinh import nap_cau_hinh
from sinhde.lean.chay_lean import LeanRunner

VI_DU = [
    ("thoa_R, decide", "example : R 2 := by decide"),
    ("thoa_R, decide +kernel", "example : R 2 := by decide +kernel"),
    ("khop_diem, decide", "example : diemQ 2 = (2 : ℚ) := by decide"),
    ("khop_diem, decide +kernel", "example : diemQ 2 = (2 : ℚ) := by decide +kernel"),
]


def main() -> None:
    dau = (
        "import Mathlib.Algebra.Order.Field.Rat\n"
        "abbrev R (p1 : ℤ) : Prop := 1 ≤ p1 ∧ p1 ≤ 6 ∧ ((p1 : ℚ) ≠ 0)\n"
        "def diemQ (p1 : ℤ) : ℚ := (p1 : ℚ)\n"
    )
    so_dong_dau = dau.count("\n")
    noi_dung = dau + "\n".join(v for _, v in VI_DU) + "\n"
    kq = LeanRunner(nap_cau_hinh()).kiem_tep_tam(noi_dung, gioi_han_giay=600)
    dong_loi = {int(m[1]) for m in re.finditer(r"Tep\.lean:(\d+):\d+: error", kq.thong_bao)}
    for i, (ten, _) in enumerate(VI_DU, start=so_dong_dau + 1):
        print(f"{ten:28s}: {'KHÔNG ĐẠT' if i in dong_loi else 'đạt'}")


if __name__ == "__main__":
    main()
