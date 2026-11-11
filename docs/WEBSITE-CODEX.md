# Website design codex

Reviewed 12 November 2026. This is a working design reference, not a claim that these choices improve conversion by a measured amount.

## Purpose

An engineer’s workshop: introduce Archit, expose useful software and explain the decisions behind it. Optimize for understanding, inspection and relevant conversations. Keep Hugo, PaperMod and static delivery; spend effort on content hierarchy before adding infrastructure.

## Reference observations

| Reference | Observed pattern | Application and trade-off |
| --- | --- | --- |
| [Mitchell Hashimoto](https://mitchellh.com/) | Plain biography linked to specific projects | State what was built; avoid prestige language. A new visitor still needs a route into the work. |
| [Julia Evans](https://jvns.ca/) and [projects](https://jvns.ca/projects/) | Topic indexes; projects explain what a tool does and why it was built | Offer questions and subjects as entry points. Keep the compact date-based archive too. |
| [Brandur](https://brandur.org/) and [technical fragment](https://brandur.org/fragments/codex-tui-tiny-features) | Distinct article formats, restrained type hierarchy, narrow reading column, small metadata | Separate short notes from reference guides without creating empty sections. Avoid copying the large photographic homepage or wide metadata gutter. |
| [Andrej Karpathy](https://karpathy.ai/) | Personal introduction tied directly to work and public resources | Lead with a name and concrete work. Do not manufacture a career timeline or metrics. |
| [Simon Willison](https://simonwillison.net/) | Tools, releases, notes and articles are visible together | Make experimentation welcome; do not invent fresh activity or promise a publishing cadence. |
| [Maggie Appleton](https://maggieappleton.com/) | Distinct content forms and explanatory visuals | Use diagrams that explain an idea. Do not add decoration that competes with reading. |
| [Werner Vogels](https://www.allthingsdistributed.com/) | Selected work before recent writing; explicit technical focus | Curate useful work before chronology. A personal site need not imitate a corporate landing page. |
| [Dan Luu](https://danluu.com/), [matklad](https://matklad.github.io/), [antirez](https://antirez.com/) | Direct access to a substantial writing archive | Preserve plain links, dates and fast loading. Their established reputations are not evidence that an unfamiliar visitor needs no introduction. |

Reference homepages were fetched. Native Brave inspection included Karpathy’s biography, Brandur’s homepage and article, Julia’s homepage and project collection, and Werner’s homepage. The remaining sites informed content structure; their full interaction paths were not tested.

## Highest-value rules

1. Name → concrete work → selected questions → recent writing. Make the introduction short enough for projects to appear early.
2. Explain each project in ordinary language: problem, behavior, source and a useful next step. Keep implementation details for readers who choose to go deeper.
3. Use a diagram, trace or screenshot only when it teaches something. Label architecture sketches; never present invented terminal output as a real run.
4. Write about what happened. Preserve dates, source links, failures and limits. Avoid universal claims, repeated slogans and defensive disclaimers on every paragraph.
5. Keep one accent, a restrained heading font and consistent spacing. Use readable contrast in both themes. Reserve borders for grouping or separation.
6. Maintain narrow article measures, visible links and headings, keyboard focus, skip navigation and reduced-motion support. Responsive layouts must preserve reading order.
7. Give readers a next step: source, related explanation, topic index, RSS or contact. No extra signup system is needed.
8. Ship small changes. Build locally, check generated links/anchors, inspect desktop and narrow layouts, merge the PR, wait for both Pages stages, then inspect production.

## Options and decision

Compared two project treatments in local Brave: two equal columns with diagrams above the copy, and stacked rows with small diagrams to the left. Selected columns because both projects remain easy to compare and the diagram labels are more readable. Below 600px, stack them in document order. Removed the previous category slogan and numbered cards; Archit’s name and actual work now carry the introduction.

These are design judgments, not conversion-test results. If visitors struggle to choose a project or article, improve labels and evidence before adding more sections.

## Verification checklist

- `hugo --gc --minify -d /tmp/hugo-verify`
- `bash scripts/check-homepage.sh`
- `python3 scripts/check-site.py /tmp/hugo-verify`
- Inspect home → project → article, topic index, Speaking → recording and Contact.
- Check both themes, a narrow viewport, keyboard focus and page-end navigation.
- Verify deployed HTML and image/CSS assets after both Actions stages succeed; a green build alone is not proof of live delivery.
