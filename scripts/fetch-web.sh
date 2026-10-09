#!/usr/bin/env bash
# Download the latest static web build of an upstream craft app into ./site
# Usage: scripts/fetch-web.sh <app> [tag]     (requires gh, unzip)
# Prints the resolved version (tag without leading "v") on stdout's last line.
set -euo pipefail

app="$1"
upstream="storytold/${app}"
tag="${2:-$(gh release view --repo "$upstream" --json tagName -q .tagName)}"

work="$(mktemp -d)"
gh release download "$tag" --repo "$upstream" --pattern "${app}-web-*.zip" --dir "$work"
rm -rf site && mkdir site
unzip -q "$work"/*.zip -d site

# Some zips wrap everything in a single top-level folder; flatten it.
if [ ! -f site/index.html ]; then
  inner="$(find site -mindepth 1 -maxdepth 1 -type d | head -n1)"
  if [ -n "$inner" ] && [ -f "$inner/index.html" ]; then
    shopt -s dotglob && mv "$inner"/* site/ && rmdir "$inner"
  fi
fi
[ -f site/index.html ] || { echo "no index.html in ${app} web zip" >&2; exit 1; }

echo "${tag#v}"
