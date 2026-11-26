# sinh-de-gt1

Hệ thống sinh câu trắc nghiệm Giải tích 1 có chứng nhận Lean. Thiết kế đang dùng: `../thiet-ke-v2.1.md` (bản cũ v1.2 ở `docs/`). Thư mục này nằm trong repo `MATH_EXAM_SOVEREIGN_WEB`; làm việc tại `~/MATH_EXAM_SOVEREIGN_WEB/sinh-de-gt1` trong Ubuntu.

Trạng thái: **M0, M1 (theo v2.1) xong**. Xem `docs/ket_qua_M0.md` và `../nhat-ky-cai-dat.md`.

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

## Trước mỗi đợt sinh
Đọc các tệp `.olean*` mà `ThuVienGT` cần vào cache (thử nghiệm 1, `docs/ket_qua_M0.md`):
```bash
.venv/bin/sinhde nen-tang lam-nong
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
