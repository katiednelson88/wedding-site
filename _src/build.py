import os, re, shutil

ROOT = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(ROOT, "src")
DIST = os.path.join(ROOT, "dist")
PREVIEW = os.path.join(ROOT, "preview")

PAGES = [
    ("index.html", "./", "The Lore", "Ktizzle and Mattyrizz"),
    ("plan.html", "plan.html", "The Plan", "The Plan · Ktizzle and Mattyrizz"),
    ("guide.html", "guide.html", "Survival Guide", "Survival Guide · Ktizzle and Mattyrizz"),
    ("advice.html", "advice.html", "Unsolicited Advice", "Unsolicited Advice · Ktizzle and Mattyrizz"),
    ("rsvp.html", "rsvp.html", "RSVP", "RSVP · Ktizzle and Mattyrizz"),
]

THISTLE = '''<svg class="thistle" viewBox="0 0 120 200" aria-hidden="true">
        <path d="M60 196 C58 160 60 120 60 92" stroke="#6E6A16" stroke-width="5" fill="none" stroke-linecap="round"/>
        <path d="M60 150 C40 140 26 146 14 134 C26 132 22 122 32 120 C34 128 46 128 48 138 C52 132 56 140 60 144 Z" fill="#BBB256" stroke="#2B0F33" stroke-width="2.5" stroke-linejoin="round"/>
        <path d="M60 128 C80 118 94 124 106 112 C94 110 98 100 88 98 C86 106 74 106 72 116 C68 110 64 118 60 122 Z" fill="#BBB256" stroke="#2B0F33" stroke-width="2.5" stroke-linejoin="round"/>
        <path d="M36 92 C36 72 84 72 84 92 C84 110 70 118 60 118 C50 118 36 110 36 92 Z" fill="#BBB256" stroke="#2B0F33" stroke-width="3"/>
        <path d="M42 86 L50 96 M54 84 L60 98 M66 84 L60 98 M78 86 L70 96 M46 100 L56 110 M74 100 L64 110" stroke="#2B0F33" stroke-width="2" stroke-linecap="round"/>
        <path d="M40 78 C34 54 30 36 34 18 M48 76 C46 50 44 30 48 10 M60 74 C60 48 60 26 60 6 M72 76 C74 50 76 30 72 10 M80 78 C86 54 90 36 86 18" stroke="#68367F" stroke-width="7" fill="none" stroke-linecap="round"/>
        <path d="M44 78 C40 58 38 42 42 26 M54 76 C54 52 52 34 54 16 M66 76 C66 52 68 34 66 16 M76 78 C80 58 82 42 78 26" stroke="#C4155F" stroke-width="4" fill="none" stroke-linecap="round"/>
        <path d="M36 80 C50 70 70 70 84 80" stroke="#2B0F33" stroke-width="3" fill="none" stroke-linecap="round"/>
      </svg>'''

SNUFF = '''<svg viewBox="0 0 140 110" aria-hidden="true">
        <ellipse cx="70" cy="82" rx="58" ry="18" fill="#68367F" stroke="#2B0F33" stroke-width="3"/>
        <rect x="12" y="58" width="116" height="24" fill="#68367F"/>
        <path d="M12 58 V82 M128 58 V82" stroke="#2B0F33" stroke-width="3"/>
        <ellipse cx="70" cy="58" rx="58" ry="18" fill="#F9AF08" stroke="#2B0F33" stroke-width="3"/>
        <g transform="rotate(-14 70 40)">
          <ellipse cx="70" cy="44" rx="60" ry="18" fill="#C4155F" stroke="#2B0F33" stroke-width="3"/>
          <rect x="10" y="30" width="120" height="14" fill="#C4155F"/>
          <path d="M10 30 V44 M130 30 V44" stroke="#2B0F33" stroke-width="3"/>
          <ellipse cx="70" cy="30" rx="60" ry="18" fill="#C4155F" stroke="#2B0F33" stroke-width="3"/>
          <ellipse cx="70" cy="30" rx="40" ry="10" fill="none" stroke="#F9AF08" stroke-width="3"/>
          <text x="70" y="35" text-anchor="middle" font-family="Archivo Black, Arial Black, sans-serif" font-size="14" fill="#FFFFFF">SNUFF</text>
        </g>
      </svg>'''

RAIN = '''<div class="rain">
        <strong>Pack for Scotland</strong>
        <ul>
          <li>Rain boots</li><li>Rain coat</li><li>Layers</li><li>No heels needed</li>
        </ul>
        <span style="font-size:15px">Cold outside, warm once everyone's dancing. More weather intel closer to the date.</span>
      </div>'''

FONTS = '<link rel="preconnect" href="https://fonts.googleapis.com">\n<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo+Black&family=Bricolage+Grotesque:opsz,wght@12..96,400;12..96,600;12..96,800&family=Space+Mono:wght@400;700&display=swap">\n<link rel="stylesheet" href="styles.css">'


def nav(current):
    items = []
    for fname, href, label, _ in PAGES:
        cur = ' aria-current="page"' if fname == current else ''
        cls = ' class="btn"' if fname == "rsvp.html" else ''
        items.append(f'        <li><a{cls} href="{href}"{cur}>{label}</a></li>')
    return "\n".join(items)


def page(fname, title, body):
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{title}</title>
<meta name="description" content="Ktizzle and Mattyrizz are getting married at Blairmore Millhouse, Inverness, 26 to 28 May 2028.">
{FONTS}
</head>
<body>
<header class="site">
  <div class="wrap">
    <a class="logo" href="./"><span>KT&nbsp;+&nbsp;MR</span> Rizz Airways</a>
    <nav aria-label="Main">
      <ul>
{nav(fname)}
      </ul>
    </nav>
  </div>
</header>
<main>
{body}
</main>
<footer class="site">
  <div class="wrap">
    <span class="mono">Rizz Airways &middot; KT2028 &middot; INV</span>
    <span class="mono">Questions? Text Katie or Matt.</span>
  </div>
</footer>
<script src="site.js"></script>
</body>
</html>
'''


def main():
    for d in (DIST, PREVIEW):
        shutil.rmtree(d, ignore_errors=True)
        os.makedirs(d)
    for fname, _, _, title in PAGES:
        body = open(os.path.join(SRC, fname)).read()
        body = body.replace("{{THISTLE}}", THISTLE).replace("{{SNUFF}}", SNUFF).replace("{{RAIN}}", RAIN)
        html = page(fname, title, body)
        open(os.path.join(DIST, fname), "w").write(html)
        if fname == "index.html":
            frag = html
            for pat in [r"<!doctype html>\n", r'<html lang="en">\n', r"<head>\n", r'<meta charset="utf-8">\n',
                        r'<meta name="viewport"[^>]*>\n', r"</head>\n", r"<body>\n", r"</body>\n", r"</html>\n"]:
                frag = re.sub(pat, "", frag, count=1)
            frag = frag.replace("</title>", '</title>\n<meta name="claude:viewport-fit-sides" content="cover">', 1)
            open(os.path.join(PREVIEW, fname), "w").write(frag)
        else:
            open(os.path.join(PREVIEW, fname), "w").write(html)
    for asset in ("styles.css", "site.js"):
        shutil.copy(os.path.join(ROOT, asset), os.path.join(DIST, asset))
        shutil.copy(os.path.join(ROOT, asset), os.path.join(PREVIEW, asset))
    print("built", os.listdir(DIST))


main()
