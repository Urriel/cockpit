---
name: cockpit
description: >
  Read-only personal operations brief. Use when the user says `/cockpit`,
  "daily brief", "what needs me today", or wants one ranked view of what
  demands attention across their sources (mail, chat, calendar, tasks, git,
  analytics, ...). Aggregates many surfaces into a single ranked "attention
  queue" rendered as a self-contained HTML dashboard. Read-only — never sends,
  moves, or writes anything.
allowed-tools: Bash Read Grep Glob
---

# Cockpit — Personal Ops Brief

A cockpit does **deterministic aggregation** across your attention surfaces and
produces **one ranked brief** — the answer to *"what needs me right now?"*. Code
and queries do the ETL; the agent does the ranking and synthesis. It composes
whatever sources you already have wired — it does not build connectors.

## When to use
- `/cockpit`, "daily brief", "what needs me", "where am I right now"
- Morning kickoff, or any on-demand pulse during the day.

## Sources (compose, don't build)
A cockpit reads from whatever you can already query. Common surfaces:

| Surface | Example signal |
|---|---|
| Mail | unread needing a reply |
| Chat (Slack/Discord/...) | DMs + mentions awaiting reply |
| Calendar | invites, scheduling commitments, hard deadlines |
| Tasks | overdue + due-today |
| Git / issues | open PRs, assigned issues, failing CI |
| Analytics / billing | revenue, signups, churn, anomalies |

Wire these via local CLIs, MCP servers, or files you already keep. The skill is
the **cross-surface read** that sits above them.

## The attention item
Each surfaced thing carries: `who` · `what` · `why it matters` · `urgency` ·
`suggested action` · `provenance`. You hold this while ranking; the rendered
card shows the parts that matter.

## Ranking heuristic
1. **Urgency** — overdue > due-today > due-this-week > undated.
2. **Convergence** — an item surfacing on N surfaces at once is the real
   priority. Detect and call it out explicitly. *This is the thing no single
   app shows.*
3. **Stakes** — client / revenue / brand / blocking-a-teammate outranks
   internal/FYI.
4. **Demote noise** — newsletters, promos, receipts, bot notifications → a
   folded "filtered" note, never the queue. Flag only security-relevant
   exceptions (e.g. an unexpected password-reset mail).

## Output format — data-driven HTML dashboard
Presentation (CSS + a small JS renderer) is frozen in `template.html`. **Each
run you only author a small JSON spec** — you never hand-write dashboard HTML.

Per run:
1. Write the day's spec to a JSON file (schema below).
2. Build the self-contained HTML by injecting the spec into the template's
   `<script type="application/json" id="cockpit-data">` island. The data is
   **inlined** (not `fetch()`-ed) so the result works on `file://` and mobile
   webviews, where a sibling-`.json` fetch would be CORS-blocked.
   ```bash
   python3 render.py brief.json brief.html   # or: python3 render.py brief.json
   ```
3. `open` the HTML (or report the path). Echo a 3–5 line text summary in chat;
   the HTML is the deliverable.

### JSON schema
A cockpit is an **ordered array of typed cards** plus an optional rail. The
renderer walks `cards` top→bottom in the main column; `rail` fills the right
`<aside>`.
```
date, time, sources, footer : strings (footer/headline/sub/what/bodyHtml may contain inline HTML)
cards : [ Card ]          // rendered in array order in the main column
rail  : [ str ]           // right-rail one-liners; omit / [] → no rail, main goes full-width
railTitle? : string       // rail heading (default "✅ Done today")

Card = one of (discriminated by .type); every card takes an optional
       accent ∈ red | amber | blue | violet | green | gray  (default gray):
  hero   { type, accent?, title, badge?, headline, sub?, chips?:[str] }
  metric { type, accent?, title, badge?, items:[{ label, value, delta?, deltaKind?, sub? }] }
  list   { type, accent?, title, badge?, items:[{ who?, what, sub?, chips?:[str], tags?:[{label,kind}] }] }
  feed   { type, accent?, title, badge?, items:[{ what, sub?, meta? }] }
  note   { type, accent?, summary, bodyHtml, collapsed?, open?, footnote? }

deltaKind ∈ up | down | warn | flat   (author picks meaning; up=green, down=red, warn=amber, flat=muted)
tag.kind  ∈ late | today | high | med | low
```
On mobile the rail collapses above the feed; with no rail the main column is full-width.

### Composing a brief
A typical morning brief composes: a **hero** (the one priority), a **metric**
row (overnight numbers), one or more **list** cards (replies, tasks, bugs), a
collapsed **note** (filtered noise + any security exception), and a **rail** of
what got done. On a same-day re-run, **move** resolved items into `rail` rather
than dropping them — the running record of the day.

See `gallery/` for ready-to-render samples (`morning-briefing.json`,
`build-in-public.json`).

## Boundaries
Read-only. No mail sent or moved, no task created or status changed, no message
posted. Write-back is out of scope by design — a cockpit tells you what needs
you; you act in the source.
