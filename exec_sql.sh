#!/bin/bash

SQL_PATH=$1
cd "$(dirname "${BASH_SOURCE[0]}")"
[ ! $SQL_PATH ] && SQL_PATH=create_db.sql

if [[ ! -f flask_app/sql_config.py || "$1" == "reset" || "$2" == "reset" ]]; then
	read -p "MySQL username: " username
	read -sp "MySQL password: " password
	echo ""
	echo "username='$username';password='$password'" > flask_app/sql_config.py
	chmod 600 flask_app/sql_config.py
fi

source flask_app/sql_config.py
sudo mysql -u"$username" -p"$password" < $SQL_PATH 
