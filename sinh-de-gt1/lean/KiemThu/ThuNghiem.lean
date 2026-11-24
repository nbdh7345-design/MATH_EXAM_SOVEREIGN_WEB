-- Module mẫu cho kiểm thử tiện ích kiem_khop (M0, thử nghiệm 3). Không phải chứng nhận thật.
namespace KiemThu.ThuNghiem

theorem dung : (2 : Nat) + 2 = 4 := rfl

theorem gia : True := trivial

axiom tuKhai : (1 : Nat) = 2

theorem dungAxiomTuKhai : (2 : Nat) + 2 = 4 := by
  have := tuKhai
  rfl

end KiemThu.ThuNghiem
