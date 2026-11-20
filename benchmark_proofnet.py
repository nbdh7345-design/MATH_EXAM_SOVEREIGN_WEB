# -*- coding: utf-8 -*-
"""
benchmark_proofnet.py - Đo chức năng lõi FR08 (hình thức hóa) trên các bài Giải tích 1 của ProofNet# (MT3: đối chiếu
với kết quả công bố). ProofNet#: Poiroux và cộng sự, "Improving Autoformalization using Type Checking" (arXiv 2406.07222),
dữ liệu PAug/ProofNetSharp; tập con Giải tích 1 ở data/benchmarks/proofnet_sharp/gt1_subset.json.

Mỗi bài là một định lý (không có đáp số): lõi nhận đề tiếng Anh, sinh mệnh đề Lean, kiểm năm điều kiện của QT15.
Chỉ đo FR08, không chứng minh định lý (FR09).

Các lệnh (chạy lần lượt):
  python benchmark_proofnet.py subset      [--split valid|test|all] [--include-borderline]
      Liệt kê các bài sẽ chạy. Không gọi Lean, không gọi LLM.
  python benchmark_proofnet.py check-refs  [--split …] [--include-borderline]
      Biên dịch mệnh đề tham chiếu trên Lean/Mathlib của máy (ProofNet# hỗ trợ Lean v4.7–v4.16), sau khi chuyển cú
      pháp đã đổi (∑ x in s -> ∑ x ∈ s). Bài không biên dịch được bị loại khỏi lượt chạy. Không gọi LLM.
  python benchmark_proofnet.py run         --name TÊN [--split …] [--include-borderline] [--limit N] [--ids ID …]
                                           [--env KHÓA=GIÁ_TRỊ …]
      Chạy FR08 cho từng bài, ghi runs/TÊN/results.jsonl; bị ngắt thì chạy lại cùng lệnh để làm tiếp.
      --env dùng cho thí nghiệm bật/tắt (ví dụ MATH_FORMALIZE_CANDIDATES=1, MATH_REQUIRE_EQUIV=0, MATH_FORM_CHECK=0).
  python benchmark_proofnet.py score       --name TÊN [--rescore]
      Chấm tương đương kiểu BEq (rút gọn): Lean chứng minh hai chiều mệnh đề sinh ⇔ mệnh đề tham chiếu bằng một bộ
      tactic cố định. Ghi runs/TÊN/scores.jsonl và review.md (các bài cần chấm tay). Không gọi LLM.
  python benchmark_proofnet.py judge       --name TÊN [--model opus] [--effort max] [--dry-run] [--rejudge]
      Chấm lại bằng LLM mạnh những mệnh đề bộ chấm Lean CHƯA xác nhận tương đương (giám khảo không biết kết quả của
      hệ thống); ghi runs/TÊN/llm_labels.json (cùng dạng manual.json, nhưng là nhãn của LLM, không phải chấm tay).
  python benchmark_proofnet.py report      --name TÊN [--labels manual.json | llm_labels.json]
      Tính chỉ số từ results.jsonl + scores.jsonl (+ file nhãn nếu có), ghi runs/TÊN/summary.json.

Chỉ số: tỉ lệ biên dịch được, độ chính xác của mệnh đề được chọn (so với GPT-4o trong bài báo: 31,0% sinh một lần,
45,1% lọc + tự nhất quán, trên toàn bộ test), tỉ lệ "đã xác nhận", độ chính xác của mệnh đề "đã xác nhận", độ phủ,
số lượt gọi LLM và thời gian mỗi bài.
"""

import argparse
import hashlib
import json
import os
import re
import sys
import threading
import time
from collections import Counter, defaultdict
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BENCH_DIR = os.path.join(BASE_DIR, "data", "benchmarks", "proofnet_sharp")
SUBSET_PATH = os.path.join(BENCH_DIR, "gt1_subset.json")
REFCHECK_PATH = os.path.join(BENCH_DIR, "refcheck.json")
RUNS_DIR = os.path.join(BENCH_DIR, "runs")
SPLITS = ("valid", "test")

# Cấu hình mặc định giống run_server.bat; --env và biến môi trường đã đặt sẵn được ưu tiên
DEFAULT_ENV = {
    "MATH_LLM_PROVIDER": "claude-cli",
    "MATH_LLM_MODEL": "haiku",
    "MATH_PROOF_ESCALATE_MODEL": "sonnet",
    "MATH_LLM_EFFORT": "low",
    "MATH_CLAUDE_CLI_MAX_PARALLEL": "4",
    # Mỗi lượt chạy đánh giá độc lập: không dùng lại kết quả FR09 (có gọi LLM) đã lưu từ lượt trước
    "MATH_FR09_CACHE": "0",
}
# Bộ import: phần Giải tích hệ thống dùng hằng ngày + các module mà mệnh đề tham chiếu Giải tích 1 của ProofNet# cần.
# `import Mathlib` đầy đủ cần nhiều RAM hơn (máy còn ~4 GB thì Lean báo "failed to read file .olean");
# máy đủ RAM thì chọn bằng --env MATH_LEAN_IMPORTS=Mathlib.
BENCH_EXTRA_IMPORTS = [
    "Mathlib.Analysis.Convex.Function", "Mathlib.Analysis.Convex.Deriv", "Mathlib.Topology.Bornology.Basic",
    "Mathlib.Topology.UniformSpace.UniformConvergence", "Mathlib.Order.LiminfLimsup", "Mathlib.Data.EReal.Basic",
    "Mathlib.Data.PNat.Basic", "Mathlib.Analysis.Calculus.Deriv.Inverse", "Mathlib.Topology.Order.IntermediateValue",
]

# Cú pháp Mathlib đã đổi sau Lean v4.16 (bản ProofNet# hỗ trợ cao nhất)
MIGRATIONS = [(re.compile(r"([∑∏]\s*[^,∈]*?\S)\s+in\s+"), r"\1 ∈ ")]

# Hết hạn mức gói Claude (Pro/Max) hoặc bị giới hạn tốc độ: dừng lượt chạy, không ghi bài đang dở
_LIMIT_RE = re.compile(r"hit your [\w -]*limit|usage limit|rate.?limit|\b429\b|overloaded|limit\s*·\s*resets",
                       re.IGNORECASE)

COMPARED = {"GPT-4o (greedy, test, chấm tay)": 31.0, "GPT-4o (lọc kiểm kiểu + tự nhất quán, test, chấm tay)": 45.1}


# =============================================================================
# Dữ liệu
# =============================================================================


def _read_jsonl(path: str) -> List[Dict[str, Any]]:
    if not os.path.exists(path):
        return []
    with open(path, encoding="utf-8") as f:
        return [json.loads(ln) for ln in f if ln.strip()]


def _latest(rows: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Mỗi bài lấy bản ghi mới nhất (bài lỗi được chạy lại thì bản ghi sau thay bản trước)."""
    last: Dict[str, Dict[str, Any]] = {}
    for r in rows:
        last[r["id"]] = r
    return list(last.values())


def _append_jsonl(path: str, row: Dict[str, Any]) -> None:
    with open(path, "a", encoding="utf-8", newline="\n") as f:
        f.write(json.dumps(row, ensure_ascii=False) + "\n")


def _sha256(path: str) -> str:
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def load_items(split: str = "all", include_borderline: bool = False) -> List[Dict[str, Any]]:
    """Các bài Giải tích 1 (nhóm 'chinh', thêm 'bien' nếu được yêu cầu), kèm dữ liệu gốc của ProofNet#."""
    with open(SUBSET_PATH, encoding="utf-8") as f:
        subset = json.load(f)
    chosen = [{**e, "nhom": "chinh"} for e in subset["chinh"]]
    if include_borderline:
        chosen += [{**e, "nhom": "bien"} for e in subset["bien"]]
    rows = {r["id"]: (s, r) for s in SPLITS for r in _read_jsonl(os.path.join(BENCH_DIR, f"proofnet_sharp_{s}.jsonl"))}
    items = []
    for e in chosen:
        s, r = rows[e["id"]]
        if s != e["split"]:
            raise ValueError(f"{e['id']}: gt1_subset ghi split {e['split']}, dữ liệu là {s}")
        if split in ("all", s):
            items.append({**r, "split": s, "chu_de": e["chu_de"], "nhom": e["nhom"]})
    return items


def _migrate(src: str) -> Tuple[str, bool]:
    out = src
    for pat, rep in MIGRATIONS:
        out = pat.sub(rep, out)
    return out, out != src


def parse_reference(item: Dict[str, Any]) -> Dict[str, Any]:
    """Tách mệnh đề tham chiếu: phần mở đầu (def phụ), tên định lý, các binder, kết luận, các dòng open của header."""
    src, migrated = _migrate(item["lean4_formalization"])
    heads = list(re.finditer(r"^theorem\s+(\S+)", src, re.MULTILINE))
    if not heads:
        raise ValueError(f"{item['id']}: không tìm thấy theorem")
    m = heads[-1]
    preamble = src[:m.start()].strip()
    rest = re.sub(r":=\s*(by\s+)?(sorry)?\s*$", "", src[m.end():].strip()).strip()
    depth, cut = 0, None
    for i, ch in enumerate(rest):
        if ch in "([{⦃⟨":
            depth += 1
        elif ch in ")]}⦄⟩":
            depth -= 1
        elif ch == ":" and depth == 0 and rest[i + 1:i + 2] != "=":
            cut = i
            break
    if cut is None:
        raise ValueError(f"{item['id']}: không tách được binder và kết luận")
    opens = [ln.strip() for ln in item["lean4_src_header"].splitlines()
             if ln.strip().startswith(("open ", "set_option "))]
    return {"name": m.group(1), "preamble": preamble, "binders": rest[:cut].strip(), "concl": rest[cut + 1:].strip(),
            "opens": opens, "migrated": migrated}


def _lines(block: List[str]) -> List[str]:
    """Tách khối thành các dòng thật (binder, def phụ, mệnh đề có thể nhiều dòng) để đếm đúng số dòng báo lỗi của Lean."""
    return "\n".join(block).split("\n")


def _block_ok(msgs: List[Tuple[int, str, str]], lo: int, hi: int) -> Tuple[bool, str]:
    errs = [m for m in msgs if lo <= m[0] <= hi and m[1] == "error"]
    return not errs, "\n".join(m[2] for m in errs)[:1500]


# =============================================================================
# Lệnh
# =============================================================================


def cmd_subset(args: argparse.Namespace) -> None:
    items = load_items(args.split, args.include_borderline)
    refcheck = _load_refcheck()
    for it in items:
        rc = refcheck.get(it["id"])
        tag = "chưa kiểm" if rc is None else ("biên dịch được" if rc["ok"] else "KHÔNG biên dịch được")
        print(f"[{it['split']:5s}] [{it['nhom']:5s}] {it['id']:28s} {it['chu_de']:42s} tham chiếu: {tag}")
    print(f"Tổng: {len(items)} bài ({Counter(i['split'] for i in items)})")


def _load_refcheck() -> Dict[str, Any]:
    if not os.path.exists(REFCHECK_PATH):
        return {}
    with open(REFCHECK_PATH, encoding="utf-8") as f:
        return json.load(f)


def cmd_check_refs(args: argparse.Namespace) -> None:
    import lean_core as C

    items = load_items(args.split, args.include_borderline)
    lines = [*[f"import {m}" for m in C.lean_imports()], ""]
    ranges = {}
    for n, it in enumerate(items):
        ref = parse_reference(it)
        start = len(lines) + 1
        lines += _lines([f"namespace PNREF{n}", *ref["opens"], ref["preamble"],
                         f"theorem {ref['name']} {ref['binders']} :", f"    {ref['concl']} := by", "  sorry",
                         f"end PNREF{n}", ""])
        ranges[it["id"]] = (start, len(lines), ref["migrated"])
    print(f"Biên dịch {len(items)} mệnh đề tham chiếu trong một file (có thể mất vài phút)…", flush=True)
    res = C.compile_lean("PROOFNET-REFCHECK", "\n".join(lines) + "\n", timeout_sec=1800)
    if res["infra_error"] or res["returncode"] == -1:
        raise SystemExit(f"Lỗi hạ tầng / quá thời gian khi chạy Lean: {res['output'][-800:]}")
    msgs = C._split_messages(res["output"])
    out = _load_refcheck()
    for it in items:
        lo, hi, migrated = ranges[it["id"]]
        ok, err = _block_ok(msgs, lo, hi)
        out[it["id"]] = {"ok": ok, "migrated": migrated, "errors": err, "checked_at": datetime.now().isoformat(timespec="seconds")}
        print(f"  {'ĐẠT ' if ok else 'LỖI '} {it['id']:28s}{' (đã chuyển cú pháp)' if migrated else ''}{'' if ok else ' ' + err[:160]}")
    with open(REFCHECK_PATH, "w", encoding="utf-8", newline="\n") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    good = sum(1 for it in items if out[it["id"]]["ok"])
    print(f"{good}/{len(items)} mệnh đề tham chiếu biên dịch được trên Lean của máy; ghi {REFCHECK_PATH}")


def _versions() -> Dict[str, Any]:
    import lean_core as C

    info: Dict[str, Any] = {}
    try:
        with open(os.path.join(C.LEAN_PROJECT, "lean-toolchain"), encoding="utf-8") as f:
            info["lean"] = f.read().strip()
        with open(os.path.join(C.LEAN_PROJECT, "lake-manifest.json"), encoding="utf-8") as f:
            info["mathlib"] = next((p.get("rev") for p in json.load(f)["packages"] if p.get("name") == "mathlib"), None)
    except Exception as exc:
        info["error"] = str(exc)
    return info


def _run_config(args: argparse.Namespace, items: List[Dict[str, Any]]) -> Dict[str, Any]:
    import lean_core as C

    status = {k: v for k, v in C.lean_status().items() if k not in ("warmup", "lake", "project")}
    return {
        "split": args.split, "include_borderline": args.include_borderline, "env_overrides": dict(args.env_pairs),
        "llm": {"provider": os.environ.get("MATH_LLM_PROVIDER"), "model": C.LEAN_MODEL,
                "proof_escalate_model": C.PROOF_ESCALATE_MODEL, "judge_model": C.JUDGE_MODEL,
                "judge_effort": C.JUDGE_EFFORT,
                "normalize_model": C.NORMALIZE_MODEL, "backtranslate_model": C.BACKTRANSLATE_MODEL,
                "effort": os.environ.get("MATH_LLM_EFFORT")},
        "fr08": {"max_llm_calls": C.FR08_MAX_LLM_CALLS, "candidates": C.NUM_CANDIDATES, "extra": C.EXTRA_CANDIDATES,
                 "equiv_llm_pairs": C.EQUIV_LLM_PAIRS, "equiv_llm_fixes": C.EQUIV_LLM_FIXES,
                 "judge_groups": C.JUDGE_GROUPS, "semantic_rank": C.SEMANTIC_RANK,
                 "deep_vacuity": C.DEEP_VACUITY, "vacuity_model": C.VACUITY_MODEL,
                 "fr09_cache": os.environ.get("MATH_FR09_CACHE", "1")},
        "core": status, "lean_imports": C.lean_imports(), "versions": _versions(),
        "data_sha256": {s: _sha256(os.path.join(BENCH_DIR, f"proofnet_sharp_{s}.jsonl")) for s in SPLITS},
        "subset_sha256": _sha256(SUBSET_PATH), "items": [it["id"] for it in items],
    }


def cmd_run(args: argparse.Namespace) -> None:
    import lean_core as C

    items = load_items(args.split, args.include_borderline)
    if args.ids:
        items = [it for it in items if it["id"] in set(args.ids)]
    refcheck = _load_refcheck()
    if not args.skip_refcheck:
        if not refcheck:
            raise SystemExit("Chưa kiểm mệnh đề tham chiếu: chạy `check-refs` trước (hoặc --skip-refcheck).")
        skipped = [it["id"] for it in items if not refcheck.get(it["id"], {}).get("ok")]
        items = [it for it in items if it["id"] not in skipped]
        if skipped:
            print(f"Bỏ {len(skipped)} bài có mệnh đề tham chiếu không biên dịch được / chưa kiểm: {skipped}")
    run_dir = os.path.join(RUNS_DIR, args.name)
    os.makedirs(run_dir, exist_ok=True)
    cfg_path, res_path = os.path.join(run_dir, "config.json"), os.path.join(run_dir, "results.jsonl")
    cfg = _run_config(args, items)
    if os.path.exists(cfg_path):
        with open(cfg_path, encoding="utf-8") as f:
            old = json.load(f)
        keys = ("env_overrides", "llm", "fr08", "core", "lean_imports", "versions", "data_sha256")
        if any(old.get(k) != cfg.get(k) for k in keys):
            raise SystemExit(f"Lượt chạy '{args.name}' đã có với cấu hình khác: đặt tên mới để kết quả tái lập được.")
    else:
        with open(cfg_path, "w", encoding="utf-8", newline="\n") as f:
            json.dump(cfg, f, ensure_ascii=False, indent=1)
    done = {r["id"] for r in _latest(_read_jsonl(res_path)) if r["status"] != "ERROR"}  # bài lỗi được chạy lại
    todo = [it for it in items if it["id"] not in done][: args.limit or None]
    print(f"Lượt chạy '{args.name}': {len(done)} bài đã xong, chạy {len(todo)} bài; mô hình sinh {C.LEAN_MODEL}, "
          f"giám khảo {C.JUDGE_MODEL}", flush=True)
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
            task = C.FormalTask(code="PN-" + re.sub(r"[^A-Za-z0-9_]", "_", it["id"]), text_vi=it["nl_statement"])
            run = C.CoreRun()
            row: Dict[str, Any] = {"id": it["id"], "split": it["split"], "chu_de": it["chu_de"], "nhom": it["nhom"]}
            try:
                fz = C.formalize(task, run)  # FR08 tự kết luận, không chứng minh mệnh đề
                confirmed = fz["selected"]
                top = fz["ranking"][0] if fz["ranking"] else None
                group_of = {id(c): len(g) for _, g in fz["ranking"] for c in g}
                row.update({
                    "status": "CONFIRMED" if confirmed else ("UNCONFIRMED" if fz["typed"] else "NO_TYPED"),
                    "fr08": run.pipeline.get("fr08"),
                    "top": _stmt(top[0], len(top[1])) if top else None,
                    "confirmed": _stmt(confirmed, group_of.get(id(confirmed), 1)) if confirmed else None,
                    "candidates": [{**_stmt(c, group_of.get(id(c), 0)), "vacuous": c["vacuous"]} for c in fz["typed"]],
                    "statement_kind": run.kind,
                })
            except Exception as exc:
                msg = f"{type(exc).__name__}: {exc}"
                if _LIMIT_RE.search(msg):
                    raise SystemExit(f"Dừng ở bài {it['id']} ({n}/{len(todo)}): hết hạn mức / giới hạn tốc độ của Claude.\n"
                                     f"  {msg[:300]}\n  Kết quả {n - 1} bài trước đã được lưu; khi hạn mức được làm mới, "
                                     f"chạy lại đúng lệnh này để làm tiếp từ bài {it['id']}.")
                row.update({"status": "ERROR", "error": msg[:1000]})
            row.update({"history": run.history, "timings_s": run.timings, "llm_calls": dict(calls),
                        "elapsed_s": round(time.perf_counter() - t0, 1), "finished_at": datetime.now().isoformat(timespec="seconds")})
            _append_jsonl(res_path, row)
            print(f"  [{n}/{len(todo)}] {it['id']:28s} {row['status']:12s} {row['elapsed_s']:6.0f}s LLM={sum(calls.values())}",
                  flush=True)
            if row["status"] == "ERROR" and "Mathlib" in row.get("error", ""):
                raise SystemExit(f"Dừng: {row['error']}")
    finally:
        C._call_structured = original


def _stmt(rep: Dict[str, Any], group_size: int) -> Dict[str, Any]:
    return {"slot": rep["slot"], "statement": rep["statement"], "opens": rep["form"]["open_namespaces"],
            "group_size": group_size, "restatement": rep.get("restatement", ""), "judge": rep.get("judge"),
            "conditions": rep.get("conditions"), "auto_ok": rep.get("auto_ok", False)}


# Chấm tương đương kiểu BEq (Poiroux và cộng sự): mỗi chiều chứng minh mệnh đề này từ mệnh đề kia, CHỈ dùng mệnh đề kia
# làm giả thiết (h) và một bộ tactic NÔNG cố định: đổi ký hiệu thuộc khoảng/đoạn/ảnh/range, áp dụng h, convert, tự động
# hóa ngắn (simp_all, aesop, tauto, fun_prop). Không tìm kiếm thư viện (exact?) và không để LLM viết chứng minh: mọi định
# lý của ProofNet# đều đúng, nên với bộ chứng minh đủ mạnh, hai mệnh đề đúng BẤT KỲ đều "tương đương" (chấm nhầm).
# Không có sorry; tiên đề của từng chứng minh phải là tiên đề chuẩn.
# Kết quả: tương đương (hai chiều), một chiều, không chứng minh được (cần chấm tay).
_UNFOLD = ("Set.mem_Ioo, Set.mem_Ioi, Set.mem_Ici, Set.mem_Iio, Set.mem_Iic, Set.mem_Icc, Set.mem_Ico, Set.mem_Ioc, "
           "Set.mem_uIcc, Set.mem_image, Finset.mem_range, Function.Injective")
VERDICTS = {"tuong_duong": "tương đương", "sinh_suy_ra_chuan": "1 chiều: sinh ⇒ chuẩn",
            "chuan_suy_ra_sinh": "1 chiều: chuẩn ⇒ sinh", "khong_chung_minh_duoc": "không c/m được"}


def _beq_tactics(h: str) -> List[str]:
    close = f"first | assumption | exact default | (simp_all [{_UNFOLD}]; done) | fun_prop | aesop"
    return [
        f"exact {h}",
        f"(intros; apply {h} <;> {close})",
        f"(simpa [{_UNFOLD}] using {h})",
        f"(simp_all [{_UNFOLD}]; done)",
        f"(intros; simp_all [{_UNFOLD}]; done)",
        "tauto",
        "aesop",
        *[f"(convert {h} using {k} <;> first | rfl | (simp_all [{_UNFOLD}]; done) | aesop)" for k in (1, 2, 3)],
    ]


def _equiv_block(n: int, ref: Dict[str, Any], gen: Dict[str, Any]) -> List[str]:
    opens = " ".join(dict.fromkeys(gen["opens"]))
    ref_prop = f"∀ {ref['binders']}, {ref['concl']}" if ref["binders"].strip() else ref["concl"]
    first = lambda tactics: ["  first", *[f"    | {t}" for t in tactics]]  # noqa: E731
    return _lines([f"namespace PNEQ{n}", *ref["opens"], f"open {opens}" if opens else "", ref["preamble"],
                   "MARK_G2R",
                   f"theorem gen_to_ref (h_gen : {gen['statement']}) {ref['binders']} :", f"    {ref['concl']} := by",
                   *first(_beq_tactics("h_gen")),
                   "MARK_R2G",
                   f"theorem ref_to_gen (h_ref : {ref_prop}) :", f"    {gen['statement']} := by",
                   *first(_beq_tactics("h_ref")),
                   "MARK_END",
                   "#print axioms gen_to_ref", "#print axioms ref_to_gen",
                   f"end PNEQ{n}", ""])


def _proved(out: str, msgs: List[Tuple[int, str, str]], name: str, lo: int, hi: int) -> Tuple[bool, str]:
    """Chứng minh được chấp nhận: không lỗi trong khối, và `#print axioms` chỉ gồm tiên đề chuẩn (không có sorryAx)."""
    ok, err = _block_ok(msgs, lo, hi)
    m = re.search(rf"'{re.escape(name)}' depends on axioms: \[(.*?)\]", out, re.DOTALL)
    used = {a.strip() for a in m.group(1).split(",")} if m else set()
    if ok and m and not used <= {"propext", "Classical.choice", "Quot.sound"}:
        return False, f"dùng tiên đề ngoài chuẩn: {sorted(used)}"
    if ok and not m and f"'{name}' does not depend on any axioms" not in out:
        return False, "không đọc được kết quả #print axioms"
    return ok, err


def cmd_score(args: argparse.Namespace) -> None:
    import lean_core as C

    run_dir = os.path.join(RUNS_DIR, args.name)
    results = _latest(_read_jsonl(os.path.join(run_dir, "results.jsonl")))
    score_path = os.path.join(run_dir, "scores.jsonl")
    scored = {} if args.rescore else {r["id"]: r for r in _read_jsonl(score_path)}
    items = {it["id"]: it for it in load_items("all", True)}
    jobs = []  # (id, "top"/"confirmed", ref, gen)
    for r in results:
        if r["id"] in scored or r["status"] == "ERROR":
            continue
        ref = parse_reference(items[r["id"]])
        for key in ("top", "confirmed"):
            if r.get(key):
                jobs.append((r["id"], key, ref, r[key]))
    if not jobs:
        print("Không còn gì để chấm.")
        return
    lines = [*[f"import {m}" for m in C.lean_imports()], ""]
    marks = []
    for n, (rid, key, ref, gen) in enumerate(jobs):
        start = len(lines) + 1
        block = _equiv_block(n, ref, gen)
        idx = [block.index(m) for m in ("MARK_G2R", "MARK_R2G", "MARK_END")]
        for i in idx:
            block[i] = ""
        lines += block
        marks.append((n, *[start + i for i in idx]))
    print(f"Chấm {len(jobs)} mệnh đề ({len({j[0] for j in jobs})} bài) trong một file Lean…", flush=True)
    res = C.compile_lean(f"PROOFNET-SCORE-{args.name}", "\n".join(lines) + "\n", timeout_sec=3600)
    if res["infra_error"] or res["returncode"] == -1:
        raise SystemExit(f"Lỗi hạ tầng / quá thời gian khi chạy Lean: {res['output'][-800:]}")
    out = res["output"]
    msgs = C._split_messages(out)
    per_id: Dict[str, Dict[str, Any]] = defaultdict(dict)
    for (rid, key, _, _), (n, mg, mr, me) in zip(jobs, marks):
        g2r, e1 = _proved(out, msgs, f"PNEQ{n}.gen_to_ref", mg, mr - 1)
        r2g, e2 = _proved(out, msgs, f"PNEQ{n}.ref_to_gen", mr, me - 1)
        verdict = ("tuong_duong" if g2r and r2g else "sinh_suy_ra_chuan" if g2r else "chuan_suy_ra_sinh" if r2g
                   else "khong_chung_minh_duoc")
        per_id[rid][key] = {"equivalent": g2r and r2g, "gen_to_ref": g2r, "ref_to_gen": r2g, "verdict": verdict,
                            "errors": "\n".join(filter(None, [e1, e2]))[:800]}
    for rid, sc in per_id.items():
        _append_jsonl(score_path, {"id": rid, **sc, "scored_at": datetime.now().isoformat(timespec="seconds")})
        print(f"  {rid:28s} " + " | ".join(f"{k}: {VERDICTS[v['verdict']]}" for k, v in sc.items()))
    _write_review(run_dir, results, {**scored, **per_id}, items)


def _write_review(run_dir: str, results: List[Dict[str, Any]], scores: Dict[str, Any], items: Dict[str, Any]) -> None:
    """Các bài mà bộ chấm tự động không xác nhận được tương đương: cần người chấm tay (BEq có thể báo sai âm)."""
    out = ["# Các mệnh đề cần chấm tay", "",
           "Ghi kết luận vào manual.json, ví dụ: {\"Rudin|exercise_5_1\": {\"top\": true, \"confirmed\": true}}", ""]
    for r in results:
        sc = scores.get(r["id"], {})
        for key in ("top", "confirmed"):
            if r.get(key) and not sc.get(key, {}).get("equivalent"):
                it = items[r["id"]]
                verdict = VERDICTS.get(sc.get(key, {}).get("verdict", ""), "chưa chấm")
                out += [f"## {r['id']} · {key}", "", f"**Chấm tự động:** {verdict}", "",
                        f"**Đề:** {it['nl_statement']}", "",
                        "**Tham chiếu:**", "```lean", it["lean4_formalization"], "```", "",
                        "**Mệnh đề sinh ra:**", "```lean", r[key]["statement"], "```", "",
                        f"**Bản diễn đạt lại:** {r[key].get('restatement') or '(không có)'}", ""]
    with open(os.path.join(run_dir, "review.md"), "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(out))


# Chấm lại bằng LLM mạnh (mặc định Opus, effort max) các mệnh đề mà bộ chấm Lean chưa xác nhận tương đương. Giám khảo
# không biết mệnh đề do hệ thống nào sinh, không thấy kết quả chấm Lean hay kết luận của FR08; tiêu chí là mệnh đề có
# cùng nghĩa với đề tiếng Anh (mệnh đề tham chiếu của ProofNet# chỉ để tham khảo). Nhãn ghi ra file riêng (mặc định
# llm_labels.json), cùng dạng manual.json, để `report --labels llm_labels.json` dùng; đây KHÔNG phải nhãn chấm tay.
LLM_GRADER_SCHEMA: Dict[str, Any] = {
    "type": "object",
    "properties": {
        "phan_tich": {"type": "string"},
        "khac_biet": {"type": "array", "items": {"type": "object", "properties": {
            "mo_ta": {"type": "string"}, "lam_doi_nghia": {"type": "boolean"}},
            "required": ["mo_ta", "lam_doi_nghia"], "additionalProperties": False}},
        "dung_nghia": {"type": "boolean"},
    },
    "required": ["phan_tich", "khac_biet", "dung_nghia"],
    "additionalProperties": False,
}
LLM_GRADER_SYSTEM = """Bạn là chuyên gia toán và Lean 4 + Mathlib, chấm một bản hình thức hóa (autoformalization) cho benchmark ProofNet#.
Bạn nhận: (1) phát biểu toán bằng tiếng Anh; (2) mệnh đề Lean tham chiếu do người viết (đúng nghĩa, nhưng chỉ là MỘT cách viết đúng; có thể khác Lean bản mới ở vài tên định lý); (3) mệnh đề Lean CẦN CHẤM.
Câu hỏi: mệnh đề cần chấm có phải là một hình thức hóa ĐÚNG NGHĨA của phát biểu (1) không, tức là tương đương về toán học với điều phát biểu khẳng định, theo cách hiểu chuẩn của người làm toán (đối tượng, miền và kiểu như tham chiếu hiểu, giả thiết, lượng từ, kết luận)?
- Cách viết khác nhưng chắc chắn cùng nghĩa vẫn là đúng: đổi tên biến, dùng định nghĩa Mathlib tương đương (ví dụ IsLUB thay cho sSup khi sup tồn tại), dịch chỉ số với cùng nội dung, thêm điều kiện mà phát biểu ngầm giả định (ví dụ sự tồn tại của đại lượng được nhắc tới).
- Sai nghĩa: thêm giả thiết phát biểu không có (kể cả giả thiết làm bài dễ hơn), bỏ giả thiết, thu hẹp hay mở rộng miền/kiểu của đối tượng so với phát biểu, đổi lượng từ hoặc thứ tự lượng từ, kết luận mạnh hơn hay yếu hơn, chỉ phát biểu một chiều khi phát biểu là "khi và chỉ khi", giới hạn lấy trên lân cận có cả điểm đang xét khi phát biểu là giới hạn thông thường, dùng hàm Mathlib cho giá trị quy ước (lim, deriv, sSup, ∫, tsum) mà không có điều kiện tồn tại tương ứng làm nghĩa khác đi.
Hãy đọc kỹ từng phần Lean (ép kiểu, phép chia/trừ trên ℕ, phạm vi của ∀/∃, dấu ngoặc). Điền phan_tich (lập luận ngắn), khac_biet (mọi khác biệt với phát biểu; lam_doi_nghia = true nếu khác biệt làm đổi nghĩa), và dung_nghia (true khi và chỉ khi không có khác biệt nào làm đổi nghĩa)."""


def cmd_judge(args: argparse.Namespace) -> None:
    import lean_core as C

    run_dir = os.path.join(RUNS_DIR, args.name)
    results = _latest(_read_jsonl(os.path.join(run_dir, "results.jsonl")))
    scores = {r["id"]: r for r in _read_jsonl(os.path.join(run_dir, "scores.jsonl"))}
    out_path = os.path.join(run_dir, args.out)
    labels: Dict[str, Any] = {}
    if os.path.exists(out_path) and not args.rejudge:
        labels = json.load(open(out_path, encoding="utf-8"))
    items = {it["id"]: it for it in load_items("all", True)}
    unscored = [r["id"] for r in results if r["status"] != "ERROR" and r["id"] not in scores]
    if unscored:
        raise SystemExit(f"Còn bài chưa chấm bằng Lean, chạy `score --name {args.name}` trước: {unscored}")
    jobs = []  # (id, khóa, mệnh đề): chỉ mệnh đề mà bộ chấm Lean CHƯA xác nhận tương đương
    for r in results:
        for key in ("top", "confirmed"):
            if r.get(key) and not scores[r["id"]].get(key, {}).get("equivalent") and key not in labels.get(r["id"], {}):
                jobs.append((r["id"], key, r[key]["statement"]))
    distinct = {(rid, C._normalize_statement(st)) for rid, _, st in jobs}
    print(f"Chấm lại bằng {args.model} (effort {args.effort}): {len(distinct)} mệnh đề khác nhau "
          f"({len(jobs)} mục top/confirmed) mà bộ chấm Lean chưa xác nhận; nhãn ghi vào {out_path}", flush=True)
    if args.model == C.JUDGE_MODEL:
        print(f"  Lưu ý: {args.model} cũng là giám khảo bên trong FR08, nên lần chấm này không độc lập với hệ thống.")
    if args.dry_run or not jobs:
        return
    labels["_ghi_chu"] = (f"Nhãn do LLM {args.model} (effort {args.effort}) chấm, chỉ cho mệnh đề bộ chấm Lean chưa xác "
                          f"nhận tương đương; KHÔNG phải nhãn chấm tay. Tiêu chí: đúng nghĩa đề tiếng Anh.")
    done: Dict[Tuple[str, str], Dict[str, Any]] = {}
    for n, (rid, key, st) in enumerate(jobs, 1):
        k = (rid, C._normalize_statement(st))
        if k not in done:
            it = items[rid]
            user = (f"(1) Phát biểu:\n{it['nl_statement']}\n\n(2) Mệnh đề tham chiếu:\n```lean\n"
                    f"{it['lean4_formalization']}\n```\n\n(3) Mệnh đề cần chấm:\n```lean\n{st}\n```")
            t0 = time.perf_counter()
            try:
                done[k] = C._call_structured(LLM_GRADER_SYSTEM, user, LLM_GRADER_SCHEMA, model=args.model,
                                             effort=args.effort)
            except Exception as exc:
                msg = f"{type(exc).__name__}: {exc}"
                stop = "hết hạn mức / giới hạn tốc độ" if _LIMIT_RE.search(msg) else "lỗi"
                raise SystemExit(f"Dừng ở {rid} · {key} ({n}/{len(jobs)}): {stop}: {msg[:300]}\n  Nhãn đã chấm được "
                                 f"giữ trong {out_path}; chạy lại đúng lệnh này để chấm tiếp.")
            done[k]["giay"] = round(time.perf_counter() - t0, 1)
        res = done[k]
        entry = labels.setdefault(rid, {})
        entry[key] = bool(res["dung_nghia"])
        entry[f"{key}_phan_tich"] = res["phan_tich"]
        entry[f"{key}_khac_biet"] = res["khac_biet"]
        if key == "top" or "ly_do" not in entry:
            doi = [d["mo_ta"] for d in res["khac_biet"] if d["lam_doi_nghia"]]
            entry["ly_do"] = f"{args.model}: " + ("; ".join(doi) if doi else "đúng nghĩa")
        with open(out_path, "w", encoding="utf-8", newline="\n") as f:
            json.dump(labels, f, ensure_ascii=False, indent=1)
        print(f"  [{n}/{len(jobs)}] {rid:28s} {key:9s} {'ĐÚNG NGHĨA' if res['dung_nghia'] else 'SAI NGHĨA':10s} "
              f"{res.get('giay', 0):5.0f} s | {entry['ly_do'][:110]}", flush=True)
    print(f"Xong. Xem chỉ số: python benchmark_proofnet.py report --name {args.name} --labels {args.out}")


def _pct(a: int, b: int) -> Optional[float]:
    return round(100.0 * a / b, 1) if b else None


def cmd_report(args: argparse.Namespace) -> None:
    run_dir = os.path.join(RUNS_DIR, args.name)
    results = _latest(_read_jsonl(os.path.join(run_dir, "results.jsonl")))
    scores = {r["id"]: r for r in _read_jsonl(os.path.join(run_dir, "scores.jsonl"))}
    manual_path = os.path.join(run_dir, args.labels)
    if args.labels != "manual.json" and not os.path.exists(manual_path):
        raise SystemExit(f"Không có file nhãn {manual_path}")
    manual = json.load(open(manual_path, encoding="utf-8")) if os.path.exists(manual_path) else {}
    manual.pop("_ghi_chu", None)

    def correct(r: Dict[str, Any], key: str, use_manual: bool) -> bool:
        if not r.get(key):
            return False
        if use_manual and key in manual.get(r["id"], {}):
            return bool(manual[r["id"]][key])
        return bool(scores.get(r["id"], {}).get(key, {}).get("equivalent"))

    def metrics(rows: List[Dict[str, Any]], use_manual: bool) -> Dict[str, Any]:
        n = len(rows)
        typed = sum(1 for r in rows if r["status"] in ("CONFIRMED", "UNCONFIRMED"))
        conf = [r for r in rows if r["status"] == "CONFIRMED"]
        top_ok = sum(correct(r, "top", use_manual) for r in rows)
        conf_ok = sum(correct(r, "confirmed", use_manual) for r in conf)
        calls = Counter()
        for r in rows:
            calls.update(r.get("llm_calls", {}))
        return {
            "so_bai": n, "loi": sum(1 for r in rows if r["status"] == "ERROR"),
            "ti_le_bien_dich_duoc_%": _pct(typed, n),
            "do_chinh_xac_menh_de_chon_%": _pct(top_ok, n),
            "ti_le_da_xac_nhan_%": _pct(len(conf), n),
            "do_chinh_xac_cua_da_xac_nhan_%": _pct(conf_ok, len(conf)),
            "do_phu_xac_nhan_dung_%": _pct(conf_ok, n),
            "luot_LLM_trung_binh": {m: round(c / n, 2) for m, c in calls.items()} if n else {},
            "thoi_gian_trung_binh_s": round(sum(r.get("elapsed_s", 0) for r in rows) / n, 1) if n else None,
        }

    unscored = [r["id"] for r in results if r["status"] != "ERROR" and r["id"] not in scores]
    summary = {
        "luot_chay": args.name, "chua_cham": unscored,
        "tu_dong_BEq": metrics(results, False),
        "sau_cham_tay": metrics(results, True) if manual else None,
        "theo_split": {s: metrics([r for r in results if r["split"] == s], bool(manual)) for s in SPLITS
                       if any(r["split"] == s for r in results)},
        "theo_nhom": {g: metrics([r for r in results if r["nhom"] == g], False) for g in ("chinh", "bien")
                      if any(r["nhom"] == g for r in results)},
        "theo_nhom_cham_tay": {g: metrics([r for r in results if r["nhom"] == g], True) for g in ("chinh", "bien")
                               if any(r["nhom"] == g for r in results)} if manual else None,
        "doi_chieu_bai_bao_%": COMPARED,
        "luu_y": "Không so trực tiếp được: bài báo chấm tay trên toàn bộ 186 bài test, Lean v4.7-v4.16; ở đây là tập "
                 "con Giải tích 1, Lean của máy, chấm tự động kiểu BEq rút gọn (có thể báo sai âm) và chấm tay nếu có.",
    }
    with open(os.path.join(run_dir, "summary.json"), "w", encoding="utf-8", newline="\n") as f:
        json.dump(summary, f, ensure_ascii=False, indent=1)
    if args.json:
        print(json.dumps(summary, ensure_ascii=False, indent=1))
        return
    title = "SAU CHẤM TAY (manual.json)" if args.labels == "manual.json" else f"THEO NHÃN {args.labels}"
    _print_report(args.name, summary, results, scores, manual, title)


def _print_report(name: str, summary: Dict[str, Any], results: List[Dict[str, Any]], scores: Dict[str, Any],
                  manual: Dict[str, Any], title: str = "SAU CHẤM TAY (manual.json)") -> None:
    """In báo cáo dạng bảng ra terminal (summary.json giữ đủ số liệu dạng JSON)."""
    group = {"chinh": "Chính", "bien": "Biên"}
    cols = [("Toàn bộ", summary["tu_dong_BEq"]), *[(group[g], m) for g, m in summary["theo_nhom"].items()]]
    if summary["sau_cham_tay"]:
        cols += [("Toàn bộ", summary["sau_cham_tay"]),
                 *[(group[g], m) for g, m in summary["theo_nhom_cham_tay"].items()]]
    rows = [("Số bài", "so_bai", ""), ("Biên dịch được", "ti_le_bien_dich_duoc_%", "%"),
            ("Đã xác nhận (đủ 5 điều kiện)", "ti_le_da_xac_nhan_%", "%"),
            ("Mệnh đề được chọn đúng nghĩa đề", "do_chinh_xac_menh_de_chon_%", "%"),
            ("Trong số đã xác nhận: đúng nghĩa đề", "do_chinh_xac_cua_da_xac_nhan_%", "%"),
            ("Đã xác nhận và đúng / tổng số bài", "do_phu_xac_nhan_dung_%", "%"),
            ("Thời gian trung bình mỗi bài", "thoi_gian_trung_binh_s", " s")]
    w0, w = 40, 10
    n_auto = 1 + len(summary["theo_nhom"])
    line = "-" * (w0 + w * len(cols))
    print(f"\nBÁO CÁO LƯỢT CHẠY: {name}\n{line}")
    head = "CHẤM TỰ ĐỘNG (Lean)".center(w * n_auto)
    if len(cols) > n_auto:
        head += title.center(w * (len(cols) - n_auto))
    print(" " * w0 + head)
    print("Chỉ số".ljust(w0) + "".join(c.rjust(w) for c, _ in cols))
    print(line)
    for label, key, unit in rows:
        vals = [m.get(key) for _, m in cols]
        print(label.ljust(w0) + "".join(("—" if v is None else f"{v}{unit}").rjust(w) for v in vals))
    calls = "; ".join(f"{m} {v}" for m, v in summary["tu_dong_BEq"]["luot_LLM_trung_binh"].items())
    print("Lượt gọi LLM trung bình mỗi bài".ljust(w0) + calls.rjust(w * len(cols)))
    print(line)
    print("Đối chiếu bài báo (toàn bộ test, chấm tay): " + "; ".join(f"{k}: {v}%" for k, v in COMPARED.items()))
    print("Lưu ý: bộ chấm tự động khắt khe (mệnh đề đúng nghĩa nhưng viết khác vẫn bị tính sai); "
          "xem review.md và ghi manual.json để có số liệu sau chấm tay.")
    if summary["chua_cham"]:
        print(f"Chưa chấm (cần chạy score): {summary['chua_cham']}")
    label = {"CONFIRMED": "Đã xác nhận", "UNCONFIRMED": "CHƯA xác nhận", "NO_TYPED": "Không biên dịch được",
             "ERROR": "LỖI"}
    print(f"\nTỪNG BÀI\n{line}")
    for r in results:
        sc = scores.get(r["id"], {}).get("top", {})
        eq = "—" if not sc else VERDICTS.get(sc.get("verdict"), "tương đương" if sc.get("equivalent") else "không c/m được")
        man = manual.get(r["id"], {})
        man_txt = f" | nhãn: {'ĐÚNG' if man.get('top') else 'SAI'}" if "top" in man else ""
        print(f"[{r['nhom']:5s}] {r['id']:26s} {label.get(r['status'], r['status']):14s} Lean: {eq:22s}"
              f" {r.get('elapsed_s', 0):5.0f} s{man_txt}")
        if r["status"] == "UNCONFIRMED":
            reasons = [h.split("chưa xác nhận, ", 1)[1] for h in r.get("history", []) if "chưa xác nhận, " in h]
            for reason in reasons[:2]:
                print(f"{'':10s}└ lý do: {reason[:150]}")
        elif r["status"] == "ERROR":
            print(f"{'':10s}└ lỗi: {r.get('error', '')[:150]}")
        if man.get("ly_do"):
            print(f"{'':10s}└ nhãn: {man['ly_do'][:150]}")
    print(line)


# =============================================================================


def main() -> None:
    if sys.platform == "win32":
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)
    for name in ("subset", "check-refs", "run", "score", "judge", "report"):
        sp = sub.add_parser(name)
        if name in ("subset", "check-refs", "run"):
            sp.add_argument("--split", choices=["valid", "test", "all"], default="valid")
            sp.add_argument("--include-borderline", action="store_true")
        if name in ("run", "score", "judge", "report"):
            sp.add_argument("--name", required=True)
        if name == "run":
            sp.add_argument("--limit", type=int, default=0)
            sp.add_argument("--ids", nargs="*")
            sp.add_argument("--skip-refcheck", action="store_true")
            sp.add_argument("--env", nargs="*", default=[], help="KHÓA=GIÁ_TRỊ, ví dụ MATH_FORMALIZE_CANDIDATES=1")
        if name == "score":
            sp.add_argument("--rescore", action="store_true")
        if name == "judge":
            sp.add_argument("--model", default="opus", help="mô hình chấm lại (mặc định opus; khác giám khảo của FR08)")
            sp.add_argument("--effort", default="max", help="mức suy nghĩ của mô hình chấm (mặc định max)")
            sp.add_argument("--out", default="llm_labels.json", help="file nhãn ghi ra trong thư mục lượt chạy")
            sp.add_argument("--rejudge", action="store_true", help="chấm lại cả những mục đã có nhãn")
            sp.add_argument("--dry-run", action="store_true", help="chỉ đếm số mục cần chấm, không gọi LLM")
        if name == "report":
            sp.add_argument("--json", action="store_true", help="in toàn bộ số liệu dạng JSON thay vì bảng")
            sp.add_argument("--labels", default="manual.json",
                            help="file nhãn trong thư mục lượt chạy (mặc định manual.json; ví dụ manual_nhap.json)")
    args = p.parse_args()
    args.env_pairs = [tuple(kv.split("=", 1)) for kv in getattr(args, "env", [])]
    # Biến môi trường phải đặt TRƯỚC khi import lean_core (cấu hình được đọc lúc import)
    for k, v in DEFAULT_ENV.items():
        os.environ.setdefault(k, v)
    for k, v in args.env_pairs:
        os.environ[k] = v
    sys.path.insert(0, BASE_DIR)
    if "MATH_LEAN_IMPORTS" not in os.environ:
        import lean_core

        lean_core._BASE_IMPORTS = list(dict.fromkeys(lean_core._BASE_IMPORTS + BENCH_EXTRA_IMPORTS))
        os.environ["MATH_LEAN_IMPORTS"] = ",".join(lean_core._BASE_IMPORTS)  # ghi lại cho config.json
    {"subset": cmd_subset, "check-refs": cmd_check_refs, "run": cmd_run, "score": cmd_score, "judge": cmd_judge,
     "report": cmd_report}[args.cmd](args)


if __name__ == "__main__":
    main()
