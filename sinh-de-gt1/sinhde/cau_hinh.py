"""Nạp và kiểm tra `config.yaml` (mục 5.4)."""

from __future__ import annotations

from pathlib import Path
from typing import Literal

import yaml
from pydantic import BaseModel, ConfigDict, Field

THU_MUC_GOC = Path(__file__).resolve().parent.parent


class _Mo(BaseModel):
    model_config = ConfigDict(extra="forbid")


class CauHinhLLM(_Mo):
    nha_cung_cap: str
    mo_hinh: str
    nhiet_do_de_xuat: float = Field(ge=0, le=1)
    nhiet_do_chung_minh: float = Field(ge=0, le=1)
    so_ung_vien_moi_lan: int = Field(ge=1)
    token_toi_da: int = Field(ge=1)
    ngan_sach_moi_dot_usd: float = Field(ge=0)


class CauHinhGiaiDoan1(_Mo):
    so_vong_sua_khuon: int = Field(ge=0)
    so_vong_sua_chung_minh: int = Field(ge=0)
    thoi_gian_lean_khuon_giay: int = Field(ge=1)
    mien_toi_da_tach_gia_tri: int = Field(ge=1)
    so_lan_lhospital_toi_da: int = Field(ge=0)


class CauHinhGiaiDoan2(_Mo):
    thoi_gian_lean_cau_giay: int = Field(ge=1)


class CauHinhKhuon(_Mo):
    mien_toi_thieu: int = Field(ge=1)
    do_sau_toi_da: int = Field(ge=1)
    so_nut_toi_da: int = Field(ge=1)
    kich_thuoc_mien_toi_da: int = Field(ge=1)


class CauHinhLean(_Mo):
    so_tien_trinh: int = Field(ge=1)
    bo_nho_gb: int = Field(ge=1)
    anh_docker: str


class CauHinhKiemMau(_Mo):
    so_cau_dau_moi_khuon: int = Field(ge=0)
    ti_le_ngau_nhien: float = Field(gt=0, le=1)


class CauHinhDuongDan(_Mo):
    csdl: str
    lean: str


class CauHinh(_Mo):
    che_do: Literal["phat_trien", "chinh_thuc"]
    llm: CauHinhLLM
    giai_doan_1: CauHinhGiaiDoan1
    giai_doan_2: CauHinhGiaiDoan2
    khuon: CauHinhKhuon
    lean: CauHinhLean
    kiem_mau: CauHinhKiemMau
    duong_dan: CauHinhDuongDan

    def duong_dan_tuyet_doi(self, tuong_doi: str) -> Path:
        return (THU_MUC_GOC / tuong_doi).resolve()


def nap_cau_hinh(duong_dan: Path | None = None) -> CauHinh:
    """Đọc `config.yaml`; báo lỗi rõ ràng nếu thiếu khóa hoặc sai kiểu."""
    tep = duong_dan or THU_MUC_GOC / "config.yaml"
    with open(tep, encoding="utf-8") as f:
        du_lieu = yaml.safe_load(f)
    return CauHinh.model_validate(du_lieu)
