@echo off
chcp 65001 >nul
title @gng5 Sovereign Higher Math Exam System (20-Agent Swarm + LEAN 4.35.0 + Python)
echo ===============================================================================
echo   @gng5 HỆ THỐNG WEB SINH ĐỀ TOÁN CAO CẤP (GIẢI TÍCH & ĐẠI SỐ)
echo   Kiểm chứng kép: LEAN 4.35.0 + Python SymPy/NumPy ^| 20 Agent Song Song
echo ===============================================================================
cd /d "%~dp0"
rem LLM: Claude qua Claude Code CLI, dùng gói claude.ai (Pro/Max) đã đăng nhập, không cần API key
set MATH_LLM_PROVIDER=claude-cli
rem Haiku (Claude Haiku 5.5) cho moi buoc: sinh de, solver, viet menh de, luot chung minh dau tien
set MATH_LLM_MODEL=haiku
rem Lean bao chung minh sai: cac luot sua chung minh chuyen sang Sonnet (Claude Sonnet 5.5)
set MATH_PROOF_ESCALATE_MODEL=sonnet
rem Mức suy nghĩ: low (nhanh, ít token) | medium | high
set MATH_LLM_EFFORT=low
rem So luot goi LLM chay cung luc (moi luot ~215 MB RAM); Lean van chay tung luot mot
set MATH_CLAUDE_CLI_MAX_PARALLEL=4
rem Chờ server trả lời được rồi mới mở trình duyệt (tránh lỗi "không kết nối được" khi server còn đang khởi động)
start "" /b powershell -NoProfile -WindowStyle Hidden -Command "for($i=0;$i -lt 240;$i++){try{Invoke-WebRequest http://127.0.0.1:8088/ -UseBasicParsing -TimeoutSec 2 | Out-Null; break}catch{Start-Sleep -Milliseconds 500}}; Start-Process http://127.0.0.1:8088"
python app.py
pause
