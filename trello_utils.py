from trello import TrelloClient

_client = None


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
