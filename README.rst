Introduction
============

This skill provides some Trello commands that I found useful. It will eventually be expanded to support more commands and use cases.

**[BETA WARNING]** This is currently in heavy development; most important it currently does not support account linking, thus only interacts with 1 Trello account as defined in the environment variables (see Deployment below).


Features
--------

Below listed features either implemented or planned:

- List boards
- **(TODO)** Set board as default
- **(TODO)** List available lists on board X / default board
- **(TODO)** List items in list Y on board X / default board
- **(TODO)** Add Account Link to Trello OAuth 1.0; see http://code-coverage.net/building-amazon-alexa-skills-with-net/
- **(TODO)** Fully tested


Setup Skill
===========

Use the UI wizard to create the skill through this page:

    https://developer.amazon.com/edw/home.html#/skills

We could also create the skill with the ask_ cli tool:

.. code-block:: bash

   ask new [-n|--skill-name <name>] [-p| --profile <profile>] [--lambda-name <lambda-name>]


Updating the interaction model
------------------------------

The interaction model can be found in ``model.json``. It defines the invocation name, intents and slots as well as custom types.

This file should be uploaded for each language in the Skill builder.

We can also update the model from the ask_ cli tool:

.. code-block:: bash

   ask api update-model  -f model.json -s <skill-id> -l <locale>

To update all known languages of skill with ``$SKILL_ID`` (must be set in env), use the helper script:

.. code-block:: bash

   heroku run bash update_model.sh


Deployment
==========

During development I found it easiest to use heroku, (however any host would work just as fine).

Using heroku means that dependencies are specified in the ``Pipfile`` (i.e use pipenv_), and certain environment variables must be set in ``heroku config``.


Requirements
------------

The project was developed using new features from Python 3.6, so this is the only supported version, and there are no plans to backport.

- alexandra
- py-trello
- python-dotenv
- gunicorn
- sqlalchemy
- alembic
- psycopg2

Environment Variables
---------------------

Configure at least the values below as required:

- TRELLO_API_KEY: Trello API application key
- TRELLO_API_SECRET: Trello API application secret
- DATABASE_URL: Database URL (normally set by ``Heroku Postgres`` addon)
- SKILL_ID: which skill to update when running ``update_models.py``

Database Setup
==============

Certain information, such as tokens and other user preferences, needs to be stored persistently. The data requirements should be pretty modest, thus a free tier Heroku Postgres addon instance should suffice.

Create Database
---------------

When managing our own database, i.e during development, we need to start by creating a database.

.. code-blcok:: bash

	$ sudo su - postgres
	(postgres) $ psql

.. code-block:: sql

    > CREATE USER test_alexa WITH PASSWORD '<password>';
    > CREATE DATABASE test_alexa OWNER test_alexa;

Database Schema Migrations
--------------------------

We use the alembic_ package to maintain migrations.


Run Migrations
~~~~~~~~~~~~~~

To migrate the DB schema to latest revision (i.e ``head``), run ``upgrade``:

.. code-block:: bash

   alembic upgrade head


Create Migration
~~~~~~~~~~~~~~~~

Create a new migration with the ``revision`` command:

.. code-block:: bash

   alembic revision --autogenerate


Development
-----------

When running code locally, start by setting up the python environment.

.. code-block:: bash

   pip install pipenv
   pipenv install

Later, prepend pipenv to any command you'd like to run. Here are some examples

.. code-block:: bash

   # make migration
   pipenv run alembic revision --autogenerate

   # run migration
   pipenv run alembic upgrade head

   # run gunicorn webserver
   pipenv run gunicorn trello_skill:wsgi

   # run debug webserver
   pipenv run python trello_skill.py

   # update alexa interaction model
   pipenv run bash update_model.sh

   # run interactive shell
   pipenv shell

.. _pipenv: https://docs.pipenv.org/
.. _ask: https://developer.amazon.com/docs/smapi/ask-cli-command-reference.html
.. _alembic: http://alembic.zzzcomputing.com/