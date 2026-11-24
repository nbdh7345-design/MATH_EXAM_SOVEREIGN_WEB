"""Thử nghiệm rủi ro 3 (đối chứng): so cổng kiểm bằng tệp văn bản (bản 1.1) với kiem_khop (bản 1.2).

Module `KiemThu.TanCong` khai báo macro_rules đọc "(2 : Nat) + 2 = 4" thành `True`.
Cần build trước: KiemThu.TanCong và kiem_khop (xem tests/test_kiem_khop.py).
Chạy: .venv/bin/python thu_nghiem/tan_cong/chay.py
"""

import json

from sinhde.cau_hinh import nap_cau_hinh
from sinhde.lean.chay_lean import LeanRunner

TEP_KIEM_KHOP_VAN_BAN = """import KiemThu.TanCong
-- Cổng kiểm kiểu bản 1.1: elaborate mệnh đề dạng văn bản sau khi đã import module cần kiểm.
example : (2 : Nat) + 2 = 4 := KiemThu.TanCong.tanCong
#print axioms KiemThu.TanCong.tanCong
"""


def main() -> None:
    r = LeanRunner(nap_cau_hinh())
    van_ban = r.kiem_tep_tam(TEP_KIEM_KHOP_VAN_BAN, gioi_han_giay=120)
    print("Bản 1.1 (tệp văn bản): biên dịch", "ĐẠT → bị lừa" if van_ban.dat else "không đạt")
    print("  thông báo:", " ".join(van_ban.thong_bao.split()))
    expr = r.kiem_khop({"module": "KiemThu.TanCong", "dinh_ly": "KiemThu.TanCong.tanCong",
                        "kieu": "(a (c Eq 1) (c Nat) (a (c Nat.add) (n 2) (n 2)) (n 4))"}, 120)
    print("Bản 1.2 (kiem_khop, mức Expr):", "đạt → bị lừa" if expr.dat else "KHÔNG ĐẠT → chặn đúng")
    print("  kết quả:", json.dumps(json.loads(expr.thong_bao), ensure_ascii=False))


if __name__ == "__main__":
    main()
