#!/usr/bin/env bash
# Build the Hugo site and assert the shipped homepage answers the five
# playbook.html "Website rewrite" questions. This drives `hugo` and reads
# public/index.html — it does not reimplement the templates.
set -euo pipefail

root="$(cd "$(dirname "$0")/.." && pwd)"
cd "$root"

if ! command -v hugo >/dev/null 2>&1; then
  echo "FAIL: hugo not on PATH" >&2
  exit 1
fi

hugo --minify --cleanDestinationDir

home="$root/public/index.html"
if [[ ! -f "$home" ]]; then
  echo "FAIL: missing $home" >&2
  exit 1
fi

python3 - "$home" <<'PY'
import sys
from pathlib import Path

html = Path(sys.argv[1]).read_text(encoding="utf-8", errors="replace")
low = html.lower()

def need(label, pred):
    if not pred:
        print(f"FAIL: {label}", file=sys.stderr)
        sys.exit(1)
    print(f"PASS: {label}")

need("who: engineer building reliable AI-agent and security systems",
     "engineer building reliable ai-agent and security systems" in low)
need("thesis: memory, deterministic constraints, evaluation, and observability",
     "memory, deterministic constraints, evaluation, and observability" in low)
need("built: Memori", "memori" in low)
need("built: Luffy", "luffy" in low)
need("built: Memori evidence URL", "github.com/archit15singh/memori" in low)
need("built: Luffy evidence URL", "github.com/archit15singh/luffy-pr-review-agent" in low)
need("research: agent memory", "agent memory" in low)
need("research: agent reliability", "agent reliability" in low)
need("research: AI security", "ai security" in low)
need("research: enterprise systems", "enterprise systems" in low)
need("evidence: GitHub", "github.com/archit15singh" in low)
need("intro title: AI Agents × Security × Systems",
     "ai agents" in low and "security" in low and "systems" in low)
print("PASS: homepage five-answer check")
PY
