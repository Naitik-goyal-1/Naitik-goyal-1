import math
from lib import *
from build_a import write, mdi_path


# ------------------------------------------------------------------ ID CARD
def build_id():
    W, H, P = 1000, 760, "idc"
    img, iw, ih = png_data_uri("id.png", 560)
    ph = 280
    pw_ = round(iw * ph / ih)
    # decorative barcode (seeded, encodes nothing)
    seed, x, bars = 7, -108, ""
    while x < 106:
        seed = (seed * 1103515245 + 12345) & 0x7FFFFFFF
        bw = 1 + (seed >> 8) % 4
        seed = (seed * 1103515245 + 12345) & 0x7FFFFFFF
        gap = 1 + (seed >> 8) % 3
        bars += '<rect x="%d" y="536" width="%d" height="26" fill="%s" fill-opacity=".85"/>' % (x, bw, INK)
        x += bw + gap + 1
    css = (font_face_css(["bg-bold", "jbm-regular", "jbm-bold"]) + """
.disp{font-family:%s;font-weight:700}.mono{font-family:%s;font-weight:400}.monob{font-family:%s;font-weight:700}
.i-drop{animation:i-drop 1.25s both}
@keyframes i-drop{0%%{transform:translateY(-110px);animation-timing-function:cubic-bezier(.55,0,.85,.55)}52%%{transform:translateY(0);animation-timing-function:cubic-bezier(.2,.6,.4,1)}72%%{transform:translateY(9px);animation-timing-function:ease-in-out}88%%{transform:translateY(-3px);animation-timing-function:ease-in-out}100%%{transform:translateY(0)}}
.i-swing{transform-origin:0 0;animation:i-settle 3.6s ease-in-out .5s both,i-sway 3.2s ease-in-out 4.1s infinite alternate forwards}
@keyframes i-settle{0%%{transform:rotate(0deg)}20%%{transform:rotate(-6deg)}42%%{transform:rotate(4deg)}62%%{transform:rotate(-3deg)}80%%{transform:rotate(2.3deg)}100%%{transform:rotate(-1.7deg)}}
@keyframes i-sway{from{transform:rotate(-1.7deg)}to{transform:rotate(1.7deg)}}
.i-sweep{animation:i-sweep 5.5s ease-in-out 1.8s infinite both}
@keyframes i-sweep{0%%{transform:translateX(-120px)}38%%{transform:translateX(520px)}100%%{transform:translateX(520px)}}
.i-shadow{animation:i-sh 1.25s ease-out both}@keyframes i-sh{from{opacity:0}to{opacity:1}}
""" % (DISP, MONO, MONO) + REDUCED)
    s = svg_open(W, H, "idc-title", "idc-desc", "Developer ID illustration",
                 "Illustrated hanging lanyard card with portrait, name NAITIK GOYAL, role STUDENT DEVELOPER and MITS GWALIOR. "
                 "The barcode is purely decorative and encodes no information. It is not an official identification document.")
    s += "<defs><style>%s</style>" % css + base_defs(P, W, H, 28, None)
    s += radial("idc-glow-blue", BLUE, .34) + radial("idc-glow-red", RED, .30) + radial("idc-photo-blue", BLUE, .55) + radial("idc-photo-red", RED, .45)
    s += ('<linearGradient id="idc-metal" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#f4f6fc"/><stop offset=".35" stop-color="#aab5cd"/>'
          '<stop offset=".7" stop-color="#6c7896"/><stop offset="1" stop-color="#d3daea"/></linearGradient>'
          '<linearGradient id="idc-card-fill" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#101a38"/><stop offset="1" stop-color="#0a1020"/></linearGradient>'
          '<linearGradient id="idc-foil-grad" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="%s" stop-opacity=".16"/><stop offset=".5" stop-color="#fff" stop-opacity="0"/>'
          '<stop offset="1" stop-color="%s" stop-opacity=".18"/></linearGradient>'
          '<linearGradient id="idc-sweep-grad" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".5" stop-color="#fff" stop-opacity=".2"/>'
          '<stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>'
          '<pattern id="idc-foil" width="7" height="7" patternUnits="userSpaceOnUse" patternTransform="rotate(35)"><rect width="7" height="1.6" fill="#fff" fill-opacity=".05"/></pattern>'
          '<pattern id="idc-weave" width="5" height="5" patternUnits="userSpaceOnUse"><path d="M0 5L5 0" stroke="#fff" stroke-opacity=".07"/></pattern>'
          '<clipPath id="idc-card-clip"><rect x="-170" y="100" width="340" height="480" rx="28"/></clipPath>'
          '<clipPath id="idc-photo-clip"><rect x="-138" y="144" width="276" height="%d" rx="20"/></clipPath>') % (BLUE, RED, ph)
    s += "</defs>"
    s += '<g clip-path="url(#idc-clip)">' + frame(P, W, H, 28)
    s += '<circle cx="150" cy="420" r="330" fill="url(#idc-glow-blue)"/><circle cx="850" cy="430" r="330" fill="url(#idc-glow-red)"/>'
    s += '<circle cx="500" cy="420" r="300" fill="none" stroke="url(#idc-border)" stroke-width="1.2" stroke-dasharray="3 8" opacity=".6"/>'
    s += '<ellipse class="i-shadow" cx="500" cy="738" rx="160" ry="11" fill="#000" fill-opacity=".45"/>'
    s += '<g transform="translate(500,130)"><g class="i-drop"><g class="i-swing">'
    # strap
    s += ('<rect x="-15" y="-300" width="30" height="326" fill="#111b3b"/><rect x="-15" y="-300" width="30" height="326" fill="url(#idc-weave)"/>'
          '<rect x="-15" y="-300" width="3.5" height="326" fill="%s"/><rect x="11.5" y="-300" width="3.5" height="326" fill="%s"/>'
          '<rect x="-1.5" y="-300" width="3" height="326" fill="%s" fill-opacity=".8"/>') % (RED, RED, BLUE)
    # card
    s += '<rect x="-170" y="100" width="340" height="480" rx="28" fill="url(#idc-card-fill)"/>'
    s += '<g clip-path="url(#idc-card-clip)"><rect x="-170" y="100" width="340" height="480" fill="url(#idc-foil)"/>'
    s += '<rect x="-170" y="100" width="340" height="480" fill="url(#idc-foil-grad)"/>'
    s += '<rect x="-170" y="100" width="340" height="480" fill="url(#idc-dots)"/>'
    # photo
    s += '<g clip-path="url(#idc-photo-clip)"><rect x="-138" y="144" width="276" height="%d" fill="#09101f"/>' % ph
    s += '<circle cx="-70" cy="300" r="170" fill="url(#idc-photo-blue)"/><circle cx="85" cy="330" r="150" fill="url(#idc-photo-red)"/>'
    s += '<image x="%.1f" y="144" width="%d" height="%d" href="%s" xlink:href="%s" preserveAspectRatio="xMidYMid meet"/></g>' % (-pw_ / 2, pw_, ph, img, img)
    s += '<rect x="-138" y="144" width="276" height="%d" rx="20" fill="none" stroke="url(#idc-border)" stroke-width="1.6"/>' % ph
    # text
    s += '<text class="disp" x="0" y="466" font-size="34" fill="%s" text-anchor="middle" letter-spacing="-.3">NAITIK GOYAL</text>' % INK
    s += '<text class="monob" x="0" y="494" font-size="14" fill="%s" text-anchor="middle" letter-spacing="2.5">STUDENT DEVELOPER</text>' % BLUE_L
    s += '<text class="mono" x="0" y="518" font-size="13" fill="%s" text-anchor="middle" letter-spacing="3">MITS GWALIOR</text>' % MUTED
    s += bars
    # light sweep
    s += '<g class="i-sweep"><rect x="-260" y="90" width="70" height="500" fill="url(#idc-sweep-grad)" transform="skewX(-18)"/></g></g>'
    s += '<rect x="-170" y="100" width="340" height="480" rx="28" fill="none" stroke="url(#idc-border)" stroke-width="2.2"/>'
    # slot, clasp, ring
    s += '<rect x="-30" y="110" width="60" height="12" rx="6" fill="#050914" stroke="#3a4670" stroke-width="1.2"/>'
    s += ('<rect x="-19" y="44" width="38" height="78" rx="16" fill="url(#idc-metal)" stroke="#59658a" stroke-width="1"/>'
          '<rect x="-8" y="60" width="16" height="46" rx="8" fill="#0a1020" stroke="#59658a" stroke-width="1"/>'
          '<circle cx="0" cy="28" r="17" fill="none" stroke="url(#idc-metal)" stroke-width="6"/>'
          '<circle cx="-5" cy="22" r="3" fill="#fff" fill-opacity=".55"/>')
    s += '</g></g></g></g>' + border(P, W, H, 28) + '</svg>'
    write("id-dashboard.svg", s)


# ------------------------------------------------------------------ CONNECT
def build_connect():
    W, H, P = 1000, 440, "connect"
    img, iw, ih = png_data_uri("right_pointing.png", 640)
    dh = 420
    dw = round(iw * dh / ih)
    ix, iy = 24, H - dh
    tipx, tipy = ix + .876 * dw, iy + .613 * dh
    plats = [("GitHub", "Code & repositories", "simple", "github", BLUE),
             ("LinkedIn", "Professional profile", "fa", "linkedin", BLUE_L),
             ("Instagram", "Social profile", "simple", "instagram", RED)]
    syms = "".join(symbol("connect-i-" + n.lower(), lib, nm) for n, _, lib, nm, _ in plats)
    css = (font_face_css(["bg-bold", "jbm-regular"]) + """
.disp{font-family:%s;font-weight:700}.mono{font-family:%s;font-weight:400}
.c-char{animation:c-char 1.2s cubic-bezier(.2,.8,.2,1) .2s both}
@keyframes c-char{from{opacity:0;transform:translateX(-26px)}to{opacity:1;transform:translateX(0)}}
.c-card{animation:c-in .8s cubic-bezier(.2,.8,.2,1) both}.c-card-1{animation-delay:.5s}.c-card-2{animation-delay:.7s}.c-card-3{animation-delay:.9s}
@keyframes c-in{from{opacity:0;transform:translateX(34px)}to{opacity:1;transform:translateX(0)}}
.c-head{animation:c-fade .8s ease-out .3s both}@keyframes c-fade{from{opacity:0;transform:translateY(8px)}to{opacity:1;transform:translateY(0)}}
.c-chev{opacity:.9;animation:c-nudge 1.8s ease-in-out infinite both}
.c-chev-2{animation-delay:.18s}.c-chev-3{animation-delay:.36s}
@keyframes c-nudge{0%%,100%%{opacity:.3;transform:translateX(0)}50%%{opacity:1;transform:translateX(8px)}}
""" % (DISP, MONO) + REDUCED)
    s = svg_open(W, H, "connect-title", "connect-desc", "Connect with Naitik Goyal",
                 "An illustrated portrait pointing to the right toward three platform cards: GitHub, LinkedIn and Instagram. "
                 "The actual clickable links are listed directly below this image in the README.")
    s += "<defs><style>%s</style>" % css + base_defs(P, W, H, 28, None)
    s += radial("connect-glow-blue", BLUE, .5) + radial("connect-glow-red", RED, .38) + syms + "</defs>"
    s += '<g clip-path="url(#connect-clip)">' + frame(P, W, H, 28)
    s += '<circle cx="190" cy="270" r="280" fill="url(#connect-glow-blue)"/><circle cx="940" cy="400" r="260" fill="url(#connect-glow-red)"/>'
    s += '<g class="c-char"><image x="%d" y="%d" width="%d" height="%d" href="%s" xlink:href="%s" preserveAspectRatio="xMidYMid meet"/></g>' % (ix, iy, dw, dh, img, img)
    # chevrons from fingertip toward cards
    for k in range(3):
        x = tipx + 26 + k * 24
        s += ('<g class="c-chev c-chev-%d"><polyline points="%.1f,%.1f %.1f,%.1f %.1f,%.1f" fill="none" stroke="url(#connect-accent)" stroke-width="4.5" '
              'stroke-linecap="round" stroke-linejoin="round"/></g>') % (k + 1, x, tipy - 13, x + 11, tipy, x, tipy + 13)
    s += '<g class="c-head"><text class="mono" x="480" y="72" font-size="13" fill="%s" letter-spacing="3">FIND ME ON</text>' % BLUE_L
    s += '<text class="disp" x="478" y="116" font-size="46" fill="%s" letter-spacing="-.8">Let&#8217;s connect</text></g>' % INK
    top = round(tipy - 36 - 86)
    for i, (name, sub, lib, nm, acc) in enumerate(plats):
        y = top + i * 86
        cy = y + 36
        s += '<g class="c-card c-card-%d">' % (i + 1)
        s += '<rect x="480" y="%d" width="488" height="72" rx="20" fill="%s" fill-opacity=".94" stroke="%s" stroke-opacity=".7" stroke-width="1.4"/>' % (y, CARD, acc)
        s += '<rect x="480" y="%d" width="6" height="72" rx="3" fill="%s" clip-path="inset(0 round 3px)"/>' % (y, acc) if False else ''
        s += '<circle cx="530" cy="%d" r="27" fill="#0f1a36" stroke="%s" stroke-width="2"/>' % (cy, acc)
        s += '<use href="#connect-i-%s" xlink:href="#connect-i-%s" x="516" y="%d" width="28" height="28" fill="%s"/>' % (name.lower(), name.lower(), cy - 14, INK)
        s += '<text class="disp" x="574" y="%d" font-size="27" fill="%s">%s</text>' % (cy - 2, INK, name)
        s += '<text class="mono" x="574" y="%d" font-size="13" fill="%s">%s</text></g>' % (cy + 21, MUTED, esc(sub))
    s += '<text class="mono" x="480" y="%d" font-size="13" fill="%s">Clickable links are listed right below this image.</text>' % (top + 3 * 86 + 18, MUTED)
    s += '</g>' + border(P, W, H, 28) + '</svg>'
    write("connect.svg", s)


if __name__ == "__main__":
    build_id(); build_connect()
