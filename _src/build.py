"""Builds the site pages from the page sources in this folder.

Run: python3 _src/build.py
Writes finished pages to the repo root, plus a preview copy in _src/_preview/.
"""
import os, re, shutil

ROOT = os.path.dirname(os.path.abspath(__file__))
SRC = ROOT
DIST = os.path.dirname(ROOT)  # repo root
PREVIEW = os.path.join(ROOT, "_preview")
VERSION = "4"

# (file, href, nav label, page title)
PAGES = [
    ("index.html", "./", "The Lore", "Ktizzle and Mattyrizz"),
    ("plan.html", "plan.html", "The Plan", "The Plan · Ktizzle and Mattyrizz"),
    ("guide.html", "guide.html", "Survival Guide", "Survival Guide · Ktizzle and Mattyrizz"),
    ("advice.html", "advice.html", "Advice", "Unsolicited Advice · Ktizzle and Mattyrizz"),
    ("rsvp.html", "rsvp.html", "RSVP", "RSVP · Ktizzle and Mattyrizz"),
]

D_THISTLE = '<path d="M30 88 V52"/><path d="M30 74 C22 70 18 74 12 68 C18 66 16 60 22 60 C22 64 28 66 30 70"/><path d="M30 64 C38 60 42 64 48 58 C42 56 44 50 38 50 C38 54 32 56 30 60"/><path d="M18 42 C18 30 42 30 42 42 C42 52 36 56 30 56 C24 56 18 52 18 42 Z"/><path d="M22 40 L28 48 M30 38 L30 50 M38 40 L32 48"/><path d="M20 32 C16 22 14 14 16 6 M25 30 C24 20 24 12 26 4 M30 30 V2 M35 30 C36 20 36 12 34 4 M40 32 C44 22 46 14 44 6"/>'
D_COW = '<path d="M30 26 C20 26 8 22 6 8 C12 14 20 16 28 18"/><path d="M60 26 C70 26 82 22 84 8 C78 14 70 16 62 18"/><ellipse cx="22" cy="34" rx="7" ry="4" transform="rotate(-20 22 34)"/><ellipse cx="68" cy="34" rx="7" ry="4" transform="rotate(20 68 34)"/><path d="M30 24 C28 48 34 64 45 70 C56 64 62 48 60 24 C52 20 38 20 30 24 Z"/><path d="M30 26 L34 38 L39 28 L44 40 L49 28 L54 38 L60 26"/><ellipse cx="45" cy="62" rx="10" ry="6"/><path d="M41 62 H41.5 M48.5 62 H49"/>'
D_TIN = '<path d="M8 40 V50 C8 62 72 62 72 50 V40"/><ellipse cx="40" cy="40" rx="32" ry="9"/><g transform="rotate(-12 40 22)"><ellipse cx="40" cy="22" rx="33" ry="9"/><path d="M7 22 V28 C7 38 73 38 73 28 V22"/><path d="M34 20 C34 16 40 16 40 20 C40 16 46 16 46 20 C46 24 40 27 40 27 C40 27 34 24 34 20 Z"/></g>'
D_SHEEP = '<path d="M26 40 C22 32 30 24 38 28 C40 20 52 18 56 26 C62 20 74 24 72 34 C80 38 78 50 70 52 C70 60 58 62 54 56 C48 62 36 62 34 54 C26 56 20 46 26 40 Z"/><ellipse cx="18" cy="40" rx="9" ry="11"/><path d="M10 34 C6 32 6 28 10 28 M26 34 C30 32 30 28 26 28"/><path d="M15 39 H15.5 M21 39 H21.5"/><path d="M38 58 V68 M50 59 V68 M62 58 V68"/>'


def svg(style, box, body):
    return f'<svg class="doodle" aria-hidden="true" style="{style}" viewBox="{box}">{body}</svg>'


HERO_DOODLES = "\n      ".join([
    svg("top:22px;left:26px;width:58px;height:88px", "0 0 60 90", D_THISTLE),
    svg("top:26px;right:24px;width:92px;height:80px", "0 0 90 80", D_COW),
    svg("bottom:22px;left:24px;width:84px;height:64px", "0 0 80 64", D_TIN),
    svg("bottom:20px;right:24px;width:92px;height:72px", "0 0 90 70", D_SHEEP),
])

PAGE_DOODLES = {
    "plan.html": [("top:36px;left:6%;width:84px;height:64px", "0 0 80 64", D_TIN), ("bottom:30px;right:6%;width:92px;height:72px", "0 0 90 70", D_SHEEP)],
    "guide.html": [("top:30px;left:6%;width:92px;height:80px", "0 0 90 80", D_COW), ("bottom:30px;right:6%;width:58px;height:88px", "0 0 60 90", D_THISTLE)],
    "rsvp.html": [("top:36px;left:6%;width:58px;height:88px", "0 0 60 90", D_THISTLE), ("bottom:30px;right:6%;width:84px;height:64px", "0 0 80 64", D_TIN)],
    "advice.html": [("top:30px;left:6%;width:92px;height:72px", "0 0 90 70", D_SHEEP), ("bottom:30px;right:6%;width:92px;height:80px", "0 0 90 80", D_COW)],
}

FONTS = f'''<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Luckiest+Guy&family=Bricolage+Grotesque:opsz,wght@12..96,400;12..96,600;12..96,800&display=swap">
<link rel="stylesheet" href="styles.css?v={VERSION}">'''


def nav(current):
    links = []
    for fname, href, label, _ in PAGES:
        cur = ' aria-current="page"' if fname == current else ''
        links.append(f'    <a href="{href}"{cur}>{label}</a>')
    brand = '    <a class="brand" href="./">Ktizzle + Mattyrizz</a>'
    return "\n".join(links[:2] + [brand] + links[2:])


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
<header class="top gut">
  <nav class="wrap" aria-label="Main">
{nav(fname)}
  </nav>
</header>
<main>
{body}
</main>
<footer class="site gut">Rizz Airways &middot; KM2028 &middot; INV &middot; Questions? Text Katie or Matt.</footer>
<script src="site.js?v={VERSION}"></script>
</body>
</html>
'''


def main():
    shutil.rmtree(PREVIEW, ignore_errors=True)
    os.makedirs(PREVIEW)
    for fname, _, _, title in PAGES:
        body = open(os.path.join(SRC, fname)).read()
        doodles = "\n      ".join(svg(*d) for d in PAGE_DOODLES.get(fname, []))
        body = body.replace("{{HERO_DOODLES}}", HERO_DOODLES).replace("{{PAGE_DOODLES}}", doodles)
        html = page(fname, title, body)
        open(os.path.join(DIST, fname), "w").write(html)
        # Preview copy: asset links without version query; home page as a fragment.
        prev = html.replace(f"styles.css?v={VERSION}", "styles.css").replace(f"site.js?v={VERSION}", "site.js")
        if fname == "index.html":
            for pat in [r"<!doctype html>\n", r'<html lang="en">\n', r"<head>\n", r'<meta charset="utf-8">\n',
                        r'<meta name="viewport"[^>]*>\n', r"</head>\n", r"<body>\n", r"</body>\n", r"</html>\n"]:
                prev = re.sub(pat, "", prev, count=1)
            prev = prev.replace("</title>", '</title>\n<meta name="claude:viewport-fit-sides" content="cover">', 1)
        open(os.path.join(PREVIEW, fname), "w").write(prev)
    for asset in ("styles.css", "site.js"):
        shutil.copy(os.path.join(DIST, asset), os.path.join(PREVIEW, asset))
    shutil.copytree(os.path.join(DIST, "img"), os.path.join(PREVIEW, "img"))
    print("built", [p[0] for p in PAGES])


main()
