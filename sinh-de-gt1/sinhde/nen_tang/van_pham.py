"""Bộ đọc N1 (mục 6.1, 6.2 của thiết kế v2.1): chuỗi → cây biểu thức, ràng buộc, tập, phương án.

Nội dung do LLM sinh chỉ được đọc qua các hàm này (nguyên tắc I1), không bao giờ `eval`.
Ngoài văn phạm, bộ đọc kiểm hai quy tắc chung cho mọi dạng bài:
- `E_LUYTHUA_NGUYEN`: số mũ của `luythua` không được là số nguyên (khi đó phải dùng `^`);
- `E_BIEN_T`: biến `t` chỉ xuất hiện trong thân `tp(…)`, không ở cận và không ở ngoài.
Vai trò của các biến x, y, n theo từng dạng bài do A2 kiểm (mục 6.2).
"""

from __future__ import annotations

from fractions import Fraction
from functools import lru_cache
from pathlib import Path
from typing import Any

from lark import Lark, Token, Transformer, v_args
from lark.exceptions import UnexpectedCharacters, UnexpectedEOF, UnexpectedInput, UnexpectedToken

from sinhde.nen_tang import cay as C

TEP_VAN_PHAM = Path(__file__).with_name("van_pham.lark")
DIEM_BAT_DAU = ["bieu_thuc", "dieu_kien", "tap", "diem2", "dac_biet"]


class LoiVanPham(ValueError):
    """Lỗi đọc chuỗi, kèm mã lỗi (mặc định E_VAN_PHAM, mục 11.2) và dòng, cột nếu biết."""

    def __init__(self, thong_bao: str, dong: int | None = None, cot: int | None = None,
                 ma: str = "E_VAN_PHAM"):
        self.thong_bao, self.dong, self.cot, self.ma = thong_bao, dong, cot, ma
        vi_tri = f" (dòng {dong}, cột {cot})" if dong is not None else ""
        super().__init__(f"[{ma}] {thong_bao}{vi_tri}")


def tao_parser(strict: bool = True) -> Lark:
    """Bộ phân tích LALR; `strict=True` báo lỗi nếu văn phạm có xung đột hay va chạm token."""
    return Lark(TEP_VAN_PHAM.read_text(encoding="utf-8"), start=DIEM_BAT_DAU,
                parser="lalr", strict=strict)


@lru_cache(maxsize=1)
def _parser() -> Lark:
    return tao_parser()


@v_args(inline=True)
class _SangCay(Transformer):
    # ----- biểu thức -----
    def so(self, tok: Token) -> C.Nut:
        return C.So(Fraction(int(tok)))

    def bien(self, tok: Token) -> C.Nut:
        return C.Bien(str(tok))

    def tham_so(self, tok: Token) -> C.Nut:
        return C.ThamSo(str(tok))

    def an(self) -> C.Nut:
        return C.An()

    def pi(self) -> C.Nut:
        return C.Pi()

    def hang_e(self) -> C.Nut:
        return C.hang_e()

    def ham(self, ten: Token, a: C.Nut) -> C.Nut:
        return C.Ham(str(ten), a)

    def luythua(self, a: C.Nut, b: C.Nut) -> C.Nut:
        return C.LuyThua(a, b)

    def tich_phan_t(self, f: C.Nut, a: C.Nut, b: C.Nut) -> C.Nut:
        return C.TichPhanT(f, a, b)

    def am(self, a: C.Nut) -> C.Nut:
        return C.Am(a)

    def cong(self, a: C.Nut, b: C.Nut) -> C.Nut:
        return C.Cong(a, b)

    def tru(self, a: C.Nut, b: C.Nut) -> C.Nut:
        return C.Tru(a, b)

    def nhan(self, a: C.Nut, b: C.Nut) -> C.Nut:
        return C.Nhan(a, b)

    def chia(self, a: C.Nut, b: C.Nut) -> C.Nut:
        return C.Chia(a, b)

    def so_mu_duong(self, tok: Token) -> int:
        return int(tok)

    def so_mu_am(self, tok: Token) -> int:
        return -int(tok)

    def mu(self, a: C.Nut, n: int) -> C.Nut:
        return C.Mu(a, n)

    # ----- ràng buộc -----
    def so_sanh(self, trai: C.Nut, op: Token, phai: C.Nut) -> C.SoSanh:
        return C.SoSanh(str(op), trai, phai)

    def va(self, a, b) -> C.Va:
        return C.Va(a, b)

    def hoac(self, a, b) -> C.Hoac:
        return C.Hoac(a, b)

    # ----- tập, khoảng, điểm, phương án đặc biệt -----
    def tap_rong(self) -> C.TapRong:
        return C.TapRong()

    def tap_huu_han(self, *phan_tu: C.Nut) -> C.TapHuuHan:
        return C.TapHuuHan(tuple(phan_tu))

    def hop_khoang(self, *cac_khoang: C.Khoang) -> C.HopKhoang:
        return C.HopKhoang(tuple(cac_khoang))

    def khoang(self, kieu: Token, trai: C.DauMut, phai: C.DauMut) -> C.Khoang:
        return C.Khoang(str(kieu), trai, phai)

    def duong_vc(self) -> C.VoCung:
        return C.VoCung(True)

    def am_vc(self) -> C.VoCung:
        return C.VoCung(False)

    def diem2(self, x: C.Nut, y: C.Nut) -> C.Diem2:
        return C.Diem2(x, y)

    def khong_ton_tai(self) -> C.DacBiet:
        return C.DacBiet("khong_ton_tai")

    def duong_vc_pa(self) -> C.DacBiet:
        return C.DacBiet("duong_vc")

    def am_vc_pa(self) -> C.DacBiet:
        return C.DacBiet("am_vc")


# ----- Các quy tắc chung ngoài văn phạm -----
def _kiem_bieu_thuc(t: C.Nut) -> None:
    from sinhde.nen_tang.chuan_hoa import chuan_hoa  # tránh import vòng

    for nut in _cac_nut(t):
        if isinstance(nut, C.LuyThua):
            so_mu = chuan_hoa(nut.b)
            if isinstance(so_mu, C.So) and so_mu.q.denominator == 1:
                raise LoiVanPham("luythua có số mũ nguyên; hãy dùng ^ (mục 6.2)",
                                 ma="E_LUYTHUA_NGUYEN")
        if isinstance(nut, C.TichPhanT) and ("t" in C.bien_tu_do(nut.a) or "t" in C.bien_tu_do(nut.b)):
            raise LoiVanPham("Cận của tp(…) không được chứa biến t (mục 6.2)", ma="E_BIEN_T")
    if "t" in C.bien_tu_do(t):
        raise LoiVanPham("Biến t chỉ được dùng trong thân tp(…) (mục 6.2)", ma="E_BIEN_T")


def _cac_nut(t: C.Nut):
    yield t
    for c in C.con(t):
        yield from _cac_nut(c)


def _bieu_thuc_trong(gia_tri: Any):
    """Các biểu thức nằm trong một kết quả đọc (biểu thức, ràng buộc, tập, điểm…)."""
    if isinstance(gia_tri, C.Nut):
        yield gia_tri
    elif isinstance(gia_tri, C.SoSanh):
        yield gia_tri.trai
        yield gia_tri.phai
    elif isinstance(gia_tri, (C.Va, C.Hoac)):
        yield from _bieu_thuc_trong(gia_tri.a)
        yield from _bieu_thuc_trong(gia_tri.b)
    elif isinstance(gia_tri, C.TapHuuHan):
        yield from gia_tri.phan_tu
    elif isinstance(gia_tri, C.HopKhoang):
        for k in gia_tri.cac_khoang:
            yield from (d for d in (k.trai, k.phai) if isinstance(d, C.Nut))
    elif isinstance(gia_tri, C.Diem2):
        yield gia_tri.x
        yield gia_tri.y


def _doc(chuoi: str, diem_bat_dau: str):
    try:
        cay_lark = _parser().parse(chuoi, start=diem_bat_dau)
    except UnexpectedCharacters as e:
        raise LoiVanPham(f"Ký tự không hợp lệ {chuoi[e.pos_in_stream]!r}", e.line, e.column) from None
    except UnexpectedToken as e:
        tok = "hết chuỗi" if e.token.type == "$END" else repr(str(e.token))
        raise LoiVanPham(f"Không chờ đợi {tok}", e.line, e.column) from None
    except UnexpectedEOF:
        raise LoiVanPham("Chuỗi kết thúc giữa chừng") from None
    except UnexpectedInput as e:  # pragma: no cover - phòng xa
        raise LoiVanPham(str(e), getattr(e, "line", None), getattr(e, "column", None)) from None
    ket_qua = _SangCay().transform(cay_lark)
    for bt in _bieu_thuc_trong(ket_qua):
        _kiem_bieu_thuc(bt)
    return ket_qua


def doc_bieu_thuc(chuoi: str) -> C.Nut:
    return _doc(chuoi, "bieu_thuc")


def doc_dieu_kien(chuoi: str) -> C.DieuKien:
    return _doc(chuoi, "dieu_kien")


def doc_tap(chuoi: str) -> C.Tap:
    return _doc(chuoi, "tap")


def doc_diem2(chuoi: str) -> C.Diem2:
    return _doc(chuoi, "diem2")


def doc_dac_biet(chuoi: str) -> C.DacBiet:
    return _doc(chuoi, "dac_biet")


def doc_phuong_an(chuoi: str, kieu: str):
    """Đọc một phương án theo kiểu đáp án (mục 1.4, 11.1). Kiểm đúng kiểu là việc của A2."""
    if kieu == "T1":
        return doc_dac_biet(chuoi) if chuoi.strip() in C.LOAI_DAC_BIET else doc_bieu_thuc(chuoi)
    if kieu == "T2":
        return doc_tap(chuoi)
    if kieu == "T3":
        return doc_bieu_thuc(chuoi)
    raise ValueError(f"Kiểu đáp án không đọc bằng N1: {kieu} (T4 dùng mẫu khẳng định)")
