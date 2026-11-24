-- Thử nghiệm rủi ro 2 (M0): decide trên chuanHoa với ℚ. Không thuộc ThuVienGT.
-- Định nghĩa chép theo mục 7.1 và 7.3 của thiết kế v1.2 (chỉ phần tính được).
import Mathlib

namespace ThuNghiem

inductive Ham
  | sin | cos | tan | cot | arcsin | arccos | arctan | exp | ln | sqrt | cbrt | abs
  deriving DecidableEq, Repr

inductive BT
  | hang (q : ℚ)
  | x
  | am (a : BT)
  | cong (a b : BT)
  | tru (a b : BT)
  | nhan (a b : BT)
  | chia (a b : BT)
  | mu (a : BT) (n : ℤ)
  | luythua (a b : BT)
  | ham (f : Ham) (a : BT)
  deriving DecidableEq, Repr

def mkAm : BT → BT
  | .hang q => .hang (-q)
  | e       => .am e

def mkCong : BT → BT → BT
  | .hang p, .hang q => .hang (p + q)
  | a, .hang q       => if q < 0 then .tru a (.hang (-q)) else .cong a (.hang q)
  | a, b             => .cong a b

def mkTru : BT → BT → BT
  | .hang p, .hang q => .hang (p - q)
  | a, .hang q       => if q < 0 then .cong a (.hang (-q)) else .tru a (.hang q)
  | a, b             => .tru a b

def mkNhan : BT → BT → BT
  | .hang p, .hang q => .hang (p * q)
  | .hang p, b       =>
      if p = 1 then b
      else if p = -1 then .am b
      else if p < 0 then .am (.nhan (.hang (-p)) b)
      else .nhan (.hang p) b
  | a, b             => .nhan a b

def mkChia : BT → BT → BT
  | .hang p, .hang q => if q ≠ 0 then .hang (p / q) else .chia (.hang p) (.hang q)
  | a, b             => .chia a b

def mkMu : BT → ℤ → BT
  | .hang p, n => if p ≠ 0 ∨ 0 < n then .hang (p ^ n) else .mu (.hang p) n
  | a, n       => if n = 1 then a else .mu a n

def chuanHoa : BT → BT
  | .hang q      => .hang q
  | .x           => .x
  | .am a        => mkAm (chuanHoa a)
  | .cong a b    => mkCong (chuanHoa a) (chuanHoa b)
  | .tru a b     => mkTru (chuanHoa a) (chuanHoa b)
  | .nhan a b    => mkNhan (chuanHoa a) (chuanHoa b)
  | .chia a b    => mkChia (chuanHoa a) (chuanHoa b)
  | .mu a n      => mkMu (chuanHoa a) n
  | .luythua a b => .luythua (chuanHoa a) (chuanHoa b)
  | .ham f a     => .ham f (chuanHoa a)

/-- Khuôn tham số p1 (giống `de p1` ở mục 11.3): độ sâu 8, khoảng 40 nút. -/
def de (p1 : ℤ) : BT :=
  .chia
    (.cong
      (.tru (.mu .x 3) (.nhan (.hang ((3 : ℚ) / 2)) (.mu (.hang (p1 : ℚ)) 2)))
      (.nhan (.am (.hang (p1 : ℚ)))
        (.cong (.mu (.ham .sin (.chia .x (.hang (p1 : ℚ)))) 2)
               (.tru (.hang ((-7 : ℚ) / 3)) (.nhan (.hang 2) (.mu .x (-1)))))))
    (.tru
      (.nhan (.cong .x (.hang ((p1 : ℚ) / 5))) (.ham .sqrt (.cong (.mu .x 2) (.hang 1))))
      (.mu (.tru (.hang (p1 : ℚ)) (.hang ((1 : ℚ) / 4))) 3))

/-- Cây "đọc ngược" giả lập: cùng dạng chuẩn với `de 2`, viết khác đi. -/
def deDoc : BT := chuanHoa (de 2)

end ThuNghiem
open ThuNghiem

set_option maxRecDepth 100000 in
example : chuanHoa (de 2) = chuanHoa deDoc := by CHIEN_THUAT
