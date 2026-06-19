# Impress.js Pitch Deck Structure (`index.html`)
> [!NOTE]
> This is an automatically generated token-efficient structural representation of `index.html`.
> It describes layouts, design tokens, classes, positioning, and script logic so AI models
> don't need to scan the entire 1300+ line HTML file for styling or step positions.
> **Only modify this file if there are major layout, CSS style, or structural additions.**

## 1. Design Tokens (CSS Custom Properties)
These define the core theme palette and typography used throughout the deck:
| Variable | Value | Description / Usage |
|---|---|---|
| `--primary-blue` | `#0E4B8A` | Color code |
| `--primary-blue-deep` | `#0A3868` | Color code |
| `--active-green` | `#1E7833` | Color code |
| `--active-green-deep` | `#155726` | Color code |
| `--canvas-bg` | `#FFFFFF` | Color code |
| `--neutral-text` | `#2C3E50` | Color code |
| `--card-canvas` | `#F8FAFC` | Color code |
| `--pink-bg` | `#FCE7F3` | Color code |
| `--pink-text` | `#9D174D` | Color code |
| `--blue-bg` | `#E0F2FE` | Color code |
| `--blue-text` | `#0369A1` | Color code |
| `--red-bg` | `#FEE2E2` | Color code |
| `--red-text` | `#DC2626` | Color code |
| `--green-bg` | `#DCFCE7` | Color code |
| `--green-text` | `#1E7833` | Color code |
| `--glossary` | `#94A3B8` | Color code |
| `--sans` | `'Manrope', system-ui, sans-serif` | Font family |
| `--serif` | `'Lora', Georgia, serif` | Font family |

## 2. Core Layout Elements & Classes
Use these classes to structure card layouts within step canvases:
- `.step`: Base step container (`width: 1100px; min-height: 760px;`). Aligned using impress data coordinates.
- `.hero`: Full slide gradient banner block used for `#title` and `#whatsnext`.
- `.note-card`: Main presentation card style. Uses inline `--accent: COLOR;` to color headers, left borders, and inner sub-titles.
- `.card-header` & `.card-body`: Structural parts of a `.note-card`.
- `.mini-grid`: Grid layouts (`cols-2`, `cols-3`, `cols-4`) for aligning small items.
- `.mini-card`: Left-bordered mini card used inside grids.
- `.stat-grid` & `.stat-tile`: Layout structure for statistical KPIs.
- `.funnel`, `.funnel-row`, `.funnel-bar`, `.funnel-label`: Horizontal bar-chart funnels (e.g. for TAM/SAM/SOM).
- `.phase-track`, `.phase`: Three-column horizontal phase roadmap.
- `table.bn-table`: Full-width responsive comparison table structure.
- `.pill`, `.pill-pink`, `.pill-blue`, `.pill-red`, `.pill-green`, `.pill-ghost`: Semantic tag pill highlights.
- `.hl-underline`: Custom underlined, italicized footnote style.
- `.status-pill`: Rounded pill label style for roles/states.

## 3. Fixed Chrome Layout (HUD Overlay)
Elements locked outside the impress canvas:
- `.chrome.wordmark`: Logo and brand name (top-left).
- `.chrome.progress-pill` (`#progressPill`): Dynamic slide index label (top-right, e.g. `01 / 13`).
- `.chrome.fab-stack`: Vertically stacked FAB buttons: `#mapBtn` (Zoom out), `#prevBtn` (Up/Left), `#nextBtn` (Down/Right).
- `.chrome.hint-chrome`: Navigation helper text bar (bottom-left).
- `#mobileOverlay`: Landscape locking orientation popup for mobile screens.

## 4. Slides (Impress Steps) Directory & Map
The 13 presentation steps mapped in 3D canvas space:
| Index | Slide ID | X Coord | Y Coord | Z Coord | Rotate | Scale | Layout & Content Structure |
|---|---|---|---|---|---|---|---|
| 01 | `title` | 0 | 0 | 0 | 0° | 1× | **Hero Layout**: Title: "BClass" | Tagline: ""The only education platform you'll need."" |
| 02 | `exec-summary` | -1400 | 850 | -40 | -3° | 1× | **Note-Card** (Accent: `#0E4B8A`, Header: "Executive Summary", Tag: "Elevator Pitch")<br>- Sub-sections: "The Problem", "The Solution", "The Impact" |
| 03 | `team` | 0 | 850 | -40 | 2° | 1× | **Note-Card** (Accent: `#0369A1`, Header: "The Team", Tag: "4 People")<br>- Mini-Grid (4 items): "ESSAIDI Fouad ("Bigovi")" (Founder · CTO · Product Lead), "SADAOUI Ayoub" (UI/UX Designer · Frontend), "BOUZAGHOU Chafik" (Backend & Security Lead), "DAHMANI Rayhane" (Pharmacy Community Lead) |
| 04 | `problem` | 1400 | 850 | -40 | -2° | 1× | **Note-Card** (Accent: `#DC2626`, Header: "Problem Statement", Tag: "Real & Measured")<br>- Sub-sections: "Case Study"<br>- Stat-Grid (3 tiles): 4+ hrs (to decipher one topic), <20% (average lecture attendance), 0 (faculty-aligned exam banks) |
| 05 | `solution` | -2100 | 1700 | -80 | 3° | 1× | **Note-Card** (Accent: `#1E7833`, Header: "The Solution", Tag: "3-Step Workflow")<br>- Sub-sections: "Step 1 — Centralized Resource Hub", "Step 2 — AI-Powered MCQ Generation", "Step 3 — Exam-Aware Study Summaries" |
| 06 | `traction` | -700 | 1700 | -80 | -2° | 1× | **Note-Card** (Accent: `#1E7833`, Header: "Prototype & Traction", Tag: "Live Beta")<br>- Sub-sections: "Live Today", "Next 6 Months"<br>- Stat-Grid (3 tiles): 150+ (active students, Blida), 0 DZD (spent on marketing), 500+ (users targeted, end 2025) |
| 07 | `ip` | 700 | 1700 | -80 | 2° | 1× | **Note-Card** (Accent: `#0E4B8A`, Header: "Intellectual Property", Tag: "IP Strategy")<br>- Mini-Grid (4 items): "Patents", "Trademark", "Copyright", "Trade Secrets" |
| 08 | `value` | 2100 | 1700 | -80 | -3° | 1× | **Note-Card** (Accent: `#1E7833`, Header: "Value Added", Tag: "Outcomes")<br>- Sub-sections: "Quantitative", "Qualitative", "Near-Term" |
| 09 | `competitive` | -2100 | 2550 | -120 | -2° | 1× | **Note-Card** (Accent: `#9D174D`, Header: "Competitive Analysis", Tag: "Blue Ocean")<br>- Table structure: Headers ['Feature', 'BClass', 'NotebookLM'], 5 data rows |
| 10 | `market` | -700 | 2550 | -120 | 3° | 1× | **Note-Card** (Accent: `#0369A1`, Header: "Target Market", Tag: "TAM · SAM · SOM")<br>- Sub-sections: "Pricing", "AI Units:"<br>- Funnel (3 rows): TAM — 20,000 -> All Algerian pharmacy students, SAM — 10,000 -> Blida, Algiers, Constantine, Oran,
                Tizi-Ouzou, SOM — 1,500 -> Paying users, 3-yr realistic capture |
| 11 | `business` | 700 | 2550 | -120 | -3° | 1× | **Note-Card** (Accent: `#0E4B8A`, Header: "Business Model", Tag: "Unit Economics")<br>- Sub-sections: "Path to Profitability"<br>- Stat-Grid (4 tiles): 750 DZD (CAC), 5,416 DZD (LTV), 7.2× (LTV : CAC), 7 mo (payback) |
| 12 | `roadmap` | 2100 | 2550 | -120 | 2° | 1× | **Note-Card** (Accent: `#1E7833`, Header: "Roadmap & Vision", Tag: "3 Phases")<br>- Roadmap Phases (3 phases): Phase 1 of 3: "6 Months — Q3/Q4 2025", Phase 2 of 3: "1 Year — 2026", Phase 3 of 3: "3 Years — 2027/28" |
| 13 | `whatsnext` | 0 | 1275 | 0 | 0° | 8× | **Hero Layout**: Title: "What's Next" | Tagline: "Help us turn 150 organic users into the national backboneof Algerian pharmacy education." |

## 5. Client-Side Script Functionality
- **Impress Initialization**: Duration 900ms, bounds 1100x760, perspective 1200.
- **Progress Indicator**: Tracks `impress:stepenter` events and updates `#progressText` format `current / total`.
- **Step Navigation Click**: Clicking on an inactive step moves the viewport to that step.
- **Chrome FAB Hooks**: `#nextBtn` (next), `#prevBtn` (prev), `#mapBtn` (goes to overview `#whatsnext`).
- **Mobile Landscape Overlay**: Shows `#mobileOverlay` when screen height > screen width on touch-capable/mobile devices.
- **Fullscreen triggers**: `#fullscreenBtn` enters full screen; `#exitFullscreenText` exits.
- **Swipe/Tap Sim**: Left half tap = previous; right half tap = next (ignoring interactive elements).
