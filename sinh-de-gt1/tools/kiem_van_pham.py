"""Kiểm văn phạm không có xung đột LALR và không có va chạm token (mục 6.7, 8.5).

Dùng chế độ `strict=True` của Lark (cần gói `interegular`). M3 sẽ thêm văn phạm đọc
`latex_con.lark` vào danh sách.

Chạy: .venv/bin/python tools/kiem_van_pham.py
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from sinhde.nen_tang.van_pham import TEP_VAN_PHAM, tao_parser  # noqa: E402

CAC_VAN_PHAM = [("N1", TEP_VAN_PHAM, tao_parser)]


def main() -> int:
    loi = 0
    for ten, tep, tao in CAC_VAN_PHAM:
        try:
            tao(strict=True)
            print(f"{ten} ({tep.name}): đạt — LALR không xung đột, token không va chạm")
        except Exception as e:  # Lark báo GrammarError hoặc lỗi va chạm token
            loi += 1
            print(f"{ten} ({tep.name}): KHÔNG ĐẠT — {e}")
    return 1 if loi else 0


if __name__ == "__main__":
    raise SystemExit(main())
