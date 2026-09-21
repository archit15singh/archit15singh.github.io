"""Local review UI for meme-post-generator (agent-in-the-loop).

Serves a page showing the current option batch (read from options.json), lets the
human edit copy and either Select one (final) or type a steer and Generate more.

Actions are written to action.json, which the driving Claude agent watches:
  {"type":"select","id":"B","post":"..."}      -> agent renders/saves the final
  {"type":"regenerate","prompt":"funnier..."}  -> agent writes a fresh options.json

On Select the server also saves the chosen meme image + post text into a dated
output/ folder so you have durable files to upload and paste.

Run from a working dir that contains options.json:
  IMGFLIP_* not needed here (rendering happens agent-side); this only serves + saves.
  python3 review_server.py [port]
"""
import json, os, sys, time, urllib.request
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
 .regen{background:var(--panel);border:1px solid var(--line);border-radius:16px;padding:18px;margin:28px auto 0;max-width:64ch;box-shadow:var(--shadow)}
 .regen textarea{height:76px}
 .gen{background:var(--panel2);color:var(--ink);border:1px solid #3a4a5f}.gen:hover{background:#28303c}
 .done{display:none;background:var(--ok);border:1px solid var(--ok-line);color:var(--ok-ink);padding:16px 18px;border-radius:12px;margin:20px auto 0;max-width:64ch;font-size:14px}
 code{background:var(--bg);border:1px solid var(--line);padding:2px 7px;border-radius:6px;font-size:12.5px}
</style></head><body>
<div class=wrap>
<header>
 <h1>Pick a meme + post</h1>
 <p class=sub>Edit the copy if you want, then Select one to finalize -- or write a steer and Generate more.</p>
</header>
<div class=grid id=grid></div>
<div class=regen>
 <div class=tpl>Steer the next batch</div>
 <textarea id=prompt placeholder="e.g. funnier, lean into the safety angle, try Distracted Boyfriend, punchier captions..."></textarea>
 <button class="btn gen" onclick="regen()">Generate more options</button>
</div>
<div class=done id=done></div>
</div>
<script>
let OPTS=[];
async function load(){OPTS=await (await fetch('/options.json?_='+Date.now())).json();render()}
function render(){
 grid.innerHTML='';
 OPTS.forEach(o=>{
  const c=document.createElement('div');c.className='card';
  c.innerHTML=`<img src="${o.meme_url}"><div class=tpl>${o.template}</div>
   <textarea class=post id="p_${o.id}">${o.post}</textarea>
   <button class="btn sel" onclick="pick('${o.id}')">Select this</button>`;
  grid.appendChild(c);
 });
}
async function pick(id){
 const post=document.getElementById('p_'+id).value;
 const r=await (await fetch('/action',{method:'POST',headers:{'Content-Type':'application/json'},
   body:JSON.stringify({type:'select',id,post})})).json();
 const o=OPTS.find(x=>x.id===id);
 done.style.display='block';
 done.innerHTML=`<b>Selected option ${id} (${o.template}).</b> Saved to <code>${r.path||'output/'}</code>. Upload the image and paste the copy into LinkedIn. You can close this tab.`;
 window.scrollTo(0,document.body.scrollHeight);
}
async function regen(){
 await fetch('/action',{method:'POST',headers:{'Content-Type':'application/json'},
   body:JSON.stringify({type:'regenerate',prompt:prompt.value})});
 done.style.display='block';
 done.innerHTML='<b>Sent to the agent.</b> A fresh batch is being generated -- this page refreshes when it is ready.';
 poll();
}
let seen=null;
async function poll(){
 const o=await (await fetch('/options.json?_='+Date.now())).json();
 const sig=JSON.stringify(o.map(x=>x.meme_url));
 if(seen && sig!==seen){seen=sig;done.style.display='none';return load();}
 seen=seen||sig; setTimeout(poll,1500);
}
load();
</script></body></html>"""


def save_selection(action):
    """Download the selected meme + write the post text into a dated output/ folder."""
    opts = json.load(open(os.path.join(HERE, "options.json")))
    chosen = next((o for o in opts if o["id"] == action["id"]), None)
    if not chosen:
        return {"ok": False, "error": "unknown option id"}
    outdir = os.path.join(HERE, "output", time.strftime("%Y%m%d-%H%M%S"))
    os.makedirs(outdir, exist_ok=True)
    ext = chosen["meme_url"].rsplit(".", 1)[-1] if chosen.get("meme_url") else "png"
    if chosen.get("meme_url"):
        req = urllib.request.Request(chosen["meme_url"], headers={"User-Agent": "Mozilla/5.0"})
        open(os.path.join(outdir, f"meme.{ext}"), "wb").write(urllib.request.urlopen(req).read())
    open(os.path.join(outdir, "post.txt"), "w").write(action.get("post", chosen.get("post", "")))
    json.dump(chosen, open(os.path.join(outdir, "selection.json"), "w"), indent=2)
    return {"ok": True, "path": os.path.relpath(outdir, HERE)}


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
