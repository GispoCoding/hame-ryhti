# hame-ryhti

[![CI/CD](https://github.com/GispoCoding/hame-ryhti/actions/workflows/ci.yml/badge.svg)](https://github.com/GispoCoding/hame-ryhti/actions/workflows/ci.yml)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)

HAME regional land use planning database and QGIS project compatible with [national Ryhti data model](https://ryhti.syke.fi/alueidenkaytto/tietomallimuotoinen-kaavoitus/) -
[Ryhti-yhteensopiva](https://ryhti.syke.fi/alueidenkaytto/tietomallimuotoinen-kaavoitus/) tietokanta ja QGIS-projekti maakuntakaavoitukseen.

The database and functions can be run on AWS (Amazon Web Services) cloud platform.

- [Architecture](#architecture)
- [Development requirements](#development-requirements)
- [Development](#development)
  - [Database and functions](#database-and-functions)
  - [Database changes](#database-changes)
  - [Adding requirements](#adding-requirements)
- [Data model](#data-model)
- [Connecting the database](#connecting-the-database)
  - [Creating SSH key pairs](#creating-ssh-key-pairs)
  - [Opening a SSH tunnel to the server](#opening-a-ssh-tunnel-to-the-server)
  - [Connecting the database from QGIS](#connecting-the-database-from-qgis)

## Architecture

HAME-Ryhti consists of
1. a PostGIS database,
2. various AWS Lambda functions to manage the database and import or export planning data, and
3. QGIS project to connect to the database and create regional land use plans.

To manage Hame-Ryhti AWS resources, check the [infra](./infra) directory.

## Development requirements

- Python 3.12
- Docker (Install Docker based on [your platform's instructions](https://docs.docker.com/get-started/#download-and-install-docker).)

## Development

1. Create a Python virtual environment and activate it.
2. `pip install pip-tools`
3. `pip-sync requirements.txt requirements-dev.txt`
4. `pre-commit install`

### Database and functions

1. Run tests with `make pytest`
2. Build and start the development containers with `docker-compose -f docker-compose.dev.yml up -d` (or `make rebuild`).
3. Fill the database with current data model by `make test-create-db`.
4. Populate national code tables from [koodistot.suomi.fi](https://koodistot.suomi.fi) by `make test-koodistot`.
5. Edit the lambda functions under [database](./database), run tests and rebuild again.

If test using pytest-docker get stuck, you can remove the dangling containers with:

```shell
docker ps --format '{{.Names}}' |grep pytest | awk '{print $1}' | xargs -I {} docker stop {}
docker ps --format '{{.Names}}' |grep pytest | awk '{print $1}' | xargs -I {} docker rm {}
docker network ls --format {{.Name}} |grep pytest | awk '{print $1}' | xargs -I {} docker network rm {}
```

### Database changes

1. Database is defined using SQLAlchemy, so familiarize yourself with [SQLAlchemy declarative style](https://docs.sqlalchemy.org/en/20/orm/declarative_tables.html).
2. Database is divided into two schemas: `codes` contains all the Ryhti specific [national code lists](https://ryhti.syke.fi/ohjeet-ja-tuki/tietomallit/), while `hame` contains all the data tables (plans, plan objects, plan regulations etc.).
3. If you want to change *all* tables in a schema (i.e. edit *all* the code tables, or add a field to *all* the data tables), the abstract base classes are in [base.py](./database/base.py).
4. If you only want to change/add *one* code table or one data table, please edit/add the right table in [codes.py](./database/codes.py) or [models.py](./database/models.py).
5. To get the changes tested and usable in your functions, create a new database revision with `make revision name="describe_your_changes"`, e.g. `make revision name="add_plan_object_table"`. This creates a new random id (`uuid`) for your migration, and a revision file `YYYY-MM-DD-HHMM-uuid-add_plan_object_table` in the [alembic versions dir](./database/migrations/versions). Please check that the autogenerated revision file seems to do approximately sensible things.
    - Specifically, when adding geometry fields, please note [GeoAlchemy2 bug with Alembic](https://geoalchemy-2.readthedocs.io/en/latest/alembic.html#interactions-between-alembic-and-geoalchemy-2), which means you will have to *manually remove* `op.create_index` and `op.drop_index` in the revision file. This is because GeoAlchemy2 already automatically creates geometry index whenever adding a geometry column.
6. Run tests with `make pytest` to check that the revision file runs correctly. At minimum, you may have to change the tested table counts (codes_count and hame_count) in [database test setup](./database/test/conftest.py) to reflect the correct number of tables in the database.
7. Run `make rebuild` and `make test-create-db` to start development instance with the new model.
<!-- 8. To update the [database documentation](./backend/databasemodel/dbdoc/README.md) to reflect the changes, install [tbls](https://github.com/k1LoW/tbls) and run `tbls doc --force`. -->
8. Commit your changes and the new revision file in [alembic versions dir](./database/migrations/versions).

### Adding requirements

To add new requirements:
1. Add the Python library in requirements.in (if used in production) or requirements-dev.in (if used in development/CI/CD).
2. `pip-compile requirements.in` or `pip-compile requirements-dev.in`
3. `pip-sync requirements.txt requirements-dev.txt`

To update requirements to latest versions:
1. `pip-compile requirements.in --upgrade` and `pip-compile requirements-dev.in --upgrade`
2. `pip-sync requirements.txt requirements-dev.txt`

<!-- ## Data model

[Database documentation](./database/dbdoc/README.md) -->

## Connecting the database

Connecting the database is done with the secure shell protocol (SSH). To be able to connect to the database, you will have to
1. Create a SSH key pair on your computer (this has to be done only once)
2. Have db admin add the public key to the server (this has to be done only once)
3. Open a SSH tunnel on your computer (this has to be done each time)

Detailed instructions to these steps are provided below.

### Creating SSH key pairs

Generation of the key pair can be done, for example, with a program called ssh-keygen (available also in Windows 10 and 11):

- Open a command prompt (for example, open start menu and type 'cmd' and hit enter)
- Type in the command prompt `ssh-keygen -t ed25519` and press enter. This will generate a key pair (using ed25519 algorithm).
Here you could also spesify the name of the key file and passphrase to protect the key (see Fig.). If you accept the defaults, just press enter.

By default the key pair is saved to `<your home folder>/.ssh/`: it contains your public key (id25519.pub), a text file which
you have to provide to the database administrator, and the private key in file `id25519` (without the .pub suffix) which you MUST KEEP PRIVATE AND NOT SHARE IT WITH ANYONE!

![screenshot of ssh key pair creation dialog](docs/img/ssh-keygen.png)


### Opening a SSH tunnel to the server

Once the administrator has added your public key to the server, you can connect to the database using ssh. You are provided also with the necessary connection parameters (host address, port etc.) and credentials, that are needed in the following commands. Open the command prompt again
(type 'cmd' in the start menu) and in it, run the command:
- `ssh -N -L 5433:<database server address>:<port number> -i "~/.ssh/<name of the private key file>" ec2-tunnel@<host address>`
- Enter the passphrase for the key (if set) and hit enter. If no error messages appear, the tunnel is connected. Do not close the command prompt window, otherwise the SSH tunnel is disconnected.
- Now you can connect to the database using `localhost` as the host and `5433` as the port. The details how to do this with
different software are given in the following sections.
- Additional tips: the connection can automatically terminate, for example, due to server rebooting or network issues (this is usually accompanied by a message, such as `client_loop: send disconnect: Connection reset`). If this happens, run again the previous command. You can usually access the history of the commands run in terminal window by up/down arrow keys on the keyboard. So pressing "up" key and then "Enter" should do the job. In case you want to close an open SSH tunnel, press `Ctrl+C`.

### Connecting the database from QGIS

The data is read from a PostgreSQL service named `postgres` with a QGIS authentication which id is `ryhtirw`. Here is a way to set up database connection in QGIS:

1. Create a PostgreSQL service file for each environment (at the moment, there is only development environment). The file can be created, for example, with a text editor. Add the following with correct values for each environment:
```ini
[postgres]
host=localhost
port=5433
dbname=hame-dev
```
Save the file to some folder, an example location could be `<your home folder>/hameconfig/`. Name the saved file for example `pg_service_hame_dev.conf` (yes, the suffix '.conf' is part of the file name). Do not save this file as a text file (with a suffix .txt), but instead choose 'All types' from the 'Save as type' dropdown menu.

![screenshot of pgservice file made with notepad](docs/img/pg_servicefile_notepad.png)

NOTE: the Postgres service file for the dev environment is also included in in this repository under the docs folder, so alternatively you can copy the file from the into a convenient location on your computer.

2. Create a QGIS-profile for each environment. Name the profile for example `ryhti-hame-dev`. A new QGIS window will open to this profile, use that in the following.

![screenshot of new profile menu](docs/img/qgis-new-profile.png)

3. In QGIS settings add a `PGSERVICEFILE` environment variable and fill the file path of corresponding service file as a value.

![screenshot of menu location](docs/img/qgis-settings.png)

![screenshot of the setting dialog](docs/img/qgis-pgservicefile-environment-variable.png)

4. Restart QGIS to make the environment variable to take effect.

5. Create a authentication key to QGIS which ID is `ryhtirw`.

NOTE: you may be prompted for setting a master password in QGIS, if not set earlier. If so, set master password and make sure to save it to a secure place for yourself. The master password is used to manage and access the saved authentication configurations in QGIS (for more information, see the [QGIS Documentation](https://docs.qgis.org/latest/en/docs/user_manual/auth_system/auth_overview.html)).

![setting qgis master password](docs/img/qgis-auth-password.png)

Now you can proceed with the database authentication details. As in step 3, open `Settings > Options` in QGIS and choose `Authentication` on the left panel. Click the green plus sign to add a new authentication configuration and fill in details as in the following image. It is important to use the authentication Id `ryhtirw` and database username and password here.

![screenshot of the authentication dialog](docs/img/qgis-authentication.png)

6. Create a new PostgreSQL connection

![screenshot of the new connection menu](docs/img/qgis-new-connection.png)

Add the necessary parameters as follows. You can also test the connection at this point and when done, press OK.

![screenshot of the new connection dialog](docs/img/qgis-create-connection.png)
