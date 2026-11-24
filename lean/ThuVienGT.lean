-- TIN CẬY (phần định nghĩa) — thư viện ThuVienGT (mục 7).
-- M0: thư viện còn rỗng; các tệp con được thêm ở M2.
--
-- Import cụ thể thay cho `import Mathlib` ngay từ M0 (mục 7 cho phép đổi ở cuối M2):
-- trên máy phát triển 15,5 GB RAM, `import Mathlib` cần khoảng 5,5 GB cache, lần chạy lạnh
-- mất 351 s và làm Windows cạn bộ nhớ; bộ import dưới đây cần 1,45 GB và mất 21 s
-- (thử nghiệm 1, docs/ket_qua_M0.md). M2 thêm import khi cần.
import Mathlib.Analysis.SpecialFunctions.Trigonometric.ArctanDeriv
import Mathlib.Analysis.SpecialFunctions.Trigonometric.InverseDeriv
import Mathlib.Analysis.SpecialFunctions.Pow.Deriv
import Mathlib.Analysis.SpecialFunctions.Sqrt
import Mathlib.Analysis.Calculus.LHopital
import Mathlib.Tactic.IntervalCases
import Mathlib.Tactic.FieldSimp
