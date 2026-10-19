import re, os, io, base64, glob, zipfile, sys
import xml.etree.ElementTree as ET
from PIL import Image
import numpy as np
R=os.path.abspath(os.path.join(os.path.dirname(__file__),".."))
res=[]
def chk(name, ok, note=""): res.append((name, ok, note)); print(("PASS " if ok else "FAIL ")+name, note)
svgs=sorted(glob.glob(R+"/assets/*.svg"))
chk("5 SVGs present", len(svgs)==5, str([os.path.basename(s) for s in svgs]))
for f in svgs:
    n=os.path.basename(f); t=open(f,encoding="utf-8").read()
    try: root=ET.fromstring(t); chk(n+" well-formed XML",True)
    except Exception as e: chk(n+" well-formed XML",False,str(e)); continue
    chk(n+" has width/height/viewBox", all(k in root.attrib for k in("width","height","viewBox")), root.attrib.get("viewBox"))
    chk(n+" no script/foreignObject/event handlers", not re.search(r"<script|foreignObject|\son[a-z]+=",t))
    ext=[u for u in re.findall(r'(?:href|src)="([^"]+)"',t)+re.findall(r"url\(([^)]+)\)",t) if not (u.startswith("#") or u.startswith("data:") or u.startswith("'data:") or u.startswith("url(#") )]
    ext=[u for u in ext if not u.startswith("#")]
    chk(n+" no external references", not ext and "@import" not in t and not re.search(r"https?://(?!www\.w3\.org)",t), str(ext[:3]))
    ids=re.findall(r'\sid="([^"]+)"',t); pre=n.split("-")[0].replace(".svg","")
    chk(n+" unique ids", len(ids)==len(set(ids)))
    refs=set(re.findall(r'url\(#([^)]+)\)',t))|set(re.findall(r'(?:href)="#([^"]+)"',t))
    chk(n+" all id references resolve", refs<=set(ids), str(refs-set(ids)))
    pfx={"hero":"hero","about":"about","stack":"stack","id":"idc","connect":"connect"}[n.split("-")[0].split(".")[0]]
    chk(n+" ids namespaced '%s-'"%pfx, all(i.startswith(pfx+"-") for i in ids), str([i for i in ids if not i.startswith(pfx+"-")][:3]))
    for m in re.finditer(r'href="data:image/png;base64,([^"]+)"',t):
        im=Image.open(io.BytesIO(base64.b64decode(m.group(1)))); a=np.array(im.convert("RGBA"))[:,:,3]
        chk(n+" embedded PNG decodes + real alpha", im.mode=="RGBA" and a.min()==0 and (a==0).mean()>.3, f"{im.size} transparent={(a==0).mean():.0%}")
        break
    chk(n+" fonts are data URIs", "data:font/woff2;base64" in t)
    chk(n+" size < 2MB", len(t.encode())<2e6, f"{len(t)//1024} KB")
for a in ("id","right_pointing"):
    im=Image.open(f"{R}/assets/{a}.png"); al=np.array(im.convert("RGBA"))[:,:,3]
    chk(f"assets/{a}.png original intact RGBA alpha", im.mode=="RGBA" and al.min()==0, str(im.size))
rd=open(R+"/README.md",encoding="utf-8").read()
for n in ("hero","about-life","stack","id-dashboard","connect"):
    chk(f"README embeds ./assets/{n}.svg?v=1", f"(./assets/{n}.svg?v=1)" in rd)
    chk(f"assets/{n}.svg exists", os.path.exists(f"{R}/assets/{n}.svg"))
urls={"AirCanvas":"https://github.com/Naitik-goyal-1/AirCanvas-AI-Hand-Tracking-Virtual-Drawing","GoCart":"https://github.com/Naitik-goyal-1/Go---Cart-","FutureSelf":"https://github.com/Naitik-goyal-1/your-Future-Self",
"GitHub":"https://github.com/Naitik-goyal-1","LinkedIn":"https://www.linkedin.com/in/naitik-goyal-og","Instagram":"https://www.instagram.com/naitik.0g_?obrf=MXdsbThmMGdnejZ0Mw=="}
for k,u in urls.items():
    chk(f"README contains exact URL: {k}", f"]({u})" in rd)
    chk(f"preview.html contains exact URL: {k}", f'href="{u}"' in open(R+"/preview.html",encoding="utf-8").read())
chk("README has no placeholders/TODO/fake metrics/YouTube/Topmate", not re.search(r"TODO|\[placeholder\]|youtube|topmate|stars|followers|commits",rd,re.I))
chk("README: social links appear after connect image", rd.index("connect.svg")<rd.index("](https://www.linkedin.com"))
pv=open(R+"/preview.html",encoding="utf-8").read()
chk("preview.html local-only (no http src/CDN/script)", not re.search(r'(src|href)="https?://(?!github.com|www.linkedin.com|www.instagram.com)',pv) and "<script" not in pv and "@import" not in pv)
chk("preview.html asset files exist", all(os.path.exists(R+"/"+p) for p in re.findall(r'src="(assets/[^"?]+)',pv)))
for lic in ("OFL-BricolageGrotesque.txt","OFL-JetBrainsMono.txt","SimpleIcons-CC0-1.0.md","FontAwesome-Free-LICENSE.txt","MaterialDesignIcons-Pictogrammers-LICENSE.txt","README.md"):
    chk("LICENSES/"+lic+" non-empty", os.path.getsize(f"{R}/LICENSES/{lic}")>200)
# links: syntax only (no network)
for k,u in urls.items(): chk(f"URL syntax valid: {k}", bool(re.match(r"^https://[\w.-]+/[^\s]+$",u)))
open(R+"/tests/reports/validation.txt","w").write("\n".join(("PASS " if o else "FAIL ")+n+(" | "+x if x else "") for n,o,x in res))
print("\nTOTAL",len(res),"FAILED",sum(1 for r in res if not r[1]))
