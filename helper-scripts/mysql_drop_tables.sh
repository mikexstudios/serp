#!/bin/bash

#Note that $0 contains the full path of the script being executed.
script_path=`dirname $0`
cd "${script_path}/.."

#Each script creates new bash shell so we need to activate the env.
source env/bin/activate

#Snippet from: http://www.djangosnippets.org/snippets/1896/
echo 'show tables;' \
    | python manage.py dbshell \
    | sed -n 2,\$p \
    | awk 'BEGIN {print "set foreign_key_checks=0;"} { print "drop table `" $1 "`;"}' \
    | python manage.py dbshell

echo 'All tables have been dropped!'
