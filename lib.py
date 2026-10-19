"""Shared helpers for building the profile SVGs (no network access, everything local)."""
import base64, io, os, re
from fontTools.ttLib import TTFont
from PIL import Image

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
BUILD = os.path.join(ROOT, "tests", "build")
FONT_SRC = "/mnt/skills/examples/canvas-design/canvas-fonts/"
ICON_ROOT = "/usr/local/lib/python3.12/dist-packages/material/templates/.icons"

NAVY, BLUE, RED = "#070b16", "#247bff", "#ff354f"
INK, MUTED, BLUE_L = "#e9eefc", "#9aa8c9", "#6aa3ff"
CARD = "#0c1428"

DISP = "'Bricolage Grotesque','Segoe UI',Helvetica,Arial,sans-serif"
MONO = "'JetBrains Mono',ui-monospace,SFMono-Regular,Menlo,Consolas,'Liberation Mono',monospace"

_FONTS = {
    "bg-bold": ("Bricolage Grotesque", 700, "BricolageGrotesque-Bold.ttf"),
    "bg-regular": ("Bricolage Grotesque", 400, "BricolageGrotesque-Regular.ttf"),
    "jbm-regular": ("JetBrains Mono", 400, "JetBrainsMono-Regular.ttf"),
    "jbm-bold": ("JetBrains Mono", 700, "JetBrainsMono-Bold.ttf"),
}
_ttf_cache = {}


def b64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()


def font_face_css(keys):
    out = []
    for k in keys:
        fam, wt, _ = _FONTS[k]
        out.append("@font-face{font-family:'%s';font-weight:%d;font-style:normal;"
                   "src:url(data:font/woff2;base64,%s) format('woff2');}" % (fam, wt, b64(os.path.join(BUILD, k + ".woff2"))))
    return "".join(out)


def measure(key, text, size, spacing=0.0):
    """Advance width (no kerning) using the real font file."""
    if key not in _ttf_cache:
        t = TTFont(FONT_SRC + _FONTS[key][2])
        _ttf_cache[key] = (t.getBestCmap(), t["hmtx"], t["head"].unitsPerEm)
    cmap, hmtx, upm = _ttf_cache[key]
    w = 0
    for ch in text:
        g = cmap.get(ord(ch), ".notdef")
        w += hmtx[g][0]
    return w * size / upm + spacing * len(text)


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def png_data_uri(name, target_h):
    """Downscaled (alpha-preserving) copy of an original asset for embedding; originals stay untouched in assets/."""
    im = Image.open(os.path.join(ROOT, "assets", name)).convert("RGBA")
    w = round(im.width * target_h / im.height)
    im = im.resize((w, target_h), Image.LANCZOS)
    buf = io.BytesIO()
    im.save(buf, "PNG", optimize=True)
    return "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode(), im.width, im.height


def icon(lib, name):
    """Return (viewBox, [path d...]) from a locally bundled icon set (simple / fontawesome/brands / material)."""
    sub = {"simple": "simple", "fa": "fontawesome/brands", "mdi": "material"}[lib]
    svg = open(os.path.join(ICON_ROOT, sub, name + ".svg"), encoding="utf-8").read()
    vb = re.search(r'viewBox="([^"]+)"', svg).group(1)
    ds = re.findall(r'<path[^>]*\sd="([^"]+)"', svg)
    return vb, ds


def symbol(sym_id, lib, name, color=None):
    vb, ds = icon(lib, name)
    fill = ' fill="%s"' % color if color else ""
    return '<symbol id="%s" viewBox="%s">%s</symbol>' % (sym_id, vb, "".join('<path d="%s"%s/>' % (d, fill) for d in ds))


def base_defs(p, w, h, rx, fonts):
    """Common defs: fonts/css shell is added by caller; here patterns, border gradient, clip."""
    return (
        '<pattern id="%s-dots" width="20" height="20" patternUnits="userSpaceOnUse">'
        '<circle cx="2" cy="2" r="1" fill="%s" fill-opacity=".22"/></pattern>'
        '<linearGradient id="%s-border" x1="0" y1="0" x2="1" y2="1">'
        '<stop offset="0" stop-color="%s"/><stop offset=".55" stop-color="%s" stop-opacity=".25"/>'
        '<stop offset="1" stop-color="%s"/></linearGradient>'
        '<linearGradient id="%s-accent" x1="0" y1="0" x2="1" y2="0">'
        '<stop offset="0" stop-color="%s"/><stop offset="1" stop-color="%s"/></linearGradient>'
        '<clipPath id="%s-clip"><rect width="%d" height="%d" rx="%d"/></clipPath>'
    ) % (p, BLUE, p, BLUE, BLUE, RED, p, BLUE, RED, p, w, h, rx)


def frame(p, w, h, rx):
    return ('<rect width="%d" height="%d" rx="%d" fill="%s"/>'
            '<rect width="%d" height="%d" rx="%d" fill="url(#%s-dots)"/>') % (w, h, rx, NAVY, w, h, rx, p)


def border(p, w, h, rx, sw=1.5):
    o = sw / 2
    return '<rect x="%.2f" y="%.2f" width="%.2f" height="%.2f" rx="%.2f" fill="none" stroke="url(#%s-border)" stroke-width="%s"/>' % (
        o, o, w - sw, h - sw, rx - o, p, sw)


def radial(gid, color, opacity):
    return ('<radialGradient id="%s"><stop offset="0" stop-color="%s" stop-opacity="%s"/>'
            '<stop offset="1" stop-color="%s" stop-opacity="0"/></radialGradient>') % (gid, color, opacity, color)


REDUCED = "@media (prefers-reduced-motion: reduce){*{animation:none !important}}"


def svg_open(w, h, tid, did, title, desc):
    return ('<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="%d" height="%d" '
            'viewBox="0 0 %d %d" role="img" aria-labelledby="%s %s">'
            '<title id="%s">%s</title><desc id="%s">%s</desc>') % (w, h, w, h, tid, did, tid, esc(title), did, esc(desc))
