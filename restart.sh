!#/bin/bash
rm db.sqlite3
rm -rf bookings/migrations/0*.py
python manage.py makemigrations
python manage.py migrate
python manage.py runscript maintenance --script-args ./exports-db/AIYCB-2018-11-20.txt


