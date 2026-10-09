# Port map

One unique host port per app so they coexist on the LAN. Over Tailscale each container gets its own hostname, so the port is irrelevant there.

| App | Replaces | Host port | Container port | Image |
|---|---|---|---|---|
| PhotoCraft | Adobe Photoshop | 8181 | 8080 | `ghcr.io/gerardumbert/photocraft-web` |
| WordCraft | Microsoft Word | 8182 | 8080 | `ghcr.io/gerardumbert/wordcraft-web` |
| GridCraft | Microsoft Excel | 8183 | 8080 | `ghcr.io/gerardumbert/gridcraft-web` |
| DeckCraft | Microsoft PowerPoint | 8184 | 8080 | `ghcr.io/gerardumbert/deckcraft-web` |
| LightCraft | Adobe Lightroom | 8185 | 8080 | `ghcr.io/gerardumbert/lightcraft-web` |
| VectorCraft | Adobe Illustrator | 8186 | 8080 | `ghcr.io/gerardumbert/vectorcraft-web` |
| DesignCraft | Adobe InDesign | 8187 | 8080 | `ghcr.io/gerardumbert/designcraft-web` |
| PdfCraft | Adobe Acrobat | 8188 | 8080 | `ghcr.io/gerardumbert/pdfcraft-web` |
| FilmCraft | Adobe Premiere Pro | 8189 | 8080 | `ghcr.io/gerardumbert/filmcraft-web` |
| EffectCraft | Adobe After Effects | 8190 | 8080 | `ghcr.io/gerardumbert/effectcraft-web` |
| SoundCraft | Avid Pro Tools | 8191 | 8080 | `ghcr.io/gerardumbert/soundcraft-web` |
| CADCraft | AutoCAD | 8192 | 8080 | `ghcr.io/gerardumbert/cadcraft-web` |
