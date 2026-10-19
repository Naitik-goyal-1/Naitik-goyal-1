import asyncio, os, re, glob
from playwright.async_api import async_playwright
R=os.path.abspath(os.path.join(os.path.dirname(__file__),".."))
OUT=R+"/tests/renders"; os.makedirs(OUT,exist_ok=True); os.makedirs(R+"/tests/build/static",exist_ok=True)
NAMES=["hero","about-life","stack","id-dashboard","connect"]
def strip(n):
    t=open(f"{R}/assets/{n}.svg",encoding="utf-8").read()
    t=re.sub(r"<animate(Motion|Transform)?\b[^>]*/>","",t)
    t=re.sub(r"animation(-[a-z-]+)?:[^;}]*;?","",t)
    t=re.sub(r"@media \(prefers-reduced-motion: reduce\)\{[^}]*\}\}","",t)
    p=f"{R}/tests/build/static/{n}.svg"; open(p,"w",encoding="utf-8").write(t); return p
async def shot(b,path,t,out,width,motion="no-preference"):
    ctx=await b.new_context(viewport={"width":width,"height":1200},reduced_motion=motion); p=await ctx.new_page()
    await p.goto("file://"+R+"/tests/blank.html"); await p.set_content(f'<body style="margin:0;background:#0d1117"><img id=i src="file://{path}" style="width:{width}px;display:block">')
    await p.wait_for_function("document.getElementById('i').complete")
    ok=await p.evaluate("document.getElementById('i').naturalWidth>0")
    await p.wait_for_timeout(int(t*1000))
    await (await p.query_selector("#i")).screenshot(path=out); await ctx.close(); return out,ok
async def main():
    async with async_playwright() as pw:
        b=await pw.chromium.launch(args=["--allow-file-access-from-files"])
        jobs=[]
        for n in NAMES:
            a=f"{R}/assets/{n}.svg"; s=strip(n)
            for t in (0,2,5,9,13): jobs.append(shot(b,a,t,f"{OUT}/{n}_t{t}.png",1000))
            jobs.append(shot(b,s,1,f"{OUT}/{n}_static.png",1000))
            jobs.append(shot(b,a,1,f"{OUT}/{n}_reduced-motion.png",1000,"reduce"))
            jobs.append(shot(b,a,9,f"{OUT}/{n}_mobile390.png",390))
            jobs.append(shot(b,a,9,f"{OUT}/{n}_readme830.png",830))
        r=await asyncio.gather(*jobs); bad=[o for o,k in r if not k]
        print("rendered",len(r),"images; failed to decode:",bad)
        ctx=await b.new_context(viewport={"width":1000,"height":900}); p=await ctx.new_page()
        errs=[]; p.on("requestfailed",lambda q:errs.append(q.url[:80])); p.on("console",lambda m:errs.append(m.text) if m.type=="error" else None)
        await p.goto("file://"+R+"/preview.html"); await p.wait_for_timeout(5000)
        await p.screenshot(path=f"{OUT}/preview_full.png",full_page=True)
        ow=await p.evaluate("document.documentElement.scrollWidth")
        print("preview loaded; failed requests/errors:",errs,"| scrollWidth",ow)
        await ctx.close(); await b.close()
asyncio.run(main())
