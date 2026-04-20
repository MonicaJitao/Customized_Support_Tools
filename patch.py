#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
One-shot patch: restructure page-config + merge fxcb/stratCost -> bizCost
"""
import re, sys

src = open('index.html', encoding='utf-8').read()
orig_len = len(src)

def replace_once(s, old, new, label):
    if old not in s:
        print(f"  MISS: {label}")
        return s
    result = s.replace(old, new, 1)
    print(f"  OK:   {label}")
    return result

# ── 1. CSS: add config-section-header after .config-panel.active ──────────
src = replace_once(src,
    '.config-panel { display: none; }\n.config-panel.active { display: block; }',
    '''.config-panel { display: none; }
.config-panel.active { display: block; }

/* param-config section headers */
.config-section-header {
    font-size: 13px;
    font-weight: 600;
    color: var(--ink-mid);
    text-transform: uppercase;
    letter-spacing: .05em;
    padding: 6px 0 8px;
    margin: 24px 0 12px;
    border-bottom: 2px solid var(--border);
}
.config-section-header:first-child { margin-top: 0; }''',
    'CSS config-section-header')

# ── 2. Nav: add stats nav item after page-config nav item ─────────────────
src = replace_once(src,
    "onclick=\"UI.switchPage('page-config', this)\">\n                <span class=\"nav-icon\">&#9881;</span>",
    "onclick=\"UI.switchPage('page-config', this)\">\n                <span class=\"nav-icon\">&#9881;</span>",
    'nav stats placeholder')  # will fix below

# Actually find the closing </div> of the page-config nav item and insert after
old_nav_block = "onclick=\"UI.switchPage('page-config', this)\">\n                <span class=\"nav-icon\">&#9881;</span>\u53c2\u6570\u914d\u7f6e\n            </div>"
new_nav_block = ("onclick=\"UI.switchPage('page-config', this)\">\n                <span class=\"nav-icon\">&#9881;</span>\u53c2\u6570\u914d\u7f6e\n            </div>\n"
    "            <div class=\"nav-item nav-admin-only\" data-page=\"page-stats\" onclick=\"UI.switchPage('page-stats', this); StatsPanel.refresh()\">\n"
    "                <span class=\"nav-icon\">&#128202;</span>\u4f7f\u7528\u7edf\u8ba1\n            </div>")
src = replace_once(src, old_nav_block, new_nav_block, 'nav stats item')
