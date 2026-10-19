# Third-party licenses and sources

All files were bundled locally; nothing is loaded from the network at runtime.

## Fonts (embedded as base64 WOFF2 subsets, Basic Latin + a few punctuation glyphs)
| Font | Use | Source | License file |
| --- | --- | --- | --- |
| Bricolage Grotesque (Regular, Bold) | Display text | https://github.com/ateliertriay/bricolage | `OFL-BricolageGrotesque.txt` (SIL OFL 1.1) |
| JetBrains Mono (Regular, Bold) | Monospaced text | https://github.com/JetBrains/JetBrainsMono | `OFL-JetBrainsMono.txt` (SIL OFL 1.1) |

Both OFL texts declare no Reserved Font Name, so subsetting and embedding is permitted. The TTFs came from the local font bundle; their name tables carry the OFL notice and copyright.

## Icons
| Icons | Source | License file |
| --- | --- | --- |
| C++, Python, JavaScript, React, Node.js, Express.js, PostgreSQL, Supabase, Git, GitHub, Instagram | Simple Icons (local copy bundled with mkdocs-material 9.7.6) | `SimpleIcons-CC0-1.0.md` (CC0 1.0) |
| LinkedIn | Font Awesome Free 7.1.0 brands (Simple Icons no longer ships it) | `FontAwesome-Free-LICENSE.txt` (icons CC BY 4.0, attribution: "Font Awesome Free by Fonticons, Inc., https://fontawesome.com") |
| SQL (database), REST APIs (api), map marker, school, laptop, palette, rocket | Material Design Icons (Pictogrammers) | `MaterialDesignIcons-Pictogrammers-LICENSE.txt` |

SQL and REST APIs are not brands with an official logo, so generic concept glyphs are used and labelled with text. Brand marks remain trademarks of their owners; their use does not imply endorsement or certification.
