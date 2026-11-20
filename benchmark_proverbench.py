# -*- coding: utf-8 -*-
"""
benchmark_proverbench.py - Đo chức năng lõi FR09 (chứng minh tự động, chế độ tìm chứng minh) trên các bài Giải tích của
ProverBench (DeepSeek-Prover-V2, Ren và cộng sự 2025; dữ liệu deepseek-ai/DeepSeek-ProverBench, 325 bài Lean 4).
Tập con dùng: calculus (90 bài) và real_analysis (30 bài).

FR09 ở chế độ tìm chứng minh là bộ máy mà FR01 dùng để chứng minh đáp án (chiều đúng) và FR08 dùng để kiểm điều kiện
(2) và (4). Mỗi bài ProverBench là một định lý Lean đã cố định: FR09 nhận đúng định lý đó (phần mở đầu của bộ dữ liệu:
định nghĩa phụ, `open`, `axiom` của bài nhiều phần, giữ nguyên), thử tactic tự động -> LLM viết và sửa theo lỗi -> chia
bước. Chứng minh được Lean chấp nhận theo QT18 (không sorry, chỉ tiên đề chuẩn và tiên đề do phần mở đầu khai báo), nên
mọi bài "chứng minh được" đều đúng chắc chắn; chỉ số đo là TỈ LỆ CHỨNG MINH ĐƯỢC trong giới hạn (lượt LLM, heartbeat).

Chia bộ dữ liệu (FR07): ProverBench không có tập điều chỉnh / kiểm tra, nên chia cố định theo băm tên bài (khoảng 1/3 vào
tập điều chỉnh "valid"); các phần của cùng một bài (…_p35_1, …_p35_2) luôn cùng tập. Chỉnh cấu hình chỉ trên valid;
tập test chạy một lần với cấu hình đã chốt.

Các lệnh:
  python benchmark_proverbench.py subset     [--split valid|test|all]
      Liệt kê các bài sẽ chạy và cách chia. Không gọi Lean, không gọi LLM.
  python benchmark_proverbench.py check-refs [--split …]
      Biên dịch từng định lý với chứng minh tạm `sorry` trên Lean/Mathlib của máy (ProverBench viết cho Lean bản cũ hơn);
      bài không biên dịch được bị loại khỏi lượt chạy. Không gọi LLM.
  python benchmark_proverbench.py run        --name TÊN [--split valid] [--direction dung|mau_thuan|sai] [--limit N]
                                             [--ids TÊN_BÀI …] [--env KHÓA=GIÁ_TRỊ …]
      Chạy FR09 cho từng bài, ghi runs/TÊN/results.jsonl; bị ngắt (kể cả hết hạn mức Claude) thì chạy lại cùng lệnh.
      --direction mau_thuan / sai: kiểm tra phụ. Các định lý đúng không thể có giả thiết mâu thuẫn (trừ khi đề hỏng) và
      không thể bị bác bỏ; bài "chứng minh được" ở hai chiều này là đề lỗi của bộ dữ liệu (hoặc lỗi của hệ thống).
  python benchmark_proverbench.py recheck    --name TÊN
      Biên dịch lại mọi chứng minh đã lưu (không gọi LLM), kiểm tái lập (NFR05).
  python benchmark_proverbench.py report     --name TÊN [--json]
      Tỉ lệ chứng minh được (toàn bộ / theo lĩnh vực / theo tập), cách tìm được, lý do dừng, lượt LLM, thời gian.
"""

import argparse
import hashlib
import json
import os
import re
import sys
import threading
import time
from collections import Counter
from datetime import datetime
from typing import Any, Dict, List, Optional

from benchmark_proofnet import (BENCH_EXTRA_IMPORTS, DEFAULT_ENV, MIGRATIONS, _LIMIT_RE, _append_jsonl, _latest,
                                _read_jsonl, _sha256, _versions)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BENCH_DIR = os.path.join(BASE_DIR, "data", "benchmarks", "proverbench")
DATA_PATH = os.path.join(BENCH_DIR, "proverbench.jsonl")
REFCHECK_PATH = os.path.join(BENCH_DIR, "refcheck.json")
RUNS_DIR = os.path.join(BENCH_DIR, "runs")
AREAS = ("calculus", "real_analysis")
VALID_SHARE = 3  # 1/3 nhóm bài vào tập điều chỉnh
# Mặc định riêng của benchmark này (--env vẫn ghi đè được): nhiều lượt sửa theo lỗi Lean hơn chế độ sinh câu hỏi
# (FR01 dùng 2 lượt sửa, trần 6 lượt LLM): 6 lượt sửa, trần 11 lượt LLM mỗi bài = 1 Haiku + 6 Sonnet sửa + chia bước 3 +
# lượt cuối Opus 1. Số liệu valid (2026-11-14): mọi bài chứng minh được đều xong trong <= 7 lượt; 20 lượt sửa không
# chứng minh thêm bài nào mà mỗi bài thất bại tốn ~24 lượt.
PB_DEFAULT_ENV = {"MATH_PROOF_FIXES": "6", "MATH_FR09_MAX_LLM": "11"}
# Module Mathlib thêm cho các bài Giải tích của ProverBench (bỏ qua module không có trong Mathlib của máy)
PB_EXTRA_IMPORTS = BENCH_EXTRA_IMPORTS + [
    "Mathlib.Analysis.Calculus.Taylor", "Mathlib.Analysis.Calculus.LocalExtr.Basic",
    "Mathlib.Analysis.SpecialFunctions.Integrals", "Mathlib.Analysis.SpecialFunctions.Pow.Deriv",
    "Mathlib.Analysis.SpecialFunctions.Trigonometric.ArctanDeriv", "Mathlib.Analysis.Calculus.MeanValue",
    "Mathlib.Topology.MetricSpace.Basic", "Mathlib.Analysis.SpecificLimits.Basic",
]
STATEMENT_RE = re.compile(r"^\s*((?:/-.*?-/\s*)*)(?:theorem|lemma)\s+(\S+)(.*?):=\s*(?:by\s+sorry\s*)?$", re.DOTALL)
AXIOM_RE = re.compile(r"^\s*axiom\s+([^\s(:{\[⦃]+)", re.MULTILINE)

# Bộ dữ liệu thứ hai: các mệnh đề Lean CHUẨN (đã sửa) của ProofNet# phần Giải tích 1 (27 bài: nhóm 'chinh' + 'bien',
# chia valid/test sẵn của ProofNet#). FR09 nhận thẳng mệnh đề tham chiếu (không qua FR08).
DATASET = "proverbench"
PN_DIR = os.path.join(BASE_DIR, "data", "benchmarks", "proofnet_sharp")
# Bài có mệnh đề tham chiếu SAI, tự động bỏ khỏi lượt chạy (chiều dung) và khỏi tỉ lệ trong report, ghi lý do.
# Bốn bài valid có chứng minh Lean của phủ định trong data/benchmarks/proofnet_sharp/de_tham_chieu_sai.lean.
_PN_PROOF = " [Lean chứng minh phủ định: de_tham_chieu_sai.lean]"
KNOWN_FALSE = {
    "proofnet": {
        "Rudin|exercise_5_7": "đề tham chiếu sai: dùng 𝓝 x thay vì 𝓝[≠] x, tại t = x Lean tính 0/0 = 0 nên đòi "
                              "f'(x)/g'(x) = 0 (phản ví dụ f = g = t - x) [phân tích tay]",
        "Rudin|exercise_4_19": "đề tham chiếu sai: giả thiết giá trị trung gian chỉ viết cho f a < c < f b với a < b; "
                               "hàm giảm ngặt có bước nhảy (x<0: -x, x≥0: -x-1) thỏa mọi giả thiết nhưng không liên tục"
                               + _PN_PROOF,
        "Rudin|exercise_5_2": "đề tham chiếu sai: f⁻¹ trong Mathlib là 1/f (nghịch đảo từng điểm), không phải hàm ngược; "
                              "f = id trên (-1, 1) thì 1/x không khả vi tại 0" + _PN_PROOF,
        "Rudin|exercise_5_15": "đề tham chiếu sai: sSup của tập không bị chặn trong ℝ bằng 0 (quy ước Mathlib, Rudin cho "
                               "phép +∞); f = id trên (0, ∞) cho M0 = 0, M1 = 1, M2 = 0 nên 1 ≤ 0" + _PN_PROOF,
        "Rudin|exercise_4_8b": "đề tham chiếu sai (cả đề bằng lời): hàm liên tục đều trên tập BỊ CHẶN của ℝ luôn bị chặn; "
                               "đề gốc của Rudin là E KHÔNG bị chặn" + _PN_PROOF,
    },
}


def _use_dataset(name: str) -> None:
    global DATASET, BENCH_DIR, DATA_PATH, REFCHECK_PATH, RUNS_DIR, AREAS
    DATASET = name
    if name == "proofnet":
        BENCH_DIR = PN_DIR
        DATA_PATH = os.path.join(PN_DIR, "gt1_subset.json")
        REFCHECK_PATH = os.path.join(PN_DIR, "refcheck.json")  # do benchmark_proofnet.py check-refs ghi
        RUNS_DIR = os.path.join(PN_DIR, "runs_fr09")  # tách khỏi runs/ của đánh giá FR08
        AREAS = ("chinh", "bien")


# =============================================================================
# Dữ liệu
# =============================================================================


def _group(name: str) -> str:
    """Các phần của cùng một bài (calculus__p35_1, calculus__p35_2, …) chung một nhóm."""
    return re.sub(r"_\d+$", "", name)


def _splits(rows: List[Dict[str, Any]]) -> Dict[str, str]:
    """Chia cố định theo từng lĩnh vực: các nhóm bài của lĩnh vực xếp theo giá trị băm tên nhóm, cứ VALID_SHARE nhóm thì
    một nhóm vào tập điều chỉnh (valid), còn lại vào tập kiểm tra (test)."""
    out: Dict[str, str] = {}
    for area in AREAS:
        groups = sorted({_group(r["name"]) for r in rows if r["area"] == area},
                        key=lambda g: hashlib.sha256(g.encode()).hexdigest())
        for i, g in enumerate(groups):
            out[g] = "valid" if i % VALID_SHARE == 0 else "test"
    return out


def _migrate(src: str) -> str:
    for pat, rep in MIGRATIONS:
        src = pat.sub(rep, src)
    return src


def load_items(split: str = "all") -> List[Dict[str, Any]]:
    if DATASET == "proofnet":
        import benchmark_proofnet as N

        return [{**it, "area": it["nhom"]} for it in N.load_items(split, include_borderline=True)]
    with open(DATA_PATH, encoding="utf-8") as f:
        rows = [json.loads(ln) for ln in f if ln.strip()]
    split_of = _splits(rows)
    items = [{**r, "id": r["name"], "split": split_of[_group(r["name"])]} for r in rows if r["area"] in AREAS]
    return [it for it in items if split == "all" or it["split"] == split]


def parse_item(it: Dict[str, Any]) -> Dict[str, Any]:
    """Tách định lý ProverBench: tên, các nhóm binder (giữ nguyên văn), đích; phần mở đầu = header bỏ dòng import, kèm
    chú thích đặt trước định lý; tiên đề do header khai báo."""
    if DATASET == "proofnet":
        import benchmark_proofnet as N

        ref = N.parse_reference(it)
        return {"name": ref["name"], "binders": ref["binders"], "goal": ref["concl"],
                "preamble": "\n".join(filter(None, [*ref["opens"], ref["preamble"]])), "axioms": [], "imports": []}
    header, fs = _migrate(it["header"]), _migrate(it["formal_statement"])
    m = STATEMENT_RE.match(fs)
    if not m:
        raise ValueError("không đọc được dòng khai báo định lý")
    doc, name, rest = m.group(1).strip(), m.group(2), m.group(3)
    import lean_core as C

    groups, pos = [], 0
    while True:
        while pos < len(rest) and rest[pos].isspace():
            pos += 1
        if pos >= len(rest) or rest[pos] not in "({[⦃":
            break
        g = C._lean_args(rest, pos, 1)[0]
        groups.append(g)
        pos = rest.index(g, pos) + len(g)
    if pos >= len(rest) or rest[pos] != ":":
        raise ValueError("không tách được binder và đích")
    imports = [ln.split()[1] for ln in header.splitlines() if ln.strip().startswith("import ")]
    body = "\n".join(ln for ln in header.splitlines() if not ln.strip().startswith("import "))
    # ProverBench viết cho Lean mặc định autoImplicit = true (có đề dùng biến chưa khai báo)
    preamble = "\n".join(filter(None, ["set_option autoImplicit true", body.strip(), doc]))
    return {"name": name, "binders": " ".join(groups), "goal": rest[pos + 1:].strip(), "preamble": preamble,
            "axioms": AXIOM_RE.findall(header), "imports": [i for i in imports if i != "Mathlib"]}


def proof_object(it: Dict[str, Any], hint: bool = False):
    """ProofNet#: kèm đề bằng lời (như FR01 có đề tiếng Việt); --hint thêm lời giải bằng lời của bộ dữ liệu."""
    import lean_prover as P

    p = parse_item(it)
    pn = DATASET == "proofnet"
    return P.ProofObject(goal=p["goal"], context=P.parse_binders(p["binders"]), imports=p["imports"],
                         name=p["name"], code=("PN-" if pn else "PB-") + re.sub(r"[^A-Za-z0-9_]", "_", it["id"]),
                         preamble=p["preamble"], extra_axioms=p["axioms"],
                         text_vi=it.get("nl_statement", "") if pn else "",
                         hint=(it.get("nl_proof") or "").strip() if pn and hint else "")


def _load_refcheck() -> Dict[str, Any]:
    if not os.path.exists(REFCHECK_PATH):
        return {}
    with open(REFCHECK_PATH, encoding="utf-8") as f:
        return json.load(f)


# =============================================================================
# Lệnh
# =============================================================================


def cmd_subset(args: argparse.Namespace) -> None:
    items = load_items(args.split)
    ref = _load_refcheck()
    for it in items:
        try:
            p = parse_item(it)
            note = f"{len(p['axioms'])} tiên đề trong header" if p["axioms"] else ""
        except ValueError as exc:
            note = f"KHÔNG ĐỌC ĐƯỢC: {exc}"
        st = ref.get(it["id"], {}).get("ok")
        print(f"[{it['split']:5s}] [{it['area']:13s}] {it['id']:28s} "
              f"{'' if st is None else ('biên dịch được' if st else 'KHÔNG biên dịch được'):22s} {note}")
    c = Counter((it["split"], it["area"]) for it in items)
    print(f"Tổng: {len(items)} bài; " + "; ".join(f"{s}/{a}: {n}" for (s, a), n in sorted(c.items())))


def cmd_check_refs(args: argparse.Namespace) -> None:
    import lean_core as C

    if DATASET == "proofnet":
        raise SystemExit("ProofNet#: kiểm mệnh đề tham chiếu bằng `python benchmark_proofnet.py check-refs "
                         "--split all --include-borderline` (ghi cùng refcheck.json).")
    items = load_items(args.split)
    lines = [*[f"import {m}" for m in C.lean_imports()], ""]
    marks, ref = [], _load_refcheck()
    for n, it in enumerate(items):
        try:
            p = parse_item(it)
        except ValueError as exc:
            ref[it["id"]] = {"ok": False, "error": str(exc)}
            continue
        for mod in p["imports"]:
            lines.insert(0, f"import {mod}")
        start = len(lines) + 1
        lines += [f"namespace PBRef{n}", p["preamble"], f"theorem {p['name']} {p['binders']} :", f"    {p['goal']} := by",
                  "  sorry", f"end PBRef{n}", ""]
        marks.append((it["id"], start, len(lines)))
    code = "\n".join(lines) + "\n"
    print(f"Biên dịch {len(marks)} định lý (chứng minh tạm sorry) trong một file…", flush=True)
    res = C.compile_lean("PROVERBENCH-REFCHECK", code, timeout_sec=3600)
    if res["infra_error"] or res["returncode"] == -1:
        raise SystemExit(f"Lỗi hạ tầng / quá thời gian khi chạy Lean: {res['output'][-800:]}")
    # dòng của từng khối tính lại sau khi chèn import lên đầu file
    shift = sum(1 for ln in lines if ln.startswith("import ")) - len(C.lean_imports())
    msgs = C._split_messages(res["output"])
    ok_n = 0
    for rid, lo, hi in marks:
        errs = [m for m in msgs if m[1] == "error" and lo + shift <= m[0] <= hi + shift]
        ref[rid] = {"ok": not errs, "error": errs[0][2][:400] if errs else ""}
        ok_n += not errs
    with open(REFCHECK_PATH, "w", encoding="utf-8", newline="\n") as f:
        json.dump(ref, f, ensure_ascii=False, indent=1)
    print(f"Biên dịch được {ok_n}/{len(marks)}; ghi {REFCHECK_PATH}")
    for rid, v in ref.items():
        if not v["ok"] and any(rid == m[0] for m in marks):
            print(f"  KHÔNG biên dịch được: {rid}: {v['error'][:200]}")


def _run_config(args: argparse.Namespace, items: List[Dict[str, Any]]) -> Dict[str, Any]:
    import lean_core as C
    import lean_prover as P

    return {
        "dataset": DATASET, "hint": bool(getattr(args, "hint", False)),
        "split": args.split, "direction": args.direction, "env_overrides": dict(args.env_pairs),
        "llm": {"provider": os.environ.get("MATH_LLM_PROVIDER"), "model": C.LEAN_MODEL,
                "proof_escalate_model": C.PROOF_ESCALATE_MODEL, "effort": os.environ.get("MATH_LLM_EFFORT")},
        "fr09": {"version": P.version(), "max_llm_calls": P.SEARCH_MAX_LLM, "fixes": C.PROOF_FIXES,
                 "decompose": C.DECOMPOSE, "auto": C.AUTO_PROVE, "heartbeats": P.SEARCH_HEARTBEATS,
                 "final_model": P.FINAL_MODEL, "final_effort": P.FINAL_EFFORT,
                 "skeleton_model": P.SKELETON_MODEL, "skeleton_effort": P.SKELETON_EFFORT,
                 "cache": os.environ.get("MATH_FR09_CACHE", "1")},
        "lean_imports": C.lean_imports(), "versions": _versions(), "data_sha256": _sha256(DATA_PATH),
        "items": [it["id"] for it in items],
    }


def _false_items(run_names: List[str], split: str) -> Dict[str, str]:
    """Bài có đề SAI đã được Lean xác nhận: chứng minh được ¬(đề) trong một lượt chạy chiều `sai`."""
    out: Dict[str, str] = {}
    for name in run_names:
        run_dir = os.path.join(RUNS_DIR, name)
        cfg_path = os.path.join(run_dir, "config.json")
        if not os.path.exists(cfg_path):
            raise SystemExit(f"--exclude-false: không có lượt chạy '{name}'")
        with open(cfg_path, encoding="utf-8") as f:
            if json.load(f).get("direction") != "sai":
                raise SystemExit(f"--exclude-false: lượt '{name}' không chạy chiều sai (--direction sai)")
        for r in _latest(_read_jsonl(os.path.join(run_dir, "results.jsonl"))):
            if r["status"] == "PROVED":
                out[r["id"]] = f"đề sai: Lean chứng minh được phủ định ({name}, {r.get('proof_path', '')})"
    return out


def cmd_run(args: argparse.Namespace) -> None:
    import lean_core as C
    import lean_prover as P

    items = load_items(args.split)
    if args.ids:
        items = [it for it in items if it["id"] in set(args.ids)]
    if getattr(args, "first", 0):
        items = items[: args.first]
    excluded = _false_items(getattr(args, "exclude_false", None) or [], args.split)
    excluded.update({i: "bỏ qua theo --skip" for i in (getattr(args, "skip", None) or [])})
    if args.direction == "dung":
        excluded.update(KNOWN_FALSE.get(DATASET, {}))
    if excluded:
        skipped = [it["id"] for it in items if it["id"] in excluded]
        items = [it for it in items if it["id"] not in excluded]
        print(f"Bỏ {len(skipped)} bài đề sai / bỏ qua: {skipped}")
    ref = _load_refcheck()
    if not args.skip_refcheck:
        if not ref:
            raise SystemExit("Chưa kiểm định lý: chạy `check-refs` trước (hoặc --skip-refcheck).")
        bad = [it["id"] for it in items if not ref.get(it["id"], {}).get("ok")]
        items = [it for it in items if it["id"] not in bad]
        if bad:
            print(f"Bỏ {len(bad)} bài không biên dịch được / chưa kiểm: {bad}")
    run_dir = os.path.join(RUNS_DIR, args.name)
    os.makedirs(run_dir, exist_ok=True)
    cfg_path, res_path = os.path.join(run_dir, "config.json"), os.path.join(run_dir, "results.jsonl")
    cfg = _run_config(args, items)
    if os.path.exists(cfg_path):
        with open(cfg_path, encoding="utf-8") as f:
            old = json.load(f)
        old.setdefault("dataset", "proverbench")
        old.setdefault("hint", False)
        if any(old.get(k) != cfg.get(k) for k in ("dataset", "hint", "direction", "env_overrides", "llm", "fr09",
                                                   "lean_imports", "versions", "data_sha256")):
            raise SystemExit(f"Lượt chạy '{args.name}' đã có với cấu hình khác: đặt tên mới để kết quả tái lập được.")
    else:
        with open(cfg_path, "w", encoding="utf-8", newline="\n") as f:
            json.dump(cfg, f, ensure_ascii=False, indent=1)
    if excluded:
        ex_path = os.path.join(run_dir, "excluded.json")
        old_ex = json.load(open(ex_path, encoding="utf-8")) if os.path.exists(ex_path) else {}
        old_ex.update({i: excluded[i] for i in skipped})
        with open(ex_path, "w", encoding="utf-8", newline="\n") as f:
            json.dump(old_ex, f, ensure_ascii=False, indent=1)
    done ={r["id"] for r in _latest(_read_jsonl(res_path)) if r["status"] != "ERROR"}
    todo = [it for it in items if it["id"] not in done][: args.limit or None]
    print(f"Lượt chạy '{args.name}' (FR09, chiều {args.direction}): {len(done)} bài đã xong, chạy {len(todo)} bài; "
          f"mô hình {C.LEAN_MODEL} -> {C.PROOF_ESCALATE_MODEL}, tối đa {P.SEARCH_MAX_LLM} lượt LLM/bài", flush=True)
    C.ensure_mathlib()
    calls: Counter = Counter()
    lock = threading.Lock()
    original = C._call_structured

    def counted(system: str, user: str, schema: Dict[str, Any], model: Optional[str] = None,
                effort: Optional[str] = None) -> Dict[str, Any]:
        with lock:
            calls[model or "?"] += 1
        return original(system, user, schema, model=model, effort=effort)

    C._call_structured = counted
    try:
        for n, it in enumerate(todo, 1):
            calls.clear()
            t0 = time.perf_counter()
            row: Dict[str, Any] = {"id": it["id"], "area": it["area"], "split": it["split"], "direction": args.direction}
            try:
                req = P.ProofRequest(proof_object(it, getattr(args, "hint", False)), direction=args.direction, mode=P.TIM,
                                     priority=C.PRIORITY_FR01, decompose=C.DECOMPOSE)
                r = P.prove_request(req)
                row.update({"status": "PROVED" if r.ok else "NOT_PROVED", "method": r.method,
                            "attempts": r.attempts, "stop_reason": r.stop_reason,
                            "remaining_goal": r.remaining_goal[:600], "last_error": "" if r.ok else r.last_error[-600:],
                            "axioms": r.axioms, "proof_path": r.proof_path, "history": r.history})
            except Exception as exc:
                msg = f"{type(exc).__name__}: {exc}"
                if _LIMIT_RE.search(msg):
                    raise SystemExit(f"Dừng ở bài {it['id']} ({n}/{len(todo)}): hết hạn mức / giới hạn tốc độ của Claude."
                                     f"\n  {msg[:300]}\n  Kết quả {n - 1} bài trước đã được lưu; chạy lại đúng lệnh này để "
                                     f"làm tiếp.")
                row.update({"status": "ERROR", "error": msg[:1000]})
            row.update({"llm_calls": dict(calls), "elapsed_s": round(time.perf_counter() - t0, 1),
                        "finished_at": datetime.now().isoformat(timespec="seconds")})
            _append_jsonl(res_path, row)
            print(f"  [{n}/{len(todo)}] {it['id']:28s} {row['status']:11s} {row.get('method', ''):10s} "
                  f"{row['elapsed_s']:6.0f}s LLM={sum(calls.values())}", flush=True)
            if row["status"] == "ERROR" and "Mathlib" in row.get("error", ""):
                raise SystemExit(f"Dừng: {row['error']}")
    finally:
        C._call_structured = original


def cmd_recheck(args: argparse.Namespace) -> None:
    import lean_prover as P

    run_dir = os.path.join(RUNS_DIR, args.name)
    rows = [r for r in _latest(_read_jsonl(os.path.join(run_dir, "results.jsonl"))) if r["status"] == "PROVED"]
    items = {it["id"]: it for it in load_items("all")}
    ok = 0
    for r in rows:
        p = parse_item(items[r["id"]])
        v = P.recheck_saved(r["proof_path"], p["name"], p["axioms"])
        ok += v["ok"]
        print(f"  {r['id']:28s} {'OK' if v['ok'] else 'LỖI: ' + '; '.join(v['problems'])}", flush=True)
    print(f"Kiểm lại không cần LLM: {ok}/{len(rows)} chứng minh vẫn được Lean chấp nhận")


def _pct(a: int, b: int) -> Optional[float]:
    return round(100.0 * a / b, 1) if b else None


def cmd_report(args: argparse.Namespace) -> None:
    run_dir = os.path.join(RUNS_DIR, args.name)
    rows = _latest(_read_jsonl(os.path.join(run_dir, "results.jsonl")))
    # bài có đề tham chiếu sai (KNOWN_FALSE) đã chạy trước khi được phát hiện: không tính vào tỉ lệ chiều dung
    cfg_path = os.path.join(run_dir, "config.json")
    direction = json.load(open(cfg_path, encoding="utf-8")).get("direction") if os.path.exists(cfg_path) else "dung"
    kf = KNOWN_FALSE.get(DATASET, {}) if direction == "dung" else {}
    raw = rows
    rows = [r for r in raw if r["id"] not in kf]
    late = {r["id"]: (kf[r["id"]], r["status"]) for r in raw if r["id"] in kf}

    def metrics(rs: List[Dict[str, Any]]) -> Dict[str, Any]:
        n = len(rs)
        proved = [r for r in rs if r["status"] == "PROVED"]
        calls: Counter = Counter()
        for r in rs:
            calls.update(r.get("llm_calls", {}))
        return {"so_bai": n, "chung_minh_duoc": len(proved), "ti_le_%": _pct(len(proved), n),
                "loi": sum(r["status"] == "ERROR" for r in rs),
                "cach_tim": dict(Counter(r.get("method", "") for r in proved)),
                "ly_do_dung": dict(Counter(r.get("stop_reason", "") for r in rs if r["status"] == "NOT_PROVED")),
                "luot_LLM_trung_binh": {m: round(c / n, 2) for m, c in calls.items()} if n else {},
                "thoi_gian_trung_binh_s": round(sum(r.get("elapsed_s", 0) for r in rs) / n, 1) if n else None}

    summary = {"luot_chay": args.name, "toan_bo": metrics(rows), "tho_truoc_khi_loai_de_sai": metrics(raw),
               "de_sai_da_loai": {i: why for i, (why, _) in late.items()},
               "theo_linh_vuc": {a: metrics([r for r in rows if r["area"] == a]) for a in AREAS
                                 if any(r["area"] == a for r in rows)},
               "theo_tap": {s: metrics([r for r in rows if r["split"] == s]) for s in ("valid", "test")
                            if any(r["split"] == s for r in rows)},
               "luu_y": "Mọi bài 'chứng minh được' đã được Lean kiểm (QT18), nên không có chứng minh sai; chỉ số là tỉ lệ "
                        "chứng minh được trong giới hạn lượt LLM và heartbeat. Chỉ đo chế độ tìm chứng minh của FR09."}
    with open(os.path.join(run_dir, "summary.json"), "w", encoding="utf-8", newline="\n") as f:
        json.dump(summary, f, ensure_ascii=False, indent=1)
    if args.json:
        print(json.dumps(summary, ensure_ascii=False, indent=1))
        return
    cols = [("Toàn bộ", summary["toan_bo"]), *[(a, m) for a, m in summary["theo_linh_vuc"].items()]]
    w0, w = 34, 14
    line = "-" * (w0 + w * len(cols))
    print(f"\nBÁO CÁO FR09 TRÊN {'PROOFNET# (GT1)' if DATASET == 'proofnet' else 'PROVERBENCH'}: {args.name}\n{line}")
    print("Chỉ số".ljust(w0) + "".join(c.rjust(w) for c, _ in cols))
    print(line)
    for label, key in (("Số bài", "so_bai"), ("Chứng minh được", "chung_minh_duoc"), ("Tỉ lệ chứng minh được (%)", "ti_le_%"),
                       ("Lỗi hệ thống", "loi"), ("Thời gian trung bình (s)", "thoi_gian_trung_binh_s")):
        print(label.ljust(w0) + "".join(str(m.get(key)).rjust(w) for _, m in cols))
    m = summary["toan_bo"]
    print(line)
    print("Cách tìm được (bài chứng minh được): " + ", ".join(f"{k}: {v}" for k, v in m["cach_tim"].items()))
    print("Lý do dừng (bài không chứng minh được): " + ", ".join(f"{k}: {v}" for k, v in m["ly_do_dung"].items()))
    print("Lượt gọi LLM trung bình mỗi bài: " + ", ".join(f"{k} {v}" for k, v in m["luot_LLM_trung_binh"].items()))
    print(summary["luu_y"])
    if late:
        t = summary["tho_truoc_khi_loai_de_sai"]
        print(f"Số liệu thô (tính cả {len(late)} bài đề sai): {t['chung_minh_duoc']}/{t['so_bai']} = {t['ti_le_%']}%")
    ex_path = os.path.join(run_dir, "excluded.json")
    ex = {}
    if os.path.exists(ex_path):
        with open(ex_path, encoding="utf-8") as f:
            ex = json.load(f)
    ex.update({i: f"{why} (đã chạy: {st})" for i, (why, st) in late.items()})
    if ex:
        print(f"\nĐÃ BỎ QUA {len(ex)} BÀI (không tính vào tỉ lệ):")
        for i, why in ex.items():
            print(f"  {i:28s} {why}")
    print(f"\nTỪNG BÀI\n{line}")
    for r in raw:
        extra = r.get("method") if r["status"] == "PROVED" else r.get("stop_reason") or r.get("error", "")[:60]
        print(f"[{r['split']:5s}] [{r['area']:13s}] {r['id']:28s} {r['status']:11s} {str(extra):24s} "
              f"{r.get('elapsed_s', 0):5.0f} s  LLM={sum(r.get('llm_calls', {}).values())}")


def main() -> None:
    if sys.platform == "win32":
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)
    for name in ("subset", "check-refs", "run", "recheck", "report"):
        sp = sub.add_parser(name)
        sp.add_argument("--dataset", choices=["proverbench", "proofnet"], default="proverbench",
                        help="proofnet = mệnh đề Lean chuẩn của ProofNet# phần Giải tích 1")
        if name in ("subset", "check-refs", "run"):
            sp.add_argument("--split", choices=["valid", "test", "all"], default="valid" if name == "run" else "all")
        if name in ("run", "recheck", "report"):
            sp.add_argument("--name", required=True)
        if name == "run":
            sp.add_argument("--direction", choices=["dung", "mau_thuan", "sai"], default="dung")
            sp.add_argument("--limit", type=int, default=0)
            sp.add_argument("--ids", nargs="*")
            sp.add_argument("--first", type=int, default=0, help="chỉ lấy N bài đầu của tập (cố định, trước khi lọc)")
            sp.add_argument("--exclude-false", nargs="*", metavar="RUN",
                            help="bỏ các bài đã chứng minh được là SAI trong các lượt chạy chiều sai này")
            sp.add_argument("--skip", nargs="*", metavar="ID", help="bỏ qua các bài này (ghi lại trong excluded.json)")
            sp.add_argument("--skip-refcheck", action="store_true")
            sp.add_argument("--hint", action="store_true",
                            help="ProofNet#: đưa lời giải bằng lời của bộ dữ liệu cho FR09 làm gợi ý")
            sp.add_argument("--env", nargs="*", default=[], help="KHÓA=GIÁ_TRỊ, ví dụ MATH_FR09_MAX_LLM=4")
        if name == "report":
            sp.add_argument("--json", action="store_true")
    args = p.parse_args()
    _use_dataset(args.dataset)
    args.env_pairs = [tuple(kv.split("=", 1)) for kv in getattr(args, "env", [])]
    # Biến môi trường phải đặt TRƯỚC khi import lean_core / lean_prover (cấu hình được đọc lúc import)
    for k, v in {**DEFAULT_ENV, **PB_DEFAULT_ENV}.items():
        os.environ.setdefault(k, v)
    for k, v in args.env_pairs:
        os.environ[k] = v
    sys.path.insert(0, BASE_DIR)
    if "MATH_LEAN_IMPORTS" not in os.environ:
        import lean_core

        extra = [m for m in PB_EXTRA_IMPORTS if lean_core._mathlib_module_exists(m)]
        lean_core._BASE_IMPORTS = list(dict.fromkeys(lean_core._BASE_IMPORTS + extra))
        os.environ["MATH_LEAN_IMPORTS"] = ",".join(lean_core._BASE_IMPORTS)  # ghi lại cho config.json
    {"subset": cmd_subset, "check-refs": cmd_check_refs, "run": cmd_run, "recheck": cmd_recheck,
     "report": cmd_report}[args.cmd](args)


if __name__ == "__main__":
    main()
