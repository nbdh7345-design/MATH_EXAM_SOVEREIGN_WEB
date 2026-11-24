# sinh-de-gt1

Hệ thống sinh đề bài Giải tích 1 có chứng nhận Lean. Thiết kế: `docs/thiet-ke-pipeline-sinh-de-v1.2.md`.

Trạng thái: **M0 xong** (khung repo, Lean + Mathlib cố định, sandbox Docker, CSDL). Xem `docs/ket_qua_M0.md`.

## Cài đặt (WSL2 Ubuntu)
```bash
uv venv --python 3.12 .venv && uv pip install -e ".[dev]"
```
```bash
cd lean && lake exe cache get && lake build && cd ..
```
```bash
docker build -t sinhde-lean sandbox/
```

## Kiểm thử
```bash
.venv/bin/pytest -q
```
```bash
.venv/bin/pytest -q -m sandbox
```
```bash
.venv/bin/sinhde nen-tang kiem
```
