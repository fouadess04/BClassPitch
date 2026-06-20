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

## 5. Client-Side Script Functionality
- **Impress Initialization**: Duration 900ms, bounds 1100x760, perspective 1200.
- **Progress Indicator**: Tracks `impress:stepenter` events and updates `#progressText` format `current / total`.
- **Step Navigation Click**: Clicking on an inactive step moves the viewport to that step.
- **Chrome FAB Hooks**: `#nextBtn` (next), `#prevBtn` (prev), `#mapBtn` (goes to overview `#whatsnext`).
- **Mobile Landscape Overlay**: Shows `#mobileOverlay` when screen height > screen width on touch-capable/mobile devices.
- **Fullscreen triggers**: `#fullscreenBtn` enters full screen; `#exitFullscreenText` exits.
- **Swipe/Tap Sim**: Left half tap = previous; right half tap = next (ignoring interactive elements).
