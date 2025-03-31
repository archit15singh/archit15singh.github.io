
---
title: "JS execution model in depth"
date: 2022-07-29T12:00:00.000Z
tags:
  - JavaScript
  - JavaScript Execution Model
categories: JavaScript
description: "An in-depth breakdown of the JS execution model"
cover:
  hidden: false
  relative: false
  image: /images/uploads/cosmic-timetraveler.webp
  alt: "JS execution model"
  caption: "JS execution model"
editPost:
  URL: ""
  Text: ""
  appendFilePath: false
showToc: true
TocOpen: true
hidemeta: false
comments: true
disableHLJS: false
disableShare: false
hideSummary: false
searchHidden: false
ShowReadingTime: true
ShowBreadCrumbs: true
ShowPostNavLinks: true
ShowWordCount: true
ShowRssButtonInSectionTermList: false
UseHugoToc: true
image_format: "webp"
---



# JS execution model
Alright, let’s break this down recursively and deeply, line by line, starting with the **JavaScript execution model** intro and progressing through the first sections. I’ll give you:

1. **Literal meaning** (What it says)
2. **Deeper understanding** (Why it matters)
3. **Mental model / real-world analogy** (To cement intuition)

---

### 📘 **"JavaScript execution model"**

#### ✅ Literal meaning:
This document explains how JavaScript runs behind the scenes — how it processes code, manages memory, handles functions, etc.

#### 🔍 Deeper understanding:
Think of this as the operating system of JavaScript — what *actually happens* when you write `let a = 5` or `setTimeout(...)`.

#### 🧠 Analogy:
If your code is like a script in a play, the execution model is the stage manager deciding when and how each line of the script gets read and acted upon.

---

### 📝 **"This page introduces the basic infrastructure of the JavaScript runtime environment."**

#### ✅ Literal meaning:
We’re talking about the *runtime* — where JS code is executed (not compiled). This includes things like memory, stacks, event loops, etc.

#### 🔍 Deeper understanding:
JavaScript isn’t just interpreted randomly. There’s a whole structure that controls how code gets parsed, run, paused, resumed.

#### 🧠 Analogy:
Imagine a kitchen: the runtime is the kitchen itself (countertop = stack, fridge = heap, bell = job queue). Chefs = JavaScript agents.

---

### 🛠 **"The model is largely theoretical and abstract, without any platform-specific or implementation-specific details."**

#### ✅ Literal meaning:
This isn’t about Chrome’s V8 engine or Node’s internals — it’s the universal, spec-level blueprint.

#### 🔍 Deeper understanding:
You’re learning how things *should* behave according to ECMAScript — the spec all JS engines follow (more or less).

#### 🧠 Analogy:
Like learning the *rules* of chess, not how Magnus Carlsen plays.

---

### 🧠 **"Modern JavaScript engines heavily optimize the described semantics."**

#### ✅ Literal meaning:
Real engines like V8 or SpiderMonkey tweak things under the hood for speed, but they follow the same rules.

#### 🔍 Deeper understanding:
JS engines may compile JS to bytecode, inline functions, optimize away allocations — but logically, they obey this model.

#### 🧠 Analogy:
Like a Formula 1 pit crew following safety rules — they do things super fast, but not incorrectly.

---

### 📖 **"This page is a reference. It assumes you are already familiar with the execution model of other programming languages, such as C and Java."**

#### ✅ Literal meaning:
If you’ve worked with languages that have stacks, heaps, and memory — this will feel familiar.

#### 🔍 Deeper understanding:
JS is dynamic and event-driven, but under the hood, it's not that different from C/Java — it just hides more from you.

#### 🧠 Analogy:
It’s like someone who’s driven automatic cars learning how a manual transmission works under the hood.

---

### 🔧 **"It makes heavy references to existing concepts in operating systems and programming languages."**

#### ✅ Literal meaning:
Terms like stack, heap, queue, thread — all come from OS/PL theory.

#### 🔍 Deeper understanding:
This section connects JS to how *all* programming languages manage code execution and memory.

#### 🧠 Analogy:
It’s like learning JavaScript’s "internals" by understanding its plumbing — threads, memory, job queues.

---

Next section...

---

## 🔥 **The engine and the host**

### 🧩 **"JavaScript execution requires the cooperation of two pieces of software: the JavaScript engine and the host environment."**

#### ✅ Literal meaning:
JS doesn’t run on its own. It needs:
- A **JS engine** (like V8, SpiderMonkey)
- A **host** (like the browser or Node)

#### 🔍 Deeper understanding:
The engine knows how to *parse* and *run* JavaScript.
The host (browser/Node) knows how to *give JS things to do* — like making network requests or rendering HTML.

#### 🧠 Analogy:
The JS engine is the actor. The host is the stage, props, lighting, and audience.

---

### 🧠 **"The JavaScript engine implements the ECMAScript (JavaScript) language, providing the core functionality."**

#### ✅ Literal meaning:
The engine knows what `let`, `function`, `Promise`, etc., mean. That’s ECMAScript.

#### 🔍 Deeper understanding:
Things like `setTimeout` or `document.querySelector`? Those are host-provided, not part of the language spec.

#### 🧠 Analogy:
The engine knows English. The host gives it a job — like reading a book, or talking to a user.

---

### 🌍 **"In order to interact with the outside world [...] we need additional environment-specific mechanisms provided by the host environment."**

#### ✅ Literal meaning:
To talk to files, web APIs, timers, you need help from the host — JS alone can’t do it.

#### 🔍 Deeper understanding:
This is where browsers give us `document`, and Node gives us `fs`, etc. It’s why JS looks different in each environment.

#### 🧠 Analogy:
JavaScript is a brilliant chef, but it needs the host to supply groceries, an oven, or even the guests to cook for.

---

### 🌐 **"For example, the HTML DOM is the host environment when JavaScript is executed in a web browser. Node.js is another host environment..."**

#### ✅ Literal meaning:
DOM and `window` exist only in the browser. `require` and `process` exist only in Node.

#### 🔍 Deeper understanding:
Same language, different surroundings = different power/tools. JS is *host-agnostic*; host APIs change.

#### 🧠 Analogy:
Same actor, different movie set. A sci-fi set vs. a historical drama set gives the actor different things to interact with.

---
Awesome — let's dive into a **line-by-line, recursive breakdown** of the JavaScript Execution Model section. I'll break down each sentence, unpack the underlying concepts, and relate them to real-world analogies and code where helpful.

---

### 🔹**JavaScript execution model**
> **This page introduces the basic infrastructure of the JavaScript runtime environment.**

- **Breakdown:** We’re about to learn how JavaScript runs "under the hood." That means looking beyond syntax into how your code gets executed, managed, and scheduled by the JS engine.

> **The model is largely theoretical and abstract, without any platform-specific or implementation-specific details.**

- **Breakdown:** This is not about how Chrome, Node, or Deno *implement* JavaScript — it’s about the ECMAScript **specification-level model**. Think of this as the universal blueprint all JS engines follow.

> **Modern JavaScript engines heavily optimize the described semantics.**

- **Breakdown:** V8 (Chrome), SpiderMonkey (Firefox), and others add many performance improvements — JIT compilation, inlining, hidden classes — but they **preserve the behavior** defined in this theoretical model.

---

### 🔹**This page is a reference. It assumes you are already familiar with the execution model of other programming languages, such as C and Java.**

- **Breakdown:** It expects you know what a *call stack*, *heap*, and *execution context* are from other languages — but don't worry, we’ll unpack everything from a JavaScript-first view.

---

### 🔹**The engine and the host**

> **JavaScript execution requires the cooperation of two pieces of software: the JavaScript engine and the host environment.**

- **Breakdown:**  
  - **Engine** → Understands & runs JS (e.g. V8, SpiderMonkey).
  - **Host** → Provides APIs **outside** of JS (e.g., the DOM, `setTimeout`, `fs` in Node).
  
📌 Analogy: The engine is the actor, but the host is the stage, props, and audience.

---

> **The JavaScript engine implements the ECMAScript (JavaScript) language, providing the core functionality. It takes source code, parses it, and executes it.**

- **Breakdown:**
  1. **Parses** → Converts your code into an Abstract Syntax Tree (AST).
  2. **Executes** → Evaluates it via interpreters or compilers.

```js
let x = 5;
```
- Engine knows how to parse and execute this, but not how to access the DOM. That’s the host's job.

---

> **However, in order to interact with the outside world, such as to produce any meaningful output, to interface with external resources, or to implement security- or performance-related mechanisms, we need additional environment-specific mechanisms provided by the host environment.**

- **Breakdown:** Engine alone can’t do I/O, networking, file access. Host provides:
  - `console.log`, `fetch`, `setTimeout`, `document`, `process.env`, etc.

---

> **For example, the HTML DOM is the host environment when JavaScript is executed in a web browser. Node.js is another host environment that allows JavaScript to be run on the server side.**

- **Breakdown:**
  - Browser = JS engine + DOM + `window` + events.
  - Node = JS engine + `fs`, `http`, `Buffer`, `process`, etc.

---

> **While we focus primarily on the mechanisms defined in ECMAScript in this reference, we will occasionally talk about mechanisms defined in the HTML spec, which is often mimicked by other host environments like Node.js or Deno.**

- **Breakdown:** 
  - Core focus = ECMAScript (language spec).
  - But we'll touch on HTML-defined behaviors (like the Event Loop, microtasks) — because Node/Deno borrow them too.

---

### 🔹**Agent Execution Model**

> **In the JavaScript specification, each autonomous executor of JavaScript is called an agent, which maintains its facilities for code execution:**

- **Breakdown:**  
  - Think of an **agent** as an independent "runner" of JavaScript — like a tab, worker, or Node thread.
  - Each agent has its own **heap**, **call stack**, and **job queue**.

---

Now, let’s recursively unpack the **three components** of an agent:

---

#### 🔸 **Heap (of objects)**
> **This is just a name to denote a large (mostly unstructured) region of memory. It gets populated as objects get created in the program.**

- **Breakdown:**  
  - Heap = where **reference types** live: objects, arrays, closures, functions.
  - Variables like `let obj = {}` create entries in the heap.
  
```js
let obj = { name: "you" };
```
The object lives in the heap; `obj` points to it.

---

> **Note that in the case of shared memory, each agent has its own heap with its own version of a SharedArrayBuffer object, but the underlying memory represented by the buffer is shared.**

- **Breakdown:**  
  - Each worker/tab has its own isolated heap — but **shared memory** (via `SharedArrayBuffer`) creates **cross-agent bridges**.
  - Shared memory enables atomic operations between agents.

📌 Think: *Multiple agents → own memory → but one shared space for coordination*.

---

#### 🔸 **Queue (of jobs)**

> **This is known in HTML (and also commonly) as the event loop which enables asynchronous programming in JavaScript while being single-threaded.**

- **Breakdown:**
  - Queue = **Job Queue / Task Queue**.
  - Works with the **event loop** to schedule **async tasks** (like `setTimeout`, Promises).

---

> **It's called a queue because it's generally first-in-first-out: earlier jobs are executed before later ones.**

- **Breakdown:**
  - Classic **FIFO** structure.
  - Tasks are queued and **executed one by one**, preserving order.

---

#### 🔸 **Stack (of execution contexts)**

> **This is what's known as a call stack and allows transferring control flow by entering and exiting execution contexts like functions.**

- **Breakdown:**
  - Stack = execution history — functions being called and exited.
  - LIFO — last-in, first-out.

```js
function a() {
  b();
}
function b() {
  c();
}
a(); // a → b → c → return → return → return
```

---

> **It's called a stack because it's last-in-first-out. Every job enters by pushing a new frame onto the (empty) stack, and exits by emptying the stack.**

- **Breakdown:**
  - A function call pushes a **frame** onto the stack.
  - When it returns, the frame is popped off.

---

> **These are three distinct data structures that keep track of different data.**

- **Heap** → Long-lived objects.
- **Queue** → Pending jobs (like `fetch().then()`).
- **Stack** → Current execution chain (call stack).

---

> **We will introduce the queue and the stack in more detail in the following sections. To read more about how heap memory is allocated and freed, see memory management.**

- **Breakdown:**  
  - Stack and queue will be our main focus because they control **how code runs**.
  - Heap is for **storage**, not **flow**.

---

### 🧠 Up Next:
We’ll dive into the next section — **realms**, agents on the web (workers, windows), and how these fit together using the diagram you shared.

Want to continue into that next?
