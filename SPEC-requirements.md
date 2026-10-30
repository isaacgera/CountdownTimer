# Countdown to Date — Requirements

- **Category:** Productivity
- **Complexity tier:** Simple
- **Status:** Built — v1.2.4, live on GitHub Pages, device-tested on iPhone
- **Version:** 1.2.4 (display name "Countdown" in-app / "Countdown Timer" full; folder/backlog id remains "Countdown to Date")
- **Stack:** Vanilla HTML/CSS/JS, single file + PWA plumbing (no build step)
- **Platforms:** Desktop web, mobile web, installable PWA
- **Data stance:** Local-first. All data in `localStorage`; nothing leaves the device.

## Summary
A simple, local-first app that counts down to the dates that matter — birthdays,
deadlines, trips, anniversaries. Add named events with a date (and optional time),
see the days remaining at a glance, and keep them sorted and filtered.

Built deliberately to share one event data model with the future **Event Planner**
app (Home / Medium tier), so countdowns created here can later be read, merged, or
promoted into Event Planner without a migration.

## User stories & acceptance criteria

### US-1 — Add a countdown
As a user, I want to add a named event with a date so I can track days remaining.
- Given a name and a date, when I submit, then the event is saved and appears in the list.
- Time is optional; without it the event is treated as **all-day**.
- A category can be chosen (default **General**); a short note is optional.
- Empty name or missing date is rejected with a gentle message (no silent failure).

### US-2 — See the countdown
As a user, I want to see how long until each event.
- Upcoming events show whole **days to go**; 1 day shows the singular "day to go".
- An event dated today shows **Today**.
- Past events show **N days ago** and are visually de-emphasised.
- Timed events additionally show an `Hh Mm left` sub-line.
- Colour status: today = green, within 7 days = amber ("soon"), past = muted.
  Colour is never the only signal (text labels carry the meaning too).

### US-3 — Edit / delete
As a user, I want to correct or remove an event.
- Editing loads the event into the form and saves in place (id and createdAt preserved).
- Deleting asks for confirmation first and cannot be undone (except via an imported backup).

### US-4 — Organise the list
As a user, I want to sort and filter so the list stays useful.
- Sort: soonest first (default), furthest first, by name, by category.
- Filter: all / upcoming only / past only.
- A live count shows "X of Y events".

### US-5 — Stay current without refresh
As a user, I want the counts to stay accurate while the app is open.
- The list re-renders at least once a minute so timed events tick down and all-day
  events roll over at midnight without a manual refresh.

### US-6 — Back up & restore (and interoperate)
As a user, I want to export my events and import them back.
- Export writes a JSON backup file.
- Import accepts that backup (or a plain events array) and **merges by id**
  (existing ids update, new ids add), reporting how many were added vs updated.
- The export format is the shared **`forje-events`** envelope (see design), so the
  same file can later be imported by Event Planner.

### US-7 — Install & work offline
As a user, I want to install it and use it offline.
- Installable PWA (manifest + service worker).
- Works offline after first load (cache-first; navigations fall back to the app shell).

### US-8 — Theme
As a user, I want light and dark themes.
- Respects the OS preference on first run; a manual toggle persists the choice.
- Contrast holds in both themes.

## Non-functional requirements
- **Accessibility:** semantic structure, keyboard operable, visible focus, ARIA labels
  on icon-only buttons, `aria-live` on the list/count, honours `prefers-reduced-motion`.
- **Data safety:** validate on input and import; tolerate corrupt/partial storage by
  starting empty rather than throwing; never overwrite on import (merge only).
- **No backend, no tracking, no accounts.**
- **Branding:** "Powered by Forjé" + copyright footer (holder: Isaac A Gera), excluded from print.

## Added in v1.2.0
- **Display rename** to "Countdown Timer" (header + title); folder/backlog id unchanged.
- **Mobile-first redesign:** phone-first layout, 44px touch targets, gradient banner header
  (top) and gradient bottom navigation bar (mobile), top pill tabs on wide screens.
- **Tabbed views:** Upcoming (default, nearest first) and Past as separate views with live
  count badges; Add is its own view (pill next to the tabs on desktop, centre of the bottom
  bar on mobile). The old upcoming/past filter dropdown is retired; sort dropdown retained.
- **Recurring events:** repeat = none / weekly / monthly / yearly / **custom** (every N
  days/weeks/months/years). A repeating event always counts to its next occurrence and stays
  under Upcoming; marked with a ↻ chip. Edit targets the base date.
- **Sort wording:** "Nearest first" (default) / "Furthest first"; "nearest" is direction-aware
  (closest-to-today in both Upcoming and Past).
- **Pagination:** 10 per page with prev/next + "page X of Y" beside the sort control; only
  shown when a list exceeds one page.
- **Theme personalisation:** 8 distinct colour palettes (Blue default, Teal, Green, Amber,
  Orange, Crimson, Purple, Magenta) plus a light/dark toggle, via a Personalise sheet
  (palette = hue, mode = light/dark). Persisted (`cd_palette`, `cd_theme`).
- **Calendar app icon** (replaces the original stopwatch) in the header and PWA icons.
- Primary form button reads **Save** in both add and edit modes.

Data-model note: `repeat`, and (for custom) `repeatEvery` + `repeatUnit`, are **additive
optional fields** on the shared schema — older events and Event Planner stay compatible
(absent = "does not repeat").

## Out of scope (v1.2)
- Notifications / reminders (needs OS permissions; iOS-PWA-sensitive).
- Multiple devices / sync (local-first by design; backup file is the transfer path).
- The full Event Planner feature set (guest lists, to-dos, food, venue) — that is the
  separate Event Planner app this one is designed to feed into.

## Integration requirement (Event Planner)
This is a first-class requirement, not an afterthought:
- Countdown events MUST be stored in a shared, app-neutral schema and storage key so
  Event Planner can adopt the same store.
- The export/backup MUST use a shared envelope type (`forje-events`) that Event Planner
  will recognise.
- Each event records its `source` ("countdown") so a future merged app can tell where
  it originated.
See `SPEC-design.md` → "Event Planner integration" for the contract.
