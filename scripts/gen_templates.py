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
