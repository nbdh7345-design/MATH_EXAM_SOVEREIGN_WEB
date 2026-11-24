"""Giao diện dòng lệnh `sinhde` (mục 15). Ở M0 mới có các lệnh kiểm môi trường."""

from __future__ import annotations

import typer

from sinhde.cau_hinh import nap_cau_hinh

app = typer.Typer(help="Sinh đề Giải tích 1 có chứng nhận Lean.", no_args_is_help=True)
nen_tang = typer.Typer(help="Quản lý nền tảng (mục 3.3).", no_args_is_help=True)
app.add_typer(nen_tang, name="nen-tang")


@app.command("cau-hinh")
def cau_hinh() -> None:
    """Kiểm `config.yaml` hợp lệ và in chế độ chạy."""
    ch = nap_cau_hinh()
    typer.echo(f"config.yaml hợp lệ. Chế độ: {ch.che_do}.")


@nen_tang.command("lam-nong")
def nen_tang_lam_nong() -> None:
    """Chạy một lần Lean nạp ThuVienGT trong sandbox để làm nóng cache; chạy đầu mỗi đợt sinh."""
    from sinhde.lean.chay_lean import LeanRunner

    kq = LeanRunner(nap_cau_hinh()).lam_nong()
    typer.echo(f"Làm nóng: {'đạt' if kq.dat else 'KHÔNG đạt'} ({kq.thoi_gian_ms / 1000:.1f} s).")
    if not kq.dat:
        typer.echo(kq.thong_bao)
        raise typer.Exit(1)


@nen_tang.command("kiem")
def nen_tang_kiem() -> None:
    """Kiểm môi trường: tạo CSDL và chạy một tệp Lean thử trong sandbox."""
    from sinhde.lean.chay_lean import LeanRunner
    from sinhde.luu_tru.kho import Kho

    ch = nap_cau_hinh()
    Kho(ch.duong_dan_tuyet_doi(ch.duong_dan.csdl)).tao_bang()
    typer.echo("CSDL: đã tạo bảng.")
    kq = LeanRunner(ch).kiem_tep_tam("example : 1 + 1 = 2 := rfl\n", gioi_han_giay=120)
    typer.echo(f"Lean trong sandbox: {'đạt' if kq.dat else 'KHÔNG đạt'} ({kq.thoi_gian_ms} ms).")
    if not kq.dat:
        typer.echo(kq.thong_bao)
        raise typer.Exit(1)


if __name__ == "__main__":
    app()
