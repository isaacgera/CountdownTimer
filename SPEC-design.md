# Countdown to Date — Design

- **Category:** Productivity | **Tier:** Simple | **Version:** 1.2.4 (display name "Countdown")

## Stack choice & justification
Vanilla HTML/CSS/JS in a single `index.html`, plus a manifest, service worker and icons.

- **Why vanilla:** the app is a short form + a list + date maths. A framework would add a
  build step and Windows tooling for no real gain. This matches the Simple-tier intuition
  in the backlog and the family's no-build "just open it / Live Server" workflow.
- **PWA:** installable + offline via a cache-first service worker — Isaac's usual target.
- **Trade-off noted:** no component framework means manual DOM updates, which is fine at
  this size (one list render function). If Event Planner grows complex, *it* can choose a
  richer stack and still consume this app's data via the shared schema below.

## Architecture / module layout
Single file, three logical layers kept cleanly separated inside one `<script>`:

1. **`EventStore`** — the shared data layer (CRUD + export/import over `localStorage`).
   Deliberately self-contained and app-neutral so it can be lifted wholesale into Event
   Planner. This is the integration seam.
2. **Countdown maths** — pure functions: `targetDate`, `daysUntil`, `breakdown`,
   `statusClass`, `fmtDate`. No DOM, easy to reason about and reuse.
3. **UI** — form handling, `render()`, sort/filter, theme, export/import wiring, SW
   registration. The only layer that touches the DOM.

## Data model — the shared event schema (v1)
One record per event. This schema is the contract shared with Event Planner.

```
{
  id:         string   // unique, stable — "ev_<base36 time>_<rand>"
  title:      string   // <= 80 chars
  date:       string   // ISO 8601 — "YYYY-MM-DD" when all-day, full ISO when timed
  allDay:     boolean
  category:   string   // General | Birthday | Deadline | Holiday | Anniversary | Trip | Event | ...
  repeat:     string   // none | weekly | monthly | yearly | custom   (v1.2, optional; absent = none)
  repeatEvery:number   // custom only — N (1..999)                     (v1.2, optional)
  repeatUnit: string   // custom only — day | week | month | year      (v1.2, optional)
  notes:      string   // <= 140 chars
  createdAt:  string   // ISO timestamp
  updatedAt:  string   // ISO timestamp
  source:     string   // owning app — "countdown" here
}
```

The `repeat` / `repeatEvery` / `repeatUnit` fields are **additive and optional** (added in
v1.2.0). Records without them read as non-repeating, so pre-v1.2 data and Event Planner
remain compatible. Recurrence is computed at read time (next-occurrence rolling) — the stored
`date` is always the original/base date, never mutated.

## v1.2.0 UI architecture notes
- **Two colour axes:** MODE (light/dark via `data-theme`) and PALETTE (hue via `--primary`/
  `--primary-strong`/`--accent` set from a named preset). The banner + bottom-nav gradient
  (`--banner-grad`) derives from the palette, so chrome re-tints on palette change.
- **View model:** a single list panel renders either Upcoming or Past (filtered by `isPast`),
  plus an Add/Edit panel. Nav is a bottom bar on mobile (`< 600px`) and a top pill row on
  wider screens; both drive the same `showList`/`showAdd` logic. Buttons use `aria-pressed`.
- **Recurrence:** `occurrence()` rolls the base date forward by the repeat step until it's
  not in the past; repeating events never fall into "Past".
- **Pagination:** `PAGE_SIZE = 10`, `currentPage` state; pager shown only when `totalPages > 1`.
- **Sort direction** is view-aware so "Nearest first" means closest-to-today in both lists.

- **Storage key:** `forje_events_v1` — intentionally *not* app-specific. Event Planner,
  when built, can read/write the same key and immediately see these events.
- **Validation:** a record needs at least a string `id`, `title` and `date`. Anything
  else is dropped on load so corrupt storage degrades to "empty", never a crash.
- **All-day vs timed:** all-day events compare on calendar day (so they read "Today"
  for the whole day); timed events compare on the exact instant and also show an
  `Hh Mm` sub-line.

## Export / import envelope
The backup file is a portable envelope, not a bare array:

```
{
  type:          "forje-events",   // recognised by Countdown AND Event Planner
  schemaVersion: 1,
  exportedAt:    ISO timestamp,
  app:           "Countdown to Date",
  appVersion:    "1.0.0",
  events:        [ ...event records ]
}
```

- **Import** accepts either this envelope or a plain `events` array, and **merges by id**
  (update existing, add new) — never a destructive overwrite. Returns `{added, updated, total}`.
- Because the envelope `type` and the event schema are shared, an export from Countdown
  imports cleanly into Event Planner (and vice-versa) once Event Planner exists.

## PWA / offline approach
- `manifest.json`: standalone display, brand `theme_color` `#5b8def`, SVG icons
  (`icon.svg` any + `icon-maskable.svg` maskable).
- `sw.js`: `CACHE_NAME = countdown-v1.0.0`. **Core** assets cached atomically on install
  (app shell + manifest + primary SVG icon); **optional** assets (maskable SVG, PNGs,
  user guide) cached best-effort with `.catch()` so a missing optional asset can never
  fail the install or break offline. Fetch is cache-first with a navigate fallback to
  `index.html`. Bump `CACHE_NAME` on every release.

### Icons — known limitation (this build)
- PNG icons (192/512 + maskable) could **not** be generated in this session: installing
  Pillow failed with an SSL certificate error on the BT corporate network (no PyPI access).
- Mitigation: the manifest ships **SVG icons only**, which are valid and installable in
  modern browsers and installed PWAs. `icons/generate-icons.py` (a Pillow script that
  mirrors `icon.svg`) is included so the PNGs can be produced later off-network, then
  re-added to the manifest. PNGs are a nice-to-have for older Android launchers, not an
  install blocker.

## Theming & visual design
- Design tokens as CSS custom properties; dark theme via `:root[data-theme="dark"]`.
- First run follows `prefers-color-scheme`; the manual toggle persists to `cd_theme`.
- Quick (140–200ms) ease-out transitions; hover lift + visible focus rings; card
  entrance animation. All motion collapses under `prefers-reduced-motion`.
- Status colour (today/soon/past) is always paired with a text label — never colour alone.

## Event Planner integration — the contract
Countdown to Date is intentionally the **first writer** of the shared event store.
When Event Planner is built (Home / Medium), it should:

1. **Reuse `EventStore` verbatim** (same `forje_events_v1` key, same schema) — it can lift
   the module from this file. Countdown's events appear automatically.
2. **Extend, don't fork, the schema** — Event Planner adds its richer fields (guests,
   to-dos, food, venue) as *additional* optional properties on the same record, keyed off
   the same `id`. Countdown ignores unknown fields; Event Planner reads them. This keeps
   both apps forward/backward compatible on one record.
3. **Share the `forje-events` envelope** for export/import so a backup moves between the
   two apps without conversion.
4. **Use `source`** to distinguish origin ("countdown" vs "event-planner") for display or
   filtering in a future merged view.

Net effect: an event you start as a countdown here can later be opened in Event Planner
and fleshed out into a full plan — no migration, no data loss, no duplicate entry.

### Design decisions that enable this (and why)
- **App-neutral storage key** (`forje_events_v1`, not `countdown_events`): the single
  biggest enabler — two apps, one store.
- **`EventStore` isolated from the UI:** so it ports as a unit.
- **Envelope with a `type` discriminator:** lets any sibling app detect "this is our data".
- **Merge-by-id import, never overwrite:** safe to import the same data into either app.
- **`source` + extensible records:** supports a future unified app without a schema break.
