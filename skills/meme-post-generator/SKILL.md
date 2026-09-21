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
- **Rendering**: Imgflip `caption_image` API (needs a free Imgflip account).
- **Publish path**: no LinkedIn API. Show the post text (copy button) + the meme (download); the human pastes into LinkedIn and uses LinkedIn's own preview before it goes live.
- **Input**: paste a blog URL; the tool fetches and extracts the main text.
- **Stack (when the tool is built)**: local Python backend + a small web UI, run on the laptop. Claude API for matching, captions, and post copy. No hosting, no auth.

## Prerequisites

```bash
export ANTHROPIC_API_KEY=...          # Claude API
export IMGFLIP_USERNAME=...           # free account at imgflip.com/signup
export IMGFLIP_PASSWORD=...
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

### 5. Render each option with Imgflip

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

`caption_image` needs `template_id` + one `boxes[n][text]` per slot. On multi-box templates prefer the `boxes[]` form over the legacy `text0/text1`.

### 6. Review + paste (the approval gate)

Present the 3 rendered options (meme URL + LinkedIn copy) to the human. They pick one, tweak the wording, download the image, and paste both into LinkedIn — where LinkedIn's native composer gives a final preview before publish. **The tool never publishes.**

LinkedIn renders in-feed images best at **1080×1080 (square)**; templates vary wildly in aspect ratio, so pad/center the rendered meme onto a square canvas before download if it looks cramped in the feed.

## Why the free path, and the paid alternatives

Imgflip has its own AI endpoints that would collapse steps 2, 4, and 5 into one call — but each needs a **Premium account and costs per call**, so we deliberately don't use them:

- `ai_meme` — Imgflip writes the whole meme from a prompt ($0.02/creation after 50/mo, Premium).
- `automeme` — turns freeform text into a meme, auto-picking a template ($0.02/creation, Premium).
- `search_memes` — search 1M+ templates beyond the free top-100 ($0.005/search after 200/mo, Premium).

Our path (free `get_memes` top-100 + Claude for matching/captions/post copy) gives more taste control at ~$0 of Imgflip spend. Reach for the paid endpoints only if the top-100 bank stops being enough.

## When you build the actual tool

The web UI wraps steps 3-6: one URL field, a "generate" button, three cards (meme + editable post text + copy/download), no login. Steps 1-2 are a one-time setup script. Keep it local; there is nothing here that needs hosting or auth.

## Gotchas

- `box_count` mismatch is the #1 failure — Imgflip silently mis-renders if you send the wrong number of boxes. `box_count` is the template's *default* slot count (some accept more); emit exactly `box_count` captions as the safe default and validate that length before calling `caption_image`.
- The regex HTML extractor in step 3 is a placeholder; real posts need `trafilatura` or a readability lib or the meme captions get polluted by nav text.
- Free Imgflip accounts keep a minimal watermark; `no_watermark` needs Premium and costs $0.01/creation after 100/month. The free `caption_image` render itself is fine for personal use.
- Meme taste is the thing most likely to be wrong — that is exactly why this generates options and gates on a human, never auto-posts.
