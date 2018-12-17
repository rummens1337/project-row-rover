# Copy settings to appdata dir if it does not excist.

from pathlib import Path
from shutil import copyfile, copytree
import os
from subprocess import call

settings_template = "settings.conf"
settings = "/appdata/" + settings_template
log_path = "/appdata/log"

if not Path(log_path).is_dir():
    os.makedirs(log_path)

if not Path(settings).is_file():
    copyfile(settings_template, settings)

if not Path("/appdata/mysql").is_dir():
	copytree("mysql", "/appdata/mysql")


# call("supervisord")