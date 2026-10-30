# Countdown to Date — Tasks

Display name: **Countdown** (in-app) / **Countdown Timer** (full). Current version **1.2.4** — Built, live on GitHub Pages (github.com/isaacgera/CountdownTimer).

## Done — v1.0.0 (30 Oct 2026)
- [x] Requirements, design, build v1 — add/edit/delete, live countdown, sort/filter,
      export/import, light/dark, accessibility, Forjé footer.
- [x] Shared `EventStore` (`forje_events_v1`, `forje-events` envelope).
- [x] PWA plumbing — `manifest.json`, `sw.js`, SVG icons.

## Done — v1.2.0 (30 Oct 2026, prototyped then ported)
- [x] Prototyped mobile-first in `prototypes/` (v1.1.0 → v1.3.3-proto), data-isolated.
- [x] Renamed display name to "Countdown Timer" (folder/backlog id unchanged).
- [x] Mobile-first redesign: gradient banner header + gradient bottom nav (mobile),
      top pill tabs (desktop), 44px touch targets, safe-area insets.
- [x] Tabbed views: Upcoming (default, nearest first) / Past / Add, live count badges.
- [x] Add = own view (desktop pill + mobile bottom-bar centre); FAB removed; old
      upcoming/past filter retired; sort kept.
- [x] Recurring events: none/weekly/monthly/yearly/custom (every N units), next-occurrence
      rolling, ↻ chip; additive schema fields (`repeat`, `repeatEvery`, `repeatUnit`).
- [x] Sort reworded "Nearest/Furthest first", direction-aware for Past.
- [x] Pagination — 10/page, prev/next + "X / Y" beside sort, shown only when >1 page.
- [x] Theme personalisation — 8 distinct palettes + light/dark via a Personalise sheet
      (`cd_palette`, `cd_theme`).
- [x] Calendar app icon (header + `icons/icon.svg` + `icons/icon-maskable.svg`).
- [x] Primary button reads "Save" (add + edit).
- [x] Accessibility fix: nav uses `aria-pressed` (valid toggle semantics).
- [x] Ported prototype → live `index.html` (live keys + SW registration).
- [x] `sw.js` CACHE_NAME → `countdown-v1.2.0`; `manifest.json` name → "Countdown Timer".
- [x] Diagnostics clean on index.html / sw.js / manifest.json.
- [x] Docs synced (SPEC trilogy, SESSION-LOG, userguide, overview); Ideas row updated.

## Blocked / deferred
- [ ] PNG icons (192/512 + maskable) — pip install Pillow blocked by corporate-network SSL
      (no PyPI). App installs on the SVG icons. `icons/generate-icons.py` ready to run
      off-network; regenerate for the calendar mark when possible.

## Sign-off — done (v1.2.1–v1.2.4, post-deploy)
- [x] Pushed to GitHub (github.com/isaacgera/CountdownTimer) + GitHub Pages enabled.
- [x] PWA manifest fixes: square PNG icons generated (stdlib, no Pillow) + screenshots;
      Manifest panel clean (v1.2.1/v1.2.2).
- [x] Real-device (iPhone) test surfaced mobile-only issues; fixed in v1.2.3:
      emoji/Unicode icons → matched SVG line icons (header, bottom-nav, empty states),
      non-wrapping title row, larger bottom-nav + inline count badges.
- [x] v1.2.4 — shortened in-app title to "Countdown" so it no longer truncates on mobile.
- [x] Licence — MIT LICENSE (Copyright (c) 2026 Isaac A. Gera).
- [x] Ideas.md status → `Built (Countdown Timer v1.2.4)`.

## Later (v1.3+ candidates)
- [ ] Optional README for the repo.
- [ ] Replace placeholder PWA icons/screenshots with higher-fidelity renders off-network.
- [ ] Notifications / reminders (OS permissions; iOS-PWA-sensitive).
- [ ] When Event Planner is built: lift `EventStore`, extend the shared record.
