#!/usr/bin/env python3
import os
import re
import hashlib
from html.parser import HTMLParser

class HTMLNode:
    def __init__(self, tag, attrs):
        self.tag = tag
        self.attrs = dict(attrs)
        self.classes = self.attrs.get('class', '').split()
        self.id = self.attrs.get('id', '')
        self.style = self.attrs.get('style', '')
        self.children = []
        self.text_content = []

    def get_text(self):
        return "".join(self.text_content).strip()

class DOMBuilder(HTMLParser):
    def __init__(self):
        super().__init__()
        self.root = HTMLNode('root', {})
        self.stack = [self.root]

    def handle_starttag(self, tag, attrs):
        node = HTMLNode(tag, attrs)
        self.stack[-1].children.append(node)
        # Avoid pushing self-closing/void tags onto the DOM stack
        void_tags = {'area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input', 'link', 'meta', 'param', 'source', 'track', 'wbr'}
        if tag.lower() not in void_tags:
            self.stack.append(node)

    def handle_endtag(self, tag):
        if len(self.stack) > 1:
            self.stack.pop()

    def handle_data(self, data):
        self.stack[-1].text_content.append(data)

def parse_html_to_dom(html_content):
    parser = DOMBuilder()
    parser.feed(html_content)
    return parser.root

def get_nodes_by_class(node, class_name, results=None):
    if results is None:
        results = []
    if class_name in node.classes:
        results.append(node)
    for child in node.children:
        get_nodes_by_class(child, class_name, results)
    return results

def get_nodes_by_tag(node, tag_name, results=None):
    if results is None:
        results = []
    if node.tag == tag_name:
        results.append(node)
    for child in node.children:
        get_nodes_by_tag(child, tag_name, results)
    return results

def extract_css_variables(html_content):
    # Find all CSS root variables
    root_match = re.search(r':root\s*{(.*?)}', html_content, re.DOTALL)
    if not root_match:
        return []
    variables = []
    for line in root_match.group(1).split('\n'):
        line = line.strip()
        if line.startswith('--') and ':' in line:
            parts = line.split(':', 1)
            name = parts[0].strip()
            val = parts[1].split(';')[0].strip()
            variables.append((name, val))
    return variables

def analyze_step_structure(step_node):
    structure = []
    
    # Check for Hero layout
    hero_nodes = get_nodes_by_class(step_node, 'hero')
    if hero_nodes:
        hero = hero_nodes[0]
        title_nodes = get_nodes_by_tag(hero, 'h1')
        title = title_nodes[0].get_text() if title_nodes else "Untitled Hero"
        taglines = get_nodes_by_class(hero, 'tagline')
        tagline = taglines[0].get_text() if taglines else ""
        structure.append(f"**Hero Layout**: Title: \"{title}\" | Tagline: \"{tagline}\"")
        return structure

    # Check for Note Card
    note_card_nodes = get_nodes_by_class(step_node, 'note-card')
    if note_card_nodes:
        card = note_card_nodes[0]
        # Get accent color
        accent = card.attrs.get('style', '')
        accent_color = ""
        if '--accent' in accent:
            match = re.search(r'--accent:\s*([^;]+)', accent)
            if match:
                accent_color = match.group(1).strip()
        
        # Get header
        header_nodes = get_nodes_by_class(card, 'card-header')
        h2_nodes = get_nodes_by_tag(card, 'h2')
        card_title = h2_nodes[0].get_text() if h2_nodes else "Untitled Card"
        
        tag_nodes = get_nodes_by_class(card, 'tag')
        card_tag = tag_nodes[0].get_text() if tag_nodes else ""
        
        header_desc = f"**Note-Card** (Accent: `{accent_color}`, Header: \"{card_title}\""
        if card_tag:
            header_desc += f", Tag: \"{card_tag}\""
        header_desc += ")"
        structure.append(header_desc)
        
        # Check inside body
        body_nodes = get_nodes_by_class(card, 'card-body')
        if body_nodes:
            body = body_nodes[0]
            # Find subheaders
            subheaders = []
            for child in body.children:
                if child.tag in ('h3', 'h4'):
                    subheaders.append(f"\"{child.get_text()}\"")
            if subheaders:
                structure.append(f"- Sub-sections: {', '.join(subheaders)}")
            
            # Check mini-grid
            mini_grid_nodes = get_nodes_by_class(body, 'mini-grid')
            if mini_grid_nodes:
                mini_cards = get_nodes_by_class(mini_grid_nodes[0], 'mini-card')
                card_infos = []
                for mc in mini_cards:
                    mch4 = get_nodes_by_tag(mc, 'h4')
                    mc_title = mch4[0].get_text() if mch4 else "Untitled"
                    role_nodes = get_nodes_by_class(mc, 'role')
                    role = role_nodes[0].get_text() if role_nodes else ""
                    if role:
                        card_infos.append(f"\"{mc_title}\" ({role})")
                    else:
                        card_infos.append(f"\"{mc_title}\"")
                structure.append(f"- Mini-Grid ({len(mini_cards)} items): {', '.join(card_infos)}")
            
            # Check stat-grid
            stat_grid_nodes = get_nodes_by_class(body, 'stat-grid')
            if stat_grid_nodes:
                tiles = get_nodes_by_class(stat_grid_nodes[0], 'stat-tile')
                tile_infos = []
                for tile in tiles:
                    num_nodes = get_nodes_by_class(tile, 'num')
                    lbl_nodes = get_nodes_by_class(tile, 'lbl')
                    num = num_nodes[0].get_text() if num_nodes else "?"
                    lbl = lbl_nodes[0].get_text() if lbl_nodes else "?"
                    tile_infos.append(f"{num} ({lbl})")
                structure.append(f"- Stat-Grid ({len(tiles)} tiles): {', '.join(tile_infos)}")
                
            # Check funnel
            funnel_nodes = get_nodes_by_class(body, 'funnel')
            if funnel_nodes:
                rows = get_nodes_by_class(funnel_nodes[0], 'funnel-row')
                funnel_infos = []
                for r in rows:
                    lbl_nodes = get_nodes_by_class(r, 'funnel-label')
                    bar_nodes = get_nodes_by_class(r, 'funnel-bar')
                    lbl = lbl_nodes[0].get_text() if lbl_nodes else "?"
                    bar = bar_nodes[0].get_text() if bar_nodes else "?"
                    funnel_infos.append(f"{lbl} -> {bar}")
                structure.append(f"- Funnel ({len(rows)} rows): {', '.join(funnel_infos)}")
                
            # Check phase-track (Roadmap)
            phase_track_nodes = get_nodes_by_class(body, 'phase-track')
            if phase_track_nodes:
                phases = get_nodes_by_class(phase_track_nodes[0], 'phase')
                phase_infos = []
                for p in phases:
                    cnt_nodes = get_nodes_by_class(p, 'step-count')
                    ph4 = get_nodes_by_tag(p, 'h4')
                    cnt = cnt_nodes[0].get_text() if cnt_nodes else "?"
                    title = ph4[0].get_text() if ph4 else "?"
                    phase_infos.append(f"{cnt}: \"{title}\"")
                structure.append(f"- Roadmap Phases ({len(phases)} phases): {', '.join(phase_infos)}")
                
            # Check table
            table_nodes = get_nodes_by_tag(body, 'table')
            if table_nodes:
                rows = get_nodes_by_tag(table_nodes[0], 'tr')
                # get headers
                headers = []
                if rows:
                    th_nodes = get_nodes_by_tag(rows[0], 'th')
                    headers = [th.get_text() for th in th_nodes]
                structure.append(f"- Table structure: Headers {headers}, {len(rows)-1 if rows else 0} data rows")
                
    return structure

def generate_efficiency_markdown(html_file_path):
    with open(html_file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    css_vars = extract_css_variables(content)
    dom_root = parse_html_to_dom(content)
    
    # Find all steps
    all_steps = get_nodes_by_class(dom_root, 'step')
    
    md_lines = []
    md_lines.append("# Impress.js Pitch Deck Structure (`index.html`)")
    md_lines.append("> [!NOTE]")
    md_lines.append("> This is an automatically generated token-efficient structural representation of `index.html`.")
    md_lines.append("> It describes layouts, design tokens, classes, positioning, and script logic so AI models")
    md_lines.append("> don't need to scan the entire 1300+ line HTML file for styling or step positions.")
    md_lines.append("> **Only modify this file if there are major layout, CSS style, or structural additions.**")
    md_lines.append("")
    
    # Design Tokens
    md_lines.append("## 1. Design Tokens (CSS Custom Properties)")
    md_lines.append("These define the core theme palette and typography used throughout the deck:")
    md_lines.append("| Variable | Value | Description / Usage |")
    md_lines.append("|---|---|---|")
    for name, val in css_vars:
        desc = "Font family" if "font" in name or name in ("--sans", "--serif") else "Color code"
        md_lines.append(f"| `{name}` | `{val}` | {desc} |")
    md_lines.append("")
    
    # CSS Layout Elements
    md_lines.append("## 2. Core Layout Elements & Classes")
    md_lines.append("Use these classes to structure card layouts within step canvases:")
    md_lines.append("- `.step`: Base step container (`width: 1100px; min-height: 760px;`). Aligned using impress data coordinates.")
    md_lines.append("- `.hero`: Full slide gradient banner block used for `#title` and `#whatsnext`.")
    md_lines.append("- `.note-card`: Main presentation card style. Uses inline `--accent: COLOR;` to color headers, left borders, and inner sub-titles.")
    md_lines.append("- `.card-header` & `.card-body`: Structural parts of a `.note-card`.")
    md_lines.append("- `.mini-grid`: Grid layouts (`cols-2`, `cols-3`, `cols-4`) for aligning small items.")
    md_lines.append("- `.mini-card`: Left-bordered mini card used inside grids.")
    md_lines.append("- `.stat-grid` & `.stat-tile`: Layout structure for statistical KPIs.")
    md_lines.append("- `.funnel`, `.funnel-row`, `.funnel-bar`, `.funnel-label`: Horizontal bar-chart funnels (e.g. for TAM/SAM/SOM).")
    md_lines.append("- `.phase-track`, `.phase`: Three-column horizontal phase roadmap.")
    md_lines.append("- `table.bn-table`: Full-width responsive comparison table structure.")
    md_lines.append("- `.pill`, `.pill-pink`, `.pill-blue`, `.pill-red`, `.pill-green`, `.pill-ghost`: Semantic tag pill highlights.")
    md_lines.append("- `.hl-underline`: Custom underlined, italicized footnote style.")
    md_lines.append("- `.status-pill`: Rounded pill label style for roles/states.")
    md_lines.append("")
    
    # Fixed UI Chrome
    md_lines.append("## 3. Fixed Chrome Layout (HUD Overlay)")
    md_lines.append("Elements locked outside the impress canvas:")
    md_lines.append("- `.chrome.wordmark`: Logo and brand name (top-left).")
    md_lines.append("- `.chrome.progress-pill` (`#progressPill`): Dynamic slide index label (top-right, e.g. `01 / 13`).")
    md_lines.append("- `.chrome.fab-stack`: Vertically stacked FAB buttons: `#mapBtn` (Zoom out), `#prevBtn` (Up/Left), `#nextBtn` (Down/Right).")
    md_lines.append("- `.chrome.hint-chrome`: Navigation helper text bar (bottom-left).")
    md_lines.append("- `#mobileOverlay`: Landscape locking orientation popup for mobile screens.")
    md_lines.append("")
    
    # Slide List and positioning
    md_lines.append("## 4. Slides (Impress Steps) Directory & Map")
    md_lines.append("The 13 presentation steps mapped in 3D canvas space:")
    md_lines.append("| Index | Slide ID | X Coord | Y Coord | Z Coord | Rotate | Scale | Layout & Content Structure |")
    md_lines.append("|---|---|---|---|---|---|---|---|")
    
    for i, step in enumerate(all_steps, 1):
        idx_str = f"{i:02d}"
        sid = step.id or f"step-{i}"
        x = step.attrs.get('data-x', '0')
        y = step.attrs.get('data-y', '0')
        z = step.attrs.get('data-z', '0')
        rot = step.attrs.get('data-rotate', '0')
        scale = step.attrs.get('data-scale', '1')
        
        # Analyze structure inside the step
        structure_list = analyze_step_structure(step)
        structure_desc = "<br>".join(structure_list) if structure_list else "*Text content layout*"
        
        md_lines.append(f"| {idx_str} | `{sid}` | {x} | {y} | {z} | {rot}° | {scale}× | {structure_desc} |")
    
    md_lines.append("")
    
    # JavaScript logic summary
    md_lines.append("## 5. Client-Side Script Functionality")
    md_lines.append("- **Impress Initialization**: Duration 900ms, bounds 1100x760, perspective 1200.")
    md_lines.append("- **Progress Indicator**: Tracks `impress:stepenter` events and updates `#progressText` format `current / total`.")
    md_lines.append("- **Step Navigation Click**: Clicking on an inactive step moves the viewport to that step.")
    md_lines.append("- **Chrome FAB Hooks**: `#nextBtn` (next), `#prevBtn` (prev), `#mapBtn` (goes to overview `#whatsnext`).")
    md_lines.append("- **Mobile Landscape Overlay**: Shows `#mobileOverlay` when screen height > screen width on touch-capable/mobile devices.")
    md_lines.append("- **Fullscreen triggers**: `#fullscreenBtn` enters full screen; `#exitFullscreenText` exits.")
    md_lines.append("- **Swipe/Tap Sim**: Left half tap = previous; right half tap = next (ignoring interactive elements).")
    md_lines.append("")
    
    return "\n".join(md_lines)

def run_update_if_needed(html_path='index.html', output_path='eff.md'):
    if not os.path.exists(html_path):
        print(f"Error: {html_path} not found.")
        return

    new_markdown = generate_efficiency_markdown(html_path)

    # Check if eff.md exists and compare contents
    if os.path.exists(output_path):
        with open(output_path, 'r', encoding='utf-8') as f:
            existing_markdown = f.read()
        
        # If no changes, skip writing
        if existing_markdown.strip() == new_markdown.strip():
            return

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(new_markdown)
    print(f"Successfully updated {output_path} (structural change detected in {html_path}).")

if __name__ == '__main__':
    run_update_if_needed()
