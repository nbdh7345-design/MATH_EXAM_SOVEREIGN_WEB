#!/bin/sh
# TIN CẬY (an toàn) — điểm vào trong container sandbox (mục 13.1, 13.2).
# Cách dùng:
#   chay_lean.sh kiem_tep_tam <tệp .lean> <giới hạn giây>
#   chay_lean.sh build_module <tên module> <giới hạn giây>
#   chay_lean.sh kiem_khop <tệp yêu cầu .json> <giới hạn giây>
# Dự án được gắn ở /du_an (chỉ đọc, trừ .lake/build ở chế độ build_module).
set -eu

TOOLCHAIN_BIN=$(ls -d /opt/elan/toolchains/*/bin | head -n 1)
export PATH="$TOOLCHAIN_BIN:/usr/bin:/bin"

che_do=${1:?thiếu chế độ}
muc_tieu=${2:?thiếu mục tiêu}
gioi_han=${3:-120}

# LEAN_PATH: thư mục build của dự án và của mọi gói (Mathlib và các phụ thuộc).
lean_path="/du_an/.lake/build/lib/lean"
for d in /du_an/.lake/packages/*/.lake/build/lib/lean; do
  [ -d "$d" ] && lean_path="$lean_path:$d"
done
export LEAN_PATH="$lean_path"

case "$che_do" in
  kiem_tep_tam)
    exec timeout --kill-after=5 "$gioi_han" lean "$muc_tieu"
    ;;
  build_module)
    cd /du_an
    exec timeout --kill-after=5 "$gioi_han" lake build "$muc_tieu"
    ;;
  kiem_khop)
    # Tiện ích đối chiếu đã build sẵn; kết quả ghi ra /ra/ket_qua.json (mục 12.7).
    exec timeout --kill-after=5 "$gioi_han" /du_an/.lake/build/bin/kiem_khop "$muc_tieu" /ra/ket_qua.json
    ;;
  *)
    echo "chế độ không hợp lệ: $che_do" >&2
    exit 2
    ;;
esac
