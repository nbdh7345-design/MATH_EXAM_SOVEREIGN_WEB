# Kết quả mốc M0 và ba thử nghiệm rủi ro

Ngày: 2026-11-24 · Máy: Windows 11 Home, 15,5 GB RAM, WSL2 Ubuntu 24.04, Docker Engine 29.1.3. WSL được cấp 10 GB lúc đầu, hạ xuống 8 GB khi sửa thử nghiệm 1 (xem bên dưới).

## Phiên bản đã cố định
- Lean `leanprover/lean4:v4.36.0` (`lean/lean-toolchain`).
- Mathlib tag `v4.36.0`, commit `fc4f59e577feb1a4956671bc04ac18aaaf8cd842` (`lean/lake-manifest.json`).
- Cache Mathlib tải bằng `lake exe cache get` (9117 tệp; `.lake/packages` khoảng 7,3 GB).
- Môi trường Python dựng bằng `uv` (Ubuntu thiếu gói `python3.12-venv`, cài gói này cần sudo).

## Nghiệm thu M0 (mục 17)
| Tiêu chí | Kết quả |
|---|---|
| `lake build` dự án rỗng chạy được trong sandbox | Đạt: `LeanRunner.build_module("ThuVienGT")`, khoảng 15 giây khi nóng |
| `pytest` chạy được | Đạt: 6 kiểm thử thường, 16 kiểm thử `-m sandbox` (gồm 8 kiểm thử `kiem_khop`) |
| Tệp Lean có lệnh truy cập mạng bị chặn | Đạt: `curl` trong `#eval` trả mã lỗi khác 0 (`--network none`) |
| Thêm: ghi vào thư mục dự án bị chặn, quá giờ bị dừng, mọi lần chạy ghi vào `lan_chay_lean` | Đạt |

## Thử nghiệm 1: thời gian và bộ nhớ của Lean trong container
Tệp thử: các import cộng một `norm_num` nhỏ, chạy trong sandbox (`thu_nghiem/do_lean/chay.py`).

**Lần đo đầu** (`import Mathlib`, WSL 10 GB): lạnh 108 s, nóng 24 s rồi 5 s; lần lạnh chạm trần 6 GB của container.

**Vì sao chậm** (tìm ra khi sửa):
- Lean 4.36 dùng hệ thống module: mỗi module có `.olean` (1,76 GB cho cả Mathlib), `.olean.private` (3,66 GB) và `.olean.server` (0,10 GB). `ThuVienGT` chưa khai báo `module`, nên nạp cả phần private: tổng 5,51 GB.
- Cache đọc tệp tính vào giới hạn bộ nhớ của container (6 GB), nên lần lạnh phải đọc rồi thu hồi cache liên tục.
- Trên máy 15,5 GB RAM, cache của WSL ăn vào bộ nhớ commit của Windows. Lúc đo, Windows chạm giới hạn commit và **tắt máy ảo WSL giữa chừng** (ba lần trong năm phút).

**Đo lại sau khi khởi động lại Windows:**

| Bộ import | Số module | Tệp `.olean*` | Lần 1 (lạnh) | Lần 2 | Lần 3 |
|---|---|---|---|---|---|
| `import Mathlib` (WSL 10 GB) | 9117 | 5,51 GB | 351 s, peak 6144 MB | 80 s | 25 s |
| Import cụ thể của `ThuVienGT` (WSL 8 GB) | 2322 | 1,45 GB | **21 s**, peak 3608 MB | **2,8 s** | **2,3 s** |
| Như trên, đọc trước tệp `.olean*` từ máy (9,4 s) | 2322 | 1,45 GB | 18,9 s | 3,1 s | 3,2 s |

Kết luận và thay đổi:
- **Yếu tố quyết định là chỉ import phần Mathlib cần dùng.** `lean/ThuVienGT.lean` đã chuyển sang import cụ thể ngay từ M0 (mục 7 cho phép đổi ở cuối M2); M2 thêm import khi cần. Với `Mathlib.Algebra.Order.Field.Rat` riêng (đủ cho `chuanHoa`): 799 module, 0,48 GB.
- **Đọc trước tệp từ máy gần như vô ích** (bớt 2,5 s, tốn 9,4 s): phần chậm còn lại nằm ở toolchain trong ảnh Docker. `LeanRunner.lam_nong()` và lệnh `sinhde nen-tang lam-nong` vì vậy chạy **một tệp Lean chỉ gồm các import trong sandbox**, một lần ở đầu mỗi đợt sinh (khoảng 21 s khi lạnh, 2–3 s khi nóng). Mã tính bao đóng import (`sinhde/lean/bao_dong_import.py`) được giữ để đo dung lượng.
- `.wslconfig` hạ `memory` từ 10 GB xuống 8 GB. Giữ `so_tien_trinh: 1`, `bo_nho_gb: 6`.
- **Bộ nhớ Windows là ràng buộc thật của máy này.** Tiến trình `fczf` (do `fclauncher.exe` khởi chạy) chiếm khoảng 4,8 GB từ lúc máy khởi động. Khi chạy kiểm thử, commit của Windows xuống còn 0,3–0,4 GB. Trước các đợt sinh dài nên tắt chương trình này, và nên đặt thêm pagefile trên ổ D: (ổ C: còn ít chỗ) để nâng giới hạn commit.
- Ghi chú cho M2: nếu `ThuVienGT` dùng hệ thống module (`module`), import từ module khác chỉ nạp phần `.olean` công khai (nhẹ hơn khoảng 3 lần). Nhưng khi đó thân định nghĩa không được xuất mặc định, mà `decide +kernel` trong chứng nhận cần thân của `chuanHoa`; phải đánh dấu xuất các định nghĩa đó. Cần thử trước khi quyết định.

## Thử nghiệm 2: `decide` trên `chuanHoa` với ℚ (mục 7.9, 12.6)
Tệp: `thu_nghiem/decide/`. Định nghĩa `BT`, `chuanHoa` chép theo mục 7.1, 7.3; chỉ import `Mathlib.Algebra.Order.Field.Rat`.

**Lần đo đầu (bản cũ, giữ để đối chiếu):** một cây viết tay (độ sâu 8, khoảng 40 nút).

| Chiến thuật | Kết quả |
|---|---|
| `decide` | Không đạt: elaborator không rút gọn được các phép toán trên ℚ |
| `decide +kernel` | Đạt |
| `rfl` | Không đạt |

Cách đo của lần này sai: mốc nền lấy từ lần chạy lạnh, nên các số "trừ nền" bị âm; và mới thử 1 cây, trong khi mục 7.9 yêu cầu 50 cây.

**Lần đo sửa lại** (`chay_50_cay.py`): 50 cây ngẫu nhiên (seed 20261124), mỗi cây 35–40 nút, độ sâu 7–8, có hằng nguyên, phân số, tham số `((2 : ℤ) : ℚ)` như `de 2`, lũy thừa từ −2 đến 3 và 12 hàm. Mệnh đề thử `chuanHoa e = chuanHoa (chuanHoa e)`, chứng minh bằng `decide +kernel`. Mỗi cây được đo riêng bằng mốc `IO.monoMsNow` trước và sau, với `Elab.async false`.

| Chỉ số | Kết quả |
|---|---|
| Số cây đạt | **50/50** |
| Thời gian mỗi cây | trung bình **69 ms**, lớn nhất **89 ms** (tiêu chí 7.9: dưới 10 s) |
| Cả tệp, gồm nạp Mathlib | 5,3 s |
| Phụ: tính lũy đẳng của `chuanHoa` | đúng trên cả 50 cây |

`thoa_R` và `khop_diem` (`chay_rang_buoc.py`): đạt với cả `decide` thường lẫn `decide +kernel`, vì không có phép chia nào trên ℚ cần rút gọn.

Kết luận: `thoa_R`, `khop_cay`, `khop_diem` (mục 12.6) đều dùng `decide +kernel` cho thống nhất. Không dùng `native_decide`.

## Thử nghiệm 3: tiện ích `kiem_khop` (mục 12.7) — bản sửa
Bản đầu chạy bằng `lean --run` (thông dịch), kiểu mong đợi viết cứng trong mã, chưa có JSON và chưa thử tấn công. Bản sửa:
- `lean/KiemKhop/Main.lean`, build thành `lean_exe kiem_khop` (tệp thực thi khoảng 124 MB), chạy qua `LeanRunner.kiem_khop`.
- Đầu vào: tệp JSON `{"module", "dinh_ly", "kieu"}`, trong đó `kieu` là S-biểu thức của `Expr`: `(c Tên cấp…)`, `(a hàm đối…)`, `(n số)`. Tiện ích dựng `Expr` thẳng từ S-biểu thức, không qua bộ phân tích Lean.
- Đầu ra: tệp JSON trong thư mục `/ra` gắn riêng cho lần chạy; Python không đọc stdout.
- Đạt khi: tồn tại, là `theorem`, không có tham số vũ trụ, kernel xác nhận kiểu khớp, mọi axiom thuộc {`propext`, `Classical.choice`, `Quot.sound`}.

Kiểm thử `tests/test_kiem_khop.py` (8/8 đạt), trên các module mẫu `lean/KiemThu/`:

| Trường hợp | Kết quả |
|---|---|
| `dung : 2 + 2 = 4` | Đạt, không có axiom |
| `gia : True` | Bị loại: `khop_kieu = false` |
| `dungAxiomTuKhai` (dùng axiom tự khai báo) | Bị loại: `axiom_chuan = false` |
| `tuKhai` (là `axiom`) | Bị loại: `la_theorem = false` |
| `khongCo` | Bị loại: `ton_tai = false` |
| **`TanCong.tanCong`**: module khai báo `macro_rules` đọc "(2 : Nat) + 2 = 4" thành `True` | **Bị loại**: `khop_kieu = false` |
| S-biểu thức hỏng | Bị loại, không có tệp kết quả |
| Module không tồn tại | Bị loại |

**Đối chứng với cổng kiểm bản 1.1** (`thu_nghiem/tan_cong/chay.py`), cùng module tấn công:

| Cổng kiểm | Kết quả |
|---|---|
| Bản 1.1: tệp văn bản `example : (2 : Nat) + 2 = 4 := KiemThu.TanCong.tanCong` cộng `#print axioms` | **Biên dịch đạt, báo không có axiom → bị lừa** |
| Bản 1.2: `kiem_khop` ở mức `Expr` | **Chặn đúng** (`khop_kieu = false`) |

Đây là bằng chứng trực tiếp cho thay đổi số 1 của bản 1.2: một macro toàn cục trong module được import đủ để làm cổng kiểm dạng văn bản chấp nhận một chứng nhận rỗng.

API đã chốt cho Lean 4.36.0:
- `importModules #[{ module := m }] {} (loadExts := false)`; không gọi `enableInitializersExecution`.
- `Kernel.isDefEq env {} a b : Except Kernel.Exception Bool`.
- `collectAxioms : Name → m (Array Name)` (cần `MonadEnv`), chạy qua `CoreM.toIO`.
- `Lean.levelOne` đã lỗi thời, dùng `Level.one`.

Đề xuất cho M4: Python (`kiem_tin_cay.py`, tin cậy) dịch cây đọc ngược thành S-biểu thức `Expr` của `DeDungGioiHan00 …`; tiện ích giữ dạng tổng quát như hiện nay. Cách này giữ tiện ích Lean nhỏ, dễ duyệt.

Cần sửa thiết kế mục 13.2: ở chế độ `build_module`, ngoài `.lake/build`, thư mục `.lake/config` cũng phải ghi được, vì Lake ghi lại bản cache cấu hình mỗi khi `lakefile.lean` thay đổi.

## Ghi chú cho các mốc sau
- Lean 4.36 cảnh báo `imports Mathlib … designed for use with the module system; consider adding module`. Xem xét dùng hệ thống module ở M2.
