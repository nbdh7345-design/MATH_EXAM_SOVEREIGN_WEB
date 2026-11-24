# TIN CẬY (an toàn) — ảnh sandbox chạy Lean (mục 13.2).
# Chứa đúng toolchain Lean của dự án. Mathlib và mã dự án được gắn vào lúc chạy, chỉ đọc.
FROM ubuntu:24.04

ARG LEAN_TOOLCHAIN=leanprover/lean4:v4.36.0

RUN apt-get update \
 && apt-get install -y --no-install-recommends ca-certificates curl git \
 && rm -rf /var/lib/apt/lists/*

# elan cài vào /opt/elan để mọi uid đọc được; lúc chạy gọi thẳng toolchain, không qua elan
ENV ELAN_HOME=/opt/elan
RUN curl -sSfL https://elan.lean-lang.org/elan-init.sh -o /tmp/elan-init.sh \
 && sh /tmp/elan-init.sh -y --no-modify-path --default-toolchain "${LEAN_TOOLCHAIN}" \
 && rm /tmp/elan-init.sh \
 && /opt/elan/bin/elan toolchain install "${LEAN_TOOLCHAIN}" \
 && chmod -R a+rX /opt/elan

COPY chay_lean.sh /usr/local/bin/chay_lean.sh
RUN chmod 0755 /usr/local/bin/chay_lean.sh

WORKDIR /du_an
ENTRYPOINT ["/usr/local/bin/chay_lean.sh"]
