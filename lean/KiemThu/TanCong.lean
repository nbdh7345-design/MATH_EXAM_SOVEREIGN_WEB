-- Module mẫu cho phép thử tấn công (M0, thử nghiệm 3). Giả lập một bộ sinh tệp bị lỗi
-- hoặc bị tấn công: khai báo một macro toàn cục (không `local`) đổi nghĩa đúng một mệnh đề.
-- Mọi tệp import module này đều đọc "(2 : Nat) + 2 = 4" thành `True`.
macro_rules | `((2 : Nat) + 2 = 4) => `(True)

namespace KiemThu.TanCong

/-- Văn bản trông như chứng minh 2 + 2 = 4, nhưng kiểu thật là `True`. -/
theorem tanCong : (2 : Nat) + 2 = 4 := trivial

end KiemThu.TanCong
