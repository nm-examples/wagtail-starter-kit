# Backend Development

The project uses Docker for local development. The Wagtail project is in the `app` directory. The project is set up to use a SQLite database by default.

It's recommended to use the same database in development as you will use in production.

If you added any data to the SQLite database you will need to add it again to the new database if you change it here. It's therefore a good idea to **choose your database before you start** adding data/content to the project.

The process to change the database is simple and is outlined below, essentially you need to comment out the database you are not using and uncomment the one you are using in the `Makefile` and rebuild the Docker containers.

## Use MYSQL database while developing

Open the Makefile (at the root of your project) and comment out the line:

```bash
DC = docker compose -f compose.yaml -f compose.sqlite3.override.yaml # SQLITE Database
```

and uncomment the line:

```bash
DC = docker compose -f compose.yaml -f compose.mysql.override.yaml # MySQL Database
```

This will run a MySQL database as a service in the Docker container and use it as the database for the project.

## Use Postgres database while developing

Open the Makefile (at the root of your project) and comment out the line:

```bash
DC = docker compose -f compose.yaml -f compose.sqlite3.override.yaml # SQLITE Database
```

and uncomment the line:

```bash
DC = docker compose -f compose.yaml -f compose.postgresql.override.yaml # PostgreSQL Database
```

This will run a Postgres database as a service in the Docker container and use it as the database for the project.

### Database settings

The database settings are already set as environment variables in the docker-compose files so no further configuration is required.

You will need to run though the [initial setup steps](../README.md#getting-started) again including `applying migrations` and `creating a superuser`

## Reload while developing

`django-browser-reload` is used to automatically reload the browser when changes are made to the backend files when debug is enabled.

## Styleguide module

The project includes a styleguide page at [http://localhost:8000/style-guide/](http://localhost:8000/style-guide/) which demonstrates the Pico CSS classless styling and includes some common HTML elements.

The styleguide is available only in debug mode.
