"""Cây biểu thức và phương án N1 (mục 6.3 của thiết kế v2.1).

So sánh bằng theo cấu trúc, chuyển sang JSON hai chiều. `to_sexpr` phải trùng từng ký tự
với `toSExpr` của Lean (mục 7.1).
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from typing import Any, Union

TEN_HAM = ("sin", "cos", "tan", "cot", "arcsin", "arccos", "arctan",
           "exp", "ln", "sqrt", "cbrt", "abs")
TEN_BIEN = ("x", "y", "t", "n")
CHU_THAM_SO = "abcdfghkpqrsuvwz"
KIEU_KHOANG = ("kmo", "kdong", "ktrai", "kphai")      # (a;b) [a;b] [a;b) (a;b]
LOAI_DAC_BIET = ("khong_ton_tai", "duong_vc", "am_vc")


class Nut:
    """Lớp cơ sở của mọi nút biểu thức."""


@dataclass(frozen=True)
class So(Nut):
    q: Fraction


@dataclass(frozen=True)
class Bien(Nut):
    ten: str  # "x" | "y" | "t" | "n"


@dataclass(frozen=True)
class ThamSo(Nut):
    ten: str


@dataclass(frozen=True)
class An(Nut):
    """Ẩn m của dạng "tìm m"."""


@dataclass(frozen=True)
class Pi(Nut):
    pass


@dataclass(frozen=True)
class Am(Nut):
    a: Nut


@dataclass(frozen=True)
class Cong(Nut):
    a: Nut
    b: Nut


@dataclass(frozen=True)
class Tru(Nut):
    a: Nut
    b: Nut


@dataclass(frozen=True)
class Nhan(Nut):
    a: Nut
    b: Nut


@dataclass(frozen=True)
class Chia(Nut):
    a: Nut
    b: Nut


@dataclass(frozen=True)
class Mu(Nut):
    a: Nut
    n: int  # số mũ nguyên


@dataclass(frozen=True)
class LuyThua(Nut):
    a: Nut
    b: Nut  # số mũ thực


@dataclass(frozen=True)
class Ham(Nut):
    ten: str
    a: Nut


@dataclass(frozen=True)
class TichPhanT(Nut):
    """∫_a^b f(t) dt; f dùng biến t, a và b không chứa t."""
    f: Nut
    a: Nut
    b: Nut


def hang_e() -> Nut:
    """Số e, biểu diễn là exp(1) (mục 6.2)."""
    return Ham("exp", So(Fraction(1)))


# ----- Ràng buộc -----
@dataclass(frozen=True)
class SoSanh:
    op: str
    trai: Nut
    phai: Nut


@dataclass(frozen=True)
class Va:
    a: "DieuKien"
    b: "DieuKien"


@dataclass(frozen=True)
class Hoac:
    a: "DieuKien"
    b: "DieuKien"


DieuKien = Union[SoSanh, Va, Hoac]


# ----- Phương án -----
@dataclass(frozen=True)
class DacBiet:
    loai: str  # "khong_ton_tai" | "duong_vc" | "am_vc"


@dataclass(frozen=True)
class VoCung:
    """Đầu mút vô cùng của khoảng."""
    duong: bool


DauMut = Union[Nut, VoCung]


@dataclass(frozen=True)
class Khoang:
    kieu: str  # một trong KIEU_KHOANG
    trai: DauMut
    phai: DauMut


@dataclass(frozen=True)
class TapHuuHan:
    phan_tu: tuple[Nut, ...]


@dataclass(frozen=True)
class HopKhoang:
    cac_khoang: tuple[Khoang, ...]


@dataclass(frozen=True)
class TapRong:
    pass


Tap = Union[TapRong, TapHuuHan, HopKhoang]


@dataclass(frozen=True)
class Diem2:
    x: Nut
    y: Nut


@dataclass(frozen=True)
class KhangDinh:
    """Khẳng định điền từ mẫu khẳng định của N3 (kiểu T4)."""
    ma_mau: str
    cho_trong: tuple[Nut, ...]


HAI_NGOI = (Cong, Tru, Nhan, Chia, LuyThua)
LA = (So, Bien, ThamSo, An, Pi)


# ----- Duyệt cây -----
def con(t: Nut) -> tuple[Nut, ...]:
    """Các nút con trực tiếp."""
    if isinstance(t, HAI_NGOI):
        return (t.a, t.b)
    if isinstance(t, (Am, Mu, Ham)):
        return (t.a,)
    if isinstance(t, TichPhanT):
        return (t.f, t.a, t.b)
    return ()


def _dung_lai(t: Nut, cac_con: list[Nut]) -> Nut:
    """Dựng lại nút cùng loại với các con mới."""
    if isinstance(t, HAI_NGOI):
        return type(t)(cac_con[0], cac_con[1])
    if isinstance(t, Am):
        return Am(cac_con[0])
    if isinstance(t, Mu):
        return Mu(cac_con[0], t.n)
    if isinstance(t, Ham):
        return Ham(t.ten, cac_con[0])
    if isinstance(t, TichPhanT):
        return TichPhanT(*cac_con)
    return t


def bien_dung(t: Nut) -> set[str]:
    """Mọi biến xuất hiện trong cây, kể cả biến t bị buộc trong tích phân."""
    ket_qua = {t.ten} if isinstance(t, Bien) else set()
    for c in con(t):
        ket_qua |= bien_dung(c)
    return ket_qua


def bien_tu_do(t: Nut) -> set[str]:
    """Các biến tự do: biến t trong thân tích phân `tp(f, a, b)` bị buộc."""
    if isinstance(t, Bien):
        return {t.ten}
    if isinstance(t, TichPhanT):
        return (bien_tu_do(t.f) - {"t"}) | bien_tu_do(t.a) | bien_tu_do(t.b)
    ket_qua: set[str] = set()
    for c in con(t):
        ket_qua |= bien_tu_do(c)
    return ket_qua


def chua_an(t: Nut) -> bool:
    return isinstance(t, An) or any(chua_an(c) for c in con(t))


def chua_bien(t: Nut, ten: str = "x") -> bool:
    return ten in bien_tu_do(t)


def chi_chua_tham_so(t: Nut) -> bool:
    """Không có biến tự do nào và không có ẩn m: một biểu thức hằng theo tham số."""
    return not bien_tu_do(t) and not chua_an(t)


def tham_so_dung(t: Nut) -> set[str]:
    if isinstance(t, ThamSo):
        return {t.ten}
    ket_qua: set[str] = set()
    for c in con(t):
        ket_qua |= tham_so_dung(c)
    return ket_qua


def tham_so_dung_dk(dk: DieuKien) -> set[str]:
    if isinstance(dk, SoSanh):
        return tham_so_dung(dk.trai) | tham_so_dung(dk.phai)
    return tham_so_dung_dk(dk.a) | tham_so_dung_dk(dk.b)


def do_sau(t: Nut) -> int:
    return 1 + max((do_sau(c) for c in con(t)), default=0)


def so_nut(t: Nut) -> int:
    return 1 + sum(so_nut(c) for c in con(t))


def thay_tham_so(t: Nut, gia_tri: dict[str, Fraction]) -> Nut:
    """Thay mọi `ThamSo` có trong `gia_tri` bằng `So`. Không chuẩn hóa."""
    if isinstance(t, ThamSo):
        return So(Fraction(gia_tri[t.ten])) if t.ten in gia_tri else t
    return _dung_lai(t, [thay_tham_so(c, gia_tri) for c in con(t)])


def thay_tham_so_dk(dk: DieuKien, gia_tri: dict[str, Fraction]) -> DieuKien:
    if isinstance(dk, SoSanh):
        return SoSanh(dk.op, thay_tham_so(dk.trai, gia_tri), thay_tham_so(dk.phai, gia_tri))
    return type(dk)(thay_tham_so_dk(dk.a, gia_tri), thay_tham_so_dk(dk.b, gia_tri))


def bien_doi_pa(pa: Any, f) -> Any:
    """Áp dụng f lên mọi biểu thức con của một phương án (hoặc một biểu thức)."""
    if isinstance(pa, Nut):
        return f(pa)
    if isinstance(pa, (DacBiet, VoCung, TapRong)):
        return pa
    if isinstance(pa, Khoang):
        return Khoang(pa.kieu, bien_doi_pa(pa.trai, f), bien_doi_pa(pa.phai, f))
    if isinstance(pa, TapHuuHan):
        return TapHuuHan(tuple(f(e) for e in pa.phan_tu))
    if isinstance(pa, HopKhoang):
        return HopKhoang(tuple(bien_doi_pa(k, f) for k in pa.cac_khoang))
    if isinstance(pa, Diem2):
        return Diem2(f(pa.x), f(pa.y))
    if isinstance(pa, KhangDinh):
        return KhangDinh(pa.ma_mau, tuple(f(e) for e in pa.cho_trong))
    raise TypeError(f"Không phải phương án: {pa!r}")


def thay_tham_so_pa(pa: Any, gia_tri: dict[str, Fraction]) -> Any:
    return bien_doi_pa(pa, lambda e: thay_tham_so(e, gia_tri))


# ----- S-biểu thức: phải trùng từng ký tự với toSExpr của Lean (mục 6.3, 7.1) -----
def so_str(q: Fraction) -> str:
    return f"{q.numerator}/{q.denominator}"


_TEN_SEXPR = {Cong: "cong", Tru: "tru", Nhan: "nhan", Chia: "chia", LuyThua: "luythua"}


def to_sexpr(t: Any) -> str:
    if isinstance(t, So):
        return f"(hang {so_str(t.q)})"
    if isinstance(t, Pi):
        return "pi"
    if isinstance(t, Bien):
        return f"(bien {t.ten})"
    if isinstance(t, An):
        return "an"
    if isinstance(t, Am):
        return f"(am {to_sexpr(t.a)})"
    if isinstance(t, Mu):
        return f"(mu {to_sexpr(t.a)} {t.n})"
    if isinstance(t, Ham):
        return f"(ham {t.ten} {to_sexpr(t.a)})"
    if isinstance(t, HAI_NGOI):
        return f"({_TEN_SEXPR[type(t)]} {to_sexpr(t.a)} {to_sexpr(t.b)})"
    if isinstance(t, TichPhanT):
        return f"(tpt {to_sexpr(t.f)} {to_sexpr(t.a)} {to_sexpr(t.b)})"
    # ----- phương án -----
    if isinstance(t, DacBiet):
        return f"(dacbiet {t.loai})"
    if isinstance(t, VoCung):
        return "duongvc" if t.duong else "amvc"
    if isinstance(t, Khoang):
        def dau(d: DauMut) -> str:
            return to_sexpr(d) if isinstance(d, VoCung) else f"(so {to_sexpr(d)})"
        return f"(khoang {t.kieu} {dau(t.trai)} {dau(t.phai)})"
    if isinstance(t, TapRong):
        return "(tap rong)"
    if isinstance(t, TapHuuHan):
        return "(tap huuhan" + "".join(" " + to_sexpr(e) for e in t.phan_tu) + ")"
    if isinstance(t, HopKhoang):
        return "(tap hop" + "".join(" " + to_sexpr(k) for k in t.cac_khoang) + ")"
    if isinstance(t, Diem2):
        return f"(diem2 {to_sexpr(t.x)} {to_sexpr(t.y)})"
    if isinstance(t, KhangDinh):
        return f"(khangdinh {t.ma_mau}" + "".join(" " + to_sexpr(e) for e in t.cho_trong) + ")"
    raise ValueError(f"Nút không có trong BT của Lean: {t!r}")  # ThamSo


# ----- JSON hai chiều -----
_LOP = {c.__name__: c for c in (So, Bien, ThamSo, An, Pi, Am, Cong, Tru, Nhan, Chia, Mu, LuyThua,
                                Ham, TichPhanT, SoSanh, Va, Hoac, DacBiet, VoCung, Khoang,
                                TapHuuHan, HopKhoang, TapRong, Diem2, KhangDinh)}


def to_json(t: Any) -> Any:
    d: dict[str, Any] = {"loai": type(t).__name__}
    for ten, gia in vars(t).items():
        if isinstance(gia, Fraction):
            d[ten] = so_str(gia)
        elif isinstance(gia, tuple):
            d[ten] = [to_json(x) for x in gia]
        elif isinstance(gia, (str, int, bool)):
            d[ten] = gia
        else:
            d[ten] = to_json(gia)
    return d


def from_json(d: Any) -> Any:
    lop = _LOP[d["loai"]]
    doi_so: dict[str, Any] = {}
    for ten, gia in d.items():
        if ten == "loai":
            continue
        if lop is So and ten == "q":
            doi_so[ten] = Fraction(gia)
        elif isinstance(gia, list):
            doi_so[ten] = tuple(from_json(x) for x in gia)
        elif isinstance(gia, dict):
            doi_so[ten] = from_json(gia)
        else:
            doi_so[ten] = gia
    return lop(**doi_so)
