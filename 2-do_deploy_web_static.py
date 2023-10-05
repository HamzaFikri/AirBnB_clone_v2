#!/usr/bin/python3
"""
Fabric script for deploying an archive to web servers.
"""

from fabric.api import env, put, run
from os.path import exists
from os import remove
import os

# Update these with your actual server IP addresses and SSH key
env.hosts = ['18.204.14.176', '54.226.7.139']
env.user = 'ubuntu'
env.key_filename = 'etc/letsencrypt/live/www.mhfsoft.tech/fullchain.pem'

def do_deploy(archive_path):
    """
    Distributes an archive to web servers and deploys it.
    """
    if not exists(archive_path):
        return False

    try:
        # Upload the archive to the /tmp/ directory of the web server
        put(archive_path, '/tmp/')

        # Extract the filename without extension
        archive_filename = os.path.basename(archive_path)
        archive_name = os.path.splitext(archive_filename)[0]

        # Create the release directory
        release_dir = f'/data/web_static/releases/{archive_name}'
        run(f'mkdir -p {release_dir}')

        # Uncompress the archive to the release directory
        run(f'tar -xzf /tmp/{archive_filename} -C {release_dir}')

        # Delete the archive from the web server
        run(f'rm /tmp/{archive_filename}')

        # Delete the symbolic link /data/web_static/current
        current_link = '/data/web_static/current'
        if exists(current_link):
            run(f'rm {current_link}')

        # Create a new symbolic link to the new version
        run(f'ln -s {release_dir} {current_link}')

        print('New version deployed!')
        return True
    except Exception as e:
        print(f'Error: {e}')
        return False

