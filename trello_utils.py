from os.path import join, dirname
from os import environ

from dotenv import load_dotenv
from trello import TrelloClient

_client = None

# TODO: use a persistant store instead of in-memory
user_token_map = {}


def get_client(api_key, token, api_secret=None, token_secret=None):
    """
    API secret / token are optional, will be used if a 3-legged
    Oauth 1.0 transaction is completed.
    """
    global _client
    if not _client:
        _client = TrelloClient(
            api_key=api_key,
            token=token,
            api_secret=api_secret,
            token_secret=token_secret
        )
    return _client


def trello_client(session):
    global user_token_map
    if not user_token_map:
        api_key, user_token_map = setup_tokens()
    assert session.user_id in user_token_map, (
        'Session.user_id "%s" was not found in token map!' % session.user_id)
    return get_client(api_key=api_key, token=user_token_map[session.user_id])


def setup_tokens():
    """ Parse env vars for user Trello board tokens """
    dotenv_path = join(dirname(__file__), '.env')
    load_dotenv(dotenv_path, verbose=True)

    api_key = environ.get('TRELLO_API_KEY')
    assert api_key, 'Missing TRELLO_API_KEY value!'
    for key, value in environ.items():
        if key.startswith('TRELLO_API_TOKEN_'):
            user_token_map[key[17:]] = value
    return api_key, user_token_map
