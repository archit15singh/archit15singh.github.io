---
title: "Listen to this post: free text-to-speech on a Hugo blog"
description: "How every post on this site got a read-aloud button with the Web Speech API: the two approach families, the seven browser bugs that shaped the code, the accessibility decisions, and the two Hugo traps that could have dropped the whole feature silently."
date: 2026-08-30T00:45:00+05:30
tags: [Engineering, WebSpeech, Accessibility, Hugo]
categories: [Engineering]
cover:
  image: "/images/uploads/tts-listen-banner.jpeg"
  alt: "A dark banner with a colored waveform and the words Give your blog a voice"
  hidden: false
---

There is a Listen button on top of every post here now. Press it and the browser reads the article aloud, highlights the paragraph it is speaking, shows progress in a status bar, and lets you jump to any paragraph by clicking it. It costs nothing per listener, stores no files, and shipped as three files and a config flag. Here is exactly how it works and what I had to dodge to make it survive the real world.

## Two ways to make a blog speak

Pre-generated audio and browser synthesis solve the same problem with opposite tradeoffs. The first option runs a script over every post, sends the cleaned prose to a TTS service or model, and commits an mp3. The voice is consistent, playback works offline and without JavaScript, and the audio file opens discoverability doors like RSS enclosures and schema markup. The cost is money per character, a regeneration pipeline on every edit, and a repo that grows by megabytes per post.

The second option uses the Web Speech API, specifically `speechSynthesis`. It has been in every serious browser since around 2016. You hand it a string, it says it with a voice that already lives on the device. No audio files, no API key, no build step, no cost. The price is that voice quality becomes a lottery controlled by the reader's operating system, playback stops the moment JavaScript fails, and nothing about the experience is machine-readable.

I chose browser synthesis. This is a small personal site with eleven posts. A generation pipeline would be more machinery than it serves, and the accessibility win is the same either way: people who would rather listen get to listen. When the site grows up and a consistent narrator matters, the honest upgrade path is pre-generated audio behind the same button, not a rewrite.

## What ships

Three files live in the repo.

`layouts/_default/single.html` is a byte-for-byte copy of the PaperMod single-post template with one extra line injected above the content: `partial "listen.html"`. Hugo prefers the root layout over the theme's, so the theme submodule stays untouched. That is the only reason the override stays maintainable; any theme bump shows up as a one-line diff instead of a fork war.

`layouts/partials/listen.html` renders the player: a Listen button that becomes Pause then Resume, a Stop button, a speed toggle that cycles 1x, 1.25x, 1.5x, 2x, and a voice picker. It starts with the `hidden` attribute and only un-hides when JavaScript confirms `speechSynthesis` exists. If the browser can't speak, the button simply never appears. The CSS is scoped inside the partial so the player never leaks styling into the theme.

`static/js/listen.js` does the work. It walks the article with a `TreeWalker`, collects text from paragraphs and list items, skips code blocks, footnotes, and asides, splits everything into short speakable chunks, and drives the state machine: idle, playing, paused.

The global kill switch is one flag in `config.yml`, `params.tts.enabled`. A post can opt out with `tts: false` in its frontmatter.

## The bug pile

Every piece of the design is a scar from a browser behavior that fails silently. Chunking is the first. Chrome cancels an utterance after roughly 15 seconds of speech, which lands around 200 to 300 characters depending on the voice, and it does it without firing an error. Safari is worse, older versions stopped mid-sentence and newer ones bail around the same length. The fix is to never hand the engine anything longer than 220 characters. My chunks are sentence-sized, so listeners get a tiny pause that sounds natural, and I renegotiate the chunk between blocks so a long paragraph doesn't just keep going.

iOS Safari denies `speak()` outright unless it runs inside a tap or click handler. No error, no log entry, just silence. Everything in the player starts from a button click, and the rate change restarts the current chunk from inside its own click, which keeps the chain alive. The famous workaround is to speak a blank utterance during the first click to "unlock" the engine for everything after. My first click is the first real utterance, so the unlock is the feature itself.

Android does not pause. `speechSynthesis.pause()` on Android cancels instead, and the difference is invisible from JavaScript. So the player never calls pause. Pause is implemented as cancel plus a remembered position, and resume re-speaks from the current chunk. The cost is that resuming rereads at most one sentence, which is a trade everyone accepts once Android is in the room.

Voices don't load on a schedule. Chrome and Firefox load the list asynchronously and fire `voiceschanged`. Safari often loads it synchronously and sometimes never fires the event at all. The picker populates from the event when it arrives, and a 250 ms polling fallback keeps filling until voices show up. Both paths write into the same function, so whichever wins, the dropdown ends up complete.

The strangest one came from a bug report filed years after the API stabilized. On iOS 26 and macOS 26, a spoken string that starts with `<` or ends with `>` bricks every voice in the browser until the user restarts Safari. Not a wrong reading, a dead speech engine. I sanitize the text before it becomes an utterance, swapping angle brackets for their full-width lookalikes, because a blog about command-line tools is exactly the kind of page where `->` shows up in prose. I have no idea which Apple build introduced it, and the workaround costs one line.

## Accessibility is the point, not the polish

A read-aloud button is an accessibility feature first. It helps people with low vision, dyslexia, or any situation where eyes are busy. So the player itself has to pass the standards it exists to serve.

Every button carries an `aria-label` that changes with state. A screen reader hears "Pause reading", not a button that says Pause and means something different tomorrow. The status line is `role="status"` with `aria-live="polite"`, so state transitions are announced without yanking focus. The whole player declares itself a `role="region"` landmark named "Article reader", which lets screen-reader users jump straight to it. Touch targets sit at a 2.4rem minimum, because the stop button was useless on a phone at the size a mouse likes. Focus stays visible.

And WCAG gets cheap here in a way most accessibility work doesn't. The audio is generated from the article text at read time, so the on-page text is the transcript by construction. There is no separate transcript to write, no synchronization to maintain. Adding a player to real content inherits that honesty for free.

## The two traps that eat features silently

Posters on `buildFuture: false` blog setups share a sad genre of GitHub issue: the post built fine locally, deployed clean, and is nowhere on the internet. A future date in the persona wheel and the post silently drops out of the build. Setting a usable date in frontmatter is step zero for this site.

The second trap is Hugo's `default` helper. `(.Param "tts") | default true` returns `true` when frontmatter sets `tts: false`, because Hugo treats `false` as empty. The per-post opt-out therefore has to be spelled `and .Site.Params.tts.enabled (ne (.Param "tts") false)`. Half the TTS code that exists in the wild is buggy for a one-word reason.

## What I deliberately skipped

Pre-generated audio, og:audio tags, AudioObject schema, RSS enclosures, and a podcast feed all look like obvious next steps. They all have the same requirement, which is a real audio file. Browser synthesis never creates one, so none of those signals apply to this setup. And the SEO case for chasing them is weaker than the hype: AudioObject has no Google rich result today, so the markup is entity bookkeeping, not a SERP feature. A local 82-parameter voice model running on-device is genuinely tempting, but it trades the consistent-voice problem for a multi-megabyte download per reader. At eleven posts it is not worth it.

## Verifying without a phone

The player gets exercised in headless Chrome with a small Playwright script that clicks through the whole state machine: start, read status changes to "Reading · 0%", pause flips to "Resume", clicking a paragraph two-thirds down the article jumps the reader to "Reading · 59%", stop resets everything, and the console ends with zero errors. That catches regressions but misses the mobile truth. iOS behavior was confirmed the boring way: on a real phone, with a real tap, because emulated clicks do not carry the same autoplay permissions as the thing on the desk next to me.

## The honest limits

The voice is the reader's OS voice. On a Mac the picker offers all 181 installed voices and the quality is genuinely good. On a phone it depends on what the manufacturer shipped. There is no seek bar, because the Speech API does not expose position, only chunk boundaries. And background-tab playback is unreliable; browsers throttle synthesis when the tab loses focus, so this is a read-along feature, not a hands-free podcast replacement.

Those limits are the other side of the trade that made this free and zero-maintenance. The moment consistent narration matters more than the cost of generating it, I know exactly which files to rewrite and which button stays.

Try the Listen button at the top of this post. Give it a slow voice, it reads like a person. Give it a fast one and see how far the highlight tracking holds.