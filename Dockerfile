# Thin runtime image: serves the prebuilt static web build (<app>-web-<ver>.zip)
# published in each upstream release. Nothing is compiled here.
# Build context must contain ./site (the unzipped web build); see scripts/fetch-web.sh.
FROM nginxinc/nginx-unprivileged:1.28-alpine

ARG APP=craft
ARG VERSION=unknown
LABEL org.opencontainers.image.title="${APP}-web" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.source="https://github.com/GerardUmbert/ArtCraftTools" \
      org.opencontainers.image.description="Static web build of ${APP} served by nginx"

COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY site/ /usr/share/nginx/html/

EXPOSE 8080
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s \
  CMD wget -q -O /dev/null http://127.0.0.1:8080/healthz || exit 1
