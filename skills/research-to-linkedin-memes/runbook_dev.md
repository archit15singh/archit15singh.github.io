# runbook — research-to-linkedin-memes (verified commands)

Concrete, copy-pasteable commands that were run and verified building this skill, plus the context worth not re-deriving. `SKILL.md` is the how/why; this is the exact "what to type". Run everything from a scratch dir like `/tmp/meme-run/`, never the repo.

## 0. Env (only what a given step needs)

```bash
export IMGFLIP_USERNAME=...   # free account at imgflip.com/signup; API render only
export IMGFLIP_PASSWORD=...   # shell only — NEVER paste in chat; rotate if leaked
export OPENALEX_MAILTO=you@example.com   # optional, faster OpenAlex pool
```
When a Claude agent drives the loop, no `ANTHROPIC_API_KEY` is needed — the agent is the model (sourcing, decomposition, explainer, captions, post copy are done in-conversation).

## 1. Source a paper (openalex) — `-o` is GLOBAL, before the subcommand

```bash
~/.claude/bin/openalex -o json search "self-improving language model agents" -n 15
~/.claude/bin/openalex -o json top "artificial intelligence" -n 10
~/.claude/bin/openalex -o json score W4323655724
```
Returns per work: `id, title, year, cited_by_count, relevance_score, blended_score, authors, doi`.
Recursive online alternative: `WebSearch` the concept → `WebFetch` the best primary sources → treat those as the source. Same rest-of-pipeline.

## 2. Seed the meme template bank (one time)

```bash
mkdir -p bank && curl -s "https://api.imgflip.com/get_memes" \
  | python3 -c "import sys,json; json.dump(json.load(sys.stdin)['data']['memes'], open('bank/templates.json','w'), indent=2); print(len(json.load(open('bank/templates.json'))),'templates')"
```
Get an id + box_count by name:
```bash
python3 -c "import json;b={t['name']:t for t in json.load(open('bank/templates.json'))};[print(b[n]['id'],b[n]['box_count'],n) for n in ['Drake Hotline Bling','Two Buttons','Gru\'s Plan']]"
```
Verified ids: Drake `181913649` (2 boxes), Two Buttons `87743020` (3), Gru's Plan `131940431` (4), Distracted Boyfriend `112126428` (3), Anakin Padme 4 Panel `322841258` (3), Epic Handshake `135256802` (3), Always Has Been `252600902` (2), UNO Draw 25 `217743513` (2), Waiting Skeleton `4087833` (2).

## 3. options.json (v2 schema the UI reads)

```json
{
  "explainer": {
    "paper": {"title":"...","authors":"...","year":2023,"url":"...","doi":"..."},   // PRIVATE provenance; never rendered, never posted
    "concept": "plain descriptive name (NOT the paper's branded term)",
    "hook": "one line that makes it click",
    "plain": "plain, exact, jargon-free explanation",
    "analogy": "everyday analogy",
    "how_it_works": ["step 1","step 2","step 3"],
    "examples": ["example 1","example 2 (different domain)","example 3"],
    "visual": "small ASCII diagram (rendered monospace)",
    "taxonomy": ["node1","node2","node3"]
  },
  "options": [
    {"id":"A","template":"Drake Hotline Bling","template_id":"181913649",
     "captions":["reject line","prefer line"],"post":"LinkedIn copy","meme_url":"(filled by render)"}
  ]
}
```

**Two hard rules (verified with the user):**
- **Never reference the source paper anywhere the user sees** — not in the explainer's rendered fields, the captions, or the post. Teach the idea in your own words + a coined plain name. Keep the real paper only in the private `paper` field on disk.
- **LinkedIn post craft**: hook < ~10 words in line 1 (before the ~140-210 char fold); white space (1-3 sentence paragraphs, single-line sentences, blank lines); shape = hook → payoff → substance (manual `→` bullets) → a closing question; ≤1 emoji, no hashtag spam; ~600-1,300 chars. Hook types that work: contrarian, specific number, pain-point, unexpected comparison.

## 4a. Render via Imgflip API (default) — UA header is REQUIRED

Python `urllib` gets HTTP 403 from Imgflip without a `User-Agent`; plain `curl` doesn't. Needed on the POST *and* when downloading `meme_url`.

```bash
python3 - <<'PY'
import json, os, urllib.parse, urllib.request
data=json.load(open("options.json")); opts=data["options"] if isinstance(data,dict) else data
for o in opts:
    boxes={f"boxes[{j}][text]":c for j,c in enumerate(o["captions"])}
    payload={"template_id":o["template_id"],"username":os.environ["IMGFLIP_USERNAME"],
             "password":os.environ["IMGFLIP_PASSWORD"], **boxes}
    req=urllib.request.Request("https://api.imgflip.com/caption_image",
        data=urllib.parse.urlencode(payload).encode(), headers={"User-Agent":"Mozilla/5.0"})
    r=json.loads(urllib.request.urlopen(req).read())
    o["meme_url"]=r["data"]["url"] if r["success"] else None
    print(o["id"], o.get("meme_url") or r.get("error_message"))
json.dump(data, open("options.json","w"), indent=2)
PY
```
Free tier: adds a small watermark, returns 500×500. `no_watermark` is Premium ($0.01/creation after 100/mo).

## 4b. Render via local Pillow (fallback, no account, watermark-free, 1200×1200)

Needs a per-template text-region map. Verified Drake layout (right half of each of the two panels), Impact font at `/System/Library/Fonts/Supplemental/Impact.ttf`:

```bash
python3 - <<'PY'
from PIL import Image, ImageDraw, ImageFont
import json, urllib.request
FONT="/System/Library/Fonts/Supplemental/Impact.ttf"
data=json.load(open("options.json")); o=(data["options"] if isinstance(data,dict) else data)[0]
tpl={t['id']:t for t in json.load(open('bank/templates.json'))}[o['template_id']]
urllib.request.urlretrieve(tpl['url'],"template.img")
img=Image.open("template.img").convert("RGB"); W,H=img.size; d=ImageDraw.Draw(img)
def wrap(t,f,mw):
    ws,ls,cur=t.split(),[],""
    for w in ws:
        s=(cur+" "+w).strip()
        if d.textlength(s,font=f)<=mw: cur=s
        else: ls.append(cur); cur=w
    if cur: ls.append(cur)
    return ls
def block(t,box):
    x0,y0,x1,y1=box; mw=x1-x0; sz=64
    while sz>20:
        f=ImageFont.truetype(FONT,sz); ls=wrap(t,f,mw)
        if sz*1.15*len(ls)<=(y1-y0): break
        sz-=2
    f=ImageFont.truetype(FONT,sz); lh=sz*1.15; y=y0+((y1-y0)-lh*len(ls))/2
    for ln in ls:
        x=x0+(mw-d.textlength(ln,font=f))/2
        d.text((x,y),ln,font=f,fill="white",stroke_width=max(2,sz//18),stroke_fill="black"); y+=lh
block(o["captions"][0],(int(W*0.52),40,W-40,H//2-40))
block(o["captions"][1],(int(W*0.52),H//2+40,W-40,H-40))
img.save("meme.png"); print("saved meme.png",img.size)
PY
```

## 5. Launch the UI + watch for the select

```bash
cd /tmp/meme-run && rm -f action.json
python3 /path/to/skills/research-to-linkedin-memes/scripts/review_server.py 8765 >srv.log 2>&1 &
sleep 1 && open http://localhost:8765/
# looping watcher (catches EVERY click, not one-shot):
cd /tmp/meme-run; while true; do until [ -f action.json ]; do sleep 1; done; echo "$(cat action.json)"; rm -f action.json; done
```
Select saves `output/<ts>/` with `meme.jpg` + `post.txt` + `selection.json` + `explainer.json`.
Regenerate = say "regenerate" in chat; agent rewrites `options.json`; page auto-refreshes (polls it).

## 6. UI design values (verified)

- Button contrast: white on `#3b82f6` = 3.7:1 (fails AA). Use `#2563eb` = **5.17:1 (passes)**, hover `#1d4ed8` = 6.7:1. Compute with the WCAG relative-luminance formula, don't eyeball.
- Keep text containers ≤ ~64–78ch; adaptive `grid-template-columns:repeat(auto-fit,minmax(320px,1fr))`.

## 7. Cleanup

```bash
lsof -ti tcp:8765 | xargs kill 2>/dev/null          # stop the server (one port at a time; multi-port lsof errors)
cd <main repo> && git worktree remove <path> --force # remove a worktree
git checkout main -q && git pull --rebase origin main -q
```

## Context worth keeping

- **Agent-in-the-loop, no API key**: the whole generate/regenerate loop runs with the driving agent as the model; the file relay (`options.json` out, `action.json` in) is the only glue. A standalone version would swap in an `ANTHROPIC_API_KEY` backend + the openalex CLI.
- **Recursion cap**: taxonomy tree at depth 2, ~3-5 nodes/level; stop a branch when nodes stop adding a *distinct* angle. Same saturation rule as any recursive research loop.
- **Voice**: say-it-plain + deslop + `WRITING-GUIDE.md` for everything — replies, explainer, captions, post copy.
- **Public repo hygiene**: run in a scratch dir; the skill's `.gitignore` covers `options.json`/`action.json`/`output/`/`bank/`/pycache; never commit generated memes or an Imgflip password.
