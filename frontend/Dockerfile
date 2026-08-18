# Serve the static portfolio site with Nginx.
FROM nginx:1.27-alpine

# Patch OS packages to pull security fixes (e.g. OpenSSL CVE-2026-31789).
# apk upgrade brings libssl3/libcrypto3 to the fixed version.
RUN apk update && apk upgrade --no-cache

# Remove the default Nginx welcome page.
RUN rm -rf /usr/share/nginx/html/*

# Copy our static site into Nginx's web root.
COPY . /usr/share/nginx/html

# Nginx serves on port 80 by default.
EXPOSE 80
