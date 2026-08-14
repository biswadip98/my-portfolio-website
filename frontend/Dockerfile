# Serve the static portfolio site with Nginx.
FROM nginx:1.27-alpine

# Remove the default Nginx welcome page.
RUN rm -rf /usr/share/nginx/html/*

# Copy our static site into Nginx's web root.
COPY . /usr/share/nginx/html

# Nginx serves on port 80 by default.
EXPOSE 80
