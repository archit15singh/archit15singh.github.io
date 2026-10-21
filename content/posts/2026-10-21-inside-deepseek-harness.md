---
title: "The Model Is Not the Agent — Inside DeepSeek Harness"
description: "A source-code deep dive into the execution loop, tool calling, context management, and state that turn an LLM into a working agent."
date: 2026-10-21T01:00:00+05:30
tags: [AI Agents, DeepSeek, Architecture, Reliability]
categories: [Engineering]
cover:
  image: "/images/uploads/deepseek-harness-execution.svg"
  alt: "Source-verified DeepSeek Harness execution loop and state boundaries"
  hidden: false
---

You ask a coding agent to fix a failing test. Somewhere, a model generates tokens. But tokens do not open files, decide which shell command is permitted, preserve a session after a crash, or establish that the test now passes. The execution system has to make those things happen.

That system is the harness. Its decisions determine how reasoning becomes action, what the model sees next, and which failures remain recoverable. To understand an agent's reliability, we need to follow those boundaries in code.

For this first source dive, I examined the official [DeepSeek Harness repository](https://github.com/deepseek-ai/deepseek-harness) at [commit `687f282e8625c6b8d11ff58211a90524be2e4317`](https://github.com/deepseek-ai/deepseek-harness/tree/687f282e8625c6b8d11ff58211a90524be2e4317). The repository identifies this as a developer preview built on Cordis. Every source link below is pinned because a moving branch is a poor foundation for an architectural claim.

This is a source-level investigation with a controlled tool-round-trip reference, not a live-model benchmark or a claim that I watched a real bug get fixed. I ran the upstream loop, cancellation, session-repair and compaction suites at this revision: 262 tests passed across five files. Those controlled tests support the branches discussed here; they do not establish production success rates. The interesting result is how the implementation separates an action from knowledge of its outcome.

## Follow one request through the machine

The useful place to start is `ReactLoopAgent`, rather than the model provider. Its driver separates a **turn**, the work triggered by incoming messages, from a **step**, one model interaction and its resulting tool work. That distinction gives cancellation, retries and follow-up messages somewhere precise to land.

For a small, inspectable execution, consider the repository's own [tool round-trip test](https://github.com/deepseek-ai/deepseek-harness/blob/687f282e8625c6b8d11ff58211a90524be2e4317/packages/core/agent-loop/tests/loop.spec.ts#L488). A mock adapter first requests `echo({text: "ping"})`; a registered tool returns `echo: ping`; the adapter then returns `done`. The test checks two model requests, the tool result in the second request, and both call and result events in the session log. It exercises the real driver and registry with controlled inference. It does not establish whether a production model can fix a bug.

Here is the path that makes that round trip possible.

**The task enters an inbox.** `followup()` supplies a user message. The driver claims the relevant pending messages and opens a turn. It doesn't simply concatenate every message it has ever seen into a prompt. The [pre-step path](https://github.com/deepseek-ai/deepseek-harness/blob/687f282e8625c6b8d11ff58211a90524be2e4317/packages/core/agent-loop/src/agent.ts#L267) assembles the system prompt and current context, then passes the proposed step through an `agent/pre-step` extension point. A policy can reject the step before a model call occurs.

**The request acquires an explicit model route.** The [request preparation path](https://github.com/deepseek-ai/deepseek-harness/blob/687f282e8625c6b8d11ff58211a90524be2e4317/packages/core/agent-loop/src/agent.ts#L564) starts with provider/model settings, lets the `agent/request` waterfall modify them, and resolves an adapter through `llm.prepareCall()`. Missing routing is an error. Adapter defaults are resolved for the request; they are not assumed to be permanent properties of the conversation.

**The model receives a projection of recorded state.** Prompt and user/context inputs enter the session as events. [`buildRequest()`](https://github.com/deepseek-ai/deepseek-harness/blob/687f282e8625c6b8d11ff58211a90524be2e4317/packages/core/agent-loop/src/agent.ts#L615) records the relevant request header and context metadata, derives the current messages, and freezes the request boundary. The durable history and the current model-visible conversation are related structures, with different jobs. The former supports reconstruction; the latter is what this inference actually consumes.

**Inference produces a stream, then a committed assistant message.** [`step()`](https://github.com/deepseek-ai/deepseek-harness/blob/687f282e8625c6b8d11ff58211a90524be2e4317/packages/core/agent-loop/src/agent.ts#L400) consumes chunks through `AssistantStreamAttempt`. The implementation distinguishes a live stream from its settled session record. A visible fragment is therefore not automatically a complete assistant action. Once the response settles, the driver extracts its tool-call blocks.

**The harness executes the request to call a tool.** [`executeToolCalls()`](https://github.com/deepseek-ai/deepseek-harness/blob/687f282e8625c6b8d11ff58211a90524be2e4317/packages/core/agent-loop/src/tool-calls.ts#L60) parses the arguments, classifies execution mode, and schedules calls through the tool runtime. The model has proposed a name and arguments. It has not directly invoked a shell or modified a file.

**The observation becomes input for the next step.** The scheduler records `tool/call` and `tool/result`, retaining their relationship. The next request derives its messages from the updated session. In the controlled round trip, this is where `echo: ping` becomes a tool-role observation that the second inference can read. When that inference returns `done` without another tool call, the step reports completion. Queued follow-ups and stopping hooks can still affect whether the turn actually ends.

![Source-verified DeepSeek Harness execution loop](/images/uploads/deepseek-harness-execution.svg)

*Original diagram traced against commit `687f282e8625c6b8d11ff58211a90524be2e4317`. It shows the default driver and extension boundaries, not every plugin in a deployed profile. The echo round trip is the executable reference; “fix a failing test” remains the motivating task.*

For a coding task, replace the echo tool with file inspection, edits and shell execution. The control structure remains recognizable, but the consequences change. Reading a file and running a migration are both tool calls; their recovery semantics are very different.

## Where the responsibilities live

The [architecture document](https://github.com/deepseek-ai/deepseek-harness/blob/687f282e8625c6b8d11ff58211a90524be2e4317/docs/architecture.md#core-packages) makes an unusually explicit commitment: the agent loop itself is a Cordis plugin. So are the model adapter, tool registry and session services. A running product is a configured plugin tree, rather than a model SDK with a few callbacks attached.

| Responsibility | Source module | What to inspect |
| --- | --- | --- |
| Agent driving | `packages/core/agent-loop` | Turns, steps, streaming, scheduling and termination |
| Agent API | `packages/core/agent` | Registry, lifecycle and interaction contract |
| Model boundary | `packages/llm/llm` | Prepared calls, routing and stream vocabulary |
| Provider implementation | `packages/llm/llm-deepseek` | Provider-specific request/response adaptation |
| Tool execution | `packages/core/tools` | Registry, policies, guards and dispatch |
| Prompt/context assembly | `packages/core/system-prompt` | Sections, current context and tool schemas |
| Session state | `packages/core/session` | Event history, message derivation and repair |
| Durable storage | `packages/session/session-persistence-jsonl` | Persistence backend, separate from the in-memory session |
| Context reduction | `packages/compaction/compaction-basic` | Pre-step policy and overflow recovery |

For filesystem and shell behavior, follow the consumers into `packages/fs/tool-fs` and `packages/shell/tool-bash`, then onward to their providers and sandbox policy. The [bash tool](https://github.com/deepseek-ai/deepseek-harness/blob/687f282e8625c6b8d11ff58211a90524be2e4317/packages/shell/tool-bash/src/index.ts#L1) explicitly separates its model-facing contract from process execution. Its behavior also depends on whether a job registry is composed: a timeout can lead to background work in a supported composition, rather than proving the process has stopped.

That last detail matters when interpreting screenshots of agents. “The tool returned” and “the underlying operation has finished” are different observations.

## Three decisions that change reliability

### 1. The event log and the model's working context are distinct

A chat transcript is often treated as a list to append to until the context window fills. DeepSeek Harness gives the session another role: recording the facts from which requests and other views can be reconstructed.

The request builder logs configuration changes, obtains `session.deriveMessages()`, and carries tool history separately. System-prompt updates have explicit handling for whether the routed adapter supports updates in history. Changes to tools or the admitted surface can start a new request series. These are concrete decisions about what a model sees and what can be replayed, not cosmetic conversation formatting.

The benefit is inspectability. When behavior changes, there is a place to ask which messages, schemas, route and context were admitted. The cost is coordination: a plugin that changes model-visible input has to participate in the recording and projection contract. A hidden mutation makes later reconstruction misleading, even if the live answer looked fine.

Compaction fits this design as policy. The [basic compaction plugin](https://github.com/deepseek-ai/deepseek-harness/blob/687f282e8625c6b8d11ff58211a90524be2e4317/packages/compaction/compaction-basic/src/index.ts#L137) hooks pre-step handling and structured request errors. For overflow recovery, it checks route information, cancellation and retry limits. Crucially, a retry requires the replacement surface to have advanced. Re-sending the same oversized context is not treated as recovery.

This doesn't make summaries lossless. A compacted conversation can still omit the detail a later decision needs. The architecture gives us boundaries to inspect; evaluation still has to ask which facts survived and whether the remaining context supports the next action.

### 2. Concurrent execution keeps ordered commitments

Tool calls are not all equivalent scheduling units. Some can safely overlap; others need to run alone. The [tool scheduler](https://github.com/deepseek-ai/deepseek-harness/blob/687f282e8625c6b8d11ff58211a90524be2e4317/packages/core/agent-loop/src/tool-calls.ts#L122) combines a bounded rolling pool with exclusive barriers. It also rechecks later calls before starting them, so a changed registry or policy can affect work that has not yet begun.

Results are finalized and appended in model order, even when the bodies finish out of order. This keeps the recorded conversation stable without forcing every independent read to wait for the previous read's entire execution.

There is a price. An early slow operation can hold up ordered result commitment. Cancellation also waits for started work to settle rather than pretending abandoned promises have disappeared. From these await points, a tool that ignores cancellation and never settles can delay teardown. That is a source-derived failure possibility, not a measured hang in a production session.

The registry provides another boundary: [`prepareExecution()`](https://github.com/deepseek-ai/deepseek-harness/blob/687f282e8625c6b8d11ff58211a90524be2e4317/packages/core/tools/src/index.ts#L1501) applies pre-execution policy and then checks live guards. A policy's permission decision is not equivalent to unconditional access; a guard can still deny dispatch. The actual tool body is reached through a separate execution path.

For comparisons between agents, “supports parallel tools” is too weak a description. Ask which calls overlap, where policy is enforced, what order observations enter history, and what cancellation waits for.

### 3. Resume repairs uncertainty instead of inventing success

The [resume path](https://github.com/deepseek-ai/deepseek-harness/blob/687f282e8625c6b8d11ff58211a90524be2e4317/packages/core/agent-loop/src/index.ts#L875) acquires write ownership before loading and preparing the session. It then appends semantic interruption closers to the physically valid log. Missing tool results, step endings and turn endings are handled at the agent/session layer, rather than being confused with storage recovery.

The most revealing part is in [`repair.ts`](https://github.com/deepseek-ai/deepseek-harness/blob/687f282e8625c6b8d11ff58211a90524be2e4317/packages/core/session/src/repair.ts#L14). It distinguishes `TOOL_NOT_STARTED` from `TOOL_OUTCOME_UNKNOWN`. The latter means a call was recorded as started but no completed result was durably recorded. The recovery message directs attention to the operation's semantics and external state before retrying a side effect.

This enables a coherent resumed conversation without claiming that the interrupted action failed. It costs the convenience of blindly continuing: somebody still has to resolve the uncertainty. A valid transcript does not provide exactly-once execution of an external operation.

That distinction is the architectural finding I would carry into any production agent review.

## The failure hidden between execution and observation

Imagine a shell tool updates a release marker in another system. The update succeeds. Before the result reaches durable session history, the agent process dies.

On restart, the log contains a started tool call and no result. Repeating the call might duplicate a release action. Treating it as successful might skip work that never happened. The model cannot infer the external truth from that log alone.

DeepSeek Harness's unknown-outcome repair preserves this ambiguity. The counterexample is to the claim that persistent sessions automatically make agents safe to resume. They preserve recorded knowledge; they cannot retroactively make a remote side effect and a local log append one transaction.

For a read-only inspection, retrying is usually straightforward. For a write, recovery may require reading the external system, an idempotency key, a transaction identifier or a human decision. Those mechanisms belong to the tool and its environment. Their absence cannot be fixed by a more confident assistant message.

There are other failure boundaries worth keeping separate. Cancellation during streaming retains safe interrupted assistant content when available, while failed attempts are recorded differently. A response cut off at the output-token ceiling doesn't simply authorize dispatching whatever partial tool call happened to arrive. A tool error can become a model-visible observation and allow another step; an unrecoverable request error can terminate the turn.

None of those paths proves that every task recovers correctly. They tell us where to inject failures and what evidence a test should demand.

## A framework for inspecting the next agent

The comparison framework I would reuse has six questions.

**Admission:** What enters the next request? Trace user instructions, repository guidance, dynamic context, tool output and schemas to the actual request boundary. Check whether source and authority remain distinguishable.

**Execution:** What can turn a proposed tool call into an effect? Find validation, policy, guards, provider dispatch and sandbox enforcement. A tool hidden from the prompt is not necessarily an operation denied at execution.

**Commitment:** When does an observation become authoritative state? Separate live UI output, accepted session events and durable storage. Inspect ordering when concurrent tools finish differently.

**Recovery:** What happens after interruption between each pair of those boundaries? Demand an explicit distinction between failure, success, not-started and unknown outcome. Identify the system that can resolve each uncertainty.

**Context continuity:** What survives pruning, compaction, model changes and resume? Trace the transformation and its recorded provenance. Check the facts needed for the next decision, rather than judging a summary by how fluent it sounds.

**Verification:** What establishes completion? Find actual test execution and its results. A driver stopping because the model emitted no more tool calls is a lifecycle event; it is not proof that the requested bug is fixed.

These questions apply to Claude Code, Codex, OpenCode and other runtimes without assuming their implementations match DeepSeek's. The next investigation can hold a task and model constant, vary one boundary, inject a failure and compare recorded effects. That would test a reliability claim. This article establishes the map for doing it.

If two agents use the same model but behave differently, which parts of their execution systems explain the difference?
