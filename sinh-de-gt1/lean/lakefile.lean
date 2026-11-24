import Lake
open Lake DSL

package sinh_de where

-- Mathlib cố định theo bản phát hành khớp lean-toolchain (mục 5.2, 5.5)
require mathlib from git
  "https://github.com/leanprover-community/mathlib4" @ "v4.36.0"

@[default_target]
lean_lib ThuVienGT

lean_lib ThuVienKhuon where
  globs := #[.submodules `ThuVienKhuon]

lean_lib ChungNhan where
  globs := #[.submodules `ChungNhan]

-- Module mẫu cho kiểm thử của tiện ích đối chiếu (không phải chứng nhận thật).
lean_lib KiemThu where
  globs := #[.submodules `KiemThu]

-- Tiện ích đối chiếu (TIN CẬY, mục 12.7). Chỉ import Lean;
-- không import ThuVienKhuon hay ChungNhan: module cần kiểm được nạp lúc chạy.
-- Bản M0 (thử nghiệm 3); hoàn thiện và duyệt ở M4.
lean_exe kiem_khop where
  root := `KiemKhop.Main
