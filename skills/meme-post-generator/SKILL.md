---
name: meme-post-generator
description: Turn a blog post into a meme + a LinkedIn post, drafted for human approval. Given a blog URL, it fetches the text, matches it to a template from a curated Imgflip-seeded bank, writes the caption + the LinkedIn copy, renders the meme, and hands back options for you to review and paste. Use when the user says "make a meme post", "meme this blog post", "turn this post into a LinkedIn meme", or hands over a blog URL and wants a meme + post drafted.
---

# meme-post-generator

Turn one blog post into a meme and a LinkedIn post you can approve and paste. Personal, single-user. **Nothing auto-posts.** The tool drafts several options; a human picks, edits, and pastes into LinkedIn.

## The decisions this bakes in

These were settled up front — do not re-litigate them, just follow:

- **Audience**: you, so you ship LinkedIn posts more often. Not a SaaS, no accounts, no billing.
- **Human in the loop**: AI generates several options; you review and approve. Never auto-post.
- **Template bank**: curated, seeded from Imgflip's top 100. Each template carries a written "use when…" fit-note plus its `box_count` (how many text slots). The AI matches a post against those notes, not raw names.
- **Rendering**: the **interactive tool defaults to the Imgflip `caption_image` API** — it auto-places text into each template's boxes, so any template in the bank renders correctly with no per-template layout code. Needs a free account (env creds) and, on the Free tier, adds a small watermark + returns 500×500. Local Pillow is the fallback (no account, watermark-free, 1200×1200) but needs a hand-built text-region map per template, so it does not scale across the bank on its own.
- **Publish path**: no LinkedIn API. Show the post text (copy button) + the meme (download); the human pastes into LinkedIn and uses LinkedIn's own preview before it goes live.
- **Input**: paste a blog URL; the tool fetches and extracts the main text.
- **Stack (when the tool is built)**: local Python backend + a small web UI, run on the laptop. Claude API for matching, captions, and post copy. No hosting, no auth.

## Fastest path (verified, zero keys)

Ran end-to-end on `content/posts/2026-03-23-hard-constraints-belong-in-code.md` — matched **Drake Hotline Bling**, wrote captions, rendered a real meme. What made it one-shot:

- **When a Claude agent (e.g. Claude Code) is running this, you need NO `ANTHROPIC_API_KEY`.** The agent *is* the model — it does step 2 (fit-notes) and step 4 (match + captions + LinkedIn copy) directly in-conversation. The `anthropic`-SDK scripts in steps 2/4 are only for the standalone/built-tool case.
- **Rendering**: the interactive tool renders via the Imgflip API (reliable across any template). If you have no account, the local Pillow render (step 5) is the zero-key, watermark-free fallback — but it only handles templates you've written a region map for.

So the minimal run is: seed bank once (step 1) → agent picks template + writes captions/copy (steps 3-4, in-conversation) → render (Imgflip API, or local Pillow fallback) → review in the browser UI and select one (ask the agent to "regenerate" in chat for a fresh batch; see Interactive review UI). Generation needs no `ANTHROPIC_API_KEY` when an agent drives it; Imgflip rendering needs the env creds.

## Prerequisites

Nothing required when a Claude agent drives it and you render locally. Optional, only for the standalone tool or the Imgflip API render:

```bash
export ANTHROPIC_API_KEY=...          # only for the standalone (non-agent) match/caption scripts
export IMGFLIP_USERNAME=...           # only for the Imgflip API render; free account at imgflip.com/signup
export IMGFLIP_PASSWORD=...           # NEVER paste this into a chat — set it in the shell
```

Model: default to the latest capable Claude (e.g. `claude-opus-4-8` for the taste-heavy match/caption step; a cheaper Sonnet is fine for bulk fit-note writing).

## Workflow

### 1. Seed the template bank (one time)

Download Imgflip's top 100 templates with metadata (name, image URL, dimensions, `box_count`):

```bash
mkdir -p bank/images
curl -s "https://api.imgflip.com/get_memes" \
  | python3 -c "import sys,json; json.dump(json.load(sys.stdin)['data']['memes'], open('bank/templates.json','w'), indent=2)"

# pull the images
python3 - <<'PY'
import json, urllib.request, os
for m in json.load(open('bank/templates.json')):
    ext = m['url'].split('.')[-1]
    urllib.request.urlretrieve(m['url'], f"bank/images/{m['id']}.{ext}")
print("downloaded", len(json.load(open('bank/templates.json'))), "templates")
PY
```

Each entry looks like: `{"id":"181913649","name":"Drake Hotline Bling","box_count":2,...}`. `box_count` is the number of text boxes you must fill (Drake=2, Two Buttons=3, Gru's Plan=4). **The caption generator must emit exactly `box_count` strings.**

### 2. Write a fit-note per template (one time)

Ask Claude, once, to write a short "use when…" note for each template so matching is by meaning, not by name. Keep it to one line each.

```bash
python3 - <<'PY'
import json, anthropic
tpls = json.load(open('bank/templates.json'))
names = "\n".join(f"- {t['name']} (boxes={t['box_count']})" for t in tpls)
msg = anthropic.Anthropic().messages.create(
    model="claude-sonnet-5", max_tokens=4000,
    messages=[{"role":"user","content":
        "For each meme template below, write ONE line: 'Name => use when <the single situation this format nails>'. "
        "Be concrete about the rhetorical move (contrast, escalation, hard tradeoff, inevitability, etc.).\n\n"+names}])
open('bank/fit_notes.txt','w').write(msg.content[0].text)
print(msg.content[0].text[:500])
PY
```

Store the notes next to `templates.json`. Prune templates you would never post; the bank is yours to curate over time.

### 3. Fetch + extract the blog post

```bash
python3 - <<'PY'
import sys, urllib.request, re
url = sys.argv[1]
html = urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent":"Mozilla/5.0"})).read().decode("utf-8","ignore")
# minimal extraction; swap in trafilatura/readability for production
text = re.sub(r"<[^>]+>"," ", re.sub(r"(?is)<(script|style|nav|header|footer).*?</\1>"," ", html))
text = re.sub(r"\s+"," ", text).strip()
open("post.txt","w").write(text)
print(text[:600])
PY
```
Call with the URL as `$1`. For paywalled/draft posts, skip this and paste the body into `post.txt` directly.

### 4. Match + caption + write the LinkedIn post

One Claude call: give it the post text + the fit-notes, ask for **several** options (matching the "generate options, human picks" decision). Force it to pick a real template id and emit exactly `box_count` captions.

```bash
python3 - <<'PY'
import json, anthropic
post = open("post.txt").read()[:8000]
notes = open("bank/fit_notes.txt").read()
tpls = {t['name']:t for t in json.load(open('bank/templates.json'))}
prompt = f"""You draft LinkedIn meme posts for a single user. Read the blog post, then propose THREE options.
For each option return JSON: {{"template_name","captions":[...],"linkedin_post"}}.
- template_name MUST be one from the fit-notes list.
- captions MUST have exactly as many entries as that template's box_count.
- linkedin_post: 2-4 short lines, a hook + why the post matters + a soft CTA. No hashtag spam, no emojis unless they land.
Return a JSON array of 3 options, nothing else.
The linkedin_post copy MUST clear this repo's writing bar (see Writing the post copy below).

FIT NOTES:
{notes}

BLOG POST:
{post}"""
msg = anthropic.Anthropic().messages.create(model="claude-opus-4-8", max_tokens=2000,
    messages=[{"role":"user","content":prompt}])
opts = json.loads(msg.content[0].text)
for o in opts:
    o['template_id'] = tpls[o['template_name']]['id']
json.dump(opts, open("options.json","w"), indent=2)
print(json.dumps(opts, indent=2)[:800])
PY
```

### 4b. Writing the post copy (quality bar)

The `linkedin_post` on every option is real published writing under your name, so hold it to the repo's editorial standard, not generic LLM voice:

- **`WRITING-GUIDE.md`** (repo root) is the source of truth — specific over vague, a real voice with "I"/"we", one surprising sentence, direct not hedged, and the Tier-1 banned-word list. The copy must pass it.
- **Run `/deslop`** over each drafted post before it reaches the UI — strip AI tells, filler, and the banned words. When an agent is driving the loop, invoke the `deslop` skill on the copy; don't just eyeball it.
- **Borrow `/pr-writeup`'s framing**: lead with the outcome/idea the blog post delivers to the reader, not a description of the post ("I wrote about X"). Hook first, the payoff, then a soft nudge to read.

Net: the meme carries the joke; the copy earns the click and reads like you wrote it.

### 5. Render (default: local Pillow, no account, no watermark)

This is the verified path. Download the chosen template image, draw the captions with the Impact font, auto-fit each caption to its region. The example below is the **Drake** layout that shipped (two stacked panels, text on the right half of each); other templates need their own box regions — see the note after.

```bash
python3 - <<'PY'
from PIL import Image, ImageDraw, ImageFont
import json, urllib.request
FONT = "/System/Library/Fonts/Supplemental/Impact.ttf"   # macOS; any bold TTF works

opts = json.load(open("options.json"))
o = opts[0]                                              # the human's pick
tpl = {t['id']:t for t in json.load(open('bank/templates.json'))}[o['template_id']]
urllib.request.urlretrieve(tpl['url'], "template.img")
img = Image.open("template.img").convert("RGB"); W,H = img.size
d = ImageDraw.Draw(img)

def wrap(text, font, maxw):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t=(cur+" "+w).strip()
        if d.textlength(t, font=font)<=maxw: cur=t
        else: lines.append(cur); cur=w
    if cur: lines.append(cur)
    return lines

def draw_block(text, box):                               # auto-shrink to fit the region
    x0,y0,x1,y1 = box; maxw=x1-x0; size=64
    while size>20:
        font=ImageFont.truetype(FONT,size); lines=wrap(text,font,maxw)
        if size*1.15*len(lines) <= (y1-y0): break
        size-=2
    font=ImageFont.truetype(FONT,size); lh=size*1.15
    y=y0+((y1-y0)-lh*len(lines))/2
    for ln in lines:
        x=x0+(maxw-d.textlength(ln,font=font))/2
        d.text((x,y),ln,font=font,fill="white",stroke_width=max(2,size//18),stroke_fill="black")
        y+=lh

# Drake regions: right half of the top and bottom panels
draw_block(o["captions"][0], (int(W*0.52),40,W-40,H//2-40))
draw_block(o["captions"][1], (int(W*0.52),H//2+40,W-40,H-40))
img.save("meme.png"); print("saved meme.png", img.size)
PY
```

**Per-template box regions**: text placement is template-specific and is the one thing this step can get wrong. Drake = right half of each panel (above). Two Buttons = the two button labels + the sweating figure. Distracted Boyfriend = three people. Store a small region map per template you actually use, or eyeball the downloaded image once and hardcode the boxes. This is exactly why step 6 gates on a human looking at the result.

### 5 (alternative). Render with the Imgflip API

Only if you want Imgflip's own placement and accept the Free-tier watermark + 500×500 output. Needs the env vars from Prerequisites — **never inline a password**.

```bash
python3 - <<'PY'
import json, os, urllib.parse, urllib.request
opts = json.load(open("options.json"))
for i,o in enumerate(opts):
    boxes = {f"boxes[{j}][text]":c for j,c in enumerate(o["captions"])}
    data = {"template_id":o["template_id"],"username":os.environ["IMGFLIP_USERNAME"],
            "password":os.environ["IMGFLIP_PASSWORD"], **boxes}
    r = json.loads(urllib.request.urlopen("https://api.imgflip.com/caption_image",
        data=urllib.parse.urlencode(data).encode()).read())
    o["meme_url"] = r["data"]["url"] if r["success"] else None
    print(i, o.get("meme_url") or r.get("error_message"))
json.dump(opts, open("options.json","w"), indent=2)
PY
```

`caption_image` needs `template_id` + one `boxes[n][text]` per slot; it auto-places text in each template's default boxes (why it needs no region map). On multi-box templates prefer the `boxes[]` form over the legacy `text0/text1`.

### 6. Review + paste (the approval gate)

Present the 3 rendered options (meme URL + LinkedIn copy) to the human. They pick one, tweak the wording, download the image, and paste both into LinkedIn — where LinkedIn's native composer gives a final preview before publish. **The tool never publishes.**

LinkedIn renders in-feed images best at **1080×1080 (square)**; templates vary wildly in aspect ratio, so pad/center the rendered meme onto a square canvas before download if it looks cramped in the feed.

## Why the free path, and the paid alternatives

Imgflip has its own AI endpoints that would collapse steps 2, 4, and 5 into one call — but each needs a **Premium account and costs per call**, so we deliberately don't use them:

- `ai_meme` — Imgflip writes the whole meme from a prompt ($0.02/creation after 50/mo, Premium).
- `automeme` — turns freeform text into a meme, auto-picking a template ($0.02/creation, Premium).
- `search_memes` — search 1M+ templates beyond the free top-100 ($0.005/search after 200/mo, Premium).

Our path (free `get_memes` top-100 + Claude for matching/captions/post copy) gives more taste control at ~$0 of Imgflip spend. Reach for the paid endpoints only if the top-100 bank stops being enough.

## Interactive review UI (the built tool)

This is the actual review loop, verified end-to-end (a blog URL → 3 rendered options → browser select). It is **agent-in-the-loop**: the Claude agent generates and renders; a tiny local server (`scripts/review_server.py`) shows the batch in the browser and relays your click back to the agent through a watched file. No API key for generation; Imgflip env creds only for rendering.

**How to run it** (agent does all of this):

1. **Get the input** — you hand the agent a blog URL (it fetches + extracts, step 3) or paste raw text. The agent does NOT need an in-page input box; input arrives at invocation.
2. **Generate the first batch** — the agent (as the model) writes 3 options: `{"id","template","template_id","captions":[...],"post"}`. Render each (Imgflip API default; see step 5), attach `meme_url`, and write the array to `options.json` in a scratch run dir (e.g. `/tmp/meme-run/`), **never the repo**.
3. **Launch the UI** — from that run dir:
   ```bash
   cd /tmp/meme-run && python3 /path/to/skills/meme-post-generator/scripts/review_server.py
   open http://localhost:8765/
   ```
4. **Watch for the selection** — the agent uses a looping monitor so it catches the click (not a one-shot wait):
   ```bash
   cd <run dir>; while true; do until [ -f action.json ]; do sleep 1; done; echo "$(cat action.json)"; rm -f action.json; done
   ```
5. **Handle the selection** — `{"type":"select","id":"B","post":"..."}` → **final**. The server has already saved the chosen meme image + post text into `output/<timestamp>/`; tell the user the path. Done.

**Regeneration is a chat request, not a UI control.** There is no "generate more" button. To get a different batch, the user simply tells the agent **"regenerate"** in chat (optionally with a steer, e.g. "funnier, lean into the safety angle"). The agent writes a fresh `options.json` (replace, not append) to the run dir and the open page **auto-refreshes** to it — the page polls `options.json` and swaps in any new batch. A bare "regenerate" with no steer means the agent picks its own short creative direction (e.g. *"try unexpected templates"*, *"go absurd and meme-native"*, *"punchier, fewer words"*). Because the human drives each round from chat, there is no runaway self-steering tree and no round cap to enforce.

**Files (all in the run dir, all gitignored):** `options.json` (current batch, agent→UI, page polls it for refresh), `action.json` (the select, UI→agent), `output/<ts>/` (final meme + `post.txt` + `selection.json`). The skill ships a `.gitignore` so none of these land in the repo even if the run dir is inside it.

## When you build a fuller standalone version

To run without an agent watching, add a backend that calls Claude directly to generate the batch (needs `ANTHROPIC_API_KEY`) — including a regenerate control back in the page if you want it self-service — and keep the same `review_server.py` page. Everything else — bank, matching prompt, Imgflip render, output folder — is unchanged. Keep it local; nothing here needs hosting or auth.

## Gotchas

- `box_count` mismatch is the #1 failure — Imgflip silently mis-renders if you send the wrong number of boxes. `box_count` is the template's *default* slot count (some accept more); emit exactly `box_count` captions as the safe default and validate that length before calling `caption_image`.
- The regex HTML extractor in step 3 is a placeholder; real posts need `trafilatura` or a readability lib or the meme captions get polluted by nav text.
- Free Imgflip accounts keep a minimal watermark AND downsize the result to 500×500; `no_watermark` needs Premium ($0.01/creation after 100/month). The local Pillow render avoids both — prefer it for the file you actually post.
- **Text placement is per-template.** The local render must know each template's box regions (Drake = right half of each panel). Get it from the downloaded image once; a wrong region is the most likely visible defect. The Imgflip API sidesteps this by auto-placing into default boxes.
- macOS ships Impact at `/System/Library/Fonts/Supplemental/Impact.ttf` (the classic meme font). Any bold TTF works if Impact is absent.
- **Never paste an Imgflip password into a chat.** Set it as a shell env var. If one leaks, rotate it. (Free meme account = low stakes, but the habit matters.)
- **Imgflip `caption_image` returns HTTP 403 to Python `urllib`'s default user-agent.** Plain `curl` works, but `urllib.request` is blocked until you set a header: `Request(url, data=..., headers={"User-Agent":"Mozilla/5.0"})`. Same header is needed when downloading the rendered `meme_url`. Found the hard way — a 403 here is the UA, not bad creds.
- **Run the UI in a scratch dir, never the repo.** `options.json`/`action.json`/`output/` are generated at runtime; the shipped `.gitignore` covers them, but keeping the run dir out of the repo (e.g. `/tmp/meme-run/`) avoids any chance of committing generated images to a public repo.
- Meme taste is the thing most likely to be wrong — that is exactly why this generates options and gates on a human, never auto-posts.
