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

projects="$root/public/projects/index.html"
about="$root/public/about/index.html"
if [[ ! -f "$projects" ]]; then
  echo "FAIL: missing $projects" >&2
  exit 1
fi
if [[ ! -f "$about" ]]; then
  echo "FAIL: missing $about" >&2
  exit 1
fi

research="$root/public/research/index.html"
speaking="$root/public/speaking/index.html"
contact="$root/public/contact/index.html"
for f in "$research" "$speaking" "$contact"; do
  if [[ ! -f "$f" ]]; then
    echo "FAIL: missing $f" >&2
    exit 1
  fi
done

if find "$root/public" \( -iname 'playbook.html' -o -iname 'current_state.json' -o -iname 'search-online-about-me.json' \) | grep -q .; then
  echo "FAIL: local dump shipped in public/" >&2
  exit 1
fi
echo "PASS: playbook.html, current_state.json, search-online-about-me.json not in public/"

python3 - "$home" "$projects" "$about" "$research" "$speaking" "$contact" <<'PY'
import sys
from pathlib import Path

home, projects, about, research, speaking, contact = (
    Path(p).read_text(encoding="utf-8", errors="replace").lower() for p in sys.argv[1:]
)

def need(label, pred):
    if not pred:
        print(f"FAIL: {label}", file=sys.stderr)
        sys.exit(1)
    print(f"PASS: {label}")

for label in ("research", "projects", "writing", "speaking", "about", "contact"):
    need(f"nav: {label}", f">{label}<" in home)

need("home links to /projects/", "projects/" in home)
need("home links to /research/", "research/" in home)

need("projects: Memori flagship", "memori" in projects and "flagship" in projects)
need("projects: Luffy", "luffy" in projects)
need("projects: Memori GitHub", "github.com/archit15singh/memori" in projects)
need("projects: Luffy GitHub", "github.com/archit15singh/luffy-pr-review-agent" in projects)
need("projects: py-memori PyPI", "pypi.org/project/py-memori" in projects)
need("projects: memori-ai-core crates.io", "crates.io/crates/memori-ai-core" in projects)
need("projects: memori-ai-core docs.rs", "docs.rs/crate/memori-ai-core" in projects)
for heading in ("problem", "thesis", "architecture", "implementation", "results", "lessons", "code", "research"):
    need(f"projects spine: {heading}", heading in projects)

need("research: Memory for AI agents", "memory for ai agents" in research)
need("research: Reliable agent systems", "reliable agent systems" in research)
need("research: AI × security", "ai" in research and "security" in research)
need("research: AI-native software engineering", "ai-native software engineering" in research)

need("about: five-question who", "engineer building reliable ai-agent and security systems" in about)
need("about: links to projects", "projects/" in about)
need("speaking page exists", "speaking" in speaking and ("contact" in speaking or "invitat" in speaking))
need("contact: GitHub", "github.com/archit15singh" in contact)
need("contact: LinkedIn", "linkedin.com/in/archit15singh" in contact)
print("PASS: full 0-30d IA check")
PY
