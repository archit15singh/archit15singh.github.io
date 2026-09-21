"""Local review UI for meme-post-generator (agent-in-the-loop).

Serves a page showing a plain-language explainer of the concept (analogy, how-it-
works steps, examples, an ASCII visual -- deliberately NOT citing the source paper)
plus the current option batch (read from options.json) and lets the human edit copy and
Select one (final). options.json is either a bare options array (legacy) or the v2
shape {"explainer": {...}, "options": [...]}; the explainer panel renders when
present. There is no in-page "generate more":
to get a different batch the user asks the driving Claude agent to "regenerate" in
chat; the agent writes a fresh options.json and the page auto-refreshes to it
(it polls options.json and swaps in any new batch).

The Select action is written to action.json, which the agent watches:
  {"type":"select","id":"B","post":"..."}  -> agent confirms the saved final

On Select the server also saves the chosen meme image + post text into a dated
a descriptively-named .png (+ matching .txt) in ~/linkedin-memes/ so you have durable, searchable files to upload and paste.

Run from a working dir that contains options.json:
  IMGFLIP_* not needed here (rendering happens agent-side); this only serves + saves.
  python3 review_server.py [port]
"""
import io, json, os, re, sys, urllib.request
from http.server import BaseHTTPRequestHandler, HTTPServer

HERE = os.getcwd()                       # options.json / action.json / output live here
PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8765

PAGE = """<!doctype html><html><head><meta charset=utf-8>
<title>Meme post review</title>
<style>
 :root{--bg:#0f1115;--panel:#171a21;--panel2:#1e222b;--line:#2a2e37;--ink:#e8eaed;--muted:#9aa0a6;
   --accent:#2563eb;--accent-h:#1d4ed8;--ok:#132b16;--ok-line:#1f5127;--ok-ink:#b6efc0;--shadow:0 1px 2px rgba(0,0,0,.4),0 8px 24px rgba(0,0,0,.28)}
 *{box-sizing:border-box}
 body{font-family:-apple-system,Segoe UI,Roboto,sans-serif;background:radial-gradient(120% 90% at 50% -10%,#151926 0%,var(--bg) 55%);
   color:var(--ink);margin:0;padding:40px 24px;line-height:1.5;-webkit-font-smoothing:antialiased}
 .wrap{max-width:1120px;margin:0 auto}
 header{max-width:64ch;margin:0 auto 28px;text-align:center}
 h1{font-size:26px;font-weight:700;letter-spacing:-.01em;margin:0 0 6px}
 .sub{color:var(--muted);margin:0;font-size:14px}
 .grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(320px,1fr));gap:20px;align-items:start}
 .card{background:var(--panel);border:1px solid var(--line);border-radius:16px;padding:14px;display:flex;flex-direction:column;
   box-shadow:var(--shadow);transition:transform .15s ease,border-color .15s ease}
 .card:hover{transform:translateY(-3px);border-color:#39414f}
 .card img{width:100%;border-radius:10px;background:#000;display:block}
 .tpl{font-size:11px;font-weight:600;letter-spacing:.06em;text-transform:uppercase;color:var(--muted);margin:12px 2px 6px}
 textarea{width:100%;background:var(--bg);color:var(--ink);border:1px solid var(--line);border-radius:10px;padding:11px;
   font:inherit;font-size:13.5px;line-height:1.45;resize:vertical}
 textarea:focus-visible{outline:2px solid var(--accent);outline-offset:1px;border-color:transparent}
 .post{height:132px}
 .btn{margin-top:12px;padding:11px 16px;border:0;border-radius:10px;font-weight:600;font-size:14px;cursor:pointer;transition:background .12s ease}
 .btn:focus-visible{outline:2px solid var(--accent-h);outline-offset:2px}
 .sel{background:var(--accent);color:#fff} .sel:hover{background:var(--accent-h)}
 .done{display:none;background:var(--ok);border:1px solid var(--ok-line);color:var(--ok-ink);padding:16px 18px;border-radius:12px;margin:20px auto 0;max-width:64ch;font-size:14px}
 code{background:var(--bg);border:1px solid var(--line);padding:2px 7px;border-radius:6px;font-size:12.5px}
 .explain{background:var(--panel);border:1px solid var(--line);border-radius:16px;padding:22px 24px;margin:0 auto 28px;max-width:80ch;box-shadow:var(--shadow)}
 .explain h2{font-size:19px;font-weight:700;margin:0 0 6px;letter-spacing:-.01em}
 .explain .hook{font-size:15px;color:var(--accent-h);font-weight:600;margin:0 0 12px}
 .explain p{margin:0 0 14px;font-size:14.5px;line-height:1.65;color:#d7dade}
 .explain .lbl{font-size:11px;font-weight:700;letter-spacing:.06em;text-transform:uppercase;color:var(--muted);margin:16px 0 6px}
 .explain .analogy{background:var(--bg);border:1px solid var(--line);border-left:3px solid #8b5cf6;border-radius:8px;padding:12px 14px;margin:0 0 6px;font-style:italic;color:#e2e4e8}
 .explain ol{margin:0 0 6px;padding-left:20px} .explain ol li{margin:0 0 6px;font-size:14px;line-height:1.55}
 .explain ul.eg{list-style:none;margin:0;padding:0}
 .explain ul.eg li{background:var(--bg);border:1px solid var(--line);border-left:3px solid var(--accent);border-radius:8px;padding:10px 13px;margin:0 0 8px;font-size:13.5px;line-height:1.5}
 .explain pre{background:#0b0d12;border:1px solid var(--line);border-radius:8px;padding:14px;overflow:auto;font-size:12.5px;line-height:1.4;color:#cfe3ff;margin:0 0 6px}
 .chips{display:flex;flex-wrap:wrap;gap:7px} .chip{font-size:12px;background:var(--panel2);border:1px solid #3a4a5f;color:#cdd3da;border-radius:999px;padding:4px 11px}
</style></head><body>
<div class=wrap>
<header>
 <h1>Learn it, then meme it</h1>
 <p class=sub>Read the concept below, then pick the meme + post that lands it best. Edit any copy, then Select to finalize. Want a different batch? Tell the agent "regenerate" -- this page updates on its own.</p>
</header>
<div class=explain id=explain style=display:none></div>
<div class=grid id=grid></div>
<div class=done id=done></div>
</div>
<script>
let OPTS=[];
// options.json is either a bare array (legacy) or {explainer, options} (v2).
function esc(s){return (s||'').replace(/[&<>]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;'}[c]))}
function ingest(data){
 if(Array.isArray(data)){OPTS=data; return null;}
 OPTS=data.options||[]; return data.explainer||null;
}
function renderExplain(e){
 if(!e){explain.style.display='none'; return;}
 // No source-paper reference is rendered on purpose (see SKILL.md): the idea is
 // taught in plain words, not cited.
 const steps=(e.how_it_works||[]).map(s=>`<li>${esc(s)}</li>`).join('');
 const egs=(e.examples||[]).map(x=>`<li>${esc(x)}</li>`).join('');
 const chips=(e.taxonomy||[]).map(t=>`<span class=chip>${esc(t)}</span>`).join('');
 explain.innerHTML = `
  <h2>${esc(e.concept||'The idea')}</h2>
  ${e.hook?`<div class=hook>${esc(e.hook)}</div>`:''}
  <p>${esc(e.plain||'')}</p>
  ${e.analogy?`<div class=lbl>Picture it</div><div class=analogy>${esc(e.analogy)}</div>`:''}
  ${steps?`<div class=lbl>How it works</div><ol>${steps}</ol>`:''}
  ${e.visual?`<div class=lbl>The shape of it</div><pre>${esc(e.visual)}</pre>`:''}
  ${egs?`<div class=lbl>Examples</div><ul class=eg>${egs}</ul>`:''}
  ${chips?`<div class=lbl>Angles we explored</div><div class=chips>${chips}</div>`:''}`;
 explain.style.display='block';
}
function render(){
 grid.innerHTML='';
 OPTS.forEach(o=>{
  const c=document.createElement('div');c.className='card';
  c.innerHTML=`<img src="${o.meme_url}"><div class=tpl>${esc(o.template)}</div>
   <textarea class=post id="p_${o.id}">${esc(o.post)}</textarea>
   <button class="btn sel" onclick="pick('${o.id}')">Select this</button>`;
  grid.appendChild(c);
 });
}
async function load(){renderExplain(ingest(await (await fetch('/options.json?_='+Date.now())).json()));render()}
async function pick(id){
 const post=document.getElementById('p_'+id).value;
 const r=await (await fetch('/action',{method:'POST',headers:{'Content-Type':'application/json'},
   body:JSON.stringify({type:'select',id,post})})).json();
 const o=OPTS.find(x=>x.id===id);
 done.style.display='block';
 done.innerHTML=`<b>Selected option ${id} (${esc(o.template)}).</b> Saved to <code>${esc(r.path||'~/linkedin-memes/')}</code>. Upload the image and paste the copy into LinkedIn. You can close this tab.`;
 window.scrollTo(0,document.body.scrollHeight);
}
// Auto-refresh: when the agent writes a fresh options.json (you asked it to
// "regenerate"), swap the new batch (and explainer) in without a manual reload.
let seen=null;
async function poll(){
 const data=await (await fetch('/options.json?_='+Date.now())).json();
 const e=ingest(data); const sig=JSON.stringify(OPTS.map(x=>x.meme_url));
 if(seen && sig!==seen){done.style.display='none';renderExplain(e);render()}
 seen=sig; setTimeout(poll,1500);
}
load().then(()=>{seen=JSON.stringify(OPTS.map(x=>x.meme_url));poll()});
</script></body></html>"""


SAVE_ROOT = os.path.join(os.path.expanduser("~"), "linkedin-memes")


def _safe_name(text, maxlen=120):
    """Make an agent-authored title safe for a filename WITHOUT rewriting its meaning:
    drop filesystem-unsafe characters, collapse whitespace to hyphens, cap length."""
    s = re.sub(r"[^\w\s-]", "", (text or "")).strip()
    s = re.sub(r"[\s_-]+", "-", s)
    return s[:maxlen].strip("-") or "meme"


def save_selection(action):
    """Save the selected meme as one descriptively-named .png in ~/linkedin-memes/
    (searchable by title alone), with the post copy as a matching .txt sidecar. The
    title is the agent-authored `filename` on the option; the code only sanitizes it."""
    data = json.load(open(os.path.join(HERE, "options.json")))
    # v2 schema is {explainer, options}; legacy is a bare options array.
    opts = data["options"] if isinstance(data, dict) else data
    explainer = data.get("explainer") if isinstance(data, dict) else None
    chosen = next((o for o in opts if o["id"] == action["id"]), None)
    if not chosen:
        return {"ok": False, "error": "unknown option id"}
    os.makedirs(SAVE_ROOT, exist_ok=True)
    # Prefer the agent's own elaborate title; fall back to concept/post only if absent.
    title = chosen.get("filename") or (explainer or {}).get("concept") \
        or action.get("post") or chosen.get("post") or " ".join(chosen.get("captions", []))
    base = _safe_name(title)
    name, n = base, 2
    while os.path.exists(os.path.join(SAVE_ROOT, name + ".png")):  # don't clobber an earlier pick
        name, n = f"{base}-{n}", n + 1
    png_path = os.path.join(SAVE_ROOT, name + ".png")
    if chosen.get("meme_url"):
        req = urllib.request.Request(chosen["meme_url"], headers={"User-Agent": "Mozilla/5.0"})
        raw = urllib.request.urlopen(req).read()
        try:  # honor .png even though Imgflip serves jpg
            from PIL import Image
            Image.open(io.BytesIO(raw)).convert("RGB").save(png_path, "PNG")
        except Exception:
            open(png_path, "wb").write(raw)  # fall back to raw bytes under the .png name
    open(os.path.join(SAVE_ROOT, name + ".txt"), "w").write(action.get("post", chosen.get("post", "")))
    return {"ok": True, "path": png_path}


class H(BaseHTTPRequestHandler):
    def log_message(self, *a):
        pass

    def _send(self, code, body, ctype="application/json"):
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.end_headers()
        self.wfile.write(body if isinstance(body, bytes) else body.encode())

    def do_GET(self):
        if self.path.startswith("/options.json"):
            self._send(200, open(os.path.join(HERE, "options.json"), "rb").read())
        else:
            self._send(200, PAGE, "text/html")

    def do_POST(self):
        n = int(self.headers.get("Content-Length", 0))
        action = json.loads(self.rfile.read(n).decode())
        open(os.path.join(HERE, "action.json"), "w").write(json.dumps(action))
        result = save_selection(action) if action.get("type") == "select" else {"ok": True}
        self._send(200, json.dumps(result))


if __name__ == "__main__":
    print(f"serving http://localhost:{PORT}/  (cwd={HERE})")
    HTTPServer(("127.0.0.1", PORT), H).serve_forever()
