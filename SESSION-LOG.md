# Countdown to Date - Session Log

- **Category:** Productivity
- **Complexity tier:** Simple
- **Status:** In Progress — v1.0.0 code-complete, awaiting Isaac's sign-off
- **Description:** Countdown to events (birthdays, deadlines), built to share a data model with Event Planner.
- **Scope (v1):** Add named dates, live days/hours remaining, past-event handling; local-first PWA; integration-ready event schema + JSON export/import.

---

## Scaffold - 30 Aug 2026
Placeholder folder + docs created from the Ideas backlog. No build work yet.

## v1.0.0 build - 30 Oct 2026
First full build in one session (Default → effectively a focused Simple build).

**Build-standards flags agreed:** Simple tier; vanilla HTML/CSS/JS, no build step;
installable PWA (desktop + mobile web); local-first; copyright holder **Isaac A Gera** (default).

**What was built**
- `index.html` — single-file app: add/edit/delete countdowns (name, date, optional time,
  category, note); live "days to go" with Today / soon (≤7d) / passed states and an
  optional hours-minutes sub-line for timed events; sort (soonest/furthest/name/category)
  and filter (all/upcoming/past); live re-render every 60s; light/dark theme (follows OS,
  persists); export/import JSON (merge-by-id, never overwrite); toast feedback;
  confirm-on-delete; accessibility (ARIA labels, visible focus, aria-live, reduced-motion);
  Forjé footer (`.no-print`).
- PWA: `manifest.json`, `sw.js` (CACHE_NAME `countdown-v1.0.0`, core-atomic + optional
  best-effort caching, cache-first + navigate fallback), `icons/icon.svg` + `icons/icon-maskable.svg`.
- Docs: SPEC-requirements, SPEC-design, SPEC-tasks fleshed out; `userguide.html` and
  `overview.html` written; this log.

**Integration-by-design (the key decision)**
Countdown is the first writer of a shared event store so the future **Event Planner**
can reuse it with no migration:
- App-neutral localStorage key `forje_events_v1` (not app-specific).
- Shared event schema: `{id,title,date,allDay,category,notes,createdAt,updatedAt,source}`.
- Shared export envelope `{type:"forje-events",schemaVersion:1,...,events:[]}`.
- `EventStore` module kept isolated from the UI so it ports as a unit.
- Full contract documented in SPEC-design → "Event Planner integration".

**Known limitation / blocker**
- PNG icons (192/512 + maskable) not generated: `pip install Pillow` fails with an SSL
  cert error on the BT network (no PyPI). Manifest ships **SVG icons only** (valid +
  installable); `icons/generate-icons.py` left ready to run off-network to produce PNGs
  later. Not an install blocker — a nice-to-have for older Android launchers.

**Verified**
- Diagnostics clean on `index.html`, `manifest.json`, `sw.js`.
- NOT yet run in a live browser here (no Live Server in this environment).

**Awaiting Isaac (before marking Built)**
- Manual check via Live Server / hosted URL (not `file://`): add/edit/delete, theme,
  export→import round-trip, install + offline reload. Real-device install if targeting iPhone.
- Licence choice for a LICENSE file. Optional README.
- On sign-off: set Ideas.md row → `Built (Countdown to Date v1.0.0)`.

## v1.2.0 — prototype-driven redesign + port (30 Oct 2026)
Built in a `prototypes/` sandbox (data-isolated `cdproto_` keys, no SW), iterated with Isaac
over several rounds (v1.1.0 → v1.3.3-proto), then ported into the live app in one deliberate pass.

**Promoted to Quick Spec** at the start (multi-behaviour change touching the data model).

**What changed (v1.2.0)**
- Display renamed to **Countdown Timer** (header + title); folder/backlog id stays "Countdown to Date".
- **Mobile-first** redesign: phone-first CSS, 44px touch targets, safe-area insets; gradient
  banner header and a gradient **bottom navigation bar** on mobile; top pill tabs on ≥600px.
- **Tabbed views** — Upcoming (default, nearest first) / Past, with live count badges; **Add**
  is its own view (pill beside the tabs on desktop; centre of the bottom bar on mobile). The
  earlier floating + FAB was tried then removed; old upcoming/past filter retired (sort kept).
- **Recurring events** — none/weekly/monthly/yearly/**custom** (every N days/weeks/months/years);
  always counts to the next occurrence, stays under Upcoming, shows a ↻ chip. Schema gains
  optional `repeat`/`repeatEvery`/`repeatUnit` (additive; Event-Planner-safe).
- **Sort** reworded "Nearest / Furthest first"; "nearest" is direction-aware (fixes Past order).
- **Pagination** — 10/page with prev/next + "X / Y" beside sort; only when >1 page.
- **Personalise sheet** — 8 distinct colour palettes (re-spaced around the wheel) + light/dark.
- **Calendar app icon** replaces the stopwatch (header + PWA `icon.svg`/`icon-maskable.svg`).
- Primary button now reads **Save** (add + edit). Nav uses `aria-pressed` (a11y fix).

**Port chores done**
- Live `index.html` rewritten from the finalised prototype with live values: `forje_events_v1`,
  `cd_theme`, `cd_palette`, `APP_VERSION 1.2.0`, SW registration re-added, banner removed,
  export filename/app-name restored.
- `sw.js` CACHE_NAME `countdown-v1.0.0` → `countdown-v1.2.0`; `manifest.json` name → "Countdown Timer".
- Diagnostics clean on index.html / sw.js / manifest.json.

**Known limitation**
- PNG icons still not generated (corporate-network SSL blocks `pip install Pillow`). App installs
  fine on the SVG icons; `icons/generate-icons.py` left ready to regenerate the calendar PNGs off-network.

**Verified here:** diagnostics only. **Not verified here:** live browser / installed PWA.

**Awaiting Isaac (before Built):** deploy + real-device PWA install/offline test (SW cache bump
means a hard refresh / reopening the installed app to pick up the new build), feature spot-check,
licence choice. On sign-off → Ideas.md `Built (Countdown to Date v1.2.0)`.

## v1.2.1–v1.2.4 — deploy, PWA fixes, device test & sign-off (30 Oct 2026)
Shipped to GitHub and tested on a real iPhone; the device surfaced issues neither desktop
nor the emulator showed. Closed out as **Built**.

- **Repo + deploy:** new public repo `github.com/isaacgera/CountdownTimer` (one-app-per-repo,
  matching Splitzy); `main` pushed; GitHub Pages enabled (deploy from `main` / root). Live at
  `https://isaacgera.github.io/CountdownTimer/`. `prototypes/` excluded via `.gitignore`;
  `sample-events.json` kept; local `CountdownTimer_*.json` convenience copies git-ignored.
- **v1.2.1 / v1.2.2 — PWA manifest:** DevTools Manifest panel flagged failed SVG icon loads +
  "needs square icons" + missing screenshots. Generated square PNG icons (192/512 + maskable)
  and two screenshots with a **stdlib-only** script (`icons/make-png-icons.py`,
  `make-screenshots.py`) — no Pillow/network, which had been the blocker. Dropped the fussy
  SVGs from the manifest icon array (kept as favicon). Manifest panel clean.
- **v1.2.3 — real-device UI fixes (iPhone):** emoji/Unicode icons rendered as colour emoji on
  iOS; replaced header (palette/export/import), bottom-nav (Upcoming/Add/Past) and empty-state
  icons with matched **SVG line icons**. Fixed the header title wrapping (title + version pill
  on one row, tagline beneath) and enlarged the bottom nav with inline count badges.
- **v1.2.4 — title fit:** shortened the in-app title to **"Countdown"** (full name
  "Countdown Timer" retained for the browser tab / installed-app name) so it no longer
  truncates on a phone.
- **Licence:** MIT (`Copyright (c) 2026 Isaac A. Gera`).

**Verified:** Isaac installed and tested on iPhone via GitHub Pages; UI issues resolved.
**Status:** **Built (Countdown Timer v1.2.4)** — Ideas.md updated.

**Lesson for next time:** a Simple-tier tool stretched across many refinement rounds. Two
things would have trimmed it: (1) do the real-device PWA check *early* (emoji-vs-SVG and the
title wrap only ever showed on the actual iPhone, not desktop/emulator), and (2) treat icon/
PWA-manifest assets as a known up-front task rather than discovering the square-PNG + MIME
issues at deploy. Worth remembering before polishing the next small app.

## Follow-ups (optional, not blocking)
- Repo README.
- Higher-fidelity PWA icons/screenshots (current ones are simple stdlib-drawn placeholders).
