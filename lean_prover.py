# -*- coding: utf-8 -*-
"""
lean_prover.py - FR09 chứng minh tự động (đặc tả mục 2.5, 3.2 FR09; QT18, QT19; NFR03-NFR05).

Đầu vào là một yêu cầu chứng minh (ProofRequest):
  - đối tượng (ProofObject): một đích Lean kèm ngữ cảnh: biến, giả thiết, biến do bước Đặt/Chọn đưa vào (giữ đúng biểu
    thức định nghĩa); có thể là mệnh đề đã xác nhận / đang được kiểm trong FR08, hoặc một nghĩa vụ trong khung Lean (FR05);
  - chiều: DUNG (chứng minh đích), SAI (chỉ ra phản ví dụ: một trường hợp cụ thể thỏa mọi giả thiết mà đích sai, tức là
    chứng minh ¬ (∀ ngữ cảnh, đích)), MAU_THUAN (suy ra False từ ngữ cảnh);
  - chế độ: TIM (tìm chứng minh, dùng cho FR01 và FR08) hoặc KIEM_BUOC (kiểm bước, dùng cho FR05). Bên gọi chọn chế độ,
    FR09 không tự đổi chế độ;
  - danh sách định lý được phép (chỉ chế độ kiểm bước), mức ưu tiên, giới hạn.
Đầu ra (ProofResult): "chứng minh được" kèm chứng minh Lean đã chấp nhận, cách tìm được, tài nguyên đã dùng, số lần thử
và chi phí (chiều sai: kèm phản ví dụ); hoặc "không chứng minh được" kèm lý do dừng và đích còn lại cuối cùng.
FR09 KHÔNG quyết định kết luận nghiệp vụ: việc hiểu kết quả thành nhãn gì do bên gọi (QT06, QT15, QT21) quyết định.

Chế độ tìm chứng minh: thử từ cách rẻ đến cách tốn kém: tactic tự động; LLM viết chứng minh và sửa theo thông báo lỗi
(lượt sửa dùng mô hình mạnh hơn); chia thành các bước trung gian và chứng minh từng bước. Chiều sai: LLM đề xuất phản ví
dụ, Lean phải xác nhận. Có giới hạn lượt gọi LLM cho mỗi yêu cầu (NFR04).
Chế độ kiểm bước: chỉ một bộ tactic cố định; không dùng LLM, không tự chia bước, không dùng lệnh tìm kiếm trong toàn thư
viện (exact?, apply?, …). Định lý được dùng gồm tập bổ đề cơ bản và các định lý bên gọi đưa vào. Chiều sai: thử các giá
trị trên một lưới điểm cố định cho các biến số, Lean kiểm chính xác (giả thiết đúng và đích sai tại điểm đó, bằng
norm_num); không dùng LLM. Giới hạn tính riêng cho từng nghĩa vụ (mỗi nghĩa vụ một định lý riêng với giới hạn heartbeat
riêng), nên kết luận không phụ thuộc thứ tự hay số lượng nghĩa vụ khác.

Điều kiện chấp nhận (QT18): không còn chỗ bỏ trống (sorry), chỉ dựa vào tiên đề chuẩn (#print axioms), đúng mệnh đề đã cố
định (dòng khai báo định lý do hệ thống viết, LLM chỉ viết phần sau `:= by` và bổ đề phụ), không dùng lệnh làm sai lệch
kết quả (khai báo tiên đề, bỏ qua kiểm tra, chạy mã, set_option, …).
Giới hạn chính đo bằng heartbeat của Lean (không phụ thuộc tốc độ máy), kèm giới hạn thời gian thực để phòng treo. Hết
giới hạn thì trả "không chứng minh được" kèm lý do dừng; kết quả này không có nghĩa là đối tượng sai (QT19).
Bộ nhớ đệm: kết quả lưu theo nội dung đối tượng, chiều, chế độ, danh sách định lý được phép, các giới hạn và phiên bản hệ
thống (Lean, Mathlib, cấu hình, prompt, mô hình); đổi phiên bản thì bộ nhớ đệm bị xóa. Mọi chứng minh tìm được ở chế độ
tìm chứng minh được lưu thành file Lean để kiểm lại mà không cần gọi lại LLM (NFR05, recheck_saved).
"""

import hashlib
import itertools
import json
import os
import re
import threading
import time
from dataclasses import asdict, dataclass, field
from typing import Any, Callable, Dict, List, Optional, Tuple

import lean_core as C

DUNG, SAI, MAU_THUAN = "dung", "sai", "mau_thuan"
TIM, KIEM_BUOC = "tim_chung_minh", "kiem_buoc"
DIRECTIONS, MODES = (DUNG, SAI, MAU_THUAN), (TIM, KIEM_BUOC)
# Lý do dừng khi không chứng minh được
STOP_RESOURCE, STOP_ATTEMPTS, STOP_LLM_BUDGET = "het_gioi_han_tai_nguyen", "het_so_lan_thu", "het_han_muc_LLM"
STOP_NOT_APPLICABLE = "khong_ap_dung"

# ---- Cấu hình (ghi vào phiên bản hệ thống; chỉnh trên tập điều chỉnh) ----
SEARCH_HEARTBEATS = int(os.environ.get("MATH_FR09_SEARCH_HEARTBEATS", "400000"))
CHECK_HEARTBEATS = int(os.environ.get("MATH_FR09_CHECK_HEARTBEATS", "100000"))
CHECK_TIMEOUT_SEC = int(os.environ.get("MATH_FR09_CHECK_TIMEOUT", "600"))  # cả file kiểm bước (nhiều nghĩa vụ)
SEARCH_MAX_LLM = int(os.environ.get("MATH_FR09_MAX_LLM", "6"))  # lượt gọi LLM tối đa cho MỘT yêu cầu tìm chứng minh
DECOMPOSE_FILLS = 2  # số lượt LLM viết các bước còn lại sau khi chia bước
# Lượt thử CUỐI CÙNG bằng mô hình mạnh nhất, chỉ khi mọi cách trước (tactic, LLM + sửa, chia bước) đều thất bại; luôn
# được giữ chỗ 1 lượt trong hạn mức LLM của yêu cầu. Chuỗi rỗng: tắt. FR08 (kiểm mâu thuẫn / tương đương) không dùng.
FINAL_MODEL = os.environ.get("MATH_FR09_FINAL_MODEL", "opus").strip()
FINAL_EFFORT = os.environ.get("MATH_FR09_FINAL_EFFORT", "high").strip() or None
# Mô hình viết DÀN Ý khi chia bước (1 lượt, chỉ ở bài khó, quyết định hướng của cả chứng minh); các lượt điền bước
# còn thiếu vẫn dùng C.PROOF_ESCALATE_MODEL. Chuỗi rỗng: dùng C.PROOF_ESCALATE_MODEL như cũ.
SKELETON_MODEL = os.environ.get("MATH_FR09_SKELETON_MODEL", "opus").strip()
SKELETON_EFFORT = os.environ.get("MATH_FR09_SKELETON_EFFORT", "high").strip() or None
CACHE_PATH = os.path.join(C.BASE_DIR, "cache", "fr09_cache.json")
PROOF_DIR = os.path.join(C.BASE_DIR, "verified_lean", "fr09")

# Bộ tactic cố định của chế độ kiểm bước, theo thứ tự thử; {L} là danh sách bổ đề (tập cơ bản + định lý được phép)
CHECK_TACTICS = [
    "norm_num", "simp", "ring_nf", "field_simp", "positivity", "linarith", "nlinarith",
    "norm_num [{L}]", "simp [{L}]", "(field_simp; ring_nf)", "(norm_num [{L}]; linarith)", "(simp [{L}]; nlinarith)",
]
CHECK_CONTRA_TACTICS = ["simp_all", "norm_num at *", "linarith", "nlinarith", "(norm_num at *; linarith)",
                        "(simp_all [{L}])", "(norm_num [{L}] at *; nlinarith)"]
# Mẫu dùng riêng từng định lý mà bước trích dẫn ({T}); tập bổ đề cơ bản chỉ dùng qua {L}
CHECK_THEOREM_TACTICS = ["exact {T}", "(rw [{T}])", "(apply {T} <;> first | assumption | norm_num | positivity | linarith)",
                         "(simp_all [{T}])", "(nlinarith [{T}])"]
BASIC_LEMMAS = [  # đại số sơ cấp, bất đẳng thức cơ bản, giá trị tuyệt đối, min và max
    "sq_nonneg", "sq_abs", "abs_nonneg", "abs_mul", "abs_sub_comm", "abs_abs", "abs_le", "abs_lt", "abs_pos",
    "abs_sub_abs_le_abs_sub", "abs_add_le", "mul_pos", "mul_nonneg", "mul_self_nonneg", "pow_pos", "pow_nonneg",
    "add_sq", "sub_sq", "mul_comm", "min_le_left", "min_le_right", "le_max_left", "le_max_right", "le_min",
    "max_le", "div_pos", "div_nonneg",
]
# Lưới điểm tìm phản ví dụ ở chế độ kiểm bước, theo kiểu của biến (giá trị đơn giản trước)
GRID = {"ℝ": ["0", "1", "-1", "2", "-2", "1/2", "-1/2", "3", "10"], "ℚ": ["0", "1", "-1", "2", "-2", "1/2", "-1/2", "3"],
        "ℤ": ["0", "1", "-1", "2", "-2", "3", "-3"], "ℕ": ["0", "1", "2", "3", "5", "10"]}
GRID_MAX_POINTS = int(os.environ.get("MATH_FR09_GRID_MAX", "48"))

_IDENT_RE = re.compile(r"^[A-Za-z_][\w.'₀-₉]*$")
_RELATION_RE = re.compile(r"[<>≤≥=≠∈∉∣↔→∧∨¬∀∃]|\b(Continuous|Differentiable|HasDerivAt|Tendsto|IsLUB|IsGLB|Is[A-Z]\w*)")
_SORRY_RE = re.compile(r"\bsorry\b")
_HEARTBEAT_RE = re.compile(r"maximum number of heartbeats")
_GOAL_HYP_HINT_RE = re.compile(r"→|∀[^,]*?[∈<>≤≥≠]|\(\s*h\w*\s*:")  # đích có giả thiết (→, ∀ x ∈ S, ∀ ε > 0, …)
_INTRO_LINE_RE = re.compile(r"^(intro|intros|rintro)\b")
USE_CACHE = os.environ.get("MATH_FR09_CACHE", "1") == "1"


# =============================================================================
# Đối tượng, yêu cầu, kết quả
# =============================================================================


@dataclass
class Binder:
    """Một phần tử của ngữ cảnh. kind: "var" (biến), "hyp" (giả thiết), "def" (biến do bước Đặt/Chọn đưa vào, luôn
    bằng biểu thức định nghĩa `expr`: không được chọn tùy ý khi tìm phản ví dụ)."""
    kind: str
    name: str
    type: str
    expr: str = ""
    raw: str = ""  # nhóm binder giữ nguyên văn ({x : ℝ}, [Fintype α], ⦃ε⦄ …): in ra đúng như vậy

    def render(self) -> str:
        if self.raw:
            return self.raw
        if self.kind == "def":
            return f"({self.name} : {self.type}) (hdef_{self.name} : {self.name} = {self.expr})"
        return f"({self.name} : {self.type})"


@dataclass
class ProofObject:
    """Đích Lean kèm ngữ cảnh tại vị trí của nó."""
    goal: str
    context: List[Binder] = field(default_factory=list)
    opens: List[str] = field(default_factory=list)
    imports: List[str] = field(default_factory=list)  # module import thêm ngoài bộ mặc định
    name: str = "fr09_goal"  # tên định lý chính trong file Lean
    code: str = "FR09"  # đặt tên file Lean và ghi nhật ký
    text_vi: str = ""  # phát biểu tiếng Việt (chỉ để LLM hiểu, không ảnh hưởng mệnh đề)
    hint: str = ""  # lời giải tham khảo cho LLM
    context_text: str = ""  # định nghĩa / định lý truy xuất cho LLM
    # Giả thiết nằm TRONG đích (đích dạng ∀ x, H₁ → H₂ → C): chiều mâu thuẫn khi đó là suy ra False từ ngữ cảnh cùng các
    # giả thiết của đích (dùng cho điều kiện (2) của FR08, khi mệnh đề tự lượng hóa mọi đối tượng của đề)
    hyps_in_goal: bool = False
    # Phần mở đầu do HỆ THỐNG (hoặc bộ dữ liệu đánh giá) cung cấp, đặt trước định lý: open, định nghĩa phụ, variable, …
    # LLM không viết phần này (phần LLM viết vẫn bị chặn def/axiom/set_option …)
    preamble: str = ""
    # Tiên đề do chính phần mở đầu khai báo (ví dụ bài nhiều phần của bộ dữ liệu cho kết quả phần trước dưới dạng
    # axiom): được phép xuất hiện trong #print axioms, ngoài các tiên đề chuẩn của Lean (QT18)
    extra_axioms: List[str] = field(default_factory=list)

    def binders(self) -> str:
        return " ".join(b.render() for b in self.context)

    def header(self, direction: str, name: Optional[str] = None) -> List[str]:
        """Hai dòng khai báo định lý, do hệ thống viết (LLM không sửa được)."""
        name, b, goal = name or self.name, self.binders(), self.goal.strip()
        if direction == DUNG or (direction == MAU_THUAN and self.hyps_in_goal):
            # mâu thuẫn với giả thiết trong đích: chứng minh chính đích, nhưng theo khuôn intro … / exfalso / … (_shape)
            return [f"theorem {name} {b} :".replace("  ", " "), f"    {goal} := by"]
        if direction == MAU_THUAN:
            return [f"theorem {name} {b} :".replace("  ", " "), "    False := by"]
        body = f"∀ {b}, {goal}" if b else goal
        return [f"theorem {name} :", f"    ¬ ({body}) := by"]

    def has_hypotheses(self) -> bool:
        return any(b.kind in ("hyp", "def") for b in self.context) or (
            self.hyps_in_goal and bool(_GOAL_HYP_HINT_RE.search(self.goal)))

    def key_text(self) -> str:
        return " | ".join([re.sub(r"\s+", " ", self.binders()), re.sub(r"\s+", " ", self.goal.strip()),
                           " ".join(sorted(set(self.opens))), " ".join(sorted(set(self.imports))),
                           "hyps_in_goal" if self.hyps_in_goal else "", re.sub(r"\s+", " ", self.preamble.strip()),
                           " ".join(sorted(set(self.extra_axioms)))])


def parse_binders(binders: str) -> List[Binder]:
    """Đọc chuỗi binder Lean "(x : ℝ) (hx : 0 < x)" thành ngữ cảnh. Kiểu chứa quan hệ / tên mệnh đề là giả thiết, còn lại
    là biến. Dùng cho ngữ cảnh do hệ thống sinh (tham số và miền của câu hỏi)."""
    out: List[Binder] = []
    for group in C._lean_args(binders, 0, 1000):
        g = group.strip()
        inner = g[1:-1] if g[:1] in "({[⦃" else g
        if ":" not in inner:  # [Fintype α] … : giữ nguyên văn
            out.append(Binder("var", "", "", raw=g))
            continue
        names, ty = inner.split(":", 1)
        kind = "hyp" if _RELATION_RE.search(ty) else "var"
        if g[:1] == "(":
            out += [Binder(kind, n, ty.strip()) for n in names.split()]
        else:  # {x : ℝ}, ⦃ε : ℝ⦄, [h : …]: giữ nguyên kiểu ngoặc (một binder cho cả nhóm)
            out.append(Binder(kind, names.split()[0] if names.split() else "", ty.strip(), raw=g))
    return out


@dataclass
class ProofRequest:
    obj: ProofObject
    direction: str = DUNG
    mode: str = TIM
    allowed: List[str] = field(default_factory=list)  # định lý được phép (chế độ kiểm bước)
    priority: int = C.PRIORITY_FR01
    max_llm_calls: Optional[int] = None  # chế độ tìm chứng minh; None: SEARCH_MAX_LLM
    fixes: Optional[int] = None  # số lượt sửa theo lỗi Lean; None: C.PROOF_FIXES
    decompose: bool = False  # cho phép chia bước trung gian
    try_auto: bool = True  # False khi bên gọi đã biết tactic tự động thất bại
    heartbeats: Optional[int] = None
    model: Optional[str] = None  # mô hình lượt đầu; None: C.LEAN_MODEL
    fix_model: Optional[str] = None  # mô hình các lượt sửa; None: C.PROOF_ESCALATE_MODEL
    # LLM được kết luận "không tìm thấy" (ví dụ: tin rằng giả thiết không mâu thuẫn): dừng sớm, không gọi tiếp
    allow_give_up: bool = False
    # Tên giả thiết trong ngữ cảnh mà chứng minh BẮT BUỘC dùng: hệ thống biên dịch lại đúng chứng minh đó với giả thiết
    # thay bằng True; vẫn đúng thì chứng minh không dùng giả thiết và không được chấp nhận (điều kiện (4) của FR08)
    must_use: str = ""
    # Mô hình của lượt thử cuối; None: FINAL_MODEL; "": không có lượt thử cuối
    final_model: Optional[str] = None


@dataclass
class ProofResult:
    ok: bool
    direction: str
    mode: str
    method: str = ""  # cách tìm được: auto / llm / decompose / tactic: … / luoi
    proof: str = ""
    helper_lemmas: str = ""
    lean_code: str = ""  # file Lean đầy đủ của lần kiểm cuối
    axioms: List[str] = field(default_factory=list)
    counterexample: Optional[Dict[str, str]] = None  # chiều sai: giá trị các biến (Lean đã xác nhận)
    attempts: int = 0  # số lần Lean kiểm một chứng minh
    llm_calls: int = 0
    models: List[str] = field(default_factory=list)
    heartbeats: int = 0
    elapsed_s: float = 0.0
    stop_reason: str = ""
    remaining_goal: str = ""
    last_error: str = ""
    statement_view: str = ""
    proof_path: str = ""
    cached: bool = False
    version: str = ""
    history: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        d["lean_code"] = d["lean_code"][-4000:]
        return d


# =============================================================================
# Phiên bản hệ thống và bộ nhớ đệm
# =============================================================================

_PROMPTS: Dict[str, str] = {}  # điền ở cuối module (để băm vào phiên bản)


def version() -> str:
    """Phiên bản hệ thống của FR09: Lean, Mathlib, cấu hình, prompt, mô hình. Đổi phiên bản thì bộ nhớ đệm bị xóa."""
    parts: Dict[str, Any] = {}
    for fname in ("lean-toolchain", "lake-manifest.json"):
        try:
            with open(os.path.join(C.LEAN_PROJECT, fname), encoding="utf-8") as f:
                parts[fname] = hashlib.sha256(f.read().encode()).hexdigest()[:16]
        except OSError:
            parts[fname] = None
    parts["config"] = [SEARCH_HEARTBEATS, CHECK_HEARTBEATS, SEARCH_MAX_LLM, DECOMPOSE_FILLS, CHECK_TACTICS,
                       CHECK_CONTRA_TACTICS, CHECK_THEOREM_TACTICS, BASIC_LEMMAS, GRID, GRID_MAX_POINTS,
                       C.AUTO_PROVE_TACTICS, C.lean_imports(), sorted(C.ALLOWED_AXIOMS)]
    parts["models"] = [C.LEAN_MODEL, C.PROOF_ESCALATE_MODEL, FINAL_MODEL, FINAL_EFFORT, SKELETON_MODEL, SKELETON_EFFORT]
    parts["prompts"] = hashlib.sha256(json.dumps(_PROMPTS, ensure_ascii=False, sort_keys=True).encode()).hexdigest()[:16]
    return hashlib.sha256(json.dumps(parts, ensure_ascii=False, sort_keys=True).encode()).hexdigest()[:16]


class _Cache:
    """Bộ nhớ đệm FR09 (file JSON). Lưu cả kết quả "không chứng minh được": khóa gồm cả các giới hạn, nên yêu cầu chứng
    minh lại với giới hạn lớn hơn không dùng lại kết quả cũ."""

    def __init__(self, path: str):
        self.path, self._lock, self._data = path, threading.Lock(), None

    def _load(self) -> Dict[str, Any]:
        if self._data is None:
            v = version()
            try:
                with open(self.path, encoding="utf-8") as f:
                    data = json.load(f)
            except (OSError, ValueError):
                data = {}
            self._data = data if data.get("version") == v else {"version": v, "entries": {}, "lemmas": {}}
        return self._data

    def get(self, key: str) -> Optional[Dict[str, Any]]:
        with self._lock:
            return self._load()["entries"].get(key)

    def put(self, key: str, value: Dict[str, Any]) -> None:
        with self._lock:
            self._load()["entries"][key] = value
            self._save()

    def lemmas(self) -> Dict[str, bool]:
        with self._lock:
            return self._load().setdefault("lemmas", {})

    def put_lemmas(self, known: Dict[str, bool]) -> None:
        with self._lock:
            self._load().setdefault("lemmas", {}).update(known)
            self._save()

    def clear(self) -> None:
        with self._lock:
            self._data = {"version": version(), "entries": {}, "lemmas": {}}
            self._save()

    def _save(self) -> None:
        os.makedirs(os.path.dirname(self.path), exist_ok=True)
        tmp = self.path + ".tmp"
        with open(tmp, "w", encoding="utf-8", newline="\n") as f:
            json.dump(self._data, f, ensure_ascii=False)
        os.replace(tmp, self.path)


CACHE = _Cache(CACHE_PATH)


def _request_key(req: ProofRequest) -> str:
    limits = [req.heartbeats or (SEARCH_HEARTBEATS if req.mode == TIM else CHECK_HEARTBEATS)]
    if req.mode == TIM:
        limits += [req.max_llm_calls or SEARCH_MAX_LLM, C.PROOF_FIXES if req.fixes is None else req.fixes,
                   req.decompose, req.try_auto, req.model, req.fix_model, req.allow_give_up, req.must_use,
                   req.final_model]
    raw = json.dumps([version(), req.obj.key_text(), req.direction, req.mode, sorted(set(req.allowed)), limits],
                     ensure_ascii=False)
    return hashlib.sha256(raw.encode()).hexdigest()[:24]


# =============================================================================
# Biên dịch và điều kiện chấp nhận
# =============================================================================


def _file_head(imports: List[str], heartbeats: Optional[int] = None) -> List[str]:
    mods = list(dict.fromkeys(C.lean_imports() + imports))
    head = [*[f"import {m}" for m in mods], "set_option autoImplicit false"]
    if heartbeats:
        head.append(f"set_option maxHeartbeats {heartbeats}")
    return head + [""]


def _search_file(obj: ProofObject, direction: str, proof: str, helper: str, heartbeats: int) -> Tuple[str, int]:
    """File Lean của chế độ tìm chứng minh; trả (mã, số dòng (đếm từ 1) của dòng đầu phần chứng minh)."""
    lines = _file_head(obj.imports, heartbeats)
    lines[0:0] = [f"-- {obj.code}: FR09 ({direction}), Lean 4 + Mathlib; dòng khai báo định lý do hệ thống viết."]
    if obj.opens:
        lines.append("open " + " ".join(dict.fromkeys(obj.opens)))
    if obj.preamble.strip():
        lines += ["", *obj.preamble.strip().splitlines()]
    if helper.strip():
        lines += ["", *helper.strip().splitlines()]
    lines += ["", *obj.header(direction)]
    start = len(lines) + 1
    lines += ["  " + ln for ln in proof.strip().splitlines()]
    lines += ["", f"#print axioms {obj.name}", ""]
    return "\n".join(lines), start


def statement_view(obj: ProofObject, direction: str) -> str:
    """Định lý cần chứng minh, dạng Lean đưa cho LLM (chỗ chứng minh để `sorry`)."""
    opens = "open " + " ".join(dict.fromkeys(obj.opens)) if obj.opens else ""
    return "\n".join([opens, obj.preamble.strip(), "", *obj.header(direction), "  sorry"]).strip("\n")


def _unsolved_goal(errors: List[Tuple[int, str, str]]) -> str:
    for _, _, msg in errors:
        if "unsolved goals" in msg:
            return msg.split("unsolved goals", 1)[1].strip()[:1500]
    return ""


def _judge(res: Dict[str, Any], name: str, lo: int, hi: int, check_axioms: bool = True,
           extra_axioms: Any = ()) -> Dict[str, Any]:
    """Điều kiện chấp nhận (QT18) cho một định lý nằm ở các dòng lo..hi của file đã biên dịch. extra_axioms: tiên đề do
    phần mở đầu của hệ thống khai báo (ProofObject.extra_axioms), được phép ngoài các tiên đề chuẩn."""
    allowed = C.ALLOWED_AXIOMS | set(extra_axioms)
    out = res["output"]
    mine = [m for m in C._split_messages(out) if lo <= m[0] <= hi]
    errors = [m for m in mine if m[1] == "error"]
    problems = []
    if res["infra_error"]:
        problems.append("lỗi hệ thống khi nạp Mathlib")
    if errors:
        problems.append("biên dịch lỗi")
    if any("declaration uses 'sorry'" in m[2] for m in mine):
        problems.append("chứng minh dùng sorry")
    used: set = set()
    if check_axioms and not errors and not res["infra_error"]:
        ax = re.search(rf"'{re.escape(name)}' depends on axioms: \[(.*?)\]", out, re.DOTALL)
        none = f"'{name}' does not depend on any axioms" in out
        used = {a.strip() for a in ax.group(1).split(",")} if ax else set()
        if not (ax or none):
            problems.append("không đọc được kết quả #print axioms")
        if used - allowed:
            problems.append(f"dùng tiên đề ngoài chuẩn: {sorted(used - allowed)}")
    timed_out = res["returncode"] == -1 and "vượt thời gian" in out
    return {"ok": not problems, "problems": problems, "axioms": sorted(used),
            "resource": timed_out or any(_HEARTBEAT_RE.search(m[2]) for m in errors),
            "remaining_goal": _unsolved_goal(errors),
            "errors": "\n".join(re.sub(r"^.*?\.lean:(\d+):", lambda mm: f"dòng {int(mm.group(1)) - lo + 1}:", m[2],
                                       count=1) for m in mine if m[1] != "info")}


def _static(proof: str, helper: str, name: str) -> Optional[str]:
    """Chặn trước khi biên dịch: lệnh có thể làm sai lệch kết quả (QT18), mở/đóng scope, dùng lại tên định lý chính."""
    for part, txt in (("proof", proof), ("helper_lemmas", helper)):
        s = C._strip_comments(txt)
        hit = C._BANNED_RE.search(s) or C._SCOPE_RE.search(s) or re.search(rf"(?<![\w.']){re.escape(name)}(?![\w'])", s)
        if hit:
            return f"phần {part} dùng cấu trúc bị cấm: {hit.group(0)!r}"
    if not proof.strip():
        return "phần proof rỗng"
    return None


def _contra_shape(proof: str) -> Optional[str]:
    """Chiều mâu thuẫn với giả thiết nằm trong đích: chứng minh phải gồm các dòng intro/intros/rintro (đưa giả thiết của
    đích vào ngữ cảnh), rồi đúng một dòng `exfalso`, rồi phần suy ra False. Sau `exfalso` đích là False và chỉ còn ngữ
    cảnh, nên Lean chấp nhận nghĩa là các giả thiết mâu thuẫn; chứng minh thẳng kết luận của đích bị chặn."""
    lines = [ln.strip() for ln in C._strip_comments(proof).splitlines() if ln.strip()]
    k = 0
    while k < len(lines) and _INTRO_LINE_RE.match(lines[k]):
        k += 1
    if k >= len(lines) or lines[k] != "exfalso":
        return "chứng minh phải gồm các dòng intro/intros/rintro, rồi đúng một dòng `exfalso`, rồi phần suy ra False"
    if k + 1 >= len(lines):
        return "thiếu phần suy ra False sau dòng `exfalso`"
    return None


# =============================================================================
# Chế độ tìm chứng minh
# =============================================================================

PROOF_SCHEMA: Dict[str, Any] = {
    "type": "object",
    "properties": {"helper_lemmas": {"type": "string"}, "proof": {"type": "string"}},
    "required": ["helper_lemmas", "proof"], "additionalProperties": False,
}
CEX_SCHEMA: Dict[str, Any] = {
    "type": "object",
    "properties": {"phan_vi_du": {"type": "string"}, "helper_lemmas": {"type": "string"}, "proof": {"type": "string"}},
    "required": ["phan_vi_du", "helper_lemmas", "proof"], "additionalProperties": False,
}


def _schema(direction: str, give_up: bool) -> Dict[str, Any]:
    base = CEX_SCHEMA if direction == SAI else PROOF_SCHEMA
    if not give_up:
        return base
    props = {"tim_duoc": {"type": "boolean"}, "ly_do": {"type": "string"}, **base["properties"]}
    return {**base, "properties": props, "required": list(props)}
PROOF_SYSTEM = """Bạn là chuyên gia Lean 4 và Mathlib (Lean 4.35, Mathlib bản tương ứng). Nhiệm vụ: CHỨNG MINH một định lý Lean 4 + Mathlib đã được cố định. Dòng khai báo định lý do hệ thống viết; KHÔNG được sửa, chỉ viết phần chứng minh.
Bạn viết:
- helper_lemmas: các bổ đề phụ đặt trước định lý chính (chỉ dùng lemma/theorem, có chứng minh đầy đủ) hoặc chuỗi rỗng.
- proof: các dòng tactic thay cho `sorry` sau `:= by` của định lý chính (không viết `by`).
Các namespace trong dòng `open` đã được mở sẵn.

""" + C._BANNED_NOTE
SAI_NOTE = """Định lý cần chứng minh là PHỦ ĐỊNH của phát biểu, tức là chỉ ra một PHẢN VÍ DỤ: một trường hợp cụ thể thỏa MỌI giả thiết mà kết luận sai. Cách thường dùng: `intro h`, áp `h` vào các giá trị cụ thể (kèm chứng minh từng giả thiết tại các giá trị đó), rồi chỉ ra kết luận không đúng (với giới hạn dùng tính duy nhất `tendsto_nhds_unique` cùng giới hạn đúng). Biến có giả thiết dạng `hdef_x : x = …` (do bước Đặt / Chọn đưa vào) phải lấy ĐÚNG giá trị của biểu thức đó, không được chọn tùy ý. Ghi các giá trị đã chọn vào phan_vi_du."""
MAU_THUAN_NOTE = """Định lý cần chứng minh là False từ các giả thiết, tức là chỉ ra các giả thiết MÂU THUẪN nhau (nêu giả thiết nào mâu thuẫn với giả thiết nào trong chứng minh)."""
MAU_THUAN_GOAL_NOTE = """Nhiệm vụ: kiểm xem các GIẢ THIẾT của mệnh đề trên (kể cả biến cố định của định lý và các giả thiết nằm trong mệnh đề, dạng ∀ … → …) có MÂU THUẪN nhau không; giả thiết mâu thuẫn thì mệnh đề nào cũng chứng minh được, nên bản dịch vô nghĩa. Không chứng minh kết luận của mệnh đề. Chứng minh phải theo đúng khuôn: các dòng `intro …` / `intros …` / `rintro …` đặt tên các biến và giả thiết, rồi MỘT dòng `exfalso`, rồi suy ra False CHỈ từ các giả thiết (có thể dùng định lý Mathlib)."""
MUST_USE_NOTE = """Chứng minh PHẢI suy ra kết luận TỪ giả thiết `{name}` (biến đổi, viết lại, áp dụng `{name}`). Hệ thống chạy lại đúng chứng minh đó với `{name} : True`: nếu vẫn đúng (tức là chứng minh kết luận mà không cần `{name}`) thì chứng minh bị loại."""
GIVE_UP_NOTE = """Điền tim_duoc = true và chứng minh nếu bạn tìm được; nếu bạn tin là điều cần chứng minh SAI hoặc không suy ra được (ví dụ các giả thiết không mâu thuẫn, hay hai mệnh đề không cùng nghĩa) thì điền tim_duoc = false, ly_do (giải thích ngắn) và để trống hai trường còn lại."""
FINAL_NOTE = """Đây là LƯỢT THỬ CUỐI CÙNG: các lần viết và sửa chứng minh trước đều bị Lean từ chối (lần gần nhất ở trên). Đừng chỉ vá lỗi cục bộ: xem lại toàn bộ hướng chứng minh, chọn cách chắc chắn nhất (có thể khác hẳn, ví dụ chia thành các bổ đề phụ nhỏ, dùng định lý Mathlib có sẵn), kiểm kỹ tên định lý và kiểu dữ liệu của Lean 4 / Mathlib hiện hành trước khi trả lời."""
_PROMPTS.update(proof=PROOF_SYSTEM, sai=SAI_NOTE, mau_thuan=MAU_THUAN_NOTE, mau_thuan_goal=MAU_THUAN_GOAL_NOTE,
                must_use=MUST_USE_NOTE, give_up=GIVE_UP_NOTE, skeleton=C.SKELETON_NOTE, fill=C.FILL_NOTE,
                final=FINAL_NOTE)


class _Search:
    """Một lần chạy chế độ tìm chứng minh cho một yêu cầu."""

    def __init__(self, req: ProofRequest, log: Optional[Callable[[str], None]]):
        self.req, self.obj = req, req.obj
        self.hb = req.heartbeats or SEARCH_HEARTBEATS
        self.budget = req.max_llm_calls if req.max_llm_calls is not None else SEARCH_MAX_LLM
        self.fixes = C.PROOF_FIXES if req.fixes is None else req.fixes
        self.final = (FINAL_MODEL if req.final_model is None else req.final_model).strip()
        # giữ 1 lượt cho lượt thử cuối (chỉ khi hạn mức còn chỗ cho ít nhất một lượt thường)
        self.reserve = 1 if self.final and self.budget >= 2 else 0
        self.res = ProofResult(ok=False, direction=req.direction, mode=TIM, heartbeats=self.hb,
                               statement_view=statement_view(self.obj, req.direction))
        self._log = log

    def log(self, msg: str) -> None:
        self.res.history.append(msg)
        if self._log:
            self._log(msg)

    def compile(self, proof: str, helper: str) -> Tuple[Dict[str, Any], str, int]:
        code, start = _search_file(self.obj, self.req.direction, proof, helper, self.hb)
        out = C.compile_lean(f"{self.obj.code}-FR09", code)
        if out["infra_error"]:
            raise RuntimeError(C.INFRA_MSG)
        self.res.attempts += 1
        verdict = _judge(out, self.obj.name, 1, code.count("\n") + 1, extra_axioms=self.obj.extra_axioms)
        self.res.lean_code, self.res.last_error = code, ("; ".join(verdict["problems"]) + "\n" + out["output"])[-6000:]
        self.res.remaining_goal = verdict["remaining_goal"] or self.res.remaining_goal
        self.last_resource, self.last_output = verdict["resource"], out["output"]
        return verdict, code, start

    def accept(self, verdict: Dict[str, Any], proof: str, helper: str, method: str) -> Optional[ProofResult]:
        """Chấp nhận chứng minh Lean đã nhận (QT18); với must_use, kiểm thêm khối đối chứng: thay giả thiết bằng True mà
        chứng minh vẫn đúng thì chứng minh không dùng giả thiết và bị loại (trả None)."""
        if self.req.must_use:
            ctx = [Binder(b.kind, b.name, "True", b.expr) if b.name == self.req.must_use else b for b in self.obj.context]
            if ctx == self.obj.context:
                raise ValueError(f"must_use: ngữ cảnh không có giả thiết {self.req.must_use}")
            ctl = ProofObject(**{**asdict(self.obj), "context": ctx})
            code, _ = _search_file(ctl, self.req.direction, proof, helper, self.hb)
            out = C.compile_lean(f"{self.obj.code}-FR09-CTL", code)
            if out["infra_error"]:
                raise RuntimeError(C.INFRA_MSG)
            self.res.attempts += 1
            if _judge(out, self.obj.name, 1, code.count("\n") + 1, extra_axioms=self.obj.extra_axioms)["ok"]:
                self.res.last_error = (f"chứng minh vẫn đúng khi thay {self.req.must_use} bằng True: không dùng giả "
                                       "thiết, không được chấp nhận")
                self.log(self.res.last_error)
                return None
        r = self.res
        r.ok, r.method, r.proof, r.helper_lemmas, r.axioms = True, method, proof, helper, verdict["axioms"]
        r.stop_reason, r.remaining_goal = "", ""
        return r

    def llm(self, previous: Optional[Tuple[str, str]], model: str, note: str = "", effort: Optional[str] = None,
            final: bool = False) -> Optional[Dict[str, Any]]:
        if self.res.llm_calls >= self.budget - (0 if final else self.reserve):
            self.res.stop_reason = STOP_LLM_BUDGET
            return None
        self.res.llm_calls += 1
        self.res.models.append(model)
        req = self.req
        notes = (MAU_THUAN_GOAL_NOTE if req.direction == MAU_THUAN and self.obj.hyps_in_goal
                 else {SAI: SAI_NOTE, MAU_THUAN: MAU_THUAN_NOTE}.get(req.direction, ""))
        parts = [f"Phát biểu:\n{self.obj.text_vi}" if self.obj.text_vi else "",
                 "Định lý cần chứng minh (đã cố định, KHÔNG được sửa; `sorry` là chỗ bạn viết chứng minh):\n```lean\n"
                 + self.res.statement_view + "\n```", notes,
                 MUST_USE_NOTE.format(name=req.must_use) if req.must_use else "",
                 GIVE_UP_NOTE if req.allow_give_up else "",
                 "Các module đã import sẵn: " + ", ".join(dict.fromkeys(C.lean_imports() + self.obj.imports)),
                 self.obj.context_text,
                 f"Lời giải tham khảo (để định hướng chứng minh):\n{self.obj.hint[:3000]}" if self.obj.hint else "",
                 *C._previous_part(previous, "chứng minh"), note]
        out = C._call_structured(PROOF_SYSTEM, "\n\n".join(p for p in parts if p),
                                 _schema(req.direction, req.allow_give_up), model=model, effort=effort)
        if req.direction == SAI and out.get("phan_vi_du"):
            self.claimed_cex = out["phan_vi_du"]
        return out

    def static(self, proof: str, helper: str) -> Optional[str]:
        why = _static(proof, helper, self.obj.name)
        if not why and self.req.direction == MAU_THUAN and self.obj.hyps_in_goal:
            why = _contra_shape(proof)
        return why

    def run(self) -> ProofResult:
        req, obj = self.req, self.obj
        self.claimed_cex, self.last_resource, self.last_output = "", False, ""
        if req.direction == MAU_THUAN and not obj.has_hypotheses():
            self.res.stop_reason = STOP_NOT_APPLICABLE
            self.log("Mâu thuẫn: ngữ cảnh không có giả thiết nào")
            return self.res
        # (1) tactic tự động, không gọi LLM
        if C.AUTO_PROVE and req.try_auto:
            auto = C.AUTO_PROOF
            if req.direction == MAU_THUAN and obj.hyps_in_goal:
                auto = "intros\nexfalso\n" + "first\n" + "\n".join(
                    f"  | ({t}; done)" for t in CHECK_CONTRA_TACTICS if "{L}" not in t)
            verdict, _, _ = self.compile(auto, "")
            if verdict["ok"]:
                acc = self.accept(verdict, auto, "", "auto")
                if acc is not None:
                    self.log("Tactic tự động chứng minh được")
                    return self._finish(acc)
            else:
                self.log("Tactic tự động: không chứng minh được")
        # (2) LLM viết chứng minh, sửa theo lỗi Lean (lượt sửa dùng mô hình mạnh hơn)
        first_model = req.model or C.LEAN_MODEL
        fix_model = req.fix_model or C.PROOF_ESCALATE_MODEL or first_model
        previous: Optional[Tuple[str, str]] = None
        for attempt in range(1, self.fixes + 2):
            model = fix_model if attempt > 1 else first_model
            pf = self.llm(previous, model)
            if pf is None:
                break
            if req.allow_give_up and not pf.get("tim_duoc", True):
                self.res.last_error = f"LLM kết luận không tìm thấy: {pf.get('ly_do', '')[:400]}"
                self.res.stop_reason = STOP_ATTEMPTS
                self.log(f"LLM lần {attempt} ({model}): {self.res.last_error}")
                return self._finish(self.res)
            why = self.static(pf["proof"], pf["helper_lemmas"])
            if why:
                previous = (json.dumps(pf, ensure_ascii=False, indent=1), f"Bị chặn trước khi biên dịch: {why}")
                self.log(f"LLM lần {attempt}: {previous[1]}")
                continue
            verdict, code, _ = self.compile(pf["proof"], pf["helper_lemmas"])
            if verdict["ok"]:
                acc = self.accept(verdict, pf["proof"], pf["helper_lemmas"], "llm")
                if acc is None:  # chứng minh không dùng giả thiết bắt buộc: không phải lỗi sửa được, dừng
                    self.res.stop_reason = STOP_ATTEMPTS
                    return self._finish(self.res)
                self.log(f"LLM lần {attempt} ({model}): Lean chấp nhận")
                return self._finish(acc)
            previous = (C._numbered(code), self.res.last_error)
            self.log(f"LLM lần {attempt} ({model}): Lean: {'; '.join(verdict['problems'])}")
        # (3) chia bước trung gian
        if req.decompose and self.res.stop_reason != STOP_LLM_BUDGET:
            dec = self.decompose(previous)
            if dec is not None:
                return self._finish(dec)
        # (4) lượt thử cuối bằng mô hình mạnh nhất (đã giữ chỗ trong hạn mức)
        if self.final:
            fin = self.final_attempt(previous)
            if fin is not None:
                return self._finish(fin)
        if not self.res.stop_reason:
            self.res.stop_reason = STOP_RESOURCE if self.last_resource else STOP_ATTEMPTS
        return self._finish(self.res)

    def final_attempt(self, previous: Optional[Tuple[str, str]]) -> Optional[ProofResult]:
        """Một lượt LLM bằng FINAL_MODEL, nhận lần thử lỗi gần nhất của vòng sửa; Lean chấm như mọi lượt khác."""
        pf = self.llm(previous, self.final, FINAL_NOTE, effort=FINAL_EFFORT, final=True)
        if pf is None:
            return None
        label = f"Lượt cuối ({self.final})"
        if self.req.allow_give_up and not pf.get("tim_duoc", True):
            self.log(f"{label}: LLM kết luận không tìm thấy: {pf.get('ly_do', '')[:400]}")
            return None
        why = self.static(pf["proof"], pf["helper_lemmas"])
        if why:
            self.log(f"{label}: bị chặn trước khi biên dịch: {why}")
            return None
        verdict, _, _ = self.compile(pf["proof"], pf["helper_lemmas"])
        if verdict["ok"]:
            acc = self.accept(verdict, pf["proof"], pf["helper_lemmas"], "llm_final")
            if acc is not None:
                self.log(f"{label}: Lean chấp nhận")
            return acc
        self.log(f"{label}: Lean: {'; '.join(verdict['problems'])}")
        return None

    def decompose(self, previous: Optional[Tuple[str, str]]) -> Optional[ProofResult]:
        """LLM viết khung `have … := by sorry`; hệ thống thay mọi `sorry` bằng tactic tự động, Lean chỉ ra bước nào chưa
        chứng minh được; LLM viết các bước đó."""
        model = C.PROOF_ESCALATE_MODEL or C.LEAN_MODEL  # mô hình điền các bước còn thiếu
        sk = self.llm(previous, SKELETON_MODEL or model, C.SKELETON_NOTE,
                      effort=SKELETON_EFFORT if SKELETON_MODEL else None)
        if sk is None:
            return None
        proof, helper = sk["proof"].strip(), sk["helper_lemmas"]
        if not _SORRY_RE.search(proof) or _SORRY_RE.search(helper):
            self.log("Chia bước: khung không hợp lệ (không có bước `have … := by sorry` hoặc bổ đề phụ dùng sorry)")
            return None
        why = self.static(_SORRY_RE.sub("trivial", proof), helper)
        if why:
            self.log(f"Chia bước: khung bị chặn trước khi biên dịch: {why}")
            return None
        slot_idx = [proof[:m.start()].count("\n") for m in _SORRY_RE.finditer(proof)]
        auto_proof = _SORRY_RE.sub(C._AUTO_INLINE, proof)
        verdict, code, start = self.compile(auto_proof, helper)
        if verdict["ok"]:
            return self.accept(verdict, auto_proof, helper, "decompose")
        slot_lines = [start + i for i in slot_idx]
        errors = [m for m in C._split_messages(self.last_output) if m[1] == "error"]
        if not errors or any(m[0] not in slot_lines for m in errors):
            self.log("Chia bước: khung chứng minh lỗi ngoài các bước have")
            return None
        failing = {m[0] for m in errors}
        pieces = _SORRY_RE.split(proof)
        partial = pieces[0] + "".join(("sorry" if slot_lines[j] in failing else C._AUTO_INLINE) + pieces[j + 1]
                                      for j in range(len(slot_lines)))
        self.log(f"Chia bước: tactic tự động chứng minh được {len(slot_lines) - len(failing)}/{len(slot_lines)} bước")
        partial_code, _ = _search_file(self.obj, self.req.direction, partial, helper, self.hb)
        previous = (C._numbered(partial_code), "Các bước còn `sorry` (thông báo của Lean khi thử tactic tự động):\n"
                    + "\n".join(m[2] for m in errors)[-4000:])
        for _ in range(DECOMPOSE_FILLS):
            pf = self.llm(previous, model, C.FILL_NOTE)
            if pf is None:
                return None
            why = self.static(pf["proof"], pf["helper_lemmas"])
            if why:
                previous = (json.dumps(pf, ensure_ascii=False, indent=1), f"Bị chặn trước khi biên dịch: {why}")
                continue
            verdict, code, _ = self.compile(pf["proof"], pf["helper_lemmas"])
            if verdict["ok"]:
                return self.accept(verdict, pf["proof"], pf["helper_lemmas"], "decompose")
            previous = (C._numbered(code), self.res.last_error)
        self.log("Chia bước: vẫn còn bước chưa chứng minh được")
        return None

    def _finish(self, r: ProofResult) -> ProofResult:
        if r.ok and self.req.direction == SAI:
            r.counterexample = {"mo_ta_cua_LLM": self.claimed_cex} if self.claimed_cex else {}
        return r


# =============================================================================
# Chế độ kiểm bước
# =============================================================================


def known_lemmas(names: List[str], imports: List[str]) -> Dict[str, bool]:
    """Tên định lý nào có trong Mathlib/MathExam của phiên bản hiện tại (kiểm bằng `#check`, lưu vào bộ nhớ đệm)."""
    names = list(dict.fromkeys(n for n in names if n))
    have = CACHE.lemmas()
    tag = "|".join(sorted(set(imports)))
    todo = [n for n in names if f"{tag}::{n}" not in have and _IDENT_RE.match(n)]
    if todo:
        lines = _file_head(imports)
        marks = {}
        for n in todo:
            marks[n] = len(lines) + 1
            lines.append(f"#check @{n}")
        res = C.compile_lean("FR09-LEMMAS", "\n".join(lines) + "\n", timeout_sec=CHECK_TIMEOUT_SEC)
        if res["infra_error"]:
            raise RuntimeError(C.INFRA_MSG)
        bad = {m[0] for m in C._split_messages(res["output"]) if m[1] == "error"}
        CACHE.put_lemmas({f"{tag}::{n}": marks[n] not in bad for n in todo})
        have = CACHE.lemmas()
    return {n: bool(_IDENT_RE.match(n) and have.get(f"{tag}::{n}")) for n in names}


def _check_tactics(req: ProofRequest, lemmas: List[str], theorems: List[str]) -> List[str]:
    base = CHECK_CONTRA_TACTICS if req.direction == MAU_THUAN else CHECK_TACTICS
    L = ", ".join(lemmas)
    tactics = [t.replace("{L}", L) for t in base if "{L}" not in t or L]
    if req.direction == DUNG:
        tactics += [t.replace("{T}", th) for th in theorems for t in CHECK_THEOREM_TACTICS]
    return list(dict.fromkeys(tactics))


_NUMERIC = set(GRID)


def _grid_points(obj: ProofObject) -> Optional[List[Dict[str, str]]]:
    """Các điểm trên lưới cho biến số tự do (biến do Đặt/Chọn không được chọn: lấy theo biểu thức định nghĩa).
    None nếu ngữ cảnh có biến không phải số (hàm, tập, …): không tìm phản ví dụ bằng lưới."""
    free = [b for b in obj.context if b.kind == "var"]
    if any(b.type.strip() not in _NUMERIC for b in free):
        return None
    choices = [[(b.name, f"({v} : {b.type.strip()})") for v in GRID[b.type.strip()]] for b in free]
    points = sorted(itertools.product(*choices),
                    key=lambda pt: sum(GRID[b.type.strip()].index(v.split(" : ")[0][1:]) for b, (_, v) in zip(free, pt)))
    return [dict(pt) for pt in points[:GRID_MAX_POINTS]]


def _cex_proof(obj: ProofObject, point: Dict[str, str]) -> str:
    """Chứng minh ¬ (∀ ngữ cảnh, đích) tại một điểm: giả thiết kiểm bằng norm_num, biến Đặt/Chọn lấy đúng biểu thức (rfl)."""
    args = []
    for b in obj.context:
        if b.kind == "var":
            args.append(point[b.name])
        elif b.kind == "def":
            args += ["_", "rfl"]
        else:
            args.append("(by norm_num)")
    return "\n".join(["intro h", f"have hcex := h {' '.join(args)}".rstrip(), "norm_num at hcex"])


def check_obligations(reqs: List[ProofRequest]) -> List[ProofResult]:
    """Chế độ kiểm bước cho nhiều nghĩa vụ trong MỘT file Lean (Mathlib nạp một lần). Mỗi (nghĩa vụ, cách thử) là một
    định lý riêng với giới hạn heartbeat riêng, nên kết luận của nghĩa vụ không phụ thuộc các nghĩa vụ khác."""
    results: List[Optional[ProofResult]] = [None] * len(reqs)
    todo = []
    for i, req in enumerate(reqs):
        assert req.mode == KIEM_BUOC and req.direction in DIRECTIONS
        key = _request_key(req)
        hit = CACHE.get(key) if USE_CACHE else None
        if hit:
            results[i] = ProofResult(**{**hit, "cached": True})
        else:
            todo.append((i, req, key))
    if not todo:
        return results  # type: ignore[return-value]
    imports = list(dict.fromkeys(m for _, r, _ in todo for m in r.obj.imports))
    lines = _file_head(imports)
    blocks: Dict[int, List[Tuple[str, Any, int, int, str]]] = {}
    for i, req, _ in todo:
        obj, hb = req.obj, req.heartbeats or CHECK_HEARTBEATS
        tries: List[Tuple[str, Any]] = []
        if req.direction == SAI:
            pts = _grid_points(obj)
            tries = [("luoi", pt) for pt in (pts or [])]
        elif req.direction == MAU_THUAN and not any(b.kind in ("hyp", "def") for b in obj.context):
            tries = []
        else:
            known = known_lemmas(BASIC_LEMMAS + req.allowed, imports)
            lemmas = [n for n in dict.fromkeys(BASIC_LEMMAS + req.allowed) if known.get(n)]
            theorems = [n for n in req.allowed if known.get(n)]
            tries = [("tactic", t) for t in _check_tactics(req, lemmas, theorems)]
        blocks[i] = []
        for j, (kind, what) in enumerate(tries):
            # mỗi khối một namespace: định nghĩa của phần mở đầu không trùng tên giữa các khối
            ns, name = f"FR09Chk{i}x{j}", "fr09_chk"
            body = _cex_proof(obj, what) if kind == "luoi" else what
            start = len(lines) + 1
            lines += [f"namespace {ns}", *(["open " + " ".join(dict.fromkeys(obj.opens))] if obj.opens else []),
                      *obj.preamble.strip().splitlines(), f"set_option maxHeartbeats {hb} in",
                      *obj.header(req.direction, name), *["  " + ln for ln in body.splitlines()], f"end {ns}",
                      f"#print axioms {ns}.{name}", ""]
            blocks[i].append((kind, what, start, len(lines), f"{ns}.{name}"))
    t0 = time.perf_counter()
    with C.lean_priority(min(r.priority for _, r, _ in todo)):
        out = C.compile_lean("FR09-CHECK", "\n".join(lines) + "\n", timeout_sec=CHECK_TIMEOUT_SEC)
    if out["infra_error"]:
        raise RuntimeError(C.INFRA_MSG)
    elapsed = round(time.perf_counter() - t0, 1)
    for i, req, key in todo:
        r = ProofResult(ok=False, direction=req.direction, mode=KIEM_BUOC,
                        heartbeats=req.heartbeats or CHECK_HEARTBEATS, elapsed_s=elapsed,
                        statement_view=statement_view(req.obj, req.direction), version=version())
        resource = False
        for kind, what, lo, hi, name in blocks[i]:
            r.attempts += 1
            v = _judge(out, name, lo, hi, extra_axioms=req.obj.extra_axioms)  # QT18 cả ở chế độ kiểm bước
            if v["ok"]:
                r.ok, r.axioms = True, v["axioms"]
                if kind == "luoi":
                    r.method, r.counterexample = "luoi", what
                    r.proof = _cex_proof(req.obj, what)
                else:
                    r.method, r.proof = f"tactic: {what}", what
                r.lean_code = "\n".join(lines[lo - 1:hi])
                break
            resource = resource or v["resource"]
            r.remaining_goal = r.remaining_goal or v["remaining_goal"]
        if not r.ok:
            if not blocks[i]:
                r.stop_reason = STOP_NOT_APPLICABLE
                r.last_error = ("ngữ cảnh có biến không phải số: không tìm phản ví dụ bằng lưới" if req.direction == SAI
                                else "ngữ cảnh không có giả thiết nào")
            else:
                r.stop_reason = STOP_RESOURCE if resource else STOP_ATTEMPTS
        if not out["returncode"] == -1:  # không lưu kết quả khi cả file bị cắt vì quá thời gian thực
            if USE_CACHE:
                CACHE.put(key, {**asdict(r), "cached": False})
        results[i] = r
    return results  # type: ignore[return-value]


# =============================================================================
# API
# =============================================================================


def prove_request(req: ProofRequest, log: Optional[Callable[[str], None]] = None) -> ProofResult:
    """FR09: xử lý một yêu cầu chứng minh theo đúng chế độ bên gọi chọn."""
    if req.direction not in DIRECTIONS or req.mode not in MODES:
        raise ValueError(f"Chiều / chế độ không hợp lệ: {req.direction} / {req.mode}")
    if req.mode == KIEM_BUOC:
        return check_obligations([req])[0]
    key = _request_key(req)
    hit = CACHE.get(key) if USE_CACHE else None
    if hit:
        r = ProofResult(**{**hit, "cached": True})
        if log:
            log(f"FR09: dùng kết quả đã lưu ({'chứng minh được' if r.ok else 'không chứng minh được'})")
        return r
    t0 = time.perf_counter()
    with C.lean_priority(req.priority):
        r = _Search(req, log).run()
    r.elapsed_s, r.version = round(time.perf_counter() - t0, 1), version()
    if r.ok:  # lưu chứng minh để kiểm lại bằng Lean mà không gọi lại LLM (NFR05)
        os.makedirs(PROOF_DIR, exist_ok=True)
        r.proof_path = os.path.join(PROOF_DIR, f"{key}.lean")
        with open(r.proof_path, "w", encoding="utf-8", newline="\n") as f:
            f.write(r.lean_code)
    if USE_CACHE:
        CACHE.put(key, {**asdict(r), "cached": False})
    return r


def recheck_saved(path: str, name: str, extra_axioms: Any = ()) -> Dict[str, Any]:
    """Kiểm lại một chứng minh đã lưu bằng Lean (không gọi LLM): cùng điều kiện chấp nhận như lúc tìm được (QT18)."""
    with open(path, encoding="utf-8") as f:
        code = f.read()
    res = C.compile_lean("FR09-RECHECK", code)
    return _judge(res, name, 1, code.count("\n") + 1, extra_axioms=extra_axioms)
