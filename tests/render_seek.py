"""Deterministic time-seek renders: SVG opened as a top-level document, CSS animations paused+seeked via Web Animations API, SMIL via setCurrentTime."""
import asyncio, os
from playwright.async_api import async_playwright
R=os.path.abspath(os.path.join(os.path.dirname(__file__),".."))
OUT=R+"/tests/renders"
NAMES=["hero","about-life","stack","id-dashboard","connect"]
async def one(b,n,t):
    ctx=await b.new_context(viewport={"width":1000,"height":800}); p=await ctx.new_page()
    await p.goto(f"file://{R}/assets/{n}.svg")
    await p.evaluate("""t=>{const s=document.documentElement;s.pauseAnimations();s.setCurrentTime(t);
      document.getAnimations().forEach(a=>{a.pause();a.currentTime=t*1000});}""",t)
    await p.wait_for_timeout(150)
    box=await p.evaluate("(()=>{const r=document.documentElement.getBoundingClientRect();return [r.width,r.height]})()")
    await p.screenshot(path=f"{OUT}/{n}_t{t}.png",clip={"x":0,"y":0,"width":box[0],"height":box[1]}); await ctx.close()
async def main():
    async with async_playwright() as pw:
        b=await pw.chromium.launch(args=["--allow-file-access-from-files"])
        for n in NAMES:
            await asyncio.gather(*[one(b,n,t) for t in (0,2,5,9,13)])
        await b.close(); print("seek renders done")
asyncio.run(main())
