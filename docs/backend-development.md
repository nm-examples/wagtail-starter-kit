# Backend Development

The project uses Docker for local development. The Wagtail project is in the `app` directory. The project is set up to use a SQLite database by default.

It's recommended to use the same database in development as you will use in production.

If you added any data to the SQLite database you will need to add it again to the new database if you change it here. It's therefore a good idea to **choose your database before you start** adding data/content to the project.

The process to change the database is simple and is outlined below. You select the database using a `.env` file without editing the `Makefile`.

## Choose a database using .env

1. Copy the example env file and pick a database:

```bash
cp .env.example .env
# choose one of: sqlite (default), postgres, mysql
sed -i '' 's/^DATABASE=.*/DATABASE=mysql/' .env   # macOS example
```

2. Build and start the stack:

```bash
make build
make up
```

3. Apply migrations and create a superuser:

```bash
make migrate
make superuser
```

When `DATABASE=mysql` the MySQL service from `compose.mysql.override.yaml` is used. When `DATABASE=postgres` the PostgreSQL service from `compose.postgresql.override.yaml` is used. Otherwise SQLite is used by default.

## Notes for Postgres and MySQL

- No manual edits to the Makefile are required; it reads `.env` and selects the correct compose override.
- Database environment variables (`MYSQL_*` / `POSTGRES_*`) are provided by the override files and consumed by `app/settings/base.py`.

### Database settings

The database settings are already set as environment variables in the docker-compose files so no further configuration is required beyond setting `DATABASE` in `.env`.

### Validate environment

Before building or starting services, verify required variables with:

```bash
make check-env
```

This checks common settings and the DB-specific variables for the selected `DATABASE` in `.env`. If anything is missing, it prints the missing keys so you can update `.env` (use `.env.example` as a guide).

You will need to run though the [initial setup steps](../README.md#getting-started) again including `applying migrations` and `creating a superuser`

## Reload while developing

`django-browser-reload` is used to automatically reload the browser when changes are made to the backend files when debug is enabled.

## Styleguide module

The project includes a styleguide page at [http://localhost:8000/style-guide/](http://localhost:8000/style-guide/) which demonstrates the Pico CSS classless styling and includes some common HTML elements.

The styleguide is available only in debug mode.
