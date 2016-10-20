#!/bin/bash

source .ve/bin/activate

git pull --no-edit && pip install -r requirements.txt | grep -v "Requirement already satisfied" && python ./minify_static.py && ./site/manage.py migrate && ./site/manage.py collectstatic --noinput
echo "touching to reload uwsgi..."
touch /tmp/dargprod-master.pid

# Backing up database
echo "backing up database to dropbox"
python manage.py dbbackup --encrypt

echo "...done"
