# -*- coding: utf-8 -*-
"""
lean_retrieval.py - Bước 2 của quy trình formalize: truy xuất định nghĩa và định lý minh họa cho từng khái niệm con.

Hai nguồn truy xuất:
1. Từ điển khái niệm Giải tích I (tiếng Việt -> Lean): mỗi khái niệm giáo trình trỏ tới định nghĩa trong Mathlib
   hoặc thư viện MathExam và các định lý minh họa cách dùng. Tên trong từ điển được đối chiếu với chỉ mục,
   tên nào không tồn tại thì bị bỏ (không đưa tên sai cho LLM).
2. Chỉ mục khai báo (theorem/lemma/def/structure) đọc trực tiếp từ mã nguồn Mathlib và MathExam trong workspace
   Lean, tìm theo từ khóa tiếng Anh mà bước 1 (chuẩn hóa đề) gán cho từng khái niệm.

Mỗi kết quả gồm tên đầy đủ, chữ ký kiểu, docstring và module chứa nó; với định nghĩa, kèm một định lý dùng định
nghĩa đó làm ví dụ cách dùng.
"""

from __future__ import annotations

import json
import os
import re
import threading
from typing import Any, Dict, List, Optional

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LEAN_PROJECT = os.environ.get("MATH_LEAN_PROJECT", r"D:\MATH_EXAM_LEAN")
INDEX_PATH = os.path.join(BASE_DIR, "cache", "lean_decl_index.json")

# Các phần Mathlib liên quan tới Giải tích I (và ma trận cho Hessian/Sylvester)
MATHLIB_DIRS = [
    "Analysis/Calculus", "Analysis/SpecialFunctions", "Analysis/Asymptotics", "Analysis/SpecificLimits",
    "Analysis/Convex", "Topology/Order", "Topology/Algebra/Order", "Topology/Defs", "Topology/NhdsWithin.lean",
    "MeasureTheory/Integral", "MeasureTheory/Measure/Lebesgue", "Order/Filter", "Order/Bounds", "LinearAlgebra/Matrix",
]
CORE_CHECK_PATH = os.path.join(BASE_DIR, "cache", "lean_core_checks.json")

_DECL_RE = re.compile(
    r"^(?:@\[[^\]]*\]\s*)?(?:(?:public|protected|nonrec|noncomputable|private)\s+)*"
    r"(theorem|lemma|def|abbrev|structure|class|irreducible_def)\s+([^\s(:{\[⦃]+)"
)
_NS_RE = re.compile(r"^(namespace|section)\s*([^\s]*)")
_END_RE = re.compile(r"^end\b\s*([^\s]*)")
_DOC_RE = re.compile(r"/--(.*?)-/", re.DOTALL)

# =============================================================================
# Từ điển khái niệm Giải tích I: cụm từ tiếng Việt -> định nghĩa, định lý minh họa, ghi chú cách viết trong Lean
# =============================================================================

CONCEPTS: List[Dict[str, Any]] = [
    {"vi": ["giới hạn hàm", "giới hạn khi x", "lim"], "defs": ["Filter.Tendsto", "nhdsWithin"],
     "examples": ["MathExam.tendsto_div_pow_of_isLittleO", "MathExam.tendsto_div_of_isLittleO"],
     "note": "lim_{x→a} f(x) = L viết `Filter.Tendsto f (𝓝[≠] a) (𝓝 L)` (mở Topology). Dùng 𝓝[≠] a khi f không xác định tại a (Lean coi 0/0 = 0)."},
    {"vi": ["giới hạn trái", "giới hạn phải", "giới hạn một phía"], "defs": ["MathExam.HasLeftLimit", "MathExam.HasRightLimit"],
     "examples": ["MathExam.tendsto_nhdsNE_iff_left_right"], "note": "Giới hạn trái: `Tendsto f (𝓝[<] a) (𝓝 L)`, phải: `𝓝[>] a`."},
    {"vi": ["vô cực", "dần ra vô cùng", "x → +∞", "x → -∞"], "defs": ["Filter.atTop", "Filter.atBot"],
     "examples": [], "note": "x → +∞: `Filter.atTop`; x → -∞: `Filter.atBot`."},
    {"vi": ["giới hạn dãy", "dãy số"], "defs": ["Filter.Tendsto", "Filter.atTop"],
     "examples": ["tendsto_one_div_atTop_nhds_zero_nat"], "note": "lim u_n = L viết `Tendsto (fun n : ℕ => u n) atTop (𝓝 L)`."},
    {"vi": ["khai triển taylor", "khai triển maclaurin", "vô cùng bé bậc cao", "o(x"], "defs": ["Asymptotics.IsLittleO"],
     "examples": ["MathExam.exp_maclaurin", "MathExam.sin_mul_maclaurin", "MathExam.cos_mul_maclaurin",
                  "MathExam.log_one_add_maclaurin", "MathExam.one_add_rpow_maclaurin", "MathExam.arctan_maclaurin",
                  "MathExam.isLittleO_pow_of_le", "MathExam.isLittleO_comp_mul_pow", "taylor_isLittleO_univ"],
     "note": "Khai triển f = P + o(xⁿ) viết `(fun x => f x - P x) =o[𝓝 0] fun x => x ^ n`."},
    {"vi": ["vô cùng bé tương đương", "vcb tương đương", "tương đương"], "defs": ["Asymptotics.IsEquivalent"],
     "examples": ["MathExam.sin_equiv", "MathExam.one_sub_cos_equiv", "MathExam.log_one_add_equiv",
                  "MathExam.tendsto_div_of_isEquivalent"], "note": "f ~ g khi x → 0 viết `f ~[𝓝 0] g`."},
    {"vi": ["vô cùng bé", "vcb", "bậc của vô cùng bé"], "defs": ["MathExam.IsInfinitesimal", "MathExam.IsInfinitesimalOfOrder"],
     "examples": ["MathExam.isInfinitesimalOfOrder_of_isEquivalent", "MathExam.isInfinitesimalOfOrder_of_isLittleO"], "note": ""},
    {"vi": ["liên tục"], "defs": ["ContinuousAt", "Continuous", "ContinuousOn"],
     "examples": ["continuousAt_iff_punctured_nhds", "MathExam.continuousAt_iff_left_right_limit"],
     "note": "Liên tục tại a: `ContinuousAt f a`; trên ℝ: `Continuous f`; trên tập: `ContinuousOn f s`. "
             "Bài 'tìm a để f liên tục' nên phát biểu dạng `ContinuousAt f x₀ ↔ a = ANSWER`."},
    {"vi": ["gián đoạn", "điểm gián đoạn", "khử được", "bước nhảy"],
     "defs": ["MathExam.IsRemovableDiscontinuity", "MathExam.IsJumpDiscontinuity", "MathExam.IsFirstKindDiscontinuity",
              "MathExam.IsSecondKindDiscontinuity"],
     "examples": ["MathExam.isRemovableDiscontinuity_iff", "MathExam.discontinuity_trichotomy"], "note": ""},
    {"vi": ["hàm cho từng khúc", "hàm nhiều công thức", "nếu x"], "defs": [], "examples": [],
     "note": "Hàm cho từng khúc viết `fun x : ℝ => if x = 0 then a else ...` hoặc `if x < 1 then ... else ...`."},
    {"vi": ["đạo hàm", "tiếp tuyến", "hệ số góc"], "defs": ["deriv", "HasDerivAt"],
     "examples": ["HasDerivAt.deriv", "HasDerivAt.comp"], "note": "f'(a) viết `deriv f a`; nên chứng minh qua `HasDerivAt f v a` rồi `.deriv`."},
    {"vi": ["đạo hàm cấp", "đạo hàm cấp cao", "leibniz"], "defs": ["iteratedDeriv"],
     "examples": ["iteratedDeriv_succ", "iteratedDeriv_exp_const_mul"], "note": "f⁽ⁿ⁾(a) viết `iteratedDeriv n f a`."},
    {"vi": ["cực trị", "cực đại", "cực tiểu"], "defs": ["IsLocalMin", "IsLocalMax"],
     "examples": ["isLocalMin_of_deriv_deriv_pos", "isLocalMax_of_deriv_deriv_neg"], "note": ""},
    {"vi": ["giá trị lớn nhất", "giá trị nhỏ nhất", "gtln", "gtnn"], "defs": ["IsGreatest", "IsLeast", "IsMaxOn", "IsMinOn"],
     "examples": ["IsCompact.exists_isMaxOn"],
     "note": "GTLN của f trên S: `IsGreatest (f '' S) ANSWER` hoặc `IsGreatest {y | ∃ x ∈ S, y = f x} ANSWER`."},
    {"vi": ["định lý rolle", "rolle"], "defs": [], "examples": ["exists_deriv_eq_zero"], "note": ""},
    {"vi": ["định lý lagrange", "giá trị trung bình", "số gia hữu hạn"], "defs": [], "examples": ["exists_deriv_eq_slope"], "note": ""},
    {"vi": ["định lý cauchy"], "defs": [], "examples": ["exists_ratio_deriv_eq_ratio_slope"], "note": ""},
    {"vi": ["l'hospital", "lopital", "lôpitan"], "defs": [], "examples": ["deriv.lhopital_zero_nhds", "HasDerivAt.lhopital_zero_nhds"], "note": ""},
    {"vi": ["lồi", "lõm", "điểm uốn"], "defs": ["ConvexOn", "ConcaveOn", "MathExam.IsInflectionPoint"],
     "examples": ["convexOn_of_deriv2_nonneg", "MathExam.isInflectionPoint_of_deriv2_sign"], "note": ""},
    {"vi": ["tiệm cận"], "defs": ["MathExam.IsVerticalAsymptote", "MathExam.IsHorizontalAsymptoteAtTop",
                                  "MathExam.IsSlantAsymptoteAtTop"],
     "examples": ["MathExam.isSlantAsymptoteAtTop_iff"], "note": ""},
    {"vi": ["tích phân xác định", "tích phân"], "defs": ["intervalIntegral"],
     "examples": ["intervalIntegral.integral_eq_sub_of_hasDerivAt", "MathExam.integral_eq_of_hasDerivAt", "integral_pow"],
     "note": "∫_a^b f viết `∫ x in (a:ℝ)..b, f x` (mở intervalIntegral)."},
    {"vi": ["nguyên hàm"], "defs": [], "examples": ["MathExam.integral_eq_of_hasDerivAt"],
     "note": "Bài tìm nguyên hàm phát biểu qua đạo hàm: `∀ x, HasDerivAt F (f x) x` với F là nguyên hàm."},
    {"vi": ["tích phân từng phần"], "defs": [],
     "examples": ["intervalIntegral.integral_mul_deriv_eq_deriv_mul", "MathExam.integral_mul_exp", "MathExam.integral_mul_sin"], "note": ""},
    {"vi": ["đổi biến"], "defs": [], "examples": ["intervalIntegral.integral_comp_mul_deriv"], "note": ""},
    {"vi": ["tích phân suy rộng", "hội tụ", "phân kỳ"], "defs": ["MeasureTheory.IntegrableOn"],
     "examples": ["MeasureTheory.integral_Ioi_of_hasDerivAt_of_tendsto", "integrableOn_Ioi_rpow_iff", "integral_Ioi_rpow_of_lt"],
     "note": "∫_a^{+∞} f viết `∫ x in Set.Ioi a, f x`; hội tụ viết `MeasureTheory.IntegrableOn f (Set.Ioi a)`."},
    {"vi": ["tích phân cận biến thiên", "cận trên biến thiên"], "defs": [],
     "examples": ["intervalIntegral.integral_hasDerivAt_right"], "note": ""},
    {"vi": ["diện tích hình phẳng", "diện tích"], "defs": ["regionBetween", "MathExam.polarRegion"],
     "examples": ["MathExam.area_regionBetween", "MathExam.area_parametric", "MathExam.area_polarRegion"],
     "note": "Diện tích S = `(MeasureTheory.volume S).toReal`."},
    {"vi": ["thể tích", "vật thể tròn xoay"], "defs": ["MathExam.solidOfRevolution"],
     "examples": ["MathExam.volume_real_solidOfRevolution"], "note": ""},
    {"vi": ["độ dài cung", "độ dài đường cong"], "defs": ["MathExam.arcLength", "MathExam.graphCurve", "MathExam.polarCurve"],
     "examples": ["MathExam.arcLength_graph", "MathExam.arcLength_paramCurve", "MathExam.arcLength_polar"], "note": ""},
    {"vi": ["mặt tròn xoay"], "defs": ["MathExam.surfaceArea", "MathExam.revSurface"],
     "examples": ["MathExam.surfaceArea_revSurface"], "note": ""},
    {"vi": ["tọa độ cực"], "defs": ["MathExam.polarRegion", "polarCoord"], "examples": ["MathExam.area_polarRegion"], "note": ""},
    {"vi": ["đạo hàm riêng"], "defs": ["MathExam.partialX", "MathExam.partialY", "MathExam.partialXY"],
     "examples": ["MathExam.partialX_eq_fderiv", "MathExam.partialXY_eq_partialYX"],
     "note": "Hàm hai biến viết `fun p : ℝ × ℝ => ...` với p.1 = x, p.2 = y."},
    {"vi": ["vi phân toàn phần", "tính gần đúng"], "defs": ["fderiv"],
     "examples": ["MathExam.fderiv_apply_eq_partial", "MathExam.totalDiff_approx"], "note": ""},
    {"vi": ["hàm hợp"], "defs": [], "examples": ["MathExam.hasDerivAt_comp_curve", "MathExam.partialX_comp", "HasFDerivAt.comp"], "note": ""},
    {"vi": ["hàm ẩn"], "defs": [], "examples": ["MathExam.hasDerivAt_implicit", "HasStrictFDerivAt.implicitFunction"], "note": ""},
    {"vi": ["đạo hàm theo hướng", "gradient"], "defs": ["lineDeriv", "gradient"], "examples": [], "note": ""},
    {"vi": ["hessian", "cực trị hàm nhiều biến", "điểm dừng"], "defs": ["MathExam.hessianMatrix"],
     "examples": ["MathExam.isLocalMin_of_hessian_two", "MathExam.isLocalMax_of_hessian_two", "MathExam.posDef_two_iff"], "note": ""},
    {"vi": ["nhân tử lagrange", "cực trị có điều kiện"], "defs": [],
     "examples": ["IsLocalExtrOn.exists_multipliers_of_hasStrictFDerivAt"], "note": ""},
    {"vi": ["chuỗi", "tổng chuỗi"], "defs": ["HasSum", "Summable"], "examples": [], "note": "Tổng chuỗi viết `HasSum (fun n : ℕ => a n) ANSWER`."},
]

# =============================================================================
# Chỉ mục khai báo
# =============================================================================

_index: Optional[Dict[str, Any]] = None
_index_lock = threading.Lock()


def _module_of(path: str, root: str) -> str:
    rel = os.path.relpath(path, root)
    return rel[:-5].replace(os.sep, ".")


def _scan_file(path: str, module: str, out: List[Dict[str, Any]]) -> None:
    try:
        text = open(path, encoding="utf-8").read()
    except OSError:
        return
    lines = text.splitlines()
    ns_stack: List[str] = []
    # số dòng (0-based) kết thúc docstring -> nội dung docstring
    docs ={text.count("\n", 0, m.end()): " ".join(m.group(1).split()) for m in _DOC_RE.finditer(text)}
    for i, raw in enumerate(lines):
        line = raw.strip()
        ns = _NS_RE.match(line)
        if ns:
            ns_stack.append(ns.group(2) if ns.group(1) == "namespace" else "")
            continue
        if _END_RE.match(line) and ns_stack:
            ns_stack.pop()
            continue
        if line.startswith("private ") or " private " in line[:30]:
            continue
        dm = _DECL_RE.match(line)
        if not dm:
            continue
        kind, name = dm.group(1), dm.group(2)
        if name.startswith("_root_."):
            full = name[len("_root_."):]
        else:
            prefix = ".".join(p for p in ns_stack if p)
            full = f"{prefix}.{name}" if prefix else name
        sig_lines = [raw.rstrip()]
        for j in range(i + 1, min(i + 8, len(lines))):
            if ":=" in sig_lines[-1] or sig_lines[-1].rstrip().endswith(" where"):
                break
            nxt = lines[j]
            if _DECL_RE.match(nxt.strip()) or not nxt.strip():
                break
            sig_lines.append(nxt.rstrip())
        sig = " ".join(s.strip() for s in sig_lines)
        sig = sig.split(":=")[0].strip()
        doc = docs.get(i - 1, "") or docs.get(i - 2, "")
        out.append({"name": full, "kind": kind, "sig": sig[:400], "doc": doc[:300], "module": module})


def build_index() -> Dict[str, Any]:
    decls: List[Dict[str, Any]] = []
    mathlib_root = os.path.join(LEAN_PROJECT, ".lake", "packages", "mathlib")
    for d in MATHLIB_DIRS:
        base = os.path.join(mathlib_root, "Mathlib", *d.split("/"))
        if base.endswith(".lean"):
            if os.path.exists(base):
                _scan_file(base, _module_of(base, mathlib_root), decls)
            continue
        for dirpath, _, files in os.walk(base):
            for fn in files:
                if fn.endswith(".lean"):
                    p = os.path.join(dirpath, fn)
                    _scan_file(p, _module_of(p, mathlib_root), decls)
    mathexam_dir = os.path.join(LEAN_PROJECT, "MathExam")
    if os.path.isdir(mathexam_dir):
        for fn in sorted(os.listdir(mathexam_dir)):
            if fn.endswith(".lean"):
                p = os.path.join(mathexam_dir, fn)
                _scan_file(p, _module_of(p, LEAN_PROJECT), decls)
    index = {"decls": decls}
    os.makedirs(os.path.dirname(INDEX_PATH), exist_ok=True)
    with open(INDEX_PATH, "w", encoding="utf-8") as f:
        json.dump(index, f, ensure_ascii=False)
    return index


def load_index(rebuild: bool = False) -> Dict[str, Any]:
    """Nạp chỉ mục (xây lại khi chưa có, khi yêu cầu, hoặc khi thư viện MathExam mới hơn bản đã lưu)."""
    global _index
    with _index_lock:
        if _index is not None and not rebuild:
            return _index
        stale = not os.path.exists(INDEX_PATH)
        mathexam_dir = os.path.join(LEAN_PROJECT, "MathExam")
        if not stale and os.path.isdir(mathexam_dir):
            built = os.path.getmtime(INDEX_PATH)
            stale = any(os.path.getmtime(os.path.join(mathexam_dir, fn)) > built
                        for fn in os.listdir(mathexam_dir) if fn.endswith(".lean"))
        if rebuild or stale:
            _index = build_index()
        else:
            with open(INDEX_PATH, encoding="utf-8") as f:
                _index = json.load(f)
        by_name: Dict[str, Dict[str, Any]] = {}
        for d in _index["decls"]:
            by_name.setdefault(d["name"], d)
        _index["by_name"] = by_name
        _index["core"] = {}
        if os.path.exists(CORE_CHECK_PATH):
            with open(CORE_CHECK_PATH, encoding="utf-8") as f:
                _index["core"] = json.load(f).get("verified", {})
        return _index


def _lookup(name: str, index: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Tìm khai báo theo tên đầy đủ, theo hậu tố tên (ví dụ `lhopital_zero_nhds`), hoặc trong danh sách tên
    đã được Lean xác nhận bằng `#check` (các định nghĩa nền tảng sinh bằng macro như `HasSum`, `IsLittleO`)."""
    by_name = index["by_name"]
    if name in by_name:
        return by_name[name]
    for full, d in by_name.items():
        if full.endswith("." + name):
            return d
    core = index.get("core", {})
    if name in core:
        return {"name": name, "kind": "core", "sig": core[name], "doc": "", "module": ""}
    return None


def verify_dictionary() -> Dict[str, Any]:
    """Dùng Lean (`#check`) xác nhận mọi tên trong từ điển khái niệm; lưu chữ ký của các tên hợp lệ.
    Chạy lại sau khi cập nhật Mathlib hoặc từ điển."""
    from lean_core import compile_lean, lean_imports  # import muộn để tránh vòng import

    index = load_index()
    names = sorted({n for e in CONCEPTS for n in e["defs"] + e["examples"]})
    modules = {index["by_name"][n]["module"] for n in names if n in index["by_name"]}
    modules = sorted(m for m in modules if m and m != "MathExam" and not m.startswith("MathExam."))
    src = "\n".join(f"import {m}" for m in dict.fromkeys(lean_imports() + modules)) + "\n\n"
    src += "\n".join(f"#check @{n}" for n in names) + "\n"
    res = compile_lean("RETRIEVAL_DICTIONARY_CHECK", src, timeout_sec=1800)
    out = res["output"]
    verified: Dict[str, str] = {}
    for n in names:
        m = re.search(rf"^@?{re.escape(n)} :(.*?)(?=^\S|\Z)", out, re.MULTILINE | re.DOTALL)
        if m:
            verified[n] = f"{n} :" + " ".join(m.group(1).split())
    missing = [n for n in names if n not in verified]
    os.makedirs(os.path.dirname(CORE_CHECK_PATH), exist_ok=True)
    with open(CORE_CHECK_PATH, "w", encoding="utf-8") as f:
        json.dump({"verified": verified, "missing": missing}, f, ensure_ascii=False, indent=1)
    global _index
    _index = None  # nạp lại ở lần truy xuất sau để dùng danh sách vừa xác nhận
    return {"verified": len(verified), "missing": missing}


_WORD_RE = re.compile(r"[A-Za-z][a-z]*|[A-Z]+(?![a-z])|\d+")


def _tokens(s: str) -> List[str]:
    return [w.lower() for w in _WORD_RE.findall(s.replace("_", " ").replace(".", " "))]


def _usage_example(decl: Dict[str, Any], index: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Định lý minh họa cách dùng một định nghĩa: định lý ngắn nhất có tên định nghĩa trong chữ ký."""
    short = decl["name"].split(".")[-1]
    pat = re.compile(rf"(?<![A-Za-z0-9_]){re.escape(short)}(?![A-Za-z0-9_])")
    best = None
    for d in index["decls"]:
        if d["kind"] not in ("theorem", "lemma") or d["name"] == decl["name"]:
            continue
        if pat.search(d["sig"]) and (best is None or len(d["sig"]) < len(best["sig"])):
            best = d
    return best


def retrieve(concepts: List[Dict[str, Any]], problem_text: str = "", max_items: int = 24) -> Dict[str, Any]:
    """Truy xuất cho danh sách khái niệm con [{vi, lean_keywords}] (từ bước 1) và văn bản đề bài."""
    index = load_index()
    hay = (problem_text + " " + " ".join(c.get("vi", "") for c in concepts)).lower()
    items: List[Dict[str, Any]] = []
    notes: List[str] = []
    seen: set = set()

    def add(decl: Optional[Dict[str, Any]], role: str, concept: str) -> None:
        if decl and decl["name"] not in seen and len(items) < max_items:
            seen.add(decl["name"])
            items.append({**decl, "role": role, "concept": concept})

    # 1. Từ điển khái niệm giáo trình
    for entry in CONCEPTS:
        if not any(k in hay for k in entry["vi"]):
            continue
        if entry["note"]:
            notes.append(f"[{entry['vi'][0]}] {entry['note']}")
        for n in entry["defs"]:
            d = _lookup(n, index)
            add(d, "định nghĩa", entry["vi"][0])
            if d and not entry["examples"]:
                add(_usage_example(d, index), "ví dụ cách dùng", entry["vi"][0])
        for n in entry["examples"]:
            add(_lookup(n, index), "định lý minh họa", entry["vi"][0])

    # 2. Tìm theo từ khóa tiếng Anh trong chỉ mục cho các khái niệm chưa có trong từ điển
    for c in concepts:
        kws = [k.lower() for k in c.get("lean_keywords", []) if k]
        if not kws:
            continue
        kw_tokens = set(t for k in kws for t in _tokens(k))
        scored = []
        for d in index["decls"]:
            name_tokens = set(_tokens(d["name"]))
            score = len(kw_tokens & name_tokens) * 2 + sum(1 for k in kws if k in d["name"].lower())
            # Giải tích I làm việc trên ℝ: ưu tiên MathExam, hạ điểm các kết quả về số phức
            if d["module"].startswith("MathExam"):
                score += 1
            if "Complex" in d["name"] or "ℂ" in d["sig"]:
                score -= 3
            if score >= 2:
                scored.append((score, -len(d["sig"]), d))
        scored.sort(key=lambda t: (t[0], t[1]), reverse=True)
        for _, _, d in scored[:3]:
            add(d, "định nghĩa" if d["kind"] in ("def", "abbrev", "structure", "class") else "định lý liên quan", c.get("vi", ""))
            if d["kind"] in ("def", "abbrev", "structure", "class"):
                add(_usage_example(d, index), "ví dụ cách dùng", c.get("vi", ""))
    return {"items": items, "notes": notes}


_closure_cache: Dict[tuple, set] = {}
_IMPORT_RE = re.compile(r"^\s*(?:public\s+)?import\s+([A-Za-z0-9_.]+)", re.MULTILINE)


def import_closure(imports: List[str]) -> set:
    """Tập module được nạp (trực tiếp hoặc gián tiếp) khi import danh sách `imports`."""
    key = tuple(sorted(imports))
    if key in _closure_cache:
        return _closure_cache[key]
    mathlib_root = os.path.join(LEAN_PROJECT, ".lake", "packages", "mathlib")
    seen: set = set()
    stack = list(imports)
    while stack:
        mod = stack.pop()
        if mod in seen:
            continue
        seen.add(mod)
        root = LEAN_PROJECT if mod.split(".")[0] == "MathExam" else mathlib_root
        path = os.path.join(root, *mod.split(".")) + ".lean"
        if not os.path.exists(path):
            continue
        try:
            head = open(path, encoding="utf-8").read(20000)
        except OSError:
            continue
        stack.extend(m for m in _IMPORT_RE.findall(head) if m.split(".")[0] in ("Mathlib", "MathExam") and m not in seen)
    _closure_cache[key] = seen
    return seen


def _display_sig(it: Dict[str, Any]) -> str:
    """Chữ ký hiển thị với TÊN ĐẦY ĐỦ (kèm namespace) để LLM gọi đúng tên."""
    if it["kind"] == "core":
        return it["sig"]
    short = it["name"].split(".")[-1]
    m = re.search(rf"\b(theorem|lemma|def|abbrev|structure|class|irreducible_def)\s+\S*?{re.escape(short)}\b", it["sig"])
    if not m:
        return f"{it['name']} — {it['sig']}"
    return f"{m.group(1)} {it['name']}{it['sig'][m.end():]}"


def format_context(result: Dict[str, Any], default_imports: List[str]) -> str:
    """Định dạng kết quả truy xuất thành đoạn văn đưa vào prompt formalize."""
    if not result["items"] and not result["notes"]:
        return ""
    loaded = import_closure(default_imports)
    lines = ["Định nghĩa và định lý liên quan tới đề (truy xuất từ Mathlib / MathExam; chỉ dùng đúng các tên này):"]
    for it in result["items"]:
        mod = it["module"]
        imported = mod in loaded
        imp = "" if imported else f"  [cần extra_imports: \"{mod}\"]"
        doc = f"  -- {it['doc']}" if it["doc"] else ""
        lines.append(f"- ({it['role']} · {it['concept']}) {_display_sig(it)}{imp}{doc}")
    if result["notes"]:
        lines.append("Ghi chú cách viết trong Lean:")
        lines.extend(f"- {n}" for n in result["notes"])
    return "\n".join(lines)
