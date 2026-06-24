# Atlas USA — US Account Penetration Map

A single self-contained `index.html` that renders an interactive `geoAlbersUsa` map of the
50 states + DC and tracks retail/distribution account penetration, read **live and
read-only** from a Google Sheet. No framework, no bundler, no CDN — d3 v7,
topojson-client, and the us-atlas `states-10m` TopoJSON are all inlined.

## Use it

Open `index.html` in any browser (or host it — see Deploy). On first load it shows **sample
data** so the map + heat colors render immediately. Click **⚙ Connect Google Sheet** to wire
your own sheet; the settings (Sheet ID + tab names) are saved in `localStorage`. **↻ Refresh**
re-pulls the sheet.

## Connect your Google Sheet

1. **Share it read-only:** in Google Sheets → *Share* → "Anyone with the link · **Viewer**"
   (or *File → Share → Publish to web*). No API key or OAuth is needed — the app reads the
   sheet through Google's CSV export:
   `https://docs.google.com/spreadsheets/d/<ID>/gviz/tq?tqx=out:csv&sheet=<Tab>`
2. Paste the sheet **URL or ID** into the settings dialog, set the two tab names, **Save & load**.

The app never writes back — you edit accounts in the Sheet, the map reflects them on Refresh.

### `Accounts` tab columns (header casing/spacing/order are tolerant)

`Name, Address, City, State, Type, GPen, Stundenglass, [Lat], [Lng], [Notes]`

- **State** — 2-letter (`TX`) or full name (`Texas`). If blank, it's derived from a trailing
  state/ZIP in **Address**. Rows that still can't be placed are listed (see the status line →
  "N unplaced").
- **Type** — Smoke Shop / Dispensary / Lounge / Distributor (matched loosely: "vape" →
  Smoke Shop, "disp" → Dispensary, "hookah" → Lounge, "wholesale/distro" → Distributor).
- **GPen, Stundenglass** — booleans: `TRUE/FALSE`, `yes/no`, `1/0`, `x`, `✓`.
- **Lat/Lng** — optional. If present, accounts also drop point pins; absent → aggregate by
  state only (no geocoding).

### `Totals` tab (penetration denominators)

`State, SmokeShops, Dispensaries, Lounges, [Distributors]` — the size of the universe per
state. Penetration % = our accounts of that type ÷ that total. Missing/zero totals show
`—` (no divide-by-zero) and render grey on the map in % mode.

## Features

- **Brand toggle** (All / GPen / Stündenglass) filters every count, color, and %.
- **Color-by toggle**: Accounts (count) or % Penetration — legend updates to match.
- **Type filter** (All / Smoke / Disp / Lounge / Distro) — respected by colors, stats, panel.
- **Heat map** red→yellow→green; thresholds are tunable constants (see below).
- **State panel** on click: total accounts, penetration per type + overall (number + bar),
  searchable account list with brand badges.
- **Header stats**: accounts, states covered, overall %, and per-type counts (all filtered).
- Hover tooltip, zoom/pan + click-to-zoom, state search box, and **Export CSV** of the
  current filter.

## Tune the heat-map thresholds

Near the top of the app `<script>` in `index.html` (and in `build/app.template.html`):

```js
const HEAT = {
  count:       { mid: 3,  high: 12 },   // accounts: 0=red, mid=yellow, high+=green
  penetration: { mid: 15, high: 40 },   // percent
};
```

## Deploy (GitHub Pages)

Put `index.html` at the repo root (or in `/docs`), then *Settings → Pages → Deploy from a
branch*. It's fully static — nothing else to configure. (The `build/` folder and this README
are not required at runtime.)

## Regenerate `index.html`

`index.html` is assembled from `build/`:

```
cd build && python3 build.py   # -> writes ../index.html
```

- `build/app.template.html` — the app (HTML/CSS/JS) with `__D3_LIBS__` and `__US_TOPO_JSON__`
  placeholders. **Edit the app here**, then rebuild.
- `build/libs.html` — inlined d3 v7 + topojson-client.
- `build/us-states-10m.json` — us-atlas `states-10m` TopoJSON.
