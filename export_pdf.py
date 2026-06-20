#!/usr/bin/env python3
"""Export the impress.js presentation to a multi-page landscape PDF.

Produces a **vector** PDF with selectable text and high-quality images
by leveraging Playwright's built-in page.pdf() renderer (Chromium print-to-PDF).

Usage:
    python export_pdf.py                     # uses http://localhost:5000
    python export_pdf.py --url http://...    # custom URL
    python export_pdf.py --html index.html   # local HTML file
    python export_pdf.py --output deck.pdf   # custom output filename

Requirements (install inside venv):
    pip install playwright pypdf
    playwright install chromium
"""
import argparse
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright
from pypdf import PdfWriter, PdfReader

# Ordered list of slide IDs matching the presentation flow
SLIDE_IDS = [
    "title",
    "exec-summary",
    "team",
    "problem",
    "solution",
    "prototype-links",
    "traction",
    "ip",
    "value",
    "competitive",
    "market",
    "business",
    "roadmap",
    "whatsnext",
]

# ── CSS injected once on load to hide interactive chrome ──────────────
HIDE_CHROME_CSS = """
/* Hide interactive chrome */
.chrome.progress-pill,
.chrome.fab-stack,
.chrome.hint-chrome,
.hint,
#mobileOverlay,
.fallback-message {
    display: none !important;
}

/* Make running wordmark smaller in the corner */
.chrome.wordmark {
    top: 12px !important;
    left: 14px !important;
    gap: 5px !important;
}
.chrome.wordmark img {
    width: 18px !important;
    height: 18px !important;
}
.chrome.wordmark span {
    font-size: 0.75rem !important;
}
"""

# ── CSS injected per-slide to flatten 3D transforms for print ─────────
# This converts the impress.js 3D canvas into a flat, printable layout
# so Chromium's print-to-PDF engine can emit real text + vector shapes.
PRINT_FLATTEN_CSS = """
/* ── Body: flexbox center the single visible slide ── */
html, body {
    overflow: visible !important;
    height: 780px !important;
    width: 1160px !important;
    margin: 0 !important;
    padding: 30px !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
}

/* ── Strip ALL impress.js wrapper transforms & positioning ── */
#impress,
#impress > div {
    transform: none !important;
    perspective: none !important;
    transform-style: flat !important;
    position: static !important;
    overflow: visible !important;
    width: auto !important;
    height: auto !important;
    top: auto !important;
    left: auto !important;
    display: block !important;
}

/* ── Hide every step by default ── */
.step {
    transform: none !important;
    transform-style: flat !important;
    position: absolute !important;
    top: -9999px !important;
    left: -9999px !important;
    opacity: 0 !important;
    pointer-events: none !important;
    visibility: hidden !important;
    width: 0 !important;
    height: 0 !important;
    overflow: hidden !important;
}

/* ── Show only the active step, properly sized ── */
.step.active {
    opacity: 1 !important;
    visibility: visible !important;
    position: static !important;
    pointer-events: auto !important;
    width: 1100px !important;
    min-height: 720px !important;
    height: auto !important;
    overflow: visible !important;
    top: auto !important;
    left: auto !important;
    margin: 0 !important;
}

/* ── What's Next hero: override the 8x scale to fit a normal page ── */
#whatsnext.active {
    opacity: 1 !important;
    visibility: visible !important;
}
#whatsnext.active .hero {
    width: calc(1100px - 80px) !important;
    min-height: calc(720px - 80px) !important;
    margin: 40px auto !important;
    font-size: 1rem !important;
}

/* ── Hide all chrome during print ── */
.chrome.wordmark {
    display: none !important;
}

/* ── Print page setup ── */
@page {
    size: 1160px 780px;
    margin: 0;
}
"""

VIEWPORT_W = 1280
VIEWPORT_H = 720


def export_pdf(url: str, output: str):
    export_dir = Path(__file__).parent / "exports"
    export_dir.mkdir(exist_ok=True)
    tmp_dir = export_dir / "_tmp"
    tmp_dir.mkdir(exist_ok=True)
    output = str(export_dir / Path(output).name)
    slide_pdfs: list[Path] = []

    print(f"🚀 Exporting {len(SLIDE_IDS)} slides from {url} ...")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        # Use 2x device scale for crisp raster elements (images, shadows)
        context = browser.new_context(
            viewport={"width": VIEWPORT_W, "height": VIEWPORT_H},
            device_scale_factor=2,
        )
        page = context.new_page()

        # Load the presentation
        page.goto(url, wait_until="networkidle")
        page.wait_for_timeout(2000)  # let impress.js fully init

        # Inject chrome-hiding CSS
        page.add_style_tag(content=HIDE_CHROME_CSS)
        page.wait_for_timeout(300)

        for i, slide_id in enumerate(SLIDE_IDS, 1):
            # Navigate to the slide via the impress API
            page.evaluate(f"impress().goto('{slide_id}')")
            page.wait_for_timeout(1200)  # transition duration (900ms) + buffer

            # Inject the flatten CSS for print rendering
            flatten_handle = page.add_style_tag(content=PRINT_FLATTEN_CSS)
            page.wait_for_timeout(200)

            # Generate a vector PDF for this single slide
            slide_path = tmp_dir / f"slide_{i:02d}.pdf"
            page.pdf(
                path=str(slide_path),
                width="1160px",
                height="780px",
                margin={"top": "0px", "right": "0px", "bottom": "0px", "left": "0px"},
                print_background=True,
                prefer_css_page_size=True,
            )
            slide_pdfs.append(slide_path)
            print(f"  ✅ Slide {i:02d}/{len(SLIDE_IDS)} — #{slide_id}")

            # Remove the flatten CSS so next navigation works correctly
            page.evaluate("(el) => el.remove()", flatten_handle)
            page.wait_for_timeout(100)

        browser.close()

    # ── Merge individual slide PDFs into one document ─────────────────
    print(f"\n📄 Merging {len(slide_pdfs)} slides → {output}")
    writer = PdfWriter()
    for pdf_path in slide_pdfs:
        reader = PdfReader(str(pdf_path))
        for pg in reader.pages:
            writer.add_page(pg)

    with open(output, "wb") as f:
        writer.write(f)

    # Cleanup temp files
    for pdf_path in slide_pdfs:
        pdf_path.unlink(missing_ok=True)
    tmp_dir.rmdir()

    print(f"✨ Done! PDF saved to: {output}")
    print(f"   → Text is selectable, images rendered at 2× device scale")


def main():
    parser = argparse.ArgumentParser(description="Export impress.js deck to PDF")
    parser.add_argument(
        "--url",
        default="http://localhost:5000",
        help="URL of the running presentation (default: http://localhost:5000)",
    )
    parser.add_argument(
        "--html",
        help="Local HTML file to export (e.g., index.html). Overrides --url.",
    )
    parser.add_argument(
        "--output",
        default="BClass — Pitch Deck.pdf",
        help="Output PDF filename (default: 'exports/BClass — Pitch Deck.pdf')",
    )
    args = parser.parse_args()

    if args.html:
        html_path = Path(args.html).resolve()
        url = f"file://{html_path}"
    else:
        url = args.url

    export_pdf(url, args.output)


if __name__ == "__main__":
    main()
