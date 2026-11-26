"""Cây biểu thức N1 (mục 6.3). So sánh bằng theo cấu trúc, chuyển sang JSON hai chiều."""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from typing import Any, Union

TEN_HAM = ("sin", "cos", "tan", "cot", "arcsin", "arccos", "arctan",
           "exp", "ln", "sqrt", "cbrt", "abs")
CHU_THAM_SO = "abcdfghkmnpqrstuvwyz"


class Nut:
    """Lớp cơ sở của mọi nút biểu thức."""


@dataclass(frozen=True)
class So(Nut):
    q: Fraction


@dataclass(frozen=True)
class Bien(Nut):
    pass


@dataclass(frozen=True)
class ThamSo(Nut):
    ten: str


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

HAI_NGOI = (Cong, Tru, Nhan, Chia, LuyThua)


# ----- Tiện ích -----
def con(t: Nut) -> tuple[Nut, ...]:
    """Các nút con trực tiếp."""
    if isinstance(t, HAI_NGOI):
        return (t.a, t.b)
    if isinstance(t, (Am, Mu, Ham)):
        return (t.a,)
    return ()


def chua_bien(t: Nut) -> bool:
    return isinstance(t, Bien) or any(chua_bien(c) for c in con(t))


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
    if isinstance(t, Am):
        return Am(thay_tham_so(t.a, gia_tri))
    if isinstance(t, Mu):
        return Mu(thay_tham_so(t.a, gia_tri), t.n)
    if isinstance(t, Ham):
        return Ham(t.ten, thay_tham_so(t.a, gia_tri))
    if isinstance(t, HAI_NGOI):
        return type(t)(thay_tham_so(t.a, gia_tri), thay_tham_so(t.b, gia_tri))
    return t


def thay_tham_so_dk(dk: DieuKien, gia_tri: dict[str, Fraction]) -> DieuKien:
    if isinstance(dk, SoSanh):
        return SoSanh(dk.op, thay_tham_so(dk.trai, gia_tri), thay_tham_so(dk.phai, gia_tri))
    return type(dk)(thay_tham_so_dk(dk.a, gia_tri), thay_tham_so_dk(dk.b, gia_tri))


# ----- S-biểu thức: phải trùng từng ký tự với BT.toSExpr của Lean (mục 6.3, 7.1) -----
def so_str(q: Fraction) -> str:
    return f"{q.numerator}/{q.denominator}"


_TEN_SEXPR = {Cong: "cong", Tru: "tru", Nhan: "nhan", Chia: "chia", LuyThua: "luythua"}


def to_sexpr(t: Nut) -> str:
    if isinstance(t, So):
        return f"(hang {so_str(t.q)})"
    if isinstance(t, Bien):
        return "x"
    if isinstance(t, Am):
        return f"(am {to_sexpr(t.a)})"
    if isinstance(t, Mu):
        return f"(mu {to_sexpr(t.a)} {t.n})"
    if isinstance(t, Ham):
        return f"(ham {t.ten} {to_sexpr(t.a)})"
    if isinstance(t, HAI_NGOI):
        return f"({_TEN_SEXPR[type(t)]} {to_sexpr(t.a)} {to_sexpr(t.b)})"
    raise ValueError(f"Nút không có trong BT của Lean: {t!r}")  # ThamSo


# ----- JSON hai chiều -----
_TEN_LOAI = {So: "So", Bien: "Bien", ThamSo: "ThamSo", Am: "Am", Cong: "Cong", Tru: "Tru",
             Nhan: "Nhan", Chia: "Chia", Mu: "Mu", LuyThua: "LuyThua", Ham: "Ham",
             SoSanh: "SoSanh", Va: "Va", Hoac: "Hoac"}
_LOAI_THEO_TEN = {v: k for k, v in _TEN_LOAI.items()}


def to_json(t: Any) -> Any:
    loai = _TEN_LOAI[type(t)]
    if isinstance(t, So):
        return {"loai": loai, "q": so_str(t.q)}
    if isinstance(t, Bien):
        return {"loai": loai}
    if isinstance(t, ThamSo):
        return {"loai": loai, "ten": t.ten}
    if isinstance(t, Am):
        return {"loai": loai, "a": to_json(t.a)}
    if isinstance(t, Mu):
        return {"loai": loai, "a": to_json(t.a), "n": t.n}
    if isinstance(t, Ham):
        return {"loai": loai, "ten": t.ten, "a": to_json(t.a)}
    if isinstance(t, SoSanh):
        return {"loai": loai, "op": t.op, "trai": to_json(t.trai), "phai": to_json(t.phai)}
    return {"loai": loai, "a": to_json(t.a), "b": to_json(t.b)}


def from_json(d: Any) -> Any:
    loai = _LOAI_THEO_TEN[d["loai"]]
    if loai is So:
        return So(Fraction(d["q"]))
    if loai is Bien:
        return Bien()
    if loai is ThamSo:
        return ThamSo(d["ten"])
    if loai is Am:
        return Am(from_json(d["a"]))
    if loai is Mu:
        return Mu(from_json(d["a"]), int(d["n"]))
    if loai is Ham:
        return Ham(d["ten"], from_json(d["a"]))
    if loai is SoSanh:
        return SoSanh(d["op"], from_json(d["trai"]), from_json(d["phai"]))
    return loai(from_json(d["a"]), from_json(d["b"]))
