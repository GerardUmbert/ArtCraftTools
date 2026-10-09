#!/usr/bin/env python3
"""Generate unraid/<app>.xml and PORTS.md from apps.json."""
import json
from pathlib import Path
from xml.sax.saxutils import escape

root = Path(__file__).resolve().parent.parent
cfg = json.loads((root / "apps.json").read_text(encoding="utf-8"))
owner, repo = cfg["owner"], cfg["repo"]
cport = cfg["container_port"]
raw = f"https://raw.githubusercontent.com/{owner}/{repo}/main"

TEMPLATE = """<?xml version="1.0"?>
<Container version="2">
  <Name>{name}</Name>
  <Repository>ghcr.io/{owner_l}/{name}-web:latest</Repository>
  <Registry>https://github.com/{owner}/{repo}/pkgs/container/{name}-web</Registry>
  <Network>bridge</Network>
  <MyIP/>
  <Shell>sh</Shell>
  <Privileged>false</Privileged>
  <Support>https://github.com/{owner}/{repo}/issues</Support>
  <Project>https://github.com/{upstream}/{name}</Project>
  <Overview>{title} is an open-source, clean-room reimplementation of {replaces} in Rust, from the ArtCraft Crafting Apps. {tagline} This container serves its browser (WebAssembly) build with nginx. All work happens in your browser: Open/Save use the browser file picker and downloads, so nothing is stored on the server and no volume is needed. WebGPU and clipboard APIs require a secure context, so reach it over HTTPS (for example via Unraid's Tailscale integration with Tailscale Serve, or a reverse proxy) or via localhost. Early alpha software.</Overview>
  <Category>{category}</Category>
  <WebUI>http://[IP]:[PORT:{cport}]/</WebUI>
  <TemplateURL>{raw}/unraid/{name}.xml</TemplateURL>
  {icon}
  <ExtraParams>--restart=unless-stopped</ExtraParams>
  <DateInstalled/>
  <Config Name="WebUI Port" Target="{cport}" Default="{port}" Mode="tcp" Description="Host port for the web UI (container port {cport}). Unique per app, see PORTS.md." Type="Port" Display="always" Required="true" Mask="false">{port}</Config>
</Container>
"""

(root / "unraid").mkdir(exist_ok=True)
rows = []
for a in cfg["apps"]:
    xml = TEMPLATE.format(
        name=a["name"], title=escape(a["title"]), replaces=escape(a["replaces"]),
        category=a["category"], port=a["port"], cport=cport, owner=owner,
        icon=(f"<Icon>{raw}/icons/{a['name']}.png</Icon>" if (root / "icons" / f"{a['name']}.png").exists() else "<Icon/>"),
        tagline=escape(a.get("tagline", "")),
        owner_l=owner.lower(), repo=repo, upstream=cfg["upstream_owner"], raw=raw,
    )
    (root / "unraid" / f'{a["name"]}.xml').write_text(xml, encoding="utf-8", newline="\n")
    rows.append(f'| {a["title"]} | {a["replaces"]} | {a["port"]} | {cport} | `ghcr.io/{owner.lower()}/{a["name"]}-web` |')

ports = "# Port map\n\nOne unique host port per app so they coexist on the LAN. Over Tailscale each container gets its own hostname, so the port is irrelevant there.\n\n| App | Replaces | Host port | Container port | Image |\n|---|---|---|---|---|\n" + "\n".join(rows) + "\n"
(root / "PORTS.md").write_text(ports, encoding="utf-8", newline="\n")
print(f'generated {len(cfg["apps"])} templates')

# ---- All-in-one: landing page + template -------------------------------------
aio_port = cfg["aio_port"]
cards = "\n".join(
    f'    <a class="card" href="{a["name"]}/"><img src="icons/{a["name"]}.png" alt="" onerror="this.style.visibility=\'hidden\'">'
    f'<b>{escape(a["title"])}</b><span>{escape(a["replaces"])} alternative</span></a>'
    for a in cfg["apps"]
)
landing = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>ArtCraft apps</title>
<style>
:root{{--bg:#fff;--fg:#1a1a1a;--card:#f3f3f5;--mut:#666}}
@media (prefers-color-scheme:dark){{:root{{--bg:#16161a;--fg:#eee;--card:#23232a;--mut:#9a9aa5}}}}
body{{margin:0;padding:24px 16px;background:var(--bg);color:var(--fg);font:16px system-ui,sans-serif}}
h1{{text-align:center}}
.grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(180px,1fr));gap:12px;max-width:900px;margin:24px auto}}
.card{{display:flex;flex-direction:column;align-items:center;gap:6px;padding:18px 12px;background:var(--card);border-radius:12px;color:inherit;text-decoration:none}}
.card img{{width:56px;height:56px}} .card span{{color:var(--mut);font-size:13px;text-align:center}}
</style></head><body>
<h1>ArtCraft apps</h1>
<div class="grid">
{cards}
</div></body></html>
"""
(root / "aio").mkdir(exist_ok=True)
(root / "aio" / "index.html").write_text(landing, encoding="utf-8", newline="\n")

AIO = TEMPLATE.replace("<Name>{name}</Name>", "<Name>artcraft-aio</Name>")
aio_xml = AIO.format(
    name="artcraft-aio", title="ArtCraft apps (all-in-one)", replaces="Photoshop, Word, Excel, PowerPoint, Lightroom, Illustrator, InDesign, Acrobat, Premiere Pro, After Effects, Pro Tools and AutoCAD",
    category="Productivity: Tools", port=aio_port, cport=cport, owner=owner, owner_l=owner.lower(), repo=repo,
    upstream=cfg["upstream_owner"], raw=raw, tagline="", icon="<Icon/>",
)
aio_xml = aio_xml.replace("<Name>artcraft-aio</Name>", "<Name>artcraft-aio</Name>")
aio_xml = aio_xml.replace(f"{{raw}}", raw)
aio_xml = aio_xml.replace(
    "ghcr.io/%s/artcraft-aio-web" % owner.lower(), "ghcr.io/%s/artcraft-aio" % owner.lower()
).replace("pkgs/container/artcraft-aio-web", "pkgs/container/artcraft-aio"
).replace("https://github.com/storytold/artcraft-aio", "https://github.com/storytold/artcraft"
).replace("is an open-source, clean-room reimplementation of", "bundles the browser builds of the ArtCraft Crafting Apps, open-source clean-room reimplementations of"
).replace(" in Rust, from the ArtCraft Crafting Apps. ", " in Rust. Open the landing page and pick an app (served at /photocraft/, /wordcraft/, ...). ")
(root / "unraid" / "artcraft-aio.xml").write_text(aio_xml, encoding="utf-8", newline="\n")
with open(root / "PORTS.md", "a", encoding="utf-8", newline="\n") as f:
    f.write(f"\nAll-in-one (`ghcr.io/{owner.lower()}/artcraft-aio`): host port {aio_port}, container port {cport}. Apps at `/<app>/`.\n")
print("generated aio")
