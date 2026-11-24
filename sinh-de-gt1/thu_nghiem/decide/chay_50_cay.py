"""Thử nghiệm rủi ro 2 (bản sửa): `decide +kernel` trên 50 cây ngẫu nhiên kích thước tối đa (mục 7.9).

Tiêu chí 7.9: mỗi cây xong trong 10 giây. Mỗi cây được đo riêng bằng dấu thời gian
`IO.monoMsNow` in ra trước và sau `example`, với `Elab.async false` để các lệnh chạy tuần tự.
Mệnh đề thử: chuanHoa e = chuanHoa (chuanHoa e) — vừa đo thời gian, vừa kiểm tính lũy đẳng.

Chạy: .venv/bin/python thu_nghiem/decide/chay_50_cay.py
"""

import random
import re
from pathlib import Path

from sinhde.cau_hinh import nap_cau_hinh
from sinhde.lean.chay_lean import LeanRunner

THU_MUC = Path(__file__).parent
HAM = ["sin", "cos", "tan", "cot", "arcsin", "arccos", "arctan",
       "exp", "ln", "sqrt", "cbrt", "abs"]
SO_CAY, NUT_TOI_DA, DO_SAU_TOI_DA, NUT_TOI_THIEU = 50, 40, 8, 30


def la(rng: random.Random) -> str:
    k = rng.random()
    if k < 0.35:
        return ".x"
    if k < 0.55:
        return "(.hang ((2 : ℤ) : ℚ))"          # tham số p1 = 2 sau khi thế (như `de 2`)
    if k < 0.8:
        return f"(.hang ({rng.randint(-9, 9)} : ℚ))"
    return f"(.hang (({rng.randint(-9, 9)} : ℚ) / {rng.randint(2, 7)}))"


def sinh(rng: random.Random, ngan_sach: int, do_sau: int) -> tuple[str, int, int]:
    """Trả về (literal Lean, số nút, độ sâu)."""
    if ngan_sach <= 1 or do_sau <= 1:
        return la(rng), 1, 1
    if ngan_sach == 2 or rng.random() < 0.25:
        con, n, d = sinh(rng, ngan_sach - 1, do_sau - 1)
        k = rng.random()
        if k < 0.3:
            return f"(.am {con})", n + 1, d + 1
        if k < 0.65:
            return f"(.mu {con} ({rng.choice([-2, -1, 0, 1, 2, 3])}))", n + 1, d + 1
        return f"(.ham .{rng.choice(HAM)} {con})", n + 1, d + 1
    trai = rng.randint(1, ngan_sach - 2)
    a, na, da = sinh(rng, trai, do_sau - 1)
    b, nb, db = sinh(rng, ngan_sach - 1 - na, do_sau - 1)
    op = rng.choice(["cong", "tru", "nhan", "chia"])
    return f"(.{op} {a} {b})", na + nb + 1, max(da, db) + 1


def sinh_cay(rng: random.Random) -> tuple[str, int, int]:
    while True:
        s, n, d = sinh(rng, NUT_TOI_DA, DO_SAU_TOI_DA)
        if NUT_TOI_THIEU <= n <= NUT_TOI_DA and d <= DO_SAU_TOI_DA:
            return s, n, d


def dinh_nghia() -> str:
    mau = (THU_MUC / "ChuanHoa.lean.tpl").read_text(encoding="utf-8")
    return mau.split("/-- Khuôn tham số p1")[0] + "end ThuNghiem\nopen ThuNghiem\n\n"


def moc(i: int) -> str:
    return f'#eval show IO Unit from do let t ← IO.monoMsNow; IO.println s!"MOC {i} {{t}}"\n'


def main() -> None:
    rng = random.Random(20261124)
    cay = [sinh_cay(rng) for _ in range(SO_CAY)]
    noi_dung = dinh_nghia() + "set_option Elab.async false\nset_option maxRecDepth 100000\n\n"
    dong_cua_cay: dict[int, int] = {}
    noi_dung += moc(0)
    for i, (s, _, _) in enumerate(cay, start=1):
        dong_cua_cay[noi_dung.count("\n") + 1] = i
        noi_dung += f"example : chuanHoa {s} = chuanHoa (chuanHoa {s}) := by decide +kernel\n"
        noi_dung += moc(i)
    (THU_MUC / "vao_50_cay.lean").write_text(noi_dung, encoding="utf-8")

    r = LeanRunner(nap_cau_hinh())
    kq = r.kiem_tep_tam(noi_dung, gioi_han_giay=1200)
    moc_tg = {int(m[1]): int(m[2]) for m in re.finditer(r"MOC (\d+) (\d+)", kq.thong_bao)}
    loi = {dong_cua_cay[int(m[1])] for m in re.finditer(r"Tep\.lean:(\d+):\d+: error", kq.thong_bao)
           if int(m[1]) in dong_cua_cay}
    tg = [moc_tg[i] - moc_tg[i - 1] for i in range(1, SO_CAY + 1) if i in moc_tg and i - 1 in moc_tg]
    print(f"Tổng: {kq.thoi_gian_ms / 1000:.1f} s (gồm nạp Mathlib), tệp {'đạt' if kq.dat else 'CÓ LỖI'}")
    print(f"Kích thước cây: {min(n for _, n, _ in cay)}–{max(n for _, n, _ in cay)} nút, "
          f"độ sâu {min(d for _, _, d in cay)}–{max(d for _, _, d in cay)}")
    if tg:
        print(f"Mỗi cây: trung bình {sum(tg) / len(tg):.0f} ms, lớn nhất {max(tg)} ms, "
              f"đo được {len(tg)}/{SO_CAY} cây; quá 10 s: {sum(t > 10000 for t in tg)}")
    print(f"Cây lỗi: {sorted(loi) if loi else 'không có'}")
    if loi or not kq.dat:
        print(" ".join(kq.thong_bao.split())[:1500])


if __name__ == "__main__":
    main()
