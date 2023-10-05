#!/usr/bin/env bash
# Sets up a web server for deployment of web_static.

#!/bin/bash

# Install Nginx if not already installed
if ! dpkg -l | grep -q nginx; then
    apt-get update
    apt-get -y install nginx
fi

# Create necessary folders if they don't exist
mkdir -p /data/web_static/releases/test
mkdir -p /data/web_static/shared

# Create a fake HTML file for testing
echo "Holberton School" > /data/web_static/releases/test/index.html

# Create or recreate the symbolic link
if [ -L /data/web_static/current ]; then
    rm /data/web_static/current
fi
ln -s /data/web_static/releases/test /data/web_static/current

# Give ownership of /data/ folder to the ubuntu user and group recursively
chown -R ubuntu:ubuntu /data/

# Update Nginx configuration to serve web_static
config_file="/etc/nginx/sites-available/default"
nginx_config="
server {
    location /hbnb_static {
        alias /data/web_static/current/;
    }
}
"
echo "$nginx_config" > "$config_file"

# Restart Nginx to apply changes
service nginx restart

