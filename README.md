# Cockpit

One ranked view of *what needs you right now* — pulled from all your scattered
sources into a single, self-contained HTML dashboard.

You live across a dozen tools: mail, chat, calendar, tasks, git, billing,
analytics. Gathering the state of your day from all of them is a daily tax. A
**cockpit** does the aggregation for you and renders one ranked *attention
queue* — the answer to "what demands me, in priority order?".

It's **data-driven**: the presentation is a frozen template; each brief is just
a small JSON spec. An agent (Claude or otherwise) authors the spec; a dumb
renderer turns it into the page. That separation is the whole idea — a cockpit
is portable *data*, not bespoke HTML.

![Morning briefing](screenshots/morning-briefing.png)

## Install as a skill

This repo is a [skills.sh](https://www.skills.sh) skill. Add it to your AI agent
(Claude Code, Cursor, …) with:

```bash
npx skills add Urriel/cockpit
```

That installs the [`cockpit`](skills/cockpit/) skill — invoke it with `/cockpit`.
It aggregates whatever sources you've wired (CLIs, MCP servers, local files),
ranks them by **urgency**, **convergence** (an item hitting multiple surfaces at
once is the real priority) and **stakes**, then renders the brief. It never
sends, moves, or writes anything.

## Quick start (standalone)

No dependencies — just Python 3.

```bash
python3 skills/cockpit/render.py skills/cockpit/gallery/morning-briefing.json
open skills/cockpit/gallery/morning-briefing.html        # macOS (xdg-open on Linux)
```

That inlines the spec into `template.html` and writes a single `.html` file you
can open anywhere — including `file://` and mobile, because the data is embedded
rather than fetched.

## The spec

A cockpit is an **ordered array of typed cards** plus an optional rail:

```jsonc
{
  "date": "Tuesday, June 30 2026",
  "time": "08:02",
  "sources": "Stripe · PostHog · Linear · Discord · Calendar",
  "footer": "Read-only, polling.",
  "cards": [ /* rendered top → bottom in the main column */ ],
  "rail":  [ "one-liners for the right rail" ],   // omit → main goes full-width
  "railTitle": "✅ Done today"
}
```

Every card has a `type` and an optional `accent`
(`red | amber | blue | violet | green | gray`):

| Type | Shape | For |
|---|---|---|
| `hero` | `title, badge?, headline, sub?, chips?` | the single most important thing |
| `metric` | `title, items:[{label, value, delta?, deltaKind?, sub?}]` | overnight numbers |
| `list` | `title, items:[{who?, what, sub?, chips?, tags?}]` | replies, tasks, bugs |
| `feed` | `title, items:[{what, sub?, meta?}]` | timestamped activity (commits, mentions) |
| `note` | `summary, bodyHtml, collapsed?, footnote?` | folded low-priority noise |

`deltaKind ∈ up | down | warn | flat` (you choose the meaning — `up` is green,
`down` red, `warn` amber). List urgency `tag.kind ∈ late | today | high | med | low`.

The full schema lives in the comment block inside
[`skills/cockpit/template.html`](skills/cockpit/template.html) and in
[`skills/cockpit/SKILL.md`](skills/cockpit/SKILL.md).

## Gallery

Ready-to-render sample cockpits — copy one and swap in your data:

| Sample | Exercises |
|---|---|
| [`morning-briefing.json`](skills/cockpit/gallery/morning-briefing.json) | hero · metric · two lists · note · rail |
| [`build-in-public.json`](skills/cockpit/gallery/build-in-public.json) | hero · metric · feed · list · **no rail (full-width)** |

![Build in public](screenshots/build-in-public.png)

## Repo layout

```
skills/cockpit/        the installable skill
  SKILL.md             read-only ops-brief instructions (rank by urgency/convergence/stakes)
  template.html        frozen CSS + vanilla-JS renderer (data inlined for file:// + mobile)
  render.py            zero-dependency spec → standalone HTML
  gallery/             sample cockpits
skills.sh.json         skills.sh manifest
screenshots/           gallery renders (for this README)
```

## How it works

- **Frozen presentation, authored data.** `template.html` holds the CSS + a
  small vanilla-JS renderer and a single `<script type="application/json">`
  data island. `render.py` replaces the island's contents with your spec.
- **Inlined, not fetched.** The spec is embedded in the output so it renders
  offline and on mobile, where fetching a sibling `.json` would be CORS-blocked.
- **Dark, glanceable, accessible.** Six semantic accent colors, WCAG-AA text
  contrast, a reduced-motion-safe entrance, responsive down to a single column.

## License

[MIT](LICENSE).
