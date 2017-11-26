from os.path import join, dirname
from os import environ

from dotenv import load_dotenv
from trello import TrelloClient

from .models import AlexaUser, TrelloUser

_client = None
_api_key = _user_token_map = None


def get_client(api_key, token, api_secret=None, token_secret=None):
    """
    API secret / token are optional, will be used if a 3-legged
    Oauth 1.0 transaction is completed.
    """
    global _client
    if _client is None:
        _client = TrelloClient(
            api_key=api_key,
            token=token,
            api_secret=api_secret,
            token_secret=token_secret
        )
    return _client


def trello_client(user_id):
    """ Retreive the authenticated Trello API client """
    api_key, token_map = setup_tokens()
    if user_id in token_map:
        token = token_map[user_id]
    else:
        token = retreive_user_token(user_id)
        if token:
            token_map[user_id] = token
    assert token, (
        f'User "{user_id}" has no known token (OAuth not yet implemented)!')
    return get_client(api_key=api_key, token=token)


def setup_tokens():
    """ Parse env vars and query DB for user Trello board tokens """
    global _user_token_map, _api_key
    if _api_key is None:
        _api_key = environ.get('TRELLO_API_KEY')
        assert _api_key, 'Missing TRELLO_API_KEY value!'

    if _user_token_map is None:
        # optional initial "cache" population skips a DB query
        _user_token_map = {}
        dotenv_path = join(dirname(__file__), '.env')
        load_dotenv(dotenv_path, verbose=True)

        for key, value in environ.items():
            if key.startswith('TRELLO_API_TOKEN_'):
                _user_token_map[key[17:]] = value
    return _api_key, _user_token_map


def get_or_create_user(user_id):
    """
    Retreive an Alexa user matching the given user_id.

    Creates the user record if it does not yet exist.
    """
    assert user_id, f'Invalid `user_id` "{user_id}"'
    user = AlexaUser.get_user(user_id)
    if not user:
        user = AlexaUser(user_id).save()
    return user


def get_trello_user(alexa_user_id):
    """
    Retreive a Trello user matching an Alexa user with the given user_id.
    """
    assert alexa_user_id, f'Invalid `alexa_user_id` "{alexa_user_id}"'
    user = TrelloUser.get_user(alexa_user_id)
    assert user, f'No TrelloUser found for AlexaUser with id {alexa_user_id}'
    return user


def retreive_user_token(user_id):
    """
    Retreive a Trello token for an Alexa user with given user_id

    Returns None if user is no matching token is found.
    """
    user = get_or_create_user(user_id)
    if user.trello_user:
        return user.trello_user.auth_token
    return None


def save_user_token(user_id, api_key, token):
    """
    Save the given api_key and token to a TrelloUser related to the
    AlexaUser record matching the igiven user_id
    """
    assert api_key and token, f'Invalid key / token: {api_key} / {token}'

    user = get_or_create_user(user_id)
    if not user.trello_user:
        user.trello_user = TrelloUser(
            auth_api_key=api_key,
            auth_token=token).save()
        user.save()
    else:
        user.trello_user.auth_api_key = api_key
        user.trello_user.auth_token = token
        user.trello_user.save()
