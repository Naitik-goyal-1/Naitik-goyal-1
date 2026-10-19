# Delivery report - Naitik Goyal animated GitHub profile

## What was built
README.md, preview.html, five self-contained SVGs (hero, about-life, stack, id-dashboard, connect), original id.png / right_pointing.png, font and icon licenses, test scripts, upload-ready.zip.

## Inputs checked
| File | Size | Mode | Alpha |
| --- | --- | --- | --- |
| id.png | 1178x1335 | RGBA | genuine (45% fully transparent, soft edges, no halo/checkerboard; touches only bottom edge, a natural body crop) |
| right_pointing.png | 1205x1305 | RGBA | genuine (57% transparent, same edge result) |
Originals are untouched in assets/. SVGs embed alpha-preserving downscaled PNG copies (640/560 px tall) to keep files near 1 MB; no redrawing or masking.

## Tested and passed (actually run)
- tests/validate.py: 89 automated checks, 0 failed (report: tests/reports/validation.txt): well-formed XML, viewBox/size, no script/foreignObject/handlers, no external references, unique namespaced IDs, all url(#)/href refs resolve, embedded PNGs decode with real alpha, fonts are data URIs, README has all five `?v=1` paths, exact project/social URLs in README and preview, no placeholders/fake metrics, licenses present, preview uses local files only.
- tests/render.py (Chromium, SVG in `<img>`): 45 renders - each SVG at 1000px, 830px (README-like) and 390px (mobile), with animation stripped, and with prefers-reduced-motion. All decode. preview.html loads offline with no failed requests.
- tests/render_seek.py: deterministic frames at 0, 2, 5, 9, 13 s (CSS animations seeked via Web Animations API, SMIL via setCurrentTime) for all five SVGs. Reviewed visually: hero role cycle/typing/name reveal, carousel progress, orbit motion, ID drop/settle/swing within the viewBox.
- Fonts: WOFF2 subsets embedded; render shows Bricolage Grotesque and JetBrains Mono, not fallbacks.

## Not verified / limitations
- Live link reachability: no network in this environment. Only URL syntax was checked. Instagram URL kept exactly as supplied (the tracking query could not be tested, so it was not normalized).
- Rendering was tested in Chromium only, not in GitHub's own pipeline, Safari or Firefox. Open the profile after pushing and check.
- SMIL cannot be disabled by prefers-reduced-motion. CSS animations stop under it; SMIL is used only for the short greeting typing and the slow orbit motion of the stack icons. Static fallback shows the final state.
- Static (no-animation) hero shows only the first role (Software Developer); all three roles are in README text and the SVG description. Carousel static fallback keeps all three interests visible in the list.
- The interests' emoji are in README text; inside the SVG they are replaced by vector glyphs, since emoji fonts cannot be embedded or relied on.
- SQL and REST APIs have no official brand logo: generic Material Design glyphs with text labels. LinkedIn uses Font Awesome Free (CC BY 4.0, attribution in LICENSES/THIRD-PARTY-NOTICES.md) because Simple Icons dropped it.
- WOFF2 files were compressed through a small Node-brotli shim (tests/shim) because Python brotli was unavailable; fonts decode correctly.
- On phones the 1000px-wide SVGs scale down, so small labels (stack chips, pills) get small. Layouts do not overflow.
- hero.svg and connect.svg are ~0.9-1 MB each because of the embedded portraits.
