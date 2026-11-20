---
title: "An online migration can quietly lose its rollback"
description: "A copy can match at cutover and return stale data on rollback. Define how long the old path stays safe, then prove it with a write."
date: 2026-11-20T20:10:00+05:30
tags: [Reliability, Data Engineering, Distributed Systems]
categories: [Engineering]
cover:
  image: "/images/uploads/migration-rollback.webp"
  alt: "Two record histories start together and split after writes switch."
---

The first write that reaches only the new store changes your rollback procedure. Reverting the application might still work at the deployment layer. If the old code reads the old store, the user can get an answer with yesterday's state.

That is an easy trap to miss in a migration plan that says “compare, switch, roll back if needed.” Put an expiration condition on the rollback. You want to know which write ends it, who can stop that write path, and what recovery looks like after it happens.

## Rehearse a rollback after the write

Stripe's online migration write-up describes moving subscription data for a system with hundreds of millions of subscription objects. The sequence backs up the engineering logic. Start writing to both representations and backfill, compare reads before switching them, change the write path, and then clean up the old representation. Moving reads and moving writes deserve separate decisions. [Stripe Engineering, Online migrations at scale](https://stripe.com/blog/online-migrations)

Here is a small example. A subscription starts at revision 1. By the time the copy finishes, both stores hold revision 2. A shadow comparison agrees, so the new read path takes over. The next write changes the new store to revision 3 only. Switch reads back and the user gets revision 2. Both stores can be perfectly healthy throughout.

{{< figure src="/downloads/software-reliability/migration-revisions.webp" link="/downloads/software-reliability/migration-revisions.webp" alt="Both stores hold revision 2 at cutover. After a new-store-only write, the new store has revision 3 while a rollback still reads revision 2 from the old store." caption="Illustrative record history. Parity at the read cutover expires when the old store stops receiving writes." width="1200" height="675" >}}

A useful rollback rehearsal writes a new value after the cutover, restores the old read path, and verifies that the latest acknowledged value is still visible. Include deletion, retry and delayed update cases as well. A revision check matters when a backfill and a live write race. If the copy can overwrite a newer value, agreement measured before that interleaving says little about the eventual result.

Amazon's rollback guide makes the same transition problem concrete for mixed versions. Deploy code that can read both forms before enabling writes in the new form. Test forward and backward transitions under mixed versions. After new-format state exists, recovery must land on a version that can read it or explicitly repair the data. [AWS Builders' Library, Ensuring rollback safety](https://aws.amazon.com/builders-library/ensuring-rollback-safety-during-deployments/)

## Pausing the copy is a different control

An online migration can fail before there is anything to roll back. GitHub reported a routine migration that ran for hours before rising customer demand and migration load saturated database connections on May 4, 2026. GitHub paused the migration. At peak, about 1.3% of requests returned 5xx responses, with an average of about 0.46% during the incident. That is an availability problem during the copy. It tells you little about whether the eventual data cutover is safe. [GitHub's May 2026 availability report](https://github.blog/news-insights/company-news/github-availability-report-may-2026/)

I'd put two decisions in the runbook. The first is a pause decision for background work, based on production latency, connections and replication lag. The second is the cutover decision, based on read comparisons and a rollback test that includes post-cutover writes. Keep the old representation current through the rollback window with a replication mechanism whose lag and failures you can see. Give the overlap an end condition, since it carries extra work and creates its own failure modes.

Once writes stop reaching the old representation, change the runbook from “switch reads back” to a recovery procedure you have actually rehearsed. That line belongs next to the write flag.

[Download the version-history example and figure script](/downloads/software-reliability/experiment.py).
