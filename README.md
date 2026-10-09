# ArtCraftTools

Unraid Community Applications templates and container images for the browser (WebAssembly) builds of the [ArtCraft](https://getartcraft.com/apps) Crafting Apps by [storytold](https://github.com/storytold): PhotoCraft, WordCraft, GridCraft, DeckCraft, LightCraft, VectorCraft, DesignCraft, PdfCraft, FilmCraft, EffectCraft, SoundCraft and CADCraft.

These are early-alpha upstream projects. This repo is unofficial packaging only.

## Files

- `unraid/<app>.xml`: Unraid Docker templates, one per app (generated, see below).
- `Dockerfile`, `nginx.conf`: a thin nginx image that serves the static web build.
- `Dockerfile.aio`, `nginx-aio.conf`, `aio/`: the all-in-one image and its landing page.
- `scripts/fetch-web.sh`: downloads the latest `<app>-web-<ver>.zip` from the upstream release.
- `.github/workflows/build-images.yml`: builds and pushes `ghcr.io/gerardumbert/<app>-web` (daily, picks up new upstream releases).
- `apps.json`: the single source of truth (app list, host ports, taglines).
- `scripts/gen_templates.py`: regenerates `unraid/*.xml` and `PORTS.md` from `apps.json`.
- `PORTS.md`: host port per app.
- `icons/`: template icons (see "Missing icons").

## All-in-one image

`ghcr.io/gerardumbert/artcraft-aio` (template `unraid/artcraft-aio.xml`, host port 8180) bundles all 12 web builds in one nginx container: a landing page at `/` and each app at `/<app>/` (e.g. `/photocraft/`). One container, one port, one Tailscale hostname. The image is large (~500 MB unpacked) and you can't stop or limit apps individually; use the per-app images if you want that.

## Nothing is compiled here

Each upstream release already ships a static site (`<app>-web-<ver>.zip`). The image just unzips it into nginx, so builds take seconds.

## Installing on Unraid

1. Docker tab, Add Container, paste the template URL into the Template field:
   `https://raw.githubusercontent.com/GerardUmbert/ArtCraftTools/main/unraid/<app>.xml`
2. Keep the default host port (see `PORTS.md`) or change it, then Apply.
3. Make the GHCR packages public (GitHub profile, Packages, each `<app>-web`, Package settings), otherwise Unraid cannot pull them.

No volumes: documents never touch the server. Open/Save use the browser file picker and downloads. Save before closing the tab; there is no autosave.

## Tailscale

WebGPU and clipboard need a secure context, so plain `http://<lan-ip>:818x` won't work from other machines. Over Tailscale it does:

- In the container's Edit page on Unraid 7+, turn on **Use Tailscale** and give it a hostname (e.g. `photocraft`). Enable **Tailscale Serve** so it's reachable over HTTPS at `https://photocraft.<tailnet>.ts.net`. Each container gets its own tailnet identity, so port numbers don't clash there.
- The LAN host ports (8181 to 8192) are unique per app, so everything also coexists on the LAN.
- Each template has an optional "Appdata (Tailscale state only)" path (`/config`) so the Unraid Tailscale hook finds a persistent folder. The app itself stores nothing there.
- Alternative: one reverse proxy (SWAG, NPM, Caddy) with HTTPS in front of the host ports.

## Maintaining

Edit `apps.json`, then `python scripts/gen_templates.py`, and commit the result.

## Missing icons

getartcraft.com publishes icons only for PhotoCraft, VectorCraft, FilmCraft, LightCraft, PdfCraft, EffectCraft and DesignCraft. WordCraft, GridCraft, DeckCraft, SoundCraft and CADCraft have none yet, so their templates have an empty `<Icon/>`. Drop `icons/<app>.png` in and re-run the generator. Community Applications submission needs an icon.

## Licensing

This packaging repo is AGPL-3.0 (see `LICENSE`).

The upstream apps are MIT or Apache-2.0; the ArtCraft name and logos are trademarks with separate brand terms. Check them before submitting to Community Applications.
