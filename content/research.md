---
title: "Research"
description: "Four research programs: memory for AI agents, reliable agent systems, AI × security, and AI-native software engineering."
url: "/research/"
showToc: true
comments: false
---

Posts are chapters. These are the programs they belong to.

The through-line lives on [Projects](/projects/): memory, tools, deterministic constraints, evaluation, observability, security, and human control.

## 1 · Memory for AI agents

Memori, architectures, retrieval, decay, identity, evaluation.

- [Forging AI’s lasting memory](/posts/2024-01-01-ai-memory/)
- [Memori architecture](/posts/2026-03-24-memori-architecture/)
- [Memori recursive design](/posts/2026-04-10-memori-recursive-design/)
- Talk: [Memory is the Agent](/speaking/)
- Artifact: [Memori](/projects/#memori--flagship)
- Artifact: [Chronicle](/projects/#also-original)

## 2 · Reliable agent systems

Luffy, tool design, control planes, observability, failure modes.

- [Designing CLI tools for AI agents](/posts/2026-02-28-designing-cli-tools-for-ai-agents/)
- [Hard constraints belong in code](/posts/2026-03-23-hard-constraints-belong-in-code/)
- [Building Luffy](/posts/2026-07-31-luffy-pr-review-agent/)
- [Vital Few](/posts/2026-09-20-vital-few/)
- Artifact: [Luffy](/projects/#luffy)
- Artifact: [Vital Few](/projects/#vital-few)
- Artifact: [Idea Generator](/projects/#also-original)

## 3 · AI × security

Agent attacks, fraud, identity, social engineering, behavioral security.

The artifacts so far are detection PRs.

- [Potential Proxy Execution Via SetupUGC](https://github.com/SigmaHQ/sigma/issues/6153) ([rule](https://github.com/SigmaHQ/sigma/pull/6152)). `setupugc.exe` as a signed LOLBin on Windows 10/11 and Server 2025.
- [Exclude Kea DHCP from CAP_NET_RAW](https://github.com/elastic/detection-rules/pull/6468). The building block was firing on a legitimate `/usr/sbin/kea-dhcp4`.
- [AWS discard_regex values with spaces](https://github.com/wazuh/wazuh/pull/37849). Unquoted Security Hub values split as extra arguments.

## 4 · AI-native software engineering

Coding agents, architecture, productivity, staff+ engineering, evaluation.

- [The AI-augmented developer playbook](/posts/2026-01-26-ai-augmented-developer-playbook/)
- [The Staff+ operating model](/posts/2026-08-30-the-staff-plus-operating-model/)
- [Listen to this post](/posts/2026-08-30-adding-text-to-speech-to-a-hugo-blog/)
- Artifact: [Free Model Eval](/projects/#also-original)
- Artifact: [Sim Bangalore](/projects/#also-original)
