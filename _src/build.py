import os, re, shutil

ROOT = os.path.dirname(os.path.abspath(__file__))
SRC = ROOT
DIST = os.path.dirname(ROOT)  # repo root
PREVIEW = os.path.join(ROOT, "_preview")

PAGES = [
    ("index.html", "./", "The Lore", "Ktizzle and Mattyrizz"),
    ("plan.html", "plan.html", "The Plan", "The Plan · Ktizzle and Mattyrizz"),
    ("guide.html", "guide.html", "Survival Guide", "Survival Guide · Ktizzle and Mattyrizz"),
    ("advice.html", "advice.html", "Unsolicited Advice", "Unsolicited Advice · Ktizzle and Mattyrizz"),
    ("rsvp.html", "rsvp.html", "RSVP", "RSVP · Ktizzle and Mattyrizz"),
]

THISTLE = ''

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

FONTS = '<link rel="preconnect" href="https://fonts.googleapis.com">\n<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo+Black&family=Bricolage+Grotesque:opsz,wght@12..96,400;12..96,600;12..96,800&family=Space+Mono:wght@400;700&display=swap">\n<link rel="stylesheet" href="styles.css?v=3">'


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
    <span class="mono">Rizz Airways &middot; KM2028 &middot; INV</span>
    <span class="mono">Questions? Text Katie or Matt.</span>
  </div>
</footer>
<script src="site.js?v=3"></script>
</body>
</html>
'''


def main():
    shutil.rmtree(PREVIEW, ignore_errors=True)
    os.makedirs(PREVIEW)
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
        shutil.copy(os.path.join(DIST, asset), os.path.join(PREVIEW, asset))
    print("built", os.listdir(DIST))


main()
