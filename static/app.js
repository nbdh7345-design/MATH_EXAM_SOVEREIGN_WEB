// app.js - Logic Tương Tác Giao Diện Hệ Thống Sinh Đề Toán Cao Cấp Sovereign (@gng5)

let globalQuestionsCache = {};
let activeExamData = null;
let userExamChoices = {};
let searchDebounceTimer = null;

function renderMath(el) {
  if (window.renderMathInElement) {
    try {
      window.renderMathInElement(el || document.body, {
        delimiters: [
          { left: "$$", right: "$$", display: true },
          { left: "\\[", right: "\\]", display: true },
          { left: "$", right: "$", display: false },
          { left: "\\(", right: "\\)", display: false }
        ],
        throwOnError: false
      });
    } catch (e) {
      console.warn("KaTeX render warning:", e);
    }
  }
}

function escapeHtml(str) {
  if (str === null || str === undefined) return "";
  return String(str)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;");
}

function formatTextWithParagraphs(text) {
  if (!text) return "";
  return String(text).replace(/\n/g, "<br/>");
}

function switchTab(tabName) {
  document.querySelectorAll(".tab-panel").forEach(p => p.classList.remove("active"));
  document.querySelectorAll(".nav-tab").forEach(b => b.classList.remove("active"));
  const panel = document.getElementById(`panel-${tabName}`);
  const btn = document.getElementById(`tabBtn-${tabName}`);
  if (panel) panel.classList.add("active");
  if (btn) btn.classList.add("active");

  if (tabName === "dashboard") loadDashboard();
  if (tabName === "questions") loadQuestions();
  if (tabName === "exam-builder") loadSavedExams();
  if (tabName === "ledger") loadMerkleLedger();
}

async function loadDashboard() {
  try {
    const res = await fetch("/api/dashboard");
    const data = await res.json();

    document.getElementById("headerMerkleRoot").textContent = (data.merkle_root || "").slice(0, 24) + "...";
    document.getElementById("statTotalQ").textContent = data.total_questions;
    document.getElementById("statSubjBreakdown").textContent = `Giải tích: ${data.calculus_count} | Đại số: ${data.algebra_count}`;
    document.getElementById("statTypeBreakdown").textContent = `${data.mcq_count} TN / ${data.essay_count} TL`;
    document.getElementById("statParamCount").textContent = `${data.parametric_count}/${data.total_questions} Câu chứa tham số (m, a, b)`;
    document.getElementById("statLeanPass").textContent = `${data.lean4_verified_count} / ${data.total_questions}`;
    document.getElementById("statPyPass").textContent = `${data.python_verified_count} / ${data.total_questions}`;
    document.getElementById("statExamsCount").textContent = data.exams_count;

    // Populate Agent Filter Dropdown
    const agentSel = document.getElementById("filterAgent");
    if (agentSel && agentSel.options.length <= 1 && data.agents && data.agents.length > 0) {
      data.agents.forEach(ag => {
        const opt = document.createElement("option");
        opt.value = ag.agent_id;
        opt.textContent = `${ag.agent_code}: ${ag.agent_name}`;
        agentSel.appendChild(opt);
      });
    }

    const llmSel = document.getElementById("llmAgentSelect");
    if (llmSel && llmSel.options.length <= 1 && data.agents && data.agents.length > 0) {
      data.agents.forEach(ag => {
        const opt = document.createElement("option");
        opt.value = ag.agent_id;
        opt.textContent = `${ag.agent_code}: ${ag.agent_name}`;
        llmSel.appendChild(opt);
      });
    }
    loadLLMStatus(data.llm_count || 0);

    // Render Agent Swarm Grid
    const grid = document.getElementById("swarmGridContainer");
    grid.innerHTML = "";
    (data.agents || []).forEach(ag => {
      const isAlg = ag.domain === "Đại số";
      const isPass = ag.status === "COMPLETED_PASS";
      const card = document.createElement("div");
      card.className = `agent-card ${isAlg ? "algebra" : ""} ${isPass ? "pass" : ""}`;
      card.onclick = () => {
        document.getElementById("filterAgent").value = ag.agent_id;
        switchTab("questions");
      };
      card.innerHTML = `
        <div class="agent-top">
          <span class="agent-code">${escapeHtml(ag.agent_code)} • ${escapeHtml(ag.domain)}</span>
          <span class="badge ${isPass ? "badge-success" : "badge-amber"}">${escapeHtml(ag.status)}</span>
        </div>
        <div class="agent-title">${escapeHtml(ag.agent_name)}</div>
        <div class="agent-desc">${escapeHtml(ag.role_desc)}</div>
        <div class="agent-metrics">
          <span>Câu hỏi: <b>${ag.questions_generated}</b></span>
          <span>LEAN 4: <b>${ag.lean4_verified}/${ag.questions_generated}</b></span>
          <span>Python: <b>${ag.python_verified}/${ag.questions_generated}</b></span>
          <span>${Math.round(ag.elapsed_ms || 0)}ms</span>
        </div>
      `;
      grid.appendChild(card);
    });

    // Render Recent Verification Logs
    const logsBox = document.getElementById("recentLogsContainer");
    if (!data.recent_logs || data.recent_logs.length === 0) {
      logsBox.innerHTML = `<p style="color: var(--text-muted);">Chưa có nhật ký kiểm chứng.</p>`;
    } else {
      logsBox.innerHTML = data.recent_logs.map(l => `
        <div style="padding: 0.65rem 0.8rem; border-bottom: 1px solid var(--border); font-size: 0.82rem; display:flex; justify-content:space-between; align-items:flex-start; gap: 1rem;">
          <div>
            <span class="badge badge-success">${escapeHtml(l.status)}</span>
            <b style="margin-left:0.4rem;">[${escapeHtml(l.question_code)}]</b> (Agent-${l.agent_id})
            <span style="color: var(--text-muted); margin-left:0.4rem;">${escapeHtml(l.output_log.split('\n')[0])}</span>
          </div>
          <div style="font-family: monospace; font-size: 0.75rem; color: var(--text-muted); white-space: nowrap;">
            ${Math.round(l.execution_ms)} ms • SHA: ${escapeHtml((l.merkle_hash || "").slice(0, 12))}...
          </div>
        </div>
      `).join("");
    }
  } catch (err) {
    console.error("Dashboard load error:", err);
  }
}

async function trigger20AgentSwarm() {
  const btn = document.getElementById("btnRunSwarm");
  const banner = document.getElementById("swarmStatusBanner");
  btn.disabled = true;
  btn.textContent = "⏳ Đang chạy 25 Agent song song (LEAN 4.35.0 + Python)...";
  banner.style.display = "block";
  banner.textContent = "⚡ Đang thực thi 25 luồng tác tử song song (ThreadPoolExecutor 25 workers): Biên dịch 75 file .lean bằng trình biên dịch Lean 4.35.0 và chạy 75 script Python SymPy/NumPy...";

  try {
    const res = await fetch("/api/swarm/run", { method: "POST" });
    const data = await res.json();
    banner.textContent = `✅ Hoàn tất ${data.swarm_workers} Agent song song trong ${(data.wall_clock_ms / 1000).toFixed(2)}s! Tổng câu hỏi: ${data.total_questions} | LEAN 4 Pass: ${data.lean4_verified}/${data.total_questions} | Python Pass: ${data.python_verified}/${data.total_questions} | Merkle Root: ${data.merkle_root.slice(0, 20)}...`;
    await loadDashboard();
  } catch (err) {
    banner.textContent = `❌ Lỗi khi chạy swarm Agent: ${err}`;
  } finally {
    btn.disabled = false;
    btn.textContent = "⚡ Kích Hoạt 25 Agent Kiểm Chứng Song Song";
  }
}

async function loadLLMStatus(llmCount) {
  const line = document.getElementById("llmStatusLine");
  if (!line) return;
  try {
    const st = await (await fetch("/api/llm/status")).json();
    const ls = await (await fetch("/api/lean/status")).json();
    const leanLine = document.getElementById("leanStatusLine");
    if (leanLine) {
      leanLine.innerHTML = ls.mathlib_ready
        ? `📐 Mathlib sẵn sàng tại <code>${escapeHtml(ls.project)}</code> • formalize 2 giai đoạn: mệnh đề → chứng minh (tối đa ${ls.max_attempts} lượt/mệnh đề)`
        : `📐 Chưa có Mathlib đã build tại <code>${escapeHtml(ls.project)}</code> (đặt MATH_LEAN_PROJECT).`;
      const cb = document.getElementById("llmFormalize");
      if (cb) cb.disabled = !ls.mathlib_ready;
    }
    line.innerHTML = st.configured
      ? `✅ ${escapeHtml(st.provider)} • Model: <code>${escapeHtml(st.model)}</code> • Endpoint: <code>${escapeHtml(st.endpoint)}</code> • Ngân hàng hiện có <b>${llmCount}</b> câu do LLM sinh.`
      : `⚠️ Chưa cấu hình LLM (${escapeHtml(st.provider)}). ${escapeHtml(st.hint)} Sau đó khởi động lại server.`;
  } catch (err) {
    line.textContent = `Lỗi kiểm tra cấu hình LLM: ${err}`;
  }
}

async function triggerLLMGenerate() {
  const btn = document.getElementById("btnLLMGenerate");
  const box = document.getElementById("llmResultBox");
  const agentId = document.getElementById("llmAgentSelect").value;
  const count = parseInt(document.getElementById("llmCount").value, 10) || 1;
  const body = {
    agent_ids: agentId ? [parseInt(agentId, 10)] : [],
    count_per_agent: count,
    question_type: document.getElementById("llmType").value,
    difficulty: document.getElementById("llmDifficulty").value,
    formalize_lean: document.getElementById("llmFormalize").checked,
  };
  const jobs = (agentId ? 1 : Math.max(1, document.getElementById("llmAgentSelect").options.length - 1)) * count;
  btn.disabled = true;
  btn.textContent = "⏳ Đang sinh và kiểm chứng...";
  box.innerHTML = `<p style="font-size:0.85rem;">⏳ Đang chạy ${jobs} lượt sinh song song. Mỗi câu gồm: sinh đề → bộ giải độc lập → đối chiếu trên lưới tham số (có thể mất vài phút)...</p>`;
  try {
    const res = await fetch("/api/llm/generate", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    });
    const data = await res.json();
    if (!res.ok) throw new Error(data.detail || res.statusText);
    box.innerHTML = `
      <p style="font-weight:600; margin-bottom:0.5rem;">
        Kết quả: ${data.accepted}/${data.requested} câu được chấp nhận • ${data.rejected} bị loại • ${(data.wall_clock_ms / 1000).toFixed(1)}s
      </p>
      ${data.results.map(r => `
        <div style="padding:0.55rem 0.8rem; border-bottom:1px solid var(--border); font-size:0.82rem;">
          <span class="badge ${r.status === "ACCEPTED" ? "badge-success" : "badge-amber"}">${escapeHtml(r.status)}</span>
          <b>${escapeHtml(r.code || "-")}</b> • ${escapeHtml(r.agent_name)} • ${escapeHtml(r.question_type)} • ${r.attempts} lần thử
          <div>${escapeHtml(r.title || "")}</div>
          ${r.status === "ACCEPTED"
            ? `<div style="color:var(--text-muted);">Khớp bộ giải độc lập tại ${r.valid_points} giá trị tham số${r.forbidden && r.forbidden.length ? ` • loại các giá trị gây trùng: ${escapeHtml(r.forbidden.join(", "))}` : ""}</div>`
            : `<div style="color:var(--danger);">${escapeHtml(r.reason || "")}</div>`}
          ${r.history && r.history.length && r.status === "ACCEPTED" ? `<div style="color:var(--text-muted);">Đã sửa sau: ${escapeHtml(r.history.join(" | "))}</div>` : ""}
          ${r.lean_mathlib ? `<div>📐 Lean + Mathlib: <b>${escapeHtml(r.lean_mathlib.status)}</b> (${r.lean_mathlib.attempts} lần) — ${escapeHtml(r.lean_mathlib.summary)}</div>` : ""}
        </div>
      `).join("")}
    `;
    await loadDashboard();
  } catch (err) {
    box.innerHTML = `<p style="color:var(--danger);">Lỗi sinh câu hỏi: ${escapeHtml(String(err.message || err))}</p>`;
  } finally {
    btn.disabled = false;
    btn.textContent = "✨ Sinh Câu Hỏi Bằng LLM";
  }
}

async function formalizeQuestion(code) {
  const btn = document.getElementById(`btnFormalize-${code}`);
  const badge = document.getElementById(`mathlibBadge-${code}`);
  btn.disabled = true;
  btn.textContent = "⏳ LLM đang formalize, Lean đang biên dịch (có thể vài phút)...";
  try {
    const res = await fetch(`/api/questions/${encodeURIComponent(code)}/formalize`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({}),
    });
    const data = await res.json();
    if (!res.ok) throw new Error(data.detail || res.statusText);
    badge.textContent = `📐 Mathlib: ${data.status}`;
    badge.className = `badge ${data.status === "VERIFIED_PASS" ? "badge-success" : "badge-amber"}`;
    const codeBox = document.getElementById(`mathlibCode-${code}`);
    const outBox = document.getElementById(`mathlibOut-${code}`);
    if (codeBox) codeBox.textContent = data.lean_code || "";
    if (outBox) outBox.textContent = `Output: ${data.summary}${data.review && data.review.issues ? "\nPhản biện: " + data.review.issues : ""}`;
    const drawer = document.getElementById(`codeDrawer-${code}`);
    if (drawer) drawer.classList.add("open");
  } catch (err) {
    alert("Lỗi formalize: " + (err.message || err));
  } finally {
    btn.disabled = false;
    btn.textContent = "📐 Formalize bằng Lean + Mathlib";
  }
}

async function deleteLLMQuestion(code) {
  if (!confirm(`Xóa câu hỏi ${code} khỏi ngân hàng?`)) return;
  const res = await fetch(`/api/questions/${encodeURIComponent(code)}`, { method: "DELETE" });
  if (!res.ok) {
    const data = await res.json();
    alert(data.detail || "Không xóa được câu hỏi");
    return;
  }
  const card = document.getElementById(`qcard-${code}`);
  if (card) card.remove();
}

function debounceLoadQuestions() {
  if (searchDebounceTimer) clearTimeout(searchDebounceTimer);
  searchDebounceTimer = setTimeout(() => loadQuestions(), 250);
}

async function loadQuestions() {
  const subject = document.getElementById("filterSubject").value;
  const qtype = document.getElementById("filterType").value;
  const agentId = document.getElementById("filterAgent").value;
  const mode = document.getElementById("filterParamMode").value;
  const search = document.getElementById("filterSearch").value.trim();

  const params = new URLSearchParams();
  if (subject && subject !== "ALL") params.set("subject", subject);
  if (qtype && qtype !== "ALL") params.set("question_type", qtype);
  if (agentId) params.set("agent_id", agentId);
  if (search) params.set("search", search);
  params.set("mode", mode);

  const container = document.getElementById("questionsListContainer");
  container.innerHTML = `<p style="padding: 1rem; color: var(--text-muted);">⏳ Đang tải ngân hàng câu hỏi và tính toán tham số...</p>`;

  try {
    const res = await fetch(`/api/questions?${params.toString()}`);
    const data = await res.json();
    document.getElementById("questionCountBadge").textContent = `${data.total} câu hỏi`;

    if (!data.questions || data.questions.length === 0) {
      container.innerHTML = `<p style="padding: 1rem;">Không tìm thấy câu hỏi phù hợp bộ lọc.</p>`;
      return;
    }

    globalQuestionsCache = {};
    data.questions.forEach(q => {
      globalQuestionsCache[q.code] = q;
    });

    container.innerHTML = data.questions.map(q => buildQuestionCardHtml(q)).join("");
    renderMath(container);
  } catch (err) {
    container.innerHTML = `<p style="color: var(--danger);">Lỗi tải câu hỏi: ${err}</p>`;
  }
}

function buildQuestionCardHtml(q) {
  const ev = q.evaluated_preview || {};
  const isMcq = q.question_type === "mcq";
  const schema = Array.isArray(q.parameters_schema) ? q.parameters_schema : [];
  const activeParams = ev.active_parameters || {};

  // Parameter Input Controls
  let paramControlsHtml = "";
  if (q.has_parameters && schema.length > 0) {
    const inputs = schema.map(p => {
      const val = activeParams[p.name] !== undefined ? activeParams[p.name] : p.default;
      return `
        <div class="param-input-item">
          <span>Tham số $${p.symbol || p.name} = $</span>
          <input type="number" id="param-${q.code}-${p.name}" value="${val}" min="${p.min ?? -20}" max="${p.max ?? 50}" step="${p.step ?? 1}"
            onchange="recalculateQuestionParams('${q.code}')" />
        </div>
      `;
    }).join("");

    paramControlsHtml = `
      <div class="param-box">
        <div class="param-controls">
          <span class="badge badge-amber">🎛️ Biến thiên Tham số</span>
          ${inputs}
          <span id="paramTargetBadge-${q.code}" style="font-size: 0.85rem; color: #78350f; font-weight: 600;">
            ${ev.target_evaluated_latex ? `Kết quả tại tham số: $${ev.target_evaluated_latex}$` : ""}
          </span>
        </div>
        <div style="display:flex; gap: 0.45rem;">
          <button class="btn btn-sm btn-primary" onclick="recalculateQuestionParams('${q.code}')">
            🧮 Tính theo tham số
          </button>
          <button class="btn btn-sm btn-accent" onclick="randomizeQuestionParams('${q.code}')">
            🎲 Ngẫu nhiên tham số
          </button>
        </div>
      </div>
    `;
  }

  // Options HTML for MCQ
  let optionsHtml = "";
  if (isMcq && ev.options) {
    optionsHtml = `
      <div class="options-grid" id="optionsGrid-${q.code}">
        ${["A", "B", "C", "D"].map(k => {
          const opt = ev.options[k] || {};
          const isCorrect = q.correct_option === k;
          return `
            <div class="option-item ${isCorrect ? "correct-highlight" : ""}">
              <span class="option-key">${k}</span>
              <div style="flex:1;">
                <div>${opt.display || opt.symbolic || ""}</div>
                ${isCorrect ? `<div style="font-size:0.74rem; color: var(--success); font-weight:700; margin-top:0.2rem;">✓ Đáp án đúng (Đã kiểm chứng LEAN 4 & Python)</div>` : ""}
              </div>
            </div>
          `;
        }).join("")}
      </div>
    `;
  }

  return `
    <div class="question-card" id="qcard-${q.code}">
      <div class="question-meta">
        <div class="question-tags">
          <span class="badge ${q.subject === "Giải tích" ? "badge-blue" : "badge-purple"}">${escapeHtml(q.subject)}</span>
          <span class="badge badge-amber">${isMcq ? "Trắc nghiệm Tham số" : "Tự luận & Chứng minh"}</span>
          <span style="font-weight: 800; font-family: monospace; color: #1e293b;">[${escapeHtml(q.code)}]</span>
          ${q.source === "llm" ? `<span class="badge badge-purple">🤖 Do LLM sinh</span>` : ""}
          <span style="font-size: 0.8rem; color: var(--text-muted);">• ${escapeHtml(q.agent_name)} • ${escapeHtml(q.topic)}</span>
        </div>
        <div class="question-tags">
          <span class="badge badge-success" id="leanBadge-${q.code}">🏛️ LEAN 4: ${escapeHtml(q.lean4_status)} (${Math.round(q.lean4_elapsed_ms || 0)}ms)</span>
          <span class="badge badge-success" id="pyBadge-${q.code}">🐍 Python: ${escapeHtml(q.python_status)} (${Math.round(q.python_elapsed_ms || 0)}ms)</span>
          <span class="badge ${q.lean4_mathlib_status === "VERIFIED_PASS" ? "badge-success" : "badge-amber"}" id="mathlibBadge-${q.code}">📐 Mathlib: ${escapeHtml(q.lean4_mathlib_status || "NOT_RUN")}</span>
        </div>
      </div>

      <div class="question-title">${escapeHtml(q.title)}</div>

      <div class="question-stem" id="stemBox-${q.code}">
        ${formatTextWithParagraphs(ev.stem_display || q.stem_symbolic)}
      </div>

      ${paramControlsHtml}
      ${optionsHtml}

      <div class="drawer-toggle-bar">
        <button class="btn btn-sm btn-outline" onclick="toggleDrawer('solDrawer-${q.code}')">
          📖 Xem Lời Giải Chi Tiết & Rubric
        </button>
        <button class="btn btn-sm btn-outline" onclick="toggleDrawer('codeDrawer-${q.code}')">
          🔬 Xem Mã Kiểm Chứng LEAN 4 & Script Python
        </button>
        <button class="btn btn-sm btn-success" onclick="reverifySingleQuestion('${q.code}')" id="btnVerify-${q.code}">
          ▶️ Chạy Kiểm Chứng Thực Tế LEAN 4 + Python
        </button>
        <button class="btn btn-sm btn-outline" onclick="loadQuestionIntoSandbox('${q.code}')">
          🧪 Mở trong Sandbox
        </button>
        <button class="btn btn-sm btn-outline" onclick="formalizeQuestion('${q.code}')" id="btnFormalize-${q.code}">
          📐 Formalize bằng Lean + Mathlib
        </button>
        ${q.source === "llm" ? `<button class="btn btn-sm btn-outline" onclick="deleteLLMQuestion('${q.code}')">🗑️ Xóa câu này</button>` : ""}
      </div>

      <div class="drawer-content" id="solDrawer-${q.code}">
        <div class="solution-box" id="solBox-${q.code}">
          <h4 style="margin-bottom:0.45rem; color: #065f46;">💡 Lời Giải Chi Tiết & Phân Tích Tham Số (${isMcq ? `Đáp án đúng: ${q.correct_option}` : "Tự luận"}):</h4>
          <div>${formatTextWithParagraphs(ev.solution_display || q.solution_symbolic)}</div>
        </div>
      </div>

      <div class="drawer-content" id="codeDrawer-${q.code}">
        <div class="code-dual-grid">
          <div class="code-panel">
            <div class="code-header">
              <span>🏛️ LEAN 4.35.0 Formal Proof (${escapeHtml(q.code)}.lean)</span>
              <span class="badge badge-success">${escapeHtml(q.lean4_status)}</span>
            </div>
            <div class="code-body">${escapeHtml(q.lean4_code)}</div>
            <div class="code-output" id="leanOut-${q.code}">Output: ${escapeHtml(q.lean4_output)}</div>
          </div>
          <div class="code-panel">
            <div class="code-header">
              <span>🐍 Python SymPy/NumPy Verification (${escapeHtml(q.code)}.py)</span>
              <span class="badge badge-success">${escapeHtml(q.python_status)}</span>
            </div>
            <div class="code-body">${escapeHtml(q.python_code)}</div>
            <div class="code-output" id="pyOut-${q.code}">Output: ${escapeHtml(q.python_output)}</div>
          </div>
        </div>
        <div class="code-panel" style="margin-top:0.8rem;">
          <div class="code-header">
            <span>📐 Lean 4 + Mathlib (formalize bởi LLM, đáp án do hệ thống điền)</span>
            <span class="badge ${q.lean4_mathlib_status === "VERIFIED_PASS" ? "badge-success" : "badge-amber"}">${escapeHtml(q.lean4_mathlib_status || "NOT_RUN")}</span>
          </div>
          <div class="code-body" id="mathlibCode-${q.code}">${escapeHtml(q.lean4_mathlib_code || "-- Chưa formalize. Bấm “Formalize bằng Lean + Mathlib”.")}</div>
          <div class="code-output" id="mathlibOut-${q.code}">Output: ${escapeHtml(q.lean4_mathlib_output || "")}${q.lean4_mathlib_review ? "\nPhản biện: " + escapeHtml(q.lean4_mathlib_review) : ""}</div>
        </div>
      </div>
    </div>
  `;
}

function toggleDrawer(drawerId) {
  const el = document.getElementById(drawerId);
  if (el) {
    el.classList.toggle("open");
    if (el.classList.contains("open")) {
      renderMath(el);
    }
  }
}

async function recalculateQuestionParams(code) {
  const q = globalQuestionsCache[code];
  if (!q) return;
  const schema = Array.isArray(q.parameters_schema) ? q.parameters_schema : [];
  const params = {};
  schema.forEach(p => {
    const inp = document.getElementById(`param-${code}-${p.name}`);
    if (inp) params[p.name] = parseFloat(inp.value);
  });
  const mode = document.getElementById("filterParamMode").value || "dual";

  try {
    const res = await fetch(`/api/questions/${code}/evaluate`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ parameters: params, mode })
    });
    const ev = await res.json();
    updateQuestionCardWithEvaluation(code, ev);
  } catch (err) {
    console.error("Evaluate error:", err);
  }
}

async function randomizeQuestionParams(code) {
  const mode = document.getElementById("filterParamMode").value || "dual";
  try {
    const res = await fetch(`/api/questions/${code}/randomize?mode=${mode}`, { method: "POST" });
    const ev = await res.json();
    // Update input fields
    if (ev.active_parameters) {
      Object.entries(ev.active_parameters).forEach(([k, v]) => {
        const inp = document.getElementById(`param-${code}-${k}`);
        if (inp) inp.value = v;
      });
    }
    updateQuestionCardWithEvaluation(code, ev);
  } catch (err) {
    console.error("Randomize error:", err);
  }
}

function updateQuestionCardWithEvaluation(code, ev) {
  const q = globalQuestionsCache[code];
  if (!q) return;

  const stemBox = document.getElementById(`stemBox-${code}`);
  if (stemBox) {
    stemBox.innerHTML = formatTextWithParagraphs(ev.stem_display);
    renderMath(stemBox);
  }

  const targetBadge = document.getElementById(`paramTargetBadge-${code}`);
  if (targetBadge) {
    targetBadge.innerHTML = ev.target_evaluated_latex ? `Kết quả tại tham số: $${ev.target_evaluated_latex}$` : "";
    renderMath(targetBadge);
  }

  const optionsGrid = document.getElementById(`optionsGrid-${code}`);
  if (optionsGrid && ev.options) {
    optionsGrid.innerHTML = ["A", "B", "C", "D"].map(k => {
      const opt = ev.options[k] || {};
      const isCorrect = q.correct_option === k;
      return `
        <div class="option-item ${isCorrect ? "correct-highlight" : ""}">
          <span class="option-key">${k}</span>
          <div style="flex:1;">
            <div>${opt.display || opt.symbolic || ""}</div>
            ${isCorrect ? `<div style="font-size:0.74rem; color: var(--success); font-weight:700; margin-top:0.2rem;">✓ Đáp án đúng (Đã kiểm chứng LEAN 4 & Python)</div>` : ""}
          </div>
        </div>
      `;
    }).join("");
    renderMath(optionsGrid);
  }

  const solBox = document.getElementById(`solBox-${code}`);
  if (solBox && ev.solution_display) {
    solBox.innerHTML = `
      <h4 style="margin-bottom:0.45rem; color: #065f46;">💡 Lời Giải Chi Tiết & Phân Tích Tham Số (${q.question_type === "mcq" ? `Đáp án đúng: ${q.correct_option}` : "Tự luận"}):</h4>
      <div>${formatTextWithParagraphs(ev.solution_display)}</div>
    `;
    renderMath(solBox);
  }
}

async function reverifySingleQuestion(code) {
  const btn = document.getElementById(`btnVerify-${code}`);
  if (btn) {
    btn.disabled = true;
    btn.textContent = "⏳ Đang chạy lean.exe & python.exe...";
  }
  try {
    const res = await fetch(`/api/questions/${code}/verify`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({})
    });
    const data = await res.json();
    const leanBadge = document.getElementById(`leanBadge-${code}`);
    const pyBadge = document.getElementById(`pyBadge-${code}`);
    const leanOut = document.getElementById(`leanOut-${code}`);
    const pyOut = document.getElementById(`pyOut-${code}`);

    if (leanBadge) leanBadge.textContent = `🏛️ LEAN 4: ${data.lean4.status} (${Math.round(data.lean4.elapsed_ms)}ms)`;
    if (pyBadge) pyBadge.textContent = `🐍 Python: ${data.python.status} (${Math.round(data.python.elapsed_ms)}ms)`;
    if (leanOut) leanOut.textContent = `Output: ${data.lean4.output}`;
    if (pyOut) pyOut.textContent = `Output: ${data.python.output}`;

    const codeDrawer = document.getElementById(`codeDrawer-${code}`);
    if (codeDrawer && !codeDrawer.classList.contains("open")) {
      codeDrawer.classList.add("open");
    }
  } catch (err) {
    alert("Lỗi kiểm chứng: " + err);
  } finally {
    if (btn) {
      btn.disabled = false;
      btn.textContent = "▶️ Chạy Kiểm Chứng Thực Tế LEAN 4 + Python";
    }
  }
}

function loadQuestionIntoSandbox(code) {
  const q = globalQuestionsCache[code];
  if (!q) return;
  document.getElementById("sandboxLeanCode").value = q.lean4_code || "";
  document.getElementById("sandboxPythonCode").value = q.python_code || "";
  switchTab("sandbox");
}

async function runSandboxVerification() {
  const btn = document.getElementById("btnRunSandbox");
  const outBox = document.getElementById("sandboxResultBox");
  const leanCode = document.getElementById("sandboxLeanCode").value;
  const pyCode = document.getElementById("sandboxPythonCode").value;

  btn.disabled = true;
  btn.textContent = "⏳ Đang biên dịch LEAN 4.35.0 & chạy Python...";
  outBox.innerHTML = `<p>Đang thực thi trình biên dịch <code>lean.exe</code> và <code>python.exe</code>...</p>`;

  try {
    const res = await fetch("/api/sandbox/verify", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        code_id: "SANDBOX-LIVE",
        lean4_code: leanCode,
        python_code: pyCode
      })
    });
    const data = await res.json();
    outBox.innerHTML = `
      <div class="section-card" style="background:#f8fafc; margin-bottom:0;">
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:0.8rem;">
          <h3>Phán Quyết Cổng Giám Đốc Thẩm @gng5: <span class="badge ${data.sovereign_verdict === "SOVEREIGN_PASSED" ? "badge-success" : "badge-amber"}">${data.sovereign_verdict}</span></h3>
          <span style="font-family:monospace; font-size:0.78rem;">Merkle Node: ${data.merkle_hash.slice(0, 24)}...</span>
        </div>
        <div class="code-dual-grid">
          <div class="code-panel">
            <div class="code-header">
              <span>Kết quả Trình biên dịch LEAN 4.35.0 (${data.lean4.elapsed_ms} ms)</span>
              <span class="badge ${data.lean4.status === "VERIFIED_PASS" ? "badge-success" : "badge-amber"}">${data.lean4.status}</span>
            </div>
            <div class="code-output">${escapeHtml(data.lean4.output)}</div>
          </div>
          <div class="code-panel">
            <div class="code-header">
              <span>Kết quả Chạy Số & Ký Hiệu Python (${data.python.elapsed_ms} ms)</span>
              <span class="badge ${data.python.status === "VERIFIED_PASS" ? "badge-success" : "badge-amber"}">${data.python.status}</span>
            </div>
            <div class="code-output">${escapeHtml(data.python.output)}</div>
          </div>
        </div>
      </div>
    `;
  } catch (err) {
    outBox.innerHTML = `<p style="color:var(--danger);">Lỗi: ${err}</p>`;
  } finally {
    btn.disabled = false;
    btn.textContent = "▶️ Chạy Kiểm Chứng Kép (LEAN 4 + Python)";
  }
}

// EXAM BUILDER & ONLINE TEST
async function loadSavedExams() {
  try {
    const res = await fetch("/api/exams");
    const data = await res.json();
    const box = document.getElementById("savedExamsList");
    if (!data.exams || data.exams.length === 0) {
      box.innerHTML = `<span style="font-size: 0.84rem; color: var(--text-muted);">Chưa có đề thi nào. Hãy bấm "⚡ Sinh Đề Thi Mới & Lưu CSDL" để tạo đề đầu tiên!</span>`;
      return;
    }
    box.innerHTML = data.exams.map(ex => `
      <button class="btn btn-sm btn-outline" onclick="openSavedExam(${ex.id})">
        📄 ${escapeHtml(ex.exam_code)} (${ex.mcq_count} TN + ${ex.essay_count} TL • ${escapeHtml(ex.subject_filter)})
      </button>
    `).join("");
    if (!activeExamData && data.exams.length > 0) {
      openSavedExam(data.exams[0].id);
    }
  } catch (err) {
    console.error("Load exams error:", err);
  }
}

async function generateNewExam() {
  const title = document.getElementById("examTitleInput").value;
  const subject_filter = document.getElementById("examSubjectInput").value;
  const mcq_count = parseInt(document.getElementById("examMcqCount").value || "10", 10);
  const essay_count = parseInt(document.getElementById("examEssayCount").value || "4", 10);
  const parameter_mode = document.getElementById("examParamMode").value;
  const duration_minutes = parseInt(document.getElementById("examDuration").value || "90", 10);
  const trust_level = document.getElementById("examTrustLevel").value;

  const container = document.getElementById("activeExamContainer");
  container.innerHTML = `<div class="section-card"><p>⏳ Các Agent đang rút trích câu hỏi, sinh bộ tham số ngẫu nhiên phân biệt và đóng gói đề thi...</p></div>`;

  try {
    const res = await fetch("/api/exams/generate", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        title,
        subject_filter,
        mcq_count,
        essay_count,
        parameter_mode,
        randomize_parameters: true,
        duration_minutes,
        trust_level
      })
    });
    const exam = await res.json();
    activeExamData = exam;
    userExamChoices = {};
    await loadSavedExams();
    renderActiveExam(exam);
  } catch (err) {
    container.innerHTML = `<div class="section-card"><p style="color:var(--danger);">Lỗi sinh đề: ${err}</p></div>`;
  }
}

async function openSavedExam(examId) {
  try {
    const res = await fetch(`/api/exams/${examId}`);
    const exam = await res.json();
    activeExamData = exam;
    userExamChoices = {};
    renderActiveExam(exam);
  } catch (err) {
    console.error("Open exam error:", err);
  }
}

function renderActiveExam(exam) {
  const container = document.getElementById("activeExamContainer");
  const mcqs = (exam.questions || []).filter(q => q.question_type === "mcq");
  const essays = (exam.questions || []).filter(q => q.question_type === "essay");

  container.innerHTML = `
    <div class="section-card">
      <div class="section-header">
        <div>
          <h2>📄 ${escapeHtml(exam.title)}</h2>
          <p style="font-size: 0.84rem; color: var(--text-muted);">
            Mã đề: <b>${escapeHtml(exam.exam_code)}</b> • Thời gian: <b>${exam.duration_minutes} phút</b> •
            Cấu trúc: <b>${exam.mcq_count} Trắc nghiệm + ${exam.essay_count} Tự luận</b> (${exam.parametric_count} câu có tham số) •
            Merkle Root: <code>${escapeHtml((exam.merkle_root || "").slice(0, 20))}...</code>
          </p>
        </div>
        <div style="display:flex; gap:0.5rem;">
          <a class="btn btn-outline" href="/api/exams/${exam.id}/export-latex" target="_blank">
            📥 Xuất Mã Nguồn LaTeX (.tex)
          </a>
          <button class="btn btn-primary" onclick="submitActiveExam(${exam.id})">
            ✅ Nộp Bài & Chấm Điểm Tự Động
          </button>
        </div>
      </div>

      <div id="examGradingResultBox"></div>

      <h3 style="margin: 1rem 0 0.8rem; color: var(--primary);">PHẦN I: TRẮC NGHIỆM KHÁCH QUAN CÓ THAM SỐ (${mcqs.length} câu)</h3>
      ${mcqs.map(q => {
        const opts = q.options || {};
        return `
          <div class="question-card" id="exam-q-${q.code}">
            <div class="question-meta">
              <div class="question-tags">
                <span class="badge badge-blue">Câu ${q.order_index}</span>
                <b>[${escapeHtml(q.code)}]</b>
                <span>${escapeHtml(q.subject)} — ${escapeHtml(q.topic)}</span>
                ${q.param_summary_latex ? `<span class="badge badge-amber">Tham số: $${q.param_summary_latex}$</span>` : ""}
              </div>
              <div class="question-tags">
                <span class="badge badge-success">LEAN 4: ${escapeHtml(q.lean4_status)}</span>
                <span class="badge badge-success">Python: ${escapeHtml(q.python_status)}</span>
              </div>
            </div>
            <div class="question-stem">${formatTextWithParagraphs(q.stem_display)}</div>
            <div class="options-grid">
              ${["A", "B", "C", "D"].map(k => {
                const o = opts[k] || {};
                return `
                  <div class="option-item selectable" id="examOpt-${q.code}-${k}" onclick="selectExamOption('${q.code}', '${k}')">
                    <span class="option-key">${k}</span>
                    <div>${o.display || o.symbolic || ""}</div>
                  </div>
                `;
              }).join("")}
            </div>
            <div class="drawer-content" id="examSol-${q.code}">
              <div class="solution-box">
                <b>Đáp án đúng: ${q.correct_option}</b> ${q.target_evaluated_latex ? `($${q.target_evaluated_latex}$)` : ""}<br/>
                ${formatTextWithParagraphs(q.solution_display)}
              </div>
            </div>
          </div>
        `;
      }).join("")}

      <h3 style="margin: 1.5rem 0 0.8rem; color: var(--purple);">PHẦN II: TỰ LUẬN TOÁN CAO CẤP (${essays.length} câu)</h3>
      ${essays.map(q => `
        <div class="question-card">
          <div class="question-meta">
            <div class="question-tags">
              <span class="badge badge-purple">Câu ${q.order_index} (Tự luận)</span>
              <b>[${escapeHtml(q.code)}]</b>
              <span>${escapeHtml(q.subject)} — ${escapeHtml(q.topic)}</span>
              ${q.param_summary_latex ? `<span class="badge badge-amber">Tham số: $${q.param_summary_latex}$</span>` : ""}
            </div>
            <div class="question-tags">
              <span class="badge badge-success">LEAN 4: ${escapeHtml(q.lean4_status)}</span>
              <span class="badge badge-success">Python: ${escapeHtml(q.python_status)}</span>
            </div>
          </div>
          <div class="question-stem">${formatTextWithParagraphs(q.stem_display)}</div>
          <div class="drawer-toggle-bar">
            <button class="btn btn-sm btn-outline" onclick="toggleDrawer('examSol-${q.code}')">
              📖 Xem Đáp Án & Thang Điểm Tự Luận (Rubric)
            </button>
          </div>
          <div class="drawer-content" id="examSol-${q.code}">
            <div class="solution-box">
              ${q.target_evaluated_latex ? `<b>Đáp số${q.param_summary_latex ? ` (với $${q.param_summary_latex}$)` : ""}: $${q.target_evaluated_latex}$</b><br/>` : ""}
              ${formatTextWithParagraphs(q.solution_display)}
            </div>
          </div>
        </div>
      `).join("")}
    </div>
  `;
  renderMath(container);
}

function selectExamOption(qcode, optKey) {
  userExamChoices[qcode] = optKey;
  ["A", "B", "C", "D"].forEach(k => {
    const el = document.getElementById(`examOpt-${qcode}-${k}`);
    if (el) {
      if (k === optKey) el.classList.add("selected");
      else el.classList.remove("selected");
    }
  });
}

async function submitActiveExam(examId) {
  try {
    const res = await fetch(`/api/exams/${examId}/submit`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        student_name: "Sinh viên ĐHBK",
        mcq_answers: userExamChoices,
        essay_self_scores: {}
      })
    });
    const result = await res.json();
    const box = document.getElementById("examGradingResultBox");
    box.innerHTML = `
      <div style="background: #ecfdf5; border: 2px solid #10b981; border-radius: 10px; padding: 1rem 1.2rem; margin-bottom: 1.2rem;">
        <h3 style="color: #065f46;">🏆 Kết Quả Chấm Điểm Tự Động: ${result.score} / 10.0 điểm</h3>
        <p style="font-size: 0.88rem; color: #047857;">
          Trắc nghiệm đúng: <b>${result.mcq_correct} / ${result.mcq_total}</b> câu • Tự luận đã đối chiếu đáp án chuẩn: <b>${result.essay_total}</b> câu.
          Đã tự động mở toàn bộ lời giải chi tiết bên dưới!
        </p>
      </div>
    `;
    // Open all solution drawers in exam
    (activeExamData.questions || []).forEach(q => {
      const sol = document.getElementById(`examSol-${q.code}`);
      if (sol) sol.classList.add("open");
      const correctEl = document.getElementById(`examOpt-${q.code}-${q.correct_option}`);
      if (correctEl) correctEl.classList.add("correct-highlight");
    });
    renderMath(document.getElementById("activeExamContainer"));
  } catch (err) {
    alert("Lỗi chấm bài: " + err);
  }
}

async function loadMerkleLedger() {
  const box = document.getElementById("merkleLedgerContainer");
  box.innerHTML = `<p>Đang tải Sổ cái Bất biến Merkle DAG...</p>`;
  try {
    const res = await fetch("/api/merkle-ledger");
    const data = await res.json();
    const nodes = (data.nodes || []).slice().reverse();
    box.innerHTML = `
      <div style="background: #0f172a; color: #f8fafc; padding: 1rem 1.2rem; border-radius: 10px; margin-bottom: 1rem; font-family: monospace; font-size: 0.84rem;">
        <div><b>Hệ thống:</b> ${escapeHtml(data.system)}</div>
        <div><b>Merkle Root Hiện Hành (SHA-256):</b> <span style="color:#fde68a;">${escapeHtml(data.merkle_root)}</span></div>
        <div><b>Tổng số Nút Bất Biến:</b> ${data.total_nodes}</div>
      </div>
      <div style="max-height: 500px; overflow-y: auto;">
        ${nodes.map(n => `
          <div style="padding: 0.75rem 1rem; border: 1px solid var(--border); border-radius: 8px; margin-bottom: 0.6rem; background: #f8fafc; font-size: 0.82rem;">
            <div style="display:flex; justify-content:space-between; font-family:monospace; font-weight:700;">
              <span style="color: var(--primary);">${escapeHtml(n.node_id)} [${escapeHtml(n.node_type)}]</span>
              <span style="color: var(--success);">SHA-256: ${escapeHtml(n.hash)}</span>
            </div>
            <pre style="margin-top:0.4rem; font-size:0.76rem; color: #334155; overflow-x:auto;">${escapeHtml(JSON.stringify(n.payload, null, 2))}</pre>
          </div>
        `).join("")}
      </div>
    `;
  } catch (err) {
    box.innerHTML = `<p style="color:var(--danger);">Lỗi tải sổ cái: ${err}</p>`;
  }
}

window.addEventListener("DOMContentLoaded", () => {
  loadDashboard();
});
