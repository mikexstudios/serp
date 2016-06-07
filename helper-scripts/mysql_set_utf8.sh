#!/bin/bash
#We need to run this before we run syncdb so that  all entries within our
#database will be set to utf8.
#To use:
#./mysql_set_utf8.sh dev  <- mysql user

#Check is user arg is set. -n means 'not empty':
if [ ! -n "$1" ]; then
    echo 'Sets the suppletext database to use utf8 encoding.'
    echo 'Usage: $0 [mysql user]'
    exit
fi

mysql_cmd='ALTER DATABASE suppletext DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci'
echo "$mysql_cmd" | mysql suppletext -u $1 -p
