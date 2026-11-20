# -*- coding: utf-8 -*-
"""
lean_core.py - Lõi dùng chung của hệ thống (mục 2.5 đặc tả): FR08 hình thức hóa và FR09 chứng minh tự động
bằng Lean 4 + Mathlib. Lõi nhận một phát biểu tiếng Việt (FormalTask) cùng phần do hệ thống cố định (biến, giả thiết,
đáp án), không phụ thuộc câu hỏi hay CSDL. lean_formalizer.py là lớp chuyển đổi cho câu hỏi trong ngân hàng (NV1).

Thiết kế chống "formalize sai đề / chứng minh mệnh đề dễ hơn":
1. Header định lý do HỆ THỐNG sinh: tên `exam_answer`, khai báo tham số và miền giá trị lấy từ CSDL.
2. LLM chỉ viết mệnh đề bài toán có chỗ trống `ANSWER`; hệ thống dịch công thức đáp án lưu trong CSDL
   (SymPy) sang thuật ngữ Lean rồi điền vào. LLM không thể tự chọn đáp án.
3. Chặn tĩnh: sorry/admit/axiom/def/notation/macro/native_decide/set_option/... trước khi biên dịch.
4. Biên dịch thật bằng `lake env lean` trong workspace Mathlib; kiểm tra `#print axioms exam_answer`
   chỉ gồm propext, Classical.choice, Quot.sound (QT18).

FR08 - hình thức hóa (giai đoạn A, hàm formalize): trả mệnh đề được chọn, bản diễn đạt lại và kết luận "đã xác nhận" /
"chưa xác nhận", không chứng minh mệnh đề. Mệnh đề chỉ "đã xác nhận" khi đủ năm điều kiện của QT15:
  (1) biên dịch được (Lean kiểm kiểu với chứng minh tạm `sorry` do hệ thống đặt, sửa tối đa MATH_STATEMENT_FIXES lượt);
  (2) giả thiết không mâu thuẫn: tactic tự động không chứng minh được False từ giả thiết (mọi ứng viên), và với mệnh đề
      sắp được chọn, LLM (VACUITY_MODEL) cũng không đưa ra được chứng minh False mà Lean chấp nhận (_vacuous_llm);
  (3) đúng dạng theo QT16 (kiểm bằng luật: điều kiện tồn tại của đại lượng cần tính, "khi và chỉ khi" cho câu tìm tham
      số / biện luận, tích phân suy rộng là giới hạn của tích phân xác định);
  (4) có ít nhất 2 bản dịch độc lập được Lean chứng minh tương đương: tactic tự động trước; chưa được thì LLM viết chứng
      minh từng chiều "từ A suy ra B" và Lean kiểm thêm rằng chứng minh thật sự dùng giả thiết (_prove_equiv_llm); vẫn
      chưa có thì sinh thêm MATH_FORMALIZE_EXTRA bản dịch;
  (5) bản diễn đạt lại bằng tiếng Việt (dịch ngược bằng BACKTRANSLATE_MODEL) khớp phát biểu gốc (B8): giám khảo là mô hình mạnh
      hơn mô hình sinh (JUDGE_MODEL), không xem mã Lean, đối chiếu TỪNG PHẦN với bảng phân tích đề của B1 (lượng từ,
      đối tượng và miền, giả thiết, điều kiện xác định, kết luận; mỗi mục "đề nói" có câu trích được máy kiểm là có
      thật trong đề) và liệt kê, phân loại mọi khác biệt. Hệ thống kết luận khớp khi mọi khác biệt chỉ là điều kiện tồn
      tại, điều kiện xác định hoặc cách viết tương đương (JUDGE_ALLOWED). Chỉ đại diện của nhóm >= 2 được đưa giám khảo.
  Mọi lượt gọi LLM của FR08 tính vào hạn mức MATH_FR08_MAX_LLM (NFR04). Không mệnh đề nào đạt đủ năm điều kiện:
  UNCONFIRMED, không đưa đi chứng minh.
FR09 - chứng minh tự động (giai đoạn B): module lean_prover.py (hai chế độ tìm chứng minh / kiểm bước, ba chiều đúng /
  sai / mâu thuẫn, giới hạn heartbeat, bộ nhớ đệm, lưu chứng minh). Ở đây hàm prove() gọi lean_prover ở chế độ tìm chứng
  minh, thử từ cách rẻ đến cách tốn kém (QT19): (1) tactic tự động, không gọi LLM; (2) LLM viết chứng minh, sửa theo lỗi
  Lean tối đa MATH_PROOF_FIXES lượt (lượt sửa dùng PROOF_ESCALATE_MODEL); (3) chia bước trung gian. Lượt gọi LLM của cả
  câu bị giới hạn bởi MATH_FR09_TASK_MAX_LLM. Vẫn thất bại thì thử mệnh đề khác cùng nhóm tương đương với mệnh đề được chọn
  (MATH_STATEMENT_FALLBACKS mệnh đề), rồi viết lại mệnh đề theo cách khác (MATH_STATEMENT_REWRITES lần; phải được Lean
  chứng minh tương đương với mệnh đề được chọn). Cuối cùng thử chứng minh PHỦ ĐỊNH của mệnh đề: được thì DISPROVED
  (phát biểu sai), không thì FAILED (QT19: không chứng minh được không có nghĩa là sai).

Các bước cải thiện (bật/tắt bằng MATH_FORMALIZE_STEPS, mặc định "1,2,3,4"):
- Bước 1 (B1): phân tích đề thành bảng năm phần (NORMALIZE_MODEL), có câu trích nguyên văn; máy kiểm câu trích, độ
  phủ công thức và lượng từ, chưa đạt thì làm lại (lần cuối bằng JUDGE_MODEL).
- Bước 2: tách đề thành khái niệm con, truy xuất định nghĩa Mathlib/MathExam kèm định lý minh họa (lean_retrieval.py).
- Bước 3: LLM suy luận ánh xạ khái niệm sang Lean (trường `analysis`) trước khi viết mệnh đề.
- Bước 4: sinh MATH_FORMALIZE_CANDIDATES mệnh đề, biên dịch chung một file; chọn theo Li và cộng sự (NeurIPS 2024),
  điều chỉnh cho Lean: gom nhóm tương đương (Lean chứng minh mệnh đề_i ↔ mệnh đề_j), xếp nhóm theo kích thước (điểm
  ký hiệu). Điểm ngữ nghĩa (cos giữa vectơ BERT LaBSE của bản dịch ngược và đề gốc, kết hợp logarit với
  α = MATH_SCORE_ALPHA) chỉ đổi thứ tự thử các nhóm mà tốn một lượt dịch ngược cho mọi ứng viên, nên mặc định tắt
  (MATH_SEMANTIC_RANK=1 để bật).
"""

import concurrent.futures
import contextlib
import heapq
import itertools
import json
import math
import os
import re
import shutil
import subprocess
import sys
import threading
import time
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple

import sympy as sp

from llm_generator import LLM_MODEL, LLM_PROVIDER, _call_structured

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MATHLIB_OUT_DIR = os.path.join(BASE_DIR, "verified_lean", "mathlib")

LEAN_PROJECT = os.environ.get("MATH_LEAN_PROJECT", r"D:\MATH_EXAM_LEAN")
# Formalize hai giai đoạn: (A) mệnh đề, kiểm tra kiểu với chứng minh tạm `sorry`; (B) chứng minh mệnh đề đã chọn
STATEMENT_FIXES = int(os.environ.get("MATH_STATEMENT_FIXES", "2"))  # số lượt sửa mệnh đề chưa hợp lệ
PROOF_FIXES = int(os.environ.get("MATH_PROOF_FIXES", "2"))  # số lượt sửa chứng minh (0-2)
# Chứng minh thất bại: thử mệnh đề khác cùng nhóm tương đương với mệnh đề đã xác nhận (Lean đã chứng minh tương đương)
STATEMENT_FALLBACKS = int(os.environ.get("MATH_STATEMENT_FALLBACKS", "1"))
# Vẫn chưa chứng minh được: viết lại mệnh đề theo cách khác (đề + đáp án giữ nguyên) rồi chứng minh lại
STATEMENT_REWRITES = int(os.environ.get("MATH_STATEMENT_REWRITES", "1"))
LEAN_TIMEOUT_SEC = int(os.environ.get("MATH_LEAN_TIMEOUT", "400"))
LEAN_MODEL = os.environ.get("MATH_LEAN_MODEL", LLM_MODEL)
# Lượt chứng minh đầu tiên dùng LEAN_MODEL; Lean báo sai thì các lượt sửa chứng minh dùng model mạnh hơn.
# Mặc định Sonnet mới nhất ("sonnet" cho claude CLI); đặt rỗng để không đổi model.
PROOF_ESCALATE_MODEL = os.environ.get(
    "MATH_PROOF_ESCALATE_MODEL", "claude-sonnet-5-5" if LLM_PROVIDER == "anthropic" else "sonnet")
# Điều kiện (5): giám khảo kiểm bản diễn đạt lại phải là mô hình mạnh hơn mô hình sinh (Haiku). Mỗi đề chỉ gọi giám khảo
# khoảng một lượt (valid_v3: 1,00 lượt/bài) và đây là bước duy nhất Lean không kiểm được, nên giám khảo có mức suy nghĩ
# riêng (JUDGE_EFFORT, mặc định high) cao hơn các bước khác. Mặc định Sonnet, KHÔNG dùng Opus: Opus là mô hình chấm lại
# benchmark (benchmark_proofnet.py judge), giữ hai vai trò "quyết định" và "chấm điểm" ở hai mô hình khác nhau.
JUDGE_MODEL = os.environ.get("MATH_JUDGE_MODEL") or PROOF_ESCALATE_MODEL or (
    "claude-sonnet-5-5" if LLM_PROVIDER == "anthropic" else "sonnet")
JUDGE_EFFORT = os.environ.get("MATH_JUDGE_EFFORT", "high")
# B1 (bảng phân tích đề) và dịch ngược: Lean không bắt được lỗi ở hai bước này (giám khảo chỉ đọc bản dịch ngược và
# đối chiếu với bảng B1), mỗi đề chỉ gọi khoảng một lượt, nên dùng mô hình mạnh hơn mô hình viết mệnh đề (mặc định Sonnet)
NORMALIZE_MODEL = os.environ.get("MATH_NORMALIZE_MODEL") or PROOF_ESCALATE_MODEL or LEAN_MODEL
BACKTRANSLATE_MODEL = os.environ.get("MATH_BACKTRANSLATE_MODEL") or PROOF_ESCALATE_MODEL or LEAN_MODEL
# Điều kiện (4): cần >= 2 bản dịch độc lập được Lean chứng minh tương đương; chưa có thì sinh thêm bấy nhiêu bản dịch
REQUIRE_EQUIV = os.environ.get("MATH_REQUIRE_EQUIV", "1") == "1"
# Điều kiện (3): kiểm đúng dạng theo QT16 bằng luật (tắt chỉ để đo đóng góp của bước này)
FORM_CHECK = os.environ.get("MATH_FORM_CHECK", "1") == "1"
EXTRA_CANDIDATES = int(os.environ.get("MATH_FORMALIZE_EXTRA", "2"))
# Điều kiện (4) khi tactic tự động không chứng minh được tương đương: LLM viết chứng minh từng chiều (FR09, chế độ tìm
# chứng minh), trước khi sinh thêm bản dịch. Số cặp thử mỗi lần xếp hạng và số lượt sửa cho mỗi cặp.
EQUIV_LLM_PAIRS = int(os.environ.get("MATH_EQUIV_LLM_PAIRS", "1"))
EQUIV_LLM_FIXES = int(os.environ.get("MATH_EQUIV_LLM_FIXES", "1"))
# Số nhóm tương đương tối đa đưa giám khảo (điều kiện 5), theo thứ tự xếp hạng
JUDGE_GROUPS = int(os.environ.get("MATH_JUDGE_GROUPS", "2"))
# Điểm ngữ nghĩa (dịch ngược mọi ứng viên + LaBSE) chỉ để sắp thứ tự các nhóm; mặc định tắt, thứ tự theo kích thước nhóm
SEMANTIC_RANK = os.environ.get("MATH_SEMANTIC_RANK", "0") == "1"
# Hạn mức lượt gọi LLM của FR08 cho một phát biểu (NFR04); FR08_RESERVE lượt giữ lại cho dịch ngược + giám khảo
FR08_MAX_LLM_CALLS = int(os.environ.get("MATH_FR08_MAX_LLM", "16"))
# Điều kiện (2) bằng FR09: tactic tự động không chứng minh được False từ giả thiết thì LLM thử (chỉ cho mệnh đề sắp được
# chọn, sau giám khảo). Bỏ sót mâu thuẫn để mệnh đề nào cũng "chứng minh được" và Lean không bắt được lỗi này, nên dùng
# mô hình mạnh (mặc định Sonnet); mỗi đề thường chỉ một lượt (LLM kết luận không mâu thuẫn thì dừng).
DEEP_VACUITY = os.environ.get("MATH_DEEP_VACUITY", "1") == "1"
VACUITY_MODEL = os.environ.get("MATH_VACUITY_MODEL") or PROOF_ESCALATE_MODEL or LEAN_MODEL
VACUITY_LLM_FIXES = int(os.environ.get("MATH_VACUITY_LLM_FIXES", "1"))
# Số lượt giữ lại cho các bước sau của FR08: dịch ngược + giám khảo (+ kiểm mâu thuẫn bằng LLM)
FR08_RESERVE = 2 + (1 if DEEP_VACUITY else 0)
# FR09 thử từ cách rẻ đến cách tốn kém: tactic tự động trước khi gọi LLM; cuối cùng chia bước trung gian
AUTO_PROVE = os.environ.get("MATH_AUTO_PROVE", "1") == "1"
DECOMPOSE = os.environ.get("MATH_PROOF_DECOMPOSE", "1") == "1"
# Hạn mức lượt gọi LLM của phần chứng minh (FR09) cho MỘT câu hỏi, gồm cả viết lại mệnh đề (NFR04)
FR09_TASK_MAX_LLM = int(os.environ.get("MATH_FR09_TASK_MAX_LLM", "14"))
# Chứng minh phủ định khi không chứng minh được mệnh đề: số lượt sửa (-1 để tắt)
DISPROVE_FIXES = int(os.environ.get("MATH_DISPROVE_FIXES", "1"))
# Mỗi tiến trình Lean nạp Mathlib cần vài GB bộ nhớ; mặc định chỉ chạy 1 tiến trình cùng lúc (RB2). Khi nhiều yêu cầu
# chờ, yêu cầu có mức ưu tiên cao hơn (số nhỏ hơn) được chạy trước (FR09): kiểm tra chứng minh của sinh viên (FR05),
# rồi sinh câu hỏi (FR01, FR08), cuối cùng là chứng minh lại khi hệ thống rảnh.
PRIORITY_FR05, PRIORITY_FR01, PRIORITY_REPROVE = 0, 1, 2
_priority_local = threading.local()


class _PriorityGate:
    """Giới hạn số tiến trình Lean chạy cùng lúc; cấp lượt theo (mức ưu tiên, thứ tự đến)."""

    def __init__(self, slots: int):
        self._slots, self._busy, self._seq = slots, 0, itertools.count()
        self._queue: List[Tuple[int, int]] = []
        self._cv = threading.Condition()

    @contextlib.contextmanager
    def slot(self, priority: int):
        ticket = (priority, next(self._seq))
        with self._cv:
            heapq.heappush(self._queue, ticket)
            while self._busy >= self._slots or self._queue[0] != ticket:
                self._cv.wait()
            heapq.heappop(self._queue)
            self._busy += 1
        try:
            yield
        finally:
            with self._cv:
                self._busy -= 1
                self._cv.notify_all()


_lean_gate = _PriorityGate(int(os.environ.get("MATH_LEAN_MAX_PARALLEL", "1")))


@contextlib.contextmanager
def lean_priority(level: int):
    """Mọi lần biên dịch Lean của luồng hiện tại trong khối này mang mức ưu tiên `level`."""
    old = getattr(_priority_local, "level", None)
    _priority_local.level = level
    try:
        yield
    finally:
        _priority_local.level = old

# Chỉ nạp các phần Mathlib cần cho Toán cao cấp: `import Mathlib` đầy đủ cần nhiều bộ nhớ hơn
# (trên máy ít RAM sẽ lỗi "failed to read file .olean"). Đặt MATH_LEAN_IMPORTS="Mathlib" để nạp toàn bộ.
_DEFAULT_IMPORTS = [
    "Mathlib.Tactic",
    "Mathlib.Analysis.SpecialFunctions.Integrals.Basic",
    "Mathlib.Analysis.SpecialFunctions.Pow.Deriv",
    "Mathlib.Analysis.SpecialFunctions.Trigonometric.Deriv",
    "Mathlib.Analysis.SpecialFunctions.Log.Deriv",
    "Mathlib.Analysis.SpecificLimits.Basic",
    "Mathlib.Analysis.Calculus.Taylor",
    "Mathlib.Analysis.Calculus.LHopital",
    "Mathlib.Analysis.Calculus.Deriv.Pow",
    "Mathlib.MeasureTheory.Integral.IntegralEqImproper",
    "Mathlib.Topology.Algebra.InfiniteSum.Real",
    "Mathlib.LinearAlgebra.Matrix.Determinant.Basic",
    "Mathlib.LinearAlgebra.Matrix.Rank",
    "Mathlib.LinearAlgebra.Matrix.Charpoly.Basic",
    "Mathlib.LinearAlgebra.Matrix.PosDef",
    "Mathlib.Analysis.InnerProductSpace.GramSchmidtOrtho",
]
_BASE_IMPORTS = [m.strip() for m in os.environ.get("MATH_LEAN_IMPORTS", ",".join(_DEFAULT_IMPORTS)).split(",") if m.strip()]
MAX_EXTRA_IMPORTS = 6

# Thư viện bổ sung MathExam (Sylvester 2×2/3×3, độ dài cung, Taylor tích phân nhiều biến, khai triển Maclaurin,
# VCB, điểm gián đoạn, đạo hàm riêng, diện tích hình phẳng, tích phân từng phần) trong workspace.
# Chỉ import khi đã `lake build MathExam` xong, để không làm hỏng biên dịch nếu chưa build.
_MATHEXAM_OLEAN = os.path.join(LEAN_PROJECT, ".lake", "build", "lib", "lean", "MathExam.olean")


def mathexam_ready() -> bool:
    return os.path.exists(_MATHEXAM_OLEAN)


def lean_imports() -> List[str]:
    return _BASE_IMPORTS + (["MathExam"] if mathexam_ready() else [])


MATHEXAM_GUIDE = """Thư viện bổ sung `MathExam` đã được import (namespace MathExam), dùng khi Mathlib thiếu:
- Độ dài cung (mặt phẳng `MathExam.Plane = EuclideanSpace ℝ (Fin 2)`):
  * `MathExam.arcLength γ a b = ∫ t in a..b, ‖deriv γ t‖`
  * `MathExam.graphCurve f`, `MathExam.paramCurve x y`, `MathExam.polarCurve r`
  * `MathExam.arcLength_graph (hf : Differentiable ℝ f) a b : arcLength (graphCurve f) a b = ∫ x in a..b, √(1 + deriv f x ^ 2)`
  * `MathExam.arcLength_paramCurve hx hy a b : arcLength (paramCurve x y) a b = ∫ t in a..b, √(deriv x t ^ 2 + deriv y t ^ 2)`
  * `MathExam.arcLength_polar hr a b : arcLength (polarCurve r) a b = ∫ θ in a..b, √(r θ ^ 2 + deriv r θ ^ 2)`
  Bài độ dài cung: statement nên là `MathExam.arcLength (MathExam.graphCurve (fun x => ...)) a b = ANSWER` (hoặc paramCurve/polarCurve), rồi rw bằng các định lý trên.
- Tiêu chuẩn Sylvester (ma trận đối xứng thực):
  * `MathExam.posDef_two_iff a b c : (!![a, b; b, c]).PosDef ↔ 0 < a ∧ 0 < a * c - b ^ 2`
  * `MathExam.negDef_two_iff a b c : (-(!![a, b; b, c])).PosDef ↔ a < 0 ∧ 0 < a * c - b ^ 2`
  * `MathExam.posDef_three_of_minors a b c d e f (h1 : 0 < a) (h2 : 0 < a * d - b ^ 2) (h3 : 0 < det !![a, b, c; b, d, e; c, e, f]) : (!![a, b, c; b, d, e; c, e, f]).PosDef`
- Taylor dạng tích phân (định lý gốc có sẵn trong Mathlib: `map_add_eq_sum_add_integral_iteratedFDeriv`,
  giả thiết `∀ t ∈ Set.Icc 0 1, ContDiffAt ℝ (n + 1) f (x + t • y)`; MathExam chỉ thêm hệ quả tiện dùng):
  * `MathExam.taylor_integral_unit n (hn : 0 < n) (hg : ContDiff ℝ n g)` (một biến, trên [0,1], dùng `iteratedDeriv`)
  * `MathExam.frechet_taylor_integral (hn : 0 < n) (hf : ∀ s ∈ Set.Icc 0 1, ContDiffAt ℝ n f (x + s • h))` (nhiều biến, giả thiết cục bộ)
  * `MathExam.frechet_taylor_integral_of_contDiff (hn : 0 < n) (hf : ContDiff ℝ n f) x h` (nhiều biến, giả thiết toàn cục)
  Với Taylor phần dư Lagrange một biến dùng `taylor_mean_remainder_lagrange` của Mathlib.
- Khảo sát hàm số (tiệm cận, điểm uốn):
  * `MathExam.IsVerticalAsymptote f a` (f → ±∞ khi x → a⁻ hoặc a⁺)
  * `MathExam.IsHorizontalAsymptoteAtTop f b` / `...AtBot` (f → b khi x → ±∞)
  * `MathExam.IsSlantAsymptoteAtTop f a b` / `...AtBot` (f x - (a*x + b) → 0)
  * `MathExam.isSlantAsymptoteAtTop_iff : IsSlantAsymptoteAtTop f a b ↔ Tendsto (fun x => f x / x) atTop (𝓝 a) ∧ Tendsto (fun x => f x - a * x) atTop (𝓝 b)` (tương tự `...AtBot_iff`)
  * `MathExam.isHorizontalAsymptoteAtTop_iff : IsHorizontalAsymptoteAtTop f b ↔ IsSlantAsymptoteAtTop f 0 b`
  * `MathExam.IsInflectionPoint f c` (đổi giữa lồi chặt và lõm chặt tại c)
  * `MathExam.isInflectionPoint_of_deriv2_sign (hδ : 0 < δ) (hf : ContinuousOn f (Icc (c-δ) (c+δ))) (h : (∀ x ∈ Ioo (c-δ) c, 0 < deriv^[2] f x) ∧ (∀ x ∈ Ioo c (c+δ), deriv^[2] f x < 0) ∨ (… ngược dấu))`
- Vật thể / mặt tròn xoay quanh Ox:
  * `MathExam.volume_real_solidOfRevolution (hf : Continuous f) (hab : a ≤ b) : (volume (solidOfRevolution f a b)).toReal = π * ∫ x in a..b, f x ^ 2`
    (bản ENNReal: `MathExam.volume_solidOfRevolution`). Statement bài thể tích: `(MeasureTheory.volume (MathExam.solidOfRevolution (fun x => ...) a b)).toReal = ANSWER`.
  * `MathExam.surfaceArea_revSurface (hf : Differentiable ℝ f) a b : surfaceArea (revSurface f) a b 0 (2 * π) = 2 * π * ∫ x in a..b, |f x| * √(1 + deriv f x ^ 2)`
  * `MathExam.surfaceArea_revSurface_of_nonneg hf (hpos : ∀ x ∈ Set.uIcc a b, 0 ≤ f x)` (bỏ trị tuyệt đối).
    Statement bài diện tích mặt tròn xoay: `MathExam.surfaceArea (MathExam.revSurface (fun x => ...)) a b 0 (2 * π) = ANSWER`.
  Khi rw với hàm cụ thể, truyền tường minh `(f := fun x => ...)` để khớp mẫu.
- Cực trị tự do hàm nhiều biến (f : EuclideanSpace ℝ (Fin n) → ℝ, điểm x₀):
  * `MathExam.hessianMatrix f x₀ i j = iteratedFDeriv ℝ 2 f x₀ ![EuclideanSpace.single i 1, EuclideanSpace.single j 1]`
    (`MathExam.hessianMatrix_apply`: bằng `fderiv ℝ (fderiv ℝ f) x₀ (single i 1) (single j 1)`)
  * `second_derivative_test (h₀ : gradient f x₀ = 0) (han : ContDiffAt ℝ 2 f x₀) (hf : (iteratedFDerivQuadraticMap f x₀).PosDef) : IsLocalMin f x₀`
  * `MathExam.isLocalMin_of_hessianMatrix_posDef h₀ hf (hH : (hessianMatrix f x₀).PosDef)`; cực đại: `MathExam.isLocalMax_of_neg_hessianMatrix_posDef` với `(-hessianMatrix f x₀).PosDef`
  * Hai biến: `MathExam.isLocalMin_of_hessian_two h₀ hf (hA : 0 < H 0 0) (hΔ : 0 < H 0 0 * H 1 1 - H 0 1 ^ 2)`, `MathExam.isLocalMax_of_hessian_two` (hA : H 0 0 < 0); ba biến: `MathExam.isLocalMin_of_hessian_three` (Δ₁, Δ₂, det > 0)
  Lưu ý: tính phần tử Hessian/gradient của hàm cụ thể qua `fderiv` khó tự động; chỉ dùng khi chứng minh được các giả thiết đó.
- Khai triển Maclaurin (phần dư Peano, dạng `(fun x => f x - P x) =o[𝓝 0] fun x => x ^ n`; mở `Filter Topology Asymptotics Real`):
  * `MathExam.exp_maclaurin a n : e^(a*x) - ∑ k ∈ range (n+1), a^k/k! * x^k = o(x^n)`; `MathExam.exp_maclaurin' n` (a = 1, dạng `x^k / k!`)
  * `MathExam.sin_maclaurin n : sin x - ∑ j ∈ range n, (-1)^j * x^(2j+1)/(2j+1)! = o(x^(2n))`; `MathExam.sin_mul_maclaurin a n` (cho `sin (a*x)`, số hạng `(a*x)^(2j+1)`)
  * `MathExam.cos_maclaurin n : cos x - ∑ j ∈ range (n+1), (-1)^j * x^(2j)/(2j)! = o(x^(2n+1))`; `MathExam.cos_mul_maclaurin a n`
  * `MathExam.log_one_add_maclaurin n : log (1+x) - ∑ k ∈ range n, (-1)^k * x^(k+1)/(k+1) = o(x^n)`
  * `MathExam.arctan_maclaurin n : arctan x - ∑ k ∈ range n, (-1)^k * x^(2k+1)/(2k+1) = o(x^(2n))`
  * `MathExam.one_add_rpow_maclaurin a n : (1+x)^a - ∑ k ∈ range (n+1), Ring.choose a k * x^k = o(x^n)` (rpow; hệ số tính bằng `MathExam.choose_real_eq a k : Ring.choose a k = (∏ i ∈ range k, (a - i)) / k!`; √ dùng `Real.sqrt_eq_rpow`)
  * `MathExam.maclaurin_of_contDiff (hf : ContDiff ℝ n f) : f x - ∑ k ∈ range (n+1), iteratedDeriv k f 0 / k! * x^k = o(x^n)` (hàm bất kỳ)
  * Thế biến: `MathExam.isLittleO_comp_mul h c` (từ `F(y)=o(yⁿ)` suy ra `F(c*x)=o(xⁿ)`); `MathExam.isLittleO_comp_mul_pow h c m hm` (`F(c*x^m) = o(x^(n*m))`, ví dụ `e^(c x²)`)
  * Hạ bậc: `MathExam.isLittleO_pow_of_le h (hnm : n ≤ m)` (o(xᵐ) ⇒ o(xⁿ)); `MathExam.isLittleO_monomial c (h : n < m)` (c*xᵐ = o(xⁿ)); nhân: `MathExam.isLittleO_mul_expansion`
  * Giới hạn: `MathExam.tendsto_div_pow_of_isLittleO (h : (fun x => f x - c * x^n) =o[𝓝 0] (·^n)) : Tendsto (fun x => f x / x^n) (𝓝[≠] 0) (𝓝 c)`;
    `MathExam.tendsto_div_of_isLittleO (hb : b ≠ 0) hf hg : Tendsto (fun x => f x / g x) (𝓝[≠] 0) (𝓝 (a / b))` (f = a xⁿ + o(xⁿ), g = b xⁿ + o(xⁿ))
  MẪU CHỨNG MINH giới hạn bằng khai triển (đã kiểm chứng):
    -- lim 6(e^(m x) - 1 - sin(m x) - m²x²/2)/x³ = 2m³
    have he := MathExam.exp_maclaurin (m : ℝ) 3
    have hs := MathExam.isLittleO_pow_of_le (MathExam.sin_mul_maclaurin (m : ℝ) 2) (by norm_num : 3 ≤ 2 * 2)
    apply MathExam.tendsto_div_pow_of_isLittleO
    refine ((he.sub hs).const_mul_left 6).congr_left fun x => ?_
    simp [Finset.sum_range_succ, Nat.factorial]
    ring
  (Mỗi khai triển thường cắt về cùng bậc n bằng `isLittleO_pow_of_le`; ghép bằng `.add`/`.sub`/`.const_mul_left`; bước cuối `congr_left` + `simp [Finset.sum_range_succ, Nat.factorial]` + `ring`.
   Với hàm hợp như `e^(-m²x²/2)`: `isLittleO_comp_mul_pow (exp_maclaurin' 2) (-m^2/2) 2 (by norm_num)` rồi trong `congr_left` viết lại đối số bằng `rw [show ... = ... by ring]`.)
- Vô cùng bé (VCB):
  * `MathExam.IsInfinitesimal f a` (f → 0 khi x → a, x ≠ a); `MathExam.IsInfinitesimalOfOrder f a k` (∃ c ≠ 0, f(x)/(x-a)^k → c); `MathExam.IsHigherOrderInfinitesimal f g a` (f = o(g))
  * `MathExam.isInfinitesimalOfOrder_of_isLittleO (hc : c ≠ 0) h`, `MathExam.isEquivalent_of_isLittleO hc h : f ~[𝓝 0] fun x => c * x^k`, `MathExam.isInfinitesimalOfOrder_of_isEquivalent hc h`
  * Bảng tương đương khi x → 0 (dạng `~[𝓝 0]`): `sin_equiv`, `tan_equiv`, `arcsin_equiv`, `arctan_equiv` (~ x), `exp_sub_one_equiv` (eˣ-1 ~ x), `log_one_add_equiv` (ln(1+x) ~ x),
    `one_sub_cos_equiv` (1 - cos x ~ 1/2 * x^2), `one_add_rpow_sub_one_equiv ha` ((1+x)^a - 1 ~ a*x), `rpow_sub_one_equiv ha ha1` (aˣ - 1 ~ log a * x), `isEquivalent_of_hasDerivAt hc h0 hd` (f ~ f'(0)·x)
  * Thay tương đương: `MathExam.tendsto_div_of_isEquivalent hf hg h`, `MathExam.tendsto_mul_of_isEquivalent`; thế biến `IsEquivalent.comp_tendsto`; đổi sang 𝓝[≠] 0 bằng `.mono nhdsWithin_le_nhds`
- Điểm gián đoạn (f : ℝ → ℝ, điểm a):
  * `MathExam.HasLeftLimit f a L`, `MathExam.HasRightLimit f a L` (giới hạn một phía hữu hạn, qua `𝓝[<] a`, `𝓝[>] a`)
  * `MathExam.IsRemovableDiscontinuity f a` (∃ L, lim f = L ≠ f a), `MathExam.IsJumpDiscontinuity f a` (∃ L₁ ≠ L₂ trái/phải), `MathExam.IsFirstKindDiscontinuity f a`, `MathExam.IsSecondKindDiscontinuity f a`
  * `MathExam.continuousAt_iff_left_right_limit`, `MathExam.tendsto_nhdsNE_iff_left_right`, `MathExam.isRemovableDiscontinuity_iff`, `MathExam.discontinuity_trichotomy`,
    `MathExam.isSecondKindDiscontinuity_of_tendsto_atTop_right` (và `_left`, `atBot`); `.not_continuousAt` cho cả ba loại
- Đạo hàm riêng hàm hai biến `f : ℝ × ℝ → ℝ` (điểm `p = (x₀, y₀)`):
  * `MathExam.partialX f p = deriv (fun x => f (x, p.2)) p.1`, `MathExam.partialY f p`; cấp hai `MathExam.partialXX/partialXY/partialYX/partialYY f p` (`partialXY = ∂/∂y(∂f/∂x)`)
  * Tính cụ thể: `simp only [MathExam.partialX]` rồi dùng `HasDerivAt.deriv` của hàm một biến
  * `MathExam.partialX_eq_fderiv hf`, `MathExam.fderiv_apply_eq_partial hf h k` (vi phân toàn phần df = f'ₓ h + f'ᵧ k), `MathExam.totalDiff_approx hf` (xấp xỉ bằng vi phân)
  * Hàm hợp: `MathExam.hasDerivAt_comp_curve hf hx hy` (z = f(x(t), y(t))), `MathExam.partialX_comp`, `MathExam.partialY_comp` (z = f(u(x,y), v(x,y)))
  * Hàm ẩn: `MathExam.hasDerivAt_implicit hF hφ (h0 : ∀ᶠ x in 𝓝 x₀, F (x, φ x) = 0) hFy : φ' = -partialX F (x₀, φ x₀) / partialY F (x₀, φ x₀)`
  * Schwarz: `MathExam.partialXY_eq_partialYX (hf : ContDiffAt ℝ 2 f p)`
- Diện tích hình phẳng (độ đo `MeasureTheory.volume` trên ℝ × ℝ):
  * `MathExam.area_regionBetween hab hf hg hfg : (volume (regionBetween f g (Icc a b))).toReal = ∫ x in a..b, (g x - f x)`
  * `MathExam.area_parametric hx hx' hg hle hg0 : (volume (regionBetween 0 g (Icc (x α) (x β)))).toReal = ∫ t in α..β, g (x t) * x' t`
  * Tọa độ cực: `MathExam.polarRegion r α β` (miền α < θ < β, 0 < ρ < r θ); `MathExam.area_polarRegion hr hα hβ hαβ hr0 : (volume (polarRegion r α β)).toReal = 1 / 2 * ∫ θ in α..β, r θ ^ 2` (-π ≤ α ≤ β ≤ π)
- Tích phân (ngoài các công thức sẵn có của Mathlib: integral_pow, integral_exp, integral_sin, integral_cos, integral_log, integral_inv_sq_add_sq, integral_sin_pow, integral_cos_sq…):
  * `MathExam.integral_eq_of_hasDerivAt hF hf` (Newton–Leibniz với nguyên hàm F tự chọn)
  * `MathExam.integral_mul_exp hc` (∫ x e^(cx)), `MathExam.integral_mul_sin hc`, `MathExam.integral_mul_cos hc`, `MathExam.integral_exp_mul_sin hpq`, `MathExam.integral_exp_mul_cos hpq`, `MathExam.integral_mul_log ha hb`

Module Mathlib KHÔNG import sẵn, thêm vào extra_imports khi cần:
- "Mathlib.Analysis.Calculus.LagrangeMultipliers": `IsLocalExtrOn.exists_multipliers_of_hasStrictFDerivAt` (nhân tử Lagrange)
- "Mathlib.Analysis.Calculus.Implicit": `HasStrictFDerivAt.implicitFunction`, `HasStrictFDerivAt.map_implicitFunction_eq` (định lý hàm ẩn — sự tồn tại)
- "Mathlib.Analysis.Calculus.ParametricIntegral": `hasDerivAt_integral_of_dominated_loc_of_deriv_le` (đạo hàm dưới dấu tích phân)
- "Mathlib.Analysis.SpecialFunctions.ImproperIntegrals": `integrableOn_Ioi_rpow_iff`, `integral_Ioi_rpow_of_lt`, `integral_exp_mul_Ioi`, `integral_exp_neg_Ioi`
- "Mathlib.Analysis.SpecialFunctions.Gamma.Beta": `Real.Gamma_eq_integral`, `Real.Gamma_add_one`, `Real.Gamma_nat_eq_factorial`, `Complex.betaIntegral`
- "Mathlib.Analysis.SpecialFunctions.Gaussian.GaussianIntegral": `integral_gaussian`
- "Mathlib.Analysis.Calculus.DerivativeTest": `isLocalMin_of_deriv_deriv_pos`, `isLocalMax_of_deriv_deriv_neg`, `isLocalMax_of_sign_deriv`, `isLocalMin_of_deriv_Ioo`
- "Mathlib.Analysis.Calculus.Deriv.MeanValue": `exists_deriv_eq_slope` (Lagrange), `exists_ratio_deriv_eq_ratio_slope` (Cauchy); "Mathlib.Analysis.Calculus.LocalExtr.Rolle": `exists_deriv_eq_zero` (Rolle)
- "Mathlib.Analysis.Convex.Deriv": `convexOn_of_deriv2_nonneg`, `strictConvexOn_of_deriv2_pos` (lồi/lõm)
- "Mathlib.Analysis.Calculus.LineDeriv.Basic": `lineDeriv` (đạo hàm theo hướng); "Mathlib.Analysis.Calculus.Gradient.Basic": `gradient`"""

# Ý nghĩa các định nghĩa MathExam, đưa cho người phản biện để đánh giá mệnh đề có dùng chúng
MATHEXAM_DEFS_FOR_REVIEW = """Các định nghĩa của thư viện MathExam (đã được kiểm tra khớp giáo trình, coi như định nghĩa chuẩn):
- MathExam.IsInfinitesimal f a: f(x) → 0 khi x → a (x ≠ a). MathExam.IsInfinitesimalOfOrder f a k: ∃ c ≠ 0, f(x)/(x-a)^k → c khi x → a (VCB bậc k). MathExam.IsHigherOrderInfinitesimal f g a: f = o(g) khi x → a.
- MathExam.HasLeftLimit/HasRightLimit f a L: giới hạn trái/phải hữu hạn bằng L. MathExam.IsRemovableDiscontinuity f a: ∃ L, lim_{x→a} f = L và L ≠ f(a) (hàm không xác định tại a được gán giá trị tùy ý).
  MathExam.IsJumpDiscontinuity f a: giới hạn trái L₁ và phải L₂ hữu hạn, L₁ ≠ L₂. MathExam.IsFirstKindDiscontinuity: khử được hoặc bước nhảy. MathExam.IsSecondKindDiscontinuity: ít nhất một giới hạn một phía không tồn tại hữu hạn.
- MathExam.partialX f (x₀, y₀) = đạo hàm của x ↦ f(x, y₀) tại x₀ (∂f/∂x); MathExam.partialY tương tự; MathExam.partialXY f = ∂/∂y(∂f/∂x), partialYX = ∂/∂x(∂f/∂y), partialXX, partialYY.
- MathExam.polarRegion r α β: miền {(ρ cos θ, ρ sin θ) | α < θ < β, 0 < ρ < r(θ)} (bỏ biên, diện tích không đổi). regionBetween f g s (Mathlib): {(x, y) | x ∈ s, f x < y < g x}. Diện tích = (MeasureTheory.volume S).toReal.
- MathExam.arcLength γ a b = ∫ ‖γ'(t)‖ dt; graphCurve/paramCurve/polarCurve: đường cong đồ thị/tham số/cực. MathExam.solidOfRevolution f a b: vật thể tròn xoay quanh Ox; MathExam.surfaceArea (revSurface f): diện tích mặt tròn xoay.
- MathExam.IsVerticalAsymptote / IsHorizontalAsymptoteAtTop / IsSlantAsymptoteAtTop …: tiệm cận đứng/ngang/xiên; MathExam.IsInflectionPoint f c: điểm uốn; MathExam.hessianMatrix f x₀: ma trận Hessian."""

ALLOWED_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}
THEOREM_NAME = "exam_answer"


def _lake_bin() -> str:
    found = shutil.which("lake")
    if found:
        return found
    elan_home = os.environ.get("ELAN_HOME", os.path.expanduser(r"~\.elan"))
    return os.path.join(elan_home, "bin", "lake.exe")


_lean_env_cache: Optional[Dict[str, str]] = None
_lean_env_lock = threading.Lock()
_warmup_state = {"status": "NOT_STARTED", "elapsed_ms": 0.0}


def _lean_env() -> Dict[str, str]:
    """Tính LEAN_PATH của workspace một lần (gọi `lake env` mỗi lần tốn thêm ~20s)."""
    global _lean_env_cache
    with _lean_env_lock:
        if _lean_env_cache is None:
            # Dùng chính Python để in LEAN_PATH: `printenv` chỉ có trong Git Bash/Linux, không có khi chạy từ cmd
            proc = subprocess.run(
                [_lake_bin(), "env", sys.executable, "-c", "import os; print(os.environ.get('LEAN_PATH', ''))"],
                capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=300, cwd=LEAN_PROJECT,
            )
            lean_path = (proc.stdout or "").strip().splitlines()[-1] if proc.returncode == 0 and proc.stdout.strip() else ""
            if not lean_path:
                raise RuntimeError(f"Không lấy được LEAN_PATH từ lake: {(proc.stderr or '').strip()[-500:]}")
            env = os.environ.copy()
            env["LEAN_PATH"] = lean_path
            _lean_env_cache = env
        return _lean_env_cache


def _lean_bin() -> str:
    found = shutil.which("lean")
    if found:
        return found
    return os.path.join(os.path.dirname(_lake_bin()), "lean.exe")


def warmup_mathlib() -> None:
    """Nạp Mathlib một lần để hệ điều hành đệm các file .olean (lần đọc đầu có thể mất vài phút)."""
    if not lean_status()["mathlib_ready"]:
        _warmup_state["status"] = "SKIPPED"
        return
    _warmup_state["status"] = "RUNNING"
    t0 = time.perf_counter()
    try:
        src = "\n".join(f"import {m}" for m in lean_imports()) + "\n#check Real.pi\n"
        res = compile_lean("WARMUP", src, timeout_sec=1800)
        _warmup_state["status"] = "DONE" if res["returncode"] == 0 else "FAILED"
    except Exception:
        _warmup_state["status"] = "FAILED"
    _warmup_state["elapsed_ms"] = round((time.perf_counter() - t0) * 1000.0, 2)


def lean_status() -> Dict[str, Any]:
    olean = os.path.join(LEAN_PROJECT, ".lake", "packages", "mathlib", ".lake", "build", "lib", "lean", "Mathlib.olean")
    return {
        "project": LEAN_PROJECT,
        "mathlib_ready": os.path.exists(olean),
        "lake": _lake_bin(),
        "model": LEAN_MODEL,
        "proof_escalate_model": PROOF_ESCALATE_MODEL,
        "max_attempts": 1 + PROOF_FIXES,
        "statement_fixes": STATEMENT_FIXES,
        "proof_fixes": PROOF_FIXES,
        "statement_fallbacks": STATEMENT_FALLBACKS,
        "statement_rewrites": STATEMENT_REWRITES,
        "warmup": dict(_warmup_state),
        "mathexam_ready": mathexam_ready(),
        "formalize_steps": sorted(FORMALIZE_STEPS),
        "formalize_candidates": NUM_CANDIDATES,
        "formalize_equivalence_check": EQUIV_CHECK,
        "formalize_vacuity_check": VACUITY_CHECK,
        "judge_model": JUDGE_MODEL,
        "require_equivalence": REQUIRE_EQUIV,
        "form_check": FORM_CHECK,
        "extra_candidates": EXTRA_CANDIDATES,
        "auto_prove": AUTO_PROVE,
        "decompose": DECOMPOSE,
        "disprove_fixes": DISPROVE_FIXES,
        "score": {"combine": SCORE_COMBINE, "alpha": SCORE_ALPHA, "embed_model": EMBED_MODEL},
    }


# =============================================================================
# Dịch công thức đáp án SymPy -> thuật ngữ Lean/Mathlib
# =============================================================================

_REAL_FUNCS = {
    sp.exp: "Real.exp", sp.log: "Real.log", sp.sin: "Real.sin", sp.cos: "Real.cos", sp.tan: "Real.tan",
    sp.atan: "Real.arctan", sp.asin: "Real.arcsin", sp.acos: "Real.arccos",
}


def sympy_to_lean(expr: sp.Expr, ty: str, params: List[str]) -> str:
    """ty ∈ {ℝ, ℚ, ℤ, ℕ}. Tham số trong Lean có kiểu ℕ/ℤ nên được ép kiểu sang `ty`."""
    exact = ty in ("ℤ", "ℕ")

    def lit(n: int) -> str:
        if ty == "ℕ" and n < 0:
            raise ValueError("Đáp án kiểu ℕ không được chứa số âm; hãy dùng ℤ hoặc ℝ")
        return f"({n} : {ty})"

    def go(e: sp.Expr) -> str:
        if e.is_Integer:
            return lit(int(e))
        if e.is_Rational:
            if exact:
                raise ValueError(f"Đáp án kiểu {ty} không được chứa phân số: {e}")
            return f"(({e.p} : {ty}) / {e.q})"
        if e.is_Symbol:
            if e.name not in params:
                raise ValueError(f"Biến lạ trong đáp án: {e.name}")
            return f"({e.name} : {ty})"
        if e == sp.pi:
            if ty != "ℝ":
                raise ValueError("π chỉ dùng được với kiểu ℝ")
            return "Real.pi"
        if e == sp.E:
            if ty != "ℝ":
                raise ValueError("e chỉ dùng được với kiểu ℝ")
            return "Real.exp 1"
        if e.is_Add:
            return "(" + " + ".join(go(a) for a in e.args) + ")"
        if e.is_Mul:
            return "(" + " * ".join(go(a) for a in e.args) + ")"
        if e.is_Pow:
            b, k = e.args
            if k.is_Integer and int(k) >= 0:
                return f"({go(b)} ^ ({int(k)} : ℕ))"
            if k.is_Integer and int(k) < 0:
                if exact:
                    raise ValueError(f"Đáp án kiểu {ty} không được chứa lũy thừa âm")
                return f"(({go(b)} ^ ({-int(k)} : ℕ))⁻¹)"
            if ty != "ℝ":
                raise ValueError("Lũy thừa không nguyên chỉ dùng được với kiểu ℝ")
            if k == sp.Rational(1, 2):
                return f"(Real.sqrt {go(b)})"
            if k == sp.Rational(-1, 2):
                return f"((Real.sqrt {go(b)})⁻¹)"
            return f"({go(b)} ^ ({go(k)} : ℝ))"
        if isinstance(e, sp.Abs):
            return f"|{go(e.args[0])}|"
        if isinstance(e, sp.factorial):
            return f"((Nat.factorial {sympy_to_lean(e.args[0], 'ℕ', params)} : ℕ) : {ty})"
        if isinstance(e, sp.binomial):
            n, k = (sympy_to_lean(a, "ℕ", params) for a in e.args)
            return f"((Nat.choose {n} {k} : ℕ) : {ty})"
        for f, name in _REAL_FUNCS.items():
            if isinstance(e, f):
                if ty != "ℝ":
                    raise ValueError(f"{name} chỉ dùng được với kiểu ℝ")
                return f"({name} {go(e.args[0])})"
        raise ValueError(f"Chưa hỗ trợ dịch biểu thức sang Lean: {e}")

    return go(expr)


# =============================================================================
# Lắp file Lean và kiểm tra tĩnh
# =============================================================================

_BANNED = [
    r"\bsorry\b", r"\badmit\b", r"\baxiom\b", r"\bunsafe\b", r"implemented_by", r"@\[\s*extern", r"\bnative_decide\b",
    r"ofReduceBool", r"#exit", r"\bset_option\b", r"\bmacro\b", r"\bmacro_rules\b", r"\bsyntax\b", r"\belab\b",
    r"\bnotation\b", r"\binfixl?r?\b", r"\bprefix\b", r"\bpostfix\b", r"\binstance\b", r"\bdef\b", r"\babbrev\b",
    r"\bopaque\b", r"\bimport\b", r"\brun_cmd\b", r"\brun_tac\b", r"open\s+private", r"\battribute\b",
    r"\bLean\.(Elab|Meta|Parser)\b", r"\bdebug\.", r"\bstructure\b", r"\binductive\b", r"\bclass\b",
    r"\bnoncomputable\b", r"\bvariable\b", r"\bexam_answer\b",
]
_BANNED_RE = re.compile("|".join(_BANNED))
_NAMESPACE_RE = re.compile(r"^[A-Za-z][A-Za-z0-9_.]*$")
_SCOPE_RE = re.compile(r"^\s*(namespace|section|end)\b", re.MULTILINE)


def _strip_comments(code: str) -> str:
    code = re.sub(r"/-.*?-/", " ", code, flags=re.DOTALL)
    return re.sub(r"--[^\n]*", " ", code)


_MODULE_RE = re.compile(r"^(Mathlib|MathExam)(\.[A-Z][A-Za-z0-9_]*)+$")


def _mathlib_module_exists(module: str) -> bool:
    if module.startswith("MathExam."):
        return mathexam_ready() and os.path.exists(os.path.join(LEAN_PROJECT, *module.split(".")) + ".lean")
    src = os.path.join(LEAN_PROJECT, ".lake", "packages", "mathlib", *module.split(".")) + ".lean"
    return os.path.exists(src)


def _static_check(form: Dict[str, Any], needs_answer: bool = True) -> None:
    extra = form.get("extra_imports", [])
    if len(extra) > MAX_EXTRA_IMPORTS:
        raise ValueError(f"Tối đa {MAX_EXTRA_IMPORTS} module import thêm")
    for mod in extra:
        if not _MODULE_RE.match(mod) or not _mathlib_module_exists(mod):
            raise ValueError(f"Module import không hợp lệ hoặc không tồn tại trong Mathlib: {mod!r}")
    for ns in form["open_namespaces"]:
        if not _NAMESPACE_RE.match(ns):
            raise ValueError(f"Tên namespace không hợp lệ: {ns!r}")
    if needs_answer and "ANSWER" not in form["statement"]:
        raise ValueError("Mệnh đề phải chứa chỗ trống ANSWER tại vị trí đáp án")
    for part in ("helper_lemmas", "statement", "proof"):
        hit = _BANNED_RE.search(_strip_comments(form[part]))
        if hit:
            raise ValueError(f"Phần {part} dùng cấu trúc bị cấm: {hit.group(0)!r}")
    if ":=" in _strip_comments(form["statement"]):
        raise ValueError("Phần statement chỉ là mệnh đề, không chứa ':='")
    # Các ứng viên được biên dịch chung một file, mỗi ứng viên trong namespace riêng: không cho tự mở/đóng scope
    for part in ("helper_lemmas", "statement", "proof"):
        if _SCOPE_RE.search(_strip_comments(form[part])):
            raise ValueError(f"Phần {part} không được dùng namespace/section/end")


def param_binders(params: List[Dict[str, Any]]) -> str:
    """Biến và giả thiết miền của các tham số nguyên, do hệ thống đặt (LLM không sửa được)."""
    binders = []
    for p in params:
        ty = "ℕ" if int(p.get("min", 0)) >= 0 else "ℤ"
        n = p["name"]
        binders.append(f"({n} : {ty}) (h{n}_lo : {int(p['min'])} ≤ {n}) (h{n}_hi : {n} ≤ {int(p['max'])})")
    return " ".join(binders)


def param_domain_note(params: List[Dict[str, Any]]) -> str:
    return ", ".join(f"{p['name']} ∈ [{p.get('min')}, {p.get('max')}] (nguyên)" for p in params) or "không có"


_PARAM_BINDER_RE = re.compile(r"\(\s*([^\s:()]+)\s*:\s*[ℕℤ]\s*\)")
_QUANT_BINDER_RE = re.compile(r"(?<![\w.])(?:∀|∃!?|fun|λ)\s+(.+?)\s*(?:,|=>|↦)", re.DOTALL)
_SET_BINDER_RE = re.compile(r"\{\s*([^{}|]+?)\s*\|")


def _ident_re(name: str) -> "re.Pattern[str]":
    return re.compile(rf"(?<![\w'.₀-₉]){re.escape(name)}(?![\w'₀-₉])")


def _bound_names(part: str) -> List[str]:
    """Tên do một lượng từ / fun / tập {x | …} đưa vào (không tính tên nằm trong kiểu, ví dụ m trong `i : Fin m`)."""
    groups = re.findall(r"[(⦃{\[]\s*([^:()⦃⦄{}\[\]]+?)\s*:", part)
    if groups:
        return " ".join(groups).split()
    return re.split(r"[:∈∉<>≤≥≠]", part)[0].split()


def _param_problems(statement: str, params: List[str]) -> List[str]:
    """QT17: tham số do hệ thống cố định (header) phải được mệnh đề dùng (ngoài chỗ ANSWER) và không bị khai báo lại.
    Mệnh đề không dùng m (ví dụ thay m bằng một số cụ thể) hoặc khai báo lại m (∀ m / ∃ m / fun m / {m | …}, che tham
    số của header) thì không còn là bài toán có tham số mà hệ thống đã kiểm đáp án."""
    s = _strip_comments(statement)
    problems = []
    for p in params:
        rx = _ident_re(p)
        if not rx.search(s.replace("ANSWER", " ")):
            problems.append(f"mệnh đề không dùng tham số {p} do hệ thống cố định trong header (ngoài chỗ ANSWER): viết "
                            f"({p} : ℝ) đúng chỗ đề dùng {p}, không thay {p} bằng một số cụ thể")
            continue
        bound = [n for m in _QUANT_BINDER_RE.finditer(s) for n in _bound_names(m.group(1))]
        bound += [n for m in _SET_BINDER_RE.finditer(s) for n in re.split(r"[:∈]", m.group(1))[0].split()]
        if p in bound:
            problems.append(f"không được khai báo lại tham số {p} (∀ {p} / ∃ {p} / fun {p} / {{{p} | …}}): {p} đã được "
                            f"header cố định, khai báo lại sẽ che tham số đó; đặt tên khác cho biến mới")
    return problems


@dataclass
class FormalTask:
    """Một phát biểu tiếng Việt cần hình thức hóa (FR08) và chứng minh (FR09), kèm phần do hệ thống cố định (QT17).
    Với câu hỏi: binders là tham số và miền, answer_expr là đáp án đã qua kiểm đáp án, được điền vào chỗ ANSWER."""

    code: str  # mã dùng đặt tên file Lean và ghi nhật ký
    text_vi: str  # phát biểu tiếng Việt
    binders: str = ""  # biến và giả thiết cố định, ví dụ "(m : ℕ) (hm_lo : 2 ≤ m) (hm_hi : m ≤ 9)"
    domain_note: str = "không có"  # mô tả tham số và miền cho bước chuẩn hóa đề
    answer_sympy: Optional[str] = None  # đáp án (SymPy) hệ thống điền vào ANSWER; None nếu phát biểu không có đáp số
    answer_expr: Optional[sp.Expr] = None
    answer_vars: List[str] = field(default_factory=list)
    hint: str = ""  # lời giải tham khảo cho lượt viết chứng minh

    @property
    def header(self) -> str:
        return f"theorem {THEOREM_NAME} {self.binders} :"

    @property
    def needs_answer(self) -> bool:
        return self.answer_expr is not None

    @property
    def param_names(self) -> List[str]:
        """Tên các tham số nguyên do hệ thống cố định trong header (không tính giả thiết miền)."""
        return _PARAM_BINDER_RE.findall(self.binders)

    def answer_term(self, answer_type: str) -> Optional[str]:
        return sympy_to_lean(self.answer_expr, answer_type, self.answer_vars) if self.needs_answer else None

    def fill(self, statement: str, term: Optional[str]) -> str:
        return statement if term is None else statement.replace("ANSWER", f"({term})")


_INFRA_ERROR_RE = re.compile(r"failed to read file '[^']*\.olean")


def compile_lean(question_code: str, lean_code: str, timeout_sec: Optional[int] = None) -> Dict[str, Any]:
    os.makedirs(MATHLIB_OUT_DIR, exist_ok=True)
    safe = re.sub(r"[^A-Za-z0-9_\-]", "_", question_code)
    path = os.path.join(MATHLIB_OUT_DIR, f"{safe}.lean")
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(lean_code)

    timeout_sec = timeout_sec or LEAN_TIMEOUT_SEC
    t0 = time.perf_counter()
    level = getattr(_priority_local, "level", None)
    with _lean_gate.slot(PRIORITY_FR01 if level is None else level):
        for retry in range(3):
            try:
                proc = subprocess.run(
                    [_lean_bin(), path],
                    capture_output=True, text=True, encoding="utf-8", errors="replace",
                    timeout=timeout_sec, cwd=LEAN_PROJECT, env=_lean_env(),
                )
                out = "\n".join(filter(None, [(proc.stdout or "").strip(), (proc.stderr or "").strip()]))
                rc = proc.returncode
            except subprocess.TimeoutExpired:
                out, rc = f"Lean vượt thời gian {timeout_sec}s", -1
            # "failed to read file ....olean" là lỗi hạ tầng (thiếu bộ nhớ khi nạp Mathlib), không phải lỗi chứng minh
            infra_error = bool(_INFRA_ERROR_RE.search(out))
            if not infra_error:
                break
            time.sleep(5 * (retry + 1))
    elapsed = round((time.perf_counter() - t0) * 1000.0, 2)

    axioms_line = re.search(rf"'{THEOREM_NAME}' depends on axioms: \[(.*?)\]", out, re.DOTALL)
    no_axioms = f"'{THEOREM_NAME}' does not depend on any axioms" in out
    used = {a.strip() for a in axioms_line.group(1).split(",")} if axioms_line else set()
    problems = []
    if infra_error:
        problems.append("lỗi hệ thống khi nạp Mathlib (thiếu bộ nhớ?)")
    if rc != 0:
        problems.append("biên dịch lỗi")
    if "declaration uses 'sorry'" in out:
        problems.append("chứng minh dùng sorry")
    if not (axioms_line or no_axioms) and rc == 0:
        problems.append("không đọc được kết quả #print axioms")
    if used - ALLOWED_AXIOMS:
        problems.append(f"dùng tiên đề ngoài chuẩn: {sorted(used - ALLOWED_AXIOMS)}")
    return {
        "ok": not problems,
        "problems": problems,
        "returncode": rc,
        "infra_error": infra_error,
        "output": out,
        "axioms": sorted(used),
        "elapsed_ms": elapsed,
        "file_path": path,
    }


# =============================================================================
# Cấu hình quy trình cải thiện formalize (4 bước)
# =============================================================================
# Bước 1: chuẩn hóa đề tiếng Việt thành dạng có cấu trúc.
# Bước 2: tách đề thành khái niệm con, truy xuất định nghĩa + định lý minh họa (lean_retrieval).
# Bước 3: LLM suy luận ánh xạ khái niệm -> Lean (trường `analysis`) trước khi viết mệnh đề.
# Bước 4: sinh nhiều ứng viên, lọc bằng biên dịch Lean, sửa theo thông báo lỗi, chọn theo đồng thuận.
# Tắt cả 4 bước (MATH_FORMALIZE_STEPS="") cho đúng quy trình gốc: 1 ứng viên, hướng dẫn tĩnh, sửa tuần tự.

FORMALIZE_STEPS = frozenset(
    int(s) for s in os.environ.get("MATH_FORMALIZE_STEPS", "1,2,3,4").replace(" ", "").split(",") if s
)
NUM_CANDIDATES = int(os.environ.get("MATH_FORMALIZE_CANDIDATES", "3"))
EQUIV_CHECK = os.environ.get("MATH_FORMALIZE_EQUIV", "1") == "1"


# =============================================================================
# Prompt
# =============================================================================

_ANALYSIS_SCHEMA: Dict[str, Any] = {
    "type": "array",
    "items": {
        "type": "object",
        "properties": {
            "doi_tuong": {"type": "string"},
            "lean": {"type": "string"},
            "ghi_chu": {"type": "string"},
        },
        "required": ["doi_tuong", "lean", "ghi_chu"],
        "additionalProperties": False,
    },
}


def _statement_schema(with_analysis: bool) -> Dict[str, Any]:
    """Giai đoạn A: chỉ mệnh đề (không chứng minh)."""
    props: Dict[str, Any] = {}
    if with_analysis:
        props["analysis"] = _ANALYSIS_SCHEMA  # đặt TRƯỚC statement: LLM điền bảng ánh xạ rồi mới viết mệnh đề
    props.update({
        "extra_imports": {"type": "array", "items": {"type": "string"}},
        "open_namespaces": {"type": "array", "items": {"type": "string"}},
        "answer_type": {"type": "string", "enum": ["ℝ", "ℚ", "ℤ", "ℕ"]},
        "statement": {"type": "string"},
    })
    return {"type": "object", "properties": props, "required": list(props), "additionalProperties": False}


STATEMENT_KINDS = ["tinh_gia_tri", "tim_tham_so", "bien_luan", "chung_minh", "khac"]

# B1. Phân tích đề thành bảng năm phần (danh sách kiểm tra cho B8). Mỗi mục "đề nói" kèm câu trích nguyên văn để hệ
# thống kiểm có thật trong đề; điều kiện xác định tách riêng vì là phần suy ra, không phải đề nói.
_QUOTED = {"type": "object", "properties": {"noi_dung": {"type": "string"}, "trich": {"type": "string"}},
           "required": ["noi_dung", "trich"], "additionalProperties": False}
NORMALIZE_SCHEMA: Dict[str, Any] = {
    "type": "object",
    "properties": {
        "loai_bai": {"type": "string"},
        "dang_cau": {"type": "string", "enum": STATEMENT_KINDS},
        "luong_tu": {"type": "array", "items": {"type": "object", "properties": {
            "loai": {"type": "string", "enum": ["moi", "ton_tai"]}, "noi_dung": {"type": "string"}, "trich": {"type": "string"}},
            "required": ["loai", "noi_dung", "trich"], "additionalProperties": False}},
        "doi_tuong": {"type": "array", "items": {"type": "object", "properties": {
            "ten": {"type": "string"}, "kieu_va_mien": {"type": "string"},
            "nguon": {"type": "string", "enum": ["de_noi", "suy_ra"]}, "trich": {"type": "string"}},
            "required": ["ten", "kieu_va_mien", "nguon", "trich"], "additionalProperties": False}},
        "gia_thiet": {"type": "array", "items": _QUOTED},
        "dieu_kien_xac_dinh": {"type": "array", "items": {"type": "object", "properties": {
            "noi_dung": {"type": "string"}, "ly_do": {"type": "string"}},
            "required": ["noi_dung", "ly_do"], "additionalProperties": False}},
        "ket_luan": {"type": "array", "items": _QUOTED},
        "an": {"type": "string"},
        "khai_niem": {"type": "array", "items": {"type": "object", "properties": {
            "vi": {"type": "string"}, "lean_keywords": {"type": "array", "items": {"type": "string"}}},
            "required": ["vi", "lean_keywords"], "additionalProperties": False}},
    },
    "required": ["loai_bai", "dang_cau", "luong_tu", "doi_tuong", "gia_thiet", "dieu_kien_xac_dinh", "ket_luan", "an",
                 "khai_niem"],
    "additionalProperties": False,
}

# Quy ước tập số của học phần Giải tích 1 (mục 1.3): đề không nói rõ thì biến, hằng số, hàm và dãy là số thực. Dùng chung
# cho B1, bước viết mệnh đề và giám khảo B8, để bản dịch trên ℝ của một đề không nói tập số không bị coi là thu hẹp đề.
REAL_CONVENTION = ("Quy ước Giải tích 1: khi đề KHÔNG nói rõ tập số, thì biến, tham số, hằng số là số thực (ℝ), hàm số là "
                   "hàm thực (từ ℝ hoặc một tập con của ℝ vào ℝ; hàm nhiều biến từ ℝⁿ vào ℝ), dãy là dãy số thực; chỉ số "
                   "của dãy (n trong s_n) là số tự nhiên. Ký hiệu |x| khi đó là giá trị tuyệt đối. Quy ước này KHÔNG áp "
                   "dụng khi đề nói rõ phạm vi khác (số phức, ℂ, không gian metric, không gian định chuẩn, ℝⁿ, tập bất kỳ, "
                   "số nguyên, số hữu tỉ, …): khi đó giữ đúng phạm vi đề nói.")

NORMALIZE_SYSTEM = """Bạn phân tích một phát biểu toán (đề bài Giải tích, tiếng Việt hoặc tiếng Anh, có LaTeX) thành bảng các phần, làm danh sách kiểm tra cho việc hình thức hóa sang Lean 4 + Mathlib.
KHÔNG giải bài, KHÔNG sửa đề, KHÔNG thêm điều đề không nói (kể cả khi đề có vẻ thiếu giả thiết hoặc sai). Điền:
- loai_bai: dạng bài (ví dụ "tính giới hạn hàm", "tìm tham số để hàm liên tục", "chứng minh hàm hằng").
- dang_cau: tinh_gia_tri (tính một đại lượng: giới hạn, đạo hàm, tích phân, cực trị, ...); tim_tham_so (tìm giá trị của một ẩn/tham số để một tính chất xảy ra, ví dụ "tìm a để f liên tục"); bien_luan (biện luận tính chất theo tham số); chung_minh (chứng minh một khẳng định); khac.
- luong_tu: các lượng từ của phát biểu: loai = moi ("với mọi", "cho", "giả sử f là ...", "for all") hoặc ton_tai ("tồn tại", "có ít nhất một", "there exists"); noi_dung: lượng từ áp lên đối tượng nào.
- doi_tuong: mọi đối tượng (tham số, biến, hàm số, dãy, tập hợp, hằng số) với kiểu và miền (kieu_va_mien, ví dụ "hàm từ ℝ vào ℝ", "số nguyên, 2 ≤ m ≤ 9", "dãy số thực"). nguon = de_noi nếu đề ghi rõ kiểu/miền (kèm trích), suy_ra nếu chỉ suy ra từ ký hiệu hoặc từ quy ước tập số bên dưới (ví dụ chỉ số n của C_n là số tự nhiên; "dãy {s_n}" không nói tập số thì ghi "dãy số thực (quy ước Giải tích 1)"); với suy_ra, trich để chuỗi rỗng. Không tự thêm ràng buộc như n ≥ 1, tập khác rỗng khi đề không nói.
- gia_thiet: từng giả thiết ĐỀ NÓI (điều được cho), mỗi giả thiết một mục.
- dieu_kien_xac_dinh: CHỈ các điều kiện để một biểu thức hay ký hiệu CÓ TRONG ĐỀ có nghĩa thông thường (mẫu số khác 0, đối số của logarit dương, biểu thức dưới căn bậc chẵn không âm, cos ≠ 0 cho tan, đối số arcsin/arccos thuộc [−1, 1], cơ số dương khi số mũ không nguyên, a < b khi đề viết khoảng (a, b) hay đoạn [a, b]); ly_do: biểu thức hay ký hiệu nào cần điều kiện đó. Không đưa giả thiết khác vào đây.
- ket_luan: từng điều đề yêu cầu tính / chứng minh, mỗi ý một mục.
- an: đại lượng cần tìm (chuỗi rỗng nếu là bài chứng minh).
- khai_niem: các khái niệm toán học con (ví dụ "giới hạn khi x → 0", "liên tục tại một điểm", "vô cùng bé tương đương"); lean_keywords là vài từ khóa tiếng Anh/tên Mathlib liên quan (ví dụ "ContinuousAt", "Tendsto", "deriv").
Trường trich (của luong_tu, doi_tuong nguon de_noi, gia_thiet, ket_luan) là câu/cụm CHÉP NGUYÊN VĂN từ đề, gồm TRỌN các công thức liên quan (giữ nguyên LaTeX). Hệ thống kiểm: trích phải có trong đề, và mọi công thức của đề phải nằm trong ít nhất một câu trích.
""" + REAL_CONVENTION

# B8. Giám khảo đối chiếu từng phần bản diễn đạt lại với bảng B1 và liệt kê, phân loại mọi khác biệt.
# Hệ thống (không phải giám khảo) kết luận khớp theo luật JUDGE_ALLOWED.
JUDGE_PARTS = ["luong_tu", "doi_tuong", "gia_thiet", "dieu_kien_xac_dinh", "ket_luan"]
JUDGE_DIFF_KINDS = [
    "dieu_kien_ton_tai", "dieu_kien_xac_dinh", "cach_viet_tuong_duong",
    "gia_thiet_them", "thieu_gia_thiet", "thu_hep_pham_vi", "mo_rong_pham_vi", "luong_tu_khac", "ket_luan_khac",
    "them_y", "thieu_y", "khac",
]
JUDGE_ALLOWED = {"dieu_kien_ton_tai", "dieu_kien_xac_dinh", "cach_viet_tuong_duong"}
JUDGE_SCHEMA: Dict[str, Any] = {
    "type": "object",
    "properties": {
        "doi_chieu": {"type": "array", "items": {"type": "object", "properties": {
            "phan": {"type": "string", "enum": JUDGE_PARTS}, "ban_dien_dat_noi": {"type": "string"},
            "khop": {"type": "boolean"}},
            "required": ["phan", "ban_dien_dat_noi", "khop"], "additionalProperties": False}},
        "khac_biet": {"type": "array", "items": {"type": "object", "properties": {
            "phan": {"type": "string", "enum": JUDGE_PARTS}, "mo_ta": {"type": "string"},
            "loai": {"type": "string", "enum": JUDGE_DIFF_KINDS}},
            "required": ["phan", "mo_ta", "loai"], "additionalProperties": False}},
    },
    "required": ["doi_chieu", "khac_biet"],
    "additionalProperties": False,
}

_BANNED_NOTE = """Cấm tuyệt đối: sorry, admit, axiom, def, abbrev, notation, macro, syntax, instance, set_option, native_decide, import, attribute, noncomputable, variable, structure, namespace, section, end. Không định nghĩa lại khái niệm; mệnh đề phải dùng trực tiếp định nghĩa của Mathlib, hoặc của thư viện MathExam khi Mathlib không có khái niệm tương ứng (VCB bậc k, điểm gián đoạn, đạo hàm riêng, miền tọa độ cực…)."""

STATEMENT_SYSTEM = """Bạn là chuyên gia Lean 4 và Mathlib (Lean 4.35, Mathlib bản tương ứng). Nhiệm vụ: hình thức hóa ĐỀ BÀI của một bài Toán cao cấp thành MỆNH ĐỀ Lean 4 + Mathlib. CHƯA cần chứng minh: hệ thống kiểm tra mệnh đề với chứng minh tạm `sorry`, một lượt khác sẽ viết chứng minh.

Hệ thống đã cố định header định lý (tên, tham số nguyên và giả thiết miền giá trị), ví dụ:
  theorem exam_answer (m : ℕ) (hm_lo : 2 ≤ m) (hm_hi : m ≤ 9) :
Bạn viết:
- statement: MỆNH ĐỀ diễn đạt CHÍNH XÁC bài toán, đặt từ khóa ANSWER đúng chỗ đáp số. Hệ thống sẽ thay ANSWER bằng đáp án có kiểu answer_type (tham số đã được ép kiểu sẵn bên trong ANSWER). Tham số m có kiểu ℕ/ℤ nên khi dùng trong biểu thức thực phải viết (m : ℝ). Mệnh đề phải dùng mọi tham số của header đúng chỗ đề dùng (không thay bằng số cụ thể), và không khai báo lại tham số (∀ m / ∃ m / fun m) vì sẽ che tham số của header.
  Mệnh đề PHẢI ghi đủ điều kiện tồn tại của đại lượng cần tính (QT16): Mathlib gán giá trị quy ước (thường là 0) khi
  đại lượng không tồn tại, nên `deriv f a = L`, `∫ … = L`, `limUnder …`, `tsum …`, `sSup …` đứng một mình có thể
  "chứng minh được" mà vô nghĩa. Hệ thống kiểm tra tự động và trả lại mệnh đề sai dạng. Mẫu theo dạng bài:
  * Giới hạn: Filter.Tendsto (fun x : ℝ => ...) (𝓝[≠] 0) (𝓝 ANSWER)  (cần mở Topology; hoặc atTop). Không dùng limUnder/lim.
    Giới hạn của hàm khi x → a (kể cả trong giả thiết, kể cả hàm nhiều biến) lấy trên lân cận BỎ ĐIỂM: 𝓝[≠] a, một phía
    𝓝[<] a / 𝓝[>] a; KHÔNG viết (𝓝 a) làm lân cận của biến, vì (𝓝 a) gồm cả x = a nên đòi luôn f a = giới hạn (tức là
    liên tục; Lean còn quy ước x/0 = 0). Phát biểu về liên tục thì dùng ContinuousAt f a.
  * Đạo hàm: HasDerivAt (fun x : ℝ => ...) ANSWER a  hoặc  DifferentiableAt ℝ f a ∧ deriv f a = ANSWER
  * Đạo hàm cấp cao: ContDiff ℝ k (fun x : ℝ => ...) ∧ iteratedDeriv k (fun x => ...) a = ANSWER
  * Tích phân xác định: IntervalIntegrable (fun x : ℝ => ...) MeasureTheory.volume a b ∧ ∫ x in (a:ℝ)..b, f x = ANSWER
  * Tích phân suy rộng = giới hạn của tích phân xác định: Filter.Tendsto (fun b : ℝ => ∫ x in (a:ℝ)..b, f x) atTop (𝓝 ANSWER)
  * Chuỗi: HasSum (fun n : ℕ => ...) ANSWER  (không dùng tsum / ∑')
  * Cực trị / GTLN / GTNN: IsGreatest {y | ∃ x, ... ∧ y = f x} ANSWER, IsLeast ..., IsLocalMax f x₀ (không dùng sSup/sInf)
  * Cận trên đúng / cận dưới đúng (sup, inf): IsLUB S ANSWER, IsGLB S ANSWER. Khẳng định về sup/inf không có đáp số thì
    đặt tên cho giá trị: ví dụ "inf A = −sup(−A)" viết ∀ a : ℝ, IsGLB A a ↔ IsLUB (-A) (-a); "sup tồn tại và …" viết
    ∃ s, IsLUB S s ∧ … (không dùng sSup/sInf/iSup/iInf/⨆/⨅)
  * Tìm tham số / biện luận: dạng "khi và chỉ khi" (↔), không chỉ một chiều. Ví dụ "tìm a để f liên tục tại 0" với ẩn a:
    ∀ a : ℝ, ContinuousAt (f a) 0 ↔ a = ANSWER
  * (Khi thư viện MathExam có sẵn) VCB bậc k: MathExam.IsInfinitesimalOfOrder (fun x => ...) 0 ANSWER
  * Gián đoạn: MathExam.IsJumpDiscontinuity f a / IsRemovableDiscontinuity / IsSecondKindDiscontinuity; bước nhảy: MathExam.HasLeftLimit f a L₁ ∧ MathExam.HasRightLimit f a L₂ ∧ L₂ - L₁ = ANSWER
  * Đạo hàm riêng: DifferentiableAt ℝ (fun p : ℝ × ℝ => ...) (x₀, y₀) ∧ MathExam.partialX (fun p : ℝ × ℝ => ...) (x₀, y₀) = ANSWER (cấp hai: ContDiffAt ℝ 2 … ∧ MathExam.partialXY …)
  * Diện tích hình phẳng: (MeasureTheory.volume (regionBetween f g (Set.Icc a b))).toReal = ANSWER hoặc (MeasureTheory.volume (MathExam.polarRegion r α β)).toReal = ANSWER
- answer_type: kiểu của đáp số trong mệnh đề.
- extra_imports: hệ thống đã import sẵn các module Mathlib liệt kê trong prompt (tactic, đạo hàm, tích phân, hàm sơ cấp, giới hạn, chuỗi, ma trận). Chỉ thêm module Mathlib khác (tối đa 6, dạng "Mathlib.X.Y") khi thực sự cần; thường để [].
- open_namespaces: danh sách namespace cần mở (ví dụ ["Real", "Filter", "Topology", "Matrix", "intervalIntegral"]).

""" + _BANNED_NOTE + """
Không được làm mệnh đề yếu hơn hoặc dễ hơn đề bài (ví dụ chỉ phát biểu cho một giá trị m, hay thay bài toán bằng đẳng thức hiển nhiên). Mệnh đề phải đúng với MỌI giá trị tham số thỏa giả thiết.
""" + REAL_CONVENTION

ANALYSIS_INSTRUCTIONS = """
Suy luận trước khi dịch (bắt buộc): điền trường analysis TRƯỚC khi viết statement. Mỗi dòng của analysis ánh xạ một đối tượng / khái niệm của đề sang Lean:
- doi_tuong: đối tượng hoặc khái niệm trong đề (hàm số, tham số, giới hạn, điều kiện, đại lượng cần tìm, ...).
- lean: biểu diễn Lean tương ứng (biểu thức, định nghĩa Mathlib/MathExam sẽ dùng).
- ghi_chu: lý do chọn và bẫy cần tránh (ép kiểu ℕ → ℝ; Lean coi x/0 = 0 nên giới hạn dùng 𝓝[≠]; điều kiện "tìm a để..." cần "↔" thay vì "→";
  miền xác định của log/sqrt; Continuous khác ContinuousAt; ...).
Sau đó viết statement nhất quán với bảng analysis."""

JUDGE_SYSTEM = """Bạn là giám khảo độc lập, kiểm tra một mệnh đề toán đã được hình thức hóa có đúng nghĩa đề hay không. Bạn KHÔNG xem mã Lean; bạn nhận:
(1) phát biểu gốc; (2) bảng phân tích phát biểu gốc theo từng phần (lượng từ, đối tượng và miền, giả thiết, điều kiện xác định, kết luận); bảng có thể sót, nên luôn đối chiếu cả với phát biểu gốc; (3) đáp số hệ thống đã điền vào mệnh đề (nếu có) và miền tham số; (4) bản diễn đạt lại bằng tiếng Việt của mệnh đề Lean (do người khác dịch ngược, chỉ nói đúng những gì mệnh đề Lean nói).
Bạn KHÔNG tự kết luận khớp hay không; hệ thống kết luận từ các khác biệt bạn liệt kê. Hãy điền:
- doi_chieu: với từng phần của bảng (phan), bản diễn đạt lại nói gì về phần đó (ban_dien_dat_noi) và có khớp với đề không (khop).
- khac_biet: MỌI khác biệt giữa bản diễn đạt lại và phát biểu gốc (thừa, thiếu, đổi), mỗi khác biệt một mục, với phan và loai:
  * dieu_kien_ton_tai: thêm điều kiện để đại lượng mà đề nhắc tới tồn tại (khả vi, khả tích, giới hạn tồn tại, cận trên đúng tồn tại); hoặc đề hỏi "tính X" mà bản diễn đạt lại khẳng định "X tồn tại và bằng <đáp số>".
  * dieu_kien_xac_dinh: thêm điều kiện để một biểu thức hay ký hiệu CÓ TRONG ĐỀ có nghĩa thông thường (mẫu số khác 0, đối số logarit dương, biểu thức dưới căn bậc chẵn không âm, a < b khi đề viết khoảng (a, b) hay đoạn [a, b], ...). Các điều như "n ≥ 1", "tập E khác rỗng", "f(0) = 0" KHÔNG thuộc loại này khi đề không có ký hiệu đòi hỏi chúng: chúng là gia_thiet_them.
  * cach_viet_tuong_duong: viết khác nhưng chắc chắn cùng nghĩa (đổi tên biến; đánh số 1..n thay 0..n−1 với cùng nội dung; "x ∈ (a, b)" thay "a < x < b"; ...).
  * gia_thiet_them, thieu_gia_thiet; thu_hep_pham_vi (kiểu, miền hay không gian hẹp hơn đề, ví dụ đề nói dãy trong không gian bất kỳ mà bản diễn đạt chỉ xét dãy số thực); mo_rong_pham_vi; luong_tu_khac (đổi mọi/tồn tại hoặc thứ tự lượng từ); ket_luan_khac (kết luận mạnh hơn hay yếu hơn, chỉ một chiều trong khi đề hỏi "tìm … để" hoặc biện luận); them_y; thieu_y; khac.
Khi phân vân giữa ba loại đầu và các loại còn lại, chọn loại còn lại. Không đánh giá đáp số đúng hay sai (Lean kiểm việc đó). Không có khác biệt thì khac_biet là mảng rỗng.
""" + REAL_CONVENTION + """ Vì vậy, khi đề không nói rõ tập số mà bản diễn đạt lại xét trên số thực theo đúng quy ước này, đó KHÔNG phải khác biệt: phần đó ghi khop = true và không ghi vào khac_biet. Ngược lại, đề nói rõ phạm vi rộng hơn (số phức, không gian metric, …) mà bản diễn đạt lại chỉ xét số thực thì vẫn là thu_hep_pham_vi."""

SKELETON_NOTE = """Các lượt trước chưa chứng minh được trọn vẹn. Lần này hãy viết KHUNG chứng minh: chia thành các bước trung gian dạng
  have h₁ : <khẳng định trung gian> := by sorry
rồi kết thúc chứng minh từ các bước đó (phần kết thúc KHÔNG dùng sorry). `sorry` CHỈ được dùng đúng dạng `:= by sorry` của các bước have, mỗi bước một dòng; mỗi bước nên đủ nhỏ để norm_num, simp, field_simp, linarith, nlinarith, positivity, fun_prop hoặc vài dòng tactic chứng minh được. helper_lemmas không được dùng sorry."""

FILL_NOTE = """Khung chứng minh trong file trên đã được Lean chấp nhận; hệ thống đã tự chứng minh được một số bước bằng tactic tự động, các bước còn `sorry` (danh sách kèm thông báo Lean ở phần lỗi) cần bạn viết chứng minh. Trả lại TOÀN BỘ phần chứng minh (giữ nguyên các bước đã có), thay mọi `sorry` bằng chứng minh thật."""


# -----------------------------------------------------------------------------
# Bước 1 + 2: chuẩn hóa đề và truy xuất
# -----------------------------------------------------------------------------


_MATH_RE = re.compile(r"\$\$(.+?)\$\$|\$(.+?)\$|\\\((.+?)\\\)|\\\[(.+?)\\\]", re.DOTALL)
_EXISTS_HINT_RE = re.compile(r"tồn tại|có ít nhất|there exists?|there is|there are|at least one", re.IGNORECASE)
_FORALL_HINT_RE = re.compile(r"với mọi|\bmọi\b|bất kỳ|for all|for every|for each|for any", re.IGNORECASE)
# Điều kiện xác định hệ thống tự suy ra từ biểu thức trong đề (không cần LLM)
_DEFINEDNESS_HINTS = [
    (re.compile(r"\\ln|\\log|\bln\b|\blog\b"), "đối số của logarit phải dương"),
    (re.compile(r"\\sqrt|√"), "biểu thức dưới dấu căn bậc chẵn phải không âm"),
    (re.compile(r"\\frac|\\dfrac|[^/]/[^/]"), "mẫu số phải khác 0"),
    (re.compile(r"\\tan|\\cot|\btan\b|\bcot\b"), "tan cần cos ≠ 0, cot cần sin ≠ 0"),
    (re.compile(r"\\arcsin|\\arccos|\barcsin\b|\barccos\b"), "đối số của arcsin, arccos phải thuộc [−1, 1]"),
]


def _squash(s: str) -> str:
    return re.sub(r"\s+|\$|\\[()\[\]]", "", s).lower()


def _definedness_hints(text: str) -> List[str]:
    return [msg for pat, msg in _DEFINEDNESS_HINTS if pat.search(text)]


def _analysis_problems(text: str, norm: Dict[str, Any]) -> List[str]:
    """Kiểm bảng B1 bằng máy: câu trích có thật trong đề, mọi công thức của đề được xếp vào một phần, lượng từ khớp từ
    khóa của đề, có kết luận."""
    src = _squash(text)
    quotes = [x["trich"] for part in ("luong_tu", "gia_thiet", "ket_luan") for x in norm[part]]
    quotes += [d["trich"] for d in norm["doi_tuong"] if d["nguon"] == "de_noi"]
    problems = []
    for q in quotes:
        if not q.strip():
            problems.append("có mục 'đề nói' thiếu câu trích nguyên văn")
        elif _squash(q) not in src:
            problems.append(f"câu trích không có nguyên văn trong đề: {q[:100]!r}")
    squashed = [_squash(q) for q in quotes]
    for m in _MATH_RE.finditer(text):
        seg = _squash(next(g for g in m.groups() if g))
        if seg and not any(seg in q for q in squashed):
            problems.append(f"công thức chưa được trích vào phần nào: {m.group(0)[:100]!r}")
    kinds = {x["loai"] for x in norm["luong_tu"]}
    if _EXISTS_HINT_RE.search(text) and "ton_tai" not in kinds:
        problems.append("đề có 'tồn tại / có ít nhất' nhưng bảng không có lượng từ tồn tại")
    if _FORALL_HINT_RE.search(text) and "moi" not in kinds:
        problems.append("đề có 'với mọi / bất kỳ' nhưng bảng không có lượng từ với mọi")
    if not norm["ket_luan"]:
        problems.append("bảng chưa có kết luận")
    return problems


def normalize_problem(task: FormalTask, run: Optional["CoreRun"] = None) -> Dict[str, Any]:
    """B1: phân tích đề thành bảng năm phần (không giải bài). Bảng được kiểm bằng máy (_analysis_problems); chưa đạt thì
    NORMALIZE_MODEL làm lại một lần, rồi một lần bằng JUDGE_MODEL. Hết lượt (hoặc hết hạn mức FR08 của run) vẫn
    chưa đạt thì giữ bảng cuối kèm danh sách lỗi (giám khảo B8 vẫn đối chiếu với đề gốc)."""
    base = f"Đề bài:\n{task.text_vi}\n\nTham số và miền giá trị (do hệ thống cố định): {task.domain_note}"
    problems: List[str] = []
    norm: Dict[str, Any] = {}
    for attempt, model in enumerate((NORMALIZE_MODEL, NORMALIZE_MODEL, JUDGE_MODEL), 1):
        if run is not None:
            if attempt > 1 and run.fr08_left(FR08_RESERVE) < 1:
                run.fr08_limited = True
                attempt -= 1
                break
            run.fr08_calls += 1
        user = base if not problems else (base + "\n\nBảng lần trước chưa đạt kiểm tra của hệ thống:\n- "
                                          + "\n- ".join(problems) + "\nHãy lập lại toàn bộ bảng.")
        norm = _call_structured(NORMALIZE_SYSTEM, user, NORMALIZE_SCHEMA, model=model)
        problems = _analysis_problems(task.text_vi, norm)
        if not problems:
            break
    norm["kiem_tra"] = {"so_lan": attempt, "loi_con_lai": problems}
    norm["dieu_kien_he_thong"] = _definedness_hints(task.text_vi)
    return norm


def _render_normalized(norm: Dict[str, Any]) -> str:
    """Bảng B1 dạng văn bản: đưa cho lượt viết mệnh đề (B3) và cho giám khảo (B8)."""
    lines = ["Bảng phân tích đề (B1):", f"- Dạng bài: {norm['loai_bai']} (dạng câu: {norm.get('dang_cau', 'khac')})"]
    lines.append("- Lượng từ: " + ("; ".join(f"[{'mọi' if x['loai'] == 'moi' else 'tồn tại'}] {x['noi_dung']}"
                                            for x in norm["luong_tu"]) or "không có"))
    lines.append("- Đối tượng và miền: " + ("; ".join(
        f"{d['ten']}: {d['kieu_va_mien']} ({'đề nói' if d['nguon'] == 'de_noi' else 'suy ra từ ký hiệu'})"
        for d in norm["doi_tuong"]) or "không có"))
    lines.append("- Giả thiết đề nói (chỉ những điều sau): " + ("; ".join(
        f"({i}) {x['noi_dung']}" for i, x in enumerate(norm["gia_thiet"], 1)) or "không có"))
    cond = [f"{x['noi_dung']} ({x['ly_do']})" for x in norm["dieu_kien_xac_dinh"]] + norm.get("dieu_kien_he_thong", [])
    lines.append("- Điều kiện xác định (suy ra từ biểu thức trong đề): " + ("; ".join(cond) or "không có"))
    lines.append("- Kết luận: " + ("; ".join(f"({i}) {x['noi_dung']}" for i, x in enumerate(norm["ket_luan"], 1))
                                 or "không có"))
    if norm["an"]:
        lines.append(f"- Đại lượng cần tìm: {norm['an']}")
    if norm["khai_niem"]:
        lines.append("- Khái niệm con: " + "; ".join(c["vi"] for c in norm["khai_niem"]))
    lines.append("Tập số: đối tượng nào đề không nói rõ tập số thì theo quy ước Giải tích 1 là số thực (dãy số thực, "
                 "hàm thực).")
    lines.append("Mệnh đề chỉ được có các giả thiết trên, cộng điều kiện tồn tại và điều kiện xác định; không thêm "
                 "giả thiết, không thu hẹp hay mở rộng miền của đối tượng.")
    return "\n".join(lines)


def _retrieval_context(task: FormalTask, norm: Optional[Dict[str, Any]]) -> Tuple[str, int]:
    """Bước 2: truy xuất định nghĩa + định lý minh họa cho các khái niệm con. Trả về (đoạn prompt, số mục)."""
    import lean_retrieval

    concepts = norm["khai_niem"] if norm else []
    res = lean_retrieval.retrieve(concepts, task.text_vi)
    return lean_retrieval.format_context(res, lean_imports()), len(res["items"])


def _context_parts(context: Dict[str, str]) -> List[str]:
    parts = []
    if context.get("normalized"):
        parts.append(context["normalized"])
    if context.get("retrieved"):
        parts.append(context["retrieved"])
    elif mathexam_ready():
        parts.append(MATHEXAM_GUIDE)
    return parts


def _previous_part(previous: Optional[Tuple[str, str]], what: str) -> List[str]:
    if not previous:
        return []
    code, err = previous
    return [f"Lần trước {what} thất bại. File Lean đã thử:\n```lean\n" + code[-6000:] + "\n```\n"
            "Lỗi / nhận xét:\n" + err[-4000:] + "\nHãy sửa và trả lại toàn bộ các trường."]


NO_ANSWER_NOTE = """Phát biểu này là một khẳng định cần chứng minh, KHÔNG có đáp số: không dùng ANSWER, bỏ qua answer_type (chọn ℝ). Header không khai báo biến nào ngoài phần đã ghi, nên mệnh đề phải tự lượng hóa mọi đối tượng của đề (ví dụ ∀ f : ℝ → ℝ, giả thiết → kết luận; hoặc ∃ … khi đề khẳng định tồn tại). Không định nghĩa đối tượng bằng def: mô tả bằng giả thiết (ví dụ dãy truy hồi: ∀ s : ℕ → ℝ, s 0 = … → (∀ n, s (n + 1) = …) → …)."""


def _statement_prompt(task: FormalTask, previous: Optional[Tuple[str, str]], context: Dict[str, str]) -> str:
    """Giai đoạn A: chỉ cần hiểu đề (không gửi lời giải để prompt ngắn hơn)."""
    parts = [
        f"Đề bài:\n{task.text_vi}",
        f"Đáp số (SymPy) mà hệ thống sẽ điền vào ANSWER: {task.answer_sympy}" if task.needs_answer else NO_ANSWER_NOTE,
        "Header cố định:\n" + task.header,
        "Các module đã import sẵn: " + ", ".join(lean_imports()),
        *_context_parts(context),
        *_previous_part(previous, "mệnh đề"),
    ]
    return "\n\n".join(parts)


# -----------------------------------------------------------------------------
# Biên dịch nhiều ứng viên mệnh đề trong MỘT file (Mathlib chỉ nạp một lần)
# -----------------------------------------------------------------------------

_MSG_HEAD_RE = re.compile(r"^(?:[A-Za-z]:)?[^:\n]*\.lean:(\d+):(\d+): (error|warning|info)", re.MULTILINE)


def _split_messages(out: str) -> List[Tuple[int, str, str]]:
    """Tách output Lean thành các thông báo (dòng, mức độ, nội dung)."""
    heads = list(_MSG_HEAD_RE.finditer(out))
    msgs = []
    for i, h in enumerate(heads):
        end = heads[i + 1].start() if i + 1 < len(heads) else len(out)
        msgs.append((int(h.group(1)), h.group(3), out[h.start():end].strip()))
    return msgs


def _candidate_block(i: int, task: FormalTask, form: Dict[str, Any], answer_term: Optional[str]) -> str:
    statement = task.fill(form["statement"], answer_term)
    opens = " ".join(dict.fromkeys(form["open_namespaces"]))
    proof = "\n".join("  " + ln for ln in form["proof"].strip().splitlines())
    return "\n".join([
        f"namespace Cand{i}",
        f"open {opens}" if opens else "",
        form["helper_lemmas"].strip(),
        "",
        task.header,
        f"    {statement.strip()} := by",
        proof,
        "",
        f"end Cand{i}",
        f"#print axioms Cand{i}.{THEOREM_NAME}",
    ])


def compile_candidates(question_code: str, task: FormalTask,
                       cands: List[Tuple[int, Dict[str, Any], Optional[str]]], allow_sorry: bool = False,
                       vacuity: bool = False, auto: bool = False) -> Dict[int, Dict[str, Any]]:
    """Biên dịch các ứng viên (chỉ số, form, answer_term) trong một file; trả kết quả riêng cho từng ứng viên.
    allow_sorry: chỉ kiểm tra mệnh đề (chứng minh tạm `sorry` do hệ thống đặt), bỏ qua kiểm tra sorry/tiên đề.
    vacuity: thêm vào CÙNG file phép thử chứng minh False từ giả thiết của từng mệnh đề (đỡ một lần nạp Mathlib);
    kết quả ở trường "vacuous".
    auto: thêm vào CÙNG file phép thử chứng minh từng mệnh đề bằng tactic tự động (bước rẻ nhất của FR09);
    kết quả ở trường "auto_ok"."""
    imports = list(dict.fromkeys(lean_imports() + [m for _, f, _ in cands for m in f.get("extra_imports", [])]))
    lines = [f"-- {question_code}: {len(cands)} ứng viên formalize, biên dịch chung một file.",
             *[f"import {m}" for m in imports], "set_option autoImplicit false", ""]
    ranges: Dict[int, Tuple[int, int]] = {}
    vac_ranges: Dict[int, Tuple[int, int]] = {}
    for i, form, term in cands:
        start = len(lines) + 1
        lines.extend(_candidate_block(i, task, form, term).split("\n"))
        ranges[i] = (start, len(lines))
        lines.append("")
    if vacuity:
        for i, form, term in cands:
            start = len(lines) + 1
            opens = " ".join(dict.fromkeys(form["open_namespaces"]))
            stmt = task.fill(form["statement"], term)
            lines += [f"section Vac{i}", f"open {opens}" if opens else "",
                      f"theorem vacuity_{i} {task.binders} :", f"    {stmt.strip()} := by", *_VACUITY_PROOF,
                      f"end Vac{i}", ""]
            vac_ranges[i] = (start, len(lines))
    auto_ranges: Dict[int, Tuple[int, int]] = {}
    if auto:
        for i, form, term in cands:
            start = len(lines) + 1
            opens = " ".join(dict.fromkeys(form["open_namespaces"]))
            stmt = task.fill(form["statement"], term)
            lines += [f"section Auto{i}", f"open {opens}" if opens else "",
                      f"theorem auto_{i} {task.binders} :", f"    {stmt.strip()} := by",
                      *["  " + ln for ln in AUTO_PROOF.split("\n")], f"end Auto{i}", ""]
            auto_ranges[i] = (start, len(lines))
    res = compile_lean(f"{question_code}-CANDIDATES", "\n".join(lines) + "\n")
    out = res["output"]
    msgs = _split_messages(out)
    results: Dict[int, Dict[str, Any]] = {}
    for i, (lo, hi) in ranges.items():
        mine = [m for m in msgs if lo <= m[0] <= hi]
        errors = [m for m in mine if m[1] == "error"]
        problems = []
        if errors:
            problems.append("biên dịch lỗi")
        ax = re.search(rf"'Cand{i}\.{THEOREM_NAME}' depends on axioms: \[(.*?)\]", out, re.DOTALL)
        no_ax = f"'Cand{i}.{THEOREM_NAME}' does not depend on any axioms" in out
        used = {a.strip() for a in ax.group(1).split(",")} if ax else set()
        if not allow_sorry:
            if any("declaration uses 'sorry'" in m[2] for m in mine):
                problems.append("chứng minh dùng sorry")
            if not errors and not (ax or no_ax):
                problems.append("không đọc được kết quả #print axioms")
            if used - ALLOWED_AXIOMS:
                problems.append(f"dùng tiên đề ngoài chuẩn: {sorted(used - ALLOWED_AXIOMS)}")
        # Đổi số dòng về vị trí trong khối của ứng viên để LLM sửa dễ
        local = "\n".join(re.sub(r"^.*?\.lean:(\d+):", lambda mm: f"dòng {int(mm.group(1)) - lo + 1}:", m[2], count=1)
                          for m in mine if m[1] != "info")
        results[i] = {"ok": not problems and not res["infra_error"], "problems": problems, "errors": local,
                      "axioms": sorted(used), "block": "\n".join(lines[lo - 1:hi])}
        if i in vac_ranges:
            vlo, vhi = vac_ranges[i]
            bad = [m for m in msgs if vlo <= m[0] <= vhi and (m[1] == "error" or "declaration uses 'sorry'" in m[2])]
            results[i]["vacuous"] = not bad and not res["infra_error"]
        if i in auto_ranges:
            alo, ahi = auto_ranges[i]
            bad = [m for m in msgs if alo <= m[0] <= ahi and (m[1] == "error" or "declaration uses 'sorry'" in m[2])]
            results[i]["auto_ok"] = not bad and not res["infra_error"]
    for r in results.values():
        r["infra_error"] = res["infra_error"]
        r["elapsed_ms"] = res["elapsed_ms"]
    return results


def _numbered(block: str) -> str:
    return "\n".join(f"{n:>3}| {ln}" for n, ln in enumerate(block.split("\n"), 1))


# -----------------------------------------------------------------------------
# Bước 4: chọn ứng viên theo Li và cộng sự (NeurIPS 2024), điều chỉnh cho Lean
#   (B1) loại mệnh đề có giả thiết mâu thuẫn: intros rồi thử chứng minh False;
#   (B2) chuẩn hóa tên biến: không cần, vì header/tham số do hệ thống cố định, đáp số khóa qua ANSWER,
#        và Lean coi các biến ràng buộc khác tên (fun x / fun t) là như nhau;
#   (B3) gom nhóm tương đương: chứng minh mệnh đề_i ↔ mệnh đề_j bằng các tactic tự động của Lean
#        (thay cho 12 tactic Isabelle và Z3/CVC5 của bài gốc);
#   điểm ký hiệu = kích thước nhóm; điểm ngữ nghĩa = cos(BERT(dịch ngược), BERT(đề gốc));
#   chuẩn hóa chia tổng; kết hợp tuyến tính / bình phương / logarit với hệ số α.
# -----------------------------------------------------------------------------

VACUITY_CHECK = os.environ.get("MATH_FORMALIZE_VACUITY", "1") == "1"
SCORE_ALPHA = float(os.environ.get("MATH_SCORE_ALPHA", "0.5"))
SCORE_COMBINE = os.environ.get("MATH_SCORE_COMBINE", "log")  # log | linear | square
EMBED_MODEL = os.environ.get("MATH_EMBED_MODEL", "sentence-transformers/LaBSE")
os.environ.setdefault("HF_HOME", os.environ.get("MATH_HF_HOME", r"D:\hf_cache"))

# Tactic tự động thay cho bộ tactic Isabelle (auto, simp, linarith, ...) của bài gốc
_AUTO_TACTICS = ["simp_all", "linarith", "nlinarith", "norm_num at *", "tauto", "aesop"]
_VACUITY_PROOF = ["  intros", "  exfalso", "  first", *[f"    | ({t}; done)" for t in _AUTO_TACTICS]]
_EQUIV_PROOF = [
    "  first",
    "    | exact Iff.rfl",
    "    | (simp; done)",
    "    | (constructor <;> intro h <;> first | (simpa using h)"
    + "".join(f" | ({t}; done)" for t in _AUTO_TACTICS) + ")",
]

# FR09 bước rẻ nhất: tactic tự động chứng minh mệnh đề (hoặc một bước trung gian) mà không gọi LLM
AUTO_PROVE_TACTICS = [
    "norm_num", "simp", "field_simp", "ring_nf", "positivity", "fun_prop", "linarith", "nlinarith", "aesop",
    "constructor <;> first | fun_prop | (norm_num; done) | (simp; done)",
]
AUTO_PROOF = "\n".join(["first", *[f"  | ({t}; done)" for t in AUTO_PROVE_TACTICS]])
_AUTO_INLINE = "(first " + " ".join(f"| ({t}; done)" for t in AUTO_PROVE_TACTICS) + ")"


# -----------------------------------------------------------------------------
# Điều kiện (3) của QT15: mệnh đề đúng dạng theo QT16 (kiểm bằng luật, không gọi LLM)
# -----------------------------------------------------------------------------

_EXISTENCE_RULES: List[Tuple["re.Pattern[str]", Optional["re.Pattern[str]"], str]] = [
    (re.compile(r"\blimUnder\b|\bFilter\.lim\b|(?<![\w.])lim\b"), None,
     "giới hạn phải viết bằng Filter.Tendsto … (𝓝 L); limUnder/lim cho giá trị quy ước khi giới hạn không tồn tại"),
    (re.compile(r"(?<![\w.])f?deriv\b|\bMathExam\.partial(X|Y|XX|XY|YX|YY)\b"),
     re.compile(r"\bHas(Strict)?F?DerivAt\b|\bHasDerivWithinAt\b|\bDifferentiable(At|On)?\b|\bContDiff(At|On)?\b"),
     "deriv/fderiv/đạo hàm riêng cho 0 khi hàm không khả vi: thêm điều kiện khả vi (DifferentiableAt ℝ f a ∧ …) "
     "hoặc dùng HasDerivAt f L a"),
    (re.compile(r"\biteratedF?Deriv\b"), re.compile(r"\bContDiff(At|On)?\b"),
     "đạo hàm cấp cao: thêm điều kiện ContDiff ℝ k f (hoặc ContDiffAt)"),
    (re.compile(r"∫[^,]*?\bin\b\s*(Set\.)?(Ioi|Ici|Iio|Iic|univ)\b"), None,
     "tích phân suy rộng phải viết là giới hạn của tích phân xác định (QT16c): "
     "Filter.Tendsto (fun b => ∫ x in a..b, f x) atTop (𝓝 L)"),
    (re.compile(r"∫[^,]*?\bin\b[^,]*?\.\."),
     re.compile(r"\bIntervalIntegrable\b|\bIntegrableOn\b|\bIntegrable\b|\bContinuous(On)?\b|\bTendsto\b"),
     "tích phân xác định cho 0 khi hàm không khả tích: thêm IntervalIntegrable f MeasureTheory.volume a b ∧ …"),
    (re.compile(r"\btsum\b|∑'"), re.compile(r"\bSummable\b"), "tsum/∑' cho 0 khi chuỗi phân kỳ: dùng HasSum f L"),
    (re.compile(r"\bsSup\b|\bsInf\b|\biSup\b|\biInf\b|⨆|⨅"), None,
     "sup/inf cho giá trị quy ước khi không tồn tại: dùng IsGreatest / IsLeast / IsLUB / IsGLB"),
]
_KIND_HINT_RE = re.compile(r"biện luận|sao cho|tìm[^.\n]{0,60}?\bđể\b|điều kiện (cần và đủ|để)", re.IGNORECASE)


def _statement_kind(task: FormalTask, norm: Optional[Dict[str, Any]]) -> str:
    """Dạng câu (QT16b): lấy từ bước chuẩn hóa đề; bước chuẩn hóa tắt hoặc lỗi thì đoán theo từ khóa của đề."""
    if norm and norm.get("dang_cau") in STATEMENT_KINDS:
        return norm["dang_cau"]
    return "tim_tham_so" if _KIND_HINT_RE.search(task.text_vi) else "khac"


_TENDSTO_RE = re.compile(r"(?<![\w.])(?:Filter\.)?Tendsto(?![\w'])")
_OPENERS, _CLOSERS = "([{⟨", ")]}⟩"
_NHDS_RE = re.compile(r"^(?:𝓝|nhds)\s+(.+)$", re.DOTALL)  # (𝓝 a), không khớp (𝓝[≠] a), (𝓝[>] a), nhdsWithin
_FUN_RE = re.compile(r"^(?:fun|λ)\s+([^\s:=>↦,]+)(?:\s*:[^=↦]*?)?\s*(?:=>|↦)\s*(.+)$", re.DOTALL)
PUNCTURED_MSG = ("giới hạn của hàm khi x → a phải lấy trên lân cận bỏ điểm (QT16c): Filter.Tendsto f (𝓝[≠] a) (𝓝 L), "
                 "một phía 𝓝[<] a / 𝓝[>] a. (𝓝 a) gồm cả x = a nên đòi f a = L, tức là liên tục, mạnh hơn đề (Lean còn "
                 "quy ước x/0 = 0). Phát biểu về liên tục thì dùng ContinuousAt f a")


def _lean_args(s: str, pos: int, n: int) -> List[str]:
    """Đọc tối đa n đối số liên tiếp của một hàm Lean bắt đầu từ vị trí pos: nhóm ngoặc cân bằng hoặc một từ."""
    args: List[str] = []
    i = pos
    while len(args) < n:
        while i < len(s) and s[i].isspace():
            i += 1
        if i >= len(s) or s[i] in _CLOSERS or s[i] in ",:":
            break
        j = i
        if s[i] in _OPENERS:
            depth = 0
            while j < len(s):
                depth += (s[j] in _OPENERS) - (s[j] in _CLOSERS)
                j += 1
                if depth == 0:
                    break
        else:
            while j < len(s) and not s[j].isspace() and s[j] not in _CLOSERS and s[j] not in _OPENERS:
                j += 1
        args.append(s[i:j])
        i = j
    return args


def _unparen(x: str) -> str:
    x = x.strip()
    while len(x) >= 2 and x[0] == "(" and x[-1] == ")" and len(_lean_args(x, 0, 1)) == 1 and _lean_args(x, 0, 1)[0] == x:
        x = x[1:-1].strip()
    return x


def _squeeze(x: str) -> str:
    return re.sub(r"[\s()]", "", x)


def _is_continuity(func: str, point: str, target: str) -> bool:
    """Tendsto f (𝓝 a) (𝓝 (f a)): phát biểu liên tục tại a, viết bằng giới hạn (được phép)."""
    f, a, t = _unparen(func), _unparen(point), _squeeze(target)
    m = _FUN_RE.match(f)
    if m:
        var, body = m.group(1), m.group(2)
        value = re.sub(rf"(?<![\w'₀-₉.]){re.escape(var)}(?![\w'₀-₉])", f"({a})", body)
        return _squeeze(value) == t
    return t == _squeeze(f"{f} {a}")


def _punctured_limit_problems(s: str) -> List[str]:
    """QT16c: Tendsto f (𝓝 a) … với (𝓝 a) là lân cận của BIẾN (không bỏ điểm a), trừ phát biểu liên tục."""
    for m in _TENDSTO_RE.finditer(s):
        args = _lean_args(s, m.end(), 3)
        if len(args) < 2:
            continue
        src = _NHDS_RE.match(_unparen(args[1]))
        if not src:
            continue
        tgt = _NHDS_RE.match(_unparen(args[2])) if len(args) > 2 else None
        if tgt and _is_continuity(args[0], src.group(1), tgt.group(1)):
            continue
        return [PUNCTURED_MSG]
    return []


def _form_problems(statement: str, kind: str) -> List[str]:
    """Các vi phạm QT16 của mệnh đề đã điền đáp án: (a) thiếu điều kiện tồn tại, (b) câu tìm tham số / biện luận không
    ở dạng "khi và chỉ khi", (c) khái niệm không theo định nghĩa giáo trình: tích phân suy rộng không là giới hạn của
    tích phân xác định, giới hạn hàm không lấy trên lân cận bỏ điểm."""
    s = _strip_comments(statement)
    problems = [msg for pat, need, msg in _EXISTENCE_RULES if pat.search(s) and not (need and need.search(s))]
    if kind in ("tim_tham_so", "bien_luan") and "↔" not in s and "Iff" not in s:
        problems.append("câu tìm tham số / biện luận phải ở dạng \"khi và chỉ khi\" (↔), không chỉ một chiều")
    problems += _punctured_limit_problems(s)
    return problems


def _normalize_statement(s: str) -> str:
    s = _strip_comments(s).replace("↦", "=>").replace("λ", "fun")
    s = re.sub(r"\s+", " ", s).strip()
    return re.sub(r"\s*([(),:\[\]{}])\s*", r"\1", s)


def _check_file(question_code: str, suffix: str, cands: List[Dict[str, Any]],
                blocks: List[Tuple[Any, List[str], List[str]]],
                report: Optional[Dict[Any, str]] = None) -> Dict[Any, bool]:
    """Biên dịch các khối kiểm tra (khóa, namespace mở, các dòng) trong một file; khóa -> khối biên dịch không lỗi.
    report: nếu có, nhận thông báo lỗi của từng khối (số dòng đổi về vị trí trong khối, để LLM sửa)."""
    imports = list(dict.fromkeys(lean_imports() + [m for c in cands for m in c["form"].get("extra_imports", [])]))
    lines = [*[f"import {m}" for m in imports], "set_option autoImplicit false", ""]
    marks: Dict[Any, Tuple[int, int]] = {}
    for n, (key, opens, body) in enumerate(blocks):
        start = len(lines) + 1
        lines += [f"section Chk{n}", f"open {' '.join(dict.fromkeys(opens))}" if opens else "", *body, f"end Chk{n}"]
        marks[key] = (start, len(lines))
    res = compile_lean(f"{question_code}-{suffix}", "\n".join(lines) + "\n")
    msgs = _split_messages(res["output"])
    bad = [m for m in msgs if m[1] == "error" or "declaration uses 'sorry'" in m[2]]
    if report is not None:
        for key, (lo, hi) in marks.items():
            report[key] = "\n".join(
                re.sub(r"^.*?\.lean:(\d+):", lambda mm: f"dòng {int(mm.group(1)) - lo + 1}:", m[2], count=1)
                for m in bad if lo <= m[0] <= hi) or (INFRA_MSG if res["infra_error"] else "")
    return {key: not res["infra_error"] and not any(lo <= m[0] <= hi for m in bad)
            for key, (lo, hi) in marks.items()}


def _vacuous_candidates(task: FormalTask, cands: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """(B1) Ứng viên mà Lean chứng minh được False từ các giả thiết của mệnh đề (giả thiết mâu thuẫn)."""
    blocks = [(i, c["form"]["open_namespaces"],
               [f"theorem vacuity_{i} {task.binders} :", f"    {c['statement']} := by", *_VACUITY_PROOF])
              for i, c in enumerate(cands)]
    proved = _check_file(task.code, "VACUITY", cands, blocks)
    return [c for i, c in enumerate(cands) if proved.get(i)]


# Điều kiện (2) bằng LLM: gọi FR09 (lean_prover), chế độ tìm chứng minh, chiều MÂU THUẪN, với giả thiết nằm trong mệnh
# đề (hyps_in_goal). FR09 bắt chứng minh theo khuôn intro … / exfalso / … nên Lean chấp nhận nghĩa là các giả thiết mâu
# thuẫn; Lean không chấp nhận thì KHÔNG kết luận được gì (QT19): mệnh đề vẫn được coi là không mâu thuẫn.
_HYPOTHESIS_HINT_RE = re.compile(r"→|∀[^,]*?[∈<>≤≥≠]|\(\s*h\w*\s*:")


def _vacuous_llm(task: FormalTask, run: "CoreRun", rep: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Điều kiện (2), bước tốn kém: FR09 (VACUITY_MODEL, sửa theo lỗi Lean VACUITY_LLM_FIXES lượt; LLM được kết luận
    "không mâu thuẫn" để dừng sớm). Trả {"mau_thuan": True, ...} khi Lean chấp nhận chứng minh False; {"mau_thuan": False,
    ...} trong mọi trường hợp còn lại; None khi mệnh đề không có giả thiết để xét."""
    import lean_prover as P

    stmt = rep["statement"].strip()
    if not _HYPOTHESIS_HINT_RE.search(stmt):
        return None
    what = f"Kiểm mâu thuẫn bằng LLM, mệnh đề ứng viên {rep['slot']}"
    left = run.fr08_left()
    if left < 1:
        run.fr08_limited = True
        run.history.append(f"{what}: bỏ qua, hết hạn mức lượt gọi LLM của FR08")
        return {"mau_thuan": False, "ly_do": "hết hạn mức lượt gọi LLM", "lean": False}
    obj = P.ProofObject(goal=stmt, context=P.parse_binders(task.binders), opens=list(rep["form"]["open_namespaces"]),
                        imports=list(rep["form"].get("extra_imports", [])), name="fr08_vacuity", code=task.code,
                        text_vi=task.text_vi, hyps_in_goal=True)
    req = P.ProofRequest(obj, direction=P.MAU_THUAN, mode=P.TIM, priority=PRIORITY_FR01, model=VACUITY_MODEL,
                         fix_model=VACUITY_MODEL, fixes=VACUITY_LLM_FIXES,
                         max_llm_calls=min(VACUITY_LLM_FIXES + 1, left), try_auto=False, allow_give_up=True,
                         final_model="")
    res = P.prove_request(req, log=lambda m: run.history.append(f"{what}: {m}"))
    run.fr08_calls += res.llm_calls
    run.tick("A_mau_thuan_FR09")
    if res.ok:
        run.history.append(f"{what}: Lean xác nhận giả thiết MÂU THUẪN")
        return {"mau_thuan": True, "ly_do": "Lean chấp nhận chứng minh False từ giả thiết", "lean": True,
                "chung_minh": res.proof, "fr09": {"llm_calls": res.llm_calls, "proof_path": res.proof_path}}
    if res.stop_reason == P.STOP_LLM_BUDGET:
        run.fr08_limited = True
    return {"mau_thuan": False, "ly_do": (res.last_error or res.stop_reason)[:300], "lean": False,
            "fr09": {"llm_calls": res.llm_calls, "stop_reason": res.stop_reason}}


def _equivalence_groups(task: FormalTask, cands: List[Dict[str, Any]], use_prover: bool) -> List[List[Dict[str, Any]]]:
    """(B3) Gom nhóm: trùng văn bản chuẩn hóa, rồi Lean chứng minh mệnh đề_i ↔ mệnh đề_j giữa các nhóm."""
    by_text: Dict[str, List[Dict[str, Any]]] = {}
    for c in cands:
        by_text.setdefault(_normalize_statement(c["statement"]), []).append(c)
    groups = list(by_text.values())
    if not use_prover or len(groups) < 2:
        return groups
    reps = [g[0] for g in groups]
    blocks = []
    for a in range(len(reps)):
        for b in range(a + 1, len(reps)):
            blocks.append(((a, b), reps[a]["form"]["open_namespaces"] + reps[b]["form"]["open_namespaces"],
                           [f"theorem equiv_{a}_{b} {task.binders} :",
                            f"    ({reps[a]['statement']}) ↔ ({reps[b]['statement']}) := by", *_EQUIV_PROOF]))
    proved = _check_file(task.code, "EQUIV", reps, blocks)
    parent = list(range(len(groups)))

    def find(x: int) -> int:
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    for (a, b), ok in proved.items():
        if ok:
            parent[find(b)] = find(a)
    merged: Dict[int, List[Dict[str, Any]]] = {}
    for gi, g in enumerate(groups):
        merged.setdefault(find(gi), []).extend(g)
    return list(merged.values())


# Điều kiện (4) bằng LLM: gọi FR09 (lean_prover), chế độ tìm chứng minh, chiều ĐÚNG, cho từng chiều "từ h_eq : A suy ra
# B". Lean chấp nhận chứng minh "A ↔ B" chưa đủ để kết luận hai bản dịch cùng nghĩa: khi cả A và B đều chứng minh được,
# chứng minh từng vế riêng rồi ghép lại cũng cho A ↔ B. Vì vậy FR09 được yêu cầu must_use = "h_eq": chứng minh vẫn đúng
# khi thay h_eq bằng True (không dùng A) thì không được chấp nhận.


def _prove_equiv_llm(task: FormalTask, run: "CoreRun", a: Dict[str, Any], b: Dict[str, Any]) -> bool:
    """Hai chiều A ⇒ B rồi B ⇒ A, mỗi chiều một yêu cầu FR09 (lượt đầu LEAN_MODEL, lượt sửa PROOF_ESCALATE_MODEL; LLM
    được kết luận "không tương đương" để dừng sớm). Chiều thứ nhất thất bại thì không thử chiều thứ hai."""
    import lean_prover as P

    what = f"Tương đương bằng LLM, ứng viên {a['slot']} ↔ {b['slot']}"
    opens = list(dict.fromkeys(a["form"]["open_namespaces"] + b["form"]["open_namespaces"]))
    imports = list(dict.fromkeys(a["form"].get("extra_imports", []) + b["form"].get("extra_imports", [])))
    for tag, hyp, goal in (("mp", a, b), ("mpr", b, a)):
        left = run.fr08_left(FR08_RESERVE)
        if left < 1:
            run.fr08_limited = True
            run.history.append(f"{what}: dừng, hết hạn mức lượt gọi LLM của FR08")
            return False
        obj = P.ProofObject(goal=goal["statement"].strip(),
                            context=P.parse_binders(task.binders) + [P.Binder("hyp", "h_eq", hyp["statement"].strip())],
                            opens=opens, imports=imports, name=f"fr08_eq_{tag}", code=task.code, text_vi=task.text_vi)
        req = P.ProofRequest(obj, direction=P.DUNG, mode=P.TIM, priority=PRIORITY_FR01, fixes=EQUIV_LLM_FIXES,
                             max_llm_calls=min(EQUIV_LLM_FIXES + 1, left), try_auto=False, allow_give_up=True,
                             must_use="h_eq", final_model="")
        res = P.prove_request(req, log=lambda m, t=tag: run.history.append(f"{what} ({t}): {m}"))
        run.fr08_calls += res.llm_calls
        run.tick("A_tuong_duong_FR09")
        if res.stop_reason == P.STOP_LLM_BUDGET:
            run.fr08_limited = True
        if not res.ok:
            return False
    run.history.append(f"{what}: Lean chấp nhận hai chiều, cả hai chiều đều dùng giả thiết")
    return True


def _llm_equivalence(task: FormalTask, run: "CoreRun", groups: List[List[Dict[str, Any]]]
                     ) -> List[List[Dict[str, Any]]]:
    """Chưa có nhóm >= 2: thử ghép hai nhóm đứng đầu (theo kích thước, rồi thứ tự sinh) bằng chứng minh của LLM; mỗi cặp
    chỉ thử một lần trong một lần chạy, tối đa EQUIV_LLM_PAIRS cặp mỗi lần gọi."""
    order = sorted(groups, key=lambda g: (-len(g), min(c["slot"] for c in g)))
    tried = 0
    for i in range(len(order)):
        for j in range(i + 1, len(order)):
            if tried >= EQUIV_LLM_PAIRS:
                return groups
            a, b = order[i][0], order[j][0]
            key = frozenset((_normalize_statement(a["statement"]), _normalize_statement(b["statement"])))
            if key in run.equiv_tried:
                continue
            run.equiv_tried.add(key)
            tried += 1
            if _prove_equiv_llm(task, run, a, b):
                run.equiv_proven.add(key)
                return [order[i] + order[j]] + [g for k, g in enumerate(order) if k not in (i, j)]
    return groups


def _merge_known(groups: List[List[Dict[str, Any]]], proven: set) -> List[List[Dict[str, Any]]]:
    """Ghép lại các nhóm mà LLM đã chứng minh tương đương ở lần xếp hạng trước (không gọi lại LLM)."""
    groups = [list(g) for g in groups]
    changed = True
    while changed:
        changed = False
        for i in range(len(groups)):
            for j in range(i + 1, len(groups)):
                ti = {_normalize_statement(c["statement"]) for c in groups[i]}
                tj = {_normalize_statement(c["statement"]) for c in groups[j]}
                if any(frozenset((x, y)) in proven for x in ti for y in tj):
                    groups[i] += groups.pop(j)
                    changed = True
                    break
            if changed:
                break
    return groups


BACKTRANSLATE_SCHEMA: Dict[str, Any] = {
    "type": "object", "properties": {"de_bai": {"type": "string"}}, "required": ["de_bai"], "additionalProperties": False,
}
BACKTRANSLATE_SYSTEM = """Bạn dịch một mệnh đề Lean 4 + Mathlib sang đề bài toán bằng tiếng Việt, văn phong đề thi Giải tích.
Diễn đạt ĐÚNG và CHỈ những gì mệnh đề Lean nói (kể cả các giả thiết và miền của tham số), không giải, không sửa cho hợp lý hơn,
không thêm điều mệnh đề không nói. Phân biệt rõ lân cận của biến trong giới hạn: Filter.Tendsto f (𝓝[≠] a) … là "khi x → a
(x ≠ a)"; Filter.Tendsto f (𝓝 a) … gồm cả x = a, phải diễn đạt là "f(x) dần tới … khi x → a, KỂ CẢ tại x = a (tức f(a)
cũng bằng giá trị đó)". Trả về trường de_bai."""

_EMBED_SCRIPT = """
import json, sys
from sentence_transformers import SentenceTransformer
data = json.load(sys.stdin)
model = SentenceTransformer(data["model"])
print("EMBED_JSON:" + json.dumps(model.encode(data["texts"], normalize_embeddings=True).tolist()))
"""


def _embed(texts: List[str]) -> List[List[float]]:
    """Vectơ nhúng (đã chuẩn hóa độ dài) bằng mô hình BERT (mặc định LaBSE, đa ngôn ngữ, có tiếng Việt).
    Chạy trong tiến trình con: mô hình chiếm ~2 GB RAM và được giải phóng ngay sau khi tính xong, để Lean
    (cần vài GB khi nạp Mathlib) không bị thiếu bộ nhớ ở các lần biên dịch sau."""
    env = {**os.environ, "PYTHONIOENCODING": "utf-8"}
    proc = subprocess.run(
        [sys.executable, "-c", _EMBED_SCRIPT], input=json.dumps({"model": EMBED_MODEL, "texts": texts}),
        capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=900, env=env,
    )
    line = next((ln for ln in (proc.stdout or "").splitlines() if ln.startswith("EMBED_JSON:")), "")
    if proc.returncode != 0 or not line:
        raise RuntimeError(f"Không tính được vectơ nhúng: {(proc.stderr or '').strip()[-500:]}")
    return json.loads(line[len("EMBED_JSON:"):])


def _back_translate(task: FormalTask, cand: Dict[str, Any]) -> str:
    """Bản diễn đạt lại bằng tiếng Việt của mệnh đề (dùng cho điểm ngữ nghĩa, điều kiện (5) và người kiểm mẫu);
    tính một lần cho mỗi ứng viên."""
    if not cand.get("back_translation"):
        stmt = task.header + "\n    " + cand["statement"]
        defs = f"\n\n{MATHEXAM_DEFS_FOR_REVIEW}" if "MathExam." in stmt else ""
        cand["back_translation"] = _call_structured(BACKTRANSLATE_SYSTEM, f"Mệnh đề Lean:\n```lean\n{stmt}\n```{defs}",
                                                    BACKTRANSLATE_SCHEMA, model=BACKTRANSLATE_MODEL)["de_bai"]
    return cand["back_translation"]


def _judge_restatement(task: FormalTask, restatement: str, analysis: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Điều kiện (5), B8: giám khảo (JUDGE_MODEL, mạnh hơn mô hình sinh) đối chiếu từng phần bản diễn đạt lại với bảng
    B1 và phát biểu gốc, liệt kê và phân loại mọi khác biệt. HỆ THỐNG kết luận từ danh sách khác biệt: khớp khi mọi
    khác biệt thuộc JUDGE_ALLOWED. Bảng đối chiếu từng phần chỉ dùng để phát hiện câu trả lời tự mâu thuẫn: có phần ghi
    "không khớp" mà danh sách khác biệt rỗng thì không kết luận khớp. Giám khảo có thể ghi một khác biệt vào phần khác
    với phần bị đánh "không khớp" (ví dụ cách mô hình hóa hàm ngược ghi ở giả thiết, phần đối tượng đánh không khớp),
    nên không ghép khác biệt với phần theo tên."""
    parts = [f"(1) Phát biểu gốc:\n{task.text_vi}",
             "(2) " + (_render_normalized(analysis) if analysis else "Bảng phân tích: (không có, đối chiếu trực tiếp với "
                                                                     "phát biểu gốc)")]
    info = []
    if task.needs_answer:
        info.append(f"Đáp số hệ thống đã điền vào mệnh đề (SymPy): {task.answer_sympy}")
    if task.domain_note and task.domain_note != "không có":
        info.append(f"Tham số và miền (do hệ thống cố định): {task.domain_note}")
    parts.append("(3) " + ("\n".join(info) if info else "Không có đáp số điền vào (phát biểu cần chứng minh)."))
    parts.append(f"(4) Bản diễn đạt lại của mệnh đề Lean:\n{restatement}")
    res = _call_structured(JUDGE_SYSTEM, "\n\n".join(parts), JUDGE_SCHEMA, model=JUDGE_MODEL, effort=JUDGE_EFFORT)
    issues = [f"[{d['loai']}] {d['mo_ta']}" for d in res["khac_biet"] if d["loai"] not in JUDGE_ALLOWED]
    if not res["khac_biet"]:
        issues += [f"[khong_khop_khong_neu_khac_biet:{r['phan']}] {r['ban_dien_dat_noi']}"
                   for r in res["doi_chieu"] if not r["khop"]]
    return {"khop": not issues, "sai_lech": "; ".join(issues), **res}


def _combine(sym: float, sem: float) -> float:
    a = SCORE_ALPHA
    if SCORE_COMBINE == "linear":
        return a * sym + (1 - a) * sem
    if SCORE_COMBINE == "square":
        return a * sym ** 2 + (1 - a) * sem ** 2
    return a * math.log(sym) + (1 - a) * math.log(sem)


def _rank_candidates(task: FormalTask, live: List[Dict[str, Any]], full: bool, vacuous_known: Optional[List[Dict[str, Any]]] = None,
                     refine: Optional[Any] = None, run: Optional["CoreRun"] = None
                     ) -> Tuple[List[Tuple[Dict[str, Any], List[Dict[str, Any]]]], List[Dict[str, Any]], Dict[str, Any]]:
    """Trả về (thứ tự chọn [(ứng viên, nhóm)], các ứng viên bị loại do giả thiết mâu thuẫn, nhật ký điểm).
    Mặc định nhóm xếp theo kích thước (lớn trước), rồi theo thứ tự sinh. Với SEMANTIC_RANK: lấy ứng viên điểm kết hợp
    cao nhất, bỏ cả nhóm tương đương của nó, rồi lặp lại (thủ tục n@k); việc dịch ngược mọi ứng viên tính vào hạn mức
    FR08 của run, không đủ hạn mức thì bỏ điểm ngữ nghĩa.
    vacuous_known: kết quả kiểm tra mâu thuẫn đã có sẵn (đã chạy chung file với kiểm tra mệnh đề).
    refine(pool, groups) -> groups: ghép thêm nhóm sau bước tactic tự động (tương đương đã biết, chứng minh của LLM)."""
    log: Dict[str, Any] = {"compiled": len(live)}
    vacuous: List[Dict[str, Any]] = []
    if vacuous_known is not None:
        vacuous = vacuous_known
        log["vacuous"] = [c["slot"] for c in vacuous]
    elif VACUITY_CHECK:  # chỉ tốn một lần biên dịch, không gọi LLM: chạy cả khi chỉ có một ứng viên
        vacuous = _vacuous_candidates(task, live)
        log["vacuous"] = [c["slot"] for c in vacuous]
    pool = [c for c in live if c not in vacuous]
    if not pool:
        return [], vacuous, log
    groups = _equivalence_groups(task, pool, use_prover=full and EQUIV_CHECK)
    if refine is not None:
        groups = refine(pool, groups)
    log["group_sizes"] = sorted((len(g) for g in groups), reverse=True)
    group_of = {id(c): g for g in groups for c in g}

    # Một nhóm duy nhất (mọi mệnh đề tương đương): điểm ngữ nghĩa không đổi được lựa chọn, bỏ qua dịch ngược + LaBSE
    need = sum(1 for c in pool if not c.get("back_translation"))
    semantic = full and SEMANTIC_RANK and len(pool) > 1 and len(groups) > 1
    if semantic and run is not None and run.fr08_left(FR08_RESERVE) < need:
        semantic = False
        log["semantic_skipped"] = "không đủ hạn mức lượt gọi LLM của FR08"
    if not semantic:
        if full and len(groups) == 1 and len(pool) > 1:
            log["semantic_skipped"] = "một nhóm tương đương"
        order = sorted(groups, key=lambda g: (-len(g), min(c["slot"] for c in g)))
        return [(g[0], g) for g in order], vacuous, log
    if run is not None:
        run.fr08_calls += need

    # Điểm ký hiệu và điểm ngữ nghĩa
    sym = [float(len(group_of[id(c)])) for c in pool]
    try:
        with concurrent.futures.ThreadPoolExecutor(max_workers=len(pool)) as ex:
            backs = list(ex.map(lambda c: _back_translate(task, c), pool))
        vecs = _embed([task.text_vi] + backs)
        sem = [max(1e-6, sum(x * y for x, y in zip(vecs[0], v))) for v in vecs[1:]]
    except Exception as exc:  # thiếu mô hình nhúng / lỗi LLM: chỉ dùng điểm ký hiệu
        backs, sem = [""] * len(pool), [1.0] * len(pool)
        log["semantic_error"] = str(exc)[:300]
    sym_n = [s / sum(sym) for s in sym]
    sem_n = [s / sum(sem) for s in sem]
    scored = []
    for c, s1, s2, n1, n2, bt in zip(pool, sym, sem, sym_n, sem_n, backs):
        c["scores"] = {"symbolic": s1, "semantic": round(s2, 4), "symbolic_norm": round(n1, 4),
                       "semantic_norm": round(n2, 4), "combined": round(_combine(n1, n2), 4), "back_translation": bt}
        scored.append(c)
    log["scores"] = [{"slot": c["slot"], **{k: v for k, v in c["scores"].items() if k != "back_translation"}}
                     for c in scored]
    log["combine"] = {"method": SCORE_COMBINE, "alpha": SCORE_ALPHA, "embed_model": EMBED_MODEL}

    order: List[Tuple[Dict[str, Any], List[Dict[str, Any]]]] = []
    remaining = sorted(scored, key=lambda c: (-c["scores"]["combined"], c["slot"]))
    while remaining:
        best = remaining[0]
        g = group_of[id(best)]
        order.append((best, g))
        remaining = [c for c in remaining if id(c) not in {id(x) for x in g}]
    return order, vacuous, log


# =============================================================================
# Chạy lõi cho một phát biểu: FR08 (giai đoạn A) rồi FR09 (giai đoạn B)
# =============================================================================

INFRA_MSG = "Lean không nạp được Mathlib (lỗi đọc .olean, thường do thiếu bộ nhớ). Hãy đóng bớt ứng dụng rồi thử lại."
PROOF_METHODS = {"auto": "tactic tự động (không gọi LLM)", "llm": "LLM viết chứng minh",
                 "decompose": "chia bước trung gian"}


class CoreRun:
    """Trạng thái một lần chạy lõi: bước bật, số ứng viên, dạng câu, ngữ cảnh truy xuất, nhật ký, thời gian từng bước."""

    def __init__(self, steps: Optional[List[int]] = None, num_candidates: Optional[int] = None):
        self.steps = frozenset(steps) if steps is not None else FORMALIZE_STEPS
        self.k = max(1, num_candidates or NUM_CANDIDATES) if 4 in self.steps else 1
        self.timings: Dict[str, float] = {}  # giây cho từng bước, cộng dồn qua các vòng
        self.pipeline: Dict[str, Any] = {"steps": sorted(self.steps), "candidates": self.k, "timings_s": self.timings}
        self.context: Dict[str, str] = {}
        self.kind = "khac"  # dạng câu (QT16b)
        self.history: List[str] = []
        self.last_code = ""
        self.last_output = ""
        self.proof_calls = 0  # số lượt LLM viết chứng minh (kể cả khung chia bước và chứng minh phủ định)
        self.analysis: Optional[Dict[str, Any]] = None  # bảng B1, danh sách kiểm tra cho giám khảo B8
        self.fr08_budget = FR08_MAX_LLM_CALLS  # hạn mức lượt gọi LLM của FR08 (NFR04)
        self.fr08_calls = 0
        self.fr08_limited = False  # có bước bị bỏ hoặc cắt bớt vì hết hạn mức
        self.fr09_budget = FR09_TASK_MAX_LLM  # hạn mức lượt gọi LLM của FR09 cho cả câu (chứng minh, viết lại, phủ định)
        self.fr09_calls = 0
        self.equiv_tried: set = set()  # cặp mệnh đề (văn bản chuẩn hóa) đã thử chứng minh tương đương bằng LLM
        self.equiv_proven: set = set()
        self._next_slot = 0
        self._mark = time.perf_counter()

    def fr08_left(self, reserve: int = 0) -> int:
        """Số lượt gọi LLM FR08 còn được dùng, sau khi giữ lại `reserve` lượt."""
        return self.fr08_budget - self.fr08_calls - reserve

    def tick(self, step: str) -> None:
        now = time.perf_counter()
        self.timings[step] = round(self.timings.get(step, 0.0) + now - self._mark, 1)
        self._mark = now

    def new_slots(self, n: int) -> List[int]:
        slots = list(range(self._next_slot, self._next_slot + n))
        self._next_slot += n
        return slots


def ensure_mathlib() -> None:
    if not lean_status()["mathlib_ready"]:
        raise RuntimeError(f"Chưa có Mathlib đã build tại {LEAN_PROJECT}")


def prepare_context(task: FormalTask, run: CoreRun) -> None:
    """B1 + B2 (lỗi ở đây không chặn quy trình: ghi lại rồi tiếp tục với các bước còn lại)."""
    norm: Optional[Dict[str, Any]] = None
    if 1 in run.steps:
        try:
            norm = normalize_problem(task, run)
            run.analysis = norm
            run.context["normalized"] = _render_normalized(norm)
            run.pipeline["normalized"] = norm
        except Exception as exc:
            run.pipeline["normalize_error"] = str(exc)[:300]
        run.tick("1_chuan_hoa_de_LLM")
    run.kind = _statement_kind(task, norm)
    run.pipeline["statement_kind"] = run.kind
    if 2 in run.steps:
        try:
            run.context["retrieved"], run.pipeline["retrieved_items"] = _retrieval_context(task, norm)
        except Exception as exc:
            run.pipeline["retrieval_error"] = str(exc)[:300]
        run.tick("2_truy_xuat")


# -----------------------------------------------------------------------------
# FR08: hình thức hóa
# -----------------------------------------------------------------------------


def write_statements(task: FormalTask, run: CoreRun,
                     pending: Dict[int, Optional[Tuple[str, str]]], budget: bool = True) -> List[Dict[str, Any]]:
    """Viết các mệnh đề (ứng viên -> phản hồi lần trước), sửa tối đa STATEMENT_FIXES lượt. Mỗi mệnh đề qua kiểm tĩnh,
    điều kiện (3) đúng dạng (luật, trước khi biên dịch), rồi Lean kiểm trong MỘT file: (1) đúng kiểu với chứng minh
    tạm `sorry` do hệ thống đặt, (2) giả thiết không mâu thuẫn, và thử chứng minh bằng tactic tự động.
    budget: tính lượt gọi vào hạn mức FR08 (giữ lại FR08_RESERVE lượt cho dịch ngược + giám khảo); không đủ thì bớt
    ứng viên của vòng đó. Trả các mệnh đề đạt (1) và (3), kèm cờ "vacuous" và "auto_ok"."""
    with_analysis = 3 in run.steps  # bước 3: LLM điền bảng ánh xạ khái niệm trước khi viết mệnh đề
    st_schema = _statement_schema(with_analysis)
    st_system = STATEMENT_SYSTEM + (ANALYSIS_INSTRUCTIONS if with_analysis else "")
    typed_now: List[Dict[str, Any]] = []
    for rnd in range(1, STATEMENT_FIXES + 2):
        if not pending:
            break
        slots = sorted(pending)
        if budget:
            left = max(0, run.fr08_left(FR08_RESERVE))
            if left < len(slots):
                run.fr08_limited = True
                run.history.append(f"Mệnh đề vòng {rnd}: hết hạn mức lượt gọi LLM của FR08, bỏ "
                                   f"{len(slots) - left}/{len(slots)} ứng viên còn chờ")
                for s in slots[left:]:
                    pending.pop(s)
                slots = slots[:left]
            if not slots:
                break
            run.fr08_calls += len(slots)
        else:  # viết lại mệnh đề trong pha chứng minh: tính vào hạn mức FR09 của câu
            left = max(0, run.fr09_budget - run.fr09_calls)
            for s_ in slots[left:]:
                pending.pop(s_)
            slots = slots[:left]
            if not slots:
                break
            run.fr09_calls += len(slots)
        with concurrent.futures.ThreadPoolExecutor(max_workers=len(slots)) as ex:
            forms = dict(zip(slots, ex.map(
                lambda s: _call_structured(st_system, _statement_prompt(task, pending[s], run.context),
                                           st_schema, model=LEAN_MODEL), slots)))
        run.tick("A_viet_menh_de_LLM")
        to_compile = []
        for s in slots:
            form = {**forms[s], "helper_lemmas": "", "proof": ""}
            try:
                _static_check(form, needs_answer=task.needs_answer)
                unused = _param_problems(form["statement"], task.param_names)
                if unused:
                    raise ValueError("; ".join(unused))
                term = task.answer_term(form["answer_type"])
            except Exception as exc:
                pending[s] = (json.dumps(forms[s], ensure_ascii=False, indent=1), f"Bị chặn trước khi biên dịch: {exc}")
                run.history.append(f"Mệnh đề vòng {rnd} · ứng viên {s}: {pending[s][1]}")
                continue
            wrong_form = _form_problems(task.fill(form["statement"], term), run.kind) if FORM_CHECK else []
            if wrong_form:
                pending[s] = (json.dumps(forms[s], ensure_ascii=False, indent=1),
                              "Mệnh đề sai dạng (QT16): " + "; ".join(wrong_form))
                run.history.append(f"Mệnh đề vòng {rnd} · ứng viên {s}: {pending[s][1]}")
                continue
            to_compile.append((s, {**form, "proof": "sorry"}, term))
        if not to_compile:
            continue
        results = compile_candidates(f"{task.code}-STMT", task, to_compile, allow_sorry=True, vacuity=VACUITY_CHECK,
                                     auto=AUTO_PROVE)
        run.tick("A_Lean_kiem_menh_de_va_mau_thuan")
        if any(r["infra_error"] for r in results.values()):
            raise RuntimeError(INFRA_MSG)
        for s, form, term in to_compile:
            r = results[s]
            run.last_code, run.last_output = r["block"], r["errors"]
            if r["ok"]:
                typed_now.append({"slot": s, "round": rnd, "form": {**form, "proof": ""}, "term": term,
                                  "statement": task.fill(form["statement"], term),
                                  "vacuous": r.get("vacuous", False), "auto_ok": r.get("auto_ok", False)})
                pending.pop(s)
            else:
                pending[s] = (_numbered(r["block"]), "; ".join(r["problems"]) + "\n" + r["errors"])
                run.history.append(f"Mệnh đề vòng {rnd} · ứng viên {s}: Lean: {'; '.join(r['problems'])}")
    return typed_now


def _rank(task: FormalTask, run: CoreRun, typed: List[Dict[str, Any]]
          ) -> List[Tuple[Dict[str, Any], List[Dict[str, Any]]]]:
    """Loại mệnh đề có giả thiết mâu thuẫn (điều kiện 2), gom nhóm tương đương (điều kiện 4: tactic tự động, rồi các
    cặp LLM đã chứng minh ở lần trước, rồi khi vẫn chưa có nhóm >= 2 thì LLM chứng minh thêm), xếp hạng."""
    if not typed:
        return []
    full = 4 in run.steps

    def refine(pool: List[Dict[str, Any]], groups: List[List[Dict[str, Any]]]) -> List[List[Dict[str, Any]]]:
        groups = _merge_known(groups, run.equiv_proven)
        if (full and REQUIRE_EQUIV and EQUIV_LLM_PAIRS > 0 and len(groups) >= 2
                and not any(len(g) >= 2 for g in groups)):
            groups = _llm_equivalence(task, run, groups)
        return groups

    ranking, vacuous, score_log = _rank_candidates(
        task, typed, full=full, vacuous_known=[c for c in typed if c["vacuous"]] if VACUITY_CHECK else [],
        refine=refine, run=run)
    run.pipeline["ranking_log"] = score_log
    for c in vacuous:
        if not c.get("vacuous_logged"):
            c["vacuous_logged"] = True
            run.history.append(f"Mệnh đề ứng viên {c['slot']}: loại do giả thiết mâu thuẫn")
    run.tick("A_chon_menh_de")
    return ranking


def formalize(task: FormalTask, run: CoreRun) -> Dict[str, Any]:
    """FR08 (mục 2.5): phát biểu tiếng Việt -> mệnh đề Lean, bản diễn đạt lại và kết luận "đã xác nhận" / "chưa xác
    nhận", độc lập với FR09 (không chứng minh mệnh đề). Thứ tự, rẻ trước tốn kém sau (QT05):
      B1 + B2 -> viết k mệnh đề, Lean kiểm (1)(2) và luật kiểm (3) -> gom nhóm tương đương (4) bằng tactic tự động;
      chưa có nhóm >= 2 thì LLM chứng minh tương đương cặp đứng đầu, vẫn chưa có thì sinh thêm EXTRA_CANDIDATES bản dịch;
      -> (5) dịch ngược + giám khảo, chỉ cho đại diện của nhóm >= 2, tối đa JUDGE_GROUPS nhóm theo thứ tự xếp hạng;
      -> (2) lần hai cho mệnh đề vừa qua giám khảo: LLM thử chứng minh False từ giả thiết, Lean chấp nhận thì loại nhóm.
    Mọi lượt gọi LLM tính vào hạn mức run.fr08_budget; hết hạn mức thì dừng, kết luận "chưa xác nhận" kèm lý do.
    Trả về: status (CONFIRMED / UNCONFIRMED), selected (mệnh đề được chọn) và group (nhóm tương đương của nó, mọi mệnh đề
    trong nhóm đều được Lean chứng minh tương đương với mệnh đề được chọn), reason, typed, ranking, statements, llm_calls."""
    prepare_context(task, run)
    typed = write_statements(task, run, {s: None for s in run.new_slots(run.k)})
    ranking = _rank(task, run, typed)
    if REQUIRE_EQUIV and EXTRA_CANDIDATES > 0 and typed and not any(len(g) >= 2 for _, g in ranking):
        n_extra = min(EXTRA_CANDIDATES, max(0, run.fr08_left(FR08_RESERVE)))
        run.fr08_limited |= n_extra < EXTRA_CANDIDATES
        if n_extra:
            run.history.append(f"Chưa có 2 bản dịch được Lean chứng minh tương đương: sinh thêm {n_extra} bản dịch")
            extra = write_statements(task, run, {s: None for s in run.new_slots(n_extra)})
            if extra:
                typed += extra
                ranking = _rank(task, run, typed)

    selected: Optional[Tuple[Dict[str, Any], List[Dict[str, Any]]]] = None
    judged = 0
    reason = ""
    for rep, g in ranking:
        if REQUIRE_EQUIV and len(g) < 2:
            confirm(task, run, rep, g)  # chỉ ghi kết quả điều kiện (4), không gọi LLM
            continue
        if judged >= JUDGE_GROUPS:
            break
        judged += 1
        if confirm(task, run, rep, g):
            vac = _vacuous_llm(task, run, rep) if DEEP_VACUITY else None
            if vac is not None:
                rep["vacuity_llm"] = vac
            if vac and vac["mau_thuan"]:  # Lean xác nhận giả thiết mâu thuẫn: cả nhóm (tương đương với nó) bị loại
                rep["confirmed"] = False
                rep["conditions"]["khong_mau_thuan"] = False
                rep["reject_reason"] = f"giả thiết mâu thuẫn, Lean xác nhận chứng minh False (điều kiện 2): {vac['ly_do']}"
                run.history.append(f"Mệnh đề ứng viên {rep['slot']}: chưa xác nhận, {rep['reject_reason']}")
                reason = rep["reject_reason"]
                continue
            selected = (rep, g)
            break
        reason = rep.get("reject_reason", "")
    if selected is None:
        if not typed:
            reason = "không có mệnh đề nào biên dịch được và đúng dạng (điều kiện 1, 3)"
        elif not ranking:
            reason = "mọi mệnh đề đều có giả thiết mâu thuẫn (điều kiện 2)"
        elif REQUIRE_EQUIV and not any(len(g) >= 2 for _, g in ranking):
            reason = "không có hai bản dịch độc lập nào được Lean chứng minh tương đương (điều kiện 4)"
        if run.fr08_limited and "hạn mức" not in reason:
            reason = (reason + "; " if reason else "") + f"dừng sớm vì hết hạn mức {run.fr08_budget} lượt gọi LLM của FR08"
    else:
        rep, g = selected
        for c in g:  # cùng nhóm với mệnh đề được chọn: được Lean chứng minh tương đương, mang kết quả xác nhận của nó
            c.setdefault("confirmed_via", rep["slot"] if c is not rep else None)
    statements = [_statement_info(rep) for rep, _ in ranking if "conditions" in rep]
    fz = {"status": "CONFIRMED" if selected else "UNCONFIRMED", "selected": selected[0] if selected else None,
          "group": selected[1] if selected else [], "reason": reason, "typed": typed, "ranking": ranking,
          "statements": statements, "llm_calls": run.fr08_calls}
    run.pipeline["fr08"] = {"status": fz["status"], "reason": reason, "llm_calls": run.fr08_calls,
                            "llm_budget": run.fr08_budget, "limited": run.fr08_limited, "group_size": len(fz["group"]),
                            "equiv_llm": {"tried": len(run.equiv_tried), "proven": len(run.equiv_proven)},
                            "vacuity_llm": [{"slot": rep["slot"], **{k: v for k, v in rep["vacuity_llm"].items()
                                                                     if k != "chung_minh"}}
                                            for rep, _ in ranking if rep.get("vacuity_llm")]}
    return fz


def confirm(task: FormalTask, run: CoreRun, rep: Dict[str, Any], group: List[Dict[str, Any]]) -> bool:
    """Kết luận mệnh đề "đã xác nhận" hay chưa (QT15). Mệnh đề trong bảng xếp hạng đã đạt (1) biên dịch, (2) không
    mâu thuẫn, (3) đúng dạng; ở đây kiểm (4) nhóm tương đương có >= 2 bản dịch và (5) giám khảo kết luận bản diễn đạt
    lại khớp phát biểu gốc. Ghi kết quả vào rep["conditions"], rep["restatement"], rep["judge"]. Không đủ hạn mức FR08
    cho dịch ngược + giám khảo thì trả False mà không lưu kết luận (lần sau có hạn mức thì kiểm lại)."""
    if "confirmed" in rep:
        return rep["confirmed"]
    cond = {"bien_dich": True, "khong_mau_thuan": True, "dung_dang": True,
            "tuong_duong": len(group) >= 2, "dien_dat_lai_khop": False}
    rep["conditions"] = cond
    if REQUIRE_EQUIV and not cond["tuong_duong"]:
        rep["confirmed"] = False
        rep["reject_reason"] = "không có bản dịch độc lập nào được Lean chứng minh tương đương (điều kiện 4)"
        run.history.append(f"Mệnh đề ứng viên {rep['slot']}: chưa xác nhận, {rep['reject_reason']}")
        return False
    cost = (0 if rep.get("back_translation") else 1) + 1
    if run.fr08_left() < cost:
        run.fr08_limited = True
        rep["reject_reason"] = "không đủ hạn mức lượt gọi LLM của FR08 cho dịch ngược và giám khảo (điều kiện 5)"
        run.history.append(f"Mệnh đề ứng viên {rep['slot']}: chưa xác nhận, {rep['reject_reason']}")
        return False
    run.fr08_calls += cost
    rep["restatement"] = _back_translate(task, rep)
    run.tick("A_dich_nguoc_LLM")
    rep["judge"] = _judge_restatement(task, rep["restatement"], run.analysis)
    run.tick("A_giam_khao_LLM")
    cond["dien_dat_lai_khop"] = bool(rep["judge"]["khop"])
    rep["confirmed"] = cond["dien_dat_lai_khop"]
    if not rep["confirmed"]:
        rep["reject_reason"] = f"bản diễn đạt lại không khớp đề (điều kiện 5): {rep['judge']['sai_lech']}"
        run.history.append(f"Mệnh đề ứng viên {rep['slot']}: chưa xác nhận, {rep['reject_reason']}")
    return rep["confirmed"]


# -----------------------------------------------------------------------------
# FR09: chứng minh tự động
# -----------------------------------------------------------------------------


def proof_object(task: FormalTask, rep: Dict[str, Any], run: Optional[CoreRun] = None):
    """Đối tượng FR09 của một mệnh đề câu hỏi: ngữ cảnh là tham số và miền do hệ thống cố định, đích là mệnh đề đã điền
    đáp án; định lý tên exam_answer (file lưu vào CSDL vẫn kiểm lại được bằng compile_lean)."""
    import lean_prover as P

    return P.ProofObject(goal=rep["statement"], context=P.parse_binders(task.binders),
                         opens=list(rep["form"]["open_namespaces"]), imports=list(rep["form"].get("extra_imports", [])),
                         name=THEOREM_NAME, code=task.code, text_vi=task.text_vi, hint=task.hint,
                         context_text="\n\n".join(_context_parts(run.context)) if run else "")


def prove(task: FormalTask, run: CoreRun, rep: Dict[str, Any], proof_fixes: int = PROOF_FIXES,
          negate: bool = False, decompose: bool = False) -> Dict[str, Any]:
    """FR01 gọi FR09 (lean_prover) ở chế độ tìm chứng minh cho một mệnh đề đã xác nhận: chiều đúng, hoặc chiều sai
    (negate=True: chứng minh phủ định, tức là phát biểu sai). Lượt gọi LLM tính vào hạn mức FR09 của câu (run.fr09_budget,
    NFR04). Thành công: {"ok": True, "form", "result", "method", "fr09"}; thất bại: {"ok": False, "view", "error", "fr09"}."""
    import lean_prover as P

    left = max(0, run.fr09_budget - run.fr09_calls)
    req = P.ProofRequest(proof_object(task, rep, run), direction=P.SAI if negate else P.DUNG, mode=P.TIM,
                         priority=PRIORITY_FR01, max_llm_calls=min(P.SEARCH_MAX_LLM, left), fixes=proof_fixes,
                         decompose=decompose, try_auto=AUTO_PROVE and (negate or bool(rep.get("auto_ok"))))
    what = f"{'Phủ định · ' if negate else ''}mệnh đề ứng viên {rep['slot']}"
    res = P.prove_request(req, log=lambda m: run.history.append(f"FR09 · {what}: {m}"))
    run.proof_calls += res.llm_calls
    run.fr09_calls += res.llm_calls
    run.pipeline.setdefault("proof_models", []).extend(res.models)
    run.pipeline.setdefault("fr09", []).append({k: v for k, v in res.to_dict().items()
                                                if k not in ("lean_code", "history", "statement_view")})
    run.tick("B_FR09_chung_minh")
    if res.lean_code:
        run.last_code, run.last_output = res.lean_code, res.last_error
    if res.ok:
        form = {**rep["form"], "helper_lemmas": res.helper_lemmas, "proof": res.proof}
        return {"ok": True, "form": form, "result": {"axioms": res.axioms}, "method": res.method, "fr09": res}
    if res.stop_reason == P.STOP_LLM_BUDGET:
        run.history.append(f"FR09 · {what}: dừng vì hết hạn mức lượt gọi LLM ({run.fr09_calls}/{run.fr09_budget})")
    return {"ok": False, "view": res.statement_view, "error": res.last_error, "fr09": res}


# -----------------------------------------------------------------------------
# FR08 + FR09 cho một phát biểu
# -----------------------------------------------------------------------------


def _statement_info(rep: Dict[str, Any]) -> Dict[str, Any]:
    return {"slot": rep["slot"], "lean": rep["statement"], "restatement": rep.get("restatement", ""),
            "conditions": rep.get("conditions"), "confirmed": rep.get("confirmed", False),
            "judge": rep.get("judge"), "reject_reason": rep.get("reject_reason", "")}


def formalize_and_prove(task: FormalTask, run: CoreRun, proof_fixes: int = PROOF_FIXES) -> Dict[str, Any]:
    """FR08 rồi FR09. FR08 (formalize) kết luận trước, độc lập với chứng minh; chỉ mệnh đề đã xác nhận (QT15) mới được
    đưa sang FR09: mệnh đề được chọn (có chia bước), rồi các mệnh đề khác cùng nhóm tương đương với nó (Lean đã chứng
    minh tương đương nên cùng được xác nhận; STATEMENT_FALLBACKS mệnh đề), rồi viết lại mệnh đề (STATEMENT_REWRITES;
    phải được Lean chứng minh tương đương với mệnh đề được chọn). Không được thì thử chứng minh phủ định.
    Trạng thái: VERIFIED_PASS (đã chứng minh), DISPROVED (Lean chứng minh phát biểu sai), FAILED (mệnh đề đã xác nhận
    nhưng không chứng minh được trong giới hạn), UNCONFIRMED (FR08 không xác nhận được mệnh đề nào)."""
    fz = formalize(task, run)
    typed, ranking = fz["typed"], fz["ranking"]

    confirmed: List[Tuple[Dict[str, Any], List[Dict[str, Any]]]] = []
    if fz["selected"] is not None:
        base, g = fz["selected"], fz["group"]
        seen = {_normalize_statement(base["statement"])}
        alts = []
        for c in g:
            key = _normalize_statement(c["statement"])
            if c is not base and key not in seen and len(alts) < STATEMENT_FALLBACKS:
                seen.add(key)
                c.update(confirmed=True, conditions=dict(base["conditions"]), restatement=base.get("restatement", ""),
                         judge=base.get("judge"))
                alts.append(c)
        confirmed = [(base, g)] + [(c, g) for c in alts]
    chosen: Optional[Dict[str, Any]] = None
    result: Optional[Dict[str, Any]] = None
    failed_proofs: List[Tuple[str, str]] = []  # (mệnh đề, lỗi Lean lần cuối) của các mệnh đề chưa chứng minh được
    for i, (rep, g) in enumerate(confirmed):
        if i:
            run.history.append(f"Chứng minh mệnh đề ứng viên {rep['slot']}, cùng nhóm tương đương với mệnh đề được chọn")
        pr = prove(task, run, rep, proof_fixes, decompose=DECOMPOSE and i == 0)
        if pr["ok"]:
            chosen = {**rep, "form": pr["form"], "group_size": len(g), "num_groups": len(ranking), "method": pr["method"]}
            result = pr["result"]
            break
        failed_proofs.append((pr["view"], pr["error"]))

    # Viết lại mệnh đề theo cách khác (đề và đáp án giữ nguyên, đã qua bộ giải độc lập), rồi chứng minh lại
    rewrites = 0
    tried = {_normalize_statement(c["statement"]) for c in typed}
    while chosen is None and failed_proofs and rewrites < STATEMENT_REWRITES:
        rewrites += 1
        tried_text = "\n\n".join(f"```lean\n{v}\n```\nLỗi Lean lần cuối:\n{e[-1500:]}" for v, e in failed_proofs[-2:])
        note = ("Các mệnh đề sau đúng kiểu nhưng sau nhiều lượt vẫn CHƯA CHỨNG MINH ĐƯỢC:\n" + tried_text +
                "\n\nHãy phát biểu lại bài toán theo CÁCH KHÁC nhưng tương đương và vẫn đúng nghĩa đề (ví dụ đổi dạng giới "
                "hạn/đạo hàm/tích phân, tách hằng số, dùng định nghĩa hoặc định lý Mathlib/MathExam có sẵn trong phần truy "
                "xuất) sao cho dễ chứng minh hơn. Không làm mệnh đề yếu hơn đề bài.")
        new = [c for c in write_statements(task, run, {s: ("", note) for s in run.new_slots(1)}, budget=False)
               if not c["vacuous"] and _normalize_statement(c["statement"]) not in tried]
        run.history.append(f"Viết lại mệnh đề lần {rewrites}: {'được 1 mệnh đề mới' if new else 'không có mệnh đề mới hợp lệ'}")
        if not new:
            break
        cand = new[0]
        tried.add(_normalize_statement(cand["statement"]))
        typed.append(cand)
        base = confirmed[0][0]
        if REQUIRE_EQUIV:  # (4) cho mệnh đề viết lại: Lean chứng minh tương đương với mệnh đề đã xác nhận
            same = len(_equivalence_groups(task, [base, cand], use_prover=True)) == 1
            run.tick("A_kiem_tuong_duong_viet_lai")
            if not same:
                run.history.append("Mệnh đề viết lại: Lean không chứng minh được tương đương với mệnh đề đã xác nhận, "
                                   "không dùng")
                continue
            cand.update(confirmed=True, conditions=dict(base["conditions"]),
                        restatement=base.get("restatement", ""), judge=base.get("judge"))
        elif not confirm(task, run, cand, [cand]):
            continue
        pr = prove(task, run, cand, proof_fixes)
        if pr["ok"]:
            chosen = {**cand, "form": pr["form"], "group_size": 1, "num_groups": len(ranking) + rewrites,
                      "method": pr["method"]}
            result = pr["result"]
        else:
            failed_proofs.append((pr["view"], pr["error"]))
    run.pipeline["statement_rewrites"] = rewrites

    # Không chứng minh được: thử chứng minh phủ định (QT19: chỉ khi chứng minh được phủ định mới kết luận là sai)
    refuted: Optional[Dict[str, Any]] = None
    if chosen is None and confirmed and DISPROVE_FIXES >= 0:
        keep = (run.last_code, run.last_output)
        rep = confirmed[0][0]
        pr = prove(task, run, rep, DISPROVE_FIXES, negate=True)
        if pr["ok"]:
            refuted = {**rep, "form": pr["form"], "method": pr["method"]}
            result = pr["result"]
        else:
            run.last_code, run.last_output = keep

    steps = sorted(run.steps)
    if chosen is not None:
        status = "VERIFIED_PASS"
        summary = (f"[Lean 4 + Mathlib OK] exam_answer chứng minh với mọi tham số trong miền; mệnh đề đã xác nhận "
                   f"(QT15: biên dịch, không mâu thuẫn, đúng dạng, nhóm {chosen['group_size']}/{len(typed)} bản dịch "
                   f"tương đương, diễn đạt lại khớp đề theo giám khảo {JUDGE_MODEL}); chứng minh bằng "
                   f"{PROOF_METHODS[chosen['method']]}; tiên đề: {', '.join(result['axioms']) or 'không'}; "
                   f"{run.proof_calls} lượt LLM viết chứng minh; bước {steps}")
    elif refuted is not None:
        status = "DISPROVED"
        summary = (f"[Lean 4 + Mathlib] Lean chứng minh được PHỦ ĐỊNH của mệnh đề đã xác nhận: phát biểu (đáp án) SAI; "
                   f"chứng minh bằng {PROOF_METHODS[refuted['method']]}; tiên đề: {', '.join(result['axioms']) or 'không'}")
    elif confirmed:
        status = "FAILED"
        summary = (f"Không chứng minh được trong giới hạn: {len(confirmed)} mệnh đề đã xác nhận, {run.proof_calls} lượt "
                   f"LLM viết chứng minh: " + " | ".join(run.history[-3:]))
    else:
        status = "UNCONFIRMED"
        summary = (f"Chưa xác nhận được mệnh đề (FR08, {run.fr08_calls}/{run.fr08_budget} lượt gọi LLM): {len(typed)} "
                   f"mệnh đề đúng kiểu, không mệnh đề nào đạt đủ năm điều kiện của QT15: {fz['reason']} | "
                   + " | ".join(run.history[-3:]))

    main = chosen or refuted or (confirmed[0][0] if confirmed else None)
    judged = main or next((rep for rep, _ in ranking if rep.get("judge")), None)
    if judged is not None and judged.get("judge"):
        review = {"faithful": bool(judged["judge"]["khop"]), "issues": judged["judge"]["sai_lech"],
                  "restatement": judged.get("restatement", ""), "judge_model": JUDGE_MODEL}
    else:
        review = {"faithful": None, "issues": "", "skipped": True}
    run.pipeline.update({"compiled_total": len(typed), "proof_calls": run.proof_calls,
                         "analysis": main["form"].get("analysis") if main else None,
                         "chosen_slot": main["slot"] if main else None,
                         "chosen_scores": main.get("scores") if main else None,
                         "proof_method": (chosen or refuted or {}).get("method"),
                         "statements": [_statement_info(rep) for rep, _ in ranking if "confirmed" in rep]})
    return {
        "status": status,
        "summary": summary,
        "output": summary + "\n" + (run.last_output or "")[-3000:],
        "review": review,
        "lean_code": run.last_code,
        "statement": _statement_info(main) if main else None,
        "chosen": chosen,
        "refuted": refuted,
        "result": result,
        "formalization": run.pipeline.get("fr08"),
    }
