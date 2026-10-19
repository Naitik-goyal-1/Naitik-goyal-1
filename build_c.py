import os
R=os.path.abspath(os.path.join(os.path.dirname(__file__),".."))
html='''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Profile preview - Naitik Goyal</title>
<style>
:root{--navy:#070b16;--blue:#247bff;--red:#ff354f;--ink:#e9eefc;--muted:#9aa8c9}
body{margin:0;background:var(--navy);color:var(--ink);font-family:"Segoe UI",Helvetica,Arial,sans-serif;line-height:1.55}
main{max-width:880px;margin:0 auto;padding:24px 16px 64px}
img{width:100%;height:auto;display:block;margin:12px 0 20px}
h2{margin:36px 0 4px;padding-bottom:6px;border-bottom:1px solid #1b2748}
a{color:#6aa3ff}.note{color:var(--muted);font-size:14px}
table{width:100%;border-collapse:collapse;display:block;overflow-x:auto}
th,td{border:1px solid #1b2748;padding:10px;text-align:left;vertical-align:top}th{background:#0e1730}
</style></head><body><main>
<p class="note">Local preview of README.md. Works offline; uses only files in ./assets.</p>
<img src="assets/hero.svg?v=1" alt="Hero">
<p><strong>Naitik Goyal</strong> · Student Developer · Madhav Institute of Technology &amp; Science, Gwalior<br>Software Developer · Full-Stack Developer · AI/ML Enthusiast<br><em>Code with purpose. Build with vision. Innovate through technology.</em></p>
<h2>About Me</h2><img src="assets/about-life.svg?v=1" alt="About Me">
<ol><li>💻 Software Development &amp; Problem Solving</li><li>🎨 UI/UX Design &amp; Creative Designing</li><li>🚀 Exploring New Technologies &amp; Building Projects</li></ol>
<h2>Technology Stack</h2><img src="assets/stack.svg?v=1" alt="Technology Stack">
<h2>Developer ID</h2><img src="assets/id-dashboard.svg?v=1" alt="Developer ID">
<h2>Projects</h2>
<table><tr><th>Project</th><th>Description</th><th>Repository</th></tr>
<tr><td><b>AirCanvas — AI-Powered Virtual Drawing</b></td><td>Draw in the air with your finger. AirCanvas turns your webcam into a virtual whiteboard using MediaPipe hand tracking, following your index finger in real time to draw continuous lines without a mouse, stylus, or touchscreen.</td><td><a href="https://github.com/Naitik-goyal-1/AirCanvas-AI-Hand-Tracking-Virtual-Drawing">AirCanvas-AI-Hand-Tracking-Virtual-Drawing</a></td></tr>
<tr><td><b>GoCart — E-Commerce Web Application</b></td><td>An e-commerce web application for a smooth, convenient online shopping experience, with an intuitive interface, product browsing, and shopping cart functionality.</td><td><a href="https://github.com/Naitik-goyal-1/Go---Cart-">Go---Cart-</a></td></tr>
<tr><td><b>Your Future Self — Personal Growth Platform</b></td><td>A personal development project that helps users reflect on their goals, visualize their future, and make better decisions, encouraging self-awareness, goal setting, and positive habits.</td><td><a href="https://github.com/Naitik-goyal-1/your-Future-Self">your-Future-Self</a></td></tr></table>
<h2>Connect</h2><img src="assets/connect.svg?v=1" alt="Connect">
<ul><li><a href="https://github.com/Naitik-goyal-1">GitHub</a></li><li><a href="https://www.linkedin.com/in/naitik-goyal-og">LinkedIn</a></li><li><a href="https://www.instagram.com/naitik.0g_?obrf=MXdsbThmMGdnejZ0Mw==">Instagram</a></li></ul>
</main></body></html>'''
open(os.path.join(R,"preview.html"),"w",encoding="utf-8").write(html)
