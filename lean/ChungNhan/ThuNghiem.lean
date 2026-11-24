-- Module mẫu cho thử nghiệm rủi ro 3 (M0). Không phải chứng nhận thật.
namespace ChungNhan.ThuNghiem

theorem dung : (2 : Nat) + 2 = 4 := rfl

theorem gia : True := trivial

axiom tuKhai : (1 : Nat) = 2

theorem dungAxiomTuKhai : (2 : Nat) + 2 = 4 := by
  have := tuKhai
  rfl

end ChungNhan.ThuNghiem
