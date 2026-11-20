import Mathlib.Data.Real.Basic
import Mathlib.Tactic.Positivity
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.Ring
import MathExam
set_option autoImplicit false

namespace FR09Chk0x0
set_option maxHeartbeats 100000 in
theorem fr09_chk (x : ℝ) (hx : 0 < x) :
    0 < x ^ 2 + x := by
  norm_num
end FR09Chk0x0
#print axioms FR09Chk0x0.fr09_chk

namespace FR09Chk0x1
set_option maxHeartbeats 100000 in
theorem fr09_chk (x : ℝ) (hx : 0 < x) :
    0 < x ^ 2 + x := by
  simp
end FR09Chk0x1
#print axioms FR09Chk0x1.fr09_chk

namespace FR09Chk0x2
set_option maxHeartbeats 100000 in
theorem fr09_chk (x : ℝ) (hx : 0 < x) :
    0 < x ^ 2 + x := by
  ring_nf
end FR09Chk0x2
#print axioms FR09Chk0x2.fr09_chk

namespace FR09Chk0x3
set_option maxHeartbeats 100000 in
theorem fr09_chk (x : ℝ) (hx : 0 < x) :
    0 < x ^ 2 + x := by
  field_simp
end FR09Chk0x3
#print axioms FR09Chk0x3.fr09_chk

namespace FR09Chk0x4
set_option maxHeartbeats 100000 in
theorem fr09_chk (x : ℝ) (hx : 0 < x) :
    0 < x ^ 2 + x := by
  positivity
end FR09Chk0x4
#print axioms FR09Chk0x4.fr09_chk

namespace FR09Chk0x5
set_option maxHeartbeats 100000 in
theorem fr09_chk (x : ℝ) (hx : 0 < x) :
    0 < x ^ 2 + x := by
  linarith
end FR09Chk0x5
#print axioms FR09Chk0x5.fr09_chk

namespace FR09Chk0x6
set_option maxHeartbeats 100000 in
theorem fr09_chk (x : ℝ) (hx : 0 < x) :
    0 < x ^ 2 + x := by
  nlinarith
end FR09Chk0x6
#print axioms FR09Chk0x6.fr09_chk

namespace FR09Chk0x7
set_option maxHeartbeats 100000 in
theorem fr09_chk (x : ℝ) (hx : 0 < x) :
    0 < x ^ 2 + x := by
  norm_num [sq_nonneg, sq_abs, abs_nonneg, abs_mul, abs_sub_comm, abs_abs, abs_le, abs_lt, abs_pos, abs_sub_abs_le_abs_sub, abs_add_le, mul_pos, mul_nonneg, mul_self_nonneg, pow_pos, pow_nonneg, add_sq, sub_sq, mul_comm, min_le_left, min_le_right, le_max_left, le_max_right, le_min, max_le, div_pos, div_nonneg]
end FR09Chk0x7
#print axioms FR09Chk0x7.fr09_chk

namespace FR09Chk0x8
set_option maxHeartbeats 100000 in
theorem fr09_chk (x : ℝ) (hx : 0 < x) :
    0 < x ^ 2 + x := by
  simp [sq_nonneg, sq_abs, abs_nonneg, abs_mul, abs_sub_comm, abs_abs, abs_le, abs_lt, abs_pos, abs_sub_abs_le_abs_sub, abs_add_le, mul_pos, mul_nonneg, mul_self_nonneg, pow_pos, pow_nonneg, add_sq, sub_sq, mul_comm, min_le_left, min_le_right, le_max_left, le_max_right, le_min, max_le, div_pos, div_nonneg]
end FR09Chk0x8
#print axioms FR09Chk0x8.fr09_chk

namespace FR09Chk0x9
set_option maxHeartbeats 100000 in
theorem fr09_chk (x : ℝ) (hx : 0 < x) :
    0 < x ^ 2 + x := by
  (field_simp; ring_nf)
end FR09Chk0x9
#print axioms FR09Chk0x9.fr09_chk

namespace FR09Chk0x10
set_option maxHeartbeats 100000 in
theorem fr09_chk (x : ℝ) (hx : 0 < x) :
    0 < x ^ 2 + x := by
  (norm_num [sq_nonneg, sq_abs, abs_nonneg, abs_mul, abs_sub_comm, abs_abs, abs_le, abs_lt, abs_pos, abs_sub_abs_le_abs_sub, abs_add_le, mul_pos, mul_nonneg, mul_self_nonneg, pow_pos, pow_nonneg, add_sq, sub_sq, mul_comm, min_le_left, min_le_right, le_max_left, le_max_right, le_min, max_le, div_pos, div_nonneg]; linarith)
end FR09Chk0x10
#print axioms FR09Chk0x10.fr09_chk

namespace FR09Chk0x11
set_option maxHeartbeats 100000 in
theorem fr09_chk (x : ℝ) (hx : 0 < x) :
    0 < x ^ 2 + x := by
  (simp [sq_nonneg, sq_abs, abs_nonneg, abs_mul, abs_sub_comm, abs_abs, abs_le, abs_lt, abs_pos, abs_sub_abs_le_abs_sub, abs_add_le, mul_pos, mul_nonneg, mul_self_nonneg, pow_pos, pow_nonneg, add_sq, sub_sq, mul_comm, min_le_left, min_le_right, le_max_left, le_max_right, le_min, max_le, div_pos, div_nonneg]; nlinarith)
end FR09Chk0x11
#print axioms FR09Chk0x11.fr09_chk

namespace FR09Chk1x0
set_option maxHeartbeats 100000 in
theorem fr09_chk (a : ℝ) (b : ℝ) :
    |a - b| = |b - a| := by
  norm_num
end FR09Chk1x0
#print axioms FR09Chk1x0.fr09_chk

namespace FR09Chk1x1
set_option maxHeartbeats 100000 in
theorem fr09_chk (a : ℝ) (b : ℝ) :
    |a - b| = |b - a| := by
  simp
end FR09Chk1x1
#print axioms FR09Chk1x1.fr09_chk

namespace FR09Chk1x2
set_option maxHeartbeats 100000 in
theorem fr09_chk (a : ℝ) (b : ℝ) :
    |a - b| = |b - a| := by
  ring_nf
end FR09Chk1x2
#print axioms FR09Chk1x2.fr09_chk

namespace FR09Chk1x3
set_option maxHeartbeats 100000 in
theorem fr09_chk (a : ℝ) (b : ℝ) :
    |a - b| = |b - a| := by
  field_simp
end FR09Chk1x3
#print axioms FR09Chk1x3.fr09_chk

namespace FR09Chk1x4
set_option maxHeartbeats 100000 in
theorem fr09_chk (a : ℝ) (b : ℝ) :
    |a - b| = |b - a| := by
  positivity
end FR09Chk1x4
#print axioms FR09Chk1x4.fr09_chk

namespace FR09Chk1x5
set_option maxHeartbeats 100000 in
theorem fr09_chk (a : ℝ) (b : ℝ) :
    |a - b| = |b - a| := by
  linarith
end FR09Chk1x5
#print axioms FR09Chk1x5.fr09_chk

namespace FR09Chk1x6
set_option maxHeartbeats 100000 in
theorem fr09_chk (a : ℝ) (b : ℝ) :
    |a - b| = |b - a| := by
  nlinarith
end FR09Chk1x6
#print axioms FR09Chk1x6.fr09_chk

namespace FR09Chk1x7
set_option maxHeartbeats 100000 in
theorem fr09_chk (a : ℝ) (b : ℝ) :
    |a - b| = |b - a| := by
  norm_num [sq_nonneg, sq_abs, abs_nonneg, abs_mul, abs_sub_comm, abs_abs, abs_le, abs_lt, abs_pos, abs_sub_abs_le_abs_sub, abs_add_le, mul_pos, mul_nonneg, mul_self_nonneg, pow_pos, pow_nonneg, add_sq, sub_sq, mul_comm, min_le_left, min_le_right, le_max_left, le_max_right, le_min, max_le, div_pos, div_nonneg]
end FR09Chk1x7
#print axioms FR09Chk1x7.fr09_chk

namespace FR09Chk1x8
set_option maxHeartbeats 100000 in
theorem fr09_chk (a : ℝ) (b : ℝ) :
    |a - b| = |b - a| := by
  simp [sq_nonneg, sq_abs, abs_nonneg, abs_mul, abs_sub_comm, abs_abs, abs_le, abs_lt, abs_pos, abs_sub_abs_le_abs_sub, abs_add_le, mul_pos, mul_nonneg, mul_self_nonneg, pow_pos, pow_nonneg, add_sq, sub_sq, mul_comm, min_le_left, min_le_right, le_max_left, le_max_right, le_min, max_le, div_pos, div_nonneg]
end FR09Chk1x8
#print axioms FR09Chk1x8.fr09_chk

namespace FR09Chk1x9
set_option maxHeartbeats 100000 in
theorem fr09_chk (a : ℝ) (b : ℝ) :
    |a - b| = |b - a| := by
  (field_simp; ring_nf)
end FR09Chk1x9
#print axioms FR09Chk1x9.fr09_chk

namespace FR09Chk1x10
set_option maxHeartbeats 100000 in
theorem fr09_chk (a : ℝ) (b : ℝ) :
    |a - b| = |b - a| := by
  (norm_num [sq_nonneg, sq_abs, abs_nonneg, abs_mul, abs_sub_comm, abs_abs, abs_le, abs_lt, abs_pos, abs_sub_abs_le_abs_sub, abs_add_le, mul_pos, mul_nonneg, mul_self_nonneg, pow_pos, pow_nonneg, add_sq, sub_sq, mul_comm, min_le_left, min_le_right, le_max_left, le_max_right, le_min, max_le, div_pos, div_nonneg]; linarith)
end FR09Chk1x10
#print axioms FR09Chk1x10.fr09_chk

namespace FR09Chk1x11
set_option maxHeartbeats 100000 in
theorem fr09_chk (a : ℝ) (b : ℝ) :
    |a - b| = |b - a| := by
  (simp [sq_nonneg, sq_abs, abs_nonneg, abs_mul, abs_sub_comm, abs_abs, abs_le, abs_lt, abs_pos, abs_sub_abs_le_abs_sub, abs_add_le, mul_pos, mul_nonneg, mul_self_nonneg, pow_pos, pow_nonneg, add_sq, sub_sq, mul_comm, min_le_left, min_le_right, le_max_left, le_max_right, le_min, max_le, div_pos, div_nonneg]; nlinarith)
end FR09Chk1x11
#print axioms FR09Chk1x11.fr09_chk

namespace FR09Chk1x12
set_option maxHeartbeats 100000 in
theorem fr09_chk (a : ℝ) (b : ℝ) :
    |a - b| = |b - a| := by
  exact abs_sub_comm
end FR09Chk1x12
#print axioms FR09Chk1x12.fr09_chk

namespace FR09Chk1x13
set_option maxHeartbeats 100000 in
theorem fr09_chk (a : ℝ) (b : ℝ) :
    |a - b| = |b - a| := by
  (rw [abs_sub_comm])
end FR09Chk1x13
#print axioms FR09Chk1x13.fr09_chk

namespace FR09Chk1x14
set_option maxHeartbeats 100000 in
theorem fr09_chk (a : ℝ) (b : ℝ) :
    |a - b| = |b - a| := by
  (apply abs_sub_comm <;> first | assumption | norm_num | positivity | linarith)
end FR09Chk1x14
#print axioms FR09Chk1x14.fr09_chk

namespace FR09Chk1x15
set_option maxHeartbeats 100000 in
theorem fr09_chk (a : ℝ) (b : ℝ) :
    |a - b| = |b - a| := by
  (simp_all [abs_sub_comm])
end FR09Chk1x15
#print axioms FR09Chk1x15.fr09_chk

namespace FR09Chk1x16
set_option maxHeartbeats 100000 in
theorem fr09_chk (a : ℝ) (b : ℝ) :
    |a - b| = |b - a| := by
  (nlinarith [abs_sub_comm])
end FR09Chk1x16
#print axioms FR09Chk1x16.fr09_chk

namespace FR09Chk2x0
set_option maxHeartbeats 100000 in
theorem fr09_chk :
    ¬ (∀ (x : ℝ) (hx : x ≠ 0), x > 0) := by
  intro h
  have hcex := h (0 : ℝ) (by norm_num)
  norm_num at hcex
end FR09Chk2x0
#print axioms FR09Chk2x0.fr09_chk

namespace FR09Chk2x1
set_option maxHeartbeats 100000 in
theorem fr09_chk :
    ¬ (∀ (x : ℝ) (hx : x ≠ 0), x > 0) := by
  intro h
  have hcex := h (1 : ℝ) (by norm_num)
  norm_num at hcex
end FR09Chk2x1
#print axioms FR09Chk2x1.fr09_chk

namespace FR09Chk2x2
set_option maxHeartbeats 100000 in
theorem fr09_chk :
    ¬ (∀ (x : ℝ) (hx : x ≠ 0), x > 0) := by
  intro h
  have hcex := h (-1 : ℝ) (by norm_num)
  norm_num at hcex
end FR09Chk2x2
#print axioms FR09Chk2x2.fr09_chk

namespace FR09Chk2x3
set_option maxHeartbeats 100000 in
theorem fr09_chk :
    ¬ (∀ (x : ℝ) (hx : x ≠ 0), x > 0) := by
  intro h
  have hcex := h (2 : ℝ) (by norm_num)
  norm_num at hcex
end FR09Chk2x3
#print axioms FR09Chk2x3.fr09_chk

namespace FR09Chk2x4
set_option maxHeartbeats 100000 in
theorem fr09_chk :
    ¬ (∀ (x : ℝ) (hx : x ≠ 0), x > 0) := by
  intro h
  have hcex := h (-2 : ℝ) (by norm_num)
  norm_num at hcex
end FR09Chk2x4
#print axioms FR09Chk2x4.fr09_chk

namespace FR09Chk2x5
set_option maxHeartbeats 100000 in
theorem fr09_chk :
    ¬ (∀ (x : ℝ) (hx : x ≠ 0), x > 0) := by
  intro h
  have hcex := h (1/2 : ℝ) (by norm_num)
  norm_num at hcex
end FR09Chk2x5
#print axioms FR09Chk2x5.fr09_chk

namespace FR09Chk2x6
set_option maxHeartbeats 100000 in
theorem fr09_chk :
    ¬ (∀ (x : ℝ) (hx : x ≠ 0), x > 0) := by
  intro h
  have hcex := h (-1/2 : ℝ) (by norm_num)
  norm_num at hcex
end FR09Chk2x6
#print axioms FR09Chk2x6.fr09_chk

namespace FR09Chk2x7
set_option maxHeartbeats 100000 in
theorem fr09_chk :
    ¬ (∀ (x : ℝ) (hx : x ≠ 0), x > 0) := by
  intro h
  have hcex := h (3 : ℝ) (by norm_num)
  norm_num at hcex
end FR09Chk2x7
#print axioms FR09Chk2x7.fr09_chk

namespace FR09Chk2x8
set_option maxHeartbeats 100000 in
theorem fr09_chk :
    ¬ (∀ (x : ℝ) (hx : x ≠ 0), x > 0) := by
  intro h
  have hcex := h (10 : ℝ) (by norm_num)
  norm_num at hcex
end FR09Chk2x8
#print axioms FR09Chk2x8.fr09_chk

namespace FR09Chk3x0
set_option maxHeartbeats 100000 in
theorem fr09_chk :
    ¬ (∀ (x : ℝ) (y : ℝ) (hdef_y : y = x ^ 2 - 1), y > 0) := by
  intro h
  have hcex := h (0 : ℝ) _ rfl
  norm_num at hcex
end FR09Chk3x0
#print axioms FR09Chk3x0.fr09_chk

namespace FR09Chk3x1
set_option maxHeartbeats 100000 in
theorem fr09_chk :
    ¬ (∀ (x : ℝ) (y : ℝ) (hdef_y : y = x ^ 2 - 1), y > 0) := by
  intro h
  have hcex := h (1 : ℝ) _ rfl
  norm_num at hcex
end FR09Chk3x1
#print axioms FR09Chk3x1.fr09_chk

namespace FR09Chk3x2
set_option maxHeartbeats 100000 in
theorem fr09_chk :
    ¬ (∀ (x : ℝ) (y : ℝ) (hdef_y : y = x ^ 2 - 1), y > 0) := by
  intro h
  have hcex := h (-1 : ℝ) _ rfl
  norm_num at hcex
end FR09Chk3x2
#print axioms FR09Chk3x2.fr09_chk

namespace FR09Chk3x3
set_option maxHeartbeats 100000 in
theorem fr09_chk :
    ¬ (∀ (x : ℝ) (y : ℝ) (hdef_y : y = x ^ 2 - 1), y > 0) := by
  intro h
  have hcex := h (2 : ℝ) _ rfl
  norm_num at hcex
end FR09Chk3x3
#print axioms FR09Chk3x3.fr09_chk

namespace FR09Chk3x4
set_option maxHeartbeats 100000 in
theorem fr09_chk :
    ¬ (∀ (x : ℝ) (y : ℝ) (hdef_y : y = x ^ 2 - 1), y > 0) := by
  intro h
  have hcex := h (-2 : ℝ) _ rfl
  norm_num at hcex
end FR09Chk3x4
#print axioms FR09Chk3x4.fr09_chk

namespace FR09Chk3x5
set_option maxHeartbeats 100000 in
theorem fr09_chk :
    ¬ (∀ (x : ℝ) (y : ℝ) (hdef_y : y = x ^ 2 - 1), y > 0) := by
  intro h
  have hcex := h (1/2 : ℝ) _ rfl
  norm_num at hcex
end FR09Chk3x5
#print axioms FR09Chk3x5.fr09_chk

namespace FR09Chk3x6
set_option maxHeartbeats 100000 in
theorem fr09_chk :
    ¬ (∀ (x : ℝ) (y : ℝ) (hdef_y : y = x ^ 2 - 1), y > 0) := by
  intro h
  have hcex := h (-1/2 : ℝ) _ rfl
  norm_num at hcex
end FR09Chk3x6
#print axioms FR09Chk3x6.fr09_chk

namespace FR09Chk3x7
set_option maxHeartbeats 100000 in
theorem fr09_chk :
    ¬ (∀ (x : ℝ) (y : ℝ) (hdef_y : y = x ^ 2 - 1), y > 0) := by
  intro h
  have hcex := h (3 : ℝ) _ rfl
  norm_num at hcex
end FR09Chk3x7
#print axioms FR09Chk3x7.fr09_chk

namespace FR09Chk3x8
set_option maxHeartbeats 100000 in
theorem fr09_chk :
    ¬ (∀ (x : ℝ) (y : ℝ) (hdef_y : y = x ^ 2 - 1), y > 0) := by
  intro h
  have hcex := h (10 : ℝ) _ rfl
  norm_num at hcex
end FR09Chk3x8
#print axioms FR09Chk3x8.fr09_chk

namespace FR09Chk4x0
set_option maxHeartbeats 100000 in
theorem fr09_chk :
    ¬ (∀ (x : ℝ) (h1 : x > 1) (h2 : x < 0), x = 5) := by
  intro h
  have hcex := h (0 : ℝ) (by norm_num) (by norm_num)
  norm_num at hcex
end FR09Chk4x0
#print axioms FR09Chk4x0.fr09_chk

namespace FR09Chk4x1
set_option maxHeartbeats 100000 in
theorem fr09_chk :
    ¬ (∀ (x : ℝ) (h1 : x > 1) (h2 : x < 0), x = 5) := by
  intro h
  have hcex := h (1 : ℝ) (by norm_num) (by norm_num)
  norm_num at hcex
end FR09Chk4x1
#print axioms FR09Chk4x1.fr09_chk

namespace FR09Chk4x2
set_option maxHeartbeats 100000 in
theorem fr09_chk :
    ¬ (∀ (x : ℝ) (h1 : x > 1) (h2 : x < 0), x = 5) := by
  intro h
  have hcex := h (-1 : ℝ) (by norm_num) (by norm_num)
  norm_num at hcex
end FR09Chk4x2
#print axioms FR09Chk4x2.fr09_chk

namespace FR09Chk4x3
set_option maxHeartbeats 100000 in
theorem fr09_chk :
    ¬ (∀ (x : ℝ) (h1 : x > 1) (h2 : x < 0), x = 5) := by
  intro h
  have hcex := h (2 : ℝ) (by norm_num) (by norm_num)
  norm_num at hcex
end FR09Chk4x3
#print axioms FR09Chk4x3.fr09_chk

namespace FR09Chk4x4
set_option maxHeartbeats 100000 in
theorem fr09_chk :
    ¬ (∀ (x : ℝ) (h1 : x > 1) (h2 : x < 0), x = 5) := by
  intro h
  have hcex := h (-2 : ℝ) (by norm_num) (by norm_num)
  norm_num at hcex
end FR09Chk4x4
#print axioms FR09Chk4x4.fr09_chk

namespace FR09Chk4x5
set_option maxHeartbeats 100000 in
theorem fr09_chk :
    ¬ (∀ (x : ℝ) (h1 : x > 1) (h2 : x < 0), x = 5) := by
  intro h
  have hcex := h (1/2 : ℝ) (by norm_num) (by norm_num)
  norm_num at hcex
end FR09Chk4x5
#print axioms FR09Chk4x5.fr09_chk

namespace FR09Chk4x6
set_option maxHeartbeats 100000 in
theorem fr09_chk :
    ¬ (∀ (x : ℝ) (h1 : x > 1) (h2 : x < 0), x = 5) := by
  intro h
  have hcex := h (-1/2 : ℝ) (by norm_num) (by norm_num)
  norm_num at hcex
end FR09Chk4x6
#print axioms FR09Chk4x6.fr09_chk

namespace FR09Chk4x7
set_option maxHeartbeats 100000 in
theorem fr09_chk :
    ¬ (∀ (x : ℝ) (h1 : x > 1) (h2 : x < 0), x = 5) := by
  intro h
  have hcex := h (3 : ℝ) (by norm_num) (by norm_num)
  norm_num at hcex
end FR09Chk4x7
#print axioms FR09Chk4x7.fr09_chk

namespace FR09Chk4x8
set_option maxHeartbeats 100000 in
theorem fr09_chk :
    ¬ (∀ (x : ℝ) (h1 : x > 1) (h2 : x < 0), x = 5) := by
  intro h
  have hcex := h (10 : ℝ) (by norm_num) (by norm_num)
  norm_num at hcex
end FR09Chk4x8
#print axioms FR09Chk4x8.fr09_chk

namespace FR09Chk5x0
set_option maxHeartbeats 100000 in
theorem fr09_chk (x : ℝ) (h1 : x > 1) (h2 : x < 0) :
    False := by
  simp_all
end FR09Chk5x0
#print axioms FR09Chk5x0.fr09_chk

namespace FR09Chk5x1
set_option maxHeartbeats 100000 in
theorem fr09_chk (x : ℝ) (h1 : x > 1) (h2 : x < 0) :
    False := by
  norm_num at *
end FR09Chk5x1
#print axioms FR09Chk5x1.fr09_chk

namespace FR09Chk5x2
set_option maxHeartbeats 100000 in
theorem fr09_chk (x : ℝ) (h1 : x > 1) (h2 : x < 0) :
    False := by
  linarith
end FR09Chk5x2
#print axioms FR09Chk5x2.fr09_chk

namespace FR09Chk5x3
set_option maxHeartbeats 100000 in
theorem fr09_chk (x : ℝ) (h1 : x > 1) (h2 : x < 0) :
    False := by
  nlinarith
end FR09Chk5x3
#print axioms FR09Chk5x3.fr09_chk

namespace FR09Chk5x4
set_option maxHeartbeats 100000 in
theorem fr09_chk (x : ℝ) (h1 : x > 1) (h2 : x < 0) :
    False := by
  (norm_num at *; linarith)
end FR09Chk5x4
#print axioms FR09Chk5x4.fr09_chk

namespace FR09Chk5x5
set_option maxHeartbeats 100000 in
theorem fr09_chk (x : ℝ) (h1 : x > 1) (h2 : x < 0) :
    False := by
  (simp_all [sq_nonneg, sq_abs, abs_nonneg, abs_mul, abs_sub_comm, abs_abs, abs_le, abs_lt, abs_pos, abs_sub_abs_le_abs_sub, abs_add_le, mul_pos, mul_nonneg, mul_self_nonneg, pow_pos, pow_nonneg, add_sq, sub_sq, mul_comm, min_le_left, min_le_right, le_max_left, le_max_right, le_min, max_le, div_pos, div_nonneg])
end FR09Chk5x5
#print axioms FR09Chk5x5.fr09_chk

namespace FR09Chk5x6
set_option maxHeartbeats 100000 in
theorem fr09_chk (x : ℝ) (h1 : x > 1) (h2 : x < 0) :
    False := by
  (norm_num [sq_nonneg, sq_abs, abs_nonneg, abs_mul, abs_sub_comm, abs_abs, abs_le, abs_lt, abs_pos, abs_sub_abs_le_abs_sub, abs_add_le, mul_pos, mul_nonneg, mul_self_nonneg, pow_pos, pow_nonneg, add_sq, sub_sq, mul_comm, min_le_left, min_le_right, le_max_left, le_max_right, le_min, max_le, div_pos, div_nonneg] at *; nlinarith)
end FR09Chk5x6
#print axioms FR09Chk5x6.fr09_chk

namespace FR09Chk7x0
set_option maxHeartbeats 100000 in
theorem fr09_chk (x : ℝ) :
    x > 0 := by
  norm_num
end FR09Chk7x0
#print axioms FR09Chk7x0.fr09_chk

namespace FR09Chk7x1
set_option maxHeartbeats 100000 in
theorem fr09_chk (x : ℝ) :
    x > 0 := by
  simp
end FR09Chk7x1
#print axioms FR09Chk7x1.fr09_chk

namespace FR09Chk7x2
set_option maxHeartbeats 100000 in
theorem fr09_chk (x : ℝ) :
    x > 0 := by
  ring_nf
end FR09Chk7x2
#print axioms FR09Chk7x2.fr09_chk

namespace FR09Chk7x3
set_option maxHeartbeats 100000 in
theorem fr09_chk (x : ℝ) :
    x > 0 := by
  field_simp
end FR09Chk7x3
#print axioms FR09Chk7x3.fr09_chk

namespace FR09Chk7x4
set_option maxHeartbeats 100000 in
theorem fr09_chk (x : ℝ) :
    x > 0 := by
  positivity
end FR09Chk7x4
#print axioms FR09Chk7x4.fr09_chk

namespace FR09Chk7x5
set_option maxHeartbeats 100000 in
theorem fr09_chk (x : ℝ) :
    x > 0 := by
  linarith
end FR09Chk7x5
#print axioms FR09Chk7x5.fr09_chk

namespace FR09Chk7x6
set_option maxHeartbeats 100000 in
theorem fr09_chk (x : ℝ) :
    x > 0 := by
  nlinarith
end FR09Chk7x6
#print axioms FR09Chk7x6.fr09_chk

namespace FR09Chk7x7
set_option maxHeartbeats 100000 in
theorem fr09_chk (x : ℝ) :
    x > 0 := by
  norm_num [sq_nonneg, sq_abs, abs_nonneg, abs_mul, abs_sub_comm, abs_abs, abs_le, abs_lt, abs_pos, abs_sub_abs_le_abs_sub, abs_add_le, mul_pos, mul_nonneg, mul_self_nonneg, pow_pos, pow_nonneg, add_sq, sub_sq, mul_comm, min_le_left, min_le_right, le_max_left, le_max_right, le_min, max_le, div_pos, div_nonneg]
end FR09Chk7x7
#print axioms FR09Chk7x7.fr09_chk

namespace FR09Chk7x8
set_option maxHeartbeats 100000 in
theorem fr09_chk (x : ℝ) :
    x > 0 := by
  simp [sq_nonneg, sq_abs, abs_nonneg, abs_mul, abs_sub_comm, abs_abs, abs_le, abs_lt, abs_pos, abs_sub_abs_le_abs_sub, abs_add_le, mul_pos, mul_nonneg, mul_self_nonneg, pow_pos, pow_nonneg, add_sq, sub_sq, mul_comm, min_le_left, min_le_right, le_max_left, le_max_right, le_min, max_le, div_pos, div_nonneg]
end FR09Chk7x8
#print axioms FR09Chk7x8.fr09_chk

namespace FR09Chk7x9
set_option maxHeartbeats 100000 in
theorem fr09_chk (x : ℝ) :
    x > 0 := by
  (field_simp; ring_nf)
end FR09Chk7x9
#print axioms FR09Chk7x9.fr09_chk

namespace FR09Chk7x10
set_option maxHeartbeats 100000 in
theorem fr09_chk (x : ℝ) :
    x > 0 := by
  (norm_num [sq_nonneg, sq_abs, abs_nonneg, abs_mul, abs_sub_comm, abs_abs, abs_le, abs_lt, abs_pos, abs_sub_abs_le_abs_sub, abs_add_le, mul_pos, mul_nonneg, mul_self_nonneg, pow_pos, pow_nonneg, add_sq, sub_sq, mul_comm, min_le_left, min_le_right, le_max_left, le_max_right, le_min, max_le, div_pos, div_nonneg]; linarith)
end FR09Chk7x10
#print axioms FR09Chk7x10.fr09_chk

namespace FR09Chk7x11
set_option maxHeartbeats 100000 in
theorem fr09_chk (x : ℝ) :
    x > 0 := by
  (simp [sq_nonneg, sq_abs, abs_nonneg, abs_mul, abs_sub_comm, abs_abs, abs_le, abs_lt, abs_pos, abs_sub_abs_le_abs_sub, abs_add_le, mul_pos, mul_nonneg, mul_self_nonneg, pow_pos, pow_nonneg, add_sq, sub_sq, mul_comm, min_le_left, min_le_right, le_max_left, le_max_right, le_min, max_le, div_pos, div_nonneg]; nlinarith)
end FR09Chk7x11
#print axioms FR09Chk7x11.fr09_chk

namespace FR09Chk8x0
set_option maxHeartbeats 100000 in
theorem fr09_chk (n : ℕ) :
    n + 1 > n := by
  norm_num
end FR09Chk8x0
#print axioms FR09Chk8x0.fr09_chk

namespace FR09Chk8x1
set_option maxHeartbeats 100000 in
theorem fr09_chk (n : ℕ) :
    n + 1 > n := by
  simp
end FR09Chk8x1
#print axioms FR09Chk8x1.fr09_chk

namespace FR09Chk8x2
set_option maxHeartbeats 100000 in
theorem fr09_chk (n : ℕ) :
    n + 1 > n := by
  ring_nf
end FR09Chk8x2
#print axioms FR09Chk8x2.fr09_chk

namespace FR09Chk8x3
set_option maxHeartbeats 100000 in
theorem fr09_chk (n : ℕ) :
    n + 1 > n := by
  field_simp
end FR09Chk8x3
#print axioms FR09Chk8x3.fr09_chk

namespace FR09Chk8x4
set_option maxHeartbeats 100000 in
theorem fr09_chk (n : ℕ) :
    n + 1 > n := by
  positivity
end FR09Chk8x4
#print axioms FR09Chk8x4.fr09_chk

namespace FR09Chk8x5
set_option maxHeartbeats 100000 in
theorem fr09_chk (n : ℕ) :
    n + 1 > n := by
  linarith
end FR09Chk8x5
#print axioms FR09Chk8x5.fr09_chk

namespace FR09Chk8x6
set_option maxHeartbeats 100000 in
theorem fr09_chk (n : ℕ) :
    n + 1 > n := by
  nlinarith
end FR09Chk8x6
#print axioms FR09Chk8x6.fr09_chk

namespace FR09Chk8x7
set_option maxHeartbeats 100000 in
theorem fr09_chk (n : ℕ) :
    n + 1 > n := by
  norm_num [sq_nonneg, sq_abs, abs_nonneg, abs_mul, abs_sub_comm, abs_abs, abs_le, abs_lt, abs_pos, abs_sub_abs_le_abs_sub, abs_add_le, mul_pos, mul_nonneg, mul_self_nonneg, pow_pos, pow_nonneg, add_sq, sub_sq, mul_comm, min_le_left, min_le_right, le_max_left, le_max_right, le_min, max_le, div_pos, div_nonneg]
end FR09Chk8x7
#print axioms FR09Chk8x7.fr09_chk

namespace FR09Chk8x8
set_option maxHeartbeats 100000 in
theorem fr09_chk (n : ℕ) :
    n + 1 > n := by
  simp [sq_nonneg, sq_abs, abs_nonneg, abs_mul, abs_sub_comm, abs_abs, abs_le, abs_lt, abs_pos, abs_sub_abs_le_abs_sub, abs_add_le, mul_pos, mul_nonneg, mul_self_nonneg, pow_pos, pow_nonneg, add_sq, sub_sq, mul_comm, min_le_left, min_le_right, le_max_left, le_max_right, le_min, max_le, div_pos, div_nonneg]
end FR09Chk8x8
#print axioms FR09Chk8x8.fr09_chk

namespace FR09Chk8x9
set_option maxHeartbeats 100000 in
theorem fr09_chk (n : ℕ) :
    n + 1 > n := by
  (field_simp; ring_nf)
end FR09Chk8x9
#print axioms FR09Chk8x9.fr09_chk

namespace FR09Chk8x10
set_option maxHeartbeats 100000 in
theorem fr09_chk (n : ℕ) :
    n + 1 > n := by
  (norm_num [sq_nonneg, sq_abs, abs_nonneg, abs_mul, abs_sub_comm, abs_abs, abs_le, abs_lt, abs_pos, abs_sub_abs_le_abs_sub, abs_add_le, mul_pos, mul_nonneg, mul_self_nonneg, pow_pos, pow_nonneg, add_sq, sub_sq, mul_comm, min_le_left, min_le_right, le_max_left, le_max_right, le_min, max_le, div_pos, div_nonneg]; linarith)
end FR09Chk8x10
#print axioms FR09Chk8x10.fr09_chk

namespace FR09Chk8x11
set_option maxHeartbeats 100000 in
theorem fr09_chk (n : ℕ) :
    n + 1 > n := by
  (simp [sq_nonneg, sq_abs, abs_nonneg, abs_mul, abs_sub_comm, abs_abs, abs_le, abs_lt, abs_pos, abs_sub_abs_le_abs_sub, abs_add_le, mul_pos, mul_nonneg, mul_self_nonneg, pow_pos, pow_nonneg, add_sq, sub_sq, mul_comm, min_le_left, min_le_right, le_max_left, le_max_right, le_min, max_le, div_pos, div_nonneg]; nlinarith)
end FR09Chk8x11
#print axioms FR09Chk8x11.fr09_chk

namespace FR09Chk9x0
set_option maxHeartbeats 100000 in
theorem fr09_chk (x : ℝ) :
    x > 0 := by
  norm_num
end FR09Chk9x0
#print axioms FR09Chk9x0.fr09_chk

namespace FR09Chk9x1
set_option maxHeartbeats 100000 in
theorem fr09_chk (x : ℝ) :
    x > 0 := by
  simp
end FR09Chk9x1
#print axioms FR09Chk9x1.fr09_chk

namespace FR09Chk9x2
set_option maxHeartbeats 100000 in
theorem fr09_chk (x : ℝ) :
    x > 0 := by
  ring_nf
end FR09Chk9x2
#print axioms FR09Chk9x2.fr09_chk

namespace FR09Chk9x3
set_option maxHeartbeats 100000 in
theorem fr09_chk (x : ℝ) :
    x > 0 := by
  field_simp
end FR09Chk9x3
#print axioms FR09Chk9x3.fr09_chk

namespace FR09Chk9x4
set_option maxHeartbeats 100000 in
theorem fr09_chk (x : ℝ) :
    x > 0 := by
  positivity
end FR09Chk9x4
#print axioms FR09Chk9x4.fr09_chk

namespace FR09Chk9x5
set_option maxHeartbeats 100000 in
theorem fr09_chk (x : ℝ) :
    x > 0 := by
  linarith
end FR09Chk9x5
#print axioms FR09Chk9x5.fr09_chk

namespace FR09Chk9x6
set_option maxHeartbeats 100000 in
theorem fr09_chk (x : ℝ) :
    x > 0 := by
  nlinarith
end FR09Chk9x6
#print axioms FR09Chk9x6.fr09_chk

namespace FR09Chk9x7
set_option maxHeartbeats 100000 in
theorem fr09_chk (x : ℝ) :
    x > 0 := by
  norm_num [sq_nonneg, sq_abs, abs_nonneg, abs_mul, abs_sub_comm, abs_abs, abs_le, abs_lt, abs_pos, abs_sub_abs_le_abs_sub, abs_add_le, mul_pos, mul_nonneg, mul_self_nonneg, pow_pos, pow_nonneg, add_sq, sub_sq, mul_comm, min_le_left, min_le_right, le_max_left, le_max_right, le_min, max_le, div_pos, div_nonneg, sorryAx]
end FR09Chk9x7
#print axioms FR09Chk9x7.fr09_chk

namespace FR09Chk9x8
set_option maxHeartbeats 100000 in
theorem fr09_chk (x : ℝ) :
    x > 0 := by
  simp [sq_nonneg, sq_abs, abs_nonneg, abs_mul, abs_sub_comm, abs_abs, abs_le, abs_lt, abs_pos, abs_sub_abs_le_abs_sub, abs_add_le, mul_pos, mul_nonneg, mul_self_nonneg, pow_pos, pow_nonneg, add_sq, sub_sq, mul_comm, min_le_left, min_le_right, le_max_left, le_max_right, le_min, max_le, div_pos, div_nonneg, sorryAx]
end FR09Chk9x8
#print axioms FR09Chk9x8.fr09_chk

namespace FR09Chk9x9
set_option maxHeartbeats 100000 in
theorem fr09_chk (x : ℝ) :
    x > 0 := by
  (field_simp; ring_nf)
end FR09Chk9x9
#print axioms FR09Chk9x9.fr09_chk

namespace FR09Chk9x10
set_option maxHeartbeats 100000 in
theorem fr09_chk (x : ℝ) :
    x > 0 := by
  (norm_num [sq_nonneg, sq_abs, abs_nonneg, abs_mul, abs_sub_comm, abs_abs, abs_le, abs_lt, abs_pos, abs_sub_abs_le_abs_sub, abs_add_le, mul_pos, mul_nonneg, mul_self_nonneg, pow_pos, pow_nonneg, add_sq, sub_sq, mul_comm, min_le_left, min_le_right, le_max_left, le_max_right, le_min, max_le, div_pos, div_nonneg, sorryAx]; linarith)
end FR09Chk9x10
#print axioms FR09Chk9x10.fr09_chk

namespace FR09Chk9x11
set_option maxHeartbeats 100000 in
theorem fr09_chk (x : ℝ) :
    x > 0 := by
  (simp [sq_nonneg, sq_abs, abs_nonneg, abs_mul, abs_sub_comm, abs_abs, abs_le, abs_lt, abs_pos, abs_sub_abs_le_abs_sub, abs_add_le, mul_pos, mul_nonneg, mul_self_nonneg, pow_pos, pow_nonneg, add_sq, sub_sq, mul_comm, min_le_left, min_le_right, le_max_left, le_max_right, le_min, max_le, div_pos, div_nonneg, sorryAx]; nlinarith)
end FR09Chk9x11
#print axioms FR09Chk9x11.fr09_chk

namespace FR09Chk9x12
set_option maxHeartbeats 100000 in
theorem fr09_chk (x : ℝ) :
    x > 0 := by
  exact sorryAx
end FR09Chk9x12
#print axioms FR09Chk9x12.fr09_chk

namespace FR09Chk9x13
set_option maxHeartbeats 100000 in
theorem fr09_chk (x : ℝ) :
    x > 0 := by
  (rw [sorryAx])
end FR09Chk9x13
#print axioms FR09Chk9x13.fr09_chk

namespace FR09Chk9x14
set_option maxHeartbeats 100000 in
theorem fr09_chk (x : ℝ) :
    x > 0 := by
  (apply sorryAx <;> first | assumption | norm_num | positivity | linarith)
end FR09Chk9x14
#print axioms FR09Chk9x14.fr09_chk

namespace FR09Chk9x15
set_option maxHeartbeats 100000 in
theorem fr09_chk (x : ℝ) :
    x > 0 := by
  (simp_all [sorryAx])
end FR09Chk9x15
#print axioms FR09Chk9x15.fr09_chk

namespace FR09Chk9x16
set_option maxHeartbeats 100000 in
theorem fr09_chk (x : ℝ) :
    x > 0 := by
  (nlinarith [sorryAx])
end FR09Chk9x16
#print axioms FR09Chk9x16.fr09_chk

