#!/bin/bash
# Kills the fcgi process. Relies on daemontools to detect that process has
# been killed and thus starts it again.

#Note that $0 contains the full path of the script being executed.
script_path=`dirname $0`
cd "${script_path}/.."

if [ -f fcgi.pid ]; then
    kill `cat fcgi.pid`
    rm fcgi.pid
    echo 'Killed the fcgi process'
fi
