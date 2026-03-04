#!/usr/bin/env python3
"""Auto-generate index.html for study materials repository."""

import os
from pathlib import Path

SECTIONS = {
    'flashcards': {'title': '🎴 Flashcards', 'color': '#4CAF50'},
    'quizzes': {'title': '🎯 Quizzes', 'color': '#2196F3'},
    'mindmaps': {'title': '🧠 Mind Maps', 'color': '#9C27B0'},
    'anki': {'title': '🃏 Anki Decks', 'color': '#FF9800'}
}

def get_files(section):
    path = Path(section)
    if not path.exists():
        return []
    files = []
    for f in sorted(path.iterdir()):
        if f.is_file():
            files.append({
                'name': f.stem.replace('_', ' ').title(),
                'filename': f.name,
                'path': f"{section}/{f.name}"
            })
    return files

def generate():
    sections = []
    for folder, cfg in SECTIONS.items():
        files = get_files(folder)
        if not files:
            continue
        links = []
        for f in files:
            ext = f['filename'].split('.')[-1].upper()
            links.append(f'<a href="{f["path"]}" class="file"><span class="name">{f["name"]}</span><span class="ext">{ext}</span></a>')
        sections.append(f'<section><h2 style="color:{cfg["color"]}">{cfg["title"]}</h2><div class="grid">{"".join(links)}</div></section>')
    
    html = f'''<!DOCTYPE html>
<html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Study Materials</title><style>
body{{font-family:-apple-system,BlinkMacSystemFont,sans-serif;background:linear-gradient(135deg,#1a1a2e,#16213e,#0f3460);min-height:100vh;color:#fff;padding:2rem}}
.container{{max-width:1200px;margin:0 auto}}
header{{text-align:center;padding:3rem 1rem}}
h1{{font-size:3rem;background:linear-gradient(90deg,#00d4ff,#7b2cbf);-webkit-background-clip:text;-webkit-text-fill-color:transparent;margin-bottom:.5rem}}
.subtitle{{color:#8892b0}}
section{{margin-bottom:3rem}}
h2{{font-size:1.8rem;margin-bottom:1.5rem;padding-bottom:.5rem;border-bottom:2px solid}}
.grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:1rem}}
.file{{display:flex;justify-content:space-between;align-items:center;background:rgba(255,255,255,.05);border:1px solid rgba(255,255,255,.1);border-radius:12px;padding:1rem 1.5rem;text-decoration:none;color:#fff;transition:all .3s}}
.file:hover{{background:rgba(255,255,255,.1);border-color:rgba(255,255,255,.3);transform:translateY(-2px);box-shadow:0 10px 30px rgba(0,0,0,.3)}}
.name{{font-weight:500}}
.ext{{font-size:.75rem;padding:.25rem .75rem;background:rgba(255,255,255,.1);border-radius:20px;color:#8892b0}}
footer{{text-align:center;padding:2rem;color:#8892b0;font-size:.9rem}}
@media(max-width:768px){{h1{{font-size:2rem}}.grid{{grid-template-columns:1fr}}}}
</style></head><body>
<div class="container"><header><h1>📚 Study Materials</h1><p class="subtitle">Interactive flashcards, quizzes, mind maps & Anki decks</p></header>
{''.join(sections) if sections else '<div style="text-align:center;padding:4rem;color:#8892b0"><h2>📝 No materials yet</h2><p>Add files to the folders and they will appear here!</p></div>'}
<footer><p>Auto-generated • Last updated: {os.popen("date -u +%Y-%m-%d %H:%M UTC").read().strip()}</p></footer>
</div></body></html>'''
    
    with open('index.html', 'w') as f:
        f.write(html)
    print('✅ index.html generated!')

if __name__ == '__main__':
    generate()
