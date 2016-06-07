#!/bin/bash
# Sets up virtualenv and installs pip requirements.txt file. This script
# should be run in the root directory (where this file is).
virtualenv --no-site-packages env
source env/bin/activate
easy_install pip
pip -E env install -r requirements.txt
