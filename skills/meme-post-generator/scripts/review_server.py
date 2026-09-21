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
 body{font-family:-apple-system,Segoe UI,Roboto,sans-serif;background:#0f1115;color:#e8eaed;margin:0;padding:32px}
 h1{font-size:20px;font-weight:600;margin:0 0 4px} .sub{color:#9aa0a6;margin:0 0 24px;font-size:13px}
 .grid{display:flex;gap:20px;flex-wrap:wrap}
 .card{background:#1a1d23;border:1px solid #2a2e37;border-radius:14px;padding:16px;width:360px;display:flex;flex-direction:column}
 .card img{width:100%;border-radius:8px;background:#000}
 .tpl{font-size:12px;color:#9aa0a6;margin:10px 0 4px}
 textarea{width:100%;box-sizing:border-box;background:#0f1115;color:#e8eaed;border:1px solid #2a2e37;border-radius:8px;padding:10px;font:inherit;font-size:13px;resize:vertical}
 .post{height:120px} .btn{margin-top:10px;padding:10px 14px;border:0;border-radius:8px;font-weight:600;cursor:pointer}
 .sel{background:#3b82f6;color:#fff} .sel:hover{background:#2f6fe0}
 .regen{background:#1a1d23;border:1px solid #2a2e37;border-radius:14px;padding:16px;margin-top:24px;max-width:756px}
 .regen textarea{height:70px} .gen{background:#22303f;color:#e8eaed;border:1px solid #3a4a5f}.gen:hover{background:#2b3d50}
 .done{display:none;background:#132b16;border:1px solid #1f5127;color:#a6e6b0;padding:14px;border-radius:10px;margin-top:20px;max-width:756px}
 code{background:#0f1115;padding:2px 6px;border-radius:4px}
</style></head><body>
<h1>Pick a meme + post</h1>
<p class=sub>Edit the copy if you want, then Select one to finalize -- or write a steer and Generate more.</p>
<div class=grid id=grid></div>
<div class=regen>
 <div class=tpl>Not quite right? Tell the agent how to steer the next batch:</div>
 <textarea id=prompt placeholder="e.g. funnier, lean into the safety angle, try Distracted Boyfriend, punchier captions..."></textarea>
 <button class="btn gen" onclick="regen()">Generate more options</button>
</div>
<div class=done id=done></div>
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
