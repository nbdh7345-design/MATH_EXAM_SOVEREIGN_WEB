"""Thử nghiệm rủi ro 2: đo decide / decide +kernel / rfl trên chuanHoa (mục 7.9).

Chạy: .venv/bin/python thu_nghiem/decide/chay.py
"""

from pathlib import Path

from sinhde.cau_hinh import nap_cau_hinh
from sinhde.lean.chay_lean import LeanRunner

MAU = Path(__file__).with_name("ChuanHoa.lean.tpl").read_text(encoding="utf-8")
CHIEN_THUAT = ["decide", "decide +kernel", "rfl"]


def main() -> None:
    r = LeanRunner(nap_cau_hinh())
    # Lần chạy làm nóng: chỉ nạp Mathlib và các định nghĩa, để thời gian đo không tính lần đọc đĩa đầu tiên.
    goc = r.kiem_tep_tam(MAU.replace("by CHIEN_THUAT", "by sorry"), gioi_han_giay=300)
    print(f"làm nóng (sorry): {goc.thoi_gian_ms} ms, dat={goc.dat}")
    for ct in CHIEN_THUAT:
        kq = r.kiem_tep_tam(MAU.replace("CHIEN_THUAT", ct), gioi_han_giay=120)
        loi = "" if kq.dat else " | " + " ".join(kq.thong_bao.split())[:300]
        print(f"{ct:16s}: dat={kq.dat}  {kq.thoi_gian_ms} ms (trừ nền ~{kq.thoi_gian_ms - goc.thoi_gian_ms} ms){loi}")


if __name__ == "__main__":
    main()
