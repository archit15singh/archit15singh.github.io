(() => {
  "use strict";

  if (!("speechSynthesis" in window)) return;

  const player = document.querySelector(".listen-player");
  const content = document.querySelector(".post-content");
  if (!player || !content) return;

  const MAX_CHARS = 220;
  const RATES = [1, 1.25, 1.5, 2];
  const VOICE_POLL_MS = 250;
  const SKIP_SELECTOR = "pre, code, .highlight, script, style, .footnotes, aside, kbd, samp";
  const VOICE_KEY = "listen-voice-name";
  const SYNTH = window.speechSynthesis;

  const btnPlay = player.querySelector(".lp-play");
  const btnStop = player.querySelector(".lp-stop");
  const btnRate = player.querySelector(".lp-rate");
  const voiceSel = player.querySelector(".lp-voice");
  const statusEl = player.querySelector(".lp-status");

  let items = [];
  let rateIdx = 0;
  let current = -1;
  let mode = "idle"; // idle | playing | paused
  let gen = 0;
  let watchdog = null;
  let voicePoll = null;
  let lastSpeechOp = 0;
  let selectedVoice = null;

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

  function sanitizeForSpeech(text) {
    return text.replace(/[<>]/g, (ch) => (ch === "<" ? "\uff1c" : "\uff1e"));
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

  function voiceRank(v) {
    let r = 0;
    if (/^en/i.test(v.lang)) r -= 2;
    if (/en[-_]US/i.test(v.lang)) r -= 1;
    if (!v.localService) r -= 1;
    return r;
  }

  function allVoices() {
    return SYNTH.getVoices ? SYNTH.getVoices().slice() : [];
  }

  function pickVoice() {
    const voices = allVoices();
    if (selectedVoice && voices.some((v) => v.name === selectedVoice.name)) {
      return selectedVoice;
    }
    const fallback = [...voices].sort((a, b) => voiceRank(a) - voiceRank(b))[0] || null;
    return fallback;
  }

  function populateVoices() {
    const voices = allVoices();
    if (!voices.length) return;
    const saved = voiceSel.value;
    voiceSel.innerHTML = "";
    const auto = document.createElement("option");
    auto.value = "";
    auto.textContent = "Default voice";
    voiceSel.appendChild(auto);
    [...voices]
      .sort((a, b) => voiceRank(a) - voiceRank(b) || a.name.localeCompare(b.name))
      .forEach((v) => {
        const opt = document.createElement("option");
        opt.value = v.name;
        opt.textContent = v.name + (v.localService ? "" : " ·online");
        voiceSel.appendChild(opt);
      });
    if (saved) {
      voiceSel.value = saved;
    } else {
      const stored = localStorage.getItem(VOICE_KEY);
      if (stored && voices.some((v) => v.name === stored)) voiceSel.value = stored;
    }
    selectedVoice =
      voices.find((v) => v.name === voiceSel.value) || null;
  }

  function utteranceFor(text) {
    const u = new SpeechSynthesisUtterance(sanitizeForSpeech(text));
    u.lang = document.documentElement.lang || "en-US";
    u.rate = RATES[rateIdx];
    const v = pickVoice();
    if (v) u.voice = v;
    return u;
  }

  function clearHighlight() {
    content.querySelectorAll(".lp-active").forEach((el) => el.classList.remove("lp-active"));
  }

  function scrollElIntoView(el) {
    if (!el) return;
    const r = el.getBoundingClientRect();
    const vh = window.innerHeight || document.documentElement.clientHeight;
    if (r.top < 0 || r.bottom > vh) {
      el.scrollIntoView({ block: "center", behavior: "smooth" });
    }
  }

  function setHighlight(el) {
    clearHighlight();
    if (el) {
      el.classList.add("lp-active");
      scrollElIntoView(el);
    }
  }

  function pct() {
    if (!items.length) return 0;
    return Math.min(100, Math.round(((current + 1) / items.length) * 100));
  }

  function setStatus(msg) {
    statusEl.textContent = msg || "";
  }

  function updateStatus() {
    if (mode === "playing") setStatus("Reading · " + pct() + "%");
    else if (mode === "paused") setStatus("Paused · " + pct() + "%");
    else setStatus("");
  }

  function setLabels() {
    btnPlay.setAttribute(
      "aria-label",
      mode === "idle" ? "Listen to this post" : mode === "paused" ? "Resume reading" : "Pause reading"
    );
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
    updateStatus();
  }

  function beginAt(i) {
    gen += 1;
    if (i < 0 || i >= items.length) i = 0;
    current = i;
    mode = "playing";
    setLabels();
    startWatchdog();
    updateStatus();
    speakOne();
  }

  function start() {
    items = buildItems();
    if (!items.length) {
      setStatus("No readable text on this page.");
      return;
    }
    beginAt(0);
  }

  function startFromElement(el) {
    items = buildItems();
    const idx = items.findIndex((it) => it.el === el);
    if (idx === -1) return;
    beginAt(idx);
  }

  function pause() {
    if (mode !== "playing") return;
    gen += 1;
    SYNTH.cancel();
    mode = "paused";
    updateStatus();
    setLabels();
  }

  function resume() {
    if (mode !== "paused" || current < 0) return;
    mode = "playing";
    setLabels();
    startWatchdog();
    updateStatus();
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
    setStatus("Finished · 100%");
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

  voiceSel.addEventListener("change", () => {
    const voices = allVoices();
    selectedVoice = voices.find((v) => v.name === voiceSel.value) || null;
    if (selectedVoice) localStorage.setItem(VOICE_KEY, selectedVoice.name);
    else localStorage.removeItem(VOICE_KEY);
    if (mode === "playing") {
      const t = gen;
      SYNTH.cancel();
      setTimeout(() => {
        if (gen === t) speakOne();
      }, 100);
    }
  });

  content.addEventListener("click", (e) => {
    if (e.target.closest("a,button")) return;
    if (window.getSelection && window.getSelection().toString()) return;
    const el = e.target.closest("p,li,td,blockquote,h2,h3,h4,h5,h6");
    if (!el || !content.contains(el)) return;
    startFromElement(el);
  });

  window.addEventListener("beforeunload", () => SYNTH.cancel());

  if (SYNTH.getVoices) {
    SYNTH.getVoices();
    SYNTH.onvoiceschanged = () => {
      SYNTH.getVoices();
      populateVoices();
      stopVoicePoll();
    };
    startVoicePoll();
  }
  populateVoices();

  function startVoicePoll() {
    stopVoicePoll();
    voicePoll = setInterval(() => {
      const voices = allVoices();
      if (voices.length) {
        populateVoices();
        stopVoicePoll();
      }
    }, VOICE_POLL_MS);
  }

  function stopVoicePoll() {
    if (voicePoll) {
      clearInterval(voicePoll);
      voicePoll = null;
    }
  }
})();