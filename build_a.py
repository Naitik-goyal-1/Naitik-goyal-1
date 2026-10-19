import math
from lib import *

OUT = os.path.join(ROOT, "assets")


def write(name, s):
    with open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
        f.write(s)
    print(name, round(len(s.encode()) / 1024), "KB")


def mdi_path(name):
    return icon("mdi", name)[1][0]


# ------------------------------------------------------------------ HERO
def build_hero():
    W, H, P = 1000, 440, "hero"
    img, iw, ih = png_data_uri("id.png", 640)
    disp_h = 420
    disp_w = round(iw * disp_h / ih)  # keep aspect
    px, py = 585, H - disp_h
    # typing SMIL values
    cw = measure("jbm-regular", "H", 22)
    n = len("Hello, World!")
    vals = ";".join("%.1f" % (cw * i) for i in range(n + 1))
    cx_vals = ";".join("%.1f" % (76 + cw * i) for i in range(n + 1))
    tw = cw * n + 4
    pin, school = mdi_path("map-marker"), mdi_path("school")

    def pill(y, text, d):
        w = 44 + measure("jbm-regular", text, 14)
        return ('<g><rect x="56" y="%d" width="%.1f" height="32" rx="16" fill="#0e1730" stroke="%s" stroke-opacity=".45"/>'
                '<path d="%s" transform="translate(70,%d) scale(.75)" fill="%s"/>'
                '<text class="mono" x="96" y="%d" font-size="14" fill="%s">%s</text></g>') % (
            y, w, BLUE, d, y + 7, BLUE_L, y + 21, INK, esc(text))

    css = (font_face_css(["bg-bold", "bg-regular", "jbm-regular"]) + """
.disp{font-family:%s;font-weight:700}.reg{font-family:%s;font-weight:400}.mono{font-family:%s;font-weight:400}
.h-name{animation:h-rise 1.1s cubic-bezier(.2,.8,.2,1) .7s both}
@keyframes h-rise{from{transform:translateY(98px)}to{transform:translateY(0)}}
.h-line{transform-box:fill-box;transform-origin:0 50%%;animation:h-grow .9s cubic-bezier(.2,.8,.2,1) 1.4s both}
@keyframes h-grow{from{transform:scaleX(0)}to{transform:scaleX(1)}}
.h-role{opacity:0;animation:h-cycle 9s ease-in-out infinite both}
.h-role-1{opacity:1;animation-delay:1.9s}.h-role-2{animation-delay:4.9s}.h-role-3{animation-delay:7.9s}
@keyframes h-cycle{0%%{opacity:0;transform:translateY(20px)}5%%,30%%{opacity:1;transform:translateY(0)}35%%,100%%{opacity:0;transform:translateY(-20px)}}
.h-pitch{animation:h-fade .9s ease-out 1.8s both}.h-pills{animation:h-fade .9s ease-out 2.1s both}
@keyframes h-fade{from{opacity:0;transform:translateY(8px)}to{opacity:1;transform:translateY(0)}}
.h-portrait{animation:h-in 1.3s cubic-bezier(.2,.8,.2,1) .4s both}
@keyframes h-in{from{opacity:0;transform:translateX(38px)}to{opacity:1;transform:translateX(0)}}
.h-glow{animation:h-glow 7s ease-in-out infinite alternate}
@keyframes h-glow{from{opacity:.75}to{opacity:1}}
""" % (DISP, DISP, MONO) + REDUCED)

    s = svg_open(W, H, "hero-title", "hero-desc", "Naitik Goyal - Student Developer",
                 "Hero banner. Greeting: Hello, World! Name: Naitik Goyal. Rotating roles: Software Developer, Full-Stack Developer, "
                 "AI/ML Enthusiast. Pitch: Code with purpose. Build with vision. Innovate through technology. "
                 "Gwalior, Madhya Pradesh, India. Madhav Institute of Technology & Science, Gwalior. Illustrated portrait on the right.")
    s += "<defs><style>%s</style>" % css
    s += base_defs(P, W, H, 28, None)
    s += radial("hero-glow-blue", BLUE, .55) + radial("hero-glow-red", RED, .45) + radial("hero-glow-soft", BLUE, .18)
    s += '<clipPath id="hero-name-clip"><rect x="40" y="92" width="540" height="98"/></clipPath>'
    s += '<clipPath id="hero-role-clip"><rect x="40" y="198" width="540" height="50"/></clipPath>'
    s += '<clipPath id="hero-type-clip"><rect x="76" y="46" height="40" width="%.1f">' % tw
    s += '<animate attributeName="width" calcMode="discrete" values="%s" dur="1.5s" begin="0s" fill="freeze"/></rect></clipPath></defs>' % (
        ";".join("%.1f" % (cw * i) for i in range(n + 1)))
    s += '<g clip-path="url(#hero-clip)">' + frame(P, W, H, 28)
    s += '<circle class="h-glow" cx="650" cy="250" r="250" fill="url(#hero-glow-blue)"/>'
    s += '<circle class="h-glow" cx="925" cy="300" r="230" fill="url(#hero-glow-red)"/>'
    s += '<circle cx="200" cy="120" r="260" fill="url(#hero-glow-soft)"/>'
    # thin decorative arcs behind portrait
    s += ('<ellipse cx="770" cy="262" rx="215" ry="190" fill="none" stroke="url(#hero-border)" stroke-width="1.2" stroke-dasharray="3 7" opacity=".7"/>')
    s += ('<g class="h-portrait"><image x="%d" y="%d" width="%d" height="%d" href="%s" xlink:href="%s" preserveAspectRatio="xMidYMid meet"/></g>'
          % (px, py, disp_w, disp_h, img, img))
    # greeting (typed with SMIL)
    s += '<circle cx="62" cy="65" r="4.5" fill="%s"/>' % RED
    s += '<g clip-path="url(#hero-type-clip)"><text class="mono" x="76" y="73" font-size="22" fill="%s">Hello, World!</text></g>' % BLUE_L
    s += ('<rect x="76" y="52" width="2.5" height="26" fill="%s" opacity="0"><animate attributeName="x" calcMode="discrete" values="%s" dur="1.5s" begin="0s" fill="freeze"/>'
          '<animate attributeName="opacity" calcMode="discrete" values="1;0" keyTimes="0;1" dur="1.5s" begin="0s" fill="freeze"/></rect>') % (BLUE, cx_vals)
    # name
    s += '<g clip-path="url(#hero-name-clip)"><text class="disp h-name" x="54" y="164" font-size="80" fill="%s" letter-spacing="-1.5">Naitik Goyal</text></g>' % INK
    s += '<rect class="h-line" x="56" y="186" width="220" height="4" rx="2" fill="url(#hero-accent)"/>'
    # roles
    s += '<rect x="56" y="209" width="4" height="28" rx="2" fill="%s"/>' % RED
    for i, r in enumerate(["Software Developer", "Full-Stack Developer", "AI/ML Enthusiast"], 1):
        s += '<g clip-path="url(#hero-role-clip)"><text class="disp h-role h-role-%d" x="76" y="232" font-size="30" fill="%s">%s</text></g>' % (i, BLUE_L, r)
    # pitch
    s += ('<g class="h-pitch"><text class="reg" x="56" y="286" font-size="19" fill="%s">Code with purpose. Build with vision.</text>'
          '<text class="reg" x="56" y="311" font-size="19" fill="%s">Innovate through technology.</text></g>') % (INK, INK)
    s += '<g class="h-pills">%s%s</g>' % (pill(340, "Gwalior, Madhya Pradesh, India", pin),
                                          pill(380, "Madhav Institute of Technology & Science, Gwalior", school))
    s += '</g>' + border(P, W, H, 28) + '</svg>'
    write("hero.svg", s)


# ------------------------------------------------------------------ ABOUT
def build_about():
    W, H, P = 1000, 520, "about"
    interests = [
        ("laptop", ["Software Development", "& Problem Solving"], "Software Development & Problem Solving"),
        ("palette", ["UI/UX Design &", "Creative Designing"], "UI/UX Design & Creative Designing"),
        ("rocket-launch", ["Exploring New Technologies", "& Building Projects"], "Exploring New Technologies & Building Projects"),
    ]
    css_seg, css_slide, css_row = "", "", ""
    seg_kf = [
        "0%{transform:scaleX(0)}33.33%{transform:scaleX(1)}100%{transform:scaleX(1)}",
        "0%,33.33%{transform:scaleX(0)}66.66%{transform:scaleX(1)}100%{transform:scaleX(1)}",
        "0%,66.66%{transform:scaleX(0)}100%{transform:scaleX(1)}",
    ]
    for i in range(3):
        a, b = i * 33.333, (i + 1) * 33.333
        css_seg += "@keyframes a-seg%d{%s}" % (i, seg_kf[i])
        start = "0%{opacity:0;transform:translateX(26px)}" if i == 0 else "0%%,%.2f%%{opacity:0;transform:translateX(26px)}" % a
        fade_in = a + 2.5
        hold = b - 2.5
        css_slide += "@keyframes a-slide%d{%s%.2f%%{opacity:1;transform:translateX(0)}%.2f%%{opacity:1;transform:translateX(0)}%.2f%%,100%%{opacity:0;transform:translateX(-18px)}}" % (
            i, start, fade_in, hold, b if i < 2 else 100)
        # row highlight: INK while active, MUTED otherwise
        if i == 0:
            kf = "0%%,%.2f%%{fill:%s}%.2f%%,100%%{fill:%s}" % (b, INK, b + .01, MUTED)
        elif i == 1:
            kf = "0%%,%.2f%%{fill:%s}%.2f%%,%.2f%%{fill:%s}%.2f%%,100%%{fill:%s}" % (a - .01, MUTED, a, b, INK, b + .01, MUTED)
        else:
            kf = "0%%,%.2f%%{fill:%s}%.2f%%,100%%{fill:%s}" % (a - .01, MUTED, a, INK)
        css_row += "@keyframes a-row%d{%s}" % (i, kf)
        css_row += "@keyframes a-dot%d{%s}" % (i, kf.replace("fill:%s" % INK, "opacity:1").replace("fill:%s" % MUTED, "opacity:0"))
    css = (font_face_css(["bg-bold", "bg-regular", "jbm-regular"]) + """
.disp{font-family:%s;font-weight:700}.reg{font-family:%s;font-weight:400}.mono{font-family:%s;font-weight:400}
.a-seg{transform-box:fill-box;transform-origin:0 50%%}
.a-slide{opacity:0}.a-slide-0{opacity:1}
.a-seg-0{animation:a-seg0 12s linear infinite both}.a-seg-1{animation:a-seg1 12s linear infinite both}.a-seg-2{animation:a-seg2 12s linear infinite both}
.a-slide-0{animation:a-slide0 12s ease-in-out infinite both}.a-slide-1{animation:a-slide1 12s ease-in-out infinite both}.a-slide-2{animation:a-slide2 12s ease-in-out infinite both}
.a-row-0{animation:a-row0 12s step-end infinite both}.a-row-1{animation:a-row1 12s step-end infinite both}.a-row-2{animation:a-row2 12s step-end infinite both}
.a-dot{opacity:0}.a-dot-0{animation:a-dot0 12s step-end infinite both}.a-dot-1{animation:a-dot1 12s step-end infinite both}.a-dot-2{animation:a-dot2 12s step-end infinite both}
.a-intro{animation:a-fade .9s ease-out .1s both}
@keyframes a-fade{from{opacity:0;transform:translateY(8px)}to{opacity:1;transform:translateY(0)}}
""" % (DISP, DISP, MONO) + css_seg + css_slide + css_row + REDUCED)

    # intro text wrap with real metrics
    para = ("I'm a student developer at Madhav Institute of Technology & Science, Gwalior. I enjoy solving problems with code "
            "and turning ideas into working projects, from computer vision to full-stack web applications.")
    maxw = 392
    lines, cur = [], ""
    for wd in para.split():
        t = (cur + " " + wd).strip()
        if measure("bg-regular", t, 18) <= maxw:
            cur = t
        else:
            lines.append(cur)
            cur = wd
    lines.append(cur)

    s = svg_open(W, H, "about-title", "about-desc", "About Naitik Goyal",
                 "Introduction: student developer at Madhav Institute of Technology & Science, Gwalior. Interests carousel with three slides, "
                 "four seconds each: 1 Software Development & Problem Solving; 2 UI/UX Design & Creative Designing; "
                 "3 Exploring New Technologies & Building Projects.")
    s += "<defs><style>%s</style>" % css + base_defs(P, W, H, 28, None)
    s += radial("about-glow-blue", BLUE, .30) + radial("about-glow-red", RED, .26)
    s += '<linearGradient id="about-card-border" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="%s" stop-opacity=".9"/><stop offset="1" stop-color="%s" stop-opacity=".8"/></linearGradient>' % (BLUE, RED)
    s += '<clipPath id="about-right-clip"><rect x="516" y="32" width="452" height="456" rx="24"/></clipPath></defs>'
    s += '<g clip-path="url(#about-clip)">' + frame(P, W, H, 28)
    s += '<circle cx="60" cy="40" r="300" fill="url(#about-glow-blue)"/><circle cx="960" cy="500" r="300" fill="url(#about-glow-red)"/>'
    # left card
    s += '<rect x="32" y="32" width="460" height="456" rx="24" fill="%s" fill-opacity=".92" stroke="url(#about-card-border)" stroke-opacity=".5" stroke-width="1.2"/>' % CARD
    s += '<g class="a-intro"><text class="mono" x="64" y="84" font-size="14" fill="%s" letter-spacing="3">ABOUT ME</text>' % BLUE_L
    s += '<rect x="64" y="98" width="46" height="4" rx="2" fill="url(#about-accent)"/>'
    s += '<text class="disp" x="64" y="154" font-size="42" fill="%s" letter-spacing="-.5">Hi, I&#8217;m Naitik.</text>' % INK
    for i, ln in enumerate(lines):
        s += '<text class="reg" x="64" y="%d" font-size="18" fill="%s">%s</text>' % (200 + i * 28, INK, esc(ln))
    py = 200 + len(lines) * 28 + 24
    s += '<rect x="64" y="%d" width="3" height="52" rx="1.5" fill="%s"/>' % (py, RED)
    s += '<text class="mono" x="80" y="%d" font-size="14" fill="%s">Code with purpose. Build with vision.</text>' % (py + 20, MUTED)
    s += '<text class="mono" x="80" y="%d" font-size="14" fill="%s">Innovate through technology.</text></g>' % (py + 42, MUTED)
    # right card
    s += '<rect x="516" y="32" width="452" height="456" rx="24" fill="%s" fill-opacity=".92" stroke="url(#about-card-border)" stroke-opacity=".5" stroke-width="1.2"/>' % CARD
    s += '<text class="mono" x="548" y="84" font-size="14" fill="%s" letter-spacing="3">INTERESTS</text>' % BLUE_L
    segw = (452 - 64 - 20) / 3
    for i in range(3):
        x = 548 + i * (segw + 10)
        s += '<rect x="%.1f" y="104" width="%.1f" height="6" rx="3" fill="#1b2748"/>' % (x, segw)
        s += '<rect class="a-seg a-seg-%d" x="%.1f" y="104" width="%.1f" height="6" rx="3" fill="url(#about-accent)"/>' % (i, x, segw)
    cxm = 742
    for i, (ic, ls, full) in enumerate(interests):
        s += '<g class="a-slide a-slide-%d">' % i
        s += '<circle cx="%d" cy="188" r="46" fill="#0f1a36" stroke="url(#about-accent)" stroke-width="2"/>' % cxm
        s += '<path d="%s" transform="translate(%d,%d) scale(2)" fill="%s"/>' % (mdi_path(ic), cxm - 24, 188 - 24, INK)
        s += '<text class="mono" x="%d" y="262" font-size="13" fill="%s" text-anchor="middle" letter-spacing="2">0%d / 03</text>' % (cxm, MUTED, i + 1)
        for j, t in enumerate(ls):
            s += '<text class="disp" x="%d" y="%d" font-size="27" fill="%s" text-anchor="middle">%s</text>' % (cxm, 300 + j * 34, INK, esc(t))
        s += '</g>'
    # static-friendly list (always visible)
    s += '<line x1="548" y1="352" x2="936" y2="352" stroke="%s" stroke-opacity=".25"/>' % BLUE
    for i, (_, _, full) in enumerate(interests):
        y = 384 + i * 36
        s += '<circle class="a-dot a-dot-%d" cx="556" cy="%d" r="4" fill="%s"/>' % (i, y - 5, RED)
        s += '<text class="mono a-row-%d" x="574" y="%d" font-size="14" fill="%s">%s</text>' % (i, y, INK, esc(full))
    s += '</g>' + border(P, W, H, 28) + '</svg>'
    write("about-life.svg", s)


# ------------------------------------------------------------------ STACK
def build_stack():
    W, P = 1000, "stack"
    TILT = -12
    CX, CY = 500, 236
    A = [("C++", "cplusplus", "simple"), ("Python", "python", "simple"), ("JavaScript", "javascript", "simple")]
    B = [("React", "react", "simple"), ("Node.js", "nodedotjs", "simple"), ("Express.js", "express", "simple")]
    C = [("SQL", "database", "mdi"), ("PostgreSQL", "postgresql", "simple"), ("Supabase", "supabase", "simple"),
         ("Git", "git", "simple"), ("GitHub", "github", "simple"), ("REST APIs", "api", "mdi")]
    orbits = [  # items, rx, ry, theta0, direction(sweep), dur, accent
        (A, 175, 72, 30, 1, 45, BLUE), (B, 300, 122, 100, 0, 70, RED), (C, 410, 170, 160, 1, 100, BLUE_L)]
    FS = 15

    def pw(label):
        return 40 + measure("jbm-regular", label, FS) + 12

    syms = {}
    for items, *_ in orbits:
        for lab, nm, lib in items:
            syms[lab] = symbol("stack-i-" + re.sub(r"[^a-z0-9]", "", lab.lower().replace("+", "p")), lib, nm)
    sid = lambda lab: "stack-i-" + re.sub(r"[^a-z0-9]", "", lab.lower().replace("+", "p"))

    def pill_markup(lab, accent, x, y, extra=""):
        w = pw(lab)
        return ('<g transform="translate(%.1f,%.1f)">%s<rect x="%.1f" y="-19" width="%.1f" height="38" rx="19" fill="%s" stroke="%s" stroke-opacity=".8" stroke-width="1.4"/>'
                '<use href="#%s" xlink:href="#%s" x="%.1f" y="-10" width="20" height="20" fill="%s"/>'
                '<text class="mono" x="%.1f" y="5.5" font-size="%d" fill="%s">%s</text>%s</g>') % (
            x, y, "", -w / 2, w, CARD, accent, sid(lab), sid(lab), -w / 2 + 12, INK, -w / 2 + 38, FS, INK, esc(lab), extra)

    body = ""
    # orbit paths
    for items, rx, ry, th0, d, dur, acc in orbits:
        body += ('<ellipse cx="%d" cy="%d" rx="%d" ry="%d" transform="rotate(%d %d %d)" fill="none" stroke="%s" stroke-opacity=".5" stroke-width="1.4"%s/>'
                 % (CX, CY, rx, ry, TILT, CX, CY, acc, ' stroke-dasharray="2 7"' if rx > 400 else ""))
    # hub
    body += ('<circle cx="%d" cy="%d" r="56" fill="url(#stack-glow)"/><circle cx="%d" cy="%d" r="40" fill="%s" stroke="url(#stack-accent)" stroke-width="2"/>'
             '<text class="mono" x="%d" y="%d" font-size="13" fill="%s" text-anchor="middle" letter-spacing="2">TECH</text>'
             '<text class="mono" x="%d" y="%d" font-size="13" fill="%s" text-anchor="middle" letter-spacing="2">STACK</text>') % (
        CX, CY, CX, CY, CARD, CX, CY - 3, INK, CX, CY + 14, INK)
    tr = math.radians(TILT)
    for items, rx, ry, th0, d, dur, acc in orbits:
        n = len(items)
        for k, (lab, nm, lib) in enumerate(items):
            th = math.radians(th0 + k * 360 / n)
            ex, ey = rx * math.cos(th), ry * math.sin(th)
            x0 = CX + ex * math.cos(tr) - ey * math.sin(tr)
            y0 = CY + ex * math.sin(tr) + ey * math.cos(tr)
            dx, dy = -2 * (x0 - CX), -2 * (y0 - CY)
            path = "M0,0 a%d,%d,%d,1,%d,%.2f,%.2f a%d,%d,%d,1,%d,%.2f,%.2f" % (rx, ry, TILT, d, dx, dy, rx, ry, TILT, d, -dx, -dy)
            anim = '<animateMotion dur="%ds" begin="0s" repeatCount="indefinite" path="%s"/>' % (dur, path)
            w = pw(lab)
            body += ('<g transform="translate(%.1f,%.1f)">%s'
                     '<g><rect x="%.1f" y="-19" width="%.1f" height="38" rx="19" fill="%s" stroke="%s" stroke-opacity=".85" stroke-width="1.4"/>'
                     '<use href="#%s" xlink:href="#%s" x="%.1f" y="-10" width="20" height="20" fill="%s"/>'
                     '<text class="mono" x="%.1f" y="5.5" font-size="%d" fill="%s">%s</text></g></g>') % (
                x0, y0, anim, -w / 2, w, CARD, acc, sid(lab), sid(lab), -w / 2 + 12, INK, -w / 2 + 38, FS, INK, esc(lab))
    # grouped chips (static fallback)
    groups = [("PROGRAMMING LANGUAGES", [x for x in A], BLUE),
              ("FRONTEND & BACKEND", [x for x in B], RED),
              ("DATABASES, APIS & TOOLS", [x for x in C], BLUE_L)]
    gx0, gw, gap, gy = 40, 288, 28, 486
    chips, maxh = "", 0
    layouts = []
    for gi, (title, items, acc) in enumerate(groups):
        rows, cur, curw = [], [], 0
        for it in items:
            w = 40 + measure("jbm-regular", it[0], FS) + 12
            if cur and curw + 8 + w > gw - 32:
                rows.append(cur); cur, curw = [], 0
            curw = curw + (8 if cur else 0) + w
            cur.append((it, w))
        rows.append(cur)
        layouts.append(rows)
        maxh = max(maxh, 62 + len(rows) * 46)
    H = gy + maxh + 34
    for gi, (title, items, acc) in enumerate(groups):
        gx = gx0 + gi * (gw + gap)
        chips += '<rect x="%d" y="%d" width="%d" height="%d" rx="20" fill="%s" fill-opacity=".92" stroke="%s" stroke-opacity=".45" stroke-width="1.2"/>' % (gx, gy, gw, maxh, CARD, acc)
        chips += '<circle cx="%d" cy="%d" r="4.5" fill="%s"/><text class="mono" x="%d" y="%d" font-size="13" fill="%s" letter-spacing="2">%s</text>' % (
            gx + 22, gy + 30, acc, gx + 36, gy + 35, MUTED, esc(title))
        for ri, row in enumerate(layouts[gi]):
            x = gx + 16
            y = gy + 62 + ri * 46
            for (lab, nm, lib), w in row:
                chips += ('<g><rect x="%.1f" y="%d" width="%.1f" height="38" rx="19" fill="#0e1730" stroke="%s" stroke-opacity=".6" stroke-width="1.2"/>'
                          '<use href="#%s" xlink:href="#%s" x="%.1f" y="%d" width="20" height="20" fill="%s"/>'
                          '<text class="mono" x="%.1f" y="%.1f" font-size="%d" fill="%s">%s</text></g>') % (
                    x, y, w, acc, sid(lab), sid(lab), x + 12, y + 9, INK, x + 38, y + 24.5, FS, INK, esc(lab))
                x += w + 8

    css = (font_face_css(["jbm-regular"]) + ".mono{font-family:%s;font-weight:400}" % MONO
           + ".s-chips{animation:s-fade .9s ease-out .2s both}@keyframes s-fade{from{opacity:0}to{opacity:1}}" + REDUCED)
    s = svg_open(W, H, "stack-title", "stack-desc", "Technology stack",
                 "Technologies orbiting a central hub on three tilted orbits. Programming languages: C++, Python, JavaScript. Frontend and backend: "
                 "React, Node.js, Express.js. Databases, APIs and developer tools: SQL, PostgreSQL, Supabase, Git, GitHub, REST APIs. "
                 "The same technologies are listed in grouped chips below the orbits.")
    s += "<defs><style>%s</style>" % css + base_defs(P, W, H, 28, None)
    s += radial("stack-glow", BLUE, .55) + radial("stack-glow-red", RED, .22) + radial("stack-glow-blue", BLUE, .20)
    s += "".join(syms.values()) + "</defs>"
    s += '<g clip-path="url(#stack-clip)">' + frame(P, W, H, 28)
    s += '<circle cx="140" cy="120" r="300" fill="url(#stack-glow-blue)"/><circle cx="880" cy="380" r="300" fill="url(#stack-glow-red)"/>'
    s += '<text class="mono" x="40" y="52" font-size="13" fill="%s" letter-spacing="3">TECH STACK</text>' % MUTED
    s += body + '<g class="s-chips">' + chips + '</g></g>' + border(P, W, H, 28) + '</svg>'
    write("stack.svg", s)


if __name__ == "__main__":
    build_hero(); build_about(); build_stack()
