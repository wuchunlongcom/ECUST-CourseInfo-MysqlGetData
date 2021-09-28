# courseinfo

## Init DB

```bash
# delete DB migration files
rm -rf classroom/migrations/0*.py

# generate DB migration files
python manage.py makemigrations

# build DB tables
rm -rf data/db.sqlite3
python manage.py migrate

# clean DB
python manage.py flush --noinput

# init DB
python initdb.py

```

## Generate static files

```bash
rm -rf static
python manage.py collectstatic
```

## Trans

```bash
django-admin makemessages
# Modify po files
django-admin compilemessages
```

