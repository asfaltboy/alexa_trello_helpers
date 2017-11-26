Introduction
============

This skill provides some Trello_ commands that I found useful. It will eventually be expanded to support more commands and use cases.

**[BETA WARNING]** This is currently in heavy development; most important it currently does not support account linking, thus only interacts with 1 Trello account as defined in the environment variables (see Deployment below).


Features
--------

Below listed features either implemented or planned:

- List boards
- **(TODO)** Set board as default
- **(TODO)** List available lists on board X / default board
- **(TODO)** List items in list Y on board X / default board
- **(TODO)** Account Link to Trello OAuth 1.0; see:

  - http://code-coverage.net/building-amazon-alexa-skills-with-net/
  - https://developer.amazon.com/docs/custom-skills/link-an-alexa-user-with-a-user-in-your-system.html

- **(TODO)** Integrate with Alexa TODO / Shopping lists:

  - https://developer.amazon.com/docs/custom-skills/access-the-alexa-shopping-and-to-do-lists.html

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

Personally I found it easiest to use heroku_, (however any host would work just as fine).

Using heroku_ means that dependencies are specified in the ``Pipfile`` (i.e use pipenv_), and certain environment variables must be set in ``heroku config``.


Requirements
------------

The project was developed using new features from Python 3.6, so this is the only supported version, and there are no plans to backport.

- alexandra_
- py-trello_
- python-dotenv_
- gunicorn_
- SQLAlchemy_
- alembic_
- psycopg2_

Environment Variables
---------------------

Configure at least the values below as required:

- ``TRELLO_API_KEY``: Trello API application key
- ``SKILL_ID``: which skill to update when running ``update_models.py``
- ``DATABASE_URL``: Database DMN

To find your ``TRELLO_API_KEY`` visit https://trello.com/app-key

For the ``SKILL_ID``, visit your alexa skill page at https://developer.amazon.com/edw/home.html

``DATABASE_URL`` is normally set by heroku-postgres_ addon in a deployed environment. In development, we default to ``sqlite:///alexa_trello_skill.db`` if the variable is unset.
Change this to whatever DB or driver you want to run. Follow the `SQLAlchemy url documentation`_ to learn more.

Database Setup
==============

Certain information, such as tokens and other user preferences, needs to be stored persistently. The data requirements should be pretty modest, thus a free tier Heroku Postgres addon instance should suffice.

Create Database
---------------

When managing our own database, i.e during development, we need to start by creating a database.

.. code-block:: bash

	$ sudo su - postgres
	(postgres) $ psql

.. code-block:: sql

    > CREATE USER test_alexa WITH PASSWORD '<password>';
    > CREATE DATABASE test_alexa OWNER test_alexa;

Database Schema Migrations
--------------------------

We use the alembic_ package to maintain migrations. Here are some common commands we normally need to run.

Run Migrations
~~~~~~~~~~~~~~

To migrate the DB schema to latest revision (i.e ``head``), run ``upgrade``:

.. code-block:: bash

   heroku run alembic upgrade head


Create Migration
~~~~~~~~~~~~~~~~

Create a new migration with the ``revision`` command:

.. code-block:: bash

   alembic revision --autogenerate


Add a Trello token for an alexa user to the Database
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

We have yet to implement the authentication link to allow alexa users to connect the skill to Trello OAuth 1.0. Thus, we need to manually add users to the application to be able to access a Trello account.

This is easy to done in shell:

.. code-block:: bash

   # open interactive python shell (if in dev)
   pipenv run ipython

   # Or, if in production, use heroku's python
   heroku run python

.. code-block:: python

   >>> from trello_skill.utils import trello_client, save_user_token, setup_tokens
   >>> user_id = 'amzn1.ask.account.AABBCC...'  # your alexa ID

   >>> # Check if token for user already saved
   >>> client = trello_client(user_id=user_id)
   AssertionError: User "amzn1.ask.account.AABBCC..." has no known token (OAuth not yet implemented)!

   >>> # if the error is raised, we need to save it
   >>> token = '4534534...'
   >>> api_key, token_map = setup_tokens()
   >>> save_user_token(user_id, api_key, token)

Development
-----------

Using dotenv with a ``.env`` file
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Create a ``.env`` file with e.g the following, to easily populate the command's environment when running locally:

.. code-block:: bash

   SKILL_ID=<your-alexa-skill-ID>  # obtain in skill mgmt page
   DATABASE_URL=<DMN-to-local-DB-instance>
   TRELLO_API_KEY=<a-trello-API-key>


Using ``pipenv``
~~~~~~~~~~~~~~~~

When running code locally, start by setting up the python environment.

.. code-block:: bash

   pip install pipenv
   pipenv install -d  # install addl packages e.g ipython

The above command may offer to install python 3.6.2 if it's not currently installed and your system has pyenv_.

Later, prepend pipenv to any command you'd like to run. Here are some examples

.. code-block:: bash

   # if you didn't install the package in editable mode, set your python path
   export PYTHONPATH=.

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

   # run interactive sysmtem shell
   pipenv shell

   # run interactive python shell (if dev deps installed)
   pipenv run ipython

.. _Trello: https://trello.com
.. _alexandra: https://github.com/erik/alexandra
.. _py-trello: https://github.com/sarumont/py-trello
.. _python-dotenv: https://github.com/theskumar/python-dotenv
.. _gunicorn: http://gunicorn.org/
.. _SQLAlchemy: http://www.sqlalchemy.org/
.. _psycopg2: http://initd.org/psycopg/
.. _pipenv: https://docs.pipenv.org/
.. _ask: https://developer.amazon.com/docs/smapi/ask-cli-command-reference.html
.. _alembic: http://alembic.zzzcomputing.com/
.. _pyenv: https://github.com/pyenv/pyenv
.. _heroku: https://www.heroku.com
.. _heroku-postgres: https://www.heroku.com/postgres
.. _SQLAlchemy url documentation: http://docs.sqlalchemy.org/en/latest/core/engines.html#database-urls