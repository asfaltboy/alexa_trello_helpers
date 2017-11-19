from os.path import join, dirname
from os import environ

from dotenv import load_dotenv
import alexandra

alex = alexandra.Application()
wsgi = alex.create_wsgi_app()
token_map = {}


@alex.intent("ListBoards")
def list_boards_intent(slots, session):
    if not token_map:
        setup_tokens()
    assert session.user_id in token_map, (
        'Session.user_id "%s" was not found in token map!' % session.user_id)
    return alex.respond("Listing your boards")


def setup_tokens():
    """ Parse env vars for user Trello board tokens """
    dotenv_path = join(dirname(__file__), '.env')
    load_dotenv(dotenv_path, verbose=True)

    api_key = environ.get('TRELLO_API_KEY')
    assert api_key, 'Missing TRELLO_API_KEY value!'
    for key, value in environ.items():
        if key.startswith('TRELLO_API_TOKEN_'):
            token_map[key[17:]] = value


if __name__ == '__main__':
    setup_tokens()
    alex.run('127.0.0.1', 8080, debug=True)
