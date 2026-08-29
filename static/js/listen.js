(() => {
  "use strict";

  if (!("speechSynthesis" in window)) return;

  const player = document.querySelector(".listen-player");
  const content = document.querySelector(".post-content");
  if (!player || !content) return;

  const MAX_CHARS = 300;
  const RATES = [1, 1.25, 1.5, 2];
  const SKIP_SELECTOR = "pre, code, .highlight, script, style, .footnotes, aside, kbd, samp";
  const SYNTH = window.speechSynthesis;

  const btnPlay = player.querySelector(".lp-play");
  const btnStop = player.querySelector(".lp-stop");
  const btnRate = player.querySelector(".lp-rate");
  const statusEl = player.querySelector(".lp-status");

  let items = [];
  let rateIdx = 0;
  let current = -1;
  let mode = "idle"; // idle | playing | paused
  let gen = 0;
  let watchdog = null;
  let lastSpeechOp = 0;

  player.hidden = false;

  function buildItems() {
    const map = new Map();
    const walker = document.createTreeWalker(content, NodeFilter.SHOW_TEXT, {
      acceptNode(node) {
        if (!node.textContent || !node.textContent.trim()) return NodeFilter.FILTER_REJECT;
        if (node.parentElement.closest(SKIP_SELECTOR)) return NodeFilter.FILTER_REJECT;
        return NodeFilter.FILTER_ACCEPT;
      },
    });
    while (walker.nextNode()) {
      const node = walker.currentNode;
      const el =
        node.parentElement.closest("p,li,td,blockquote,h2,h3,h4,h5,h6") ||
        node.parentElement;
      if (!map.has(el)) map.set(el, []);
      map.get(el).push(node.textContent.trim());
    }
    const out = [];
    map.forEach((parts, el) => {
      const text = parts.join(" ").replace(/\s+/g, " ").trim();
      if (!text) return;
      for (const chunk of splitChunks(text)) out.push({ el, text: chunk });
    });
    return out;
  }

  function splitChunks(text) {
    const sentences = text.match(/[^.!?…]+(?:[.!?…]+["')\]]*)/g) || [text];
    const chunks = [];
    for (const raw of sentences) {
      let s = raw.trim();
      if (!s) continue;
      if (s.length <= MAX_CHARS) {
        chunks.push(s);
        continue;
      }
      const words = s.split(/\s+/);
      let cur = "";
      for (const w of words) {
        if (cur && (cur + " " + w).length > MAX_CHARS) {
          chunks.push(cur);
          cur = w;
        } else {
          cur = cur ? cur + " " + w : w;
        }
      }
      if (cur) chunks.push(cur);
    }
    return chunks;
  }

  function pickVoice() {
    const voices = SYNTH.getVoices ? SYNTH.getVoices() : [];
    return (
      voices.find((v) => /en[-_]US/i.test(v.lang) && !v.localService) ||
      voices.find((v) => /en[-_]US/i.test(v.lang)) ||
      voices.find((v) => /^en/i.test(v.lang)) ||
      null
    );
  }

  function utteranceFor(text) {
    const u = new SpeechSynthesisUtterance(text);
    u.lang = document.documentElement.lang || "en-US";
    u.rate = RATES[rateIdx];
    const v = pickVoice();
    if (v) u.voice = v;
    return u;
  }

  function clearHighlight() {
    content.querySelectorAll(".lp-active").forEach((el) => el.classList.remove("lp-active"));
  }

  function setHighlight(el) {
    clearHighlight();
    if (el) el.classList.add("lp-active");
  }

  function setStatus(msg) {
    statusEl.textContent = msg || "";
  }

  function setLabels() {
    if (mode === "idle") {
      btnPlay.textContent = "Listen";
      btnStop.hidden = true;
    } else if (mode === "paused") {
      btnPlay.textContent = "Resume";
      btnStop.hidden = false;
    } else {
      btnPlay.textContent = "Pause";
      btnStop.hidden = false;
    }
  }

  function startWatchdog() {
    stopWatchdog();
    watchdog = setInterval(() => {
      if (mode !== "playing") return;
      if (current < 0 || current >= items.length) return;
      if (SYNTH.speaking || SYNTH.pending) return;
      if (Date.now() - lastSpeechOp < 2000) return;
      const t = gen;
      SYNTH.cancel();
      setTimeout(() => {
        if (gen === t) speakOne();
      }, 100);
    }, 1000);
  }

  function stopWatchdog() {
    if (watchdog) {
      clearInterval(watchdog);
      watchdog = null;
    }
  }

  function speakOne() {
    const u = items[current];
    lastSpeechOp = Date.now();
    const myGen = gen;
    const utt = utteranceFor(u.text);
    utt.onstart = () => {
      if (gen !== myGen) return;
      setHighlight(u.el);
    };
    utt.onend = () => {
      if (gen !== myGen) return;
      nextChunk();
    };
    utt.onerror = () => {
      if (gen !== myGen) return;
      nextChunk();
    };
    SYNTH.speak(utt);
  }

  function nextChunk() {
    current += 1;
    if (current >= items.length) {
      finish();
      return;
    }
    speakOne();
  }

  function start() {
    gen += 1;
    items = buildItems();
    if (!items.length) {
      setStatus("No readable text on this page.");
      return;
    }
    current = 0;
    mode = "playing";
    setStatus("Reading");
    setLabels();
    startWatchdog();
    speakOne();
  }

  function pause() {
    if (mode !== "playing") return;
    gen += 1;
    SYNTH.cancel();
    mode = "paused";
    setStatus("Paused");
    setLabels();
  }

  function resume() {
    if (mode !== "paused" || current < 0) return;
    mode = "playing";
    setStatus("Reading");
    setLabels();
    startWatchdog();
    speakOne();
  }

  function stop() {
    gen += 1;
    SYNTH.cancel();
    current = -1;
    mode = "idle";
    clearHighlight();
    setStatus("");
    setLabels();
    stopWatchdog();
  }

  function finish() {
    gen += 1;
    current = -1;
    mode = "idle";
    clearHighlight();
    setStatus("Finished");
    setLabels();
    stopWatchdog();
  }

  btnPlay.addEventListener("click", () => {
    if (mode === "idle") start();
    else if (mode === "playing") pause();
    else resume();
  });

  btnStop.addEventListener("click", stop);

  btnRate.addEventListener("click", () => {
    rateIdx = (rateIdx + 1) % RATES.length;
    btnRate.textContent = RATES[rateIdx] + "x";
    if (mode === "playing") {
      const t = gen;
      SYNTH.cancel();
      setTimeout(() => {
        if (gen === t) speakOne();
      }, 100);
    }
  });

  window.addEventListener("beforeunload", () => SYNTH.cancel());

  if (SYNTH.getVoices) {
    SYNTH.getVoices();
    SYNTH.onvoiceschanged = () => SYNTH.getVoices();
  }
})();