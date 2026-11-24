# Kết quả mốc M0 và ba thử nghiệm rủi ro

Ngày: 2026-11-24 · Máy: Windows 11 Home, WSL2 Ubuntu 24.04 (10 GB RAM cho WSL), Docker Engine 29.1.3.

## Phiên bản đã cố định
- Lean `leanprover/lean4:v4.36.0` (`lean/lean-toolchain`).
- Mathlib tag `v4.36.0`, commit `fc4f59e577feb1a4956671bc04ac18aaaf8cd842` (`lean/lake-manifest.json`).
- Cache Mathlib tải bằng `lake exe cache get` (9117 tệp; `.lake/packages` khoảng 7,3 GB).
- Môi trường Python dựng bằng `uv` (Ubuntu thiếu gói `python3.12-venv`, cài gói này cần sudo).

## Nghiệm thu M0 (mục 17)
| Tiêu chí | Kết quả |
|---|---|
| `lake build` dự án rỗng chạy được trong sandbox | Đạt: `LeanRunner.build_module("ThuVienGT")`, khoảng 15 giây khi nóng |
| `pytest` chạy được | Đạt: 4 kiểm thử thường, 8 kiểm thử `-m sandbox` |
| Tệp Lean có lệnh truy cập mạng bị chặn | Đạt: `curl` trong `#eval` trả mã lỗi khác 0 (`--network none`) |
| Thêm: ghi vào thư mục dự án bị chặn, quá giờ bị dừng, mọi lần chạy ghi vào `lan_chay_lean` | Đạt |

## Thử nghiệm 1: thời gian và bộ nhớ của Lean trong container
Tệp `import ThuVienGT` (kéo theo toàn bộ Mathlib) và một `norm_num` nhỏ:

| Lần chạy | Thời gian | `memory.peak` của container |
|---|---|---|
| Lạnh (ngay sau khi WSL khởi động) | 108 s | 6144 MB (chạm trần) |
| Nóng lần 2 | 24 s | 2612 MB |
| Nóng lần 3 | 5 s | 492 MB |

Nhận xét:
- `memory.peak` tính cả cache đọc tệp `.olean`, nên lần lạnh chạm trần 6 GB nhưng không bị giết; kernel thu hồi cache, làm chậm.
- WSL tự tắt máy ảo khi rảnh (mặc định khoảng 1 phút), nên cache bị mất giữa các lệnh cách nhau lâu. Đề xuất: đặt `vmIdleTimeout` lớn trong `%UserProfile%\.wslconfig` khi chạy các đợt sinh, và chạy một lần "làm nóng" trước mỗi đợt.
- Khi `ThuVienGT` chuyển sang import cụ thể (cuối M2), thời gian nạp sẽ giảm.
- Giữ `so_tien_trinh: 1`, `bo_nho_gb: 6`. Giới hạn thời gian của lần chạy đầu trong mỗi đợt nên để ít nhất 300 s.

## Thử nghiệm 2: `decide` trên `chuanHoa` với ℚ (mục 7.9, 12.6)
Tệp: `thu_nghiem/decide/`. Cây khuôn độ sâu 8, khoảng 40 nút, có phân số, lũy thừa âm, hàm.

| Chiến thuật | Kết quả |
|---|---|
| `decide` | **Không đạt**: elaborator không rút gọn được các phép toán trên ℚ |
| `decide +kernel` | **Đạt**, khoảng 5 s tính cả nạp Mathlib (phần `decide` dưới 1 s) |
| `rfl` | Không đạt |

Kết luận: `thoa_R`, `khop_cay`, `khop_diem` (mục 12.6) dùng `decide +kernel`. Không dùng `native_decide`.

## Thử nghiệm 3: bản thô của `kiem_khop` (mục 12.7)
Tệp: `thu_nghiem/kiem_khop/Main.lean`, chạy bằng `lean --run` trong sandbox trên module mẫu `lean/ChungNhan/ThuNghiem.lean`.

| Định lý | `theorem` | Khớp kiểu (kernel) | Axiom | Đúng mong đợi |
|---|---|---|---|---|
| `dung : 2 + 2 = 4` | có | có | không có | có |
| `gia : True` | có | **không** | không có | có |
| `dungAxiomTuKhai` | có | có | `tuKhai` (axiom tự khai báo) → **không chuẩn** | có |
| `tuKhai` (là axiom) | **không** | không | — | có |
| `khongCo` | không tồn tại | — | — | có |

API đã chốt cho Lean 4.36.0:
- `importModules #[{ module := m }] {} (loadExts := false)`; không gọi `enableInitializersExecution`.
- `Kernel.isDefEq env {} a b : Except Kernel.Exception Bool`.
- `collectAxioms : Name → m (Array Name)` (cần `MonadEnv`), chạy qua `CoreM.toIO`.
- `Lean.levelOne` đã lỗi thời, dùng `Level.one`.
- Kiểu mong đợi dựng bằng `mkApp`/`mkConst`/`mkRawNatLit`, so với kiểu đã elaborate bằng kernel: khớp.

Việc còn lại cho M4: dựng kiểu `DeDungGioiHan00 …` từ S-biểu thức, đọc yêu cầu JSON, ghi kết quả JSON ra tệp, build thành `lean_exe kiem_khop`.

## Ghi chú cho các mốc sau
- Lean 4.36 cảnh báo `imports Mathlib … designed for use with the module system; consider adding module`. Xem xét dùng hệ thống module ở M2.
