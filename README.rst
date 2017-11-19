Trello Helpers Alexa Skill
==========================

This skill provides some Trello commands that I found useful. It will eventually be expanded to support more commands and use cases.

**[BETA WARNING]** This is currently in heavy development; most important it currently does not support account linking, thus only interacts with 1 Trello account as defined in the environment variables (see Deployment below).

Setup Skill
-----------

Use the UI wizard to create the skill through this page:

    https://developer.amazon.com/edw/home.html#/skills

We could also create the skill with the ask_ cli tool:

.. code-block:: bash

   ask new [-n|--skill-name <name>] [-p| --profile <profile>] [--lambda-name <lambda-name>]

Updating the interaction model
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The interaction model can be found in ``model.json``. It defines the invocation name, intents and slots as well as custom types.

This file should be uploaded for each language in the Skill builder.

We can also update the model from the ask_ cli tool:

.. code-block:: bash

   ask api update-model  -f model.json -s <skill-id> -l <locale>

To update all known languages of skill with ``$SKILL_ID`` (must be set in env), use the helper script:

.. code-block:: bash

   heroku run bash update_model.sh


Deployment
----------

During development I found it easiest to use heroku, (however any host would work just as fine).

Using heroku means that dependencies are specified in the ``Pipfile`` (i.e use pipenv_),

Requirements
~~~~~~~~~~~~

- alexandra
- py-trello
- python-dotenv
- gunicorn


.. _pipenv: https://docs.pipenv.org/
.. _ask: https://developer.amazon.com/docs/smapi/ask-cli-command-reference.html