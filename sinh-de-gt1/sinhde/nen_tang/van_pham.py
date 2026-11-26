"""Bộ đọc N1 (mục 6.1, 6.2): chuỗi → cây biểu thức, ràng buộc, điểm.

Nội dung do LLM sinh chỉ được đọc qua các hàm này (nguyên tắc I1), không bao giờ `eval`.
"""

from __future__ import annotations

from fractions import Fraction
from functools import lru_cache
from pathlib import Path

from lark import Lark, Token, Transformer, v_args
from lark.exceptions import UnexpectedCharacters, UnexpectedEOF, UnexpectedInput, UnexpectedToken

from sinhde.nen_tang import cay as C

TEP_VAN_PHAM = Path(__file__).with_name("van_pham.lark")
DIEM_BAT_DAU = ["bieu_thuc", "dieu_kien", "diem"]


class LoiVanPham(ValueError):
    """Lỗi đọc chuỗi (mã E_VAN_PHAM, mục 11.2), kèm dòng và cột nếu biết."""

    def __init__(self, thong_bao: str, dong: int | None = None, cot: int | None = None):
        self.thong_bao, self.dong, self.cot = thong_bao, dong, cot
        vi_tri = f" (dòng {dong}, cột {cot})" if dong is not None else ""
        super().__init__(f"{thong_bao}{vi_tri}")


def tao_parser(strict: bool = True) -> Lark:
    """Bộ phân tích LALR; `strict=True` báo lỗi nếu văn phạm có xung đột hay va chạm token."""
    return Lark(TEP_VAN_PHAM.read_text(encoding="utf-8"), start=DIEM_BAT_DAU,
                parser="lalr", strict=strict)


@lru_cache(maxsize=1)
def _parser() -> Lark:
    return tao_parser()


@v_args(inline=True)
class _SangCay(Transformer):
    def so(self, tok: Token) -> C.Nut:
        return C.So(Fraction(int(tok)))

    def bien(self) -> C.Nut:
        return C.Bien()

    def tham_so(self, tok: Token) -> C.Nut:
        return C.ThamSo(str(tok))

    def ham(self, ten: Token, a: C.Nut) -> C.Nut:
        return C.Ham(str(ten), a)

    def luythua(self, a: C.Nut, b: C.Nut) -> C.Nut:
        return C.LuyThua(a, b)

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

    def so_sanh(self, trai: C.Nut, op: Token, phai: C.Nut) -> C.SoSanh:
        return C.SoSanh(str(op), trai, phai)

    def va(self, a, b) -> C.Va:
        return C.Va(a, b)

    def hoac(self, a, b) -> C.Hoac:
        return C.Hoac(a, b)

    def diem(self, a: C.Nut) -> C.Nut:
        return a


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
    return _SangCay().transform(cay_lark)


def doc_bieu_thuc(chuoi: str) -> C.Nut:
    return _doc(chuoi, "bieu_thuc")


def doc_dieu_kien(chuoi: str) -> C.DieuKien:
    return _doc(chuoi, "dieu_kien")


def doc_diem(chuoi: str) -> C.Nut:
    return _doc(chuoi, "diem")
