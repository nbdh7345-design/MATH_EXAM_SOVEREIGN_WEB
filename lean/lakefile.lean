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
