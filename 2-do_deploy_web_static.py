#!/usr/bin/python3
"""Script that does the deployment"""
from fabric.api import *
from datetime import datetime
import os.path

env.hosts = ['18.204.14.176', '54.226.7.139']


def do_deploy(archive_path):
    """transfer files to web server"""

    if os.path.isfile(archive_path):
        pre_path = archive_path.split("/")[1]
        put(archive_path, "/tmp/")
        path_l = "/tmp/" + pre_path
        path_r = "/data/web_static/releases/" + pre_path.split(".")[0]
        sudo("mkdir -p {:s}".format(path_r))
        sudo("tar -xzf {:s} -C {:s}".format(path_l, path_r))
        sudo("rm {:s}".format(path_l))
        path_m = path_r + "/web_static/*"
        path_d = path_r + "/web_static/"
        sudo("mv {:s} {:s}".format(path_m, path_r))
        sudo("rm -rf {:s}".format(path_d))
        sudo("rm -rf /data/web_static/current")
        sudo("ln -s {:s} /data/web_static/current".format(path_r))
        print("New version deployed!")
        return True
    else:
        return False
