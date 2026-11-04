"""Generates the SVG assets used by README.md. Run: python3 scripts/build_assets.py

Follows a personal design system: one accent (#aa3bff) with an 8-stop scale, gradient
buttons with accent-tinted glow, translucent rounded-2xl cards, uppercase tracked
eyebrow labels, avatar circles cycling the accent family.
"""
import html, pathlib, textwrap

OUT = pathlib.Path(__file__).resolve().parent.parent / "assets"
OUT.mkdir(exist_ok=True)

A = {"50": "#f6ebff", "100": "#e9ccff", "200": "#d399ff", "300": "#bd66ff", "500": "#aa3bff", "700": "#8700ee", "800": "#5b00a1"}
BG, SURFACE, BORDER, TEXT, MUTED = "#16171d", "#1d1e27", "#2e303a", "#f3f4f6", "#9ca3af"
FONT = "Syne, 'Plus Jakarta Sans', 'Segoe UI', Helvetica, Arial, sans-serif"
BODY = "'Plus Jakarta Sans', Inter, 'Segoe UI', Helvetica, Arial, sans-serif"
AVATARS = [A["500"], A["300"], A["700"], A["200"]]

def esc(s): return html.escape(s, quote=True)

def write(name, svg): (OUT / name).write_text(svg, encoding="utf-8")

def svg(w, h, body, defs=""):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img">'
            f'<defs>{defs}</defs>{body}</svg>')

# ---- banner
def banner():
    w, h = 1000, 240
    defs = f'''
    <radialGradient id="g1" cx="85%" cy="0%" r="70%"><stop offset="0" stop-color="{A['500']}" stop-opacity=".55"/><stop offset="1" stop-color="{A['500']}" stop-opacity="0"/></radialGradient>
    <radialGradient id="g2" cx="0%" cy="100%" r="60%"><stop offset="0" stop-color="{A['700']}" stop-opacity=".5"/><stop offset="1" stop-color="{A['700']}" stop-opacity="0"/></radialGradient>
    <linearGradient id="gt" x1="0" x2="1"><stop offset="0" stop-color="#fff"/><stop offset="1" stop-color="{A['200']}"/></linearGradient>
    <pattern id="dots" width="26" height="26" patternUnits="userSpaceOnUse"><circle cx="1" cy="1" r="1" fill="#fff" fill-opacity=".07"/></pattern>'''
    body = f'''
    <rect width="{w}" height="{h}" rx="24" fill="{BG}"/>
    <rect width="{w}" height="{h}" rx="24" fill="url(#g1)"/><rect width="{w}" height="{h}" rx="24" fill="url(#g2)"/>
    <rect width="{w}" height="{h}" rx="24" fill="url(#dots)"/>
    <rect x=".5" y=".5" width="{w-1}" height="{h-1}" rx="23.5" fill="none" stroke="#fff" stroke-opacity=".08"/>
    <text x="500" y="78" text-anchor="middle" font-family="{BODY}" font-size="12" font-weight="600" letter-spacing="4.5" fill="{A['300']}">CYBERSECURITY  /  FULL-STACK  /  DESIGN</text>
    <text x="500" y="142" text-anchor="middle" font-family="{FONT}" font-size="64" font-weight="800" letter-spacing="-2" fill="url(#gt)">Amirul Hakimi</text>
    <text x="500" y="184" text-anchor="middle" font-family="{BODY}" font-size="16" fill="#fff" fill-opacity=".62">Building software, now learning to defend it. Jitra, Kedah, Malaysia.</text>'''
    write("banner.svg", svg(w, h, body, defs))

# ---- buttons
ICONS = {
    "arrow": '<path d="M0 8L8 0M2 0h6v6" fill="none" stroke="{c}" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/>',
}
def button(name, label, primary=True, w=176):
    h = 48
    if primary:
        fill, txt, stroke, shadow = "url(#bg)", "#ffffff", "none", True
    else:
        fill, txt, stroke, shadow = "#ffffff", A["100"], "#ffffff", False
    defs = f'''<linearGradient id="bg" x1="0" x2="1" y1="0" y2="1"><stop offset="0" stop-color="{A['500']}"/><stop offset="1" stop-color="{A['700']}"/></linearGradient>
    <filter id="glow" x="-30%" y="-40%" width="160%" height="200%"><feDropShadow dx="0" dy="4" stdDeviation="7" flood-color="{A['500']}" flood-opacity=".38"/></filter>'''
    pad = 8
    if primary:
        rect = f'<rect x="{pad}" y="{pad-2}" width="{w}" height="{h}" rx="14" fill="{fill}" filter="url(#glow)"/>'
    else:
        rect = (f'<rect x="{pad}" y="{pad-2}" width="{w}" height="{h}" rx="14" fill="{SURFACE}"/>'
                f'<rect x="{pad+.5}" y="{pad-1.5}" width="{w-1}" height="{h-1}" rx="13.5" fill="none" stroke="{A["500"]}" stroke-opacity=".45"/>')
    cx = pad + w / 2
    body = (rect +
        f'<text x="{cx-8}" y="{pad-2+h/2+5}" text-anchor="middle" font-family="{BODY}" font-size="15" font-weight="700" fill="{txt}">{esc(label)}</text>'
        f'<g transform="translate({cx + len(label)*4.2 + 4},{pad-2+h/2-4})">{ICONS["arrow"].format(c=txt)}</g>')
    write(name, svg(w + pad * 2, h + pad * 2 + 2, body, defs))

# ---- eyebrow labels
def eyebrow(name, text):
    w = 40 + len(text) * 11
    body = (f'<rect x="0" y="9" width="22" height="2.5" rx="1.25" fill="{A["500"]}"/>'
            f'<text x="32" y="15" font-family="{BODY}" font-size="12" font-weight="700" letter-spacing="3.6" fill="{A["300"]}">{esc(text.upper())}</text>')
    write(name, svg(w, 24, body))

# ---- project cards
def card(name, title, desc, tags, idx):
    w, h = 420, 196
    lines = textwrap.wrap(desc, 50)[:4]
    colour = AVATARS[idx % len(AVATARS)]
    defs = f'''<linearGradient id="sh" x1="0" x2="1" y1="0" y2="1"><stop offset="0" stop-color="{A['500']}" stop-opacity=".14"/><stop offset="1" stop-color="{A['500']}" stop-opacity="0"/></linearGradient>
    <filter id="soft" x="-20%" y="-20%" width="140%" height="150%"><feDropShadow dx="0" dy="10" stdDeviation="12" flood-color="#000" flood-opacity=".35"/></filter>'''
    body = (f'<rect x="10" y="6" width="{w-20}" height="{h-24}" rx="20" fill="{SURFACE}" filter="url(#soft)"/>'
            f'<rect x="10" y="6" width="{w-20}" height="{h-24}" rx="20" fill="url(#sh)"/>'
            f'<rect x="10.5" y="6.5" width="{w-21}" height="{h-25}" rx="19.5" fill="none" stroke="#fff" stroke-opacity=".08"/>'
            f'<circle cx="46" cy="42" r="17" fill="{colour}" fill-opacity=".22"/>'
            f'<text x="46" y="48" text-anchor="middle" font-family="{FONT}" font-size="17" font-weight="800" fill="{colour}">{esc(title[0].upper())}</text>'
            f'<text x="72" y="48" font-family="{FONT}" font-size="20" font-weight="800" letter-spacing="-.4" fill="{TEXT}">{esc(title)}</text>')
    y = 82
    for ln in lines:
        body += f'<text x="32" y="{y}" font-family="{BODY}" font-size="13" fill="{MUTED}">{esc(ln)}</text>'; y += 19
    x = 32
    for t in tags:
        pw = 18 + len(t) * 7.2
        body += (f'<rect x="{x}" y="{h-58}" width="{pw}" height="22" rx="11" fill="{A["500"]}" fill-opacity=".18"/>'
                 f'<text x="{x+pw/2}" y="{h-43}" text-anchor="middle" font-family="{BODY}" font-size="11" font-weight="600" fill="{A["200"]}">{esc(t)}</text>')
        x += pw + 8
    write(name, svg(w, h, body, defs))

banner()
button("btn-portfolio.svg", "Portfolio", True, 176)
button("btn-linkedin.svg", "LinkedIn", True, 168)
button("btn-email.svg", "Email me", False, 160)
button("btn-github.svg", "GitHub", False, 150)
for n, t in [("about", "About"), ("projects", "Featured projects"), ("stack", "Tech stack"), ("stats", "GitHub stats"), ("contact", "Get in touch")]:
    eyebrow(f"eyebrow-{n}.svg", t)
PROJECTS = [
    ("loglens", "In-browser log analyzer with explainable detection rules, MITRE ATT&CK mapping, timeline and alert triage. Files never leave your browser.", ["TypeScript", "Security"]),
    ("phishcheck", "Client-side phishing email analyzer. Explains each red flag and never opens links or renders HTML. Your email stays in your browser.", ["TypeScript", "Security"]),
    ("seckit-mcp", "Read-only defensive security MCP server: CVE and ATT&CK lookups, privacy-preserving breach check, log parsing and IOC defanging.", ["MCP", "Security"]),
    ("design-system-mcp", "MCP server that exposes a personal design system (palette generator, component rules, UI review) to AI clients.", ["MCP", "Design"]),
]
for i, (n, d, t) in enumerate(PROJECTS):
    card(f"card-{n}.svg", n, d, t, i)
print("assets written:", len(list(OUT.glob('*.svg'))))
