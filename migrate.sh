#!/bin/sh

# Removes migrate version to allow flask db init
psql -d $DATABASE_URL -c "DROP TABLE IF EXISTS alembic_version;"

# Flask migrate database
flask db init
flask db migrate
flask db upgrade

# Remove shell file
rm migrate.sh